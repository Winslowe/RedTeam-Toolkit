#!/usr/bin/env python3
"""
Wordlist Generator — CUPP Benzeri (Eğitim Amaçlı)
===================================================
Hedef hakkındaki bilgilerden özel şifre listesi üretir.
"""
import sys
import itertools

def gather_info():
    """Hedef bilgilerini topla"""
    print("[*] Hedef hakkında bilgi girin (bilmiyorsanız boş bırakın):\n")
    info = {}
    info['isim'] = input("  İsim          : ").strip().lower()
    info['soyisim'] = input("  Soyisim       : ").strip().lower()
    info['nick'] = input("  Takma ad      : ").strip().lower()
    info['dogum'] = input("  Doğum tarihi  (DDMMYYYY) : ").strip()
    info['partner'] = input("  Sevgili/Eş adı: ").strip().lower()
    info['cocuk'] = input("  Çocuk adı     : ").strip().lower()
    info['evcil'] = input("  Evcil hayvan  : ").strip().lower()
    info['firma'] = input("  Firma/Okul    : ").strip().lower()
    info['ozel'] = input("  Özel kelimeler (virgülle ayır): ").strip().lower()
    return info

def generate_wordlist(info):
    """Kelime listesi üret"""
    words = set()
    base_words = []

    for key in ['isim','soyisim','nick','partner','cocuk','evcil','firma']:
        val = info.get(key, '')
        if val:
            base_words.append(val)
            base_words.append(val.capitalize())
            base_words.append(val.upper())

    if info.get('ozel'):
        for w in info['ozel'].split(','):
            w = w.strip()
            if w:
                base_words.append(w)
                base_words.append(w.capitalize())

    dogum = info.get('dogum', '')
    yil_parcalari = []
    if len(dogum) >= 4:
        yil_parcalari = [dogum, dogum[-4:], dogum[-2:], dogum[:4], dogum[:2]]

    sayilar = ['1','12','123','1234','!','!!','?','*','01','007',
               '321','666','777','999','2024','2025','2026']
    ozel_karakterler = ['!','@','#','$','*','.','_','-']

    # Temel kelimeler
    words.update(base_words)

    # Kelime + sayı kombinasyonları
    for word in base_words:
        for num in sayilar + yil_parcalari:
            words.add(f"{word}{num}")
            words.add(f"{num}{word}")

        for ch in ozel_karakterler:
            words.add(f"{word}{ch}")
            words.add(f"{ch}{word}")

    # İki kelime birleşimleri
    if len(base_words) >= 2:
        for a, b in itertools.combinations(base_words[:8], 2):
            words.add(f"{a}{b}")
            words.add(f"{b}{a}")
            for num in yil_parcalari[:3]:
                words.add(f"{a}{b}{num}")

    # Leet speak
    leet = {'a':'@','e':'3','i':'1','o':'0','s':'$','t':'7'}
    for word in list(base_words)[:5]:
        leet_word = word
        for old, new in leet.items():
            leet_word = leet_word.replace(old, new)
        if leet_word != word:
            words.add(leet_word)

    return sorted(words)

if __name__ == "__main__":
    output = sys.argv[1] if len(sys.argv) > 1 else "custom_wordlist.txt"

    print("=" * 50)
    print("  Wordlist Generator — Hedef Odaklı Şifre Listesi")
    print("=" * 50 + "\n")

    info = gather_info()
    wordlist = generate_wordlist(info)

    with open(output, 'w', encoding='utf-8') as f:
        f.write('\n'.join(wordlist))

    print(f"\n[+] {len(wordlist)} şifre üretildi!")
    print(f"[+] Dosya: {output}")
