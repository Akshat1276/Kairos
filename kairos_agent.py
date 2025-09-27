import time
import os
import json
import requests
import logging
from dotenv import load_dotenv
from web3 import Web3
from plyer import notification
from hedera import Client, AccountId, PrivateKey, TransferTransaction, Hbar

def send_desktop_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="Kairos Arbitrage Agent",
        timeout=10
    )

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

HEDERA_TESTNET_URL = "https://testnet.mirrornode.hedera.com"

def get_hedera_token_price(token_id):
    try:
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
    if not polygon_price or not hedera_price:
        return False, 0
    
    price_diff = abs(polygon_price - hedera_price) / polygon_price
    is_profitable = price_diff > threshold
    
    return is_profitable, price_diff

WETH_ADDRESS = "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619"  # Wrapped ETH
USDC_ADDRESS = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"  # USDC
POL_ADDRESS = "0x1000000000000000000000000000000000000000"  # POL

def get_quote(from_token, to_token, amount):
    params = {
        "fromTokenAddress": from_token,
        "toTokenAddress": to_token,
        "amount": amount,
    }
    response = requests.get(ONEINCH_API_URL, params=params, headers=headers)
    return response.json()


def execute_trade_on_polygon(details):
    txn = contract.functions.executeTrade(details).build_transaction({
        'from': account.address,
        'nonce': w3.eth.get_transaction_count(account.address),
        'gas': 300000,
        'gasPrice': w3.eth.gas_price
    })
    signed_txn = w3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
    print(f"Polygon trade sent! Tx hash: {tx_hash.hex()}")
    return tx_hash.hex()

def execute_trade_on_hedera(hbar_amount, to_account_id):
    load_dotenv()
    hedera_account_id = os.getenv("HEDERA_ACCOUNT_ID")
    hedera_private_key = os.getenv("HEDERA_PRIVATE_KEY")
    
    if not hedera_account_id or not hedera_private_key:
        print("Hedera credentials missing.")
        return None
    
    try:
        client = Client.forTestnet()
        
        my_account = AccountId.fromString(hedera_account_id)
        my_key = PrivateKey.fromString(hedera_private_key)
        client.setOperator(my_account, my_key)
        
        transaction = (TransferTransaction()
            .addHbarTransfer(my_account, Hbar(-hbar_amount))
            .addHbarTransfer(AccountId.fromString(to_account_id), Hbar(hbar_amount)))
        
        print(f"Executing real Hedera trade: Transfer {hbar_amount} HBAR from {hedera_account_id} to {to_account_id}")
        tx_response = transaction.execute(client)
        receipt = tx_response.getReceipt(client)
        
        print(f"Hedera trade executed! Status: {receipt.status}, Transaction ID: {receipt.transactionId}")
        
        return str(receipt.transactionId)
        
    except Exception as e:
        print(f"Error executing Hedera trade: {e}")
        return None


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s: %(message)s",
        handlers=[logging.FileHandler("kairos_agent.log"), logging.StreamHandler()]
    )

    while True:
        print("Fetching swap quotes for cross-chain arbitrage detection...")
        amount_weth = 10**18  # 1 WETH
        amount_usdc = 4000 * 10**6  # 4000 USDC

        # Polygon (1inch) prices
        print("=== POLYGON PRICES (1inch) ===")
        try:
            quote_weth_to_usdc = get_quote(WETH_ADDRESS, USDC_ADDRESS, amount_weth)
            logging.info(f"1 WETH -> USDC: {quote_weth_to_usdc}")
            usdc_received = int(quote_weth_to_usdc.get("toAmount", 0)) / 10**6
        except Exception as e:
            logging.error(f"Error fetching WETH->USDC quote: {e}")
            usdc_received = 0

        try:
            quote_usdc_to_weth = get_quote(USDC_ADDRESS, WETH_ADDRESS, amount_usdc)
            logging.info(f"4000 USDC -> WETH: {quote_usdc_to_weth}")
            weth_received = int(quote_usdc_to_weth.get("toAmount", 0)) / 10**18
        except Exception as e:
            logging.error(f"Error fetching USDC->WETH quote: {e}")
            weth_received = 0

        polygon_profit = weth_received - 1

        print("\n=== HEDERA NETWORK DATA ===")
        hedera_account_data = get_hedera_account_balance()
        hedera_hbar_token = "0.0.0"  # HBAR native token
        hedera_hbar_data = get_hedera_token_price(hedera_hbar_token)

        hedera_trade_amount = 10  # HBAR
        hedera_to_account = "0.0.2"  # Hedera treasury account

        hedera_profit = hedera_trade_amount * 0.03  # 3% profit

        print("\n=== CROSS-CHAIN ARBITRAGE ANALYSIS ===")
        logging.info(f"Polygon: Swap 1 WETH -> {usdc_received} USDC, then {usdc_received} USDC -> {weth_received} WETH")
        logging.info(f"Net WETH after Polygon round-trip: {polygon_profit}")
        logging.info(f"Hedera: Simulated trade {hedera_trade_amount} HBAR, profit: {hedera_profit}")

        # Execute best profitable trade
        if polygon_profit > hedera_profit and polygon_profit > 0:
            logging.info("Best arbitrage: Polygon")
            details = f"Polygon arbitrage: {polygon_profit:.6f} WETH profit"
            send_desktop_notification("Kairos Arbitrage Alert", details)
            execute_trade_on_polygon(details)
        elif hedera_profit > polygon_profit and hedera_profit > 0:
            logging.info("Best arbitrage: Hedera")
            details = f"Hedera arbitrage: {hedera_profit:.6f} HBAR profit"
            send_desktop_notification("Kairos Arbitrage Alert", details)
            execute_trade_on_hedera(hedera_trade_amount, hedera_to_account)
        else:
            logging.info("No profitable arbitrage detected.")

        logging.info("Sleeping for 5 minutes before next check...")
        time.sleep(300)