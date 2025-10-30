"""
Arbitrage opportunity detection

Based on fee categorization:
- c₁: Solana fixed costs (base fee 5000 lamports + priority fee + ATA creation if needed)
- c₂: Bybit withdrawal fee (fixed by coin)
- f: Bybit trading fee (percentage)
- R₁: Jupiter exchange rate (from outAmount, already includes LP/DEX fees)
- R₂: Bybit exchange rate (from ticker/orderbook)
- s: Bid-ask spread
- ε: Slippage/impact
"""
from main.shared.config import SOLANA_BASE_FEE_LAMPORTS
from main.shared.data import get_withdrawal_fee, get_token_info
from main.Bybit.pricing import get_spread, get_buy_rate, get_sell_rate
from main.Jupiter.pricing import get_quote, get_recent_priority_fees
from main.Jupiter.balance import has_ata


def calculate_path_a_profit(
    coin_symbol: str,
    usdt_amount: float,
    bybit_fee_rate: float = 0.001,
    slippage_eps: float = 0.002,
    min_profit_threshold: float = 0.1
) -> dict:
    """
    Calculate profit for Path A: Jupiter buy W → Bybit sell W → USDT
    
    Formula:
    Δ_USDT = [W_received × R₂_real × (1 - f) - c₂] - c₁ - U
    
    Args:
        coin_symbol: Coin to arbitrage (e.g., 'SOL')
        usdt_amount: Amount of USDT to invest
        bybit_fee_rate: Bybit trading fee rate (default: 0.1%)
        slippage_eps: Expected slippage/impact (default: 0.2%)
        min_profit_threshold: Minimum profit in USDT to consider (default: 0.1)
        
    Returns:
        dict: {
            "path": "A",
            "coin": str,
            "profitable": bool,
            "profit_usdt": float,
            "profit_pct": float,
            "details": {...}
        }
    """
    coin_symbol = coin_symbol.upper()
    
    # Get token info
    coin_info = get_token_info(coin_symbol)
    usdt_info = get_token_info("USDT")
    if not coin_info or not usdt_info:
        return {"path": "A", "coin": coin_symbol, "profitable": False, "error": "Token not found"}
    
    # Step 1: Jupiter buy (R₁, β from Quote; outAmount includes LP/DEX fees)
    usdt_lamports = int(usdt_amount * (10 ** usdt_info["decimals"]))
    quote = get_quote(usdt_info["mint"], coin_info["mint"], usdt_lamports, slippage_bps=50)
    
    if not quote:
        return {"path": "A", "coin": coin_symbol, "profitable": False, "error": "Failed to get Jupiter quote"}
    
    W_received = float(quote["outAmount"]) / (10 ** coin_info["decimals"])
    
    # Step 2: Bybit sell (R₂_real considering spread and slippage)
    try:
        symbol = f"{coin_symbol}USDT"
        spread_info = get_spread(symbol)
        R2_mid = spread_info["mid"]
        s = spread_info["spread_pct"]
        
        # Real rate: mid price minus half spread and slippage
        R2_real_sell = R2_mid * (1 - s/2 - slippage_eps)
        
        # After Bybit sell
        usdt_from_bybit = W_received * R2_real_sell * (1 - bybit_fee_rate)
        
    except Exception as e:
        return {"path": "A", "coin": coin_symbol, "profitable": False, "error": f"Bybit error: {str(e)}"}
    
    # Step 3: Calculate costs
    # c₁: Solana costs
    priority_fees = get_recent_priority_fees()
    priority_fee = priority_fees["p75"]  # Use 75th percentile
    c1_lamports = SOLANA_BASE_FEE_LAMPORTS + priority_fee
    
    # Check if ATA needed (one-time cost)
    if not has_ata(coin_info["mint"]):
        c1_lamports += 2039280  # Rent-exempt deposit for ATA (~0.002 SOL)
    
    c1_usdt = (c1_lamports / 1e9) * R2_mid  # Convert SOL cost to USDT
    
    # c₂: Bybit withdrawal fee (if withdrawing from Bybit)
    c2 = get_withdrawal_fee(coin_symbol) or 0
    c2_usdt = c2 * R2_mid if c2 > 0 else 0
    
    # Step 4: Calculate profit
    profit_usdt = usdt_from_bybit - c2_usdt - c1_usdt - usdt_amount
    profit_pct = (profit_usdt / usdt_amount) * 100 if usdt_amount > 0 else 0
    profitable = profit_usdt > min_profit_threshold
    
    return {
        "path": "A",
        "coin": coin_symbol,
        "profitable": profitable,
        "profit_usdt": profit_usdt,
        "profit_pct": profit_pct,
        "details": {
            "usdt_invest": usdt_amount,
            "w_received_jupiter": W_received,
            "bybit_rate": R2_real_sell,
            "usdt_from_bybit": usdt_from_bybit,
            "c1_solana_lamports": c1_lamports,
            "c1_usdt": c1_usdt,
            "c2_withdrawal_usdt": c2_usdt,
            "total_costs": c1_usdt + c2_usdt
        }
    }


