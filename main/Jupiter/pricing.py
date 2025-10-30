"""Jupiter pricing and quotes"""
import requests
from main.shared.data import get_token_info, bybit_symbol_to_mints, load_tokens

def get_quote(input_mint, output_mint, amount, slippage_bps=50):
    """Get swap quote from Jupiter"""
    response = requests.get("https://api.jup.ag/swap/v1/quote", params={
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": amount,
        "slippageBps": slippage_bps
    })
    data = response.json()
    return None if "error" in data else data

def get_exchange_rate(input_symbol, output_symbol, amount):
    """Get exchange rate between two tokens via Jupiter"""
    input_info = get_token_info(input_symbol)
    output_info = get_token_info(output_symbol)
    if not input_info or not output_info:
        return None
    input_mint = input_info["mint"]
    output_mint = output_info["mint"]
    input_decimals = input_info["decimals"]
    output_decimals = output_info["decimals"]
    amount_lamports = int(amount * (10 ** input_decimals))
    quote = get_quote(input_mint, output_mint, amount_lamports)
    if not quote:
        return None
    in_amt = quote.get("inAmount")
    out_amt = quote.get("outAmount")
    if not in_amt or not out_amt:
        return None
    return (float(out_amt) / (10 ** output_decimals)) / (float(in_amt) / (10 ** input_decimals))

def get_price_from_bybit_symbol(symbol):
    """Get Jupiter price using Bybit trading pair symbol"""
    mints = bybit_symbol_to_mints(symbol)
    if not mints:
        return None
    base_mint, quote_mint = mints
    tokens = load_tokens()
    input_symbol = None
    output_symbol = None
    for sym, data in tokens.items():
        if data and len(data) > 0:
            mint = data[0].get("mint")
            if mint == base_mint:
                input_symbol = sym
            if mint == quote_mint:
                output_symbol = sym
            if input_symbol and output_symbol:
                break
    if not input_symbol or not output_symbol:
        return None
    return get_exchange_rate(input_symbol, output_symbol, 1)

def get_recent_priority_fees():
    """Get recent prioritization fees for adaptive fee setting"""
    from .client import get_client
    client = get_client()
    try:
        fees_response = client.get_recent_prioritization_fees()
        if fees_response.value:
            fees = [f.prioritization_fee for f in fees_response.value]
            fees.sort()
            return {
                "min": min(fees) if fees else 0,
                "p50": fees[len(fees)//2] if fees else 0,
                "p75": fees[len(fees)*3//4] if fees else 0,
                "max": max(fees) if fees else 0
            }
    except:
        pass
    return {"min": 0, "p50": 0, "p75": 0, "max": 0}

