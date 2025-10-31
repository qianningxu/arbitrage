"""Execute arbitrage trades between Bybit and Jupiter"""
from main.jupiter.account.swap import u_to_crypto as jupiter_u_to_crypto, crypto_to_u as jupiter_crypto_to_u
from main.jupiter.account.transfers import withdraw as jupiter_withdraw
from main.jupiter.account.balance import check_balance as jupiter_check_balance
from main.bybit.account.swap import u_to_crypto as bybit_u_to_crypto, crypto_to_u as bybit_crypto_to_u
from main.bybit.account.transfers import withdraw as bybit_withdraw
from main.bybit.account.balance import get_balance as bybit_get_balance
from main.bybit.monitor.pricing import get_buy_rate

def execute_arbitrage(base_coin, direction):
    """
    Execute arbitrage trade between Bybit and Jupiter
    
    Args:
        base_coin: Base coin symbol (e.g., 'SOL', 'BTC')
        direction: Direction to execute ('B→J' or 'J→B')
    
    Returns:
        dict with keys: 'success', 'direction', 'coin', 'steps', 
                       'initial_balance', 'final_balance', 'actual_profit', 'error'
    """
    if direction not in ['B→J', 'J→B']:
        raise ValueError(f"direction must be 'B→J' or 'J→B', got '{direction}'")
    
    base_coin = base_coin.upper()
    result = {
        'success': False,
        'direction': direction,
        'coin': base_coin,
        'steps': [],
        'initial_balance': None,
        'final_balance': None,
        'actual_profit': None,
        'error': None
    }
    
    try:
        if direction == 'B→J':
            initial_balance = bybit_get_balance("USDT", "UNIFIED")
            print(f"💰 Initial Bybit USDT balance: ${initial_balance:.2f}")
        else:
            initial_balance = jupiter_check_balance("USDT")
            print(f"💰 Initial Jupiter USDT balance: ${initial_balance:.2f}")
        
        result['initial_balance'] = initial_balance
        
        if direction == 'B→J':
            print(f"\n🚀 Executing B→J arbitrage for {base_coin}...")
            
            print(f"\n📍 Step 1/3: Buy {base_coin} on Bybit")
            from main.jupiter.monitor.pricing import get_exchange_rate
            J = get_exchange_rate(base_coin, "USDT", 1)
            estimated_qty = initial_balance / J
            bybit_price = get_buy_rate(base_coin, estimated_qty)['rate']
            bybit_buy = bybit_u_to_crypto(base_coin, bybit_price)
            result['steps'].append({'step': 'bybit_buy', 'result': bybit_buy})
            print(f"✅ Bought {base_coin} on Bybit")
            
            print(f"\n📍 Step 2/3: Withdraw {base_coin} from Bybit to Jupiter")
            bybit_withdrawal = bybit_withdraw(base_coin)
            result['steps'].append({'step': 'bybit_withdraw', 'result': bybit_withdrawal})
            print(f"✅ Withdrawal initiated from Bybit")
            
            input("⏸️  Press Enter after confirming deposit on Jupiter...")
            
            print(f"\n📍 Step 3/3: Sell {base_coin} on Jupiter")
            jupiter_sell = jupiter_crypto_to_u(base_coin)
            result['steps'].append({'step': 'jupiter_sell', 'result': jupiter_sell})
            print(f"✅ Sold {base_coin} on Jupiter")
            
            final_balance = jupiter_check_balance("USDT")
            print(f"💰 Final Jupiter USDT balance: ${final_balance:.2f}")
        else:
            print(f"\n🚀 Executing J→B arbitrage for {base_coin}...")
            
            print(f"\n📍 Step 1/3: Buy {base_coin} on Jupiter")
            jupiter_buy = jupiter_u_to_crypto(base_coin)
            result['steps'].append({'step': 'jupiter_buy', 'result': jupiter_buy})
            print(f"✅ Bought {base_coin} on Jupiter")
            
            print(f"\n📍 Step 2/3: Withdraw {base_coin} from Jupiter to Bybit")
            jupiter_withdrawal = jupiter_withdraw(base_coin)
            result['steps'].append({'step': 'jupiter_withdraw', 'result': jupiter_withdrawal})
            print(f"✅ Withdrawal sent to Bybit")
            
            input("⏸️  Press Enter after confirming deposit on Bybit...")
            
            print(f"\n📍 Step 3/3: Sell {base_coin} on Bybit")
            bybit_sell = bybit_crypto_to_u(base_coin)
            result['steps'].append({'step': 'bybit_sell', 'result': bybit_sell})
            print(f"✅ Sold {base_coin} on Bybit")
            
            final_balance = bybit_get_balance("USDT", "FUND")
            print(f"💰 Final Bybit USDT balance: ${final_balance:.2f}")
        
        result['final_balance'] = final_balance
        actual_profit = final_balance - initial_balance
        result['actual_profit'] = actual_profit
        
        print(f"\n{'='*50}")
        print(f"📊 Arbitrage Results:")
        print(f"   Initial Balance: ${initial_balance:.2f}")
        print(f"   Final Balance:   ${final_balance:.2f}")
        print(f"   Actual Profit:   ${actual_profit:.2f} ({actual_profit/initial_balance:.2%})")
        print(f"{'='*50}")
        
        result['success'] = True
        print(f"\n🎉 Arbitrage execution completed successfully!")
        
    except Exception as e:
        result['error'] = str(e)
        print(f"\n❌ Arbitrage execution failed: {e}")
    
    return result

