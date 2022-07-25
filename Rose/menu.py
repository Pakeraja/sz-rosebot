from Rose import bot as app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from Rose.utils.lang import *


fbuttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text="🥀𝙶𝚁𝙾𝙾𝚃 𝙽𝙴𝚃𝚆𝙾𝚁𝙺🥀", url="https://t.me/Groot_Feelings"),
          InlineKeyboardButton(text="🌷𝚂𝚃𝙸𝙲𝙺𝙴𝚁 𝙿𝙰𝙲𝙺𝚂🌷", url="https://t.me/groot_Network")], 
        [ InlineKeyboardButton(text="🌹𝚃𝙴𝙻𝚄𝙶𝚄 𝙶𝚁𝙾𝚄𝙿𝚂🌹", url="https://t.me/telugulittleworld"),
          InlineKeyboardButton(text="🌸𝙵𝚄𝙽𝙽𝚈 𝙶𝙸𝙵𝚂🌸", url="https://t.me/rjbr0")], 
        [InlineKeyboardButton(text="😇 𝙾𝚆𝙽𝙴𝚁 😇", url="https://t.me/MynameisGroot")
        ],[InlineKeyboardButton("« Back", callback_data='startcq')]])

keyboard =InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="🇱🇷 English", callback_data="languages_en")],
     [InlineKeyboardButton(text="🇱🇰 සිංහල", callback_data="languages_si"), 
      InlineKeyboardButton(text="🇮🇳 हिन्दी", callback_data="languages_hi")], 
     [InlineKeyboardButton(text="🇮🇹 Italiano", callback_data="languages_it"), 
      InlineKeyboardButton(text="🇮🇳 తెలుగు", callback_data="languages_ta")], 
     [InlineKeyboardButton(text="🇮🇩 Indonesia", callback_data="languages_id"), 
      InlineKeyboardButton(text="🇦🇪 عربي", callback_data="languages_ar")], 
     [InlineKeyboardButton(text="🇮🇳 മലയാളം", callback_data="languages_ml"), 
      InlineKeyboardButton(text="🇲🇼 Chichewa", callback_data="languages_ny")], 
     [InlineKeyboardButton(text="🇩🇪 German", callback_data="languages_ge"), 
      InlineKeyboardButton(text="🇷🇺 Russian", callback_data="languages_ru")], 
     [InlineKeyboardButton("« Back", callback_data='startcq')]])

@app.on_callback_query(filters.regex("_langs"))
@languageCB
async def commands_callbacc(client, CallbackQuery, _):
    await CallbackQuery.message.edit(
        text= "Choose Your languages:",
        reply_markup=keyboard,
        disable_web_page_preview=True,
    )
    
@app.on_callback_query(filters.regex("_about"))
@languageCB
async def commands_callbacc(client, CallbackQuery, _):
    await CallbackQuery.message.edit(
        text=_["menu"],
        reply_markup=fbuttons,
        disable_web_page_preview=True,
    )

