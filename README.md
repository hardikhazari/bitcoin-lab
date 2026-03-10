# CS216 Bitcoin Transaction Lab

### Legacy vs SegWit Transaction Implementation with Bitcoin Debugger Integration

---

## Team Members

| Name     | Roll Number |
| -------- | ----------- |
| Harsh Bhalla | 240003033 |
| Hardik Sanjeev Hazari | 240003032  |
| Abhinav Jain | 240003003  |
| Jatin Singh | 240003035  |

---

# Project Overview

This project demonstrates the creation and validation of Bitcoin transactions using two different address formats:

1. **Legacy Transactions (P2PKH)**
2. **SegWit Transactions (P2SH-P2WPKH)**

The implementation uses **Bitcoin Core running in Regtest mode** along with Python scripts that interact with the Bitcoin node using RPC calls. The project now includes **comprehensive Bitcoin debugger (btcdeb) integration** to validate and analyze transaction scripts.

The goal of this lab is to understand:

* How Bitcoin transactions are constructed
* The structure of locking and unlocking scripts
* The difference between Legacy and SegWit transactions
* Transaction size and efficiency improvements introduced by SegWit
* Script validation using the Bitcoin debugger (btcdeb)
* Transaction analysis and comparison

---

# Project Structure

```
bitcoin-lab/
│
├── part1_p2pkh.py          # Implementation of Legacy P2PKH transactions with btcdeb integration
├── part2_segwit.py         # Implementation of SegWit P2SH-P2WPKH transactions with btcdeb integration
├── part3_comparison.py     # Comparative analysis of transaction sizes and scripts
├── part1_results.json      # Auto-generated results from Part 1
├── part2_results.json      # Auto-generated results from Part 2
├── requirements.txt        # Python dependencies
├── report.pdf              # Detailed project report
└── README.md               # Instructions to run the project
```

---

# Requirements

Before running the scripts, install the following:

