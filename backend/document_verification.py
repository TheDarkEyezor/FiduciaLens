"""
Document Verification System for FiduciaLens
Allows users to upload identity documents to boost their credit score
"""

from enum import Enum
from typing import Dict, Optional
from datetime import datetime
from pydantic import BaseModel
import hashlib
import base64
import random
import hmac

class DocumentType(str, Enum):
    """Supported document types"""
    PASSPORT = "passport"
    DRIVERS_LICENSE = "drivers_license"
    BANK_STATEMENT = "bank_statement"
    UTILITY_BILL = "utility_bill"
    EMPLOYMENT_LETTER = "employment_letter"
    TAX_RETURN = "tax_return"

class DocumentStatus(str, Enum):
    """Document verification status"""
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"

class VerificationRequest(BaseModel):
    """Request model for document verification"""
    wallet_address: str
    document_type: DocumentType
    document_data: str  # Base64 encoded document
    filename: str
    issuer_signature: Optional[str] = None  # Cryptographic signature from issuing authority
    issuer_id: Optional[str] = None  # ID of issuing authority (bank, government, etc.)

class VerificationResponse(BaseModel):
    """Response model for document verification"""
    success: bool
    document_id: str
    status: DocumentStatus
    credit_score_boost: int
    message: str
    verified_at: Optional[str] = None
    signature_valid: Optional[bool] = None

class Document(BaseModel):
    """Document model for storage"""
    document_id: str
    wallet_address: str
    document_type: DocumentType
    status: DocumentStatus
    credit_score_boost: int
    uploaded_at: str
    verified_at: Optional[str] = None
    filename: str
    document_hash: str  # SHA256 hash for integrity
    issuer_signature: Optional[str] = None
    issuer_id: Optional[str] = None
    signature_valid: bool = False

# In-memory storage (replace with database in production)
documents_store: Dict[str, Dict[str, Document]] = {}

# Credit score boost ranges for each document type (min, max)
# Randomized to simulate real document evaluation
CREDIT_SCORE_BOOST_RANGES = {
    DocumentType.PASSPORT: (80, 120),  # Government-issued ID gets highest boost
    DocumentType.DRIVERS_LICENSE: (60, 100),
    DocumentType.BANK_STATEMENT: (45, 75),
    DocumentType.UTILITY_BILL: (30, 50),
    DocumentType.EMPLOYMENT_LETTER: (40, 65),
    DocumentType.TAX_RETURN: (55, 90),
}

# Trusted issuer IDs (in production, this would be a database of verified institutions)
TRUSTED_ISSUERS = {
    "US_GOVT_PASSPORT": "United States Passport Agency",
    "US_DMV": "Department of Motor Vehicles",
    "CHASE_BANK": "JPMorgan Chase Bank",
    "BOA": "Bank of America",
    "WELLS_FARGO": "Wells Fargo",
    "IRS": "Internal Revenue Service",
    "UTIL_COMPANY": "Utility Provider",
    # Demo issuers for testing
    "DEMO_BANK": "Demo Bank (Test)",
    "DEMO_GOVT": "Demo Government (Test)",
}

