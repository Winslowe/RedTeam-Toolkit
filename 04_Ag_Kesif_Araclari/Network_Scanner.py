#!/usr/bin/env python3
"""
Network Scanner (Eğitim Amaçlı)
================================
ARP ve ICMP ile yerel ağdaki canlı host'ları tespit eder.
Scapy kütüphanesi gerektirir (pip install scapy)
"""
import sys
import time
try:
    import scapy.all as scapy
except ImportError:
    print("[-] Lütfen 'scapy' kütüphanesini yükleyin: pip install scapy")
    sys.exit(1)

def arp_scan(network):
    """ARP ile yerel ağdaki canlı host'ları tespit et"""
    print(f"[*] ARP taraması başlatıldı: {network}")
    print("-" * 65)
    print(f"{'IP Adresi':<20} {'MAC Adresi':<25} {'Vendor'}")
    print("-" * 65)

    arp_request = scapy.ARP(pdst=network)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    answered_list = scapy.srp(broadcast / arp_request, timeout=3, verbose=False)[0]

    results = []
    for sent, received in answered_list:
        mac = received.hwsrc
        ip = received.psrc
        vendor = mac[:8].upper()
        results.append({"ip": ip, "mac": mac})
        print(f"{ip:<20} {mac:<25} {vendor}")

    print("-" * 65)
    print(f"[+] Toplam {len(results)} canlı host bulundu.\n")
    return results

def icmp_scan(network_base, start=1, end=254):
    """ICMP (Ping) ile host tespiti"""
    print(f"[*] ICMP taraması: {network_base}.{start}-{end}")
    alive = []
    for i in range(start, end + 1):
        ip = f"{network_base}.{i}"
        pkt = scapy.IP(dst=ip) / scapy.ICMP()
        reply = scapy.sr1(pkt, timeout=1, verbose=False)
        if reply:
            alive.append(ip)
            print(f"  [+] {ip} — Aktif")
    print(f"\n[+] ICMP sonucu: {len(alive)} host aktif.")
    return alive

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım:")
        print("  ARP Taraması  : python Network_Scanner.py 192.168.1.0/24")
        print("  ICMP Taraması : python Network_Scanner.py 192.168.1.0/24 --icmp")
        sys.exit(1)

    target = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "--arp"

    if mode == "--icmp":
        base = ".".join(target.split(".")[:3])
        icmp_scan(base)
    else:
        arp_scan(target)
