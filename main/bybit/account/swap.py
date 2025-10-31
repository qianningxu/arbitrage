"""Bybit spot trading"""
import json
import requests
from main.shared.config import BYBIT_API_BASE
from main.shared.data import get_pair_info
from main.bybit.helper.auth import sign_request
from main.bybit.monitor.pricing import get_sell_rate
from main.bybit.account.transfers import transfer_to_unified

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

def place_limit_order(symbol: str, side: str, qty: float, price: float, time_in_force: str = "GTC") -> dict:
    """Place a limit order
    
    Args:
        symbol: Trading pair symbol (e.g., SOLUSDT)
        side: Buy or Sell
        qty: Order quantity
        price: Limit price
        time_in_force: GTC (Good Till Cancel), IOC (Immediate or Cancel), FOK (Fill or Kill), PostOnly
    
    Returns:
        dict with 'status' key: 'success', 'failed', or 'cancelled'
    """
    params = {
        "category": "spot",
        "symbol": symbol,
        "side": side,
        "orderType": "Limit",
        "qty": str(qty),
        "price": str(price),
        "timeInForce": time_in_force
    }
    response = requests.post(
        f"{BYBIT_API_BASE}/v5/order/create",
        json=params,
        headers=sign_request(json.dumps(params))
    )
    data = response.json()
    if data.get("retCode") != 0:
        return {
            "status": "failed",
            "retCode": data.get("retCode"),
            "retMsg": data.get("retMsg")
        }
    return {
        "status": "success",
        **data["result"]
    }

def swap(in_coin: str, out_coin: str, amount: float, amount_unit: str = "in") -> dict:
    """Swap coins on Bybit spot market (requires funds in UNIFIED account)"""
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
            base_coin = info['base']
            avg_price = get_sell_rate(base_coin, 0.01)["rate"]
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

def crypto_to_u(crypto: str) -> dict:
    """Swap crypto to USDT (checks FUND, transfers to UNIFIED, then swaps)"""
    from main.bybit.account.balance import get_balance
    crypto = crypto.upper()
    fund_balance = get_balance(crypto, "FUND")
    if fund_balance <= 0:
        raise ValueError(f"No {crypto} balance in FUND account")
    print(f"📦 Found {fund_balance} {crypto} in FUND account")
    print(f"💱 Transferring to UNIFIED and swapping {fund_balance} {crypto} to USDT...")
    return swap(crypto, "USDT", fund_balance, "in")

def u_to_crypto(crypto: str, price: float) -> dict:
    """Use all USDT in UNIFIED to buy target crypto at specified price
    
    Args:
        crypto: Target crypto symbol (e.g., SOL)
        price: Limit price for the order
    """
    from main.bybit.account.balance import get_balance
    crypto = crypto.upper()
    usdt_balance = get_balance("USDT", "UNIFIED")
    if usdt_balance <= 0:
        raise ValueError("No USDT balance in UNIFIED account")
    
    symbol = f"{crypto}USDT"
    info = get_pair_info(symbol)
    if not info:
        raise ValueError(f"Trading pair {symbol} not found")
    
    qty = usdt_balance / price
    if info["precision"] >= 1:
        qty = int(qty)
    else:
        decimals = len(str(info["precision"]).split('.')[-1])
        qty = round(qty, decimals)
    
    if qty < info["minQty"]:
        raise ValueError(f"Quantity {qty} below minimum {info['minQty']}")
    
    print(f"💰 Found {usdt_balance} USDT in UNIFIED account")
    print(f"💱 Placing limit order: Buy {qty} {crypto} at {price} USDT (IOC)...")
    result = place_limit_order(symbol, "Buy", qty, price, "IOC")
    if result.get("status") == "success":
        print(f"✅ Order placed - Order ID: {result['orderId']}")
    else:
        print(f"❌ Order failed: {result.get('retMsg')}")
    return result

