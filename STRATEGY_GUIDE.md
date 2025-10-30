# All-In Alternating Arbitrage Strategy Guide

## 🎯 Strategy Overview

**Key Principle**: Keep ALL funds on ONE exchange at a time to avoid withdrawal fees.

### How It Works

1. **All funds start on ONE exchange** (either Bybit or Solana)
2. **Check opportunities ONLY for the available path**:
   - Funds on Solana → Only check **Path A** (Jupiter buy → transfer → Bybit sell)
   - Funds on Bybit → Only check **Path B** (Bybit buy → withdraw → Jupiter sell)
3. **After arbitrage execution**, funds move to the OTHER exchange
4. **Next opportunity** will automatically use the opposite path
5. **No rebalancing withdrawals** → No unnecessary fees!

### Path Alternation

```
Initial State: Funds on Solana
    ↓
Path A: Jupiter buy W → Transfer to Bybit → Bybit sell W
    ↓
Funds now on Bybit
    ↓
Path B: Bybit buy W → Withdraw to Solana → Jupiter sell W
    ↓
Funds now on Solana
    ↓
(Cycle repeats...)
```

## 📋 Usage

### 1. Check Current Funds Location

```python
from main.workflows.arbitrage.strategy_executor import detect_funds_location

# Check where your funds are
location = detect_funds_location()
print(f"Funds on: {location['location']}")
print(f"Total USDT: ${location['total_usdt']:.2f}")
```

### 2. Check for Arbitrage Opportunity

```python
from main.workflows.arbitrage.strategy_executor import check_arbitrage_opportunity

# Check opportunities (automatically uses correct path based on funds location)
opportunity = check_arbitrage_opportunity(
    coins=['SOL', 'ETH', 'BTC'],
    min_profit_threshold=0.5  # Minimum $0.50 profit
)

if opportunity['has_opportunity']:
    print(f"Found opportunity on Path {opportunity['available_path']}")
    print(f"Coin: {opportunity['opportunity']['coin']}")
    print(f"Profit: ${opportunity['opportunity']['profit_usdt']:.2f}")
```

### 3. Execute Arbitrage (Dry Run First!)

```python
from main.workflows.arbitrage.strategy_executor import execute_arbitrage

# Always test with dry_run=True first!
result = execute_arbitrage(opportunity, dry_run=True)
print(result['message'])

# When ready for real trading:
# result = execute_arbitrage(opportunity, dry_run=False)
```

### 4. Run Continuous Monitoring Loop

```python
from main.workflows.arbitrage.strategy_executor import run_arbitrage_loop

# Run in dry-run mode (safe)
run_arbitrage_loop(
    coins=['SOL', 'ETH', 'BTC'],
    min_profit_threshold=0.5,
    check_interval=30,  # Check every 30 seconds
    dry_run=True  # Don't execute real trades
)

# For live trading (when ready):
# run_arbitrage_loop(
#     coins=['SOL', 'ETH'],
#     min_profit_threshold=1.0,
#     check_interval=60,
#     dry_run=False
# )
```

## 🔧 Utility Functions

### Consolidate Funds (If Needed)

If funds get split between exchanges, consolidate them:

```python
from main.workflows.arbitrage.consolidate_funds import (
    consolidate_to_bybit,
    consolidate_to_solana,
    consolidate_to_usdt_on_bybit,
    consolidate_to_usdt_on_solana
)

# Move all funds to Bybit
consolidate_to_bybit()

# Move all funds to Solana
consolidate_to_solana()

# Convert all coins to USDT on Bybit
consolidate_to_usdt_on_bybit()

# Convert all coins to USDT on Solana
consolidate_to_usdt_on_solana()
```

## 📊 Expected Workflow

### Scenario 1: Funds on Solana, Find Path A Opportunity

```
1. Bot detects funds on Solana
2. Checks only Path A opportunities
3. Finds profitable SOL opportunity
4. Executes:
   a. Buy SOL on Jupiter with all USDT
   b. Transfer SOL to Bybit
   c. Sell SOL on Bybit for USDT
5. All USDT now on Bybit
6. Next iteration will check Path B
```

### Scenario 2: Funds on Bybit, Find Path B Opportunity

```
1. Bot detects funds on Bybit
2. Checks only Path B opportunities
3. Finds profitable ETH opportunity
4. Executes:
   a. Buy ETH on Bybit with all USDT
   b. Withdraw ETH to Solana
   c. Sell ETH on Jupiter for USDT
5. All USDT now on Solana
6. Next iteration will check Path A
```

## ⚠️ Important Notes

### Fee Optimization

- **Withdrawal fee paid ONLY during arbitrage** (not for rebalancing)
- **No back-and-forth transfers** (funds stay on one side until next arb)
- **Path alternates naturally** (each arb moves funds to other side)

### Safety Features

1. **Dry-run mode by default** - Test without risk
2. **Minimum profit threshold** - Don't trade for tiny profits
3. **Automatic path selection** - Can't execute wrong path
4. **Split detection** - Warns if funds are split between exchanges

### Best Practices

1. **Start with dry-run mode** to understand the flow
2. **Set conservative profit thresholds** (e.g., $1-2 minimum)
3. **Monitor first few executions** to verify everything works
4. **Keep some SOL** on Solana side for transaction fees (~0.01 SOL)
5. **Check withdrawal fee** before executing to ensure profitability

## 🧪 Testing

```bash
# Activate environment
source venv/bin/activate

# Test fund detection
python test/workflows/test_arbitrage_strategy.py

# Or test individual functions
python -c "
from main.workflows.arbitrage.strategy_executor import detect_funds_location
location = detect_funds_location()
print(f'Funds on: {location[\"location\"]}')
print(f'Total: \${location[\"total_usdt\"]:.2f}')
"
```

## 🚀 Quick Start

```python
# 1. Check where funds are
from main.workflows.arbitrage.strategy_executor import detect_funds_location
location = detect_funds_location()
print(f"Your funds are on: {location['location']}")

# 2. Check for opportunities
from main.workflows.arbitrage.strategy_executor import check_arbitrage_opportunity
opp = check_arbitrage_opportunity(['SOL'], min_profit_threshold=0.5)

if opp['has_opportunity']:
    print(f"✅ Opportunity found!")
    print(f"Path: {opp['available_path']}")
    print(f"Profit: ${opp['opportunity']['profit_usdt']:.2f}")
    
    # 3. Execute (dry run)
    from main.workflows.arbitrage.strategy_executor import execute_arbitrage
    result = execute_arbitrage(opp, dry_run=True)
    print(result['message'])
else:
    print(f"❌ {opp['message']}")
```

---

**Your strategy is now fully implemented and ready to use!** 🎉

