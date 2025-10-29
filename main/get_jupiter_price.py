import requests

def get_jupiter_quote(input_mint, output_mint, amount):
    url = "https://lite-api.jup.ag/swap/v1/quote"
    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": amount
    }
    response = requests.get(url, params=params)
    data = response.json()
    
    if "error" in data:
        return None
    else:
        return data
