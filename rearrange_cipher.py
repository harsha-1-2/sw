#!/usr/bin/env python3
"""
rearrange_cipher.py

Encrypt: collect chars at even indices (0-based), then chars at odd indices.
Decrypt: given encrypted string produced by the same method, reconstruct original.

Usage:
    python rearrange_cipher.py         # interactive demo
    python rearrange_cipher.py -e "message"   # encrypt
    python rearrange_cipher.py -d "msaeesg"   # decrypt
"""

import sys
import argparse
from math import ceil

def encrypt(s: str) -> str:
    # Even-indexed characters (0,2,4,...) then odd-indexed characters (1,3,5,...)
    even_chars = s[0::2]
    odd_chars = s[1::2]
    return even_chars + odd_chars

def decrypt(encrypted: str) -> str:
    n = len(encrypted)
    evencount = (n + 1) // 2   # ceil(n/2)
    even_part = encrypted[:evencount]
    odd_part = encrypted[evencount:]
    result_chars = [''] * n
    # fill even indices
    ei = 0
    for i in range(0, n, 2):
        result_chars[i] = even_part[ei]
        ei += 1
    # fill odd indices
    oi = 0
    for i in range(1, n, 2):
        # odd_part may be shorter when n is odd, but loops align
        result_chars[i] = odd_part[oi]
        oi += 1
    return ''.join(result_chars)

# Small self-test / examples
def _run_tests():
    tests = [
        ("message", "msaeesg"),
        ("hello", "hlleo"),  # even h,l,o => hlo then odd e,l => hlleo
        ("abcd", "acbd"),    # even a,c => ac + odd b,d => bd => acbd
        ("a", "a"),
        ("", "")
    ]
    passed = True
    for orig, expected_enc in tests:
        enc = encrypt(orig)
        dec = decrypt(enc)
        ok = (enc == expected_enc and dec == orig)
        print(f"orig: {orig!r:10} enc: {enc!r:10} expected: {expected_enc!r:10} dec: {dec!r:10} -> {'OK' if ok else 'FAIL'}")
        if not ok:
            passed = False
    if passed:
        print("\nAll tests passed.")
    else:
        print("\nSome tests failed.")

def main():
    parser = argparse.ArgumentParser(description="Encrypt/decrypt by even-then-odd reordering.")
    parser.add_argument("-e", "--encrypt", help="Encrypt the given string", type=str)
    parser.add_argument("-d", "--decrypt", help="Decrypt the given string (produced by this method)", type=str)
    parser.add_argument("--test", action="store_true", help="Run built-in tests")
    args = parser.parse_args()

    if args.test:
        _run_tests()
        return

    if args.encrypt is None and args.decrypt is None:
        # interactive demo
        print("Rearrange Cipher Interactive Demo")
        s = input("Enter a message to encrypt: ")
        enc = encrypt(s)
        print("Encrypted:", enc)
        dec = decrypt(enc)
        print("Decrypted back:", dec)
        return

    if args.encrypt is not None:
        enc = encrypt(args.encrypt)
        print(enc)
    elif args.decrypt is not None:
        dec = decrypt(args.decrypt)
        print(dec)

if __name__ == "__main__":
    main()
