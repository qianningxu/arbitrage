# Functions Reference

## shared/

### config.py
- **get_env_var(key, required=True)** - Get environment variable
- **get_solana_keypair()** - Get Solana keypair from env
- **get_bybit_credentials()** - Get Bybit API credentials from env

### data.py
- **load_tokens(force_reload=False)** - Load token metadata (cached)
- **load_pairs(force_reload=False)** - Load trading pairs (cached)
- **load_withdrawal_fees(force_reload=False)** - Load withdrawal fees (cached)
- **get_token_info(symbol)** - Get token info by symbol
- **get_pair_info(symbol)** - Get trading pair info by symbol
- **get_withdrawal_fee(coin)** - Get withdrawal fee for coin
- **symbol_to_mint(symbol)** - Convert symbol to mint address
- **mint_to_symbol(mint)** - Convert mint address to symbol
- **bybit_symbol_to_mints(symbol)** - Convert Bybit pair symbol to mint addresses

---

## Bybit/

### helper/auth.py
- **sign_request(param_str)** - Create signature headers for Bybit API
- **create_headers(params=None)** - Create authenticated headers

### monitor/pricing.py
- **get_orderbook(symbol, depth=100)** - Get orderbook from Bybit
- **get_ticker(symbol)** - Get ticker with best bid/ask
- **get_buy_rate(symbol, qty, depth=100)** - Calculate average buy rate from orderbook
- **get_sell_rate(symbol, qty, depth=100)** - Calculate average sell rate from orderbook
- **get_mid_price(symbol)** - Get mid price (average of bid/ask)
- **get_spread(symbol)** - Get bid-ask spread information

### account/balance.py
- **get_balance(coin, account_type)** - Get balance for specific coin in account
- **get_all_balances(account_type)** - Get all non-zero balances in account
- **get_fund_balance(coin)** - Get balance in FUND account
- **get_unified_balance(coin)** - Get balance in UNIFIED account
- **get_total_balance(coin)** - Get total balance across all accounts
- **get_all_fund_balances()** - Get all balances in FUND
- **get_all_unified_balances()** - Get all balances in UNIFIED

### account/swap.py
- **place_market_order(symbol, side, qty, market_unit=None)** - Place market order (market_unit: 'baseCoin' or 'quoteCoin')
- **swap(in_coin, out_coin, amount, amount_unit="in")** - Swap coins on Bybit (uses quoteCoin for BUY orders)
- **market_buy(symbol, qty)** - Place market buy order
- **market_sell(symbol, qty)** - Place market sell order
- **crypto_to_u(crypto)** - Transfer crypto from FUND to UNIFIED and swap to USDT
- **u_to_crypto(crypto)** - Use all USDT in UNIFIED to buy crypto

### account/transfers.py
- **internal_transfer(coin, amount, from_account, to_account)** - Transfer between Bybit accounts
- **transfer_to_fund(coin=None, amount=None)** - Transfer from UNIFIED to FUND
- **transfer_to_unified(coin=None, amount=None)** - Transfer from FUND to UNIFIED
- **get_deposit_address(coin, chain="SOL")** - Get deposit address
- **create_withdrawal(coin, amount, address, chain="SOL")** - Create withdrawal request
- **withdraw(symbol, chain="SOL")** - Withdraw all funds of a symbol to Jupiter wallet (transfers from UNIFIED to FUND, deducts withdrawal fee, then withdraws)

---

## Jupiter/

### helper/client.py
- **get_client()** - Get Solana RPC client (cached singleton)
- **get_keypair()** - Get Solana keypair
- **get_address()** - Get Solana wallet address

### monitor/pricing.py
- **get_quote(input_mint, output_mint, amount, slippage_bps=50)** - Get swap quote from Jupiter
- **get_exchange_rate(input_symbol, output_symbol, amount)** - Get exchange rate between tokens
- **get_price_from_bybit_symbol(symbol)** - Get Jupiter price using Bybit symbol

### account/balance.py
- **get_sol_balance()** - Get SOL balance
- **get_token_balance(symbol)** - Get token balance for symbol
- **check_balance(symbol)** - Check balance (alias)
- **has_ata(mint_address)** - Check if wallet has ATA for mint

### account/swap.py
- **execute_swap(quote, priority_fee_lamports=None)** - Execute swap with quote
- **swap(input_symbol, output_symbol, amount, slippage_bps=50, auto_priority_fee=True)** - Swap tokens via Jupiter
- **crypto_to_u(crypto, slippage_bps=50, auto_priority_fee=True)** - Swap all crypto to USDT
- **u_to_crypto(crypto, slippage_bps=50, auto_priority_fee=True)** - Swap all USDT to crypto

### account/transfers.py
- **send_sol(destination, amount)** - Send native SOL
- **send_token(mint_address, destination, amount, decimals)** - Send SPL token
- **withdraw(symbol, chain="SOL")** - Withdraw all available crypto from Jupiter to Bybit

---

## workflows/

### transfers/bridge.py
- **transfer_to_bybit(coin, amount)** - Transfer coin from Jupiter to Bybit
- **transfer_to_solana(coin, amount)** - Transfer coin from Bybit to Jupiter

### arbitrage/detector.py
- **calculate_path_a_profit(coin_symbol, usdt_amount, bybit_fee_rate=0.001, slippage_eps=0.002, min_profit_threshold=0.1)** - Calculate profit for Path A (Jupiter → Bybit)
- **calculate_path_b_profit(coin_symbol, usdt_amount, bybit_fee_rate=0.001, slippage_eps=0.002, min_profit_threshold=0.1)** - Calculate profit for Path B (Bybit → Jupiter)
- **find_best_opportunity(coins, usdt_amount, bybit_fee_rate=0.001, min_profit_threshold=0.1)** - Find best arbitrage opportunity

### arbitrage/executor.py
- **detect_funds_location()** - Detect where funds are currently stored
- **check_arbitrage_opportunity(coins, min_profit_threshold=0.5, bybit_fee_rate=0.001)** - Check for arbitrage opportunity
- **execute_arbitrage(opportunity, dry_run=True)** - Execute arbitrage
- **run_arbitrage_loop(coins=['SOL','ETH','BTC'], min_profit_threshold=0.5, check_interval=10, max_iterations=None, dry_run=True)** - Run continuous arbitrage loop

### arbitrage/consolidate.py
- **consolidate_to_bybit()** - Consolidate all funds from Jupiter to Bybit
- **consolidate_to_solana()** - Consolidate all funds from Bybit to Jupiter
- **consolidate_to_usdt_on_bybit()** - Consolidate all coins to USDT on Bybit
- **consolidate_to_usdt_on_solana()** - Consolidate all coins to USDT on Jupiter
