#!/usr/bin/env python3
"""
Opt-in to the FiduciaLens loan pool smart contract.
This must be done before a user can interact with the contract.
"""

import os
import sys
from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction
from algosdk.transaction import ApplicationOptInTxn

# Algorand TestNet configuration
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

def read_wallet():
    """Read wallet credentials from wallet.txt"""
    wallet_file = os.path.join(os.path.dirname(__file__), 'wallet.txt')
    
    if not os.path.exists(wallet_file):
        print("❌ Error: wallet.txt not found!")
        print("Run: python scripts/create_test_wallet.py first")
        sys.exit(1)
    
    with open(wallet_file, 'r') as f:
        lines = f.readlines()
    
    # Extract mnemonic
    mnemonic_start = False
    mnemonic_words = []
    for line in lines:
        if "Mnemonic:" in line:
            mnemonic_start = True
            continue
        if mnemonic_start and line.strip():
            if "Private Key" in line:
                break
            mnemonic_words.append(line.strip())
    
    mn = ' '.join(mnemonic_words)
    private_key = mnemonic.to_private_key(mn)
    address = account.address_from_private_key(private_key)
    
    return private_key, address

def read_app_id():
    """Read application ID from app_id.txt"""
    app_id_file = os.path.join(os.path.dirname(__file__), 'app_id.txt')
    
    if not os.path.exists(app_id_file):
        print("❌ Error: app_id.txt not found!")
        print("Deploy the contract first: python scripts/deploy.py")
        sys.exit(1)
    
    with open(app_id_file, 'r') as f:
        first_line = f.readline()
        app_id = int(first_line.split(':')[1].strip())
    
    return app_id

def wait_for_confirmation(client, txid, timeout=10):
    """Wait for transaction confirmation"""
    start_round = client.status()["last-round"] + 1
    current_round = start_round
    
    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(txid)
        except Exception:
            current_round += 1
            client.status_after_block(current_round)
            continue
            
        if pending_txn.get("confirmed-round", 0) > 0:
            return pending_txn
        elif pending_txn["pool-error"]:
            raise Exception(f'Pool error: {pending_txn["pool-error"]}')
        
        current_round += 1
        client.status_after_block(current_round)
    
    raise Exception(f"Transaction not confirmed after {timeout} rounds")

def opt_in():
    """Opt-in to the smart contract"""
    
    print("=" * 60)
    print("🔗 OPT-IN TO FiduciaLens LOAN POOL")
    print("=" * 60)
    
    # Initialize client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)
    
    # Read credentials
    print("\n📂 Reading wallet...")
    private_key, address = read_wallet()
    print(f"✅ Address: {address}")
    
    # Read app ID
    print("\n📋 Reading application ID...")
    app_id = read_app_id()
    print(f"✅ Application ID: {app_id}")
    
    # Check if already opted in
    account_info = algod_client.account_info(address)
    apps_local_state = account_info.get('apps-local-state', [])
    
    for app in apps_local_state:
        if app['id'] == app_id:
            print(f"\n⚠️  You are already opted in to application {app_id}")
            print("No need to opt-in again!")
            return
    
    # Get transaction parameters
    params = algod_client.suggested_params()
    
    # Create opt-in transaction
    print("\n📝 Creating opt-in transaction...")
    txn = ApplicationOptInTxn(
        sender=address,
        sp=params,
        index=app_id
    )
    
    # Sign transaction
    print("✍️  Signing transaction...")
    signed_txn = txn.sign(private_key)
    
    # Send transaction
    print("📤 Sending transaction...")
    tx_id = algod_client.send_transaction(signed_txn)
    print(f"✅ Transaction ID: {tx_id}")
    
    # Wait for confirmation
    print("\n⏳ Waiting for confirmation...")
    try:
        confirmed_txn = wait_for_confirmation(algod_client, tx_id)
        
        print("\n" + "=" * 60)
        print("🎉 OPT-IN SUCCESSFUL!")
        print("=" * 60)
        print(f"\n🔗 Transaction: https://testnet.algoexplorer.io/tx/{tx_id}")
        print("\nYou can now:")
        print("  • Deposit collateral")
        print("  • Borrow funds")
        print("  • Repay loans")
        print("  • Withdraw collateral")
        print("\n💡 Use the frontend UI to interact with the pool!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error during opt-in: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    opt_in()
