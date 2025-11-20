@echo off
echo YouTube Downloader - Arka Plan Servisi Kurulumu
echo ================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo HATA: Python bulunamadi.
    echo Lutfen Python 3.8+ kurun: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python bulundu.

REM Create venv
if not exist "venv" (
    echo Sanal ortam olusturuluyor...
    python -m venv venv
) else (
    echo Sanal ortam zaten mevcut
)

REM Activate venv
echo Sanal ortam aktiflestiriliyor...
call venv\Scripts\activate.bat

REM Install dependencies
echo Bagimliliklari kuruluyor...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

REM Check ffmpeg
where ffmpeg >nul 2>&1
if errorlevel 1 (
    echo UYARI: ffmpeg bulunamadi (istege bagli ama onerilir)
    echo Kurmak icin: https://ffmpeg.org/download.html
) else (
    echo ffmpeg bulundu
)

echo.
echo Kurulum tamamlandi!
echo.
echo Baslatmak icin start.bat dosyasina cift tiklayin
echo.
pause

