# 🐘 PostgreSQL'e Geçiş Rehberi

Bu rehber, Render.com'da PostgreSQL kurulumu ve SQLite verilerinin PostgreSQL'e aktarılması için adım adım talimatlar içerir.

---

## 📋 Adım 1: Render'da PostgreSQL Servisi Oluşturma

### 1.1. PostgreSQL Servisi Ekleme

1. **Render Dashboard**'a gidin: https://dashboard.render.com
2. Sağ üstteki **"New +"** butonuna tıklayın
3. Açılan menüden **"PostgreSQL"** seçeneğini seçin

### 1.2. PostgreSQL Ayarları

Aşağıdaki ayarları yapın:

- **Name:** `tubitak2209-db` (veya istediğiniz bir isim)
- **Database:** `tubitak2209` (veya boş bırakın, otomatik oluşturulur)
- **User:** `tubitak2209_user` (veya boş bırakın)
- **Region:** Web servisinizle **aynı region**'ı seçin (örn: Frankfurt, Oregon)
- **PostgreSQL Version:** `16` (veya en son sürüm)
- **Plan:** **Free** (başlangıç için yeterli)

### 1.3. Oluşturma

1. **"Create Database"** butonuna tıklayın
2. PostgreSQL servisi oluşturulurken bekleyin (1-2 dakika)

---

## 🔗 Adım 2: PostgreSQL Bağlantı Bilgilerini Alma

### 2.1. Internal Database URL

1. PostgreSQL servisinize tıklayın
2. **"Connections"** sekmesine gidin
3. **"Internal Database URL"** kısmındaki URL'yi kopyalayın

   Örnek format:
   ```
   postgres://tubitak2209_user:password@dpg-xxxxx-a.frankfurt-postgres.render.com/tubitak2209
   ```

### 2.2. Bu URL'yi Not Edin

Bu URL'yi sonraki adımda kullanacağız.

---

## ⚙️ Adım 3: Web Servisine DATABASE_URL Ekleme

### 3.1. Environment Variables

1. **Web servisinize** (`tubitak2209`) gidin
2. **"Environment"** sekmesine tıklayın (sol menüden)
3. **"Environment Variables"** bölümüne gidin
4. **"Add Environment Variable"** butonuna tıklayın

### 3.2. DATABASE_URL Ekleme

- **Key:** `DATABASE_URL`
- **Value:** PostgreSQL'in **Internal Database URL**'sini yapıştırın

5. **"Save Changes"** butonuna tıklayın

---

## 💾 Adım 4: SQLite Verilerini PostgreSQL'e Aktarma

### 4.1. Render Shell'den Migration

**YÖNTEM 1: Render Shell (Önerilen)**

1. Web servisinizin **"Shell"** sekmesine gidin
2. Aşağıdaki komutları çalıştırın:

```bash
# 1. Proje klasörüne git
cd /opt/render/project/src

# 2. Migration script'ini çalıştır
python migrate_to_postgresql.py
```

3. **DATABASE_URL** sorulduğunda, PostgreSQL'in Internal Database URL'ini yapıştırın
4. Onay verin (`evet` yazın)

### 4.2. Lokal Bilgisayardan Migration

**YÖNTEM 2: Lokal Bilgisayarınızdan**

1. Bilgisayarınızda proje klasörüne gidin
2. Render'dan PostgreSQL'in **External Database URL**'sini alın (sadece migration için)
3. Terminal'de:

```bash
# PowerShell
$env:DATABASE_URL="postgres://user:pass@host:port/db"
python migrate_to_postgresql.py
```

**⚠️ ÖNEMLİ:** Migration'dan sonra External URL'yi kullanmayın, sadece Internal URL'yi kullanın!

---

## 🚀 Adım 5: Deploy ve Test

### 5.1. Deploy

1. Kod değişikliklerini GitHub'a push edin:

```bash
git add .
git commit -m "PostgreSQL desteği eklendi"
git push origin main
```

2. Render otomatik deploy başlayacak

### 5.2. Test

1. Site açıldığında:
   - ✅ Öğrenciler görünüyor mu?
   - ✅ Sınıflar görünüyor mu?
   - ✅ Ödevler görünüyor mu?
   - ✅ Teslimler görünüyor mu?

2. Yeni bir öğrenci kaydı yapın
3. Veritabanında kayıtlı mı kontrol edin

---

## ✅ Başarı Kontrol Listesi

- [ ] PostgreSQL servisi oluşturuldu
- [ ] Internal Database URL alındı
- [ ] Web servisine DATABASE_URL eklendi
- [ ] Migration script çalıştırıldı
- [ ] Tüm veriler aktarıldı
- [ ] Deploy yapıldı
- [ ] Site çalışıyor
- [ ] Veriler görünüyor

---

## 🔧 Sorun Giderme

### "Module not found: psycopg2"

```bash
pip install psycopg2-binary
```

### "Connection refused"

- Internal Database URL kullandığınızdan emin olun
- Web servisi ve PostgreSQL aynı region'da olmalı

### "Table does not exist"

- Önce web servisini deploy edin (tabloları oluşturur)
- Sonra migration yapın

### "Permission denied"

- PostgreSQL servisinde "Public Networking" kapalı olmalı
- Sadece Internal URL kullanın

---

## 📊 Veri Kaybı Riski

### ✅ GÜVENLİ YÖNTEM:

1. Önce PostgreSQL servisi oluştur
2. Web servisine DATABASE_URL ekle
3. Deploy yap (boş tablolar oluşur)
4. Migration yap (veriler aktarılır)
5. Test et

### ❌ RİSKLİ YÖNTEM:

- SQLite'ı silmeden önce migration yapın
- Migration'ı test etmeden canlıya geçmeyin

---

## 🎯 Sonuç

PostgreSQL'e geçiş tamamlandıktan sonra:

- ✅ Veriler kalıcı olacak (deploy'da silinmez)
- ✅ Performans artacak
- ✅ Ölçeklenebilirlik artacak

**Başarılar! 🎉**

