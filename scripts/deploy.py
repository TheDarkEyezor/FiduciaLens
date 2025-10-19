#!/usr/bin/env python3
"""
Deploy the FiduciaLens loan pool smart contract to Algorand TestNet.
Requires a funded wallet created with create_test_wallet.py
"""

import os
import sys
from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction
from algosdk.transaction import ApplicationCreateTxn, OnComplete, StateSchema
import base64

# Add parent directory to path to import contract
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from contracts.loan_pool import approval_program, clear_state_program

# Algorand TestNet configuration
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""  # Public node, no token needed

def read_wallet():
    """Read wallet credentials from wallet.txt"""
    wallet_file = os.path.join(os.path.dirname(__file__), 'wallet.txt')
    
    if not os.path.exists(wallet_file):
        print("❌ Error: wallet.txt not found!")
        print("Run: python scripts/create_test_wallet.py first")
        sys.exit(1)
    
    with open(wallet_file, 'r') as f:
        lines = f.readlines()
    
    # Extract mnemonic (starts after "Mnemonic:" line)
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

def compile_program(client, source_code):
    """Compile TEAL source code"""
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])

def wait_for_confirmation(client, txid, timeout=10):
    """Wait for transaction confirmation"""
    start_round = client.status()["last-round"] + 1
    current_round = start_round
    
    while current_round < start_round + timeout:
        try:
            pending_txn = client.pending_transaction_info(txid)
        except Exception as e:
            print(f"⏳ Waiting for confirmation... (round {current_round})")
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

def deploy_contract():
    """Deploy the loan pool smart contract"""
    
    print("=" * 60)
    print("🚀 DEPLOYING FiduciaLens LOAN POOL TO ALGORAND TESTNET")
    print("=" * 60)
    
    # Initialize algod client
    algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)
    
    # Read wallet
    print("\n📂 Reading wallet credentials...")
    private_key, address = read_wallet()
    print(f"✅ Deployer address: {address}")
    
    # Check balance
    account_info = algod_client.account_info(address)
    balance = account_info.get('amount', 0) / 1_000_000  # Convert microAlgos to Algos
    print(f"💰 Account balance: {balance:.6f} ALGO")
    
    if balance < 0.5:
        print(f"\n❌ Error: Insufficient balance!")
        print(f"Please fund your wallet at: https://bank.testnet.algorand.network/")
        print(f"Address: {address}")
        sys.exit(1)
    
    # Read compiled TEAL programs
    print("\n📜 Reading compiled TEAL programs...")
    contracts_dir = os.path.join(os.path.dirname(__file__), '..', 'contracts')
    
    approval_teal_file = os.path.join(contracts_dir, 'loan_pool_approval.teal')
    clear_teal_file = os.path.join(contracts_dir, 'loan_pool_clear.teal')
    
    if not os.path.exists(approval_teal_file) or not os.path.exists(clear_teal_file):
        print("❌ Error: TEAL files not found!")
        print("Run: python contracts/loan_pool.py first to compile")
        sys.exit(1)
    
    with open(approval_teal_file, 'r') as f:
        approval_teal = f.read()
    
    with open(clear_teal_file, 'r') as f:
        clear_teal = f.read()
    
    print("✅ TEAL programs loaded")
    
    # Compile programs
    print("\n🔨 Compiling programs...")
    approval_compiled = compile_program(algod_client, approval_teal)
    clear_compiled = compile_program(algod_client, clear_teal)
    print("✅ Programs compiled")
    
    # Define state schema
    # Global: TotalCollateral, TotalBorrow, MaxLTV (3 uints)
    # Local: Collateral, Debt, CreditScore (3 uints)
    global_schema = StateSchema(num_uints=3, num_byte_slices=0)
    local_schema = StateSchema(num_uints=3, num_byte_slices=0)
    
    print("\n📊 State Schema:")
    print(f"   Global: {global_schema.num_uints} uints, {global_schema.num_byte_slices} byte slices")
    print(f"   Local: {local_schema.num_uints} uints, {local_schema.num_byte_slices} byte slices")
    
    # Get transaction parameters
    params = algod_client.suggested_params()
    
    # Create application transaction
    print("\n📝 Creating application transaction...")
    txn = ApplicationCreateTxn(
        sender=address,
        sp=params,
        on_complete=OnComplete.NoOpOC,
        approval_program=approval_compiled,
        clear_program=clear_compiled,
        global_schema=global_schema,
        local_schema=local_schema,
        app_args=[],  # Initialize with MaxLTV=50 in the contract
    )
    
    # Sign transaction
    print("✍️  Signing transaction...")
    signed_txn = txn.sign(private_key)
    
    # Send transaction
    print("📤 Sending transaction to TestNet...")
    tx_id = algod_client.send_transaction(signed_txn)
    print(f"✅ Transaction ID: {tx_id}")
    
    # Wait for confirmation
    print("\n⏳ Waiting for confirmation...")
    try:
        confirmed_txn = wait_for_confirmation(algod_client, tx_id, timeout=10)
        app_id = confirmed_txn.get('application-index')
        
        print("\n" + "=" * 60)
        print("🎉 CONTRACT DEPLOYED SUCCESSFULLY!")
        print("=" * 60)
        print(f"\n📍 Application ID: {app_id}")
        print(f"🔗 Transaction: https://testnet.algoexplorer.io/tx/{tx_id}")
        print(f"🔗 Application: https://testnet.algoexplorer.io/application/{app_id}")
        print("\n📝 NEXT STEPS:")
        print(f"1. Update backend/.env with: APP_ID={app_id}")
        print(f"2. Update frontend-nextjs/.env.local with: NEXT_PUBLIC_APP_ID={app_id}")
        print(f"3. Restart backend and frontend servers")
        print(f"4. Test transactions in the UI!")
        print("=" * 60)
        
        # Save app_id to file
        app_id_file = os.path.join(os.path.dirname(__file__), 'app_id.txt')
        with open(app_id_file, 'w') as f:
            f.write(f"Application ID: {app_id}\n")
            f.write(f"Transaction: https://testnet.algoexplorer.io/tx/{tx_id}\n")
            f.write(f"Application: https://testnet.algoexplorer.io/application/{app_id}\n")
        
        print(f"\n✅ App ID saved to: {app_id_file}")
        
        return app_id
        
    except Exception as e:
        print(f"\n❌ Error during deployment: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    deploy_contract()
