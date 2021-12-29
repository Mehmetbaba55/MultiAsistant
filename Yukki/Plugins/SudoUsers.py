import asyncio
import os
import shutil
import subprocess
from sys import version as pyver

from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from config import OWNER_ID
from Yukki import BOT_ID, MUSIC_BOT_NAME, OWNER_ID, SUDOERS, app
from Yukki.Database import (add_gban_user, add_off, add_on, add_sudo,
                            get_active_chats, get_served_chats, get_sudoers,
                            is_gbanned_user, remove_active_chat,
                            remove_gban_user, remove_served_chat, remove_sudo)

__MODULE__ = "SudoUsers"
__HELP__ = """


/sudolist 
    Bot'un sudo kullanıcı listesini kontrol edin. 


**Not:**
Yalnızca Sudo Kullanıcıları için. 


/addsudo [Kullanıcı adı veya bir kullanıcıyı yanıtla]
- Bot'un Sudo Kullanıcılarına Kullanıcı Eklemek İçin.

/delsudo [Kullanıcı adı veya bir kullanıcıyı yanıtla]
- Bir Kullanıcıyı Bot'un Sudo Kullanıcılarından Kaldırmak İçin.

/restart 
- Botu Yeniden Başlat [Tüm indirmeler, önbellek, ham dosyalar da temizlenecek]. 

/maintenance [enable / disable]
- Etkinleştirildiğinde Bot bakım moduna girer. Artık kimse Müzik çalamaz!

/update 
- Sunucudan Güncellemeleri Al.

/clean
- Temp Dosyalarını ve Günlüklerini Temizleyin.
"""
# Add Sudo Users!


