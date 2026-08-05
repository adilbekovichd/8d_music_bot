# 🎧 8D Audio Bot

Telegram bot — istalgan qo'shiqni **8D audio formatga** o'tkazib beradi.
**aiogram 3.30.0** (eng so'nggi versiya) asosida yozilgan.

## 📁 Loyiha tuzilishi

```
8d_audio_bot/
├── main.py              # Botni ishga tushirish nuqtasi
├── handlers.py           # /start, /help va audio handlerlar
├── audio_processor.py    # 8D effekt algoritmi (pydub asosida)
├── keyboards.py          # Inline tugmalar
├── config.py              # Sozlamalar (.env dan o'qiydi)
├── requirements.txt       # Kerakli kutubxonalar
└── .env.example           # Token namunasi
```

## ⚙️ O'rnatish

### 1. FFmpeg o'rnating (audio qayta ishlash uchun MAJBURIY)

**Windows:**
1. https://www.gyan.dev/ffmpeg/builds/ dan yuklab oling (`ffmpeg-release-essentials.zip`)
2. Arxivni `C:\ffmpeg` ga chiqaring
3. `C:\ffmpeg\bin` ni Windows PATH ga qo'shing (Environment Variables)
4. Yangi terminal oching va tekshiring: `ffmpeg -version`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update && sudo apt install ffmpeg -y
```

**macOS:**
```bash
brew install ffmpeg
```

### 2. Virtual muhit yarating va faollashtiring

```powershell
python -m venv .venv
.venv\Scripts\activate      # Windows
# yoki
source .venv/bin/activate   # Linux/macOS
```

### 3. Kutubxonalarni o'rnating

```bash
pip install -r requirements.txt
```

### 4. Botni sozlang

1. Telegram'da [@BotFather](https://t.me/BotFather) ga o'ting
2. `/newbot` buyrug'i bilan yangi bot yarating va **tokenni** oling
3. `.env.example` faylini nusxalab, nomini `.env` ga o'zgartiring
4. `.env` faylni oching va tokeningizni kiriting:
   ```
   BOT_TOKEN=123456789:AAxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

### 5. Botni ishga tushiring

```bash
python main.py
```

Konsolda `Bot ishga tushmoqda...` yozuvini ko'rsangiz — bot ishlamoqda! ✅

## 🎯 Bot qanday ishlaydi

1. Foydalanuvchi `/start` bosadi → xush kelibsiz xabari chiqadi
2. Foydalanuvchi istalgan qo'shiqni (audio fayl, musiqa yoki ovozli xabar) yuboradi
3. Bot faylni yuklab oladi, 8D panorama effektini qo'llaydi (stereo tovushni
   sinusoidal ravishda chapdan-o'ngga aylantiradi)
4. Tayyor MP3 fayl foydalanuvchiga qaytariladi

## 🔧 8D effektni sozlash

`config.py` faylida quyidagi parametrlarni o'zgartirishingiz mumkin:

| Parametr | Ma'nosi | Standart qiymat |
|---|---|---|
| `pan_cycle_seconds` | Bir to'liq aylanish davomiyligi | 8.0 soniya |
| `chunk_ms` | Panorama silliqligi (kichik = silliqroq, lekin sekinroq) | 25 ms |
| `max_file_size_mb` | Maksimal fayl hajmi | 20 MB |

## ⚠️ Muhim eslatmalar

- **FFmpeg o'rnatilmagan bo'lsa**, bot audio fayllarni qayta ishlay olmaydi —
  albatta yuqoridagi 1-qadamni bajaring.
- Telegram Bot API orqali yuklab olinadigan fayllar odatda **20 MB** bilan
  cheklangan (agar kattaroq fayllar kerak bo'lsa, Local Bot API Server
  ishlatish kerak bo'ladi).
- Katta fayllarni qayta ishlash bir necha o'nlab soniya vaqt olishi mumkin —
  bu normal holat.

## 🚀 Kengaytirish g'oyalari

- SQLite/PostgreSQL orqali foydalanuvchilar statistikasini saqlash
- Boshqa audio effektlar qo'shish (bass boost, reverb, slowed+reverb va h.k.)
- Inline mode qo'llab-quvvatlash
- Admin panel (statistika, xabar yuborish)
