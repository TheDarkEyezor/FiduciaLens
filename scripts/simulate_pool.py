"""
Pool Activity Simulator
Generates realistic pool activity with multiple simulated users
For demo purposes - makes the pool look active and populated
"""

import random
import asyncio
from algosdk import account, transaction
from algosdk.v2client import algod
import os

# Algorand configuration
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""
APP_ID = int(os.getenv("APP_ID", "747988234"))

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

# Simulated user profiles
USER_PROFILES = [
    {"name": "Conservative Saver", "deposit_range": (50, 100), "borrow_pct": 0.3},
    {"name": "Active Trader", "deposit_range": (20, 50), "borrow_pct": 0.6},
    {"name": "Whale Investor", "deposit_range": (200, 500), "borrow_pct": 0.4},
    {"name": "Small Borrower", "deposit_range": (10, 30), "borrow_pct": 0.5},
    {"name": "Balanced User", "deposit_range": (40, 80), "borrow_pct": 0.45},
]

def create_simulated_wallets(count: int = 5):
    """
    Create test wallet accounts
    Returns list of (address, private_key) tuples
    """
    wallets = []
    for i in range(count):
        private_key, address = account.generate_account()
        wallets.append({
            "address": address,
            "private_key": private_key,
            "profile": USER_PROFILES[i % len(USER_PROFILES)]
        })
    return wallets

async def fund_wallet_from_faucet(address: str, amount_algo: float = 10):
    """
    Request ALGO from TestNet faucet
    Note: Faucet has rate limits (1 request per address per day)
    """
    import aiohttp
    
    url = f"https://bank.testnet.algorand.network/"
    # In practice, you'd need to visit this URL manually or use a funded dispenser wallet
    print(f"⚠️  Manual action required: Fund {address} with {amount_algo} ALGO from:")
    print(f"    {url}?account={address}")
    print(f"    Then press Enter to continue...")
    input()

async def simulate_opt_in(wallet: dict):
    """Opt-in wallet to the application"""
    try:
        params = algod_client.suggested_params()
        
        txn = transaction.ApplicationOptInTxn(
            sender=wallet["address"],
            sp=params,
            index=APP_ID
        )
        
        signed_txn = txn.sign(wallet["private_key"])
        txid = algod_client.send_transaction(signed_txn)
        
        # Wait for confirmation
        transaction.wait_for_confirmation(algod_client, txid, 4)
        
        print(f"✅ {wallet['profile']['name']} opted in: {wallet['address'][:8]}...")
        return txid
    except Exception as e:
        print(f"❌ Opt-in failed: {e}")
        return None

async def simulate_deposit(wallet: dict, amount_microalgos: int):
    """Simulate a deposit transaction"""
    try:
        params = algod_client.suggested_params()
        
        # Payment transaction to the app
        payment_txn = transaction.PaymentTxn(
            sender=wallet["address"],
            sp=params,
            receiver=algod_client.application_info(APP_ID)["params"]["creator"],
            amt=amount_microalgos
        )
        
        # App call transaction
        app_args = [
            b"deposit",
            amount_microalgos.to_bytes(8, 'big')
        ]
        
        app_call_txn = transaction.ApplicationNoOpTxn(
            sender=wallet["address"],
            sp=params,
            index=APP_ID,
            app_args=app_args
        )
        
        # Group transactions
        gid = transaction.calculate_group_id([payment_txn, app_call_txn])
        payment_txn.group = gid
        app_call_txn.group = gid
        
        # Sign both
        signed_payment = payment_txn.sign(wallet["private_key"])
        signed_app_call = app_call_txn.sign(wallet["private_key"])
        
        # Send
        txid = algod_client.send_transactions([signed_payment, signed_app_call])
        
        # Wait for confirmation
        transaction.wait_for_confirmation(algod_client, txid, 4)
        
        amount_algo = amount_microalgos / 1_000_000
        print(f"💰 {wallet['profile']['name']} deposited {amount_algo:.2f} ALGO")
        return txid
    except Exception as e:
        print(f"❌ Deposit failed: {e}")
        return None

