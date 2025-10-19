"""
Deploy the FiduciaLens Loan Pool contract to Algorand TestNet
"""

from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.transaction import ApplicationCreateTxn, StateSchema, OnComplete, wait_for_confirmation
import base64
import os

# Algorand TestNet configuration
ALGOD_ADDRESS = "https://testnet-api.algonode.cloud"
ALGOD_TOKEN = ""

def get_algod_client():
    """Initialize Algod client for TestNet"""
    return algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS)

def compile_program(client, source_code):
    """Compile TEAL source code"""
    compile_response = client.compile(source_code)
    return base64.b64decode(compile_response['result'])

def deploy_contract(private_key):
    """Deploy the loan pool contract"""
    
    # Initialize client
    client = get_algod_client()
    
    # Get account from private key
    address = account.address_from_private_key(private_key)
    print(f"Deploying from address: {address}")
    
    # Read compiled TEAL files
    with open("loan_pool_approval.teal", "r") as f:
        approval_program_source = f.read()
    
    with open("loan_pool_clear.teal", "r") as f:
        clear_program_source = f.read()
    
    # Compile programs
    approval_program = compile_program(client, approval_program_source)
    clear_program = compile_program(client, clear_program_source)
    
    # Define schema
    global_schema = StateSchema(num_uints=3, num_byte_slices=0)
    local_schema = StateSchema(num_uints=3, num_byte_slices=0)
    
    # Get suggested parameters
    params = client.suggested_params()
    
    # Create application transaction
    txn = ApplicationCreateTxn(
        sender=address,
        sp=params,
        on_complete=OnComplete.NoOpOC,
        approval_program=approval_program,
        clear_program=clear_program,
        global_schema=global_schema,
        local_schema=local_schema,
    )
    
    # Sign transaction
    signed_txn = txn.sign(private_key)
    
    # Submit transaction
    tx_id = client.send_transaction(signed_txn)
    print(f"Transaction ID: {tx_id}")
    
    # Wait for confirmation
    confirmed_txn = wait_for_confirmation(client, tx_id, 4)
    print(f"✅ Contract deployed successfully!")
    
    # Get application ID
    app_id = confirmed_txn["application-index"]
    print(f"📝 Application ID: {app_id}")
    print(f"🔗 View on AlgoExplorer: https://testnet.algoexplorer.io/application/{app_id}")
    
    return app_id

def get_application_address(app_id):
    """Get the application's Algorand address"""
    import algosdk.logic as logic
    return logic.get_application_address(app_id)

if __name__ == "__main__":
    print("🚀 FiduciaLens Contract Deployment")
    print("=" * 50)
    
    # Check for environment variable or prompt for private key
    private_key = os.getenv("ALGORAND_PRIVATE_KEY")
    
    if not private_key:
        print("\n⚠️  No private key found in environment.")
        print("Please set ALGORAND_PRIVATE_KEY environment variable")
        print("or paste your mnemonic phrase (25 words):\n")
        mnemonic_phrase = input("> ")
        private_key = mnemonic.to_private_key(mnemonic_phrase)
    
    try:
        app_id = deploy_contract(private_key)
        app_address = get_application_address(app_id)
        print(f"\n📍 Application Address: {app_address}")
        print("\n⚠️  Remember to fund this address with ALGO for contract operations!")
    except Exception as e:
        print(f"\n❌ Deployment failed: {str(e)}")
