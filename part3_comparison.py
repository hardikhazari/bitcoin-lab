"""
CS 216 - Bitcoin Transaction Lab
Part 3: Comparative Size and Script Analysis
"""

import json
import os

def load_results(filename):
    """Load results from JSON file."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found. Run Part 1 or Part 2 first.")
    
    with open(filename, 'r') as f:
        return json.load(f)

def main():
    print("=" * 80)
    print("  CS 216 - Part 3: Comparative Size and Script Analysis")
    print("=" * 80)

    try:
        # Load results from both parts
        part1_results = load_results("part1_results.json")
        part2_results = load_results("part2_results.json")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # Extract transaction data
    print("\n--- Addresses ---")
    print(f"Legacy Addresses:")
    print(f"  A:  {part1_results['addresses']['A']}")
    print(f"  B:  {part1_results['addresses']['B']}")
    print(f"  C:  {part1_results['addresses']['C']}")
    
    print(f"\nSegWit Addresses:")
    print(f"  A': {part2_results['addresses']['A_prime']}")
    print(f"  B': {part2_results['addresses']['B_prime']}")
    print(f"  C': {part2_results['addresses']['C_prime']}")

    # Extract transaction IDs
    print("\n--- Transaction IDs ---")
    print(f"Legacy A->B: {part1_results['tx_A_to_B']['txid']}")
    print(f"Legacy B->C: {part1_results['tx_B_to_C']['txid']}")
    print(f"SegWit A'->B': {part2_results['tx_Ap_to_Bp']['txid']}")
    print(f"SegWit B'->C': {part2_results['tx_Bp_to_Cp']['txid']}")

    # Extract and display scripts
    print("\n--- Legacy P2PKH Scripts ---")
    
    # A->B locking script
    for vout in part1_results['tx_A_to_B']['decoded']['vout']:
        if vout['scriptPubKey'].get('address') == part1_results['addresses']['B']:
            print(f"\nA->B Locking Script (ScriptPubKey):")
            print(f"  ASM: {vout['scriptPubKey']['asm']}")
            print(f"  HEX: {vout['scriptPubKey']['hex']}")
            print(f"  Type: {vout['scriptPubKey']['type']}")
    
    # B->C unlocking script
    for vin in part1_results['tx_B_to_C']['decoded']['vin']:
        print(f"\nB->C Unlocking Script (ScriptSig):")
        print(f"  ASM: {vin.get('scriptSig', {}).get('asm', '(empty)')}")
        print(f"  HEX: {vin.get('scriptSig', {}).get('hex', '(empty)')}")

    print("\n--- SegWit P2SH-P2WPKH Scripts ---")
    
    # A'->B' locking script
    for vout in part2_results['tx_Ap_to_Bp']['decoded']['vout']:
        if vout['scriptPubKey'].get('address') == part2_results['addresses']['B_prime']:
            print(f"\nA'->B' Locking Script (ScriptPubKey):")
            print(f"  ASM: {vout['scriptPubKey']['asm']}")
            print(f"  HEX: {vout['scriptPubKey']['hex']}")
            print(f"  Type: {vout['scriptPubKey']['type']}")
    
    # B'->C' witness data
    for vin in part2_results['tx_Bp_to_Cp']['decoded']['vin']:
        print(f"\nB'->C' Witness Data:")
        print(f"  Witness: {vin.get('txinwitness', [])}")
        print(f"  ScriptSig (Redeem Script): {vin.get('scriptSig', {}).get('asm', '(empty)')}")

    # Size comparison
    print("\n" + "=" * 80)
    print("--- Transaction Size Comparison ---")
    print("=" * 80)
    
    # Get sizes from decoded transactions
    tx_1_size = len(part1_results['signed_hex_BC']) // 2
    tx_2_size = len(part2_results['signed_hex_BC']) // 2
    
    # Get vsize and weight if available
    tx_1_vsize = part1_results['tx_B_to_C']['decoded'].get('vsize', 'N/A')
    tx_1_weight = part1_results['tx_B_to_C']['decoded'].get('weight', 'N/A')
    
    tx_2_vsize = part2_results['tx_Bp_to_Cp']['decoded'].get('vsize', 'N/A')
    tx_2_weight = part2_results['tx_Bp_to_Cp']['decoded'].get('weight', 'N/A')
    
    header = f"{'Metric':<25} {'Legacy (B->C)':<20} {'SegWit (B-prime->C-prime)':<25} {'Difference':<15}"
    print(header)
    print("-" * 85)
    
    size_diff = tx_1_size - tx_2_size
    size_pct = (size_diff / tx_1_size * 100) if tx_1_size > 0 else 0
    print(f"{'Raw Size (bytes)':<25} {tx_1_size:<20} {tx_2_size:<25} {size_diff} ({size_pct:.1f}%)")
    
    if tx_1_vsize != 'N/A' and tx_2_vsize != 'N/A':
        vsize_diff = tx_1_vsize - tx_2_vsize
        vsize_pct = (vsize_diff / tx_1_vsize * 100) if tx_1_vsize > 0 else 0
        print(f"{'Virtual Size (vbytes)':<25} {tx_1_vsize:<20} {tx_2_vsize:<25} {vsize_diff} ({vsize_pct:.1f}%)")
    
    if tx_1_weight != 'N/A' and tx_2_weight != 'N/A':
        weight_diff = tx_1_weight - tx_2_weight
        weight_pct = (weight_diff / tx_1_weight * 100) if tx_1_weight > 0 else 0
        print(f"{'Weight (units)':<25} {tx_1_weight:<20} {tx_2_weight:<25} {weight_diff} ({weight_pct:.1f}%)")

    print("\n" + "=" * 80)
    print("Key Observations:")
    print("=" * 80)
    print("1. Legacy P2PKH transactions include signature and public key in scriptSig")
    print("2. SegWit P2SH-P2WPKH transactions move witness data outside the base transaction")
    print("3. Virtual size (vsize) accounts for witness data at 1/4 weight")
    print("4. SegWit transactions are typically smaller in vsize due to witness discount")
    print("5. For fee calculation, vsize is used instead of raw size")
    print("=" * 80)

if __name__ == "__main__":
    main()