async def simulate_borrow(wallet: dict, amount_microalgos: int, credit_score: int):
    """Simulate a borrow transaction"""
    try:
        params = algod_client.suggested_params()
        
        app_args = [
            b"borrow",
            amount_microalgos.to_bytes(8, 'big'),
            credit_score.to_bytes(8, 'big'),
            b"mock_signature"  # Mock signature for simulation
        ]
        
        txn = transaction.ApplicationNoOpTxn(
            sender=wallet["address"],
            sp=params,
            index=APP_ID,
            app_args=app_args
        )
        
        signed_txn = txn.sign(wallet["private_key"])
        txid = algod_client.send_transaction(signed_txn)
        
        # Wait for confirmation
        transaction.wait_for_confirmation(algod_client, txid, 4)
        
        amount_algo = amount_microalgos / 1_000_000
        print(f"📊 {wallet['profile']['name']} borrowed {amount_algo:.2f} ALGO (Score: {credit_score})")
        return txid
    except Exception as e:
        print(f"❌ Borrow failed: {e}")
        return None

async def run_simulation(num_users: int = 5, total_pool_target_algo: float = 1000):
    """
    Run a full simulation with multiple users
    
    Args:
        num_users: Number of simulated users to create
        total_pool_target_algo: Target total pool size in ALGO
    """
    print("🎬 Starting Pool Activity Simulation")
    print(f"Target: {num_users} users, {total_pool_target_algo} ALGO total pool")
    print("-" * 60)
    
    # Step 1: Create wallets
    print("\n📝 Step 1: Creating simulated wallets...")
    wallets = create_simulated_wallets(num_users)
    
    for i, wallet in enumerate(wallets):
        print(f"  Wallet {i+1}: {wallet['address'][:8]}... ({wallet['profile']['name']})")
    
    # Step 2: Fund wallets (manual step required)
    print("\n💰 Step 2: Funding wallets from TestNet faucet...")
    print("⚠️  You need to manually fund these wallets:")
    for wallet in wallets:
        deposit_max = wallet['profile']['deposit_range'][1]
        needed = deposit_max + 5  # Extra for fees
        print(f"  {wallet['address']} needs ~{needed} ALGO")
    
    print(f"\nVisit: https://bank.testnet.algorand.network/")
    print("Fund each address, then press Enter to continue...")
    input()
    
    # Step 3: Opt-in all wallets
    print("\n🔗 Step 3: Opting in wallets...")
    for wallet in wallets:
        await simulate_opt_in(wallet)
        await asyncio.sleep(1)  # Rate limiting
    
    # Step 4: Simulate deposits
    print("\n💸 Step 4: Simulating deposits...")
    deposits_per_user = total_pool_target_algo / num_users
    
    for wallet in wallets:
        # Random amount within profile range
        min_deposit, max_deposit = wallet['profile']['deposit_range']
        deposit_amount = random.uniform(min_deposit, min(max_deposit, deposits_per_user * 1.5))
        deposit_microalgos = int(deposit_amount * 1_000_000)
        
        await simulate_deposit(wallet, deposit_microalgos)
        await asyncio.sleep(1)  # Rate limiting
    
    # Step 5: Simulate borrows
    print("\n📈 Step 5: Simulating borrows...")
    for wallet in wallets:
        # Calculate borrow amount based on profile
        profile = wallet['profile']
        borrow_pct = profile['borrow_pct']
        
        # Get wallet's deposit amount (would need to query contract state)
        # For simulation, use a percentage of their deposit range midpoint
        deposit_midpoint = sum(profile['deposit_range']) / 2
        borrow_amount = deposit_midpoint * borrow_pct
        borrow_microalgos = int(borrow_amount * 1_000_000)
        
        # Random credit score (500-850)
        credit_score = random.randint(500, 850)
        
        await simulate_borrow(wallet, borrow_microalgos, credit_score)
        await asyncio.sleep(1)  # Rate limiting
    
    # Step 6: Summary
    print("\n" + "=" * 60)
    print("✅ SIMULATION COMPLETE!")
    print("=" * 60)
    print(f"\nSimulated Users: {num_users}")
    print(f"Target Pool Size: {total_pool_target_algo} ALGO")
    print(f"\nUser Addresses (save these for cleanup):")
    for wallet in wallets:
        print(f"  - {wallet['address']}")
    
    print(f"\n🔗 Check pool state at:")
    print(f"  https://testnet.algoexplorer.io/application/{APP_ID}")

if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    num_users = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    pool_target = float(sys.argv[2]) if len(sys.argv) > 2 else 1000
    
    print(f"""
╔══════════════════════════════════════════════════════════╗
║         FiduciaLens POOL ACTIVITY SIMULATOR                ║
║                                                          ║
║  This tool creates realistic pool activity for demos    ║
║  by simulating multiple users depositing and borrowing  ║
╚══════════════════════════════════════════════════════════╝
""")
    
    asyncio.run(run_simulation(num_users, pool_target))
