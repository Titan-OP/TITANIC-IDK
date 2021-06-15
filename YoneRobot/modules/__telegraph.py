from YoneRobot.events import register
from YoneRobot import telethn as tbot
TMP_DOWNLOAD_DIRECTORY = "./"
from telethon import events
import os
from PIL import Image
from datetime import datetime
from telegraph import Telegraph, upload_file, exceptions
kittu = "YONE"
telegraph = Telegraph()
r = telegraph.create_account(short_name=kittu)
auth_url = r["auth_url"]


@register(pattern="^/t(gm|m) ?(.*)")
async def _(event):
    if event.fwd_from:
        return
    optional_title = event.pattern_match.group(2)
    if event.reply_to_msg_id:
        start = datetime.now()
        r_message = await event.get_reply_message()
        input_str = event.pattern_match.group(1)
        if input_str == "m":
            downloaded_file_name = await tbot.download_media(
                r_message,
                TMP_DOWNLOAD_DIRECTORY
            )
            end = datetime.now()
            ms = (end - start).seconds
            h = await event.reply("∂σωηℓσα∂є∂ тσ {} ιη {} ѕєcση∂ѕ.".format(downloaded_file_name, ms))
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await h.edit("ERROR: " + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                await h.edit("**Uρℓσα∂є∂ тσ [тєℓєgяαρн](https://telegra.ph{})**.\n\n**ву 𝐓𝐈𝐓𝐀𝐍 𝟐.𝟎**".format(media_urls[0]), link_preview=True)
        elif input_str == "t":
            user_object = await tbot.get_entity(r_message.sender_id)
            title_of_page = user_object.first_name # + " " + user_object.last_name
            # apparently, all Users do not have last_name field
            if optional_title:
                title_of_page = optional_title
            page_content = r_message.message
            if r_message.media:
                if page_content != "":
                    title_of_page = page_content
                downloaded_file_name = await tbot.download_media(
                    r_message,
                    TMP_DOWNLOAD_DIRECTORY
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(
                title_of_page,
                html_content=page_content
            )
            end = datetime.now()
            ms = (end - start).seconds
            await event.reply("ραѕтє∂ тσ [тєℓєgяαρн](https://telegra.ph/{}) ιη {} ѕєcση∂ѕ.".format(response["path"], ms), link_preview=True)
    else:
        await event.reply("яєρℓу тσ α мєѕѕαgє тσ gєт α ρєямαηєηт тєℓєgяα.ρн ℓιηк.")


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")