def calculate_path_b_profit(
    coin_symbol: str,
    usdt_amount: float,
    bybit_fee_rate: float = 0.001,
    slippage_eps: float = 0.002,
    min_profit_threshold: float = 0.1
) -> dict:
    """
    Calculate profit for Path B: Bybit buy W → Jupiter sell W → USDT
    
    Formula:
    W' = (U / R₂_real_buy) × (1 - f)
    W'' = W' - c₂_W  (if withdrawal needed)
    USDT_recv = outAmount(W'') - c₁
    Δ_USDT = USDT_recv - U
    
    Args:
        coin_symbol: Coin to arbitrage (e.g., 'SOL')
        usdt_amount: Amount of USDT to invest
        bybit_fee_rate: Bybit trading fee rate (default: 0.1%)
        slippage_eps: Expected slippage/impact (default: 0.2%)
        min_profit_threshold: Minimum profit in USDT to consider (default: 0.1)
        
    Returns:
        dict: Similar to path_a_profit
    """
    coin_symbol = coin_symbol.upper()
    
    # Get token info
    coin_info = get_token_info(coin_symbol)
    usdt_info = get_token_info("USDT")
    if not coin_info or not usdt_info:
        return {"path": "B", "coin": coin_symbol, "profitable": False, "error": "Token not found"}
    
    # Step 1: Bybit buy (R₂_real considering spread and slippage)
    try:
        symbol = f"{coin_symbol}USDT"
        spread_info = get_spread(symbol)
        R2_mid = spread_info["mid"]
        s = spread_info["spread_pct"]
        
        # Real rate: mid price plus half spread and slippage
        R2_real_buy = R2_mid * (1 + s/2 + slippage_eps)
        
        # After Bybit buy
        W_prime = (usdt_amount / R2_real_buy) * (1 - bybit_fee_rate)
        
        # After withdrawal (if needed)
        c2_w = get_withdrawal_fee(coin_symbol) or 0
        W_double_prime = W_prime - c2_w
        
        if W_double_prime <= 0:
            return {"path": "B", "coin": coin_symbol, "profitable": False, "error": "Amount too small after withdrawal fee"}
        
    except Exception as e:
        return {"path": "B", "coin": coin_symbol, "profitable": False, "error": f"Bybit error: {str(e)}"}
    
    # Step 2: Jupiter sell (outAmount includes LP/DEX fees)
    W_lamports = int(W_double_prime * (10 ** coin_info["decimals"]))
    quote = get_quote(coin_info["mint"], usdt_info["mint"], W_lamports, slippage_bps=50)
    
    if not quote:
        return {"path": "B", "coin": coin_symbol, "profitable": False, "error": "Failed to get Jupiter quote"}
    
    usdt_from_jupiter = float(quote["outAmount"]) / (10 ** usdt_info["decimals"])
    
    # Step 3: Calculate costs
    priority_fees = get_recent_priority_fees()
    priority_fee = priority_fees["p75"]
    c1_lamports = SOLANA_BASE_FEE_LAMPORTS + priority_fee
    
    if not has_ata(usdt_info["mint"]):
        c1_lamports += 2039280
    
    c1_usdt = (c1_lamports / 1e9) * R2_mid
    
    # Step 4: Calculate profit
    usdt_received = usdt_from_jupiter - c1_usdt
    profit_usdt = usdt_received - usdt_amount
    profit_pct = (profit_usdt / usdt_amount) * 100 if usdt_amount > 0 else 0
    profitable = profit_usdt > min_profit_threshold
    
    return {
        "path": "B",
        "coin": coin_symbol,
        "profitable": profitable,
        "profit_usdt": profit_usdt,
        "profit_pct": profit_pct,
        "details": {
            "usdt_invest": usdt_amount,
            "bybit_rate": R2_real_buy,
            "w_after_buy": W_prime,
            "c2_withdrawal": c2_w,
            "w_after_withdrawal": W_double_prime,
            "usdt_from_jupiter": usdt_from_jupiter,
            "c1_solana_lamports": c1_lamports,
            "c1_usdt": c1_usdt,
            "usdt_received": usdt_received
        }
    }


def find_best_opportunity(
    coins: list,
    usdt_amount: float,
    bybit_fee_rate: float = 0.001,
    min_profit_threshold: float = 0.1
) -> dict:
    """
    Scan multiple coins and find best arbitrage opportunity
    
    Args:
        coins: List of coin symbols to check (e.g., ['SOL', 'ETH', 'BTC'])
        usdt_amount: Amount of USDT to invest
        bybit_fee_rate: Bybit trading fee rate
        min_profit_threshold: Minimum profit threshold
        
    Returns:
        dict: Best opportunity with path, coin, and profit details
    """
    best_opportunity = None
    max_profit = min_profit_threshold
    
    for coin in coins:
        # Check both paths
        path_a = calculate_path_a_profit(coin, usdt_amount, bybit_fee_rate, min_profit_threshold=min_profit_threshold)
        path_b = calculate_path_b_profit(coin, usdt_amount, bybit_fee_rate, min_profit_threshold=min_profit_threshold)
        
        # Find best
        for result in [path_a, path_b]:
            if result.get("profitable") and result.get("profit_usdt", 0) > max_profit:
                max_profit = result["profit_usdt"]
                best_opportunity = result
    
    return best_opportunity or {"profitable": False, "message": "No profitable opportunities found"}

