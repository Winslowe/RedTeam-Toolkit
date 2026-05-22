#!/usr/bin/env python3
"""
Hash Identifier (Eğitim Amaçlı)
================================
Verilen hash değerinin türünü otomatik tespit eder.
"""
import re
import sys

HASH_PATTERNS = [
    (r'^[a-fA-F0-9]{32}$',          'MD5'),
    (r'^[a-fA-F0-9]{40}$',          'SHA-1'),
    (r'^[a-fA-F0-9]{64}$',          'SHA-256'),
    (r'^[a-fA-F0-9]{128}$',         'SHA-512'),
    (r'^[a-fA-F0-9]{56}$',          'SHA-224'),
    (r'^[a-fA-F0-9]{96}$',          'SHA-384'),
    (r'^\$2[aby]\$.{56}$',          'bcrypt'),
    (r'^\$6\$.+\$.{86}$',           'SHA-512 (Unix)'),
    (r'^\$5\$.+\$.{43}$',           'SHA-256 (Unix)'),
    (r'^\$1\$.+\$.{22}$',           'MD5 (Unix)'),
    (r'^[a-fA-F0-9]{32}:[a-fA-F0-9]+$', 'MD5 + Salt'),
    (r'^[a-fA-F0-9]{16}$',          'MySQL (eski) / CRC'),
    (r'^\*[A-F0-9]{40}$',           'MySQL 5.x'),
    (r'^[a-fA-F0-9]{40}:[a-fA-F0-9]+$', 'SHA-1 + Salt'),
]

def identify_hash(hash_value):
    """Hash türünü tespit et"""
    hash_value = hash_value.strip()
    results = []

    for pattern, name in HASH_PATTERNS:
        if re.match(pattern, hash_value):
            results.append(name)

    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python Hash_Identifier.py <HASH_DEĞERI>")
        print("Örnek  : python Hash_Identifier.py 5d41402abc4b2a76b9719d911017c592")
        sys.exit(1)

    h = sys.argv[1]
    print(f"[*] Hash     : {h}")
    print(f"[*] Uzunluk  : {len(h)} karakter")
    print("-" * 50)

    matches = identify_hash(h)
    if matches:
        print("[+] Olası hash türleri:")
        for m in matches:
            print(f"    → {m}")
    else:
        print("[-] Hash türü tespit edilemedi.")
