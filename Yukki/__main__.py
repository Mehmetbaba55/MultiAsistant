import asyncio
import importlib
import os
import re

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytgcalls import idle
from rich.console import Console
from rich.table import Table
from youtubesearchpython import VideosSearch

from config import LOG_GROUP_ID
from Yukki import (ASS_CLI_1, ASS_CLI_2, ASS_CLI_3, ASS_CLI_4, ASS_CLI_5,
                   ASSID1, ASSID2, ASSID3, ASSID4, ASSID5, ASSNAME1, ASSNAME2,
                   ASSNAME3, ASSNAME4, ASSNAME5, BOT_ID, BOT_NAME, app)
from Yukki.Core.Logger.Log import (startup_delete_last, startup_edit_last,
                                   startup_send_new)
from Yukki.Core.PyTgCalls.Yukki import (pytgcalls1, pytgcalls2, pytgcalls3,
                                        pytgcalls4, pytgcalls5)
from Yukki.Database import get_active_chats, get_sudoers, remove_active_chat
from Yukki.Inline import private_panel
from Yukki.Plugins import ALL_MODULES
from Yukki.Utilities.inline import paginate_modules

loop = asyncio.get_event_loop()
console = Console()
HELPABLE = {}


async def initiate_bot():
    with console.status(
        "[magenta] Best Pro Music Bot'u Başlatma...",
    ) as status:
        console.print("┌ [red]MongoDB önbelleğini temizleme...")
        try:
            chats = await get_active_chats()
            for chat in chats:
                chat_id = int(chat["chat_id"])
                await remove_active_chat(chat_id)
        except Exception as e:
            console.print("[red] Mongodb temizlenirken hata oluştu.")
        console.print("└ [green]MongoDB Başarıyla Temizlendi!\n\n")
        ____ = await startup_send_new("Tüm Eklentileri İçe Aktarma...")
        status.update(
            status="[bold blue]Eklenti Tarama", spinner="earth"
        )
        await asyncio.sleep(1.7)
        console.print("Bulundu {} Eklentiler".format(len(ALL_MODULES)) + "\n")
        status.update(
            status="[bold red]Eklentileri İçe Aktarma...",
            spinner="bouncingBall",
            spinner_style="yellow",
        )
        await asyncio.sleep(1.2)
        for all_module in ALL_MODULES:
            imported_module = importlib.import_module(
                "Yukki.Plugins." + all_module
            )
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
                        imported_module.__MODULE__.lower()
                    ] = imported_module
            console.print(
                f">> [bold cyan]Başarıyla içe aktarıldı: [green]{all_module}.py"
            )
            await asyncio.sleep(0.2)
        console.print("")
        _____ = await startup_edit_last(____, "Finalizing...")
        status.update(
            status="[bold blue]İçe Aktarma Tamamlandı!",
        )
        await asyncio.sleep(2.4)
        await startup_delete_last(_____)
    console.print(
        "[bold green]Tebrikler!! BestMusic Pro Music Bot başarıyla başlatıldı!\n"
    )
    try:
        await app.send_message(
            LOG_GROUP_ID,
            "<b>Tebrikler!! Müzik Botu başarıyla başlatıldı!</b>",
        )
    except Exception as e:
        print(
            "Bot, günlük Kanalına erişemedi. Botunuzu günlük kanalınıza eklediğinizden ve yönetici olarak terfi ettiğinizden emin olun.!"
        )
        console.print(f"\n[red]Stopping Bot")
        return
    a = await app.get_chat_member(LOG_GROUP_ID, BOT_ID)
    if a.status != "administrator":
        print("Bot'u Logger Kanalında Yönetici Olarak Tanıtın")
        console.print(f"\n[red]Stopping Bot")
        return
    try:
        await ASS_CLI_1.send_message(
            LOG_GROUP_ID,
            "<b>Tebrikler!! Asistan İstemci 1 başarıyla başlatıldı!</b>",
        )
    except Exception as e:
        print(
            "Asistan Hesabı 1, günlük Kanalına erişemedi. Asistanınızı günlük kanalınıza eklediğinizden ve yönetici olarak terfi ettirdiğinizden emin olun.!"
        )
        console.print(f"\n[red]Stopping Bot")
        return
    try:
        await ASS_CLI_1.join_chat("OfficialYukki")
    except:
        pass
    try:
        await ASS_CLI_2.send_message(
            LOG_GROUP_ID,
            "<b>Tebrikler!! Asistan İstemci 2 başarıyla başlatıldı!</b>",
        )
    except Exception as e:
        print(
            "Asistan Hesabı 2, günlük Kanalına erişemedi. Asistanınızı günlük kanalınıza eklediğinizden ve yönetici olarak terfi ettirdiğinizden emin olun.!"
        )
        console.print(f"\n[red]Stopping Bot")
        return
    try:
        await ASS_CLI_2.join_chat("OfficialYukki")
    except:
        pass
    try:
        await ASS_CLI_3.send_message(
            LOG_GROUP_ID,
            "<b>Tebrikler!! Asistan İstemci 3 başarıyla başlatıldı!</b>",
        )
    except Exception as e:
        print(
            "Asistan Hesabı 3, günlük Kanalına erişemedi. Asistanınızı günlük kanalınıza eklediğinizden ve yönetici olarak terfi ettirdiğinizden emin olun.!"
        )
        console.print(f"\n[red]Stopping Bot")
        return
    try:
        await ASS_CLI_3.join_chat("OfficialYukki")
    except:
        pass
    try:
        await ASS_CLI_4.send_message(
            LOG_GROUP_ID,
            "<b>Tebrikler!! Asistan İstemci 4 başarıyla başlatıldı!</b>",
        )
    except Exception as e:
        print(
            "Yardımcı Hesap 4, günlük Kanalına erişemedi. Asistanınızı günlük kanalınıza eklediğinizden ve yönetici olarak terfi ettirdiğinizden emin olun.!"
        )
        console.print(f"\n[red]Stopping Bot")
        return
    try:
        await ASS_CLI_4.join_chat("OfficialYukki")
    except:
        pass
    try:
        await ASS_CLI_5.send_message(
            LOG_GROUP_ID,
            "<b>Tebrikler!! Asistan İstemci 5 başarıyla başlatıldı!</b>",
        )
    except Exception as e:
        print(
            "Yardımcı Hesap 5, günlük Kanalına erişemedi. Asistanınızı günlük kanalınıza eklediğinizden ve yönetici olarak terfi ettirdiğinizden emin olun.!"
        )
        console.print(f"\n[red]Stopping Bot")
        return
    try:
        await ASS_CLI_5.join_chat("OfficialYukki")
    except:
        pass
    console.print(f"\n┌[red] Bot Started as {BOT_NAME}!")
    console.print(f"├[green] ID :- {BOT_ID}!")
    console.print(f"├[red] Assistant 1 Started as {ASSNAME1}!")
    console.print(f"├[green] ID :- {ASSID1}!")
    console.print(f"├[red] Assistant 2 Started as {ASSNAME2}!")
    console.print(f"├[green] ID :- {ASSID2}!")
    console.print(f"├[red] Assistant 3 Started as {ASSNAME3}!")
    console.print(f"├[green] ID :- {ASSID3}!")
    console.print(f"├[red] Assistant 4 Started as {ASSNAME4}!")
    console.print(f"├[green] ID :- {ASSID4}!")
    console.print(f"├[red] Assistant 5 Started as {ASSNAME5}!")
    console.print(f"└[green] ID :- {ASSID5}!")
    await pytgcalls1.start()
    await pytgcalls2.start()
    await pytgcalls3.start()
    await pytgcalls4.start()
    await pytgcalls5.start()
    await idle()
    console.print(f"\n[red]Stopping Bot")


