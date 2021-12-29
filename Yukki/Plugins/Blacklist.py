from pyrogram import Client, filters
from pyrogram.types import Message

from Yukki import SUDOERS, app
from Yukki.Database import blacklist_chat, blacklisted_chats, whitelist_chat

__MODULE__ = "Blacklist"
__HELP__ = """


/blacklistedchat 
- Bot'un Kara Listeye Alınmış Sohbetlerini Kontrol Edin.


**Not:**
Yalnızca Sudo Kullanıcıları için.


/blacklistchat [CHAT_ID] 
- Music Bot'u kullanarak herhangi bir sohbeti kara listeye alın


/whitelistchat [CHAT_ID] 
- Music Bot'u kullanarak kara listeye alınmış bir sohbeti beyaz listeye alın

"""


@app.on_message(filters.command("blacklistchat") & filters.user(SUDOERS))
async def blacklist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**Kullanım:**\n/blacklistchat [CHAT_ID]"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id in await blacklisted_chats():
        return await message.reply_text("Sohbet zaten kara listeye alındı.")
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        return await message.reply_text(
            "Sohbet başarıyla kara listeye alındı"
        )
    await message.reply_text("Yanlış bir şey oldu, günlükleri kontrol edin.")


@app.on_message(filters.command("whitelistchat") & filters.user(SUDOERS))
async def whitelist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**Kullanım:**\n/whitelistchat [CHAT_ID]"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats():
        return await message.reply_text("Sohbet zaten beyaz listede.")
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text(
            "Sohbet başarıyla beyaz listeye alındı"
        )
    await message.reply_text("Yanlış bir şey oldu, günlükleri kontrol edin.")


@app.on_message(filters.command("blacklistedchat"))
async def blacklisted_chats_func(_, message: Message):
    text = "**Kara Listeye Alınmış Sohbetler:**\n\n"
    j = 0
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            title = (await app.get_chat(chat_id)).title
        except Exception:
            title = "Private"
        j = 1
        text += f"**{count}. {title}** [`{chat_id}`]\n"
    if j == 0:
        await message.reply_text("Kara Listeye Alınmış Sohbet Yok")
    else:
        await message.reply_text(text)
