# CS216 Bitcoin Transaction Lab

### Legacy vs SegWit Transaction Implementation

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

The implementation uses **Bitcoin Core running in Regtest mode** along with Python scripts that interact with the Bitcoin node using RPC calls.

The goal of this lab is to understand:

* How Bitcoin transactions are constructed
* The structure of locking and unlocking scripts
* The difference between Legacy and SegWit transactions
* Transaction size and efficiency improvements introduced by SegWit

---

# Project Structure

```
bitcoin-lab/
│
├── part1_p2pkh.py          # Implementation of Legacy P2PKH transactions
├── part2_segwit.py         # Implementation of SegWit P2SH-P2WPKH transactions
├── requirements.txt        # Python dependencies
├── report_template.md      # Template for the lab report
└── README.md               # Instructions to run the project
```

---

# Requirements

Before running the scripts, install the following:

* Python 3.8 or above
* Bitcoin Core
* Python packages listed in `requirements.txt`

Install dependencies using:

```
pip install -r requirements.txt
```

---

# Running the Bitcoin Node

Start Bitcoin Core in **regtest mode**.

Example command:

```
bitcoind -regtest
```

Ensure that RPC is enabled and properly configured in `bitcoin.conf`.

---

# Running the Programs

### Run Part 1 (Legacy Transactions)

```
python part1_p2pkh.py
```

This script:

* Creates Legacy (P2PKH) addresses

* Funds an address

* Executes transactions:

  A → B
  B → C

* Prints the locking and unlocking scripts used in the transaction.

---

### Run Part 2 (SegWit Transactions)

```
python part2_segwit.py
```

This script:

* Creates SegWit addresses
* Performs transactions using **P2SH-P2WPKH**
* Displays witness data and redeem scripts
* Compares transaction size and weight.

---

# Key Concepts Demonstrated

The project highlights several important Bitcoin concepts:

* Bitcoin Script
* Locking and Unlocking Scripts
* Pay-to-Public-Key-Hash (P2PKH)
* Segregated Witness (SegWit)
* Transaction size and weight calculation
* Efficiency improvements with SegWit

---

# Output

The scripts generate console outputs including:

* Generated Bitcoin addresses
* Transaction IDs (TXIDs)
* Locking and unlocking scripts
* Witness data for SegWit transactions
* Transaction size comparison

---

# Report

A detailed explanation of the implementation, experiment setup, and analysis is provided in the **project report submitted in PDF format**.

---
