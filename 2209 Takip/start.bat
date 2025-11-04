@echo off
echo ========================================
echo TUBİTAK 2209 Takip Sistemi Başlatılıyor
echo ========================================
echo.

REM Sanal ortamı kontrol et
if exist "venv\Scripts\activate.bat" (
    echo Sanal ortam bulundu, aktive ediliyor...
    call venv\Scripts\activate.bat
) else (
    echo Uyarı: Sanal ortam bulunamadı!
    echo Önce 'python -m venv venv' komutunu çalıştırın.
    echo.
)

REM Gerekli paketleri kontrol et
echo Paketler kontrol ediliyor...
pip install -q -r requirements.txt

echo.
echo ========================================
echo Uygulama başlatılıyor...
echo ========================================
echo.
echo Tarayıcınızda şu adresi açın:
echo http://localhost:5000
echo.
echo İlk giriş bilgileri:
echo Kullanıcı adı: admin
echo Şifre: admin123
echo.
echo Durdurmak için Ctrl+C tuşlarına basın
echo ========================================
echo.

python app.py

pause

