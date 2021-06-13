# credits @InukaAsith, @Mr_dark_prince

import logging
import time

from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import (
    ChatAdminRequired,
    PeerIdInvalid,
    UsernameNotOccupied,
    UserNotParticipant,
)
from pyrogram.types import ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup

from YoneRobot import DRAGONS as SUDO_USERS
from YoneRobot import pbot
from YoneRobot.modules.sql_extended import forceSubscribe_sql as sql

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(
    lambda _, __, query: query.data == "onUnMuteRequest"
)


@pbot.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
    user_id = cb.from_user.id
    chat_id = cb.message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        channel = chat_db.channel
        chat_member = client.get_chat_member(chat_id, user_id)
        if chat_member.restricted_by:
            if chat_member.restricted_by.id == (client.get_me()).id:
                try:
                    client.get_chat_member(channel, user_id)
                    client.unban_chat_member(chat_id, user_id)
                    cb.message.delete()
                    # if cb.message.reply_to_message.from_user.id == user_id:
                    # cb.message.delete()
                except UserNotParticipant:
                    client.answer_callback_query(
                        cb.id,
                        text=f"❗ Jσιη συя @{channel} cнαηηєℓ αη∂ ρяєѕѕ 'υηмυтє мє' вυттση.",
                        show_alert=True,
                    )
            else:
                client.answer_callback_query(
                    cb.id,
                    text="❗ уσυ нανє вєєη мυтє∂ ву α∂мιηѕ ∂υє тσ ѕσмє σтнєя яєαѕση.",
                    show_alert=True,
                )
        else:
            if (
                not client.get_chat_member(chat_id, (client.get_me()).id).status
                == "administrator"
            ):
                client.send_message(
                    chat_id,
                    f"❗ **{cb.from_user.mention} ιѕ тяуιηg тσ υηмυтє нιмѕєℓƒ вυт ι cαη'т υηмυтє нιм вєcαυѕє ι αм ησт αη α∂мιη ιη тнιѕ cнαт α∂∂ мє αѕ α∂мιη αgαιη..**\n__#ℓєανιηg тнιѕ cнαт...__",
                )

            else:
                client.answer_callback_query(
                    cb.id,
                    text="❗ ωαяηιηg! ∂ση'т ρяєѕѕ тнє вυттση ωнєη уσυ cαη αℓяєα∂у тαℓк ƒяєєℓу.",
                    show_alert=True,
                )


@pbot.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
    chat_id = message.chat.id
    chat_db = sql.fs_settings(chat_id)
    if chat_db:
        user_id = message.from_user.id
        if (
            not client.get_chat_member(chat_id, user_id).status
            in ("administrator", "creator")
            and not user_id in SUDO_USERS
        ):
            channel = chat_db.channel
            try:
                client.get_chat_member(channel, user_id)
            except UserNotParticipant:
                try:
                    sent_message = message.reply_text(
                        "ωєℓ¢σмє {} ✨ \n **уσυ нανєηт נσιηє∂ συя @{} cнαηηєℓ уєт** 🙄 \n \nρℓєαѕє נσιη [συя cнαηηєℓ](https://t.me/{}) αη∂ нιт тнє **UɴMᴜᴛᴇ Mᴇ** вυттση. \n \n ".format(
                            message.from_user.mention, channel, channel
                        ),
                        disable_web_page_preview=True,
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [
                                    InlineKeyboardButton(
                                        "🔷 Jᴏɪɴ Cʜᴀɴɴᴇʟ 🔷",
                                        url="https://t.me/{}".format(channel),
                                    )
                                ],
                                [
                                    InlineKeyboardButton(
                                        "UɴMᴜᴛᴇ Mᴇ", callback_data="onUnMuteRequest"
                                    )
                                ],
                            ]
                        ),
                    )
                    client.restrict_chat_member(
                        chat_id, user_id, ChatPermissions(can_send_messages=False)
                    )
                except ChatAdminRequired:
                    sent_message.edit(
                        "❗ **𝐓𝐈𝐓𝐀𝐍 𝟐.𝟎 ιѕ ησт α∂мιη нєяє..**\n__gινє мє вαη ρєямιѕѕισηѕ αη∂ яєтяу.. \n#єη∂ιηg ƒσяcє-ѕυвѕcяιвє...__"
                    )

            except ChatAdminRequired:
                client.send_message(
                    chat_id,
                    text=f"❗ **ι ησт αη α∂мιη σƒ @{channel} cнαηηєℓ.**\n__gινє мє α∂мιηѕнιρ σƒ тнαт cнαηηєℓ αη∂ яєтяу.\n#єη∂ιηg ƒσяcє-ѕυвѕcяιвє...__",
                )


