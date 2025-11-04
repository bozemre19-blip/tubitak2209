@echo off
chcp 65001 > nul
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║   TÜBİTAK 2209 - YEREL AĞ İÇİN YAYINLAMA            ║
echo ╚════════════════════════════════════════════════════════╝
echo.

cd /d "%~dp0"

echo [1/3] IP Adresinizi Öğreniyorum...
echo.
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    set IP=!IP:~1!
    echo ✅ IP Adresiniz: !IP!
)
echo.

echo [2/3] Güvenlik duvarı iznini kontrol edin...
echo PowerShell'i Yönetici olarak açıp şunu çalıştırın:
echo.
echo New-NetFirewallRule -DisplayName "Flask App" -Direction Inbound -Protocol TCP -LocalPort 5000 -Action Allow
echo.
pause

echo [3/3] Uygulama başlatılıyor...
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║              BAŞARILI! 🎉                             ║
echo ╠════════════════════════════════════════════════════════╣
echo ║                                                        ║
echo ║  🌐 Yerel bilgisayardan:                              ║
echo ║     http://localhost:5000                             ║
echo ║                                                        ║
echo ║  🌐 Aynı ağdaki diğer cihazlardan:                    ║
echo ║     http://!IP!:5000                                  ║
echo ║                                                        ║
echo ║  📱 Mobil cihazlardan da erişebilirsiniz!             ║
echo ║                                                        ║
echo ║  ⛔ Durdurmak için: Ctrl + C                          ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

python app.py

pause

