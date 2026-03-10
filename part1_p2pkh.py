import time
import json
import subprocess
import decimal
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException

# RPC Configuration
RPC_USER = "user"
RPC_PASSWORD = "password"
RPC_HOST = "127.0.0.1"
RPC_PORT = "18443"
RPC_URL = f"http://{RPC_USER}:{RPC_PASSWORD}@{RPC_HOST}:{RPC_PORT}"

def get_rpc():
    return AuthServiceProxy(RPC_URL)

def setup_wallet(rpc, wallet_name="lab_wallet"):
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

class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle Decimal types from RPC responses."""
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)

def part1_legacy_p2pkh():
    rpc = get_rpc()
    wallet = setup_wallet(rpc)

    # 1. Generate 3 Legacy addresses: A, B, C
    print("\n1. Generating Legacy Addresses...")
    addr_a = wallet.getnewaddress("Address_A", "legacy")
    addr_b = wallet.getnewaddress("Address_B", "legacy")
    addr_c = wallet.getnewaddress("Address_C", "legacy")
    print(f"Address A: {addr_a}")
    print(f"Address B: {addr_b}")
    print(f"Address C: {addr_c}")

    # 2. Fund Address A
    print("\n2. Funding Address A...")
    # In regtest, we need to mine blocks to get initial funds
    # First, generate some blocks to a dummy address to get coinbase rewards
    dummy_addr = wallet.getnewaddress("dummy")
    wallet.generatetoaddress(101, dummy_addr) # 101 blocks to make first reward spendable
    
    # Send funds to A
    txid_fund = wallet.sendtoaddress(addr_a, 10.0)
    print(f"Funding TXID: {txid_fund}")
    wallet.generatetoaddress(1, dummy_addr) # Confirm funding tx

    # 3. Step 1: A -> B
    print("\n3. Step 1: A -> B (Legacy P2PKH)")
    unspent_a = [u for u in wallet.listunspent() if u['address'] == addr_a]
    if not unspent_a:
        raise Exception("Address A has no UTXOs")
    
    utxo = unspent_a[0]
    print(f"Using UTXO: txid={utxo['txid']}  vout={utxo['vout']}  amount={utxo['amount']}")
    
    inputs = [{"txid": utxo['txid'], "vout": utxo['vout']}]
    outputs = {addr_b: 9.99} # Simple spend, rest is fee
    
    raw_tx_1 = wallet.createrawtransaction(inputs, outputs)
    decoded_tx_1_raw = wallet.decoderawtransaction(raw_tx_1)
    
    print("\nDecoded raw tx (A to B) - ScriptPubKey for B:")
    for vout in decoded_tx_1_raw["vout"]:
        if vout["scriptPubKey"].get("address", "") == addr_b:
            spk = vout["scriptPubKey"]
            print(f"  asm : {spk['asm']}")
            print(f"  hex : {spk['hex']}")
            print(f"  type: {spk['type']}")
    
    signed_tx_1 = wallet.signrawtransactionwithwallet(raw_tx_1)
    assert signed_tx_1["complete"], "Signing failed!"
    
    txid_1 = wallet.sendrawtransaction(signed_tx_1['hex'])
    print(f"TXID A->B: {txid_1}")
    wallet.generatetoaddress(1, dummy_addr)

    # Decode and Extract
    decoded_tx_1 = wallet.decoderawtransaction(signed_tx_1['hex'])
    vin = decoded_tx_1['vin'][0]
    vout = decoded_tx_1['vout'][0]
    
    print("\n--- Legacy A->B Analysis ---")
    print(f"scriptSig (Unlocking): {vin.get('scriptSig', {}).get('asm')}")
    print(f"scriptPubKey (Locking): {vout.get('scriptPubKey', {}).get('asm')}")

    # 4. Step 2: B -> C
    print("\n4. Step 2: B -> C (Legacy P2PKH)")
    unspent_b = [u for u in wallet.listunspent() if u['address'] == addr_b]
    if not unspent_b:
        raise Exception("Address B has no UTXOs")
    
    utxo_b = unspent_b[0]
    print(f"Using UTXO: txid={utxo_b['txid']}  vout={utxo_b['vout']}  amount={utxo_b['amount']}")
    print(f"This UTXO came from txid (A to B): {txid_1}")
    print(f"UTXO source matches A->B txid: {utxo_b['txid'] == txid_1}")
    
    inputs_2 = [{"txid": utxo_b['txid'], "vout": utxo_b['vout']}]
    outputs_2 = {addr_c: 9.98}
    
    raw_tx_2 = wallet.createrawtransaction(inputs_2, outputs_2)
    signed_tx_2 = wallet.signrawtransactionwithwallet(raw_tx_2)
    assert signed_tx_2["complete"], "Signing failed!"
    
    txid_2 = wallet.sendrawtransaction(signed_tx_2['hex'])
    print(f"TXID B->C: {txid_2}")
    wallet.generatetoaddress(1, dummy_addr)

    decoded_tx_2 = wallet.decoderawtransaction(signed_tx_2['hex'])
    print("\n--- Legacy B->C Analysis ---")
    print(f"Challenge Script (Locking): {decoded_tx_2['vout'][0]['scriptPubKey']['asm']}")
    print(f"Response Script (Unlocking): {decoded_tx_2['vin'][0]['scriptSig']['asm']}")

    # Save results to JSON file
    results = {
        "addresses": {"A": addr_a, "B": addr_b, "C": addr_c},
        "tx_A_to_B": {"txid": txid_1, "decoded": decoded_tx_1},
        "tx_B_to_C": {"txid": txid_2, "decoded": decoded_tx_2},
        "signed_hex_BC": signed_tx_2["hex"],
    }
    
    with open("part1_results.json", "w") as f:
        json.dump(results, f, indent=2, cls=DecimalEncoder)
    print("\nResults saved to part1_results.json")

    # BTCdeb Validation with proper command generation
    print("\n" + "=" * 60)
    print("btcdeb command to validate Part 1:")
    print("=" * 60)
    
    # Extract unlocking script from B->C transaction
    unlocking_asm = ""
    for vin in decoded_tx_2["vin"]:
        unlocking_asm = vin.get("scriptSig", {}).get("asm", "")
    
    # Extract locking script from A->B transaction
    locking_asm = ""
    for vout in decoded_tx_1["vout"]:
        if vout["scriptPubKey"].get("address", "") == addr_b:
            locking_asm = vout["scriptPubKey"]["asm"]
    
    btcdeb_cmd = f"btcdeb '[{unlocking_asm} {locking_asm}]' --tx={signed_tx_2['hex']}"
    print(f"\n{btcdeb_cmd}\n")
    
    print("--- BTCdeb Validation for A->B ---")
    try:
        subprocess.run(["btcdeb", "-tx", signed_tx_1['hex'], "-in", "0", "-step"], check=True, capture_output=False)
        print("BTCdeb validation for A->B successful.")
    except subprocess.CalledProcessError as e:
        print(f"BTCdeb validation for A->B failed: {e}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Stderr: {e.stderr.decode()}")
    except FileNotFoundError:
        print("btcdeb command not found. Please ensure btcdeb is installed and in your PATH.")

    print("\n--- BTCdeb Validation for B->C ---")
    try:
        subprocess.run(["btcdeb", "-tx", signed_tx_2['hex'], "-in", "0", "-step"], check=True, capture_output=False)
        print("BTCdeb validation for B->C successful.")
    except subprocess.CalledProcessError as e:
        print(f"BTCdeb validation for B->C failed: {e}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Stderr: {e.stderr.decode()}")
    except FileNotFoundError:
        print("btcdeb command not found. Please ensure btcdeb is installed and in your PATH.")
    
    print("=" * 60)

if __name__ == "__main__":
    try:
        part1_legacy_p2pkh()
    except Exception as e:
        print(f"Error: {e}")
