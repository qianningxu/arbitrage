"""
All-in alternating arbitrage strategy execution

Strategy: Keep all funds on ONE exchange at a time to avoid withdrawal fees
- If funds on Solana → Execute Path A only (Jupiter buy → transfer to Bybit)
- If funds on Bybit → Execute Path B only (Bybit buy → withdraw to Solana)
"""
import json
from main.Bybit.balance import get_all_fund_balances, get_all_unified_balances
from main.Bybit.transfers import transfer_to_fund
from main.Jupiter.balance import check_balance
from .opportunity_detector import calculate_path_a_profit, calculate_path_b_profit


def detect_funds_location() -> dict:
    """Detect where funds are currently stored
    
    Returns:
        dict: {
            "location": "bybit" | "solana" | "both" | "none",
            "bybit_usdt": float,
            "solana_usdt": float,
            "total_usdt": float
        }
    """
    # Check Bybit (FUND + UNIFIED)
    fund_balances = get_all_fund_balances()
    unified_balances = get_all_unified_balances()
    bybit_usdt = fund_balances.get("USDT", 0) + unified_balances.get("USDT", 0)
    
    # Check Solana
    try:
        solana_usdt = check_balance("USDT")
    except:
        solana_usdt = 0
    
    total_usdt = bybit_usdt + solana_usdt
    
    # Determine location (threshold: 10 USDT to account for small dust)
    if bybit_usdt > 10 and solana_usdt < 10:
        location = "bybit"
    elif solana_usdt > 10 and bybit_usdt < 10:
        location = "solana"
    elif bybit_usdt > 10 and solana_usdt > 10:
        location = "both"  # Split - not ideal for strategy
    else:
        location = "none"
    
    return {
        "location": location,
        "bybit_usdt": bybit_usdt,
        "solana_usdt": solana_usdt,
        "total_usdt": total_usdt
    }


def check_arbitrage_opportunity(
    coins: list,
    min_profit_threshold: float = 0.5,
    bybit_fee_rate: float = 0.001
) -> dict:
    """Check for arbitrage opportunity based on current funds location
    
    This implements the all-in alternating strategy:
    - If funds on Solana → Only check Path A (Jupiter → Bybit)
    - If funds on Bybit → Only check Path B (Bybit → Solana)
    
    Args:
        coins: List of coins to check (e.g., ['SOL', 'ETH', 'BTC'])
        min_profit_threshold: Minimum profit in USDT
        bybit_fee_rate: Bybit trading fee rate
        
    Returns:
        dict: {
            "has_opportunity": bool,
            "funds_location": str,
            "available_path": str,  # "A" or "B" only
            "opportunity": dict or None,
            "message": str
        }
    """
    # Step 1: Detect funds location
    funds_info = detect_funds_location()
    location = funds_info["location"]
    usdt_amount = funds_info["total_usdt"]
    
    print(f"\n{'='*60}")
    print(f"💰 FUNDS LOCATION: {location.upper()}")
    print(f"{'='*60}")
    print(f"Bybit USDT: {funds_info['bybit_usdt']:.2f}")
    print(f"Solana USDT: {funds_info['solana_usdt']:.2f}")
    print(f"Total USDT: {usdt_amount:.2f}")
    print(f"{'='*60}\n")
    
    # Step 2: Check based on location
    if location == "none":
        return {
            "has_opportunity": False,
            "funds_location": location,
            "available_path": None,
            "opportunity": None,
            "message": "No USDT funds found on either exchange"
        }
    
    if location == "both":
        return {
            "has_opportunity": False,
            "funds_location": location,
            "available_path": None,
            "opportunity": None,
            "message": "⚠️  Funds split between exchanges - consolidate first!"
        }
    
    # Step 3: Check appropriate path based on location
    best_opportunity = None
    max_profit = min_profit_threshold
    
    if location == "solana":
        # Funds on Solana → Only Path A available (Jupiter buy → Bybit sell)
        print("🔍 Checking Path A opportunities (Jupiter → Bybit)...")
        available_path = "A"
        
        for coin in coins:
            result = calculate_path_a_profit(
                coin,
                usdt_amount,
                bybit_fee_rate,
                min_profit_threshold=min_profit_threshold
            )
            
            if result.get("profitable") and result.get("profit_usdt", 0) > max_profit:
                max_profit = result["profit_usdt"]
                best_opportunity = result
                print(f"  ✅ {coin}: Profit ${result['profit_usdt']:.2f} ({result['profit_pct']:.2f}%)")
            else:
                print(f"  ❌ {coin}: Not profitable")
    
    elif location == "bybit":
        # Funds on Bybit → Only Path B available (Bybit buy → Jupiter sell)
        print("🔍 Checking Path B opportunities (Bybit → Jupiter)...")
        available_path = "B"
        
        for coin in coins:
            result = calculate_path_b_profit(
                coin,
                usdt_amount,
                bybit_fee_rate,
                min_profit_threshold=min_profit_threshold
            )
            
            if result.get("profitable") and result.get("profit_usdt", 0) > max_profit:
                max_profit = result["profit_usdt"]
                best_opportunity = result
                print(f"  ✅ {coin}: Profit ${result['profit_usdt']:.2f} ({result['profit_pct']:.2f}%)")
            else:
                print(f"  ❌ {coin}: Not profitable")
    
    # Step 4: Return result
    if best_opportunity:
        return {
            "has_opportunity": True,
            "funds_location": location,
            "available_path": available_path,
            "opportunity": best_opportunity,
            "message": f"Found profitable opportunity on Path {available_path}"
        }
    else:
        return {
            "has_opportunity": False,
            "funds_location": location,
            "available_path": available_path,
            "opportunity": None,
            "message": f"No profitable opportunities on Path {available_path}"
        }


