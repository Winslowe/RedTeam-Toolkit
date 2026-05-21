#!/bin/bash
# Kurulum ve Çalıştırma Scripti (Linux/Kali)

echo -e "\e[1;32m========================================================\e[0m"
echo -e "\e[1;32m       THE ULTIMATE PENTEST ARSENAL KURULUM\e[0m"
echo -e "\e[1;32m========================================================\e[0m"
echo -e "\n[*] Gerekli Python kütüphaneleri kuruluyor, lütfen bekleyin...\n"

pip3 install -r requirements.txt

echo -e "\n[+] Kurulum tamamlandı!"
echo -e "[+] Program başlatılıyor...\n"

python3 RedTeam_C2.py
