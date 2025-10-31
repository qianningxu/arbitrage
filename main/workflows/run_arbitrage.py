"""Scan for and execute arbitrage opportunities"""
from main.workflows.check_arbitrage import scan_all_opportunities
from main.workflows.execute_arbitrage import execute_arbitrage
from main.jupiter.account.balance import check_balance as jupiter_check_balance
from main.bybit.account.balance import get_balance as bybit_get_balance

def run_arbitrage(direction, skip_confirmation=False):
    """
    Scan for profitable arbitrage opportunities and execute if found
    
    Args:
        direction: Direction to check ('B→J' or 'J→B')
        skip_confirmation: Skip manual confirmation prompts (default: False)
    
    Returns:
        dict with keys: 'initial_balance', 'final_balance', 'actual_profit',
                       'expected_profit', 'scan_result', 'execution_result', 'success'
    """
    if direction not in ['B→J', 'J→B']:
        raise ValueError(f"direction must be 'B→J' or 'J→B', got '{direction}'")
    
    if direction == 'B→J':
        initial_balance = bybit_get_balance("USDT", "UNIFIED")
    else:
        initial_balance = jupiter_check_balance("USDT")
    
    print(f"\n💰 Initial Balance: ${initial_balance:.2f}")
    
    result = {
        'initial_balance': initial_balance,
        'final_balance': None,
        'actual_profit': None,
        'expected_profit': None,
        'scan_result': None,
        'execution_result': None,
        'success': False
    }
    
    scan_result = scan_all_opportunities(initial_balance, direction)
    result['scan_result'] = scan_result
    
    if not scan_result:
        return result
    
    coin = scan_result['coin']
    expected_profit = scan_result['profit']
    result['expected_profit'] = expected_profit
    
    print(f"\n📈 预计收益: ${expected_profit:.2f} ({expected_profit/initial_balance:.2%})")
    
    execution_result = execute_arbitrage(coin, direction, skip_confirmation)
    result['execution_result'] = execution_result
    
    if direction == 'B→J':
        final_balance = jupiter_check_balance("USDT")
    else:
        final_balance = bybit_get_balance("USDT", "FUND")
    
    result['final_balance'] = final_balance
    actual_profit = final_balance - initial_balance
    result['actual_profit'] = actual_profit
    result['success'] = execution_result['success']
    
    print(f"\n{'='*50}")
    print(f"💰 Balance After: ${final_balance:.2f}")
    print(f"📊 实际收益: ${actual_profit:.2f} ({actual_profit/initial_balance:.2%})")
    print(f"{'='*50}")
    
    return result

