#!/usr/bin/env python3
"""
Port Tarama ve Açık Port Bulucu
================================
Hedef makinenin güvenlik duvarında hangi portların
dışarıya açık olduğunu tespit eder.

Önce bu scriptle açık portları bulun, sonra reverse shell'inizi
o port üzerinden kurun.

KULLANIM:
---------
  python3 4_Port_Scanner.py --target 10.10.14.1

NOT: Yalnızca izinli test ortamlarında kullanın.
"""

import socket
import sys
import argparse
import concurrent.futures
from datetime import datetime

# Güvenlik duvarlarının genelde izin verdiği yaygın portlar
COMMON_ALLOWED_PORTS = [
    20, 21,       # FTP
    22,           # SSH
    25,           # SMTP
    53,           # DNS - neredeyse her zaman açık!
    80,           # HTTP - neredeyse her zaman açık!
    110,          # POP3
    143,          # IMAP
    443,          # HTTPS - neredeyse her zaman açık!
    445,          # SMB
    587,          # SMTP TLS
    993,          # IMAPS
    995,          # POP3S
    3306,         # MySQL
    3389,         # RDP
    5432,         # PostgreSQL
    5900,         # VNC
    8080,         # HTTP Alternatif
    8443,         # HTTPS Alternatif
    8888,         # Alternatif Web
]

def scan_port(target, port, timeout=1):
    """Tek bir portu tarar."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()
        
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except OSError:
                service = "bilinmiyor"
            return port, True, service
        return port, False, None
    except Exception:
        return port, False, None

def scan_target(target, ports=None, threads=50):
    """Hedefi tarar ve açık portları listeler."""
    if ports is None:
        ports = COMMON_ALLOWED_PORTS
    
    # ANSI Renk Kodları
    class Colors:
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        CYAN = '\033[96m'
        RESET = '\033[0m'
        BOLD = '\033[1m'
        
    print(f"\n{Colors.CYAN}{'='*55}")
    print(f"  Hedef: {Colors.BOLD}{target}{Colors.RESET}{Colors.CYAN}")
    print(f"  Taranan Port Sayısı: {len(ports)}")
    print(f"  Başlangıç: {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*55}{Colors.RESET}\n")
    
    open_ports = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(scan_port, target, port): port 
            for port in ports
        }
        
        for future in concurrent.futures.as_completed(futures):
            port, is_open, service = future.result()
            if is_open:
                open_ports.append((port, service))
                print(f"  {Colors.GREEN}[+] Port {port:>5}/tcp  AÇIK  ({service}){Colors.RESET}")
    
    open_ports.sort(key=lambda x: x[0])
    
    print(f"\n{Colors.CYAN}{'='*55}")
    print(f"  Tarama Tamamlandı: {datetime.now().strftime('%H:%M:%S')}")
    print(f"  Açık Port Sayısı: {Colors.BOLD}{len(open_ports)}{Colors.RESET}{Colors.CYAN}")
    print(f"{'='*55}{Colors.RESET}")
    
    if open_ports:
        print(f"\n  {Colors.YELLOW}[*] ÖNERİLEN REVERSE SHELL PORTLARI:{Colors.RESET}")
        priority_ports = [443, 80, 53, 8080, 8443]
        for port, service in open_ports:
            if port in priority_ports:
                print(f"      {Colors.YELLOW}★ Port {port} ({service}) - Yüksek öncelik, güvenlik duvarı genelde izin verir{Colors.RESET}")
    
    return open_ports

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Güvenlik Duvarı Port Tarayıcı")
    parser.add_argument("--target", "-t", required=True, help="Hedef IP adresi")
    parser.add_argument("--all", action="store_true", help="Tüm portları tara (1-65535)")
    parser.add_argument("--threads", type=int, default=50, help="Thread sayısı (varsayılan: 50)")
    
    args = parser.parse_args()
    
    if args.all:
        ports = list(range(1, 65536))
    else:
        ports = COMMON_ALLOWED_PORTS
    
    scan_target(args.target, ports, args.threads)
