@echo off
echo === Windows Temel PrivEsc Kontrol Araci ===
echo.
echo [*] Sistem Bilgileri:
systeminfo | findstr /B /C:"OS Name" /C:"OS Version"
echo.
echo [*] Yamalar ve Guncellemeler:
wmic qfe get Caption,Description,HotFixID,InstalledOn
echo.
echo [*] Diger Kullanicilar:
net users
echo.
echo [*] Hizmetler (Unquoted Service Path kontrolu tavsiye edilir):
wmic service get name,displayname,pathname,startmode | findstr /i "auto" | findstr /i /v "c:\windows\\" | findstr /i /v """"
echo.
echo [+] Kontrol Tamamlandi.
pause
