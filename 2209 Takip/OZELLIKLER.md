# 🎓 TÜBİTAK 2209 Takip Sistemi - Özellikler

## 🌟 Genel Bakış

TÜBİTAK 2209-A Öğrenci Takip Sistemi, öğretmenlerin öğrencilerini yönetmesini, ödev vermesini ve takip etmesini kolaylaştıran modern bir web uygulamasıdır.

## 📋 Temel Özellikler

### 🔐 Kullanıcı Yönetimi

#### Kayıt ve Giriş
- ✅ Güvenli kullanıcı kayıt sistemi
- ✅ Şifreli kimlik doğrulama (bcrypt)
- ✅ Oturum yönetimi (Flask-Login)
- ✅ "Beni Hatırla" özelliği

#### Roller
- **👨‍🏫 Öğretmen/Admin**
  - Sınıf oluşturma ve yönetimi
  - Ödev verme ve notlandırma
  - Tüm öğrencileri görüntüleme
  - İstatistik ve raporlara erişim
  
- **👨‍🎓 Öğrenci**
  - Sınıflara katılma
  - Ödev görüntüleme ve teslim etme
  - Notları ve geri bildirimleri görme
  - Kişisel ilerleme takibi

### 📚 Sınıf Yönetimi

#### Öğretmen İşlevleri
- ✅ Sınıf oluşturma (isim, kod, açıklama)
- ✅ Benzersiz sınıf kodları
- ✅ Sınıf durumu yönetimi (aktif/pasif)
- ✅ Kayıtlı öğrencileri görüntüleme
- ✅ Sınıf istatistikleri

#### Öğrenci İşlevleri
- ✅ Sınıf kodunu kullanarak katılma
- ✅ Aktif sınıfları görüntüleme
- ✅ Sınıftan ayrılma
- ✅ Sınıf ödev listesini görme

### 📝 Ödev Yönetimi

#### Ödev Oluşturma
- ✅ Başlık ve detaylı açıklama
- ✅ Son teslim tarihi ve saati
- ✅ Maksimum puan belirleme
- ✅ Sınıfa özel ödevler

#### Ödev Teslimi
- ✅ PDF ve DOCX dosya desteği
- ✅ Dosya boyutu kontrolü (maks 16MB)
- ✅ Güvenli dosya adlandırma
- ✅ Tekrarlı teslim (güncelleme)
- ✅ Son teslim tarihi kontrolü
- ✅ Otomatik geç teslim işaretleme

#### Notlandırma Sistemi
- ✅ Esnek puan sistemi (0-100 veya özel)
- ✅ Detaylı geri bildirim
- ✅ Notlandırma tarihi takibi
- ✅ Öğrenciye özel yorumlar

### 📊 Raporlama ve İstatistikler

#### Admin Dashboard
- 📈 Toplam öğrenci sayısı
- 📈 Aktif sınıf sayısı
- 📈 Verilen ödev sayısı
- 📈 Toplam teslim sayısı
- 📈 Son teslim edilen ödevler listesi

#### Öğrenci Dashboard
- 📌 Kayıtlı sınıflar listesi
- 📌 Yaklaşan ödevler
- 📌 Teslim durumu
- 📌 Alınan notlar

#### Detaylı Raporlar
- 📋 Sınıf bazlı öğrenci listesi
- 📋 Ödev bazlı teslim durumu
- 📋 Teslim etmeyen öğrenciler
- 📋 Geç teslimler

### 📁 Dosya Yönetimi

#### Yükleme Özellikleri
- 📤 Drag & drop desteği (tarayıcıya bağlı)
- 📤 Dosya türü kontrolü (.pdf, .docx)
- 📤 Otomatik dosya adlandırma
- 📤 Güvenli dosya saklama

#### İndirme Özellikleri
- 📥 Öğrenci teslimleri için direkt indirme
- 📥 Orijinal dosya adını koruma
- 📥 Erişim kontrolü (sadece ilgili kişiler)

### 🎨 Kullanıcı Arayüzü

#### Tasarım
- 🎨 Modern ve temiz arayüz (Bootstrap 5)
- 🎨 Responsive tasarım (mobil uyumlu)
- 🎨 Koyu tema desteği (opsiyonel)
- 🎨 İkonlu menüler (Bootstrap Icons)
- 🎨 Hover efektleri ve animasyonlar

#### Kullanıcı Deneyimi
- ⚡ Hızlı yükleme süreleri
- ⚡ Anlaşılır navigasyon
- ⚡ Breadcrumb (içerik haritası)
- ⚡ Flash mesajları (başarı/hata bildirimleri)
- ⚡ Konfirmasyon dialogları

### 🔒 Güvenlik Özellikleri

#### Veri Güvenliği
- 🔐 Şifre hashleme (bcrypt)
- 🔐 SQL Injection koruması (SQLAlchemy ORM)
- 🔐 XSS koruması (Flask template escaping)
- 🔐 CSRF koruması (Flask built-in)

#### Erişim Kontrolü
- 🔒 Login required decorator
- 🔒 Rol bazlı yetkilendirme
- 🔒 Dosya erişim kontrolü
- 🔒 Session timeout (24 saat)

