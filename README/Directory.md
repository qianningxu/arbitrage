# Directory Structure

```
main/
├── Bybit/                        # Bybit exchange operations
│   ├── helper/
│   │   ├── auth.py               # Authentication & signing
│   │   └── pricing.py            # Orderbook & price calculation
│   ├── balance.py                # Balance retrieval
│   ├── swap.py                   # Spot trading (swaps)
│   └── transfers.py              # Internal transfers & withdrawals
│
├── Jupiter/                      # Jupiter/Solana operations
│   ├── helper/
│   │   └── client.py             # RPC client & wallet basics
│   ├── balance.py                # Balance checking
│   ├── pricing.py                # Price quotes from Jupiter
│   ├── swap.py                   # Swap execution via Jupiter
│   └── transfers.py              # Send SOL/SPL tokens
│
├── shared/                       # Shared utilities
│   ├── config.py                 # Environment vars & keypairs
│   └── data.py                   # Token/pair/fee data loading
│
└── workflows/                    # Cross-platform operations
    ├── arbitrage/
    │   ├── detector.py           # Opportunity detection
    │   ├── executor.py           # Strategy execution
    │   └── consolidate.py        # Fund consolidation
    └── transfers/
        └── bridge.py             # Transfer between Bybit ↔ Jupiter

test/
├── Bybit/                        # Bybit tests
│   ├── helper/
│   │   ├── test_auth.py
│   │   ├── test_info.py
│   │   └── test_min_order.py
│   ├── test_balance.py
│   ├── test_pricing.py
│   ├── test_transfer.py
│   ├── test_withdraw.py
│   └── test_bybit_swap.py
│
├── Jupiter/                      # Jupiter/Solana tests
│   ├── helper/
│   │   ├── test_get_id_from_pairs.py
│   │   ├── test_pricing.py
│   │   └── test_quote.py
│   ├── test_balance.py
│   ├── test_pricing.py
│   ├── test_quote.py
│   ├── test_swap.py
│   └── test_withdraw.py
│
└── workflow/                     # Cross-platform workflow tests
    ├── test_arbitrage_strategy.py
    ├── test_bybit_to_jupiter.py
    └── test_jupiter_to_bybit.py
```
