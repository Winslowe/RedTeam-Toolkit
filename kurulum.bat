@echo off
title The Ultimate Pentest Arsenal Kurulum
color 0A

echo ========================================================
echo        THE ULTIMATE PENTEST ARSENAL KURULUM
echo ========================================================
echo.
echo [*] Gerekli Python kutuphaneleri kuruluyor, lutfen bekleyin...
echo.

pip install -r requirements.txt

echo.
echo [+] Kurulum tamamlandi!
echo [+] Program baslatiliyor...
echo.

python RedTeam_C2.py
pause
