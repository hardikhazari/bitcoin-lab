import time
import json
import subprocess
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# RPC Configuration
RPC_USER = "user"
RPC_PASSWORD = "password"
RPC_HOST = "127.0.0.1"
RPC_PORT = "18443"
RPC_URL = f"http://{RPC_USER}:{RPC_PASSWORD}@{RPC_HOST}:{RPC_PORT}"

def get_rpc():
    return AuthServiceProxy(RPC_URL)

def setup_wallet(rpc, wallet_name="lab_wallet_segwit"):
    print(f"--- Setting up wallet: {wallet_name} ---")
    wallets = rpc.listwallets()
    if wallet_name not in wallets:
        try:
            rpc.createwallet(wallet_name)
            print(f"Created wallet: {wallet_name}")
        except JSONRPCException as e:
            if "already exists" in str(e):
                rpc.loadwallet(wallet_name)
                print(f"Loaded existing wallet: {wallet_name}")
            else:
                raise e
    else:
        print(f"Wallet {wallet_name} already loaded.")
    return AuthServiceProxy(f"{RPC_URL}/wallet/{wallet_name}")

def part2_segwit_p2sh_p2wpkh():
    rpc = get_rpc()
    wallet = setup_wallet(rpc)

    # 1. Generate 3 SegWit addresses: A', B', C'
    print("\n1. Generating SegWit (P2SH-P2WPKH) Addresses...")
    addr_a = wallet.getnewaddress("Address_A_SegWit", "p2sh-segwit")
    addr_b = wallet.getnewaddress("Address_B_SegWit", "p2sh-segwit")
    addr_c = wallet.getnewaddress("Address_C_SegWit", "p2sh-segwit")
    print(f"Address A': {addr_a}")
    print(f"Address B': {addr_b}")
    print(f"Address C': {addr_c}")

    # 2. Fund Address A'
    print("\n2. Funding Address A'...")
    dummy_addr = wallet.getnewaddress("dummy")
    wallet.generatetoaddress(101, dummy_addr)
    
    txid_fund = wallet.sendtoaddress(addr_a, 10.0)
    print(f"Funding TXID: {txid_fund}")
    wallet.generatetoaddress(1, dummy_addr)

    # 3. Step 1: A' -> B'
    print("\n3. Step 1: A' -> B' (SegWit P2SH-P2WPKH)")
    unspent_a = [u for u in wallet.listunspent() if u['address'] == addr_a]
    utxo = unspent_a[0]
    inputs = [{"txid": utxo['txid'], "vout": utxo['vout']}]
    outputs = {addr_b: 9.99}
    
    raw_tx_1 = wallet.createrawtransaction(inputs, outputs)
    signed_tx_1 = wallet.signrawtransactionwithwallet(raw_tx_1)
    txid_1 = wallet.sendrawtransaction(signed_tx_1['hex'])
    print(f"TXID A'->B': {txid_1}")
    wallet.generatetoaddress(1, dummy_addr)

    # Decode and Extract
    decoded_tx_1 = wallet.decoderawtransaction(signed_tx_1['hex'])
    vin = decoded_tx_1['vin'][0]
    vout = decoded_tx_1['vout'][0]
    
    print("\n--- SegWit A'->B' Analysis ---")
    print(f"scriptSig (Redeem Script): {vin.get('scriptSig', {}).get('asm')}")
    print(f"Witness Data: {vin.get('txinwitness')}")
    print(f"scriptPubKey: {vout.get('scriptPubKey', {}).get('asm')}")

    # 4. Step 2: B' -> C'
    print("\n4. Step 2: B' -> C' (SegWit P2SH-P2WPKH)")
    unspent_b = [u for u in wallet.listunspent() if u['address'] == addr_b]
    utxo_b = unspent_b[0]
    
    inputs_2 = [{"txid": utxo_b['txid'], "vout": utxo_b['vout']}]
    outputs_2 = {addr_c: 9.98}
    
    raw_tx_2 = wallet.createrawtransaction(inputs_2, outputs_2)
    signed_tx_2 = wallet.signrawtransactionwithwallet(raw_tx_2)
    txid_2 = wallet.sendrawtransaction(signed_tx_2['hex'])
    print(f"TXID B'->C': {txid_2}")
    wallet.generatetoaddress(1, dummy_addr)

    decoded_tx_2 = wallet.decoderawtransaction(signed_tx_2['hex'])
    
    # Size Comparison Data
    print("\n--- Size Comparison ---")
    print(f"Raw Size: {decoded_tx_2['size']} bytes")
    print(f"Virtual Size: {decoded_tx_2['vsize']} vbytes")
    print(f"Weight: {decoded_tx_2['weight']} units")

    # BTCdeb Validation
    print("\n--- BTCdeb Validation for A'->B' ---")
    try:
        subprocess.run(["btcdeb", "-tx", signed_tx_1['hex'], "-in", "0", "-step"], check=True, capture_output=False)
        print("BTCdeb validation for A'->B' successful.")
    except subprocess.CalledProcessError as e:
        print(f"BTCdeb validation for A'->B' failed: {e}")
        print(f"Stderr: {e.stderr.decode()}")
    except FileNotFoundError:
        print("btcdeb command not found. Please ensure btcdeb is installed and in your PATH.")

    print("\n--- BTCdeb Validation for B'->C' ---")
    try:
        subprocess.run(["btcdeb", "-tx", signed_tx_2['hex'], "-in", "0", "-step"], check=True, capture_output=False)
        print("BTCdeb validation for B'->C' successful.")
    except subprocess.CalledProcessError as e:
        print(f"BTCdeb validation for B'->C' failed: {e}")
        print(f"Stderr: {e.stderr.decode()}")
    except FileNotFoundError:
        print("btcdeb command not found. Please ensure btcdeb is installed and in your PATH.")

if __name__ == "__main__":
    try:
        part2_segwit_p2sh_p2wpkh()
    except Exception as e:
        print(f"Error: {e}")
