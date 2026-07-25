import os
from dotenv import load_dotenv
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

load_dotenv()
router = Router()


def _get_user_name(message: Message) -> str:
    if message.from_user is None:
        return "Пользователь"
    if message.from_user.full_name:
        return message.from_user.full_name
    if message.from_user.username:
        return message.from_user.username
    return "Пользователь"


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    master_id = os.getenv("BOT_MASTER_ID", "").strip()

    if master_id:
        try:
            user_id = message.from_user.id if message.from_user else None
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="ПРИНЯТЬ",
                            callback_data=f"join:approve:{user_id}",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="ОТКАЗАТЬ",
                            callback_data=f"join:reject:{user_id}",
                        )
                    ],
                ]
            )
            await message.bot.send_message(
                chat_id=int(master_id),
                text=f"Пользователь {_get_user_name(message)} запросил доступ в канал.",
                reply_markup=keyboard,
            )
        except Exception as exc:
            print(f"EXCEPTION: {exc}")
            await message.answer(
                "Произошла ошибка при отправке уведомления администратору."
            )

    await message.answer(
        "Заявка на вступление в канал принята. Ожидайте подтверждения от администратора."
    )


@router.callback_query(F.data.startswith("join:"))
async def handle_join_decision(callback: CallbackQuery) -> None:
    data = callback.data.split(":")
    if len(data) < 3:
        await callback.answer("Некорректный запрос", show_alert=True)
        return

    action = data[1]
    user_id = data[2]

    try:
        if action == "approve":
            await callback.bot.send_message(chat_id=int(user_id), text="Вы приняты в канал")
        elif action == "reject":
            await callback.bot.send_message(chat_id=int(user_id), text="Вам отказано")
        else:
            await callback.answer("Некорректное действие", show_alert=True)
            return
    except Exception as exc:
        print(f"EXCEPTION: {exc}")
        await callback.answer("Не удалось отправить сообщение пользователю", show_alert=True)
        return

    await callback.answer()
