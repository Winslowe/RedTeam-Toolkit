import os
import sys
import time

# Enable ANSI escape sequences on Windows
os.system('')

# Colors
R = '\033[91m'
G = '\033[92m'
Y = '\033[93m'
C = '\033[96m'
W = '\033[0m'
D = '\033[90m'

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
    base_dir = os.path.dirname(os.path.abspath(__file__))
    folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f)) and f[0].isdigit()]
    return sorted(folders)

def list_files(category_folder):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    cat_dir = os.path.join(base_dir, category_folder)
    files = [f for f in os.listdir(cat_dir) if f.endswith('.py') or f.endswith('.bat')]
    return sorted(files)

def run_script(path):
    clear_screen()
    print(f"{C}[*] Çalıştırılıyor: {path}{W}\n")
    os.system(f'python "{path}"' if path.endswith('.py') else f'"{path}"')
    input(f"\n{Y}[!] Devam etmek için ENTER tuşuna basın...{W}")

def main_menu():
    while True:
        clear_screen()
        print(ASCII_ART)
        categories = get_categories()
        
        print(f"{C}[ M E N Ü ]{W}\n")
        print(f"  {G}0.{W} Komuta_Kontrol_Merkezi_C2.py {R}[🔥 ANA SİSTEM]{W}")
        print(f"  {G}00.{W} Oto_Sizma_Araci.py {R}[⚔️ OTOMASYON]{W}")
        print()
        
        for i, cat in enumerate(categories, 1):
            cat_name = cat.split('_', 1)[1].replace('_', ' ')
            print(f"  {G}{i}.{W} {cat_name}")
            
        print(f"\n  {R}99.{W} Çıkış")
        
        choice = input(f"\n{Y}arsenal@karargah:~# {W}").strip()
        
        if choice == '99':
            print(f"{C}[*] Sistemden çıkılıyor... Güvende kalın!{W}")
            sys.exit(0)
        elif choice == '0':
            run_script('Komuta_Kontrol_Merkezi_C2.py')
        elif choice == '00':
            run_script('Oto_Sizma_Araci.py')
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
            script_path = os.path.join(cat_folder, files[int(choice)-1])
            run_script(script_path)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{R}[!] Zorla çıkış yapıldı.{W}")
        sys.exit(0)
