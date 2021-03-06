import random
from typing import Dict, List, Union

from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant

from Yukki import MUSIC_BOT_NAME, app
from Yukki.Database import get_assistant, save_assistant
from Yukki.Utilities.assistant import get_assistant_details, random_assistant


def AssistantAdd(mystic):
    async def wrapper(_, message):
        _assistant = await get_assistant(message.chat.id, "assistant")
        if not _assistant:
            ran_ass = random.choice(random_assistant)
            assis = {
                "saveassistant": ran_ass,
            }
            await save_assistant(message.chat.id, "assistant", assis)
        else:
            ran_ass = _assistant["saveassistant"]
        ASS_ID, ASS_NAME, ASS_USERNAME, ASS_ACC = await get_assistant_details(
            ran_ass
        )
        try:
            b = await app.get_chat_member(message.chat.id, ASS_ID)
            if b.status == "kicked":
                return await message.reply_text(
                    f"Asistan Hesabı[{ASS_ID}] yasaklandı.\nMusic Bot'u ilk kullananın yasağını kaldırın\n\nKullanıcı adı: @{ASS_USERNAME}"
                )
        except UserNotParticipant:
            if message.chat.username:
                try:
                    await ASS_ACC.join_chat(message.chat.username)
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    await message.reply_text(
                        f"__Asistan Katılamadı__\n\n**Sebep**: {e}"
                    )
                    return
            else:
                try:
                    invitelink = await app.export_chat_invite_link(
                        message.chat.id
                    )
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace(
                            "https://t.me/+", "https://t.me/joinchat/"
                        )
                    await ASS_ACC.join_chat(invitelink)
                    await message.reply(
                        f"{ASS_NAME} Başarıyla katıldı",
                    )
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    await message.reply_text(
                        f"__Asistan Katılamadı__\n\n**Sebep**: {e}"
                    )
                    return
        return await mystic(_, message)

    return wrapper
