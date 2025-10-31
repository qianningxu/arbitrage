import time
from main.jupiter.monitor.pricing import get_exchange_rate
from main.bybit.monitor.pricing import get_buy_rate, get_sell_rate
from main.workflows.arbitrage_calc import is_b2j_profitable, is_j2b_profitable
from main.shared.data import get_withdrawal_fee

def check_arbitrage(base_coin, usdt_balance, direction):
    """
    Check for arbitrage opportunities for a given coin
    
    Args:
        base_coin: Base coin symbol (e.g., 'SOL', 'BTC')
        usdt_balance: Amount of USDT to trade
        direction: Direction to check ('B→J' or 'J→B')
    
    Returns:
        dict with keys: 'direction', 'profitable', 'profit', 'bybit_price', 
        'jupiter_price', 'slippage', 'usdt_balance'
    """
    if direction not in ['B→J', 'J→B']:
        raise ValueError(f"direction must be 'B→J' or 'J→B', got '{direction}'")
    
    print(f"\nChecking {base_coin}...", end=" ")
    
    w = get_withdrawal_fee(base_coin)
    if w is None:
        print("No withdrawal fee data")
        return None
    
    J = get_exchange_rate(base_coin, "USDT", 1)
    if not J:
        print("No Jupiter data")
        return None
    
    estimated_qty = usdt_balance / J
    
    if direction == 'B→J':
        bybit_buy = get_buy_rate(base_coin, estimated_qty)
        B_price = bybit_buy['rate']
        slippage = bybit_buy['slippage']
        profitable, profit = is_b2j_profitable(B_price, J, usdt_balance, w, slippage)
    else:
        bybit_sell = get_sell_rate(base_coin, estimated_qty)
        B_price = bybit_sell['rate']
        slippage = bybit_sell['slippage']
        profitable, profit = is_j2b_profitable(J, B_price, usdt_balance, slippage)
    
    print(f"B=${B_price:.6f} | J=${J:.6f} | Slip={slippage:.2%}", end=" ")
    if profitable:
        print(f"✓ ${profit:.2f}")
    else:
        print(f"✗ ${profit:.2f}")
    
    return {
        'direction': direction if profitable else None,
        'profitable': profitable,
        'profit': profit,
        'bybit_price': B_price,
        'jupiter_price': J,
        'slippage': slippage,
        'usdt_balance': usdt_balance
    }

def scan_all_opportunities(usdt_balance, direction):
    """
    Scan tradeable coins until finding a profitable arbitrage opportunity
    
    Args:
        usdt_balance: Amount of USDT to trade
        direction: Direction to check ('B→J' or 'J→B')
    
    Returns:
        dict with first profitable opportunity found, or None if none found
    """
    if direction not in ['B→J', 'J→B']:
        raise ValueError(f"direction must be 'B→J' or 'J→B', got '{direction}'")
    
    from main.shared.data import get_all_tradeable_symbols
    import time
    
    symbols = get_all_tradeable_symbols()
    
    for symbol in symbols:
        try:
            result = check_arbitrage(symbol, usdt_balance, direction)
            if result and result['profitable']:
                result['coin'] = symbol
                return result
        except Exception as e:
            print(f"Error - {e}")
        time.sleep(1)
    
    return None