def verify_issuer_signature(document_hash: str, issuer_id: str, signature: str) -> bool:
    """
    Verify cryptographic signature from document issuer
    
    In production, this would:
    1. Look up issuer's public key from trusted registry
    2. Verify signature using public key cryptography (RSA, ECDSA)
    3. Check certificate validity and revocation status
    
    For demo, we simulate signature verification:
    - Accept signatures from known issuers
    - Verify HMAC-based signature for demo purposes
    """
    if not issuer_id or not signature:
        return False
    
    # Check if issuer is trusted
    if issuer_id not in TRUSTED_ISSUERS:
        return False
    
    # For demo: simulate signature verification
    # In production: use actual public key verification
    expected_signature = hmac.new(
        issuer_id.encode(),
        document_hash.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Accept either the HMAC signature or a demo signature format
    return (
        signature == expected_signature or
        signature.startswith("SIG_") or  # Demo signature format
        signature == f"DEMO_{issuer_id}_{document_hash[:8]}"  # Test signature
    )

def calculate_variable_boost(document_type: DocumentType, has_valid_signature: bool) -> int:
    """
    Calculate credit score boost with randomization to simulate document evaluation
    
    Factors that affect the boost:
    - Document type (different ranges)
    - Signature validity (signed documents get higher boost)
    - Random variation (simulates manual review quality assessment)
    """
    min_boost, max_boost = CREDIT_SCORE_BOOST_RANGES[document_type]
    
    if has_valid_signature:
        # Signed documents get boosts in upper 70-100% of range
        min_adjusted = int(min_boost + (max_boost - min_boost) * 0.7)
        boost = random.randint(min_adjusted, max_boost)
    else:
        # Unsigned documents get boosts in lower 40-70% of range
        max_adjusted = int(min_boost + (max_boost - min_boost) * 0.7)
        boost = random.randint(min_boost, max_adjusted)
    
    return boost

def generate_document_id(wallet_address: str, document_type: str) -> str:
    """Generate unique document ID"""
    timestamp = datetime.now().isoformat()
    data = f"{wallet_address}_{document_type}_{timestamp}"
    return hashlib.sha256(data.encode()).hexdigest()[:16]

def calculate_document_hash(document_data: str) -> str:
    """Calculate SHA256 hash of document"""
    return hashlib.sha256(document_data.encode()).hexdigest()

def verify_document_mock(document_type: DocumentType, document_data: str) -> bool:
    """
    Mock document verification logic
    In production, this would integrate with:
    - OCR services (Google Vision, AWS Textract)
    - Identity verification APIs (Stripe Identity, Onfido, Jumio)
    - Government databases
    
    For demo purposes, we accept all documents
    """
    # Simple validation: check if document is not empty and meets size requirements
    try:
        decoded = base64.b64decode(document_data)
        # Accept documents between 1KB and 10MB
        if 1024 <= len(decoded) <= 10 * 1024 * 1024:
            return True
    except Exception:
        pass
    return False

def upload_document(request: VerificationRequest) -> VerificationResponse:
    """
    Upload and verify a document with cryptographic signature validation
    """
    try:
        # Initialize wallet storage if needed
        if request.wallet_address not in documents_store:
            documents_store[request.wallet_address] = {}
        
        # Check if document type already verified
        existing_docs = documents_store[request.wallet_address]
        if request.document_type in existing_docs:
            existing = existing_docs[request.document_type]
            if existing.status == DocumentStatus.VERIFIED:
                return VerificationResponse(
                    success=False,
                    document_id=existing.document_id,
                    status=existing.status,
                    credit_score_boost=0,
                    message=f"{request.document_type.value} already verified. Cannot verify again.",
                    verified_at=existing.verified_at,
                    signature_valid=existing.signature_valid
                )
        
        # Generate document ID and hash
        document_id = generate_document_id(request.wallet_address, request.document_type)
        document_hash = calculate_document_hash(request.document_data)
        
        # Verify document format/size (basic validation)
        is_valid = verify_document_mock(request.document_type, request.document_data)
        
        if not is_valid:
            # Create rejected document record
            document = Document(
                document_id=document_id,
                wallet_address=request.wallet_address,
                document_type=request.document_type,
                status=DocumentStatus.REJECTED,
                credit_score_boost=0,
                uploaded_at=datetime.now().isoformat(),
                filename=request.filename,
                document_hash=document_hash,
                issuer_signature=request.issuer_signature,
                issuer_id=request.issuer_id,
                signature_valid=False
            )
            documents_store[request.wallet_address][request.document_type] = document
            
            return VerificationResponse(
                success=False,
                document_id=document_id,
                status=DocumentStatus.REJECTED,
                credit_score_boost=0,
                message="Document verification failed. Invalid document format or size.",
                signature_valid=False
            )
        
        # Verify cryptographic signature if provided
        signature_valid = False
        if request.issuer_signature and request.issuer_id:
            signature_valid = verify_issuer_signature(
                document_hash,
                request.issuer_id,
                request.issuer_signature
            )
            
            if not signature_valid:
                # Reject documents with invalid signatures
                document = Document(
                    document_id=document_id,
                    wallet_address=request.wallet_address,
                    document_type=request.document_type,
                    status=DocumentStatus.REJECTED,
                    credit_score_boost=0,
                    uploaded_at=datetime.now().isoformat(),
                    filename=request.filename,
                    document_hash=document_hash,
                    issuer_signature=request.issuer_signature,
                    issuer_id=request.issuer_id,
                    signature_valid=False
                )
                documents_store[request.wallet_address][request.document_type] = document
                
                return VerificationResponse(
                    success=False,
                    document_id=document_id,
                    status=DocumentStatus.REJECTED,
                    credit_score_boost=0,
                    message=f"❌ Invalid signature from {request.issuer_id}. Document rejected.",
                    signature_valid=False
                )
        
        # Calculate variable credit boost based on document type and signature
        credit_boost = calculate_variable_boost(request.document_type, signature_valid)
        verified_time = datetime.now().isoformat()
        
        # Create verified document record
        document = Document(
            document_id=document_id,
            wallet_address=request.wallet_address,
            document_type=request.document_type,
            status=DocumentStatus.VERIFIED,
            credit_score_boost=credit_boost,
            uploaded_at=verified_time,
            verified_at=verified_time,
            filename=request.filename,
            document_hash=document_hash,
            issuer_signature=request.issuer_signature,
            issuer_id=request.issuer_id,
            signature_valid=signature_valid
        )
        
        documents_store[request.wallet_address][request.document_type] = document
        
        # Build success message
        doc_type_name = request.document_type.value.replace('_', ' ').title()
        signature_badge = "🔐" if signature_valid else "📄"
        issuer_name = TRUSTED_ISSUERS.get(request.issuer_id or "", request.issuer_id or "Unknown")
        issuer_info = f" (verified by {issuer_name})" if signature_valid and request.issuer_id else ""
        
        message = f"{signature_badge} {doc_type_name} verified{issuer_info}! +{credit_boost} credit score boost."
        
        return VerificationResponse(
            success=True,
            document_id=document_id,
            status=DocumentStatus.VERIFIED,
            credit_score_boost=credit_boost,
            message=message,
            verified_at=verified_time,
            signature_valid=signature_valid
        )
        
    except Exception as e:
        return VerificationResponse(
            success=False,
            document_id="",
            status=DocumentStatus.REJECTED,
            credit_score_boost=0,
            message=f"Error processing document: {str(e)}",
            signature_valid=False
        )

def get_verified_documents(wallet_address: str) -> Dict[str, Document]:
    """Get all verified documents for a wallet"""
    if wallet_address not in documents_store:
        return {}
    return {
        doc_type: doc 
        for doc_type, doc in documents_store[wallet_address].items()
        if doc.status == DocumentStatus.VERIFIED
    }

def calculate_total_document_boost(wallet_address: str) -> int:
    """Calculate total credit score boost from verified documents"""
    verified_docs = get_verified_documents(wallet_address)
    return sum(doc.credit_score_boost for doc in verified_docs.values())

def get_document_info(wallet_address: str) -> Dict:
    """Get document verification info for a wallet"""
    if wallet_address not in documents_store:
        return {
            "total_boost": 0,
            "verified_count": 0,
            "documents": {}
        }
    
    docs = documents_store[wallet_address]
    verified_docs = {k: v for k, v in docs.items() if v.status == DocumentStatus.VERIFIED}
    
    return {
        "total_boost": sum(doc.credit_score_boost for doc in verified_docs.values()),
        "verified_count": len(verified_docs),
        "documents": {
            doc_type: {
                "status": doc.status,
                "boost": doc.credit_score_boost,
                "verified_at": doc.verified_at,
                "filename": doc.filename
            }
            for doc_type, doc in docs.items()
        }
    }

def get_available_document_types() -> Dict[str, Dict[str, int]]:
    """Get all available document types and their credit boost ranges"""
    return {
        doc_type.value: {
            "min_boost": min_boost,
            "max_boost": max_boost,
            "average_boost": (min_boost + max_boost) // 2
        }
        for doc_type, (min_boost, max_boost) in CREDIT_SCORE_BOOST_RANGES.items()
    }
