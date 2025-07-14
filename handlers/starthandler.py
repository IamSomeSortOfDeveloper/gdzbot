from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery, LabeledPrice
from aiogram.fsm.context import FSMContext
from database.Database import Database
from aiogram.filters import Command
from aiogram import Router, F
from config import bot, client, admin_id, promt_ai_text, start_message, time_break_ai, send_reshenie, send_reshenie_sub, popitka_nofree, price_sub, timetomorrow_text, success_pay_text, nosub_photo, success_pay_photo, start_photo, xuyna_text, review_text
import keyboards as keyb
import json
import datetime
import time
import subscribe as sub
import re
from dotenv import load_dotenv, find_dotenv
import os
import base64
import asyncio

router = Router()


class Dialog(StatesGroup):
    dialog_start= State()
    dialog_xuyna = State()
    review_state = State()

@router.message(Command('start'))
async def start(message: Message, database: Database, state: FSMContext):
    await state.clear()
    if message.from_user.id == admin_id:
        await bot.send_message(message.from_user.id, "<b>📊 Статистика</b>\n\n"
                                     "<b>🦶 Поэтапные шаги пользователя</b>\n\n"
                                     f"📍 <b>Старт</b> - <i>{await database.get_count_in_state_user('start')} чел.</i>\n"
                                     f"📍 <b>Диалог с ботом</b> - <i>{await database.get_count_in_state_user('dialog')} чел.</i>\n"
                                     f"📍 <b>Объяснение решения</b> - <i>{await database.get_count_in_state_user('obyasneniye')} чел.</i>\n"
                                     f"📍 <b>Новое задание</b> - <i>{await database.get_count_in_state_user('new_zadanie')} чел.</i>\n"
                                     f"📍 <b>Нет подписки</b> - <i>{await database.get_count_in_state_user('nosub')} чел.</i>\n"
                                     f"📍 <b>Ссылка на оплату</b> - <i>{await database.get_count_in_state_user('sub_pay')} чел.</i>\n\n"
                                     "<b>🎯 Общая статистика</b>\n\n"
                                     f"👤 <b>Всего пользователей</b>: <i>{await database.get_all_user()} чел.</i>\n"
                                     f"💵 <b>Всего подписок</b>: <i>{await database.get_all_subscribe()} шт.</i>\n\n"
                                     f'<i>Актуальные данные на <b>{datetime.datetime.now().strftime("%H:%M %d.%m.%Y")}</b></i>', reply_markup=keyb.admin_keyboard(), parse_mode="HTML")
    else:
        if await database.user_exists(message.from_user.id) == False:
            if message.text[7:] != "":
                await database.add_user(message.from_user.id, message.text[7:], datetime.datetime.now().day)
            else:
                await database.add_user(message.from_user.id, None, datetime.datetime.now().day)

            await database.update_state_user(message.from_user.id, "start")

            await bot.send_photo(message.from_user.id, photo=start_photo, caption=start_message)

            await state.set_state(Dialog.dialog_start)
        else:
            if await database.user_exists_subscribe(message.from_user.id) == True:
                if await database.get_sub_status(message.from_user.id) == False:
                    await database.update_state_user(message.from_user.id, "nosub")
                    await bot.send_photo(message.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")
                else:
                    await database.update_state_user(message.from_user.id, "start")
                    await bot.send_photo(message.from_user.id, photo=start_photo, caption=start_message)
                    await state.set_state(Dialog.dialog_start)
            else:
                zapros_count = await database.get_zapros_count(message.from_user.id)

                if zapros_count != 0:
                    await database.update_state_user(message.from_user.id, "start")
                    await bot.send_photo(message.from_user.id, photo=start_photo, caption=start_message)
                    await state.set_state(Dialog.dialog_start)
                else:
                    await database.update_state_user(message.from_user.id, "nosub")
                    await bot.send_photo(message.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")


# from docx import Document
# def create_docx(text, filename="output.docx"):
#     doc = Document()
#     for line in text.split("\n"):
#         doc.add_paragraph(line.strip())
#     doc.save(filename)

async def gdz_ai_photo(database: Database, user_id, photo, messageid, zapros_count, type_user):
    if await database.get_dialogs(user_id) == None:
        try:
            vision_response = await client.responses.create(
                model="gpt-4.1",
                input=[
                    {"role": "system", "content": promt_ai_text},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text": "Реши задачу из фото."
                            },
                            {
                                "type": "input_image",
                                "image_url": f"data:image/jpeg;base64, {photo}", 
                            },
                        ],
                    }
                ],
            )

            extracted_text = vision_response.output_text
            if type_user == 'sub':
                await bot.edit_message_text(text=send_reshenie_sub(extracted_text), chat_id=user_id, message_id=messageid, reply_markup=keyb.keyboard_dialog(), parse_mode="HTML")
            else:
                await bot.edit_message_text(text=send_reshenie(extracted_text, zapros_count), chat_id=user_id, message_id=messageid, reply_markup=keyb.keyboard_dialog(), parse_mode="HTML")

            dialog_list = []
            new_dialog = {
                "role": "system",
                "content": promt_ai_text
            }

            new_dialog_2 = {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Реши задачу из фото."
                    },
                    {
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64, {photo}", 
                    },
                ],
            }

            for el in vision_response.output:
                new_dialog_3 = {
                    "role": el.role,
                    "content": vision_response.output_text
                }

            dialog_list.append(new_dialog)
            dialog_list.append(new_dialog_2)
            dialog_list.append(new_dialog_3)

            await database.add_dialogs(user_id, json.dumps(dialog_list, indent=4))

        except Exception as e:
            await bot.send_message(user_id, f"Ошибка распознования {e}")

    else:
        dialog_list = json.loads(await database.get_dialogs(user_id))

        bot_promt = {
                "role": "system",
                "content": promt_ai_text
            }
        
        if dialog_list[0] != bot_promt:
            dialog_list[0] = bot_promt

        new_dialog = {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "Реши задачу из фото."
                },
                {
                    "type": "input_image",
                    "image_url":f"data:image/jpeg;base64, {photo}", 
                },
            ],
        }

        dialog_list.append(new_dialog)

        try:
            vision_response = await client.responses.create(
                model="gpt-4.1",
                input=dialog_list
            )

            extracted_text = vision_response.output_text
            if type_user == 'sub':
                await bot.edit_message_text(text=send_reshenie_sub(extracted_text), chat_id=user_id, message_id=messageid, reply_markup=keyb.keyboard_dialog(), parse_mode="HTML")
            else:
                await bot.edit_message_text(text=send_reshenie(extracted_text, zapros_count), chat_id=user_id, message_id=messageid, reply_markup=keyb.keyboard_dialog(), parse_mode="HTML")

            for el in vision_response.output:
                new_dialog_bot = {
                    "role": el.role,
                    "content": vision_response.output_text
                }

            dialog_list.append(new_dialog_bot)
            await database.add_dialogs(user_id, json.dumps(dialog_list, indent=4))

        except Exception as e:
            await bot.send_message(user_id, f"Ошибка распознования {e}")

