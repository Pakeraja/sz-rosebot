import asyncio
import importlib
import re
from contextlib import closing, suppress
from uvloop import install
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Rose.menu import *
from Rose import *
from Rose.plugins import ALL_MODULES
from Rose.utils import paginate_modules
from lang import get_command
from Rose.utils.lang import *
from Rose.utils.commands import *
from Rose.mongo.rulesdb import *
from Rose.utils.start import *
from Rose.utils.kbhelpers import *
from Rose.mongo.usersdb import *
from Rose.mongo.restart import *
from Rose.mongo.chatsdb import *
from Rose.plugins.fsub import ForceSub
import random

loop = asyncio.get_event_loop()
flood = {}
START_COMMAND = get_command("START_COMMAND")
HELP_COMMAND = get_command("HELP_COMMAND")
HELPABLE = {}

async def start_bot():
    global HELPABLE
    for module in ALL_MODULES:
        imported_module = importlib.import_module("Rose.plugins." + module)
        if (
            hasattr(imported_module, "__MODULE__")
            and imported_module.__MODULE__
        ):
            imported_module.__MODULE__ = imported_module.__MODULE__
            if (
                hasattr(imported_module, "__HELP__")
                and imported_module.__HELP__
            ):
                HELPABLE[
                    imported_module.__MODULE__.replace(" ", "_").lower()
                ] = imported_module
    all_module = ""
    j = 1
    for i in ALL_MODULES:
        if j == 1:
            all_module += "•≫ Successfully imported:{:<15}.py\n".format(i)
            j = 0
        else:
            all_module += "•≫ Successfully imported:{:<15}.py".format(i)
        j += 1           
    restart_data = await clean_restart_stage()
    try:
        if restart_data:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**Restarted Successfully**",
            )

        else:
            await app.send_message(LOG_GROUP_ID, "Bot started!")
    except Exception:
        pass
    print(f"{all_module}")
    print("""
 _____________________________________________   
|                                             |  
|          Deployed Successfully              |  
|         (C) 2021-2022 by @szteambots        | 
|          Greetings from supun  :)           |
|_____________________________________________|""")
    await idle()

    await aiohttpsession.close()
    await app.stop()
    for task in asyncio.all_tasks():
        task.cancel() 



home_keyboard_pm = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text=" 🙊𝙰𝙳𝙳 𝙼𝙴 𝚃𝙾 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿🙊 ",
                url=f"http://t.me/{BOT_USERNAME}?startgroup=new",
            )
        ],
        [
           InlineKeyboardButton(
                text=" 🧡𝙻𝙾𝚅𝙴 𝙷𝙴𝙰𝚁𝚃🧡 ", callback_data="_about"
            ),
            InlineKeyboardButton(
                text=" 🇮🇳𝙻𝙰𝙽𝙶𝚄𝙰𝙶𝙴𝚂 ", callback_data="_langs"
            ),
        ],
        [
            InlineKeyboardButton(
                text=" 😊𝙷𝙾𝚆 𝚃𝙾 𝚄𝚂𝙴 𝙼𝙴😊 ", callback_data="bot_commands"
            ),
        ],
        [
            InlineKeyboardButton(
                text="😇𝚂𝚃𝙸𝙲𝙺𝙴𝚁 𝙿𝙰𝙲𝙺𝚂😇",
                url=f"https://t.me/groot_network",
            ),
            InlineKeyboardButton(
                text="🤨𝙵𝚄𝙽𝙽𝚈 𝙶𝙸𝙵𝚂🤨",
                url=f"https://t.me/rjbr0",
            )
        ],
    ]
)

keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="👻𝙲𝙾𝙼𝙼𝙰𝙽𝙳𝚂 & 𝙷𝙴𝙻𝙿",
                url=f"t.me/{BOT_USERNAME}?start=help",
            )
        ]
    ]
)

IMG = ["https://te.legra.ph/file/7bd16e246343db1494892.jpg"]