@app.on_message(filters.command("addsudo") & filters.user(OWNER_ID))
async def useradd(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "Bir kullanıcının mesajını yanıtlayın veya username/user_id verin."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in SUDOERS:
            return await message.reply_text(
                f"{user.mention} zaten bir sudo kullanıcısı."
            )
        added = await add_sudo(user.id)
        if added:
            await message.reply_text(
                f"Added **{user.mention}** Sudo Kullanıcılarına."
            )
            os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
        else:
            await message.reply_text("Failed")
        return
    if message.reply_to_message.from_user.id in SUDOERS:
        return await message.reply_text(
            f"{message.reply_to_message.from_user.mention} zaten bir sudo kullanıcısı."
        )
    added = await add_sudo(message.reply_to_message.from_user.id)
    if added:
        await message.reply_text(
            f"Added **{message.reply_to_message.from_user.mention}** Sudo Kullanıcılarına"
        )
        os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
    else:
        await message.reply_text("Failed")
    return


@app.on_message(filters.command("delsudo") & filters.user(OWNER_ID))
async def userdel(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "Bir kullanıcının mesajını yanıtlayın veya username/user_id verin."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id not in SUDOERS:
            return await message.reply_text(f"Bot'un Sudo'sunun bir parçası değil.")
        removed = await remove_sudo(user.id)
        if removed:
            await message.reply_text(
                f"Removed **{user.mention}** from {MUSIC_BOT_NAME}'s Sudo."
            )
            return os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
        await message.reply_text(f"Ters şeyler oldu.")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id not in SUDOERS:
        return await message.reply_text(
            f"bir parçası değil {MUSIC_BOT_NAME}'s sudo."
        )
    removed = await remove_sudo(user_id)
    if removed:
        await message.reply_text(
            f"Kaldırıldı **{mention}** itibaren {MUSIC_BOT_NAME}'s sudo."
        )
        return os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
    await message.reply_text(f"Ters şeyler oldu.")


@app.on_message(filters.command("sudolist"))
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = "⭐️<u> **Owners:**</u>\n"
    sex = 0
    for x in OWNER_ID:
        try:
            user = await app.get_users(x)
            user = user.first_name if not user.mention else user.mention
            sex += 1
        except Exception:
            continue
        text += f"{sex}➤ {user}\n"
    smex = 0
    for count, user_id in enumerate(sudoers, 1):
        if user_id not in OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                if smex == 0:
                    smex += 1
                    text += "\n⭐️<u> **Sudo Kullanıcıları:**</u>\n"
                sex += 1
                text += f"{sex}➤ {user}\n"
            except Exception:
                continue
    if not text:
        await message.reply_text("Sudo Kullanıcısı Yok")
    else:
        await message.reply_text(text)


# Restart Yukki


@app.on_message(filters.command("restart") & filters.user(SUDOERS))
async def theme_func(_, message):
    A = "downloads"
    B = "raw_files"
    C = "cache"
    shutil.rmtree(A)
    shutil.rmtree(B)
    shutil.rmtree(C)
    await asyncio.sleep(2)
    os.mkdir(A)
    os.mkdir(B)
    os.mkdir(C)
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        pass
    for x in served_chats:
        try:
            await app.send_message(
                x,
                f"{MUSIC_BOT_NAME} kendini yeniden başlattı. sorunlar için özür dilerim.\n\n10-15 saniye sonra tekrar oynamaya başlayın.",
            )
            await remove_active_chat(x)
        except Exception:
            pass
    x = await message.reply_text(f"Restarting {MUSIC_BOT_NAME}")
    os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")


## Maintenance Yukki


@app.on_message(filters.command("maintenance") & filters.user(SUDOERS))
async def maintenance(_, message):
    usage = "**Usage:**\n/Yukki [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        user_id = 1
        await add_on(user_id)
        await message.reply_text("Bakım için Etkinleştirildi")
    elif state == "disable":
        user_id = 1
        await add_off(user_id)
        await message.reply_text("Bakım Modu Devre Dışı")
    else:
        await message.reply_text(usage)


## Gban Module


@app.on_message(filters.command("gban") & filters.user(SUDOERS))
async def ban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            await message.reply_text("**Kullanım:**\n/gban [USERNAME | USER_ID]")
            return
        user = message.text.split(None, 2)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id == from_user.id:
            return await message.reply_text(
                "Kendin gban yapmak ister misin? ne kadar aptalca!"
            )
        elif user.id == BOT_ID:
            await message.reply_text("Kendimi engellemeli miyim? ne kadar aptalca!")
        elif user.id in SUDOERS:
            await message.reply_text("Bir sudo kullanıcısını engellemek mi istiyorsunuz? çocuk")
        else:
            await add_gban_user(user.id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**Global Yasak Başlatılıyor {user.mention}**\n\nBeklenen zaman : {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.kick_chat_member(sex, user.id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**Yeni Global Yasak {MUSIC_BOT_NAME}**__

**Menşei:** {message.chat.title} [`{message.chat.id}`]
**Sudo Kullanıcısı:** {from_user.mention}
**Yasaklanan Kullanıcı:** {user.mention}
**Yasaklanmış Kullanıcı Kimliği:** `{user.id}`
**Sohbetler:** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
        return
    from_user_id = message.from_user.id
    from_user_mention = message.from_user.mention
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("Kendini engellemek mi istiyorsun? ne kadar aptal!")
    elif user_id == BOT_ID:
        await message.reply_text("Kendimi engellemeli miyim?!")
    elif user_id in sudoers:
        await message.reply_text("Bir sudo kullanıcısını engellemek mi istiyorsunuz?")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if is_gbanned:
            await message.reply_text("Zaten Gbanned.")
        else:
            await add_gban_user(user_id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**Global Ban başlatılıyor {mention}**\n\nBeklenen zaman : {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.kick_chat_member(sex, user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**Yeni Global Yasak {MUSIC_BOT_NAME}**__

**Menşei:** {message.chat.title} [`{message.chat.id}`]
**Sudo Kullanıcısı:** {from_user_mention}
**Yasaklanan Kullanıcı:** {mention}
**Yasaklanmış Kullanıcı Kimliği:** `{user_id}`
**Sohbetler:** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
            return


@app.on_message(filters.command("ungban") & filters.user(SUDOERS))
async def unban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "**Kullanım:**\n/ungban [USERNAME | USER_ID]"
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        sudoers = await get_sudoers()
        if user.id == from_user.id:
            await message.reply_text("Kendi engelini kaldırmak istiyorsun?")
        elif user.id == BOT_ID:
            await message.reply_text("Kendimi engellemeli miyim?")
        elif user.id in sudoers:
            await message.reply_text("Sudo kullanıcıları engellenemez / engeli kaldırılamaz.")
        else:
            is_gbanned = await is_gbanned_user(user.id)
            if not is_gbanned:
                await message.reply_text("O zaten özgür, neden ona zorbalık ediyorsun??")
            else:
                await remove_gban_user(user.id)
                await message.reply_text(f"Ungbanned!")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("Kendi engelini kaldırmak istiyorsun?")
    elif user_id == BOT_ID:
        await message.reply_text(
            "Kendimi engellemeli miyim? ama bloklu değilim."
        )
    elif user_id in sudoers:
        await message.reply_text("Sudo kullanıcıları engellenemez / engeli kaldırılamaz.")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if not is_gbanned:
            await message.reply_text("O zaten özgür, neden ona zorbalık ediyorsun?")
        else:
            await remove_gban_user(user_id)
            await message.reply_text(f"Ungbanned!")


chat_watcher_group = 5


@app.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message):
    try:
        userid = message.from_user.id
    except Exception:
        return
    checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_gbanned_user(userid):
        try:
            await message.chat.kick_member(userid)
        except Exception:
            return
        await message.reply_text(
            f"{checking} Sudo Kullanıcıları tarafından global ban olarak yasaklandı ve sohbetten atıldı.\n\n**Makul sebep:** Potansiyel Spam Gönderici ve Kötüye Kullanan."
        )


## UPDATE


@app.on_message(filters.command("update") & filters.user(SUDOERS))
async def update(_, message):
    m = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if str(m[0]) != "A":
        x = await message.reply_text("Güncellemeler Bulundu! Şimdi İtiyor.")
        return os.system(f"kill -9 {os.getpid()} && python3 -m Yukki")
    else:
        await message.reply_text("Zaten Güncel")


# Broadcast Message


@app.on_message(filters.command("broadcast_pin") & filters.user(SUDOERS))
async def broadcast_message_pin_silent(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=True)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"**Yayınlanan Mesaj {sent}  ile sohbetler {pin} Pimler.**"
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Kullanım**:\n/broadcast [MESSAGE] veya [Bir Mesajı Yanıtla]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=True)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"**Yayınlanan Mesaj {sent} sohbetler ve {pin} Pimler.**"
    )


@app.on_message(filters.command("broadcast_pin_loud") & filters.user(SUDOERS))
async def broadcast_message_pin_loud(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=False)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"**Yayınlanan Mesaj {sent}  ile sohbetler {pin} Pimler.**"
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Kullanım**:\n/broadcast [MESSAGE] veya [Bir Mesajı Yanıtla]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=False)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"**Yayınlanan Mesaj {sent} sohbetler ve {pin} Pimler.**"
    )


@app.on_message(filters.command("broadcast") & filters.user(SUDOERS))
async def broadcast(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"**Yayınlanan Mesaj {sent} sohbetler.**")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Kullanım**:\n/broadcast [MESSAGE] veya [Bir Mesajı Yanıtla]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"**Yayınlanan Mesaj {sent} sohbetler.**")


# Clean


@app.on_message(filters.command("clean") & filters.user(SUDOERS))
async def clean(_, message):
    dir = "downloads"
    dir1 = "cache"
    shutil.rmtree(dir)
    shutil.rmtree(dir1)
    os.mkdir(dir)
    os.mkdir(dir1)
    await message.reply_text("Hepsi başarıyla temizlendi **temp** dir(s)!")
