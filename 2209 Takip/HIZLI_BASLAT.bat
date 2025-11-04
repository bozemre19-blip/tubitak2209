@echo off
chcp 65001 > nul
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║     TÜBİTAK 2209 TAKİP SİSTEMİ - HIZLI BAŞLATMA      ║
echo ╚════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

REM Python kontrolü
echo [1/5] Python kontrol ediliyor...
py --version >nul 2>&1
if errorlevel 1 (
    python --version >nul 2>&1
    if errorlevel 1 (
        echo ❌ HATA: Python bulunamadı!
        echo Lütfen https://www.python.org/downloads/ adresinden Python indirin.
        pause
        exit /b 1
    )
    set PYTHON_CMD=python
) else (
    set PYTHON_CMD=py
)
echo ✅ Python bulundu!
echo.

REM Sanal ortam kontrolü
echo [2/5] Sanal ortam kontrol ediliyor...
if not exist "venv\Scripts\activate.bat" (
    echo ⚙️  Sanal ortam bulunamadı, oluşturuluyor...
    %PYTHON_CMD% -m venv venv
    if errorlevel 1 (
        echo ❌ HATA: Sanal ortam oluşturulamadı!
        pause
        exit /b 1
    )
    echo ✅ Sanal ortam oluşturuldu!
) else (
    echo ✅ Sanal ortam mevcut!
)
echo.

REM Sanal ortamı aktif et
echo [3/5] Sanal ortam aktif ediliyor...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ HATA: Sanal ortam aktif edilemedi!
    pause
    exit /b 1
)
echo ✅ Sanal ortam aktif!
echo.

REM Paketleri kontrol et ve yükle
echo [4/5] Gerekli paketler kontrol ediliyor...
pip show Flask >nul 2>&1
if errorlevel 1 (
    echo ⚙️  Paketler yüklenecek, lütfen bekleyin...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ HATA: Paketler yüklenemedi!
        pause
        exit /b 1
    )
    echo ✅ Paketler yüklendi!
) else (
    echo ✅ Paketler mevcut!
)
echo.

REM Klasörleri kontrol et
if not exist "static\uploads" mkdir "static\uploads"

echo [5/5] Uygulama başlatılıyor...
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                    BAŞARILI! 🎉                        ║
echo ╠════════════════════════════════════════════════════════╣
echo ║                                                        ║
echo ║  🌐 Tarayıcınızda açın:                               ║
echo ║     http://localhost:5000                             ║
echo ║                                                        ║
echo ║  🔑 İlk giriş bilgileri:                              ║
echo ║     Kullanıcı adı: admin                              ║
echo ║     Şifre: admin123                                   ║
echo ║                                                        ║
echo ║  ⛔ Durdurmak için: Ctrl + C                          ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

%PYTHON_CMD% app.py

pause

