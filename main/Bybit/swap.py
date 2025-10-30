"""Bybit spot trading"""
import json
import requests
from main.shared.config import BYBIT_API_BASE
from main.shared.data import get_pair_info
from .auth import sign_request
from .pricing import get_buy_rate, get_sell_rate
from .transfers import transfer_to_unified

def place_market_order(symbol: str, side: str, qty: float, market_unit: str = None) -> dict:
    """Place a market order
    
    Args:
        symbol: Trading pair symbol (e.g., SOLUSDT)
        side: Buy or Sell
        qty: Order quantity
        market_unit: 'baseCoin' (qty in base) or 'quoteCoin' (qty in quote). For market orders only.
    """
    params = {
        "category": "spot",
        "symbol": symbol,
        "side": side,
        "orderType": "Market",
        "qty": str(qty)
    }
    if market_unit:
        params["marketUnit"] = market_unit
    response = requests.post(
        f"{BYBIT_API_BASE}/v5/order/create",
        json=params,
        headers=sign_request(json.dumps(params))
    )
    data = response.json()
    if data.get("retCode") != 0:
        raise ValueError(f"Order failed: {data.get('retMsg')}")
    return data["result"]

def swap(in_coin: str, out_coin: str, amount: float, amount_unit: str = "in") -> dict:
    """Swap coins on Bybit spot market"""
    in_coin, out_coin = in_coin.upper(), out_coin.upper()
    transfer_to_unified()
    symbol, side = None, None
    info = get_pair_info(f"{out_coin}{in_coin}")
    if info:
        symbol, side = f"{out_coin}{in_coin}", "Buy"
    else:
        info = get_pair_info(f"{in_coin}{out_coin}")
        if info:
            symbol, side = f"{in_coin}{out_coin}", "Sell"
    if not symbol:
        raise ValueError(f"No trading pair found for {in_coin}/{out_coin}")
    
    market_unit = None
    if amount_unit == "in":
        if side == "Buy":
            # For Buy orders, specify amount in quote currency (USDT) directly
            qty = amount
            market_unit = "quoteCoin"
        else:
            qty = amount
    else:
        if side == "Buy":
            qty = amount
        else:
            avg_price = get_sell_rate(symbol, 0.01)
            qty = amount / avg_price
    
    # Only apply precision/minQty checks when not using quoteCoin market unit
    if market_unit != "quoteCoin":
        if info["precision"] >= 1:
            qty = int(qty)
        else:
            decimals = len(str(info["precision"]).split('.')[-1])
            qty = round(qty, decimals)
        if qty < info["minQty"]:
            raise ValueError(f"Quantity {qty} below minimum {info['minQty']}")
    
    result = place_market_order(symbol, side, qty, market_unit)
    print(f"✅ {side} {qty} {'USDT' if market_unit == 'quoteCoin' else info['base']} - Order ID: {result['orderId']}")
    return result

def market_buy(symbol: str, qty: float) -> dict:
    """Place market buy order"""
    return place_market_order(symbol, "Buy", qty)

def market_sell(symbol: str, qty: float) -> dict:
    """Place market sell order"""
    return place_market_order(symbol, "Sell", qty)

def crypto_to_u(crypto: str) -> dict:
    """Transfer crypto from FUND to UNIFIED and swap all to USDT"""
    from .balance import get_balance
    crypto = crypto.upper()
    fund_balance = get_balance(crypto, "FUND")
    if fund_balance <= 0:
        raise ValueError(f"No {crypto} balance in FUND account")
    print(f"📦 Found {fund_balance} {crypto} in FUND account")
    transfer_to_unified(crypto)
    unified_balance = get_balance(crypto, "UNIFIED")
    if unified_balance <= 0:
        raise ValueError(f"Transfer failed: No {crypto} balance in UNIFIED account")
    print(f"💱 Swapping {unified_balance} {crypto} to USDT...")
    return swap(crypto, "USDT", unified_balance, "in")

def u_to_crypto(crypto: str) -> dict:
    """Use all USDT in UNIFIED to buy target crypto"""
    from .balance import get_balance
    crypto = crypto.upper()
    usdt_balance = get_balance("USDT", "UNIFIED")
    if usdt_balance <= 0:
        raise ValueError("No USDT balance in UNIFIED account")
    print(f"💰 Found {usdt_balance} USDT in UNIFIED account")
    print(f"💱 Swapping {usdt_balance} USDT to {crypto}...")
    return swap("USDT", crypto, usdt_balance, "in")