async def gdz_ai_text(database: Database, user_id, message_text, messageid, zapros_count, type_user):
    if await database.get_dialogs(user_id) == None:

        response = await client.responses.create(
            model="gpt-4.1",
            input = [
                {"role": "system", "content": promt_ai_text},
                {"role": "user", "content": message_text}
            ],
            store=False
        )

        # if "подтверждаю" in (message.text).lower():
        #     create_docx(response.output_text)
        #     await bot.send_document(message.from_user.id, FSInputFile('output.docx'), caption="Ваш документ готов!", reply_markup=keyb.keyboard_dialog())
        # else:
        #     await bot.send_message(message.from_user.id, response.output_text, reply_markup=keyb.keyboard_dialog())

        if type_user == 'sub':
             await bot.edit_message_text(text=send_reshenie_sub(response.output_text), chat_id=user_id, message_id=messageid, reply_markup=keyb.keyboard_dialog(), parse_mode="HTML")
        else:
            await bot.edit_message_text(text=send_reshenie(response.output_text, zapros_count), chat_id=user_id, message_id=messageid, reply_markup=keyb.keyboard_dialog(), parse_mode="HTML")
        # await bot.send_message(message.from_user.id, response.output_text, reply_markup=keyb.keyboard_dialog())

        dialog_list = []
        new_dialog = {
            "role": "system",
            "content": promt_ai_text
        }

        new_dialog_2 = {
            "role": "user",
            "content": message_text
        }

        for el in response.output:
            new_dialog_3 = {
                "role": el.role,
                "content": response.output_text
            }

        dialog_list.append(new_dialog)
        dialog_list.append(new_dialog_2)
        dialog_list.append(new_dialog_3)

        await database.add_dialogs(user_id, json.dumps(dialog_list, indent=4))
    else:
        dialog_list = json.loads(await database.get_dialogs(user_id))
        
        bot_promt = {
                "role": "system",
                "content": promt_ai_text
            }
        
        if dialog_list[0] != bot_promt:
            dialog_list[0] = bot_promt

        new_dialog = {
            "role": "user",
            "content": message_text
        }

        dialog_list.append(new_dialog)

        response = await client.responses.create(
            model="gpt-4.1",
            input = dialog_list,
            store=False
        )

        # if "подтверждаю" in (message.text).lower():
        #     create_docx(response.output_text)
        #     await bot.send_document(message.from_user.id, FSInputFile('output.docx'), caption="Ваш документ готов!", reply_markup=keyb.keyboard_dialog())
        # else:
        #     await bot.send_message(message.from_user.id, response.output_text, reply_markup=keyb.keyboard_dialog())

        if type_user == 'sub':
             await bot.edit_message_text(text=send_reshenie_sub(response.output_text), chat_id=user_id, message_id=messageid, reply_markup=keyb.keyboard_dialog(), parse_mode="HTML")
        else:
            await bot.edit_message_text(text=send_reshenie(response.output_text, zapros_count), chat_id=user_id, message_id=messageid, reply_markup=keyb.keyboard_dialog(), parse_mode="HTML")

        for el in response.output:
            new_dialog_bot = {
                "role": el.role,
                "content": response.output_text
            }

        dialog_list.append(new_dialog_bot)
        await database.add_dialogs(user_id, json.dumps(dialog_list, indent=4))

