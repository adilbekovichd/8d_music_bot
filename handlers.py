"""
Bot handlerlari.

- /start, /help  -> matnli buyruqlar
- audio/voice/audio-document -> 8D formatga o'tkazish
"""
import asyncio
import logging
import os

from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.enums import ChatAction

from config import config
from audio_processor import convert_to_8d, AudioProcessingError
from keyboards import help_keyboard, back_keyboard

logger = logging.getLogger(__name__)
router = Router(name="main-router")


WELCOME_TEXT = (
    "Assalomu alaykum! 👋 Botimizga xush kelibsiz.\n\n"
    "🎧 Bu bot sizga <b>istalgan qo'shiqni 8D formatida</b> chiqarib beradi.\n\n"
    "Shunchaki menga audio fayl, ovozli xabar yoki musiqa yuboring — "
    "men uni bir necha soniyada 8D effektli qilib qaytaraman.\n\n"
    "Quloqchin (naushnik) taqib tinglashni unutmang — effekt shundagina "
    "to'liq his qilinadi! 🎶"
)

HELP_TEXT = (
    "<b>📖 Botdan qanday foydalanish mumkin:</b>\n\n"
    "1️⃣ Istalgan qo'shiqni audio fayl, musiqa yoki ovozli xabar sifatida yuboring\n"
    "2️⃣ Bot avtomatik uni qayta ishlaydi (odatda 5-30 soniya)\n"
    "3️⃣ Tayyor 8D qo'shiqni yuklab oling\n\n"
    f"⚠️ Fayl hajmi <b>{config.max_file_size_mb} MB</b> dan oshmasligi kerak.\n"
    "🎧 Eng yaxshi natija uchun naushnik/quloqchin taqib tinglang."
)


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(WELCOME_TEXT, reply_markup=help_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(HELP_TEXT, reply_markup=back_keyboard())


@router.callback_query(F.data == "how_to_use")
async def cb_how_to_use(callback: CallbackQuery):
    await callback.message.edit_text(HELP_TEXT, reply_markup=back_keyboard())
    await callback.answer()


@router.callback_query(F.data == "back_to_start")
async def cb_back_to_start(callback: CallbackQuery):
    await callback.message.edit_text(WELCOME_TEXT, reply_markup=help_keyboard())
    await callback.answer()


def _detect_format(file_name: str | None, mime_type: str | None) -> str:
    """Fayl kengaytmasi yoki mime-type asosida audio formatni aniqlaydi."""
    if file_name and "." in file_name:
        ext = file_name.rsplit(".", 1)[-1].lower()
        if ext in ("mp3", "ogg", "wav", "m4a", "flac", "opus", "oga"):
            return "ogg" if ext == "oga" else ext
    if mime_type:
        if "mpeg" in mime_type:
            return "mp3"
        if "ogg" in mime_type:
            return "ogg"
        if "wav" in mime_type:
            return "wav"
        if "mp4" in mime_type or "m4a" in mime_type:
            return "m4a"
    return "mp3"  # standart taxmin


@router.message(F.audio | F.voice | (F.document & F.document.mime_type.startswith("audio/")))
async def handle_audio(message: Message, bot: Bot):
    """Foydalanuvchi yuborgan har qanday audio faylni 8D formatga o'tkazadi."""

    # Qaysi turdagi audio ekanini aniqlash (audio / voice / document)
    file_obj = message.audio or message.voice or message.document
    file_size = getattr(file_obj, "file_size", None) or 0

    if file_size and file_size > config.max_file_size_mb * 1024 * 1024:
        await message.reply(
            f"⚠️ Kechirasiz, fayl hajmi juda katta.\n"
            f"Maksimal hajm: <b>{config.max_file_size_mb} MB</b>."
        )
        return

    original_name = getattr(file_obj, "file_name", None)
    mime_type = getattr(file_obj, "mime_type", None)
    input_format = _detect_format(original_name, mime_type)

    processing_msg = await message.reply("🎛 Qo'shiq 8D formatga o'tkazilmoqda, biroz kuting...")
    await bot.send_chat_action(message.chat.id, ChatAction.UPLOAD_VOICE)

    try:
        # Faylni Telegram serveridan yuklab olish
        file_info = await bot.get_file(file_obj.file_id)
        downloaded = await bot.download_file(file_info.file_path)
        input_bytes = downloaded.read()

        # Og'ir CPU ishini alohida threadda bajarish - botni bloklamaslik uchun
        output_buffer = await asyncio.to_thread(
            convert_to_8d,
            input_bytes,
            input_format,
            config.pan_cycle_seconds,
            config.chunk_ms,
        )

        base_name = os.path.splitext(original_name)[0] if original_name else "audio"
        result_filename = f"{base_name}_8D.mp3"

        audio_file = BufferedInputFile(output_buffer.read(), filename=result_filename)

        await message.reply_audio(
            audio=audio_file,
            caption="✅ Tayyor! Bu sizning 8D formatdagi qo'shig'ingiz 🎧\n"
                    "Eng yaxshi tajriba uchun naushnik taqib tinglang.",
            title=f"{base_name} (8D)",
        )

    except Exception as e:
        import traceback

        print("=" * 60)
        traceback.print_exc()
        print("=" * 60)

        await message.reply(str(e))
    except Exception:
        logger.exception("Kutilmagan xatolik yuz berdi")
        await message.reply(
            "❌ Kutilmagan xatolik yuz berdi. Iltimos, boshqa fayl bilan qayta urinib ko'ring."
        )

    finally:
        try:
            await processing_msg.delete()
        except Exception:
            pass


@router.message(F.text | F.photo | F.video | F.sticker | F.animation)
async def handle_other_content(message: Message):
    """Audio bo'lmagan xabarlarga javob."""
    await message.reply(
        "🎧 Menga faqat <b>audio fayl, musiqa yoki ovozli xabar</b> yuboring — "
        "men uni 8D formatga o'tkazib beraman.\n\n"
        "Yordam uchun /help buyrug'ini yuboring."
    )