home_text_pm = f"""Merhaba ,
Benim ismim {BOT_NAME}.
Bazı kullanışlı özelliklere sahip Telegram Sesli Sohbet Sesiyim.

Tüm komutlar ile kullanılabilir: / """


@app.on_message(filters.command("help") & filters.private)
async def help_command(_, message):
    text, keyboard = await help_parser(message.from_user.mention)
    await app.send_message(message.chat.id, text, reply_markup=keyboard)


@app.on_message(filters.command("start") & filters.private)
async def start_command(_, message):
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name[0] == "s":
            sudoers = await get_sudoers()
            text = "**__Bot Sudo Kullanıcıları Listesi:-__**\n\n"
            j = 0
            for count, user_id in enumerate(sudoers, 1):
                try:
                    user = await app.get_users(user_id)
                    user = (
                        user.first_name if not user.mention else user.mention
                    )
                except Exception:
                    continue
                text += f"➤ {user}\n"
                j += 1
            if j == 0:
                await message.reply_text("Sudo Kullanıcısı Yok")
            else:
                await message.reply_text(text)
        if name == "help":
            text, keyboard = await help_parser(message.from_user.mention)
            await message.delete()
            return await app.send_text(
                message.chat.id,
                text,
                reply_markup=keyboard,
            )
        if name[0] == "i":
            m = await message.reply_text("🔎 Bilgi Alınıyor!")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in results.result()["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
🔍__**Video İzleme Bilgileri**__

❇️**Başlık:** {title}

⏳**Süre:** {duration} Mins
👀**Görüntüleme:** `{views}`
⏰**Yayınlanma Süresi:** {published}
🎥**Kanal ismi:** {channel}
📎**Kanal Bağlantısı:** [Buradan Ziyaret Edin]({channellink})
🔗**Video bağlantısı:** [Link]({link})

⚡️ __Aranıyor Destekleyen {BOT_NAME}t__"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🎥 Youtube Videosunu İzle", url=f"{link}"
                        ),
                        InlineKeyboardButton(
                            text="🔄 Kapat", callback_data="close"
                        ),
                    ],
                ]
            )
            await m.delete()
            return await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode="markdown",
                reply_markup=key,
            )
    out = private_panel()
    return await message.reply_text(
        home_text_pm,
        reply_markup=InlineKeyboardMarkup(out[1]),
    )


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        """Merhaba {first_name},

Daha fazla bilgi için butonlara tıklayın.

Tüm komutlar ile kullanılabilir: /
""".format(
            first_name=name
        ),
        keyboard,
    )


@app.on_callback_query(filters.regex("shikhar"))
async def shikhar(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await CallbackQuery.message.edit(text, reply_markup=keyboard)


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""Merhaba {query.from_user.first_name},

Daha fazla bilgi için butonlara tıklayın.

Tüm komutlar ile kullanılabilir: /
 """
    if mod_match:
        module = mod_match.group(1)
        text = (
            "{} **{}**:\n".format(
                "İşte yardım için", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )
        key = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="↪️ Geri", callback_data="help_back"
                    ),
                    InlineKeyboardButton(
                        text="🔄 Kapat", callback_data="close"
                    ),
                ],
            ]
        )

        await query.message.edit(
            text=text,
            reply_markup=key,
            disable_web_page_preview=True,
        )
    elif home_match:
        out = private_panel()
        await app.send_message(
            query.from_user.id,
            text=home_text_pm,
            reply_markup=InlineKeyboardMarkup(out[1]),
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
    loop.run_until_complete(initiate_bot())
