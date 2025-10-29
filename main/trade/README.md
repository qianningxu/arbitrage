# Bybit Trading Module - Refactored Structure

## Overview
The Bybit trading functionality has been reorganized into modular files, with each file containing **≤ 3 functions** for better maintainability.

## File Structure

### Core Modules

#### 1. `bybit_auth.py` (1 function)
- `sign_request(param_str)` - Creates authentication signature for Bybit API

#### 2. `bybit_balance.py` (3 functions)
- `get_fund_balance(coin)` - Get balance in FUND account
- `get_unified_balance(coin)` - Get balance in UNIFIED account  
- `get_all_fund_balances()` - Get all non-zero balances in FUND account

#### 3. `bybit_transfer.py` (2 functions)
- `internal_transfer(coin, amount, from_account, to_account)` - Transfer between accounts
- `transfer_all_to_unified()` - **NEW**: Transfer ALL assets from FUND to UNIFIED

#### 4. `bybit_info.py` (2 functions)
- `_load_pairs()` - Load trading pairs from JSON (cached)
- `get_pair_info(symbol)` - Get trading pair information

#### 5. `bybit_swap.py` (1 function)
- `swap(in_coin, out_coin, amount, amount_unit)` - Execute spot trades
  - **Automatically transfers ALL funds from FUND to UNIFIED before trading**

### Test Files

#### Balance Tests
- `test_bybit_balance.py` - Tests for balance checking functions
- `test_bybit_transfer.py` - Tests for transfer functions
- `test_bybit_info.py` - Tests for pair info functions
- `test_bybit_auth.py` - Tests for authentication

#### Trading Tests
- `test_bybit_swap.py` - Swap execution test
- `test_bybit_swap_demo.py` - Demo showing balances and transfer flow

## Key Features

### 1. Automatic Fund Transfer
The `swap()` function now automatically calls `transfer_all_to_unified()` before trading:

```python
from main.trade.bybit_swap import swap

# This will automatically move ALL crypto from FUND to UNIFIED first
swap('SOL', 'USDT', 0.1, 'in')  # Sell 0.1 SOL for USDT
```

### 2. Separate Balance Functions
Two dedicated functions for checking balances:

```python
from main.trade.bybit_balance import get_fund_balance, get_unified_balance

fund_sol = get_fund_balance('SOL')      # Check FUND account
unified_sol = get_unified_balance('SOL') # Check UNIFIED account
```

### 3. Account Management
Easily manage funds between accounts:

```python
from main.trade.bybit_transfer import transfer_all_to_unified

# Transfer everything from FUND to UNIFIED
results = transfer_all_to_unified()
```

## Migration from Old Code

### Old Import (removed)
```python
from main.trade.bybit_helper import get_balance, sign_request, get_pair_info
```

### New Imports
```python
from main.trade.bybit_auth import sign_request
from main.trade.bybit_balance import get_fund_balance, get_unified_balance
from main.trade.bybit_info import get_pair_info
from main.trade.bybit_transfer import transfer_all_to_unified
```

## Benefits

1. **Modular Design**: Each file has ≤ 3 functions, making code easier to understand
2. **Clear Separation**: Auth, balance, transfer, and info functions are separated
3. **Automatic Management**: No need to manually transfer funds before trading
4. **Better Testing**: Separate test files for each module
5. **Type Safety**: Clear function names (get_fund_balance vs get_unified_balance)

## Usage Example

```python
# Check balances
from main.trade.bybit_balance import get_fund_balance, get_unified_balance

print(f"FUND: {get_fund_balance('SOL')} SOL")
print(f"UNIFIED: {get_unified_balance('SOL')} SOL")

# Execute swap (automatically handles transfers)
from main.trade.bybit_swap import swap

result = swap('SOL', 'USDT', 0.1, 'in')  # Sell 0.1 SOL
print(f"Order ID: {result['orderId']}")
```

