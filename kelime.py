#!/usr/bin/env python3
"""
replace_in_htmls.py

Kullanım örnekleri:
  # Değişiklikleri uygula (geçerli dizin ve alt dizinler)
  python replace_in_htmls.py /path/to/folder

  # Yalnızca önizleme (değişiklik yapma)
  python replace_in_htmls.py /path/to/folder --dry-run

  # Sadece tek klasörde (alt klasörleri gezmeden)
  python replace_in_htmls.py /path/to/folder --no-recursive
"""

import argparse
import os
import re
import shutil
from datetime import datetime

def try_read(path):
    # Önce UTF-8 dener, olmazsa latin-1 ile okur
    for enc in ("utf-8", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                return f.read(), enc
        except Exception:
            continue
    # en son çare binary olarak oku (decode hata ihtimali düşük)
    with open(path, "rb") as f:
        b = f.read()
    try:
        return b.decode("utf-8", errors="replace"), "utf-8"
    except Exception:
        return b.decode("latin-1", errors="replace"), "latin-1"

def write_with_backup(path, content, encoding):
    bak_path = path + ".bak"
    # Eğer yedek zaten varsa zaman damgası ekle
    if os.path.exists(bak_path):
        stamp = datetime.now().strftime("%Y%m%d%H%M%S")
        bak_path = f"{path}.bak.{stamp}"
    shutil.copy2(path, bak_path)
    with open(path, "w", encoding=encoding) as f:
        f.write(content)
    return bak_path

def process_file(path, pattern, repl, dry_run):
    text, enc = try_read(path)
    new_text, nsubs = re.subn(pattern, repl, text)
    if nsubs > 0:
        if dry_run:
            return True, nsubs, enc, None  # değişiklik olacaktı
        else:
            bak = write_with_backup(path, new_text, enc)
            return True, nsubs, enc, bak
    return False, 0, enc, None

def main():
    ap = argparse.ArgumentParser(description="HTML dosyalarında 'kelimehazinem' -> 'memleketim' değiştirici")
    ap.add_argument("root", nargs="?", default=".", help="İşlenecek klasör (varsayılan: geçerli dizin)")
    ap.add_argument("--dry-run", action="store_true", help="Değişiklik yapma, sadece hangi dosyaların değişeceğini göster")
    ap.add_argument("--no-recursive", action="store_true", help="Alt klasörleri gezme")
    ap.add_argument("--ignore-case", action="store_true", help="Büyük/küçük harf farkını yok say (örn. KelimeHazinem)")
    args = ap.parse_args()

    # Tam kelime eşleşmesi için \b kullanıyoruz.
    flags = re.UNICODE
    if args.ignore_case:
        flags |= re.IGNORECASE
    pattern = re.compile(r"\bkelimehazinem\b", flags)
    repl = "memleketim"

    changed_files = []
    total_subs = 0

    if args.no_recursive:
        files = [os.path.join(args.root, f) for f in os.listdir(args.root) if os.path.isfile(os.path.join(args.root, f))]
    else:
        files = []
        for dirpath, dirnames, filenames in os.walk(args.root):
            for fn in filenames:
                files.append(os.path.join(dirpath, fn))

    html_files = [p for p in files if p.lower().endswith((".html", ".htm"))]

    for p in html_files:
        try:
            changed, nsubs, enc, bak = process_file(p, pattern, repl, args.dry_run)
            if changed:
                changed_files.append((p, nsubs, enc, bak))
                total_subs += nsubs
        except Exception as e:
            print(f"[HATA] {p}: {e}")

    # Özet
    if args.dry_run:
        if changed_files:
            print("DRY-RUN: Aşağıdaki dosyalarda değişiklik yapılacaktır (gerçek değişiklik yapılmadı):")
            for p, n, enc, _ in changed_files:
                print(f" - {p} (değişecek adets: {n}, encoding: {enc})")
            print(f"Toplam {len(changed_files)} dosyada {total_subs} değişiklik.")
        else:
            print("DRY-RUN: Hiç dosyada eşleşme bulunmadı.")
    else:
        if changed_files:
            print("Değiştirilen dosyalar:")
            for p, n, enc, bak in changed_files:
                print(f" - {p} (değişen adets: {n}, encoding: {enc}, yedek: {os.path.basename(bak)})")
            print(f"Toplam {len(changed_files)} dosyada {total_subs} değişiklik yapıldı.")
        else:
            print("Hiç dosyada eşleşme bulunmadı; işlem yapılmadı.")

if __name__ == "__main__":
    main()