* Python 3.8 or above
* Bitcoin Core
* [btcdeb](https://github.com/bitcoin-core/btcdeb) (Bitcoin Script Debugger)
* Python packages listed in `requirements.txt`

Install dependencies using:

```
pip install -r requirements.txt
```

## Installing btcdeb

### On Ubuntu/Linux

btcdeb must be built from source on Ubuntu 24.04 and later. Special compile flags are needed to avoid buffer overflow issues in WSL2:

```bash
# Install build dependencies
sudo apt update
sudo apt install -y git build-essential libtool autotools-dev automake pkg-config libssl-dev

# Clone btcdeb
git clone https://github.com/bitcoin-core/btcdeb.git
cd btcdeb

# Configure with fortify and asm disabled
./autogen.sh
./configure CXXFLAGS="-O0 -U_FORTIFY_SOURCE" CFLAGS="-O0 -U_FORTIFY_SOURCE" --disable-asm

# Build
make

# Verify installation
./btcdeb '[OP_1 OP_1 OP_ADD OP_2 OP_EQUAL]'
```

### On macOS

```bash
brew install btcdeb
```

### On Windows

Download pre-built binaries from the [btcdeb releases page](https://github.com/bitcoin-core/btcdeb/releases) and add to PATH.

---

# Running the Bitcoin Node

Start Bitcoin Core in **regtest mode**.

Example command:

```
bitcoind -regtest
```

Ensure that RPC is enabled and properly configured in `bitcoin.conf`.

---

# Bitcoin Configuration

To allow the Python scripts to communicate with Bitcoin Core using RPC, create a configuration file named `bitcoin.conf` in the Bitcoin data directory.

Example location (Windows):

```
C:\Users\<username>\AppData\Roaming\Bitcoin\bitcoin.conf
```

Example location (Linux):

```
~/.bitcoin/bitcoin.conf
```

Example configuration:

```
regtest=1
server=1
rpcuser=user
rpcpassword=password
rpcallowip=127.0.0.1
fallbackfee=0.0002

[regtest]
rpcport=18443
```

---

# Running the Programs

### Run Part 1 (Legacy Transactions)

```
python part1_p2pkh.py
```

This script:

* Creates Legacy (P2PKH) addresses (A, B, C)
* Funds Address A with 10 BTC
* Executes transactions: A → B → C
* Displays locking and unlocking scripts
* Generates btcdeb validation commands
* Saves results to `part1_results.json`
* Attempts to validate scripts using btcdeb

**Output includes:**
- Generated Bitcoin addresses
- Transaction IDs (TXIDs)
- Locking scripts (ScriptPubKey) for A→B
- Unlocking scripts (ScriptSig) for B→C
- btcdeb command for manual validation

---

### Run Part 2 (SegWit Transactions)

```
python part2_segwit.py
```

This script:

* Creates SegWit (P2SH-P2WPKH) addresses (A', B', C')
* Funds Address A' with 10 BTC
* Executes transactions: A' → B' → C'
* Displays witness data and redeem scripts
* Shows transaction size, virtual size, and weight
* Generates btcdeb validation commands
* Saves results to `part2_results.json`
* Attempts to validate scripts using btcdeb

**Output includes:**
- Generated SegWit addresses
- Transaction IDs (TXIDs)
- Locking scripts (ScriptPubKey) for A'→B'
- Witness data for B'→C'
- Redeem scripts (ScriptSig)
- Transaction size metrics
- btcdeb command for manual validation

---

### Run Part 3 (Comparative Analysis)

```
python part3_comparison.py
```

This script:

* Loads results from `part1_results.json` and `part2_results.json`
* Displays all addresses and transaction IDs
* Compares locking and unlocking scripts
* Analyzes transaction sizes (raw, virtual, weight)
* Calculates efficiency improvements with SegWit
* Provides key observations about script differences

**Prerequisites:** Run Part 1 and Part 2 before running Part 3.

---

# Bitcoin Debugger (btcdeb) Integration

## What is btcdeb?

**btcdeb** is the Bitcoin Script Debugger, a tool that allows you to step through Bitcoin script execution line by line. It helps validate that scripts execute correctly and understand how Bitcoin's scripting language works.

## How It's Integrated

The scripts now automatically:

1. **Extract scripts** from transactions (locking and unlocking scripts)
2. **Generate btcdeb commands** with proper formatting
3. **Display validation commands** for manual execution
4. **Attempt automatic validation** (if btcdeb is installed and in PATH)

## Manual Script Validation

### For Legacy P2PKH Transactions (Part 1)

After running Part 1, you'll see a btcdeb command like:

```bash
btcdeb '[<signature> <pubkey> OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG]' --tx=<transaction_hex>
```

To manually validate:

```bash
btcdeb '[<signature> <pubkey> OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG]' --tx=<transaction_hex>
```

Then type `step` to step through each operation.

### For SegWit P2SH-P2WPKH Transactions (Part 2)

After running Part 2, you'll see a btcdeb command like:

```bash
btcdeb '[<witness_sig> <witness_pubkey>]' --tx=<transaction_hex>
```

For P2SH-P2WPKH, the witness stack contains only signature and public key. The OP codes (OP_DUP, OP_HASH160, etc.) are implied by the witness program and executed internally by the Bitcoin node.

## Understanding btcdeb Output

When you run btcdeb and type `step`:

- **Stack** shows the current values on the stack
- **Script** shows remaining operations to execute
- **Altstack** shows values in the alternate stack (if used)
- Each `step` executes one operation
- The final stack should contain `1` (true) for valid scripts

## Common btcdeb Commands

| Command | Description |
|---------|-------------|
| `step` | Execute one operation and show the result |
| `step 5` | Execute 5 operations |
| `print` | Print current state |
| `help` | Show available commands |
| `quit` | Exit btcdeb |

---

# Key Concepts Demonstrated

The project highlights several important Bitcoin concepts:

* **Bitcoin Script** - The stack-based scripting language used by Bitcoin
* **Locking and Unlocking Scripts** - How transactions lock and unlock UTXOs
* **Pay-to-Public-Key-Hash (P2PKH)** - Legacy transaction format
* **Segregated Witness (SegWit)** - Improved transaction format with witness data separation
* **Transaction size and weight calculation** - How SegWit reduces transaction size
* **Script validation** - Using btcdeb to validate script execution
* **Efficiency improvements with SegWit** - Witness discount and fee optimization

---

# Output

The scripts generate:

**Console Output:**
* Generated Bitcoin addresses
* Transaction IDs (TXIDs)
* Locking and unlocking scripts
* Witness data for SegWit transactions
* Transaction size comparison
* btcdeb validation commands

**JSON Files:**
* `part1_results.json` - Complete transaction data from Part 1
* `part2_results.json` - Complete transaction data from Part 2

**Script Analysis:**
* Script ASM (assembly) format
* Script HEX format
* Script types (P2PKH, P2SH, etc.)
* Witness data (for SegWit)

---

# Troubleshooting

| Issue | Solution |
|-------|----------|
| `bitcoind not found` | Ensure Bitcoin Core is installed and in PATH |
| `Connection refused` | Ensure bitcoind is running with regtest mode enabled |
| `Authorization failed` | Check RPC credentials in bitcoin.conf match script settings |
| `btcdeb not found` | Install btcdeb or add it to PATH |
| `No UTXOs found` | Ensure previous transaction was mined (run Part 1 before Part 2) |
| `Signing failed` | Check that addresses are in the wallet |
| `JSON serialization error` | Ensure DecimalEncoder is used for JSON output |

---

# Report

A detailed explanation of the implementation, experiment setup, and analysis is provided in the **project report submitted in PDF format**.

---

# References

- [Learning Bitcoin from the Command Line](https://github.com/BlockchainCommons/Learning-Bitcoin-from-the-Command-Line)
- [BIP 16: Pay to Script Hash](https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki)
- [BIP 141: Segregated Witness](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki)
- [btcdeb – Bitcoin Script Debugger](https://github.com/bitcoin-core/btcdeb)
- [python-bitcoinrpc](https://github.com/jgarzik/python-bitcoinrpc)
- [Bitcoin Core Documentation](https://bitcoincore.org/en/doc/)

---
