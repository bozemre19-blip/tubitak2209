# 🚀 TÜBİTAK 2209 Takip Sistemi - Hızlı Kurulum Kılavuzu

## ⚡ Hızlı Başlangıç (Windows)

### Yöntem 1: Otomatik Kurulum (Önerilen)

1. **Python'un yüklü olduğundan emin olun**
   - Komut satırında `python --version` yazın
   - Python 3.8 veya üzeri gereklidir
   - Yoksa [python.org](https://www.python.org/downloads/) adresinden indirin

2. **Sanal ortam oluşturun**
   ```cmd
   python -m venv venv
   ```

3. **Gerekli paketleri yükleyin**
   ```cmd
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Uygulamayı başlatın**
   ```cmd
   python app.py
   ```
   
   **VEYA** daha kolay:
   ```cmd
   start.bat
   ```

5. **Tarayıcınızda açın**
   - Adres: `http://localhost:5000`
   - Kullanıcı adı: `admin`
   - Şifre: `admin123`

## 📱 İlk Kullanım

### Admin (Öğretmen) Olarak

1. **Giriş yapın** (admin/admin123)
2. **Yeni sınıf oluşturun**
   - Sınıflar → Yeni Sınıf Oluştur
   - Sınıf adı: "Python Programlama"
   - Sınıf kodu: "PY2024" (öğrenciler bu kodu kullanacak)
3. **Ödev verin**
   - Sınıf detayına girin
   - Yeni Ödev Ver
   - Başlık, açıklama ve son teslim tarihini girin
4. **Teslimleri takip edin**
   - Ödevler → Teslimleri Gör
   - İndirin, notlandırın, geri bildirim verin

### Öğrenci Olarak

1. **Kayıt olun** (Register sayfasından)
2. **Sınıfa katılın**
   - Sınıflarım → Yeni Sınıfa Katıl
   - Öğretmeninizin verdiği kodu girin (örn: PY2024)
3. **Ödev teslim edin**
   - Sınıfınızı seçin
   - Ödev listesinden ödevi bulun
   - PDF veya DOCX dosyanızı yükleyin
4. **Notunuzu görün**
   - Öğretmen notladıktan sonra burada görünecek

## 🔧 Sorun Giderme

### "Python bulunamadı" Hatası
- Python'u PATH'e ekleyin veya tam yol kullanın:
  ```cmd
  C:\Python39\python.exe app.py
  ```

### Port 5000 Kullanımda
`app.py` dosyasının son satırını değiştirin:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Modül Bulunamadı Hatası
Sanal ortamın aktif olduğundan emin olun:
```cmd
venv\Scripts\activate
pip install -r requirements.txt
```

### Dosya Yükleme Hatası
`static/uploads` klasörünün var olduğundan emin olun.

## 📚 Özellikler

✅ Kullanıcı kayıt ve giriş sistemi  
✅ Rol bazlı erişim (Admin/Öğrenci)  
✅ Sınıf yönetimi  
✅ Ödev verme ve takip  
✅ PDF/DOCX dosya yükleme  
✅ Notlandırma ve geri bildirim  
✅ İstatistikler ve raporlar  
✅ Modern ve responsive tasarım  

## 🎯 Sonraki Adımlar

1. ✅ Uygulamayı başlatın
2. ✅ Admin şifresini değiştirin
3. ✅ İlk sınıfınızı oluşturun
4. ✅ Öğrencileri davet edin
5. ✅ İlk ödevinizi verin

## 💡 İpuçları

- 💾 Düzenli olarak `tubitak2209.db` dosyasını yedekleyin
- 🔐 Üretim ortamında `config.py` içindeki `SECRET_KEY`'i değiştirin
- 📊 Admin panelinden tüm istatistikleri görebilirsiniz
- 🎨 `static/css/style.css` dosyasından görünümü özelleştirebilirsiniz

## 📞 Destek

Sorun yaşarsanız:
1. Bu dosyayı tekrar okuyun
2. `README.md` dosyasına bakın
3. Hata mesajını not edin ve yardım isteyin

---

**İyi çalışmalar! 🎓**

