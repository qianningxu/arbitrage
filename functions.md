# Arbitrage Bot - Functions Documentation

This document lists all functions in the arbitrage bot, organized by module.

---

## 📁 main/get_price/

### get_bybit_price.py
- **get_orderbook(symbol, depth=100)** - Get orderbook data from Bybit for a trading pair
- **get_sell_rate(symbol, qty, depth=100)** - Calculate average price when selling qty into the bids
- **get_buy_rate(symbol, qty, depth=100)** - Calculate average price when buying qty from the asks

### get_jupiter_price.py
- **_load_tokens()** - Load token data from unique_mint_by_symbol.json file
- **get_exchange_rate(input_symbol, output_symbol, amount)** - Get Jupiter exchange rate between two token symbols
- **get_jupiter_price_from_bybit_symbol(symbol)** - Convert Bybit trading pair symbol to Jupiter price

### get_id_from_pairs.py
- **bybit_symbol_to_solana_mints(symbol)** - Convert Bybit trading pair symbol to Solana mint addresses tuple

---

## 📁 main/trade/

### bybit_auth.py
- **sign_request(param_str)** - Create authentication headers with signature for Bybit API requests

### bybit_balance.py
- **get_fund_balance(coin)** - Get balance of a specific coin in Bybit FUND account
- **get_unified_balance(coin)** - Get balance of a specific coin in Bybit UNIFIED account
- **get_all_fund_balances()** - Get all non-zero coin balances in Bybit FUND account
- **get_all_unified_balances()** - Get all non-zero coin balances in Bybit UNIFIED account

### bybit_info.py
- **_load_pairs()** - Load all trading pairs from all_pairs.json with caching
- **get_pair_info(symbol)** - Get trading pair information including min quantity and precision

### bybit_transfer.py
- **internal_transfer(coin, amount, from_account="FUND", to_account="UNIFIED")** - Transfer coins between Bybit FUND and UNIFIED accounts
- **transfer_all_to_unified()** - Transfer all coins from FUND to UNIFIED account

### bybit_swap.py
- **swap(in_coin, out_coin, amount, amount_unit)** - Execute market order swap on Bybit spot market

### jupiter_helpers.py
- **get_jupiter_quote(input_mint, output_mint, amount)** - Fetch swap quote from Jupiter API using mint addresses
- **_load_tokens()** - Load token data from unique_mint_by_symbol.json file
- **check_balance(symbol)** - Check token balance in Solana wallet for SOL or SPL tokens

### jupiter_swap.py
- **swap(quote)** - Execute Jupiter swap transaction with a pre-fetched quote
- **trade(input_symbol, output_symbol, amount)** - Trade tokens on Jupiter by symbol names

---

## 📁 main/transfer/

### solana_wallet.py
- **_load_tokens()** - Load token data from unique_mint_by_symbol.json file
- **get_solana_wallet_address()** - Get Solana wallet public address from private key in environment
- **get_sol_balance(keypair, client)** - Get SOL balance for a Solana keypair

### solana_send.py
- **send_native_sol(destination_address, amount)** - Send native SOL to a destination address on Solana
- **send_spl_token(token_mint, destination_address, amount, decimals)** - Send SPL token to a destination address on Solana

### bybit_deposit.py
- **get_bybit_deposit_address(coin_symbol)** - Get Bybit deposit address for a coin on Solana chain via API

### bybit_withdraw.py
- **withdraw_from_bybit(coin, amount)** - Withdraw coins from Bybit FUND account to Solana wallet

### bybit_internal.py
- **transfer_unified_to_fund()** - Transfer all coins from Bybit UNIFIED to FUND account

### transfer_to_bybit.py
- **transfer_to_bybit(coin_symbol, amount)** - Transfer specific amount of a coin from Solana wallet to Bybit

### transfer_to_jupiter.py
- **transfer_all_to_jupiter()** - Complete flow to transfer all cryptos from Bybit to Solana wallet

### transfer_multiple_to_bybit.py
- **transfer_multiple_to_bybit(crypto_names)** - Batch transfer multiple cryptos from Solana wallet to Bybit

### transfer_multiple_to_jupiter.py
- **transfer_multiple_to_jupiter(crypto_names=None)** - Batch transfer multiple cryptos from Bybit to Solana wallet

### jupiter_to_bybit.py (DEPRECATED - backward compatibility wrapper)
- **_load_tokens()** - Re-export from solana_wallet.py
- **get_bybit_deposit_address(coin_symbol)** - Re-export from bybit_deposit.py
- **get_sol_balance(keypair, client)** - Re-export from solana_wallet.py
- **send_native_sol(destination_address, amount)** - Re-export from solana_send.py
- **send_spl_token(token_mint, destination_address, amount, decimals)** - Re-export from solana_send.py
- **transfer_to_bybit(coin_symbol, amount)** - Re-export from transfer_to_bybit.py

### bybit_to_jupiter.py (DEPRECATED - backward compatibility wrapper)
- **get_solana_wallet_address()** - Re-export from solana_wallet.py
- **transfer_unified_to_fund()** - Re-export from bybit_internal.py
- **withdraw_from_bybit(coin, amount)** - Re-export from bybit_withdraw.py
- **transfer_all_to_jupiter()** - Re-export from transfer_to_jupiter.py

---

## Summary

**Total Functions: 39**

- **Price Functions:** 7 functions for fetching and calculating prices from Bybit and Jupiter
- **Trading Functions:** 11 functions for balance checks, transfers, and swaps on Bybit and Jupiter
- **Transfer Functions:** 21 functions for transferring crypto between Solana and Bybit (includes 8 deprecated re-exports)

---

## Organization Notes

The transfer module was recently reorganized for better maintainability:
- Each file now contains maximum 3 functions
- Original `jupiter_to_bybit.py` and `bybit_to_jupiter.py` are now wrapper files for backward compatibility
- New modular files: `solana_wallet.py`, `solana_send.py`, `bybit_deposit.py`, `bybit_withdraw.py`, `bybit_internal.py`
- New batch transfer functions: `transfer_multiple_to_bybit.py`, `transfer_multiple_to_jupiter.py`
