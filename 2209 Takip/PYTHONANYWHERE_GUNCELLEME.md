# 🔄 PythonAnywhere'de Güncelleme Yapma Rehberi

## 3 FARKLI GÜNCELLEME YÖNTEMİ

---

## 1️⃣ GIT İLE GÜNCELLEME (EN KOLAY) ⭐

### İlk Kurulum (Sadece 1 Kere)

#### Adım 1: GitHub'a Proje Yükleyin
```powershell
# Bilgisayarınızda
cd "C:\Users\1433d\OneDrive\Belgeler\2209 Takip"
git init
git add .
git commit -m "Initial commit"
git branch -M main

# GitHub'da yeni repo oluşturun, sonra:
git remote add origin https://github.com/KULLANICI_ADINIZ/tubitak2209.git
git push -u origin main
```

#### Adım 2: PythonAnywhere'de Klonlayın
```bash
# PythonAnywhere Bash Console
cd ~
git clone https://github.com/KULLANICI_ADINIZ/tubitak2209.git
cd tubitak2209
```

### Güncelleme Yaparken (Her Seferinde)

#### Adım 1: Bilgisayarınızda Değişiklikleri Push Edin
```powershell
cd "C:\Users\1433d\OneDrive\Belgeler\2209 Takip"
git add .
git commit -m "Yeni özellik eklendi"
git push
```

#### Adım 2: PythonAnywhere'de Pull Yapın
```bash
# PythonAnywhere Bash Console
cd ~/tubitak2209
git pull origin main
```

#### Adım 3: Web App'i Reload Edin
1. PythonAnywhere Dashboard → "Web" sekmesi
2. Yeşil **"Reload"** butonuna tıklayın
3. ✅ Güncelleme tamamlandı!

**⏱️ Süre:** 1-2 dakika

---

## 2️⃣ MANUEL DOSYA YÜKLEME

### Tek Tek Dosya Değiştirmek İçin

#### Adım 1: Dosyayı Yükleyin
1. PythonAnywhere → "Files" sekmesi
2. `/home/KULLANICI_ADINIZ/tubitak2209/` klasörüne gidin
3. Değişen dosyayı seçin → "Upload a file"

#### Adım 2: Web App'i Reload Edin
1. "Web" sekmesi → **"Reload"** butonuna tıklayın

**⏱️ Süre:** 2-3 dakika
**✅ Avantaj:** GitHub gerekmez
**⚠️ Dezavantaj:** Her dosyayı tek tek yüklemeniz gerek

---

## 3️⃣ ONLINE DÜZENLEME

### Küçük Değişiklikler İçin

#### Adım 1: Dosyayı Açın
1. PythonAnywhere → "Files"
2. Dosyayı bulun ve tıklayın
3. Doğrudan tarayıcıda düzenleyin

#### Adım 2: Kaydet ve Reload
1. "Save" butonuna tıklayın
2. "Web" → **"Reload"**

**⏱️ Süre:** 30 saniye
**✅ Avantaj:** En hızlı
**⚠️ Dezavantaj:** Sadece küçük değişiklikler için uygun

---

## 🎯 HANGİSİNİ KULLANMALIYIM?

| Durum | Yöntem | Neden? |
|-------|--------|--------|
| **İlk kurulum** | Git (1) | En profesyonel |
| **Büyük güncellemeler** | Git (1) | Otomatik, güvenli |
| **Tek dosya değişikliği** | Manuel (2) | Basit, hızlı |
| **Küçük kod düzeltmesi** | Online (3) | En hızlı |
| **Yeni özellik ekleme** | Git (1) | Versiyon kontrolü |

---

## 🗃️ VERİTABANI GÜNCELLEMELERİ

### Yeni Model Eklediyseniz (Örn: Announcement)

#### Yöntem 1: Manuel Database Reset
```bash
# PythonAnywhere Bash Console
cd ~/tubitak2209
rm tubitak2209.db  # Eski database'i sil

python3
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

#### Yöntem 2: Migration (Daha Profesyonel)
```bash
# İlk kurulum
pip install Flask-Migrate

# Her güncelleme
flask db init     # Sadece ilk seferde
flask db migrate -m "Yeni model eklendi"
flask db upgrade
```

**⚠️ UYARI:** Database'i silerseniz tüm veriler gider! Yedek almayı unutmayın.

---

## 💾 YEDEKLİ GÜNCELLEME (ÖNERİLEN)

### Her Güncellemeden Önce Yedek Alın

```bash
# PythonAnywhere Bash Console
cd ~/tubitak2209

