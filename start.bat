@echo off
cd /d "%~dp0"

if not exist "venv" (
    echo HATA: Sanal ortam bulunamadi. Lutfen install.bat dosyasini calistirin
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo YouTube Downloader Arka Plan Servisi baslatiliyor...
echo Servis http://localhost:8080 adresinde calisacak
echo Durdurmak icin Ctrl+C tuslarina basin
echo.

python api.py

