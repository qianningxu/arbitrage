"""Execute arbitrage trades between Bybit and Jupiter"""
import time
from main.jupiter.account.swap import u_to_crypto as jupiter_u_to_crypto, crypto_to_u as jupiter_crypto_to_u
from main.jupiter.account.transfers import withdraw as jupiter_withdraw
from main.jupiter.account.balance import check_balance as jupiter_check_balance
from main.bybit.account.swap import u_to_crypto as bybit_u_to_crypto, crypto_to_u as bybit_crypto_to_u
from main.bybit.account.transfers import withdraw as bybit_withdraw
from main.bybit.account.balance import get_balance as bybit_get_balance
from main.bybit.monitor.pricing import get_buy_rate

def execute_arbitrage(base_coin, direction, skip_confirmation=False):
    """
    Execute arbitrage trade between Bybit and Jupiter
    
    Args:
        base_coin: Base coin symbol (e.g., 'SOL', 'BTC')
        direction: Direction to execute ('B→J' or 'J→B')
        skip_confirmation: Skip manual confirmation prompts (default: False)
    
    Returns:
        dict with keys: 'success', 'direction', 'coin', 'steps', 'error'
    """
    if direction not in ['B→J', 'J→B']:
        raise ValueError(f"direction must be 'B→J' or 'J→B', got '{direction}'")
    
    base_coin = base_coin.upper()
    result = {
        'success': False,
        'direction': direction,
        'coin': base_coin,
        'steps': [],
        'error': None
    }
    
    try:
        if direction == 'B→J':
            print(f"\n🚀 Executing B→J arbitrage for {base_coin}...")
            
            print(f"\n📍 Step 1/3: Buy {base_coin} on Bybit")
            from main.jupiter.monitor.pricing import get_exchange_rate
            initial_balance = bybit_get_balance("USDT", "UNIFIED")
            J = get_exchange_rate(base_coin, "USDT", 1)
            estimated_qty = initial_balance / J
            bybit_price = get_buy_rate(base_coin, estimated_qty)['rate']
            initial_bybit_balance = bybit_get_balance(base_coin, "UNIFIED")
            bybit_buy = bybit_u_to_crypto(base_coin, bybit_price)
            expected_amount = bybit_buy.get("expected_amount", 0)
            result['steps'].append({'step': 'bybit_buy', 'result': bybit_buy})
            print(f"✅ Bought {base_coin} on Bybit")
            
            print(f"⏳ Waiting for balance to update (need at least {expected_amount * 0.5:.6f} {base_coin})...")
            max_wait = 30
            elapsed = 0
            target_balance = initial_bybit_balance + (expected_amount * 0.5)
            while elapsed < max_wait:
                time.sleep(10)
                elapsed += 10
                current_balance = bybit_get_balance(base_coin, "UNIFIED")
                if current_balance >= target_balance:
                    print(f"✅ Balance updated: {current_balance} {base_coin} (waited {elapsed}s)")
                    print(f"⏳ Waiting extra 10 seconds for security...")
                    time.sleep(10)
                    break
                print(f"   Retrying... current balance: {current_balance} {base_coin}, target: {target_balance:.6f} ({elapsed}s elapsed)")
            
            print(f"\n📍 Step 2/3: Withdraw {base_coin} from Bybit to Jupiter")
            bybit_withdrawal = bybit_withdraw(base_coin)
            withdrawn_amount = bybit_withdrawal.get('amount', 0) if bybit_withdrawal else 0
            result['steps'].append({'step': 'bybit_withdraw', 'result': bybit_withdrawal})
            print(f"✅ Withdrawal initiated from Bybit")
            
            if not skip_confirmation:
                input("⏸️  Press Enter after confirming deposit on Jupiter...")
            else:
                print(f"⏳ Waiting for {base_coin} deposit to arrive on Jupiter (need at least {withdrawn_amount * 0.5:.6f})...")
                initial_jupiter_balance = jupiter_check_balance(base_coin)
                target_balance = initial_jupiter_balance + (withdrawn_amount * 0.5)
                max_wait = 120
                elapsed = 0
                while elapsed < max_wait:
                    time.sleep(10)
                    elapsed += 10
                    current_balance = jupiter_check_balance(base_coin)
                    if current_balance >= target_balance:
                        print(f"✅ Deposit confirmed: {current_balance} {base_coin} (waited {elapsed}s)")
                        print(f"⏳ Waiting extra 10 seconds for security...")
                        time.sleep(10)
                        break
                    print(f"   Retrying... current balance: {current_balance} {base_coin}, target: {target_balance:.6f} ({elapsed}s elapsed)")
            
            print(f"\n📍 Step 3/3: Sell {base_coin} on Jupiter")
            jupiter_sell = jupiter_crypto_to_u(base_coin)
            result['steps'].append({'step': 'jupiter_sell', 'result': jupiter_sell})
            print(f"✅ Sold {base_coin} on Jupiter")
        else:
            print(f"\n🚀 Executing J→B arbitrage for {base_coin}...")
            
            print(f"\n📍 Step 1/3: Buy {base_coin} on Jupiter")
            initial_jupiter_balance = jupiter_check_balance(base_coin)
            jupiter_buy = jupiter_u_to_crypto(base_coin)
            expected_amount = jupiter_buy.get("expected_amount", 0)
            result['steps'].append({'step': 'jupiter_buy', 'result': jupiter_buy})
            print(f"✅ Bought {base_coin} on Jupiter")
            
            print(f"⏳ Waiting for balance to update (need at least {expected_amount * 0.5:.6f} {base_coin})...")
            max_wait = 60
            elapsed = 0
            target_balance = initial_jupiter_balance + (expected_amount * 0.5)
            while elapsed < max_wait:
                time.sleep(10)
                elapsed += 10
                current_balance = jupiter_check_balance(base_coin)
                if current_balance >= target_balance:
                    print(f"✅ Balance updated: {current_balance} {base_coin} (waited {elapsed}s)")
                    print(f"⏳ Waiting extra 10 seconds for security...")
                    time.sleep(10)
                    break
                print(f"   Retrying... current balance: {current_balance} {base_coin}, target: {target_balance:.6f} ({elapsed}s elapsed)")
            
            print(f"\n📍 Step 2/3: Withdraw {base_coin} from Jupiter to Bybit")
            jupiter_withdrawal = jupiter_withdraw(base_coin)
            withdrawn_amount = jupiter_withdrawal.get('amount', 0) if jupiter_withdrawal else 0
            result['steps'].append({'step': 'jupiter_withdraw', 'result': jupiter_withdrawal})
            print(f"✅ Withdrawal sent to Bybit")
            
            if not skip_confirmation:
                input("⏸️  Press Enter after confirming deposit on Bybit...")
            else:
                print(f"⏳ Waiting for {base_coin} deposit to arrive on Bybit (need at least {withdrawn_amount * 0.5:.6f})...")
                initial_bybit_balance = bybit_get_balance(base_coin, "FUND")
                target_balance = initial_bybit_balance + (withdrawn_amount * 0.5)
                max_wait = 120
                elapsed = 0
                while elapsed < max_wait:
                    time.sleep(10)
                    elapsed += 10
                    current_balance = bybit_get_balance(base_coin, "FUND")
                    if current_balance >= target_balance:
                        print(f"✅ Deposit confirmed: {current_balance} {base_coin} (waited {elapsed}s)")
                        print(f"⏳ Waiting extra 10 seconds for security...")
                        time.sleep(10)
                        break
                    print(f"   Retrying... current balance: {current_balance} {base_coin}, target: {target_balance:.6f} ({elapsed}s elapsed)")
            
            print(f"\n📍 Step 3/3: Sell {base_coin} on Bybit")
            bybit_sell = bybit_crypto_to_u(base_coin)
            result['steps'].append({'step': 'bybit_sell', 'result': bybit_sell})
            print(f"✅ Sold {base_coin} on Bybit")
        
        result['success'] = True
        print(f"\n🎉 Arbitrage execution completed successfully!")
        
    except Exception as e:
        result['error'] = str(e)
        print(f"\n❌ Arbitrage execution failed: {e}")
    
    return result

