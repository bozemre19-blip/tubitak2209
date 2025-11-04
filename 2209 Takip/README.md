# TÜBİTAK 2209 Öğrenci Takip Sistemi

Modern ve kullanıcı dostu bir öğrenme yönetim sistemi (LMS). TÜBİTAK 2209-A programındaki öğrencilerin ödev takibi için geliştirilmiştir.

## ✨ Özellikler

### 👨‍🏫 Öğretmen/Admin Paneli
- ✅ Sınıf oluşturma ve yönetimi
- ✅ Ödev verme ve takip etme
- ✅ Öğrenci ödevlerini indirme ve notlandırma
- ✅ Geri bildirim verme
- ✅ Detaylı raporlama ve istatistikler

### 👨‍🎓 Öğrenci Paneli
- ✅ Sınıflara katılma (sınıf kodu ile)
- ✅ Ödevleri görüntüleme
- ✅ PDF ve DOCX formatında ödev yükleme
- ✅ Notları ve geri bildirimleri görme
- ✅ Yaklaşan ödevleri takip etme

### 🔐 Güvenlik
- ✅ Şifreli kullanıcı hesapları
- ✅ Güvenli dosya yükleme
- ✅ Rol tabanlı erişim kontrolü
- ✅ Oturum yönetimi

## 📋 Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

## 🚀 Kurulum

### 1. Projeyi İndirin

```bash
git clone <repo-url>
cd "2209 Takip"
```

### 2. Sanal Ortam Oluşturun (Önerilen)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Gerekli Paketleri Yükleyin

```bash
pip install -r requirements.txt
```

### 4. Uygulamayı Başlatın

```bash
python app.py
```

Uygulama başlatıldığında otomatik olarak:
- Veritabanı oluşturulur (`tubitak2209.db`)
- Upload klasörü oluşturulur
- İlk admin kullanıcısı oluşturulur

## 🔑 İlk Giriş

### Admin/Öğretmen Hesabı
- **Kullanıcı Adı:** `admin`
- **Şifre:** `admin123`

⚠️ **Önemli:** İlk girişten sonra admin şifresini mutlaka değiştirin!

### Öğrenci Hesabı
Öğrenciler kendi hesaplarını "Kayıt Ol" sayfasından oluşturabilirler.

## 📖 Kullanım

### Öğretmen İçin

1. **Sınıf Oluşturma**
   - Admin panelinden "Sınıflar" > "Yeni Sınıf Oluştur"
   - Sınıf adı ve benzersiz bir kod belirleyin
   - Öğrenciler bu kodu kullanarak sınıfa katılacak

2. **Ödev Verme**
   - Sınıf detay sayfasından "Yeni Ödev Ver"
   - Ödev başlığı, açıklama ve son teslim tarihini girin
   - Maksimum puanı belirleyin

3. **Notlandırma**
   - Ödev teslimleri sayfasından öğrenci ödevlerini indirin
   - Her ödev için not ve geri bildirim verin

### Öğrenci İçin

1. **Sınıfa Katılma**
   - "Sınıflarım" > "Yeni Sınıfa Katıl"
   - Öğretmeninizin verdiği sınıf kodunu kullanın

2. **Ödev Teslimi**
   - Sınıfınızı seçin ve ödevleri görüntüleyin
   - Dosya seçin (PDF veya DOCX)
   - "Teslim Et" butonuna tıklayın

3. **Notları Görme**
   - Ödevler sayfasından notlandırılmış ödevlerinizi görün
   - Öğretmeninizin geri bildirimlerini okuyun

## 📁 Proje Yapısı

```
2209 Takip/
├── app.py                 # Ana Flask uygulaması
├── models.py              # Veritabanı modelleri
├── config.py              # Yapılandırma ayarları
├── requirements.txt       # Python paketleri
├── README.md             # Bu dosya
├── tubitak2209.db        # SQLite veritabanı (otomatik oluşturulur)
├── templates/            # HTML şablonları
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── admin/           # Admin sayfaları
│   │   ├── dashboard.html
│   │   ├── classes.html
│   │   ├── class_detail.html
│   │   └── assignment_submissions.html
│   └── student/         # Öğrenci sayfaları
│       ├── dashboard.html
│       ├── classes.html
│       └── assignments.html
└── static/              # Statik dosyalar
    ├── css/
    │   └── style.css
    ├── js/
    └── uploads/         # Yüklenen ödev dosyaları
```

## 🛠️ Teknolojiler

- **Backend:** Python Flask
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Icons:** Bootstrap Icons
- **Authentication:** Flask-Login
- **Password Security:** Flask-Bcrypt

## 📝 Özelleştirme

### Maksimum Dosya Boyutu
`config.py` dosyasında değiştirilebilir (varsayılan: 16MB):

```python
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
```

### Desteklenen Dosya Formatları
`config.py` dosyasında:

```python
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
```

### Secret Key
Üretim ortamında mutlaka değiştirin:

```python
SECRET_KEY = 'kendi-gizli-anahtariniz'
```

## 🔒 Güvenlik Notları

1. Üretim ortamında `SECRET_KEY` değişkenini güçlü bir değer ile değiştirin
2. `DEBUG` modunu kapatın (`app.run(debug=False)`)
3. Düzenli olarak yedek alın
4. HTTPS kullanın (üretim ortamında)
5. Admin şifresini değiştirin

## 🐛 Sorun Giderme

### Port Hatası
Eğer 5000 portu kullanımdaysa, `app.py` dosyasının sonunda portu değiştirin:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Dosya Yükleme Hatası
`static/uploads` klasörünün yazma izinlerini kontrol edin.

### Veritabanı Hatası
`tubitak2209.db` dosyasını silin ve uygulamayı yeniden başlatın.

## 📞 Destek

Sorularınız için:
- 🐛 Issue açın
- 📧 E-posta gönderin
- 📖 Dokümantasyonu okuyun

## 📄 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## 🎉 Katkıda Bulunma

Katkılarınızı bekliyoruz! Pull request göndermekten çekinmeyin.

---

**TÜBİTAK 2209-A Öğrenci Takip Sistemi** - Öğrenci başarısını desteklemek için geliştirilmiştir. 🎓

