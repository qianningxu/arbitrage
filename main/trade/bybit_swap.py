import os
import sys
import json
import requests

# Handle imports
try:
    from main.get_price.get_bybit_price import get_buy_rate, get_sell_rate
    from main.trade.bybit_auth import sign_request
    from main.trade.bybit_balance import check_balance
    from main.trade.bybit_info import get_pair_info
except ModuleNotFoundError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
    from main.get_price.get_bybit_price import get_buy_rate, get_sell_rate
    from main.trade.bybit_auth import sign_request
    from main.trade.bybit_balance import check_balance
    from main.trade.bybit_info import get_pair_info


def swap(in_coin, out_coin, amount, amount_unit):
    """Swap coins on Bybit"""
    in_coin, out_coin = in_coin.upper(), out_coin.upper()
    
    # Find pair
    for symbol, side in [(f"{out_coin}{in_coin}", "Buy"), (f"{in_coin}{out_coin}", "Sell")]:
        info = get_pair_info(symbol)
        if info:
            break
    else:
        raise ValueError(f"No pair for {in_coin}/{out_coin}")
    
    # Calculate qty
    if amount_unit == "in":
        if side == "Buy":
            avg_price = get_buy_rate(symbol, 0.01)
            qty = amount / (avg_price * 1.01)
        else:
            qty = amount
    else:
        if side == "Buy":
            qty = amount
        else:
            avg_price = get_sell_rate(symbol, 0.01)
            qty = amount / avg_price
    
    # Round qty
    qty = int(qty) if info["precision"] >= 1 else round(qty, len(str(info["precision"]).split('.')[-1]))
    
    if qty < info["minQty"]:
        raise ValueError(f"Qty {qty} below min {info['minQty']}")
    
    # Check balance
    if side == "Buy":
        avg_price = get_buy_rate(symbol, qty)
        check_balance(info["quote"], qty * avg_price * 1.01)
    else:
        check_balance(info["base"], qty)
    
    # Place order
    params = {"category": "spot", "symbol": symbol, "side": side, "orderType": "Market", "qty": str(qty)}
    response = requests.post(
        "https://api.bybit.com/v5/order/create",
        json=params,
        headers=sign_request(json.dumps(params))
    )
    
    data = response.json()
    if data.get("retCode") != 0:
        raise ValueError(f"Order failed: {data.get('retMsg')}")
    
    print(f"✅ {side} {qty} {info['base']} - Order: {data['result']['orderId']}")
    return data["result"]


if __name__ == "__main__":
    # Check balance example
    try:
        check_balance("USDT", 10)
        print("✅ Have 10 USDT")
    except ValueError as e:
        print(f"❌ {e}")
    
    # swap('USDT', 'SOL', 10, 'in')    # Spend 10 USDT
    # swap('USDT', 'SOL', 0.05, 'out') # Buy 0.05 SOL
    # swap('SOL', 'USDT', 0.05, 'in')  # Sell 0.05 SOL
