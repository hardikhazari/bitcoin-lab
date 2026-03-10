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

1.  **Legacy Transactions (P2PKH)**
2.  **SegWit Transactions (P2SH-P2WPKH)**

The implementation uses **Bitcoin Core running in Regtest mode** along with Python scripts that interact with the Bitcoin node using RPC calls. The project now includes **comprehensive Bitcoin debugger (btcdeb) integration** to validate and analyze transaction scripts.

The goal of this lab is to understand:

*   How Bitcoin transactions are constructed
*   The structure of locking and unlocking scripts
*   The difference between Legacy and SegWit transactions
*   Transaction size and efficiency improvements introduced by SegWit
*   Script validation using the Bitcoin debugger (btcdeb)
*   Transaction analysis and comparison

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

*   Python 3.8 or above
*   Bitcoin Core
*   [btcdeb](https://github.com/bitcoin-core/btcdeb) (Bitcoin Script Debugger)
*   Python packages listed in `requirements.txt`

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

# Linux Setup Guide

This section provides detailed instructions for setting up and running the Bitcoin Transaction Lab on a Linux system (e.g., Ubuntu).

## 1. Install Python and Dependencies

Ensure you have Python 3.8 or newer installed. Most modern Linux distributions come with Python pre-installed. You can check your version with:

```bash
python3 --version
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## 2. Install Bitcoin Core

Bitcoin Core is essential for running a local Bitcoin `regtest` network. Follow these steps to install it on Ubuntu:

```bash
# Update package list
sudo apt update

# Install necessary dependencies
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:bitcoin/bitcoin
sudo apt update

# Install Bitcoin Core
sudo apt install -y bitcoind bitcoin-cli
```

## 3. Configure Bitcoin Core (`bitcoin.conf`)

Create or edit the `bitcoin.conf` file in the Bitcoin data directory. For Linux, this is typically `~/.bitcoin/bitcoin.conf`.

```bash
mkdir -p ~/.bitcoin
nano ~/.bitcoin/bitcoin.conf
```

Add the following configuration to the `bitcoin.conf` file. Replace `user` and `password` with your desired RPC credentials.

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

Save and close the file (Ctrl+O, Enter, Ctrl+X in nano).

## 4. Install `btcdeb` (Bitcoin Script Debugger)

`btcdeb` is crucial for script validation. It must be built from source on Ubuntu 24.04 and later due to compatibility issues with default build flags. Follow these steps:

```bash
# Install build dependencies
sudo apt update
sudo apt install -y git build-essential libtool autotools-dev automake pkg-config libssl-dev

# Clone btcdeb repository
git clone https://github.com/bitcoin-core/btcdeb.git
cd btcdeb

# Configure with fortify and asm disabled to prevent buffer overflow issues
./autogen.sh
./configure CXXFLAGS="-O0 -U_FORTIFY_SOURCE" CFLAGS="-O0 -U_FORTIFY_SOURCE" --disable-asm

# Build btcdeb
make

# (Optional) Install btcdeb system-wide
sudo make install

# Verify installation
btcdeb '[OP_1 OP_1 OP_ADD OP_2 OP_EQUAL]'
```

If `btcdeb` is not installed system-wide, you will need to run it from the `btcdeb` directory using `./btcdeb`.

---

# Running the Bitcoin Node

Before executing any Python scripts, you must start the Bitcoin Core daemon in `regtest` mode. Open a new terminal and run:

```bash
bitcoind -regtest -daemon
```

This will start `bitcoind` in the background. You can check its status with `bitcoin-cli -regtest getblockchaininfo`.

To stop `bitcoind` when you are done:

```bash
bitcoin-cli -regtest stop
```

---

# Running the Programs

Navigate to the `bitcoin-lab` directory in your terminal.

### Update RPC Credentials

Before running, open `part1_p2pkh.py` and `part2_segwit.py` and update the `RPC_USER` and `RPC_PASSWORD` variables to match the credentials you set in your `bitcoin.conf`.

```python
# RPC Configuration
RPC_USER = "your_rpc_user" # e.g., "user"
RPC_PASSWORD = "your_rpc_password" # e.g., "password"
RPC_HOST = "127.0.0.1"
RPC_PORT = "18443"
```

### Run Part 1 (Legacy Transactions)

```bash
python3 part1_p2pkh.py
```

This script:

*   Creates Legacy (P2PKH) addresses (A, B, C)
*   Funds Address A with 10 BTC
*   Executes transactions: A → B → C
*   Displays locking and unlocking scripts
*   Generates btcdeb validation commands
*   Saves results to `part1_results.json`
*   Attempts to validate scripts using btcdeb

**Output includes:**
-   Generated Bitcoin addresses
-   Transaction IDs (TXIDs)
-   Locking scripts (ScriptPubKey) for A→B
-   Unlocking scripts (ScriptSig) for B→C
-   btcdeb command for manual validation

---

### Run Part 2 (SegWit Transactions)

```bash
python3 part2_segwit.py
```

This script:

*   Creates SegWit (P2SH-P2WPKH) addresses (A’, B’, C’)
*   Funds Address A’ with 10 BTC
*   Executes transactions: A’ → B’ → C’
*   Displays witness data and redeem scripts
*   Shows transaction size, virtual size, and weight
*   Generates btcdeb validation commands
*   Saves results to `part2_results.json`
*   Attempts to validate scripts using btcdeb

**Output includes:**
-   Generated SegWit addresses
-   Transaction IDs (TXIDs)
-   Locking scripts (ScriptPubKey) for A’→B’
-   Witness data for B’→C’
-   Redeem scripts (ScriptSig)
-   Transaction size metrics
-   btcdeb command for manual validation

---

### Run Part 3 (Comparative Analysis)

```bash
python3 part3_comparison.py
```

This script:

*   Loads results from `part1_results.json` and `part2_results.json`
*   Displays all addresses and transaction IDs
*   Compares locking and unlocking scripts
*   Analyzes transaction sizes (raw, virtual, weight)
*   Calculates efficiency improvements with SegWit
*   Provides key observations about script differences

**Prerequisites:** Run Part 1 and Part 2 before running Part 3.

---

# Bitcoin Debugger (btcdeb) Integration

## What is btcdeb?

**btcdeb** is the Bitcoin Script Debugger, a tool that allows you to step through Bitcoin script execution line by line. It helps validate that scripts execute correctly and understand how Bitcoin's scripting language works.

## How It's Integrated

The scripts now automatically:

1.  **Extract scripts** from transactions (locking and unlocking scripts)
2.  **Generate btcdeb commands** with proper formatting
3.  **Display validation commands** for manual execution
4.  **Attempt automatic validation** (if btcdeb is installed and in PATH)

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

-   **Stack** shows the current values on the stack
-   **Script** shows remaining operations to execute
-   **Altstack** shows values in the alternate stack (if used)
-   Each `step` executes one operation
-   The final stack should contain `1` (true) for valid scripts

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

*   **Bitcoin Script** - The stack-based scripting language used by Bitcoin
*   **Locking and Unlocking Scripts** - How transactions lock and unlock UTXOs
*   **Pay-to-Public-Key-Hash (P2PKH)** - Legacy transaction format
*   **Segregated Witness (SegWit)** - Improved transaction format with witness data separation
*   **Transaction size and weight calculation** - How SegWit reduces transaction size
*   **Script validation** - Using btcdeb to validate script execution
*   **Efficiency improvements with SegWit** - Witness discount and fee optimization

---

# Output

The scripts generate:

**Console Output:**
*   Generated Bitcoin addresses
*   Transaction IDs (TXIDs)
*   Locking and unlocking scripts
*   Witness data for SegWit transactions
*   Transaction size comparison
*   btcdeb validation commands

**JSON Files:**
*   `part1_results.json` - Complete transaction data from Part 1
*   `part2_results.json` - Complete transaction data from Part 2

**Script Analysis:**
*   Script ASM (assembly) format
*   Script HEX format
*   Script types (P2PKH, P2SH, etc.)
*   Witness data (for SegWit)

---

# Troubleshooting

| Issue | Solution |
|-------|----------|
| `bitcoind not found` | Ensure Bitcoin Core is installed and in PATH. Follow "Install Bitcoin Core" steps. |
| `Connection refused` | Ensure `bitcoind -regtest -daemon` is running. Check `bitcoin.conf` for correct `rpcport` and `rpcallowip`. |
| `Authorization failed` | Check `RPC_USER` and `RPC_PASSWORD` in Python scripts match `bitcoin.conf`. Ensure `[regtest]` section is correctly formatted in `bitcoin.conf`. |
| `btcdeb not found` | Install `btcdeb` by following "Install `btcdeb`" steps. Ensure it's in your PATH or run it from its directory. |
| `No UTXOs found` | Ensure previous transaction was mined (run Part 1 before Part 2). Check `bitcoind` is generating blocks. |
| `Signing failed` | Check that addresses are in the wallet and have sufficient funds. |
| `JSON serialization error` | This should be handled by `DecimalEncoder`. If it persists, ensure `decimal` is imported and `cls=DecimalEncoder` is used in `json.dump`. |
| `SyntaxError: invalid character` | Ensure your terminal and editor support UTF-8. Replace special characters (like ’ or →) with standard ASCII equivalents (e.g., ' or ->). |

---

# Report

A detailed explanation of the implementation, experiment setup, and analysis is provided in the **project report submitted in PDF format**.

---

# References

-   [Learning Bitcoin from the Command Line](https://github.com/BlockchainCommons/Learning-Bitcoin-from-the-Command-Line)
-   [BIP 16: Pay to Script Hash](https://github.com/bitcoin/bips/blob/master/bip-0016.mediawiki)
-   [BIP 141: Segregated Witness](https://github.com/bitcoin/bips/blob/master/bip-0141.mediawiki)
-   [btcdeb – Bitcoin Script Debugger](https://github.com/bitcoin-core/btcdeb)
-   [python-bitcoinrpc](https://github.com/jgarzik/python-bitcoinrpc)
-   [Bitcoin Core Documentation](https://bitcoincore.org/en/doc/)

---