def execute_arbitrage(opportunity: dict, dry_run: bool = True) -> dict:
    """Execute arbitrage based on opportunity
    
    Args:
        opportunity: Opportunity from check_arbitrage_opportunity()
        dry_run: If True, don't execute real trades (default: True for safety)
        
    Returns:
        dict: Execution result
    """
    if not opportunity.get("has_opportunity"):
        return {"success": False, "message": "No opportunity to execute"}
    
    path = opportunity["available_path"]
    opp = opportunity["opportunity"]
    coin = opp["coin"]
    
    print(f"\n{'='*60}")
    print(f"🚀 EXECUTING ARBITRAGE - PATH {path}")
    print(f"{'='*60}")
    print(f"Coin: {coin}")
    print(f"Expected Profit: ${opp['profit_usdt']:.2f} ({opp['profit_pct']:.2f}%)")
    print(f"{'='*60}\n")
    
    if dry_run:
        print("⚠️  DRY RUN MODE - No real trades executed")
        return {
            "success": True,
            "dry_run": True,
            "path": path,
            "coin": coin,
            "expected_profit": opp["profit_usdt"],
            "message": "Dry run completed successfully"
        }
    
    # Real execution
    try:
        if path == "A":
            # Path A: Jupiter buy → Transfer to Bybit → Bybit sell
            from main.Jupiter.swap import swap as jupiter_swap
            from main.workflows.transfers.bridge import transfer_to_bybit
            from main.Bybit.swap import swap as bybit_swap
            
            usdt_amount = opp["details"]["usdt_invest"]
            
            print("Step 1: Buy on Jupiter...")
            tx1 = jupiter_swap("USDT", coin, usdt_amount)
            
            print("Step 2: Transfer to Bybit...")
            w_received = opp["details"]["w_received_jupiter"]
            tx2 = transfer_to_bybit(coin, w_received)
            
            print("Step 3: Sell on Bybit...")
            result = bybit_swap(coin, "USDT", w_received, "in")
            
            return {
                "success": True,
                "dry_run": False,
                "path": "A",
                "coin": coin,
                "transactions": [tx1, tx2, result],
                "message": "Path A executed successfully - funds now on Bybit"
            }
        
        else:  # path == "B"
            # Path B: Bybit buy → Withdraw to Solana → Jupiter sell
            from main.Bybit.swap import swap as bybit_swap
            from main.workflows.transfers.bridge import transfer_to_solana
            from main.Jupiter.swap import swap as jupiter_swap
            
            # First move UNIFIED → FUND for withdrawal
            print("Step 0: Move funds to FUND account...")
            transfer_to_fund()
            
            usdt_amount = opp["details"]["usdt_invest"]
            
            print("Step 1: Buy on Bybit...")
            result1 = bybit_swap("USDT", coin, usdt_amount, "in")
            
            print("Step 2: Withdraw to Solana...")
            w_amount = opp["details"]["w_after_buy"]
            tx2 = transfer_to_solana(coin, w_amount)
            
            print("Step 3: Sell on Jupiter...")
            w_final = opp["details"]["w_after_withdrawal"]
            tx3 = jupiter_swap(coin, "USDT", w_final)
            
            return {
                "success": True,
                "dry_run": False,
                "path": "B",
                "coin": coin,
                "transactions": [result1, tx2, tx3],
                "message": "Path B executed successfully - funds now on Solana"
            }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Execution failed: {str(e)}"
        }


