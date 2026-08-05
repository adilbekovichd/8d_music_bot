"""
Bot konfiguratsiyasi.
Tokenni shu yerga yozmang! .env faylidan o'qiladi (xavfsizlik uchun).
"""
import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    bot_token: str = os.getenv("BOT_TOKEN", "")
    admin_id: int = int(os.getenv("ADMIN_ID", "0"))

    # Fayl cheklovlari
    max_file_size_mb: int = 20          # Telegram bot API cheklovi (~20MB yuklab olish uchun)
    allowed_audio_ext: tuple = (".mp3", ".ogg", ".wav", ".m4a", ".flac")

    # 8D effekt sozlamalari
    pan_cycle_seconds: float = 8.0      # bir to'liq aylanish (chapdan o'ngga) necha soniyada
    chunk_ms: int = 25                  # panorama qadam uzunligi (millisekund) - qanchalik kichik, shunchalik silliq


config = Config()

if not config.bot_token:
    raise RuntimeError(
        "BOT_TOKEN topilmadi! Loyiha papkasida .env fayl yarating va "
        "ichiga BOT_TOKEN=... qatorini yozing. (.env.example faylga qarang)"
    )
