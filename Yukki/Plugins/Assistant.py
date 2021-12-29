from inspect import getfullargspec

from pyrogram import filters
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InlineQueryResultArticle,
                            InlineQueryResultPhoto, InputTextMessageContent,
                            Message)

from Yukki import (ASS_CLI_1, ASS_CLI_2, ASS_CLI_3, ASS_CLI_4, ASS_CLI_5,
                   ASSISTANT_PREFIX, BOT_ID, BOT_USERNAME, LOG_GROUP_ID,
                   MUSIC_BOT_NAME, SUDOERS, app)
from Yukki.Database import (approve_pmpermit, disapprove_pmpermit,
                            is_pmpermit_approved)

__MODULE__ = "Assistant"
__HELP__ = f"""

**Not:**
- Yalnızca Sudo Kullanıcıları için



{ASSISTANT_PREFIX[0]}block [ Bir Kullanıcı Mesajını Yanıtlayın] 
- Kullanıcıyı Asistan Hesabından Engeller.

{ASSISTANT_PREFIX[0]}unblock [ Bir Kullanıcı Mesajını Yanıtlayın] 
- Kullanıcının Asistan Hesabındaki Engelini Kaldırır.

{ASSISTANT_PREFIX[0]}approve [ Bir Kullanıcı Mesajını yanıtla] 
- Kullanıcıyı DM için Onaylar.

{ASSISTANT_PREFIX[0]}disapprove [ Bir Kullanıcı Mesajını Yanıtlayın] 
- Kullanıcıyı DM için onaylamaz.

{ASSISTANT_PREFIX[0]}pfp [ Bir Fotoğrafı Yanıtla] 
- CAsistan hesabı PFP'yi kapatıyor.

{ASSISTANT_PREFIX[0]}bio [Bio metin] 
- CAsistan Hesabının Biyografisini asıyor.

"""

flood = {}


@ASS_CLI_1.on_message(
    filters.private
    & filters.incoming
    & ~filters.service
    & ~filters.edited
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.user(SUDOERS)
)
@ASS_CLI_2.on_message(
    filters.private
    & filters.incoming
    & ~filters.service
    & ~filters.edited
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.user(SUDOERS)
)
@ASS_CLI_3.on_message(
    filters.private
    & filters.incoming
    & ~filters.service
    & ~filters.edited
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.user(SUDOERS)
)
@ASS_CLI_4.on_message(
    filters.private
    & filters.incoming
    & ~filters.service
    & ~filters.edited
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.user(SUDOERS)
)
@ASS_CLI_5.on_message(
    filters.private
    & filters.incoming
    & ~filters.service
    & ~filters.edited
    & ~filters.me
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.user(SUDOERS)
)
async def awaiting_message(client, message):
    user_id = message.from_user.id
    if await is_pmpermit_approved(user_id):
        return
    async for m in client.iter_history(user_id, limit=6):
        if m.reply_markup:
            await m.delete()
    if str(user_id) in flood:
        flood[str(user_id)] += 1
    else:
        flood[str(user_id)] = 1
    if flood[str(user_id)] > 5:
        await message.reply_text("Spam Algılandı. Kullanıcı engellendi")
        await client.send_message(
            LOG_GROUP_ID,
            f"**Asistanda İstenmeyen Posta Algılama Engelleme**\n\n- **Engellenen Kullanıcı:** {message.from_user.mention}\n- **Kullanıcı kimliği:** {message.from_user.id}",
        )
        return await client.block_user(user_id)
    await message.reply_text(
        f"Merhaba ben {MUSIC_BOT_NAME}'s asistan.\n\nLütfen burada spam yapmayın, yoksa engellenirsiniz..\nDaha fazla Yardım başlangıcı için :- @{BOT_USERNAME}"
    )