@pbot.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
def config(client, message):
    user = client.get_chat_member(message.chat.id, message.from_user.id)
    if user.status is "creator" or user.user.id in SUDO_USERS:
        chat_id = message.chat.id
        if len(message.command) > 1:
            input_str = message.command[1]
            input_str = input_str.replace("@", "")
            if input_str.lower() in ("off", "no", "disable"):
                sql.disapprove(chat_id)
                message.reply_text("❌ **ƒσяcє ѕυвѕcяιвє ιѕ ∂ιѕαвℓє∂ ѕυccєѕѕƒυℓℓу.**")
            elif input_str.lower() in ("clear"):
                sent_message = message.reply_text(
                    "**υηмυтιηg αℓℓ мємвєяѕ ωнσ αяє мυтє∂ ву мє...**"
                )
                try:
                    for chat_member in client.get_chat_members(
                        message.chat.id, filter="restricted"
                    ):
                        if chat_member.restricted_by.id == (client.get_me()).id:
                            client.unban_chat_member(chat_id, chat_member.user.id)
                            time.sleep(1)
                    sent_message.edit("✅ **υηмυтє∂ αℓℓ мємвєяѕ ωнσ ωєяє мυтє∂ ву мє.**")
                except ChatAdminRequired:
                    sent_message.edit(
                        "❗ **ι αм ησт αη α∂мιη ιη тнιѕ cнαт.**\n__ι cαη'т υηмυтє мємвєяѕ вєcαυѕє ι αм ησт αη α∂мιη ιη тнιѕ cнαт мαкє мє α∂мιη ωιтн вαη υѕєя ρєямιѕѕιση.__"
                    )
            else:
                try:
                    client.get_chat_member(input_str, "me")
                    sql.add_channel(chat_id, input_str)
                    message.reply_text(
                        f"✅ **ƒσяcє ѕυвѕcяιвє ιѕ єηαвℓє∂**\n__ƒσяcє ѕυвѕcяιвє ιѕ єηαвℓє∂, αℓℓ тнє gяσυρ мємвєяѕ нανє тσ ѕυвѕcяιвє тнιѕ [cнαηηєℓ](https://t.me/{input_str}) ιη σя∂єя тσ ѕєη∂ мєѕѕαgєѕ ιη тнιѕ gяσυρ.__",
                        disable_web_page_preview=True,
                    )
                except UserNotParticipant:
                    message.reply_text(
                        f"❗ **ησт αη α∂мιη ιη тнє cнαηηєℓ**\n__ι αм ησт αη α∂мιη ιη тнє [cнαηηєℓ](https://t.me/{input_str}). α∂∂ мє αѕ α α∂мιη ιη σя∂єя тσ єηαвℓє ƒσяcє-ѕυвѕcяιвє.__",
                        disable_web_page_preview=True,
                    )
                except (UsernameNotOccupied, PeerIdInvalid):
                    message.reply_text(f"❗ **ιηναℓι∂ cнαηηєℓ υѕєяηαмє.**")
                except Exception as err:
                    message.reply_text(f"❗ **єяяσя:** ```{єяя}```")
        else:
            if sql.fs_settings(chat_id):
                message.reply_text(
                    f"✅ **ƒσяcє ѕυвѕcяιвє ιѕ єηαвℓє∂ ιη тнιѕ cнαт.**\n__ƒσя тнιѕ [cнαηηєℓ](https://t.me/{sql.fs_settings(chat_id).channel})__",
                    disable_web_page_preview=True,
                )
            else:
                message.reply_text("❌ **ƒσяcє ѕυвѕcяιвє ιѕ ∂ιѕαвℓє∂ ιη тнιѕ cнαт.**")
    else:
        message.reply_text(
            "❗ **gяσυρ cяєαтσя яєqυιяє∂**\n__уσυ нανє тσ вє тнє gяσυρ cяєαтσя тσ ∂σ тнαт.__"
        )


__help__ = """
*ƒσяcє ѕυвѕcяιвє:*
✮ 𝐓𝐈𝐓𝐀𝐍 𝟐.𝟎 cαη мυтє мємвєяѕ ωнσ αяє ησт ѕυвѕcяιвє∂ уσυя cнαηηєℓ υηтιℓ тнєу ѕυвѕcяιвє.
✮ ωнєη єηαвℓє∂ ι ωιℓℓ мυтє υηѕυвѕcяιвє∂ мємвєяѕ αη∂ ѕнσω тнєм α υηмυтє вυттση. ωнєη тнєу ωιℓℓ ѕυвѕcяιвє αη∂ ρяєѕѕ тнє вυттση ι ωιℓℓ υηмυтє тнєм.
🔹 *ѕєтυρ* 🔹
📍 *σηℓу gяσυρ cяєαтσя cαη υѕє тнє ƒσяcє ѕυвѕcяιвє cσммαη∂ѕ*
✮ α∂∂ мє ιη уσυя gяσυρ αѕ α∂мιη
✮ α∂∂ мє ιη уσυя cнαηηєℓ αѕ α∂мιη
 
♦️ *cσмммαη∂ѕ* ♦️
 ✮ /fsub {channel username} - тσ тυяη ση αη∂ ѕєтυρ тнє cнαηηєℓ.
    
     `💡Hint: Do this first...`

 ✮ /fsub - тσ gєт тнє cυяяєηт ѕєттιηgѕ.

 ✮ /fsub disable - тσ тυяη σƒƒ ƒσяcє-ѕυвѕcяιвє...
  
     `💡Hint: If you disable fsub, you need to set again for working.. /fsub {channel username}`

 ✮ /fsub clear - тσ υηмυтє αℓℓ мємвєяѕ ωнσ мυтє∂ ву мє.
"""
__mod_name__ = "Force-Sub📢"
