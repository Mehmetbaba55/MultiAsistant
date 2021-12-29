import random

from pyrogram import filters
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InlineQueryResultArticle,
                            InlineQueryResultPhoto, InputTextMessageContent,
                            Message)

from Yukki import SUDOERS, app
from Yukki.Database import get_assistant, save_assistant
from Yukki.Utilities.assistant import get_assistant_details, random_assistant

__MODULE__ = "Multi Assistant"
__HELP__ = """


/checkasistan
- Sohbetinizin tahsis edilen yardımcısını kontrol edin



** Sudo Kullanıcıları için: **

/changeasistan [SIRA NUMARASI]
- Önceki tahsis edilmiş asistanı yenisiyle değiştirin.

/setasistan [SAYISI veya Rastgele]
- Sohbet için bir asistan hesabı ayarlayın. 

"""


ass_num_list = ["1", "2", "3", "4", "5"]


@app.on_message(filters.command("changeasistan") & filters.user(SUDOERS))
async def assis_change(_, message: Message):
    usage = f"**Kullanım:**\n/changeasistan [ASS_NO]\n\nAralarından seçim yapın\n{' | '.join(ass_num_list)}"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    num = message.text.split(None, 1)[1].strip()
    if num not in ass_num_list:
        return await message.reply_text(usage)
    ass_num = int(message.text.strip().split()[1])
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        return await message.reply_text(
            "Önceden Kaydedilmiş Asistan Bulunamadı.\n\nAsistanı Şu Şekilde ayarlayabilirsiniz /setasistan"
        )
    else:
        ass = _assistant["saveassistant"]
    assis = {
        "saveassistant": ass_num,
    }
    await save_assistant(message.chat.id, "assistant", assis)
    await message.reply_text(
        f"**Asistan değişti**\n\nAsistan Hesabı değiştirildi **{ass}** Asistan Numarası **{ass_num}**"
    )


ass_num_list2 = ["1", "2", "3", "4", "5", "Random"]


@app.on_message(filters.command("setasistan") & filters.user(SUDOERS))
async def assis_change(_, message: Message):
    usage = f"**Kullanım:**\n/setasistan [ASS_NO veya Rastgele]\n\nAralarından seçim yapın\n{' | '.join(ass_num_list2)}\n\nRastgele Asistanı ayarlamak için 'random' komutunu kullanın"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    query = message.text.split(None, 1)[1].strip()
    if query not in ass_num_list2:
        return await message.reply_text(usage)
    if str(query) == "Random":
        ran_ass = random.choice(random_assistant)
    else:
        ran_ass = int(message.text.strip().split()[1])
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        await message.reply_text(
            f"**__Best Pro Music Bot Asistanı Atandı__**\n\nAsistan No. **{ran_ass}**"
        )
        assis = {
            "saveassistant": ran_ass,
        }
        await save_assistant(message.chat.id, "assistant", assis)
    else:
        ass = _assistant["saveassistant"]
        return await message.reply_text(
            f"Önceden Kaydedilmiş Asistan Numarası {ass} Bulundu.\n\nAsistan'ı değiştirebilirsiniz /changeasistan"
        )


@app.on_message(filters.command("checkasistan") & filters.group)
async def check_ass(_, message: Message):
    _assistant = await get_assistant(message.chat.id, "assistant")
    if not _assistant:
        return await message.reply_text(
            "Önceden Kaydedilmiş Asistan Bulunamadı.\n\nAsistanın otomatik girmesi için /oynat komutunu kullanabilirsiniz"
        )
    else:
        ass = _assistant["saveassistant"]
        return await message.reply_text(
            f"Önceden Kaydedilmiş Asistan Bulundu\n\nAsistan Numarası {ass} "
        )