# 1. Database yedeği
cp tubitak2209.db tubitak2209_backup_$(date +%Y%m%d).db

# 2. Dosya yedeği (uploads klasörü)
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz static/uploads/

# 3. Güncellemeyi yapın
git pull origin main

# 4. Reload
# Web sekmesinden Reload butonuna tıklayın
```

---

## 🔧 ORNEK GÜNCELLEME SENARYOLARI

### Senaryo 1: Yeni Özellik Ekledim

```bash
# Bilgisayarınızda
git add .
git commit -m "Öğrenci yorumları eklendi"
git push

# PythonAnywhere'de
cd ~/tubitak2209
git pull
# Web → Reload
```

### Senaryo 2: Bug Düzelttim

```bash
# Bilgisayarınızda
git add app.py
git commit -m "Dashboard bug düzeltildi"
git push

# PythonAnywhere'de
cd ~/tubitak2209
git pull
# Web → Reload
```

### Senaryo 3: Yeni Model Ekledim

```bash
# Bilgisayarınızda
git add models.py app.py
git commit -m "Announcement modeli eklendi"
git push

# PythonAnywhere'de
cd ~/tubitak2209
git pull
rm tubitak2209.db  # Dikkat: Veriler silinir!
python3
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
# Web → Reload
```

---

## 🚨 SORUN GİDERME

### "git pull" Çalışmıyor

**Hata:** `error: Your local changes would be overwritten`

**Çözüm:**
```bash
git stash  # Yerel değişiklikleri sakla
git pull
git stash pop  # Geri getir
```

### "Module not found" Hatası

**Çözüm:**
```bash
cd ~/tubitak2209
source ~/.virtualenvs/myenv/bin/activate
pip install -r requirements.txt
```

### Database Hatası

**Çözüm:**
```bash
cd ~/tubitak2209
rm tubitak2209.db
python3
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### Reload Butonu Yok

**Çözüm:**
1. Dashboard → "Web" sekmesi
2. Sayfa en üstünde yeşil buton olmalı
3. Görmüyorsanız sayfayı yenileyin (F5)

---

## 📋 GÜNCELLEME KONTROL LİSTESİ

Her güncelleme öncesi:

- [ ] Yerel bilgisayarda test ettim
- [ ] Database yedeği aldım (gerekirse)
- [ ] `git push` yaptım
- [ ] PythonAnywhere'de `git pull` yaptım
- [ ] Yeni paket eklediyse `pip install -r requirements.txt` çalıştırdım
- [ ] Database değiştiyse yeniden oluşturdum
- [ ] Web App'i Reload ettim
- [ ] Tarayıcıda test ettim

---

## 💡 EN İYİ PRATİKLER

### 1. Sık Sık Push Yapın
```bash
# Her önemli değişiklikten sonra
git add .
git commit -m "Açıklayıcı mesaj"
git push
```

### 2. Anlamlı Commit Mesajları
```bash
✅ git commit -m "Öğrenci dashboard'ına bilgilendirme bölümü eklendi"
❌ git commit -m "değişiklikler"
```

### 3. Test Edip Sonra Push Edin
```powershell
# Önce lokal test et
python app.py
# Tarayıcıda kontrol et
# Sonra push et
git push
```

### 4. Branch Kullanın (İleri Seviye)
```bash
git checkout -b yeni-ozellik
# Değişiklikler yap
git commit -m "Yeni özellik"
git checkout main
git merge yeni-ozellik
git push
```

---

## ⚡ HIZLI GÜNCELLEME ŞABLONU

### Günlük Kullanım İçin

**Bilgisayarınızda:**
```powershell
cd "C:\Users\1433d\OneDrive\Belgeler\2209 Takip"
git add .
git commit -m "Güncelleme: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push
```

**PythonAnywhere'de:**
```bash
cd ~/tubitak2209 && git pull && echo "Reload butonuna tıklayın!"
```

---

## 📊 GÜNCELLEME SIKLIĞI

**Önerilen:**
- 🟢 Günlük: Küçük bug düzeltmeleri
- 🟡 Haftalık: Yeni özellikler
- 🔴 Aylık: Büyük yapısal değişiklikler

---

## 🎓 ÖZETİN ÖZETİ

1. **Git kullanın** - En kolay ve güvenli
2. **Reload butonuna tıklamayı unutmayın** - Yoksa değişiklikler görünmez
3. **Yedek alın** - Özellikle database değişikliklerinde
4. **Test edin** - Önce lokal, sonra production

**Başarılar! 🚀**

