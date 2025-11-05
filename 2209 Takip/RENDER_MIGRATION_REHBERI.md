# 🔄 Render'da PostgreSQL'e Güvenli Geçiş Rehberi

## ⚠️ KRİTİK: Verileri Koruma Planı

Bu rehber, Render'da PostgreSQL'e geçiş yaparken **verilerinizi korumanızı** sağlar.

---

## 📋 Adım Adım Güvenli Geçiş

### ✅ Adım 1: PostgreSQL Kuruldu (TAMAMLANDI)
- PostgreSQL servisi oluşturuldu
- DATABASE_URL web servisine eklendi

### 🔍 Adım 2: Mevcut Verileri Kontrol Et

Render Shell'den kontrol edin:

```bash
# Render Shell'e girin (web servisinizden)
cd /opt/render/project/src

# SQLite dosyası var mı kontrol et
ls -lh tubitak2209.db

# Tablo sayısını kontrol et
sqlite3 tubitak2209.db "SELECT name FROM sqlite_master WHERE type='table';"
```

**Sonuç:**
- Eğer dosya varsa → Veriler mevcut ✅
- Eğer dosya yoksa → Render'da veri yok (lokal'deki verileri kullan)

---

### 💾 Adım 3: Verileri Yedekle (GÜVENLİK)

```bash
# Render Shell'de
cd /opt/render/project/src
cp tubitak2209.db tubitak2209_backup_$(date +%Y%m%d).db
```

---

### 🚀 Adım 4: Kodları Push Et

```bash
# Bilgisayarınızda
git add config.py requirements.txt migrate_to_postgresql.py
git commit -m "PostgreSQL desteği eklendi"
git push origin main
```

**⚠️ ÖNEMLİ:** Push edildikten sonra Render otomatik deploy başlar.

---

### ⏳ Adım 5: Deploy'u Bekle

1. Render Dashboard → "Events" sekmesine gidin
2. Deploy'un tamamlanmasını bekleyin (2-5 dakika)
3. Deploy tamamlandığında → PostgreSQL'e bağlanır
4. Boş tablolar oluşur (PostgreSQL'de)

**✅ Deploy tamamlandı mı?** → Devam edin

---

### 🔄 Adım 6: Migration Script'i Çalıştır

**YÖNTEM 1: Render Shell'den (ÖNERİLEN)**

```bash
# Render Shell'e girin
cd /opt/render/project/src

# DATABASE_URL'i export et
export DATABASE_URL="postgres://user:pass@host:port/db"

# Migration script'i çalıştır
python migrate_to_postgresql.py
```

**YÖNTEM 2: Lokal Bilgisayardan**

```bash
# Bilgisayarınızda
# Render'dan External Database URL'i alın (sadece migration için)
export DATABASE_URL="postgres://user:pass@host:port/db"
python migrate_to_postgresql.py
```

**⚠️ ÖNEMLİ:** Migration'dan sonra External URL'yi kullanmayın, sadece Internal URL'yi kullanın!

---

### ✅ Adım 7: Verileri Kontrol Et

1. Siteyi açın: https://tubitak2209.onrender.com
2. Giriş yapın
3. Kontrol edin:
   - ✅ Öğrenciler görünüyor mu?
   - ✅ Sınıflar görünüyor mu?
   - ✅ Ödevler görünüyor mu?
   - ✅ Teslimler görünüyor mu?

---

## 🆘 Sorun Giderme

### "Module not found: psycopg2"

```bash
pip install psycopg2-binary
```

### "Table does not exist"

- Önce deploy'un tamamlanmasını bekleyin
- Sonra migration yapın

### "Connection refused"

- Internal Database URL kullandığınızdan emin olun
- Web servisi ve PostgreSQL aynı region'da olmalı

---

## ✅ Başarı Kontrol Listesi

- [ ] PostgreSQL servisi kuruldu
- [ ] DATABASE_URL web servisine eklendi
- [ ] Mevcut veriler kontrol edildi
- [ ] Veriler yedeklendi
- [ ] Kodlar push edildi
- [ ] Deploy tamamlandı
- [ ] Migration script çalıştırıldı
- [ ] Veriler doğru aktarıldı
- [ ] Site çalışıyor

---

**Başarılar! 🎉**

