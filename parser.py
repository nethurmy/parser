from pyrogram import Client, filters, types

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import os

API_ID = ваш_апи_айди

API_HASH = "ваш_апи_хэш"

BOT_TOKEN = "токен_бота"

app = Client("parser_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("start"))
async def start_command(client, message):
    keyboard = InlineKeyboardMarkup(

        [

            [InlineKeyboar
             [QUOTE]

             [ / QUOTE]
            dButton("Парсить", callback_data="start_parse")],

    ]

    )

    await message.reply_text("Привет. жми кнопку ниже для начала", reply_markup=keyboard)


@app.on_callback_query(filters.regex("start_parse"))
async def start_parse(client, callback_query):
    keyboard = InlineKeyboardMarkup(

        [

            [InlineKeyboardButton("Назад", callback_data="back_to_menu")],

        ]

    )

    await callback_query.message.edit_text("Отправь мне @username чата для парса", reply_markup=keyboard)


@app.on_callback_query(filters.regex("back_to_menu"))
async def back_to_menu(client, callback_query):
    keyboard = InlineKeyboardMarkup(

        [

            [InlineKeyboardButton("Парсить", callback_data="start_parse")],

        ]

    )

    await callback_query.message.edit_text("Привет. жми кнопку ниже для начала", reply_markup=keyboard)


@app.on_message(filters.text & ~filters.command("start"))
async def handle_username(client, message):
    chat_username = message.text.replace("@", "")

    keyboard = InlineKeyboardMarkup(

        [

            [InlineKeyboardButton("Назад", callback_data="back_to_menu")],

        ]

    )

    try:

        await message.reply_text("Начинаю парсинг...", reply_markup=keyboard)

        chat = await client.get_chat(chat_username)

        members = []

        async for member in client.get_chat_members(chat.id):

            if member.user.username and member.user.username != "None":
                members.append(f"@{member.user.username}")

        if not members:
            await message.reply_text("В группе нет юзернеймов.", reply_markup=keyboard)

            return

        with open("users.txt", "w", encoding="utf-8") as file:

            file.write("\n".join(members))

        await client.send_document(message.chat.id, document="users.txt", caption="Список участников")

        os.remove("users.txt")

        keyboard = InlineKeyboardMarkup(

            [

                [InlineKeyboardButton("В меню", callback_data="back_to_menu")],

            ]

        )

        await message.reply_text(f"Собрано {len(members)} участников.", reply_markup=keyboard)



    except Exception as e:

        await message.reply_text(
            f"Произошла ошибка, проверьте корректность @username или убедитесь что бот имеет доступ к чату. Error: {e}",
            reply_markup=keyboard)


app.run()