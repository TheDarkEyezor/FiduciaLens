"""
FiduciaLens Backend API
Provides credit scoring and signed attestations with concurrent request handling
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from algosdk.v2client import algod, indexer
from datetime import datetime, timedelta
import hashlib
import hmac
import json
import os
import random
import asyncio
import threading
from typing import Optional, List
from queue import Queue
from collections import defaultdict

# Import document verification
from document_verification import (
    upload_document,
    get_document_info,
    get_available_document_types,
    calculate_total_document_boost,
    VerificationRequest,
    VerificationResponse,
    DocumentType
)

app = FastAPI(title="FiduciaLens API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Thread-safe WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self._lock = threading.Lock()  # Thread safety for connection list
        self._broadcast_queue = Queue()  # Queue for broadcast messages
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        with self._lock:
            self.active_connections.append(websocket)
        print(f"🔌 New WebSocket connection. Total: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        with self._lock:
            if websocket in self.active_connections:
                self.active_connections.remove(websocket)
        print(f"🔌 WebSocket disconnected. Total: {len(self.active_connections)}")
    
    async def broadcast(self, message: dict):
        """Thread-safe broadcast message to all connected clients"""
        with self._lock:
            connections = self.active_connections.copy()  # Safe copy
        
        disconnected = []
        for connection in connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"⚠️ Failed to send to client: {e}")
                disconnected.append(connection)
        
        # Clean up disconnected clients
        for connection in disconnected:
            self.disconnect(connection)
    
    def queue_broadcast(self, message: dict):
        """Queue a message for broadcast (thread-safe)"""
        self._broadcast_queue.put(message)
    
    async def process_broadcast_queue(self):
        """Process queued broadcast messages"""
        while True:
            try:
                # Non-blocking check for queued messages
                if not self._broadcast_queue.empty():
                    message = self._broadcast_queue.get_nowait()
                    await self.broadcast(message)
            except Exception as e:
                print(f"⚠️ Broadcast queue error: {e}")
            await asyncio.sleep(0.1)  # Small delay to prevent CPU spinning

manager = ConnectionManager()

# Thread-safe cache for frequently accessed data
class ThreadSafeCache:
    def __init__(self, ttl_seconds=30):
        self._cache = {}
        self._lock = threading.Lock()
        self._ttl = ttl_seconds
    
    def get(self, key: str):
        with self._lock:
            if key in self._cache:
                value, timestamp = self._cache[key]
                if datetime.now() - timestamp < timedelta(seconds=self._ttl):
                    return value
                else:
                    del self._cache[key]
            return None
    
    def set(self, key: str, value):
        with self._lock:
            self._cache[key] = (value, datetime.now())
    
    def invalidate(self, key: str):
        with self._lock:
            if key in self._cache:
                del self._cache[key]

# Caches with 30-second TTL
credit_score_cache = ThreadSafeCache(ttl_seconds=30)
pool_stats_cache = ThreadSafeCache(ttl_seconds=10)
user_stats_cache = ThreadSafeCache(ttl_seconds=15)

# Configuration
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
INDEXER_ADDRESS = "https://testnet-idx.algonode.cloud"
ALGOD_TOKEN = ""
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")

# Initialize clients
algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)
indexer_client = indexer.IndexerClient(ALGOD_TOKEN, INDEXER_ADDRESS)

# Models
class CreditScoreRequest(BaseModel):
    address: str

class CreditScoreResponse(BaseModel):
    address: str
    score: int
    factors: dict
    timestamp: str
    signature: str

class PoolStatsResponse(BaseModel):
    total_collateral: int
    total_borrow: int
    utilization_rate: float
    num_users: int

class UserStatsRequest(BaseModel):
    address: str
    app_id: int

class UserStatsResponse(BaseModel):
    collateral: int
    debt: int
    credit_score: int
    max_borrow: int
    accrued_interest: int = 0
    total_debt_with_interest: int = 0
    last_interest_update: int = 0

class MockOraclePriceResponse(BaseModel):
    asset: str
    price_usd: float
    timestamp: str
    change_24h: float
    source: str
    confidence: float
    volatility: float

# Helper functions
def calculate_credit_score(address: str) -> tuple[int, dict]:
    """
    Enhanced credit score calculation with multiple sophisticated factors
    Returns: (score, factors_dict)
    """
    try:
        # Fetch account info
        account_info = algod_client.account_info(address)
        
        # Fetch transaction history
        txns = indexer_client.search_transactions_by_address(
            address=address,
            limit=1000
        )
        
        # Initialize scoring factors with points breakdown
        factors = {
            "wallet_age_days": 0,
            "wallet_age_points": 0,
            "total_transactions": 0,
            "transaction_points": 0,
            "account_balance": 0,
            "balance_points": 0,
            "apps_opted_in": 0,
            "app_participation_points": 0,
            "asset_diversity": 0,
            "asset_diversity_points": 0,
            "transaction_velocity": 0,
            "velocity_points": 0,
            "payment_consistency": 0,
            "consistency_points": 0,
        }
        
        # 1. Calculate wallet age (based on first transaction)
        if txns.get('transactions'):
            first_txn = txns['transactions'][-1]
            first_txn_time = first_txn.get('round-time', 0)
            wallet_age_days = (datetime.now().timestamp() - first_txn_time) / 86400
            factors["wallet_age_days"] = int(wallet_age_days)
            # Wallet age: up to 15 points (max at 365 days)
            factors["wallet_age_points"] = min(15, (wallet_age_days / 365) * 15)
        
        # 2. Transaction metrics
        total_txns = len(txns.get('transactions', []))
        factors["total_transactions"] = total_txns
        # Transaction history: up to 20 points (max at 100 txns)
        factors["transaction_points"] = min(20, (total_txns / 100) * 20)
        
        # 3. Account balance (in microALGOs)
        balance = account_info.get('amount', 0)
        factors["account_balance"] = balance
        # Account balance: up to 20 points (max at 100 ALGO)
        factors["balance_points"] = min(20, (balance / 100_000_000) * 20)
        
        # 4. Apps opted into (DeFi participation)
        apps_count = len(account_info.get('apps-local-state', []))
        factors["apps_opted_in"] = apps_count
        # App participation: up to 15 points (max at 5 apps)
        factors["app_participation_points"] = min(15, (apps_count / 5) * 15)
        
        # 5. Asset diversity (unique ASAs held)
        assets = account_info.get('assets', [])
        asset_count = len(assets)
        factors["asset_diversity"] = asset_count
        # Asset diversity: up to 10 points (max at 10 different assets)
        factors["asset_diversity_points"] = min(10, (asset_count / 10) * 10)
        
        # 6. Transaction velocity (recent activity)
        # Count transactions in last 30 days
        thirty_days_ago = datetime.now().timestamp() - (30 * 86400)
        recent_txns = [
            txn for txn in txns.get('transactions', [])
            if txn.get('round-time', 0) > thirty_days_ago
        ]
        txns_per_day = len(recent_txns) / 30 if recent_txns else 0
        factors["transaction_velocity"] = round(txns_per_day, 2)
        # Velocity: up to 10 points (max at 3 txns/day)
        factors["velocity_points"] = min(10, (txns_per_day / 3) * 10)
        
        # 7. Payment consistency (regularity of transactions)
        # Higher score for consistent activity over time
        if total_txns >= 5:
            # Calculate time gaps between transactions
            time_gaps = []
            for i in range(len(txns.get('transactions', [])) - 1):
                t1 = txns['transactions'][i].get('round-time', 0)
                t2 = txns['transactions'][i + 1].get('round-time', 0)
                if t1 and t2:
                    time_gaps.append(abs(t1 - t2))
            
            if time_gaps:
                # Lower standard deviation = more consistent
                import statistics
                avg_gap = statistics.mean(time_gaps)
                std_gap = statistics.stdev(time_gaps) if len(time_gaps) > 1 else avg_gap
                consistency_ratio = 1 - min(1, std_gap / avg_gap) if avg_gap > 0 else 0
                factors["payment_consistency"] = round(consistency_ratio * 100, 1)
                # Consistency: up to 10 points
                factors["consistency_points"] = consistency_ratio * 10
        
        # Calculate total score (0-100 base)
        base_score = (
            factors["wallet_age_points"] +
            factors["transaction_points"] +
            factors["balance_points"] +
            factors["app_participation_points"] +
            factors["asset_diversity_points"] +
            factors["velocity_points"] +
            factors["consistency_points"]
        )
        
        # Scale to traditional credit score range (300-850)
        # Formula: 300 + (base_score / 100) * 550
        # 0 points → 300, 100 points → 850
        scaled_score = 300 + int((base_score / 100) * 550)
        
        # Round all point values
        for key in factors:
            if key.endswith('_points'):
                factors[key] = round(factors[key], 1)
        
        # Add base_score to factors for transparency
        factors["base_score"] = round(base_score, 1)
        factors["scaled_score"] = scaled_score
        
        return scaled_score, factors
        
    except Exception as e:
        print(f"Error calculating credit score: {e}")
        import traceback
        traceback.print_exc()
        # Return minimal score on error
        return 0, {
            "wallet_age_days": 0,
            "wallet_age_points": 0,
            "total_transactions": 0,
            "transaction_points": 0,
            "account_balance": 0,
            "balance_points": 0,
            "apps_opted_in": 0,
            "app_participation_points": 0,
            "asset_diversity": 0,
            "asset_diversity_points": 0,
            "transaction_velocity": 0,
            "velocity_points": 0,
            "payment_consistency": 0,
            "consistency_points": 0,
            "error": str(e)
        }

def sign_attestation(data: dict) -> str:
    """
    Create HMAC signature for attestation
    In production, use asymmetric signatures (Ed25519)
    """
    message = json.dumps(data, sort_keys=True)
    signature = hmac.new(
        SECRET_KEY.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    return signature

def verify_signature(data: dict, signature: str) -> bool:
    """Verify attestation signature"""
    expected = sign_attestation(data)
    return hmac.compare_digest(expected, signature)

# API Endpoints
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "FiduciaLens API",
        "status": "operational",
        "version": "1.0.0"
    }

@app.post("/api/credit-score", response_model=CreditScoreResponse)
async def get_credit_score(request: CreditScoreRequest):
    """
    Calculate and return signed credit score for an address (with caching and document boosts)
    """
    if not request.address:
        raise HTTPException(status_code=400, detail="Address is required")
    
    # Check cache first
    cache_key = f"credit:{request.address}"
    cached_result = credit_score_cache.get(cache_key)
    if cached_result:
        print(f"📦 Cache hit for {request.address[:8]}...")
        return cached_result
    
    # Calculate base score
    base_score, factors = calculate_credit_score(request.address)
    
    # Add document verification boost
    document_boost = calculate_total_document_boost(request.address)
    
    # Calculate final score (capped at 850)
    final_score = min(850, base_score + document_boost)
    
    # Add document boost to factors dict
    if document_boost > 0:
        factors["document_boost"] = document_boost
        factors["document_boost_points"] = document_boost
    
    # Create attestation with final score
    timestamp = datetime.now().isoformat()
    expiry = (datetime.now() + timedelta(hours=24)).isoformat()
    
    attestation_data = {
        "address": request.address,
        "score": final_score,  # Use final score with boosts
        "timestamp": timestamp,
        "expiry": expiry
    }
    
    # Sign attestation
    signature = sign_attestation(attestation_data)
    
    result = CreditScoreResponse(
        address=request.address,
        score=final_score,  # Return final score with document boosts
        factors=factors,
        timestamp=timestamp,
        signature=signature
    )
    
    # Cache the result
    credit_score_cache.set(cache_key, result)
    
    return result

@app.post("/api/verify-attestation")
async def verify_attestation_endpoint(
    address: str,
    score: int,
    timestamp: str,
    expiry: str,
    signature: str
):
    """Verify a credit score attestation"""
    data = {
        "address": address,
        "score": score,
        "timestamp": timestamp,
        "expiry": expiry
    }
    
    # Check signature
    is_valid = verify_signature(data, signature)
    
    # Check expiry
    is_expired = datetime.fromisoformat(expiry) < datetime.now()
    
    return {
        "valid": is_valid and not is_expired,
        "signature_valid": is_valid,
        "expired": is_expired
    }

@app.get("/api/pool-stats/{app_id}", response_model=PoolStatsResponse)
async def get_pool_stats(app_id: int):
    """Get lending pool statistics"""
    try:
        app_info = algod_client.application_info(app_id)
        global_state = app_info.get('params', {}).get('global-state', [])
        
        # Parse global state
        stats = {}
        for item in global_state:
            key = item.get('key', '')
            value = item.get('value', {})
            
            # Decode base64 key
            import base64
            decoded_key = base64.b64decode(key).decode('utf-8')
            
            if value.get('type') == 1:  # uint
                stats[decoded_key] = value.get('uint', 0)
        
        total_collateral = stats.get('TotalCollateral', 0)
        total_borrow = stats.get('TotalBorrow', 0)
        
        utilization_rate = (total_borrow / total_collateral * 100) if total_collateral > 0 else 0
        
        return PoolStatsResponse(
            total_collateral=total_collateral,
            total_borrow=total_borrow,
            utilization_rate=round(utilization_rate, 2),
            num_users=0  # Would need to track this separately
        )
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Application not found: {str(e)}")

@app.post("/api/user-stats", response_model=UserStatsResponse)
async def get_user_stats(request: UserStatsRequest):
    """Get user's lending statistics (with interest calculation)"""
    try:
        account_info = algod_client.account_info(request.address)
        
        # Find local state for this app
        local_state = {}
        for app in account_info.get('apps-local-state', []):
            if app.get('id') == request.app_id:
                for item in app.get('key-value', []):
                    import base64
                    key = base64.b64decode(item.get('key', '')).decode('utf-8')
                    value = item.get('value', {})
                    if value.get('type') == 1:
                        local_state[key] = value.get('uint', 0)
                break
        
        collateral = local_state.get('Collateral', 0)
        debt = local_state.get('Debt', 0)
        credit_score = local_state.get('CreditScore', 0)
        last_update = local_state.get('LastInterestUpdate', 0)
        
        # Calculate accrued interest (5% APR simple)
        accrued_interest = 0
        if debt > 0 and last_update > 0:
            import time
            current_time = int(time.time())
            seconds_elapsed = current_time - last_update
            # Interest = Principal * Rate * Time
            # Rate: 5% per year, Time: seconds / seconds_in_year
            accrued_interest = (debt * seconds_elapsed) // 630720000
        
        total_debt_with_interest = debt + accrued_interest
        
        # Calculate max borrow based on LTV
        base_ltv = 50
        adjusted_ltv = base_ltv + 10 if credit_score >= 70 else base_ltv
        max_borrow = (collateral * adjusted_ltv) // 100
        
        return UserStatsResponse(
            collateral=collateral,
            debt=debt,
            credit_score=credit_score,
            max_borrow=max_borrow,
            accrued_interest=accrued_interest,
            total_debt_with_interest=total_debt_with_interest,
            last_interest_update=last_update
        )
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"User stats not found: {str(e)}")