@app.on_message(filters.command(START_COMMAND))
@language
async def start(client, message: Message, _):
    FSub = await ForceSub(bot, message)
    if FSub == 400:
        return
    chat_id = message.chat.id
    if message.chat.type != "private":
        await message.reply(
            _["main2"], reply_markup=keyboard)
        await adds_served_user(chat_id)     
        return await add_served_chat(chat_id) 
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name.startswith("rules"):
                await get_private_rules(app, message, name)
                return     
        if name.startswith("learn"):
                await get_learn(app, message, name)
                return     
        if "_" in name:
            module = name.split("_", 1)[1]
            text = (_["main6"].format({HELPABLE[module].__MODULE__}
                + HELPABLE[module].__HELP__)
            )
            await message.reply(text, disable_web_page_preview=True)
        if name == "help":
            text, keyb = await help_parser(message.from_user.first_name)
            await message.reply(
                _["main5"],
                reply_markup=keyb,
                disable_web_page_preview=True,
            )
        if name == "connections":
            await message.reply("Run /connections to view or disconnect from groups!")
    else:
        await message.reply(f"""
🐷 𝙷𝚎𝚢 𝚃𝚑𝚎𝚛𝚎 {message.from_user.mention}, 
\n𝙼𝚢 𝙽𝚊𝚖𝚎 𝙸𝚜 𝙱𝙷𝙰𝙽𝚄𝙼𝙰𝚃𝙷𝙸💃 𝙸𝚊𝚖 𝙰𝚍𝚟𝚊𝚗𝚌𝚎𝚍 𝚃𝚎𝚕𝚎𝚐𝚛𝚊𝚖 𝙶𝚛𝚘𝚞𝚙 𝙼𝚊𝚗𝚊𝚐𝚎𝚖𝚎𝚗𝚝 𝙱𝚘𝚝 𝙵𝚘𝚛 𝙷𝚎𝚕𝚙. \n𝚈𝚘𝚞 𝙿𝚛𝚘𝚝𝚎𝚌𝚝 𝚈𝚘𝚞𝚛 𝙶𝚛𝚘𝚞𝚙𝚜 & 𝚂𝚞𝚒𝚝 𝙵𝚘𝚛 𝙰𝚕𝚕 𝚈𝚘𝚞𝚛 𝙽𝚎𝚎𝚍𝚜.\n\n😒 𝚂𝚎𝚗𝚍 𝙼𝚎 /help 𝙵𝚘𝚛 𝙶𝚎𝚝 𝙲𝚘𝚖𝚖𝚊𝚗𝚍𝚜.\n|| 😇 𝙾𝚆𝙽𝙴𝚁 :: @MyNameIsGROOT ||
""",reply_markup=home_keyboard_pm)
        return await add_served_user(chat_id) 


@app.on_message(filters.command(HELP_COMMAND))
@language
async def help_command(client, message: Message, _):
    FSub = await ForceSub(bot, message)
    if FSub == 400:
        return
    if message.chat.type != "private":
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).replace(" ", "_").lower()
            if str(name) in HELPABLE:
                key = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text=_["main3"],
                                url=f"t.me/{BOT_USERNAME}?start=help_{name}",
                            )
                        ],
                    ]
                )
                await message.reply(
                    _["main4"],
                    reply_markup=key,
                )
            else:
                await message.reply(
                    _["main2"], reply_markup=keyboard
                )
        else:
            await message.reply(
                _["main2"], reply_markup=keyboard
            )
    else:
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).replace(" ", "_").lower()
            if str(name) in HELPABLE:
                text = (_["main6"].format({HELPABLE[name].__MODULE__}
                + HELPABLE[name].__HELP__)
                )
                if hasattr(HELPABLE[name], "__helpbtns__"):
                       button = (HELPABLE[name].__helpbtns__) + [[InlineKeyboardButton("« Back", callback_data="bot_commands")]]
                if not hasattr(HELPABLE[name], "__helpbtns__"): button = [[InlineKeyboardButton("« Back", callback_data="bot_commands")]]
                await message.reply(text,
                           reply_markup=InlineKeyboardMarkup(button),
                           disable_web_page_preview=True)
            else:
                text, help_keyboard = await help_parser(
                    message.from_user.first_name
                )
                await message.reply(
                    _["main5"],
                    reply_markup=help_keyboard,
                    disable_web_page_preview=True,
                )
        else:
            text, help_keyboard = await help_parser(
                message.from_user.first_name
            )
            await message.reply(
                text, reply_markup=help_keyboard, disable_web_page_preview=True
            )
    return
  
