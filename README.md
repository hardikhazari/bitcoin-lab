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

# Windows Installation Guide (via Terminal)

Since `btcdeb` is a Linux-native tool, the best way to run it on Windows is through **WSL (Windows Subsystem for Linux)**. This allows you to run the debugger directly from your Windows terminal.

## 1. Enable WSL and Install Ubuntu

Open **PowerShell** or **Command Prompt** as Administrator and run:

```powershell
wsl --install
```

After the installation completes, restart your computer. Once restarted, a terminal will open to complete the Ubuntu setup (it will ask for a username and password).

## 2. Install `btcdeb` in WSL Terminal

Open your **Ubuntu** terminal (search for "Ubuntu" in the Start menu) and run the following commands to build `btcdeb` from source:

```bash
# Update package list and install build dependencies
sudo apt update
sudo apt install -y git build-essential libtool autotools-dev automake pkg-config libssl-dev

# Clone btcdeb repository
git clone https://github.com/bitcoin-core/btcdeb.git
cd btcdeb

# Configure and build
./autogen.sh
./configure CXXFLAGS="-O0 -U_FORTIFY_SOURCE" CFLAGS="-O0 -U_FORTIFY_SOURCE" --disable-asm
make

# Install btcdeb system-wide in WSL
sudo make install

# Verify installation
btcdeb '[OP_1 OP_1 OP_ADD OP_2 OP_EQUAL]'
```

## 3. Running the Python Scripts on Windows

You can continue to run your Python scripts in your Windows terminal (PowerShell/CMD). When the script prints a `btcdeb` command, you can simply copy and paste it into your **Ubuntu (WSL)** terminal to debug the script.

---

# Linux Setup Guide

If you are using a native Linux system (e.g., Ubuntu), follow these steps:

## 1. Install Bitcoin Core

```bash
sudo apt update
sudo apt install -y software-properties-common
sudo add-apt-repository -y ppa:bitcoin/bitcoin
sudo apt update
sudo apt install -y bitcoind bitcoin-cli
```

## 2. Configure Bitcoin Core (`bitcoin.conf`)

Create or edit `~/.bitcoin/bitcoin.conf`:

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

# Running the Bitcoin Node

Before executing any Python scripts, start the Bitcoin Core daemon in `regtest` mode:

```bash
bitcoind -regtest -daemon
```

To stop `bitcoind`:

```bash
bitcoin-cli -regtest stop
```

---

# Running the Programs

### Run Part 1 (Legacy Transactions)

```bash
python3 part1_p2pkh.py
```

### Run Part 2 (SegWit Transactions)

```bash
python3 part2_segwit.py
```

### Run Part 3 (Comparative Analysis)

```bash
python3 part3_comparison.py
```

---

# Bitcoin Debugger (btcdeb) Integration

The scripts automatically generate `btcdeb` commands. Copy the generated command from your Windows terminal and paste it into your **WSL/Ubuntu terminal** to step through the script execution.

Example command:
```bash
btcdeb '[<signature> <pubkey> OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG]' --tx=<transaction_hex>
```

Type `step` in the `btcdeb` interface to execute operations one by one.

---

# Troubleshooting

| Issue | Solution |
|-------|----------|
| `btcdeb command not found` | Ensure you are running the command in the **WSL/Ubuntu terminal** after following the installation steps. |
| `Connection refused` | Ensure `bitcoind -regtest -daemon` is running. |
| `Authorization failed` | Check `RPC_USER` and `RPC_PASSWORD` in Python scripts match `bitcoin.conf`. |

---

# References

-   [Learning Bitcoin from the Command Line](https://github.com/BlockchainCommons/Learning-Bitcoin-from-the-Command-Line)
-   [btcdeb – Bitcoin Script Debugger](https://github.com/bitcoin-core/btcdeb)
-   [Bitcoin Core Documentation](https://bitcoincore.org/en/doc/)

---