async def func_obyasneniye_resheniya(database: Database, user_id, messageid):
    dialog_list = json.loads(await database.get_dialogs(user_id))

    new_dialog = {
        "role": "user",
        "content": "Объясни решение подробнее"
    }

    dialog_list.append(new_dialog)

    response = await client.responses.create(
        model="gpt-4.1",
        input = dialog_list,
        store=False
    )

    await bot.edit_message_text(text=f"<b>Подробное объяснение:</b>\n\n<i>{response.output_text}</i>", chat_id=user_id, message_id=messageid, reply_markup=keyb.keyboard_obyesnil(), parse_mode="HTML")

    for el in response.output:
        new_dialog_bot = {
            "role": el.role,
            "content": response.output_text
        }

    dialog_list.append(new_dialog_bot)
    await database.add_dialogs(user_id, json.dumps(dialog_list, indent=4))

@router.message(Dialog.dialog_start)
async def dialog_li_nofree(message: Message, database: Database, state: FSMContext):
    if await database.user_exists_subscribe(message.from_user.id) == True:
        if await database.get_sub_status(message.from_user.id) == False:
            await database.update_state_user(message.from_user.id, "nosub")
            await bot.send_photo(message.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")
            await state.clear()
        else:
            await database.update_state_user(message.from_user.id, "dialog")
            await bot.send_message(message.from_user.id, time_break_ai)

            if message.content_type == "photo":
                file_info = await bot.get_file(message.photo[-1].file_id)
                downloaded = await bot.download_file(file_info.file_path)

                with open('temp.jpg', "wb") as f:
                    f.write(downloaded.getvalue())
                with open('temp.jpg', 'rb') as img:
                    b64_image = base64.b64encode(img.read()).decode('utf-8')

                os.remove('temp.jpg')
                await gdz_ai_photo(database, message.from_user.id, b64_image, message.message_id+1, 0, 'sub')
            else:
                await gdz_ai_text(database, message.from_user.id, message.text, message.message_id+1, 0, 'sub')
            await state.set_state(Dialog.dialog_xuyna)
    else:
        zapros_count = await database.get_zapros_count(message.from_user.id)
        free_day = await database.get_free_day(message.from_user.id)
        if free_day > datetime.datetime.now().day:
            if zapros_count != 0:
                await bot.send_message(message.from_user.id, time_break_ai)
                if message.content_type == "photo":
                    file_info = await bot.get_file(message.photo[-1].file_id)
                    downloaded = await bot.download_file(file_info.file_path)

                    with open('temp.jpg', "wb") as f:
                        f.write(downloaded.getvalue())
                    with open('temp.jpg', 'rb') as img:
                        b64_image = base64.b64encode(img.read()).decode('utf-8')

                    os.remove('temp.jpg')
                    await gdz_ai_photo(database, message.from_user.id, b64_image, message.message_id+1, zapros_count-1, 'user')
                else:
                    await gdz_ai_text(database, message.from_user.id, message.text, message.message_id+1, zapros_count-1, 'user')
                await state.set_state(Dialog.dialog_xuyna)

                await database.update_zapros_count(message.from_user.id, zapros_count-1)
            else:
                await database.update_state_user(message.from_user.id, "nosub")
                await bot.send_photo(message.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")
                await state.clear()

        elif free_day < datetime.datetime.now().day:
            await database.update_free_day(message.from_user.id, datetime.datetime.now().day)
            if zapros_count != 0:
                await bot.send_message(message.from_user.id, time_break_ai)

                if message.content_type == "photo":
                    file_info = await bot.get_file(message.photo[-1].file_id)
                    downloaded = await bot.download_file(file_info.file_path)

                    with open('temp.jpg', "wb") as f:
                        f.write(downloaded.getvalue())
                    with open('temp.jpg', 'rb') as img:
                        b64_image = base64.b64encode(img.read()).decode('utf-8')

                    os.remove('temp.jpg')
                    await gdz_ai_photo(database, message.from_user.id, b64_image, message.message_id+1, zapros_count-1, 'user')
                else:
                    await gdz_ai_text(database, message.from_user.id, message.text, message.message_id+1, zapros_count-1, 'user')
                await state.set_state(Dialog.dialog_xuyna)

                await database.update_zapros_count(message.from_user.id, zapros_count-1)
            else:
                await database.update_state_user(message.from_user.id, "nosub")
                await bot.send_photo(message.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")
                await state.clear()

        elif free_day == datetime.datetime.now().day:
            await database.update_free_day(message.from_user.id, datetime.datetime.now().day+1)
            if zapros_count != 0:
                await bot.send_message(message.from_user.id, time_break_ai)

                if message.content_type == "photo":
                    file_info = await bot.get_file(message.photo[-1].file_id)
                    downloaded = await bot.download_file(file_info.file_path)

                    with open('temp.jpg', "wb") as f:
                        f.write(downloaded.getvalue())
                    with open('temp.jpg', 'rb') as img:
                        b64_image = base64.b64encode(img.read()).decode('utf-8')

                    os.remove('temp.jpg')
                    await gdz_ai_photo(database, message.from_user.id, b64_image, message.message_id+1, zapros_count-1, 'user')
                else:
                    await gdz_ai_text(database, message.from_user.id, message.text, message.message_id+1, zapros_count-1, 'user')
                await state.set_state(Dialog.dialog_xuyna)

                await database.update_zapros_count(message.from_user.id, zapros_count-1)
        
            else:
                await database.update_state_user(message.from_user.id, "nosub")
                await bot.send_photo(message.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")
                await state.clear()

@router.callback_query(F.data == "reshenie_obyasnenie")
async def reshenie_obyasnenie(callback: CallbackQuery, state: FSMContext, database: Database):
    await callback.message.delete_reply_markup()

    if await database.user_exists_subscribe(callback.from_user.id) == True:
        if await database.get_sub_status(callback.from_user.id) == False:
            await database.update_state_user(callback.from_user.id, "nosub")

            await bot.send_photo(callback.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")
            if await database.get_review_user(callback.from_user.id) == 0:
                await asyncio.sleep(120)
                await bot.send_message(callback.from_user.id, review_text, reply_markup=keyb.review_keyboard())
                await database.update_review_user(callback.from_user.id, 1)
            await state.clear()

        else:
            await database.update_state_user(callback.from_user.id, "obyasneniye")
            await bot.send_message(callback.from_user.id, time_break_ai)
            await func_obyasneniye_resheniya(database, callback.from_user.id, callback.message.message_id+1)

    else:
        zapros_count = await database.get_zapros_count(callback.from_user.id)
        free_day = await database.get_free_day(callback.from_user.id)
        if free_day > datetime.datetime.now().day:
            if zapros_count != 0:
                await database.update_state_user(callback.from_user.id, "obyasneniye")
                await bot.send_message(callback.from_user.id, time_break_ai)

                await func_obyasneniye_resheniya(database, callback.from_user.id, callback.message.message_id+1)

                await database.update_zapros_count(callback.from_user.id, zapros_count-1)
            else:
                await database.update_state_user(callback.from_user.id, "nosub")
                await bot.send_photo(callback.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")
                if await database.get_review_user(callback.from_user.id) == 0:
                    await asyncio.sleep(120)
                    await bot.send_message(callback.from_user.id, review_text, reply_markup=keyb.review_keyboard())
                    await database.update_review_user(callback.from_user.id, 1)
                await state.clear()

        elif free_day < datetime.datetime.now().day:
            await database.update_free_day(callback.from_user.id, datetime.datetime.now().day)
            if zapros_count != 0:
                await database.update_state_user(callback.from_user.id, "obyasneniye")
                await bot.send_message(callback.from_user.id, time_break_ai)

                await func_obyasneniye_resheniya(database, callback.from_user.id, callback.message.message_id+1)

                await database.update_zapros_count(callback.from_user.id, zapros_count-1)
            else:
                await database.update_state_user(callback.from_user.id, "nosub")
                await bot.send_photo(callback.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")
                if await database.get_review_user(callback.from_user.id) == 0:
                    await asyncio.sleep(120)
                    await bot.send_message(callback.from_user.id, review_text, reply_markup=keyb.review_keyboard())
                    await database.update_review_user(callback.from_user.id, 1)
                await state.clear()

        elif free_day == datetime.datetime.now().day:
            await database.update_free_day(callback.from_user.id, datetime.datetime.now().day+1)
            if zapros_count != 0:
                await database.update_state_user(callback.from_user.id, "obyasneniye")
                await bot.send_message(callback.from_user.id, time_break_ai)

                await func_obyasneniye_resheniya(database, callback.from_user.id, callback.message.message_id+1)

                await database.update_zapros_count(callback.from_user.id, zapros_count-1)
        
            else:
                await database.update_state_user(callback.from_user.id, "nosub")
                await bot.send_photo(callback.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")
                if await database.get_review_user(callback.from_user.id) == 0:
                    await asyncio.sleep(120)
                    await bot.send_message(callback.from_user.id, review_text, reply_markup=keyb.review_keyboard())
                    await database.update_review_user(callback.from_user.id, 1)

                await state.clear()


    await callback.answer()

@router.message(Dialog.dialog_xuyna)
async def dialog_xuyna(message: Message):
    await bot.send_message(message.from_user.id, xuyna_text, reply_markup=keyb.keyboard_obyesnil())

@router.callback_query(F.data == "review")
async def review(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text="✍️ Напиши все что хотел сказать и отправляй!")
    await state.set_state(Dialog.review_state)
    await callback.answer()

@router.message(Dialog.review_state)
async def review_state(message: Message, state: FSMContext, database: Database):
    await bot.send_message(admin_id, f"✍️ Отзыв от пользователя @{message.from_user.username}\n\n"
                                    f"<i>{message.text}</i>", parse_mode="HTML")

    await bot.send_message(message.from_user.id, "✅ Спасибо! Мы обязательно изучим!")

    if await database.user_exists_subscribe(message.from_user.id) == True:
        if await database.get_sub_status(message.from_user.id) == False:
            await bot.send_photo(message.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")
        else:
            await bot.send_photo(message.from_user.id, photo=start_photo, caption=start_message)
            await state.set_state(Dialog.dialog_start)
    else:
        zapros_count = await database.get_zapros_count(message.from_user.id)

        if zapros_count != 0:
            await bot.send_photo(message.from_user.id, photo=start_photo, caption=start_message)
            await state.set_state(Dialog.dialog_start)
        else:
            await bot.send_photo(message.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")

    await state.clear()

@router.callback_query(F.data == "new_zadanie")
async def new_zadanie(callback: CallbackQuery, state: FSMContext, database: Database):
    if await database.user_exists_subscribe(callback.from_user.id) == True:
        if await database.get_sub_status(callback.from_user.id) == False:
            await database.update_state_user(callback.from_user.id, "nosub")
            await callback.message.delete_reply_markup()
            await bot.send_photo(callback.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")
            if await database.get_review_user(callback.from_user.id) == 0:
                await asyncio.sleep(120)
                await bot.send_message(callback.from_user.id, review_text, reply_markup=keyb.review_keyboard())
                await database.update_review_user(callback.from_user.id, 1)
            await state.clear()
        else:
            await database.update_state_user(callback.from_user.id, "new_zadanie")
            await callback.message.delete_reply_markup()
            await bot.send_message(callback.from_user.id, "Отправь фото или текст задания")
            await state.set_state(Dialog.dialog_start)
    else:
        zapros_count = await database.get_zapros_count(callback.from_user.id)
        free_day = await database.get_free_day(callback.from_user.id)
        if free_day > datetime.datetime.now().day:
            if zapros_count != 0:
                await database.update_state_user(callback.from_user.id, "new_zadanie")
                await callback.message.delete_reply_markup()
                await bot.send_message(callback.from_user.id, "Отправь фото или текст задания")
                await state.set_state(Dialog.dialog_start)
            else:
                await database.update_state_user(callback.from_user.id, "nosub")
                await callback.message.delete_reply_markup()
                await bot.send_photo(callback.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")
                if await database.get_review_user(callback.from_user.id) == 0:
                    await asyncio.sleep(120)
                    await bot.send_message(callback.from_user.id, review_text, reply_markup=keyb.review_keyboard())
                    await database.update_review_user(callback.from_user.id, 1)
                await state.clear()

        elif free_day < datetime.datetime.now().day:
            if zapros_count != 0:
                await database.update_state_user(callback.from_user.id, "new_zadanie")
                await callback.message.delete_reply_markup()
                await bot.send_message(callback.from_user.id, "Отправь фото или текст задания")
                await state.set_state(Dialog.dialog_start)
            else:
                await database.update_state_user(callback.from_user.id, "nosub")
                await callback.message.delete_reply_markup()
                await bot.send_photo(callback.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")
                if await database.get_review_user(callback.from_user.id) == 0:
                    await asyncio.sleep(120)
                    await bot.send_message(callback.from_user.id, review_text, reply_markup=keyb.review_keyboard())
                    await database.update_review_user(callback.from_user.id, 1)
                await state.clear()

        elif free_day == datetime.datetime.now().day:
            if zapros_count != 0:
                await database.update_state_user(callback.from_user.id, "new_zadanie")
                await callback.message.delete_reply_markup()
                await bot.send_message(callback.from_user.id, "Отправь фото или текст задания")
                await state.set_state(Dialog.dialog_start)
            else:
                await database.update_state_user(callback.from_user.id, "nosub")
                await callback.message.delete_reply_markup()
                await bot.send_photo(callback.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")
                if await database.get_review_user(callback.from_user.id) == 0:
                    await asyncio.sleep(120)
                    await bot.send_message(callback.from_user.id, review_text, reply_markup=keyb.review_keyboard())
                    await database.update_review_user(callback.from_user.id, 1)
                await state.clear()

    await callback.answer()

@router.callback_query(F.data == "timetomorrow")
async def timetomorrow(callback: CallbackQuery):
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, timetomorrow_text, reply_markup=keyb.keyboard_timetomorrow())
    await callback.answer()

@router.callback_query(F.data == "sub_pay")
async def sub_pay(callback: CallbackQuery, database: Database, state: FSMContext):
    await database.update_state_user(callback.from_user.id, "sub_pay") 
    await state.clear()

    prices = [LabeledPrice(label="RUB", amount=price_sub)]

    if await database.user_exists_subscribe(callback.from_user.id) == False:
        await callback.message.delete()
        await bot.send_message(callback.from_user.id, "Для отмены платежа - нажми кнопку 👇", reply_markup=keyb.otmena_pay())
        await bot.send_invoice(callback.from_user.id, title="Подписка на 1 месяц",
            description="Оплата подписки на 1 месяц",
            prices = prices,
            provider_token="",
            payload=f"{callback.from_user.id}",
            currency="XTR",
            reply_markup=keyb.payment_keyboard())
    else:
        if await database.get_sub_status(callback.from_user.id) == False:
            await callback.message.delete()
            await bot.send_message(callback.from_user.id, "Для отмены платежа - нажми кнопку 👇", reply_markup=keyb.otmena_pay())
            await bot.send_invoice(callback.from_user.id, title="Подписка на 1 месяц",
                description="Оплата подписки на 1 месяц",
                prices = prices,
                provider_token="",
                payload=f"{callback.from_user.id}",
                currency="XTR",
                reply_markup=keyb.payment_keyboard())

    await callback.answer()

@router.callback_query(F.data == "menu_start")
async def menu_start(callback: CallbackQuery, database: Database, state: FSMContext):
    if await database.user_exists_subscribe(callback.from_user.id) == True:
        if await database.get_sub_status(callback.from_user.id) == False:
            await database.update_state_user(callback.from_user.id, "nosub")
            await callback.message.delete()
            await bot.send_photo(callback.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")
            await state.clear()
        else:
            await database.update_state_user(callback.from_user.id, "dialog")
            await callback.message.edit_text("Отправьте фото или текст задания")
            await state.set_state(Dialog.dialog_start)
    else:
        zapros_count = await database.get_zapros_count(callback.from_user.id)
        free_day = await database.get_free_day(callback.from_user.id)
        if free_day > datetime.datetime.now().day:
            if zapros_count != 0:
                await database.update_state_user(callback.from_user.id, "dialog")
                await callback.message.edit_text("Отправьте фото или текст задания")
                await state.set_state(Dialog.dialog_start)
            else:
                await database.update_state_user(callback.from_user.id, "nosub")
                await callback.message.delete()
                await bot.send_photo(callback.from_user.id, photo=nosub_photo, caption=popitka_nofree, reply_markup=keyb.keyboard_subpay(), parse_mode="HTML")
                await state.clear()


    await callback.answer()

@router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)

@router.message(F.successful_payment)
async def successful_payment(message: Message, database: Database, ):
    await sub.func_pay_sub(database, int(message.successful_payment.invoice_payload), 33)

    await bot.send_photo(message.from_user.id, photo=success_pay_photo, caption=success_pay_text, reply_markup=keyb.keyboard_successpay())