# Global state for price simulation (persists across requests)
_price_state = {
    "base_price": 0.18,  # ALGO base price in USD
    "current_price": 0.18,
    "last_update": datetime.now(),
    "price_history": []
}

@app.get("/api/mock-price", response_model=MockOraclePriceResponse)
async def get_mock_price():
    """
    Mock Oracle Price Feed - Simulates real-time ALGO price data
    Uses random walk algorithm to simulate realistic price movements
    """
    global _price_state
    
    # Constants
    BASE_PRICE = _price_state["base_price"]
    VOLATILITY = 0.05  # 5% max change per update
    MEAN_REVERSION = 0.1  # Tendency to return to base price
    
    # Calculate time since last update
    now = datetime.now()
    time_diff = (now - _price_state["last_update"]).total_seconds()
    
    # Generate price movement (random walk with mean reversion)
    # Random component: -VOLATILITY to +VOLATILITY
    random_change = random.uniform(-VOLATILITY, VOLATILITY)
    
    # Mean reversion component: pull back toward base price
    current_deviation = (_price_state["current_price"] - BASE_PRICE) / BASE_PRICE
    reversion_force = -current_deviation * MEAN_REVERSION
    
    # Combine forces
    total_change = random_change + reversion_force
    
    # Apply change
    new_price = _price_state["current_price"] * (1 + total_change)
    
    # Ensure price stays within reasonable bounds (±30% of base)
    new_price = max(BASE_PRICE * 0.7, min(BASE_PRICE * 1.3, new_price))
    
    # Calculate 24h change (compare to base price as proxy)
    change_24h = ((new_price - BASE_PRICE) / BASE_PRICE) * 100
    
    # Update state
    _price_state["current_price"] = new_price
    _price_state["last_update"] = now
    
    # Add to history (keep last 100 prices)
    _price_state["price_history"].append({
        "price": new_price,
        "timestamp": now.isoformat()
    })
    if len(_price_state["price_history"]) > 100:
        _price_state["price_history"].pop(0)
    
    # Calculate volatility from recent history (last 10 prices)
    recent_prices = [p["price"] for p in _price_state["price_history"][-10:]]
    if len(recent_prices) > 1:
        price_volatility = (max(recent_prices) - min(recent_prices)) / BASE_PRICE
    else:
        price_volatility = 0.01
    
    # Generate confidence score (higher when less volatile)
    confidence = max(0.90, min(1.0, 1.0 - price_volatility))
    
    return MockOraclePriceResponse(
        asset="ALGO",
        price_usd=round(new_price, 4),
        timestamp=now.isoformat(),
        change_24h=round(change_24h, 2),
        source="mock_oracle",
        confidence=round(confidence, 4),
        volatility=round(price_volatility * 100, 2)  # As percentage
    )