@app.on_callback_query(filters.regex("startcq"))
@languageCB
async def startcq(client,CallbackQuery, _):
    served_chats = len(await get_served_chats())
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    served_users = len(await get_served_users())
    served_users = []
    users = await get_served_users()
    for user in users:
        served_users.append(int(user["bot_users"]))
    await CallbackQuery.message.edit(
            text=f"""
🐷 𝙷𝚎𝚢 𝚃𝚑𝚎𝚛𝚎 {CallbackQuery.from_user.mention}, 
\n𝙼𝚢 𝙽𝚊𝚖𝚎 𝙸𝚜 𝙱𝙷𝙰𝙽𝚄𝙼𝙰𝚃𝙷𝙸 💃 , 𝙸𝚊𝚖 𝙰𝚍𝚟𝚊𝚗𝚌𝚎𝚍 𝚃𝚎𝚕𝚎𝚐𝚛𝚊𝚖 𝙶𝚛𝚘𝚞𝚙 𝙼𝚊𝚗𝚊𝚐𝚎𝚖𝚎𝚗𝚝 𝙱𝚘𝚝 𝙵𝚘𝚛 𝙷𝚎𝚕𝚙. \n𝚈𝚘𝚞 𝙿𝚛𝚘𝚝𝚎𝚌𝚝 𝚈𝚘𝚞𝚛 𝙶𝚛𝚘𝚞𝚙𝚜 & 𝚂𝚞𝚒𝚝 𝙵𝚘𝚛 𝙰𝚕𝚕 𝚈𝚘𝚞𝚛 𝙽𝚎𝚎𝚍𝚜.\n😒 𝚂𝚎𝚗𝚍 𝙼𝚎 /help 𝙵𝚘𝚛 𝙶𝚎𝚝 𝙲𝚘𝚖𝚖𝚊𝚗𝚍𝚜.
""",disable_web_page_preview=True,reply_markup=home_keyboard_pm)


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
"""**Welcome to help menu**

💃 𝙸𝚊𝚖 𝙰 𝙶𝚛𝚘𝚞𝚙 𝙼𝚊𝚗𝚊𝚐𝚎𝚖𝚎𝚗𝚝 𝙱𝚘𝚝 𝚆𝚒𝚝𝚑 𝚂𝚘𝚖𝚎 𝚄𝚜𝚎𝚏𝚞𝚕 𝙵𝚎𝚊𝚝𝚞𝚛𝚎𝚜.
🙋🏻‍♂️ 𝚈𝚘𝚞 𝙲𝚊𝚗 𝙲𝚑𝚘𝚘𝚜𝚎 𝚊𝚗 𝙾𝚙𝚝𝚒𝚘𝚗 𝙱𝚎𝚕𝚘𝚠, 𝙱𝚢 𝙲𝚕𝚒𝚌𝚔𝚒𝚗𝚐 𝙰 𝙱𝚞𝚝𝚝𝚘𝚗.
😇 𝙸𝚏 𝚈𝚘𝚞 𝙷𝚊𝚟𝚎 𝙰𝚗𝚢 𝙱𝚞𝚐𝚜 𝙰𝚜𝚔 𝙷𝚒𝚖\n😇 𝙾𝚆𝙽𝙴𝚁 :: [𝙸𝙰𝙼 𝙶𝚁𝙾𝙾𝚃 🌱](https://t.me/mynameisgroot)

**All commands can be used with the following: / **""",keyboard,)

@app.on_message(filters.command("ads"))
async def ads_message(_, message):
	await app.forward_messages(
		chat_id = message.chat.id, 
		from_chat_id = int(-1001356358215), 
		message_ids = 2255,
	)

@app.on_callback_query(filters.regex("bot_commands"))
@languageCB
async def commands_callbacc(client,CallbackQuery, _):
    text ,keyboard = await help_parser(CallbackQuery.from_user.mention)
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=_["main5"],
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )
    await CallbackQuery.message.delete()

@app.on_callback_query(filters.regex(r"help_(.*?)"))
@languageCB
async def help_button(client, query, _):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = _["main5"]
    if mod_match:
        module = (mod_match.group(1)).replace(" ", "_")
        text = (
            "{} **{}**:\n".format(
                "Here is the help for", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
            + "\n😇 𝙾𝚆𝙽𝙴𝚁 : [𝙸𝙰𝙼 𝙶𝚁𝙾𝙾𝚃 🌱](https://t.me/mynameisgroot)"
        )
        if hasattr(HELPABLE[module], "__helpbtns__"):
                       button = (HELPABLE[module].__helpbtns__) + [[InlineKeyboardButton("« Back", callback_data="bot_commands")]]
        if not hasattr(HELPABLE[module], "__helpbtns__"): button = [[InlineKeyboardButton("« Back", callback_data="bot_commands")]]
        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(button),
            disable_web_page_preview=True,
        )
        await query.answer(f"Here is the help for {module}")
    elif home_match:
        await app.send_message(
            query.from_user.id,
            text= _["main2"],
            reply_markup=home_keyboard_pm,
        )
        await query.message.delete()
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)

if __name__ == "__main__":
    install()
    with closing(loop):
        with suppress(asyncio.exceptions.CancelledError):
            loop.run_until_complete(start_bot())
        loop.run_until_complete(asyncio.sleep(3.0)) 
