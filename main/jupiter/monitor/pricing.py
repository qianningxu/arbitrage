"""Jupiter pricing and quotes"""
import requests
from main.shared.data import get_token_info

def get_quote(input_mint, output_mint, amount, slippage_bps=50):
    """Get swap quote from Jupiter"""
    try:
        response = requests.get("https://lite-api.jup.ag/swap/v1/quote", params={
            "inputMint": input_mint,
            "outputMint": output_mint,
            "amount": amount,
            "slippageBps": slippage_bps
        }, timeout=10)
        
        if response.status_code != 200:
            return None
        data = response.json()
        return None if "error" in data else data
    except:
        return None

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

def get_price_from_bybit_symbol(symbol, amount):
    """Get Jupiter price using Bybit trading pair symbol
    Args:
        symbol: Bybit symbol like 'SOLUSDT'
        amount: Amount in USDT
    Returns:
        Price in USDT or None
    """
    # Extract base coin from symbol (e.g., 'SOL' from 'SOLUSDT')
    if symbol.endswith("USDT"):
        base_symbol = symbol[:-4]
    elif symbol.endswith("USDC"):
        base_symbol = symbol[:-4]
    else:
        return None
    
    # Get exchange rate: base -> USDT
    rate = get_exchange_rate(base_symbol, "USDT", 1)
    return rate
