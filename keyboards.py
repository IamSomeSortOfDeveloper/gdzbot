from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.Database import Database
from config import bot

def admin_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔁 Обновить", callback_data="admin_statistic"))

    return keyboard.as_markup()

def menu_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="💵 Подписка", callback_data="sub_pay"))

    return keyboard.as_markup()

def otmena_pay():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🚫 Отмена", callback_data="menu_start"))

    return keyboard.as_markup()

def keyboard_dialog():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="✏️ Новое задание", callback_data="new_zadanie"))
    keyboard.add(InlineKeyboardButton(text="📘 Объясни решение", callback_data="reshenie_obyasnenie"))
    keyboard.adjust(2)

    return keyboard.as_markup()

def keyboard_obyesnil():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="✏️ Новое задание", callback_data="new_zadanie"))

    return keyboard.as_markup()

def keyboard_subpay():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔐 Оформить подписку", callback_data="sub_pay"))
    keyboard.add(InlineKeyboardButton(text="⏳ Подождать до завтра", callback_data="timetomorrow"))
    keyboard.adjust(1)

    return keyboard.as_markup()

def keyboard_timetomorrow():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="🔐 Оформить подписку сейчас", callback_data="sub_pay"))
    keyboard.add(InlineKeyboardButton(text="✏️ Отправить новое задание", callback_data="new_zadanie"))
    keyboard.adjust(1)

    return keyboard.as_markup()

def keyboard_successpay():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="✏️ Отправить задание", callback_data="new_zadanie"))

    return keyboard.as_markup()

def review_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text="✍️ Оставить отзыв", callback_data="review"))

    return keyboard.as_markup()

def payment_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text = "Оплатить", pay=True)

    return builder.as_markup()