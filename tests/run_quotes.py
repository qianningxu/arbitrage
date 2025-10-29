import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from main.monitor.get_id import bybit_symbol_to_solana_mints
from main.monitor.get_jupiter_price import get_jupiter_quote


def load_decimals_map():
    path = os.path.join(ROOT, "files/all_mints.json")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    decimals_map = {}
    if isinstance(data, dict):
        for sym, items in data.items():
            for t in items:
                mint = t.get("mint") or t.get("id")
                dec = t.get("decimals")
                if mint and dec is not None:
                    decimals_map[mint] = int(dec)
    elif isinstance(data, list):
        for t in data:
            mint = t.get("mint") or t.get("id")
            dec = t.get("decimals")
            if mint and dec is not None:
                decimals_map[mint] = int(dec)
    return decimals_map


def get_exchange_rate(symbol, decimals_map):
    res = bybit_symbol_to_solana_mints(symbol)
    if not res:
        return None
    base_mint, quote_mint = res

    base_dec = decimals_map.get(base_mint, 6)
    quote_dec = decimals_map.get(quote_mint, 6)
    amount = 10 ** base_dec

    quote = get_jupiter_quote(base_mint, quote_mint, amount)
    if not quote:
        return None

    out_amt = quote.get("outAmount")
    in_amt = quote.get("inAmount")
    if not out_amt or not in_amt:
        return None

    in_normalized = float(in_amt) / (10 ** base_dec)
    out_normalized = float(out_amt) / (10 ** quote_dec)
    return out_normalized / in_normalized


def main():
    symbols = [
        "ETHUSDT",
        "MANAUSDT",
        "DYDXUSDT",
        "UNIUSDT",
        "ADAUSDT",
        "USDCUSDT",
        "SOLUSDT",
        "BATUSDT",
        "SPELLUSDT",
        "CAKEUSDT",
        "C98USDT",
        "UMAUSDT",
        "ETHUSDC"
    ]

    decimals_map = load_decimals_map()

    for sym in symbols:
        rate = get_exchange_rate(sym, decimals_map)
        print(f"{sym}: {rate}")


if __name__ == "__main__":
    main()
