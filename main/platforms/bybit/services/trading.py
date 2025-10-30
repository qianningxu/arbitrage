"""
Bybit trading services
"""
from main.core.data_loader import get_pair_info
from ..api.trading import place_market_order
from ..services.pricing import get_buy_rate, get_sell_rate
from ..services.transfer import transfer_to_unified


def swap(in_coin: str, out_coin: str, amount: float, amount_unit: str = "in") -> dict:
    """Swap coins on Bybit spot market
    
    Args:
        in_coin: Input coin symbol
        out_coin: Output coin symbol
        amount: Amount (interpretation depends on amount_unit)
        amount_unit: 'in' (spend amount of in_coin) or 'out' (receive amount of out_coin)
        
    Returns:
        dict: Order result
        
    Raises:
        ValueError: If trading pair not found or order fails
    """
    in_coin, out_coin = in_coin.upper(), out_coin.upper()
    
    # Auto-transfer from FUND to UNIFIED
    transfer_to_unified()
    
    # Find trading pair and side
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
    
    # Calculate quantity
    if amount_unit == "in":
        if side == "Buy":
            # Buying: spend in_coin, need to calculate base qty
            avg_price = get_buy_rate(symbol, 0.01)  # Sample rate
            qty = amount / (avg_price * 1.01)  # Buffer for slippage
        else:
            # Selling: base is in_coin, qty is amount
            qty = amount
    else:  # amount_unit == "out"
        if side == "Buy":
            # Buying: want out_coin, qty is amount
            qty = amount
        else:
            # Selling: want out_coin (quote), need to calculate base qty
            avg_price = get_sell_rate(symbol, 0.01)
            qty = amount / avg_price
    
    # Round quantity according to precision
    if info["precision"] >= 1:
        qty = int(qty)
    else:
        decimals = len(str(info["precision"]).split('.')[-1])
        qty = round(qty, decimals)
    
    # Check minimum quantity
    if qty < info["minQty"]:
        raise ValueError(f"Quantity {qty} below minimum {info['minQty']}")
    
    # Place order
    result = place_market_order(symbol, side, qty)
    print(f"✅ {side} {qty} {info['base']} - Order ID: {result['orderId']}")
    
    return result


def market_buy(symbol: str, qty: float) -> dict:
    """Place market buy order
    
    Args:
        symbol: Trading pair symbol
        qty: Quantity to buy
        
    Returns:
        dict: Order result
    """
    return place_market_order(symbol, "Buy", qty)


def market_sell(symbol: str, qty: float) -> dict:
    """Place market sell order
    
    Args:
        symbol: Trading pair symbol
        qty: Quantity to sell
        
    Returns:
        dict: Order result
    """
    return place_market_order(symbol, "Sell", qty)

