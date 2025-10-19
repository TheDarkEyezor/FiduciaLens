"""
Create a test wallet for Algorand development
"""

from algosdk import account, mnemonic

def create_wallet():
    """Generate a new Algorand account"""
    private_key, address = account.generate_account()
    pass_phrase = mnemonic.from_private_key(private_key)
    
    print("=" * 70)
    print("🎉 New Algorand Wallet Created!")
    print("=" * 70)
    print()
    print(f"📬 Address:")
    print(f"   {address}")
    print()
    print(f"🔑 Private Key:")
    print(f"   {private_key}")
    print()
    print(f"📝 Mnemonic (25 words - SAVE THIS!):")
    print(f"   {pass_phrase}")
    print()
    print("=" * 70)
    print("⚠️  IMPORTANT: Save your mnemonic phrase in a secure location!")
    print("   This is the ONLY way to recover your account.")
    print("=" * 70)
    print()
    print("📋 Next Steps:")
    print()
    print("For TestNet:")
    print(f"   1. Visit: https://bank.testnet.algorand.network/")
    print(f"   2. Paste your address: {address}")
    print(f"   3. Click 'Dispense' to get free TestNet ALGO")
    print()
    print("For Local Sandbox:")
    print(f"   1. Start sandbox: cd sandbox && ./sandbox up")
    print(f"   2. Fund account: ./sandbox goal clerk send \\")
    print(f"      -a 10000000 -f <DEFAULT_ADDR> -t {address}")
    print()
    print("To deploy contract:")
    print(f"   export ALGORAND_PRIVATE_KEY=\"{private_key}\"")
    print(f"   python3 deploy.py")
    print()

if __name__ == "__main__":
    create_wallet()