@app.get("/api/mock-price/history")
async def get_price_history(limit: int = 50):
    """Get recent price history"""
    history = _price_state["price_history"][-limit:]
    return {
        "asset": "ALGO",
        "base_price": _price_state["base_price"],
        "current_price": _price_state["current_price"],
        "history": history
    }

@app.post("/api/mock-price/reset")
async def reset_mock_price():
    """Reset price to base value (for testing)"""
    global _price_state
    _price_state["current_price"] = _price_state["base_price"]
    _price_state["price_history"] = []
    _price_state["last_update"] = datetime.now()
    return {"message": "Price reset to base", "price": _price_state["base_price"]}

@app.get("/api/price-anomaly-check")
async def check_price_anomaly():
    """
    Compare Mock Oracle price with real market data to detect anomalies
    Returns deviation percentage and alert level
    """
    mock_price = _price_state["current_price"]
    
    # Simulate "real market price" from Algorand Indexer or external sources
    # For demo purposes, we'll use a slightly different value with some noise
    import random
    # Real price simulated as base price +/- 5% random variation
    real_market_price = _price_state["base_price"] * (1 + random.uniform(-0.05, 0.05))
    
    # Calculate deviation percentage
    deviation = abs((mock_price - real_market_price) / real_market_price) * 100
    
    # Determine alert level
    if deviation < 3:
        alert_level = "normal"
        alert_color = "green"
        alert_message = "Prices are aligned within acceptable range"
    elif deviation < 5:
        alert_level = "warning"
        alert_color = "yellow"
        alert_message = "Minor price deviation detected - monitor closely"
    else:
        alert_level = "critical"
        alert_color = "red"
        alert_message = "Significant price anomaly detected - potential oracle manipulation"
    
    return {
        "mock_oracle_price": round(mock_price, 4),
        "market_price": round(real_market_price, 4),
        "deviation_percent": round(deviation, 2),
        "alert_level": alert_level,
        "alert_color": alert_color,
        "alert_message": alert_message,
        "timestamp": datetime.now().isoformat(),
        "is_healthy": deviation < 3
    }

