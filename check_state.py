#!/usr/bin/env python3
"""Check the contract and user state on the blockchain"""
import sys
from algosdk.v2client import algod
import base64

# Initialize Algod client
algod_token = ''
algod_address = 'https://testnet-api.algonode.cloud'
algod_client = algod.AlgodClient(algod_token, algod_address)

app_id = 747997888  # Updated to new contract deployment

# Get user address from command line or use default
if len(sys.argv) > 1:
    user_address = sys.argv[1]
else:
    user_address = None

print(f"🔍 Checking App ID: {app_id}\n")

# Get app info to see global state
try:
    app_info = algod_client.application_info(app_id)
    print('🌍 GLOBAL STATE:')
    global_state = app_info.get('params', {}).get('global-state', [])
    if not global_state:
        print('  (empty)')
    for kv in global_state:
        key = kv['key']
        key_decoded = base64.b64decode(key).decode('utf-8')
        if 'uint' in kv['value']:
            value = kv['value']['uint']
            print(f'  {key_decoded}: {value:,} microAlgos ({value / 1_000_000:.6f} ALGO)')
        elif 'bytes' in kv['value']:
            value = kv['value']['bytes']
            print(f'  {key_decoded}: {value}')
        else:
            print(f'  {key_decoded}: {kv["value"]}')
except Exception as e:
    print(f'❌ Error getting global state: {e}')

# If user address provided, check local state
if user_address:
    print(f'\n👤 USER LOCAL STATE ({user_address}):')
    try:
        account_info = algod_client.account_info(user_address)
        apps_local_state = account_info.get('apps-local-state', [])
        
        app_state = None
        for app in apps_local_state:
            if app['id'] == app_id:
                app_state = app
                break
        
        if not app_state:
            print('  ❌ User not opted in to this app')
        else:
            key_value = app_state.get('key-value', [])
            if not key_value:
                print('  (empty - user opted in but no state)')
            for kv in key_value:
                key = kv['key']
                key_decoded = base64.b64decode(key).decode('utf-8')
                if 'uint' in kv['value']:
                    value = kv['value']['uint']
                    print(f'  {key_decoded}: {value:,} microAlgos ({value / 1_000_000:.6f} ALGO)')
                elif 'bytes' in kv['value']:
                    value = kv['value']['bytes']
                    print(f'  {key_decoded}: {value}')
                else:
                    print(f'  {key_decoded}: {kv["value"]}')
    except Exception as e:
        print(f'  ❌ Error getting user state: {e}')

print('\n✅ Done')
