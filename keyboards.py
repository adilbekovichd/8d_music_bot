"""Bot uchun inline klaviaturalar."""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def help_keyboard() -> InlineKeyboardMarkup:
    """Yordam va qo'llab-quvvatlash tugmalari."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📖 Qanday ishlatiladi?", callback_data="how_to_use")
    )
    return builder.as_markup()


def back_keyboard() -> InlineKeyboardMarkup:
    """Orqaga qaytish tugmasi."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅️ Ortga", callback_data="back_to_start")
    )
    return builder.as_markup()