def run_arbitrage_loop(
    coins: list = ['SOL', 'ETH', 'BTC'],
    min_profit_threshold: float = 0.5,
    check_interval: int = 10,
    max_iterations: int = None,
    dry_run: bool = True
):
    """Run continuous arbitrage monitoring loop
    
    Args:
        coins: Coins to monitor
        min_profit_threshold: Minimum profit in USDT
        check_interval: Seconds between checks
        max_iterations: Maximum iterations (None for infinite)
        dry_run: If True, don't execute real trades
    """
    import time
    
    iteration = 0
    print(f"\n{'='*60}")
    print(f"🤖 ARBITRAGE BOT STARTED")
    print(f"{'='*60}")
    print(f"Coins: {', '.join(coins)}")
    print(f"Min Profit: ${min_profit_threshold}")
    print(f"Check Interval: {check_interval}s")
    print(f"Mode: {'DRY RUN' if dry_run else 'LIVE TRADING'}")
    print(f"{'='*60}\n")
    
    try:
        while max_iterations is None or iteration < max_iterations:
            iteration += 1
            print(f"\n[Iteration {iteration}] Checking opportunities...")
            
            # Check for opportunity
            opportunity = check_arbitrage_opportunity(coins, min_profit_threshold)
            
            if opportunity["has_opportunity"]:
                print(f"\n✅ OPPORTUNITY FOUND!")
                print(json.dumps(opportunity["opportunity"], indent=2))
                
                # Execute
                result = execute_arbitrage(opportunity, dry_run=dry_run)
                print(f"\n📊 Result: {result['message']}")
                
                if not dry_run and result["success"]:
                    print(f"\n⚠️  Funds location changed - next iteration will use opposite path")
            else:
                print(f"\n❌ {opportunity['message']}")
            
            # Wait before next check
            if max_iterations is None or iteration < max_iterations:
                print(f"\n⏳ Waiting {check_interval}s before next check...")
                time.sleep(check_interval)
    
    except KeyboardInterrupt:
        print(f"\n\n⚠️  Bot stopped by user")
    except Exception as e:
        print(f"\n\n❌ Bot error: {str(e)}")


if __name__ == "__main__":
    # Example: Check current opportunity
    opportunity = check_arbitrage_opportunity(['SOL'], min_profit_threshold=0.1)
    print(json.dumps(opportunity, indent=2, default=str))
    
    # Example: Run loop (dry run)
    # run_arbitrage_loop(
    #     coins=['SOL', 'ETH'],
    #     min_profit_threshold=0.5,
    #     check_interval=30,
    #     dry_run=True
    # )