#### Dosya Güvenliği
- 📂 Güvenli dosya adı oluşturma (secure_filename)
- 📂 Dosya uzantısı kontrolü
- 📂 Dosya boyutu limiti
- 📂 Yükleme klasörü izolasyonu

## 🛠️ Teknik Özellikler

### Backend
- **Framework:** Flask 3.0.0
- **Database:** SQLite (geliştirme), PostgreSQL uyumlu
- **ORM:** SQLAlchemy 3.1.1
- **Authentication:** Flask-Login 0.6.3
- **Password Hashing:** Flask-Bcrypt 1.0.1

### Frontend
- **CSS Framework:** Bootstrap 5.3.0
- **Icons:** Bootstrap Icons 1.11.0
- **JavaScript:** Vanilla JS (dependency-free)

### Database Schema

#### User (Kullanıcı)
- id, username, email, password_hash
- full_name, role, created_at
- İlişkiler: enrolled_classes, submissions

#### Class (Sınıf)
- id, name, code, description
- created_by, created_at, is_active
- İlişkiler: students, assignments, creator

#### Assignment (Ödev)
- id, title, description
- class_id, due_date, created_at, max_score
- İlişkiler: class_ref, submissions

#### Submission (Teslim)
- id, assignment_id, student_id
- file_name, file_path, submitted_at
- score, feedback, graded_at
- İlişkiler: assignment, student

### Dosya Yapısı

```
2209 Takip/
├── 📄 app.py              # Ana uygulama (500+ satır)
├── 📄 models.py           # Database modelleri
├── 📄 config.py           # Yapılandırma
├── 📄 requirements.txt    # Python bağımlılıkları
├── 📄 demo_data.py        # Demo veri scripti
├── 📄 start.bat           # Windows başlatma scripti
├── 📖 README.md           # Ana döküman
├── 📖 KURULUM.md          # Kurulum rehberi
├── 📖 OZELLIKLER.md       # Bu dosya
├── 🗄️ tubitak2209.db     # SQLite veritabanı
├── 📁 templates/          # HTML şablonları (10 dosya)
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── admin/
│   └── student/
└── 📁 static/             # Statik dosyalar
    ├── css/style.css      # Özel CSS (300+ satır)
    ├── js/
    └── uploads/           # Yüklenen dosyalar
```

## 📈 Performans

- ⚡ Hafif veritabanı (SQLite)
- ⚡ Minimal JavaScript (no framework overhead)
- ⚡ CDN üzerinden CSS/JS
- ⚡ Optimize edilmiş SQL sorguları
- ⚡ Lazy loading (ilişkiler için)

## 🔮 Gelecek Özellikler (İsteğe Bağlı)

### v2.0 Planları
- [ ] Email bildirimleri
- [ ] Toplu ödev indirme (ZIP)
- [ ] Excel/CSV export
- [ ] Takvim görünümü
- [ ] Öğrenci mesajlaşma
- [ ] Dosya önizleme
- [ ] Video yükleme desteği
- [ ] Quiz/sınav sistemi
- [ ] Devamsızlık takibi
- [ ] Çoklu dil desteği

### v3.0 Planları
- [ ] API endpoint'leri
- [ ] Mobil uygulama
- [ ] Real-time bildirimler (WebSocket)
- [ ] AI destekli geri bildirim
- [ ] Plagiarism detection
- [ ] Video konferans entegrasyonu

## 💪 Avantajlar

1. **Kolay Kurulum** - Tek komutla başlatılabilir
2. **Bağımlılık Yok** - Harici servis gerektirmez
3. **Hafif** - Minimum sistem kaynağı kullanır
4. **Ölçeklenebilir** - PostgreSQL'e kolayca geçiş
5. **Özelleştirilebilir** - Açık kaynak, modüler yapı
6. **Güvenli** - Endüstri standartlarına uygun
7. **Modern** - Güncel teknolojiler kullanır
8. **Türkçe** - Tam Türkçe arayüz ve döküman

## 🎯 Kullanım Senaryoları

### TÜBİTAK 2209 Programı
- ✅ Proje danışmanı ödev takibi
- ✅ Öğrenci ilerleme raporlama
- ✅ Döküman toplama ve değerlendirme

### Üniversite Dersleri
- ✅ Ders ödev yönetimi
- ✅ Proje teslim sistemi
- ✅ Öğrenci değerlendirme

### Eğitim Kurumları
- ✅ Online eğitim desteği
- ✅ Uzaktan ödev takibi
- ✅ Çok sınıf yönetimi

## 📞 Teknik Destek

### Dokümantasyon
- 📖 README.md - Genel bilgiler
- 📖 KURULUM.md - Adım adım kurulum
- 📖 OZELLIKLER.md - Bu dosya

### Topluluk
- 💬 GitHub Issues - Sorun bildirimi
- 📧 Email - Direkt iletişim
- 📚 Wiki - Detaylı rehberler

---

**Versiyon:** 1.0.0  
**Tarih:** Kasım 2024  
**Lisans:** Eğitim Amaçlı  
**Geliştirici:** AI Destekli Geliştirme

