import os
import sys
import json
import requests

# Handle imports
try:
    from main.get_price.get_bybit_price import get_buy_rate, get_sell_rate
    from main.trade.bybit_auth import sign_request
    from main.trade.bybit_info import get_pair_info
    from main.trade.bybit_transfer import transfer_all_to_unified
except ModuleNotFoundError:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))
    from main.get_price.get_bybit_price import get_buy_rate, get_sell_rate
    from main.trade.bybit_auth import sign_request
    from main.trade.bybit_info import get_pair_info
    from main.trade.bybit_transfer import transfer_all_to_unified


def swap(in_coin, out_coin, amount, amount_unit):
    """Swap coins on Bybit - automatically transfers all FUND assets to UNIFIED before trading"""
    in_coin, out_coin = in_coin.upper(), out_coin.upper()
    
    # Transfer all assets from FUND to UNIFIED before trading
    transfer_all_to_unified()
    
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
    # swap('USDT', 'SOL', 10, 'in')    # Spend 10 USDT
    # swap('USDT', 'SOL', 0.05, 'out') # Buy 0.05 SOL
    # swap('SOL', 'USDT', 0.05, 'in')  # Sell 0.05 SOL
    pass