# ==========================================
# DOCUMENT VERIFICATION ENDPOINTS
# ==========================================

@app.post("/api/documents/upload", response_model=VerificationResponse)
async def upload_document_endpoint(request: VerificationRequest):
    """
    Upload a document for verification
    
    **Supported Documents:**
    - Passport (+100 points)
    - Driver's License (+80 points)
    - Tax Return (+70 points)
    - Bank Statement (+60 points)
    - Employment Letter (+50 points)
    - Utility Bill (+40 points)
    """
    try:
        result = upload_document(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents/{wallet_address}")
async def get_documents(wallet_address: str):
    """Get all verified documents and total credit boost for a wallet"""
    try:
        doc_info = get_document_info(wallet_address)
        return doc_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/documents/types")
async def get_document_types():
    """Get all available document types and their credit score boost ranges"""
    try:
        types = get_available_document_types()
        # Calculate total possible boost (using max values)
        total_possible = sum(boost_info["max_boost"] for boost_info in types.values())
        
        return {
            "document_types": types,
            "total_possible_boost": total_possible,
            "description": {
                "passport": "International travel document (80-120 pts, signed: higher)",
                "drivers_license": "Government-issued photo ID (60-100 pts, signed: higher)",
                "bank_statement": "Proof of financial stability (45-75 pts, signed: higher)",
                "utility_bill": "Proof of residence (30-50 pts, signed: higher)",
                "employment_letter": "Proof of employment (40-65 pts, signed: higher)",
                "tax_return": "Government tax filing (55-90 pts, signed: higher)"
            },
            "note": "Signed documents from verified issuers receive boosts in the upper range"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/credit-score/{wallet_address}/with-documents")
async def get_credit_score_with_documents(wallet_address: str):
    """
    Get credit score with document verification boost included
    """
    try:
        # Get base credit score
        request = CreditScoreRequest(address=wallet_address)
        base_score_response = await get_credit_score(request)
        base_score = base_score_response.score
        
        # Get document boost
        document_boost = calculate_total_document_boost(wallet_address)
        doc_info = get_document_info(wallet_address)
        
        # Calculate final score (capped at 850)
        final_score = min(850, base_score + document_boost)
        
        return {
            "base_score": base_score,
            "document_boost": document_boost,
            "final_score": final_score,
            "verified_documents": doc_info["verified_count"],
            "documents": doc_info["documents"],
            "factors": base_score_response.factors
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# WEBSOCKET ENDPOINTS
# ==========================================

@app.websocket("/ws/pool-state/{app_id}")
async def websocket_pool_state(websocket: WebSocket, app_id: int):
    """
    WebSocket endpoint for real-time pool state updates
    Polls the Algorand blockchain every 5 seconds and pushes updates to connected clients
    """
    await manager.connect(websocket)
    print(f"🔌 Client connected to pool state stream for App ID: {app_id}")
    
    last_state = None
    error_count = 0
    
    try:
        while True:
            try:
                # Fetch current pool state from blockchain
                app_info = algod_client.application_info(app_id)
                global_state = app_info.get('params', {}).get('global-state', [])
                
                # Parse global state
                stats = {}
                for item in global_state:
                    key = item.get('key', '')
                    value = item.get('value', {})
                    
                    # Decode base64 key
                    import base64
                    decoded_key = base64.b64decode(key).decode('utf-8')
                    
                    if value.get('type') == 1:  # uint
                        stats[decoded_key] = value.get('uint', 0)
                
                # Build current state snapshot
                current_state = {
                    "total_collateral": stats.get('TotalCollateral', 0),
                    "total_borrow": stats.get('TotalBorrow', 0),
                    "max_ltv": stats.get('MaxLTV', 50),
                }
                
                # Only send update if state changed
                if current_state != last_state:
                    message = {
                        "type": "pool_update",
                        "app_id": app_id,
                        "data": current_state,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    await websocket.send_json(message)
                    print(f"📡 Pool state update sent - Collateral: {current_state['total_collateral']}, Borrowed: {current_state['total_borrow']}")
                    
                    last_state = current_state
                    error_count = 0  # Reset error count on success
                
            except Exception as e:
                error_count += 1
                print(f"❌ Error fetching pool state (attempt {error_count}): {e}")
                
                # If too many errors, disconnect
                if error_count > 10:
                    print(f"🚨 Too many errors, closing connection")
                    break
            
            # Poll every 5 seconds
            await asyncio.sleep(5)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        print(f"🔌 Client disconnected from pool {app_id}")
    except Exception as e:
        print(f"❌ WebSocket error: {e}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting FiduciaLens API Server")
    print("📊 Concurrent workers: 4")
    print("🔒 Thread-safe caching enabled")
    print("📡 WebSocket broadcast queue active")
    print("=" * 60)
    
    # Run with 4 worker processes for concurrency
    # Each worker can handle multiple requests simultaneously
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,  # 4 worker processes for concurrent request handling
        reload=False,  # Disable reload in production
        access_log=True,
        log_level="info"
    )
