import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY = os.getenv("ONEINCH_API_KEY")
ONEINCH_API_URL = "https://api.1inch.dev/swap/v5.2/137/quote"
headers = {
    "Authorization": f"Bearer {API_KEY}"
}

# Token addresses
WETH_ADDRESS = "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"  # Wrapped ETH
USDC_ADDRESS = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"  # USDC
POL_ADDRESS = "0x1000000000000000000000000000000000000000"  # POL (example)

def get_quote(from_token, to_token, amount):
    params = {
        "fromTokenAddress": from_token,
        "toTokenAddress": to_token,
        "amount": amount,
    }
    response = requests.get(ONEINCH_API_URL, params=params, headers=headers)
    return response.json()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    print("Fetching swap quotes for arbitrage detection...")
    amount_weth = 10**18  # 1 WETH (18 decimals)
    amount_usdc = 4000 * 10**6  # 4000 USDC (6 decimals)

    # WETH -> USDC
    try:
        quote_weth_to_usdc = get_quote(WETH_ADDRESS, USDC_ADDRESS, amount_weth)
        logging.info(f"1 WETH -> USDC: {quote_weth_to_usdc}")
        usdc_received = int(quote_weth_to_usdc.get("toAmount", 0)) / 10**6
    except Exception as e:
        logging.error(f"Error fetching WETH->USDC quote: {e}")
        usdc_received = 0

    # USDC -> WETH
    try:
        quote_usdc_to_weth = get_quote(USDC_ADDRESS, WETH_ADDRESS, amount_usdc)
        logging.info(f"4000 USDC -> WETH: {quote_usdc_to_weth}")
        weth_received = int(quote_usdc_to_weth.get("toAmount", 0)) / 10**18
    except Exception as e:
        logging.error(f"Error fetching USDC->WETH quote: {e}")
        weth_received = 0

    # Arbitrage Analysis
    logging.info("Arbitrage Analysis:")
    logging.info(f"Swap 1 WETH -> {usdc_received} USDC, then {usdc_received} USDC -> {weth_received} WETH")
    round_trip_weth = weth_received - 1
    logging.info(f"Net WETH after round-trip: {round_trip_weth}")

    if round_trip_weth > 0:
        logging.info("Arbitrage opportunity detected: PROFITABLE!")
    else:
        logging.info("No arbitrage opportunity detected.")