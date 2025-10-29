import os
import sys
import json
import time
import requests
from dotenv import load_dotenv
from solders.keypair import Keypair

# Load environment variables
load_dotenv()

# Handle imports
try:
    from main.trade.bybit_auth import sign_request
    from main.trade.bybit_balance import get_all_fund_balances, get_all_unified_balances
    from main.trade.bybit_transfer import internal_transfer
except ModuleNotFoundError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
    from main.trade.bybit_auth import sign_request
    from main.trade.bybit_balance import get_all_fund_balances, get_all_unified_balances
    from main.trade.bybit_transfer import internal_transfer


def get_solana_wallet_address():
    """Get Solana wallet address from private key in .env"""
    private_key = os.getenv("SOLANA_PRIVATE_KEY")
    if not private_key:
        raise ValueError("SOLANA_PRIVATE_KEY must be set in .env file")
    
    keypair = Keypair.from_base58_string(private_key)
    address = str(keypair.pubkey())
    return address


def transfer_unified_to_fund():
    """Transfer all coins from UNIFIED to FUND account"""
    balances = get_all_unified_balances()
    
    if not balances:
        print("ℹ️  No funds in UNIFIED account to transfer")
        return []
    
    print(f"📦 Found {len(balances)} coins in UNIFIED account")
    print(f"💰 Transferring all assets from UNIFIED to FUND...")
    results = []
    
    for coin, amount in balances.items():
        try:
            result = internal_transfer(coin, amount, "UNIFIED", "FUND")
            results.append({"coin": coin, "amount": amount, "success": True, "result": result})
        except Exception as e:
            print(f"⚠️  Failed to transfer {coin}: {str(e)}")
            results.append({"coin": coin, "amount": amount, "success": False, "error": str(e)})
    
    return results


def withdraw_from_bybit(coin, amount):
    """
    Withdraw coins from Bybit FUND account to Solana wallet
    
    Args:
        coin: Coin symbol (e.g., 'SOL', 'USDT')
        amount: Amount to withdraw
        
    Returns:
        dict: Withdrawal result with withdrawal_id
    """
    coin = coin.upper()
    solana_address = get_solana_wallet_address()
    
    # Prepare withdrawal parameters
    timestamp = str(int(time.time() * 1000))
    params = {
        "coin": coin,
        "chain": "SOL",
        "address": solana_address,
        "amount": str(amount),
        "timestamp": timestamp
    }
    
    # Make withdrawal request
    response = requests.post(
        "https://api.bybit.com/v5/asset/withdraw/create",
        json=params,
        headers=sign_request(json.dumps(params))
    )
    
    data = response.json()
    if data.get("retCode") != 0:
        raise ValueError(f"Withdrawal failed: {data.get('retMsg')}")
    
    withdrawal_id = data["result"]["id"]
    return {"withdrawal_id": withdrawal_id, "coin": coin, "amount": amount, "address": solana_address}


def transfer_all_to_jupiter():
    """
    Complete flow: Transfer all cryptos from UNIFIED to FUND, 
    then withdraw all to Jupiter (Solana) wallet
    
    Returns:
        dict: Summary of transfers and withdrawals
    """
    print("\n" + "="*60)
    print("🚀 BYBIT TO JUPITER TRANSFER FLOW")
    print("="*60 + "\n")
    
    # Step 1: Transfer from UNIFIED to FUND
    print("📍 STEP 1: Transfer UNIFIED → FUND")
    print("-" * 60)
    transfer_results = transfer_unified_to_fund()
    
    if not transfer_results:
        print("\n❌ No funds to transfer. Exiting.")
        return {"transfers": [], "withdrawals": []}
    
    # Display transfer summary
    print(f"\n✅ Transferred {sum(1 for r in transfer_results if r['success'])}/{len(transfer_results)} coins successfully")
    
    # Step 2: Get all FUND balances
    print("\n📍 STEP 2: Check FUND account balances")
    print("-" * 60)
    fund_balances = get_all_fund_balances()
    
    if not fund_balances:
        print("⚠️  No funds available in FUND account for withdrawal")
        return {"transfers": transfer_results, "withdrawals": []}
    
    print(f"💰 Available in FUND account:")
    for coin, amount in fund_balances.items():
        print(f"   {coin}: {amount}")
    
    # Step 3: Withdraw to Jupiter
    print("\n📍 STEP 3: Withdraw FUND → Jupiter (Solana)")
    print("-" * 60)
    withdrawal_results = []
    
    for coin, amount in fund_balances.items():
        try:
            # Load withdrawal fees to check if withdrawal is possible
            fees_path = os.path.join(os.path.dirname(__file__), "../../files/withdrawal_fees.json")
            with open(fees_path, 'r') as f:
                withdrawal_fees = json.load(f)
            
            if coin in withdrawal_fees:
                fee = float(withdrawal_fees[coin]["withdrawFee"])
                if fee >= amount:
                    print(f"⚠️  Skipping {coin}: Amount {amount} ≤ Fee {fee}")
                    withdrawal_results.append({
                        "coin": coin, 
                        "amount": amount, 
                        "success": False, 
                        "error": f"Amount less than withdrawal fee ({fee})"
                    })
                    continue
                
                # Withdraw (amount - fee to account for the fee)
                withdrawal_amount = amount - fee
                result = withdraw_from_bybit(coin, withdrawal_amount)
                withdrawal_results.append({
                    "coin": coin, 
                    "amount": withdrawal_amount, 
                    "fee": fee,
                    "success": True, 
                    "result": result
                })
            else:
                print(f"⚠️  No fee info for {coin}, attempting full withdrawal...")
                result = withdraw_from_bybit(coin, amount)
                withdrawal_results.append({
                    "coin": coin, 
                    "amount": amount, 
                    "success": True, 
                    "result": result
                })
                
        except Exception as e:
            print(f"❌ Failed to withdraw {coin}: {str(e)}")
            withdrawal_results.append({
                "coin": coin, 
                "amount": amount, 
                "success": False, 
                "error": str(e)
            })
    
    # Final Summary
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)
    print(f"✅ Transfers: {sum(1 for r in transfer_results if r['success'])}/{len(transfer_results)}")
    print(f"✅ Withdrawals: {sum(1 for r in withdrawal_results if r['success'])}/{len(withdrawal_results)}")
    print("="*60 + "\n")
    
    return {
        "transfers": transfer_results,
        "withdrawals": withdrawal_results
    }


if __name__ == "__main__":
    # Example: Run the complete transfer flow
    result = transfer_all_to_jupiter()
    print("\nFinal result:", json.dumps(result, indent=2))