@ASS_CLI_1.on_message(
    filters.command("approve", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_2.on_message(
    filters.command("approve", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_3.on_message(
    filters.command("approve", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_4.on_message(
    filters.command("approve", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_5.on_message(
    filters.command("approve", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def pm_approve(client, message):
    if not message.reply_to_message:
        return await eor(
            message, text="Onaylamak için bir kullanıcının mesajını yanıtlayın."
        )
    user_id = message.reply_to_message.from_user.id
    if await is_pmpermit_approved(user_id):
        return await eor(message, text="Kullanıcı zaten pm için onaylandı")
    await approve_pmpermit(user_id)
    await eor(message, text="Kullanıcı pm için onaylandı")


@ASS_CLI_1.on_message(
    filters.command("disapprove", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_2.on_message(
    filters.command("disapprove", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_3.on_message(
    filters.command("disapprove", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_4.on_message(
    filters.command("disapprove", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_5.on_message(
    filters.command("disapprove", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def pm_disapprove(client, message):
    if not message.reply_to_message:
        return await eor(
            message, text="Onaylamamak için bir kullanıcının mesajını yanıtlayın."
        )
    user_id = message.reply_to_message.from_user.id
    if not await is_pmpermit_approved(user_id):
        await eor(message, text="Kullanıcı zaten pm için onaylanmadı")
        async for m in client.iter_history(user_id, limit=6):
            if m.reply_markup:
                try:
                    await m.delete()
                except Exception:
                    pass
        return
    await disapprove_pmpermit(user_id)
    await eor(message, text="Kullanıcı pm için onaylanmadı")


@ASS_CLI_1.on_message(
    filters.command("block", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_2.on_message(
    filters.command("block", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_3.on_message(
    filters.command("block", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_4.on_message(
    filters.command("block", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_5.on_message(
    filters.command("block", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def block_user_func(client, message):
    if not message.reply_to_message:
        return await eor(message, text="Engellemek için bir kullanıcının mesajını yanıtlayın.")
    user_id = message.reply_to_message.from_user.id
    await eor(message, text="Kullanıcı başarıyla engellendi")
    await client.block_user(user_id)


@ASS_CLI_1.on_message(
    filters.command("unblock", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_2.on_message(
    filters.command("unblock", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_3.on_message(
    filters.command("unblock", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_4.on_message(
    filters.command("unblock", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_5.on_message(
    filters.command("unblock", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def unblock_user_func(client, message):
    if not message.reply_to_message:
        return await eor(
            message, text="Engellemeyi kaldırmak için bir kullanıcının mesajını yanıtlayın."
        )
    user_id = message.reply_to_message.from_user.id
    await client.unblock_user(user_id)
    await eor(message, text="Kullanıcının Engeli Başarıyla Kaldırıldı")


@ASS_CLI_1.on_message(
    filters.command("pfp", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_2.on_message(
    filters.command("pfp", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_3.on_message(
    filters.command("pfp", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_4.on_message(
    filters.command("pfp", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_5.on_message(
    filters.command("pfp", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def set_pfp(client, message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        return await eor(message, text="Bir fotoğrafı yanıtla.")
    photo = await message.reply_to_message.download()
    try:
        await client.set_profile_photo(photo=photo)
        await eor(message, text="PFP Başarıyla Değiştirildi.")
    except Exception as e:
        await eor(message, text=e)


@ASS_CLI_1.on_message(
    filters.command("bio", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_2.on_message(
    filters.command("bio", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_3.on_message(
    filters.command("bio", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_4.on_message(
    filters.command("bio", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
@ASS_CLI_5.on_message(
    filters.command("bio", prefixes=ASSISTANT_PREFIX)
    & filters.user(SUDOERS)
    & ~filters.via_bot
)
async def set_bio(client, message):
    if len(message.command) == 1:
        return await eor(message, text="Bio olarak ayarlamak için biraz metin verin.")
    elif len(message.command) > 1:
        bio = message.text.split(None, 1)[1]
        try:
            await client.update_profile(bio=bio)
            await eor(message, text="Biyografi değişti.")
        except Exception as e:
            await eor(message, text=e)
    else:
        return await eor(message, text="Bio olarak ayarlamak için biraz metin verin.")


async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    spec = getfullargspec(func.__wrapped__).args
    return await func(**{k: v for k, v in kwargs.items() if k in spec})
