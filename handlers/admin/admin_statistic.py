from aiogram.types import CallbackQuery
from database.Database import Database
from aiogram import Router, F
import keyboards as keyb
from datetime import datetime
from config import bot


router = Router()

@router.callback_query(F.data == "admin_statistic")
async def admin_statistic(callback: CallbackQuery, database: Database):
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, "<b>📊 Статистика</b>\n\n"
                                     "<b>💬 Поэтапные шаги пользователя</b>\n\n"
                                     f"📍 <b>Старт</b> - <i>{await database.get_count_in_state_user('start')} чел.</i>\n"
                                     f"📍 <b>Диалог с ботом</b> - <i>{await database.get_count_in_state_user('dialog')} чел.</i>\n"
                                     f"📍 <b>Объяснение решения</b> - <i>{await database.get_count_in_state_user('obyasneniye')} чел.</i>\n"
                                     f"📍 <b>Новое задание</b> - <i>{await database.get_count_in_state_user('new_zadanie')} чел.</i>\n"
                                     f"📍 <b>Нет подписки</b> - <i>{await database.get_count_in_state_user('nosub')} чел.</i>\n"
                                     f"📍 <b>Ссылка на оплату</b> - <i>{await database.get_count_in_state_user('sub_pay')} чел.</i>\n\n"
                                     "<b>🎯 Общая статистика</b>\n\n"
                                     f"👤 <b>Всего пользователей</b>: <i>{await database.get_all_user()} чел.</i>\n"
                                     f"💵 <b>Всего подписок</b>: <i>{await database.get_all_subscribe()} шт.</i>\n\n"
                                     f'<i>Актуальные данные на <b>{datetime.now().strftime("%H:%M %d.%m.%Y")}</b></i>', parse_mode="HTML", reply_markup=keyb.admin_keyboard())
    await callback.answer()