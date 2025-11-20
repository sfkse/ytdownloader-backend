# YouTube İndirici - Arka Plan Servisi

YouTube videolarını indirmek için arka plan servisi.

## 💻 Terminal Nasıl Açılır?

### Windows Kullanıcıları

1. **Windows Tuşu + R** tuşlarına basın
2. Açılan pencerede `cmd` yazın ve **Enter** tuşuna basın
3. Veya **Başlat Menüsü**'nde "Komut İstemi" veya "PowerShell" arayın ve açın

**Kolay Yol:** `install.bat` ve `start.bat` dosyalarına çift tıklayarak da kullanabilirsiniz (terminal açmaya gerek yok).

### Mac Kullanıcıları

1. **Spotlight** açın: **Cmd (⌘) + Boşluk** tuşlarına basın
2. "Terminal" yazın ve **Enter** tuşuna basın
3. Veya **Uygulamalar > Yardımcı Programlar > Terminal** yolunu takip edin

## 🚀 Kurulum ve Çalıştırma

### Windows Kullanıcıları (Kolay Yol)

1. `install.bat` dosyasına çift tıklayın
2. Kurulum tamamlandıktan sonra `start.bat` dosyasına çift tıklayın

### Mac/Linux Kullanıcıları

**1. Kurulum**

Terminal'i açın ve şu komutları çalıştırın:

```bash
chmod +x install.sh
./install.sh
```

**2. Başlatma**

```bash
./start.sh
```

Servis çalışmaya başlayacak. Terminal penceresini açık bırakın.

## 📋 Gereksinimler

- **Python 3.8+** (genellikle zaten yüklüdür)
- **ffmpeg** (isteğe bağlı, en iyi kalite için önerilir)

### ffmpeg Kurulumu

- **macOS**: `brew install ffmpeg`
- **Ubuntu/Debian**: `sudo apt-get install ffmpeg`
- **Windows**: https://ffmpeg.org/download.html adresinden indirin

## ⚠️ Not: Ön Yüz

Bu arka plan servisi, web arayüzü (ön yüz) ile birlikte kullanılmak üzere tasarlanmıştır. Ön yüz ayrı bir repo olarak indirilmelidir.

## 🔧 Sorun Giderme

### Port 8080 kullanımda mı?

**Windows:**
- `.env` dosyasında `PORT=3000` ayarlayın

**Mac/Linux:**
```bash
PORT=3000 ./start.sh
```

### ffmpeg bulunamadı?

ffmpeg olmadan da çalışır ama kalite sınırlı olabilir. Kurmak için yukarıdaki talimatlara bakın.

### Kurulum sorunları?

**Windows:**
- `install.bat` dosyasını tekrar çalıştırın

**Mac/Linux:**
```bash
rm -rf venv
./install.sh
```
