#!/usr/bin/env python3
"""
Create a test wallet for Algorand TestNet deployment.
Saves the mnemonic and address to wallet.txt for safekeeping.
"""

from algosdk import account, mnemonic
import os

def create_wallet():
    """Create a new Algorand account and save credentials."""
    
    # Generate account
    private_key, address = account.generate_account()
    mn = mnemonic.from_private_key(private_key)
    
    print("=" * 60)
    print("🎉 NEW ALGORAND TESTNET WALLET CREATED!")
    print("=" * 60)
    print(f"\n📍 Address: {address}")
    print(f"\n🔑 Mnemonic (SAVE THIS SECURELY!):")
    print(f"{mn}")
    print("\n" + "=" * 60)
    
    # Save to file
    wallet_file = os.path.join(os.path.dirname(__file__), 'wallet.txt')
    with open(wallet_file, 'w') as f:
        f.write(f"Algorand TestNet Wallet\n")
        f.write(f"Created: {os.popen('date').read().strip()}\n")
        f.write(f"\nAddress: {address}\n")
        f.write(f"\nMnemonic:\n{mn}\n")
        f.write(f"\nPrivate Key (base64): {private_key}\n")
    
    print(f"\n✅ Wallet info saved to: {wallet_file}")
    print("\n📝 NEXT STEPS:")
    print("1. Fund this wallet at: https://bank.testnet.algorand.network/")
    print("2. Paste the address above and request 10 ALGO")
    print("3. Wait for confirmation (usually ~4 seconds)")
    print("4. Run: python scripts/deploy.py")
    print("\n⚠️  IMPORTANT: Keep wallet.txt secure and NEVER commit to git!")
    print("=" * 60)
    
    return address, mn

if __name__ == "__main__":
    create_wallet()
