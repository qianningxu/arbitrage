from cal_profit import calculate_profit
from check_price import get_bybit_price, get_jupiter_price_lst
import json

def check_opportunity(bybit_symbol, amount=1):
    
    bybit_price = get_bybit_price(bybit_symbol)
    jupiter_prices = get_jupiter_price_lst(bybit_symbol, amount)
    
    if not jupiter_prices:
        return None
    
    best_opportunity = None
    
    for jupiter_result in jupiter_prices:
        jupiter_price = jupiter_result["price"]
        
        # Determine buy/sell prices
        buy_price = min(jupiter_price, bybit_price)
        sell_price = max(jupiter_price, bybit_price)
        direction = "BUY_DEX_SELL_CEX" if jupiter_price < bybit_price else "BUY_CEX_SELL_DEX"
        
        # Calculate profit
        net_profit = calculate_profit(buy_price, sell_price, amount*sell_price)
        
        if net_profit > 0:
            opportunity = {
                "symbol": bybit_symbol,
                "direction": direction,
                "bybit_price": bybit_price,
                "jupiter_price": jupiter_price,
                "jupiter_mint": jupiter_result["mint"],
                "net_profit_usd": net_profit,
            }
            
            if best_opportunity is None or net_profit > best_opportunity["net_profit_usd"]:
                best_opportunity = opportunity
    
    return best_opportunity

def scan_for_best():
    with open("files/monitor_pool.json", 'r') as f:
        data = json.load(f)
    bybit_symbols = [item['bybit_symbol'] for item in data]
    return bybit_symbols


if __name__ == "__main__":
    # opp = check_opportunity("TRUMPUSDT", 1)
    
    # if opp:
    #     print(opp)

    print(scan_for_best())