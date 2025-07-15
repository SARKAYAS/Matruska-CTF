# Matruşka ZIP Çıkarıcı

Bu Python scripti, iç içe geçmiş ZIP arşivlerini otomatik olarak açarak en derindeki `.txt` dosyasına ulaşmak için tasarlanmıştır. Rus matruşka bebeklerine benzer şekilde, her arşivin içinde bir diğerini çıkararak çalışır.

## Özellikler

- İç içe geçmiş `.zip` dosyalarını otomatik olarak açar.
- En sonunda bulunan `.txt` dosyasının yolunu döner ve terminale yazdırır.
- Basit, bağımsız ve kolayca özelleştirilebilir bir yapıdadır.

## Kurulum

1. Bu repoyu klonlayın veya `matruska.py` dosyasını indirin.
2. Python 3 yüklü olduğundan emin olun.
3. Gerekli modüller: `zipfile`, `os` (Python ile birlikte gelir).

## Kullanım

```bash
python matruska.py

Veya doğrudan kod içinde bulunan örnek kullanım satırını düzenleyerek:
extract_deepest("matruska.zip", "output_folder")
