# 🚀 TÜBİTAK 2209 Takip Sistemi - Yayınlama Rehberi

## 📋 İÇİNDEKİLER
1. [Yerel Ağ (LAN) Yayını](#1-yerel-ağ-lan-yayını)
2. [Render.com - Ücretsiz](#2-rendercom---ücretsiz)
3. [PythonAnywhere - Ücretsiz](#3-pythonanywhere---ücretsiz)
4. [Güvenlik Ayarları](#güvenlik-ayarları)

---

## 1️⃣ Yerel Ağ (LAN) Yayını

### Aynı WiFi/Ağdaki Bilgisayarlardan Erişim

#### Adım 1: IP Adresinizi Öğrenin
```powershell
ipconfig
```
IPv4 adresinizi bulun (örn: `192.168.1.100`)

#### Adım 2: Güvenlik Duvarı İzni
```powershell
# PowerShell'i Yönetici Olarak Açın
New-NetFirewallRule -DisplayName "Flask App" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
```

#### Adım 3: Uygulamayı Başlatın
```powershell
python app.py
```

#### Adım 4: Diğer Bilgisayarlardan Erişin
Tarayıcıda: `http://192.168.1.100:5000`

**⚠️ NOT:** Bu yöntem sadece aynı ağdaki cihazlar için çalışır.

---

## 2️⃣ Render.com - Ücretsiz ☁️

### Ücretsiz hosting, 15 dakika sonra uyur ama sürekli erişim için iyi!

#### Adım 1: Hesap Oluşturun
- [render.com](https://render.com) adresine gidin
- GitHub ile giriş yapın (önerilen)

#### Adım 2: Projeyi GitHub'a Yükleyin
```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/KULLANICI_ADINIZ/tubitak2209.git
git push -u origin main
```

#### Adım 3: Render'da Yeni Web Service
1. Dashboard → "New" → "Web Service"
2. GitHub reponuzu seçin
3. Ayarlar:
   - **Name:** tubitak2209
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free

#### Adım 4: Environment Variables Ekleyin
```
SECRET_KEY = rastgele-gizli-anahtar-buraya
```

**✅ Tamamlandı!** URL'niz: `https://tubitak2209.onrender.com`

---

## 3️⃣ PythonAnywhere - Ücretsiz 🐍

### Ücretsiz plan: Her zaman aktif, 100.000 hit/ay

#### Adım 1: Hesap Oluşturun
- [pythonanywhere.com](https://www.pythonanywhere.com) → "Start running Python online"
- Ücretsiz hesap oluşturun

#### Adım 2: Dosyaları Yükleyin
1. Dashboard → "Files"
2. "Upload a file" ile tüm dosyalarınızı yükleyin
   VEYA
3. Bash console açın:
```bash
git clone https://github.com/KULLANICI_ADINIZ/tubitak2209.git
cd tubitak2209
```

#### Adım 3: Virtual Environment
```bash
mkvirtualenv --python=/usr/bin/python3.10 myenv
pip install -r requirements.txt
```

#### Adım 4: Web App Oluşturun
1. Dashboard → "Web"
2. "Add a new web app"
3. "Manual configuration" → Python 3.10
4. WSGI configuration file düzenleyin:

```python
import sys
path = '/home/KULLANICI_ADINIZ/tubitak2209'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

5. Virtual environment yolunu ayarlayın:
   `/home/KULLANICI_ADINIZ/.virtualenvs/myenv`

6. "Reload" butonuna tıklayın

**✅ Tamamlandı!** URL'niz: `https://KULLANICI_ADINIZ.pythonanywhere.com`

---

## 🔒 Güvenlik Ayarları

### Üretim Ortamı İçin MUTLAKA Yapılması Gerekenler:

#### 1. Secret Key Değiştirin
`config.py` dosyasında:
```python
SECRET_KEY = os.environ.get('SECRET_KEY') or 'yeni-cok-gizli-rastgele-anahtar-123456789'
```

Güçlü bir anahtar oluşturun:
```python
import secrets
secrets.token_hex(32)
```

#### 2. Debug Modunu Kapatın
`app.py` dosyasında:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

#### 3. Admin Şifresini Değiştirin
İlk kurulumda `admin/admin123` ile giriş yapın ve şifreyi değiştirin!

#### 4. HTTPS Kullanın
- Render ve PythonAnywhere otomatik HTTPS sağlar ✅
- Kendi sunucunuzda Let's Encrypt kullanın

#### 5. Database Yedekleme
Düzenli olarak `tubitak2209.db` dosyasını yedekleyin:
```powershell
# Her gün otomatik yedek
Copy-Item tubitak2209.db "backup_$(Get-Date -Format 'yyyy-MM-dd').db"
```

---

## 📊 Karşılaştırma

| Özellik | Yerel Ağ | Render.com | PythonAnywhere |
|---------|----------|------------|----------------|
| **Maliyet** | Ücretsiz | Ücretsiz | Ücretsiz |
| **Kurulum** | Kolay | Orta | Orta |
| **Erişim** | Sadece yerel | İnternet | İnternet |
| **Uptime** | Bilgisayar açıkken | 15 dk sonra uyur | 7/24 |
| **Dosya Upload** | 16 MB | Sınırsız | 512 MB |
| **Domain** | IP adresi | .onrender.com | .pythonanywhere.com |

---

## 💡 Öneriler

### Eğer TÜBİTAK 2209 için kullanacaksanız:
1. **PythonAnywhere** - En iyi seçim (ücretsiz, stabil, her zaman açık)
2. **Render** - İkinci seçenek (ücretsiz ama 15 dk sonra uyur)
3. **Yerel Ağ** - Test için veya küçük gruplar için

### Okul/Üniversite için:
- Bilgisayar sınıfında **Yerel Ağ** kullanın
- Online erişim için **PythonAnywhere**

---

## 🆘 Sorun Giderme

### "Module not found" Hatası
```bash
pip install -r requirements.txt
```

### Database Hatası
```bash
python
>>> from app import app, db
>>> with app.app_context():
>>>     db.create_all()
```

### Port 5000 Kullanımda
`app.py` içinde port'u değiştirin:
```python
app.run(debug=False, host='0.0.0.0', port=8080)
```

---

## 📞 Destek

Sorun yaşarsanız:
1. Bu rehberi tekrar okuyun
2. Hata mesajını not edin
3. Logları kontrol edin

**Başarılar! 🎉**

