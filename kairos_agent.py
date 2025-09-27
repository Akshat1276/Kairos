
import os
import json
import requests
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
API_KEY = os.getenv("ONEINCH_API_KEY")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
RPC_URL = os.getenv("AMOY_RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Load ABI from Hardhat artifact
with open("artifacts/contracts/KairosVault.sol/KairosVault.json") as f:
    contract_abi = json.load(f)["abi"]

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

ONEINCH_API_URL = "https://api.1inch.dev/swap/v5.2/137/quote"
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "accept": "application/json"
}

# Hedera testnet configuration
HEDERA_TESTNET_URL = "https://testnet.mirrornode.hedera.com"

def get_hedera_token_price(token_id):
    """
    Fetch token information from Hedera testnet using REST API
    """
    try:
        # Get token info from Hedera Mirror Node
        url = f"{HEDERA_TESTNET_URL}/api/v1/tokens/{token_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"Hedera token {token_id}: {token_data}")
            return token_data
        else:
            print(f"Failed to fetch Hedera token data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching Hedera token price: {e}")
        return None

def get_hedera_account_balance():
    """
    Fetch account balance from Hedera testnet
    """
    load_dotenv()
    account_id = os.getenv("HEDERA_ACCOUNT_ID")
    
    if not account_id:
        raise ValueError("HEDERA_ACCOUNT_ID must be set in .env")
    
    try:
        url = f"{HEDERA_TESTNET_URL}/api/v1/accounts/{account_id}"
        response = requests.get(url)
        
        if response.status_code == 200:
            account_data = response.json()
            balance = account_data.get("balance", {})
            hbar_balance = int(balance.get("balance", 0)) / 100000000  # Convert tinybars to HBAR
            print(f"Hedera Account {account_id} HBAR balance: {hbar_balance}")
            return account_data
        else:
            print(f"Failed to fetch Hedera account data: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error fetching Hedera account balance: {e}")
        return None

def detect_cross_chain_arbitrage(polygon_price, hedera_price, threshold=0.02):
    """
    Detect arbitrage opportunities between Polygon and Hedera
    threshold: minimum price difference percentage to consider profitable
    """
    if not polygon_price or not hedera_price:
        return False, 0
    
    price_diff = abs(polygon_price - hedera_price) / polygon_price
    is_profitable = price_diff > threshold
    
    return is_profitable, price_diff
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

def execute_trade_on_chain(details):
    txn = contract.functions.executeTrade(details).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 300000,  # adjust as needed
        'gasPrice': w3.eth.gas_price
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Trade sent! Tx hash: {tx_hash.hex()}")
    return tx_hash.hex()

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

    print("Fetching swap quotes for cross-chain arbitrage detection...")
    amount_weth = 10**18  # 1 WETH (18 decimals)
    amount_usdc = 4000 * 10**6  # 4000 USDC (6 decimals)

    # Fetch prices from Polygon (1inch)
    print("=== POLYGON PRICES (1inch) ===")
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

    # Fetch prices from Hedera
    print("\n=== HEDERA NETWORK DATA ===")
    # Get account balance and network info
    hedera_account_data = get_hedera_account_balance()
    
    # Example token IDs (you may need to adjust these for actual Hedera tokens)
    hedera_hbar_token = "0.0.0"  # HBAR (native token)
    
    hedera_hbar_data = get_hedera_token_price(hedera_hbar_token)

    # Cross-chain Arbitrage Analysis
    print("\n=== CROSS-CHAIN ARBITRAGE ANALYSIS ===")
    logging.info(f"Polygon: Swap 1 WETH -> {usdc_received} USDC, then {usdc_received} USDC -> {weth_received} WETH")
    round_trip_weth = weth_received - 1
    logging.info(f"Net WETH after Polygon round-trip: {round_trip_weth}")

    # Simulate cross-chain price comparison
    if hedera_account_data:
        logging.info(f"Hedera account active with ID: {hedera_account_data.get('account', 'Unknown')}")
        
        # Example: Compare WETH/USDC rates between networks
        polygon_weth_usdc_rate = usdc_received / 1.0  # USDC per WETH on Polygon
        
        # For demo purposes, simulate a Hedera rate (in reality, you'd fetch from Hedera DEX)
        simulated_hedera_rate = polygon_weth_usdc_rate * 1.03  # 3% higher on Hedera
        
        is_cross_chain_profitable, price_diff = detect_cross_chain_arbitrage(
            polygon_weth_usdc_rate, 
            simulated_hedera_rate
        )
        
        logging.info(f"Polygon WETH/USDC rate: {polygon_weth_usdc_rate:.6f}")
        logging.info(f"Hedera WETH/USDC rate (simulated): {simulated_hedera_rate:.6f}")
        logging.info(f"Price difference: {price_diff:.4%}")
        
        if is_cross_chain_profitable:
            logging.info("🚀 CROSS-CHAIN ARBITRAGE OPPORTUNITY DETECTED!")
            logging.info("Strategy: Buy low on Polygon, sell high on Hedera")
            details = f"Cross-chain arb: Polygon->Hedera, rate diff: {price_diff:.4%}"
            # Note: In production, you'd execute cross-chain trades here
            logging.info("Cross-chain execution would happen here...")
        else:
            logging.info("No profitable cross-chain arbitrage detected.")

    # Execute Polygon arbitrage if profitable
    if round_trip_weth > 0:
        logging.info("Arbitrage opportunity detected on Polygon: PROFITABLE!")
        details = f"WETH->USDC, amount: {amount_weth/10**18}, USDC received: {usdc_received}"
        execute_trade_on_chain(details)
    else:
        logging.info("No arbitrage opportunity detected on Polygon.")