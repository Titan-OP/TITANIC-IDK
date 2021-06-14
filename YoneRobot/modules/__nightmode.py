#     (A Telegram Bot Project)
#    Copyright (C) 2019-Present Anonymous (https://t.me/MissJulia_Robot)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, in version 3 of the License.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see < https://www.gnu.org/licenses/agpl-3.0.en.html >


from datetime import timedelta

import dateparser
from telethon import *
from telethon.tl.types import ChatBannedRights

from YoneRobot.events import register
from YoneRobot.mongo import db
from YoneRobot import telethn as tbot

nightmod = db.nightmode


closechat = ChatBannedRights(
    until_date=None,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    send_polls=True,
    invite_users=True,
    pin_messages=True,
    change_info=True,
)

openchat = ChatBannedRights(
    until_date=None,
    send_messages=False,
    send_media=False,
    send_stickers=False,
    send_gifs=False,
    send_games=False,
    send_inline=False,
    send_polls=False,
    invite_users=True,
    pin_messages=True,
    change_info=True,
)


async def can_change_info(message):
    result = await tbot(
        functions.channels.GetParticipantRequest(
            channel=message.chat_id,
            user_id=message.sender_id,
        )
    )
    p = result.participant
    return isinstance(p, types.ChannelParticipantCreator) or (
        isinstance(p, types.ChannelParticipantAdmin) and p.admin_rights.change_info
    )


def get_info(id):
    return nightmod.find_one({"id": id})


@register(pattern="^/nightmode(?: |$)(.*)")
async def profanity(event):
    if event.fwd_from:
        return
    if event.is_private:
        return
    if not await can_change_info(message=event):
        return
    input = event.pattern_match.group(1)
    chats = nightmod.find({})
    if not input:
        for c in chats:
            if event.chat_id == c["id"]:
                await event.reply(
                    "ρℓєαѕє ρяσνι∂є ѕσмє ιηρυт уєѕ σя ησ.\n\ncυяяєηт ѕєттιηg ιѕ : **ᴏɴ**"
                )
                return
        await event.reply(
            "ρℓєαѕє ρяσνι∂є ѕσмє ιηρυт уєѕ σя ησ.\n\ncυяяєηт ѕєттιηg ιѕ : **ᴏꜰꜰ**"
        )
        return
    if input == "on":
        if event.is_group:
            chats = nightmod.find({})
            for c in chats:
                if event.chat_id == c["id"]:
                    await event.reply("ηιgнтмσ∂є ιѕ αℓяєα∂у αcтιναтє∂ ƒσя тнιѕ cнαт.")
                    return
            nightmod.insert_one(
                {
                    "id": event.chat_id,
                    "valid": False,
                    "zone": None,
                    "ctime": None,
                    "otime": None,
                }
            )
            await event.reply(
                "ηιgнтмσ∂є тυяηє∂ ση ƒσя тнιѕ cнαт\n**ɴᴏᴛᴇ:** ιт ωιℓℓ ησт ωσяк υηℓєѕѕ уσυ ѕρєcιƒу тιмє αη∂ zσηє ωιтн `/setnightmode`"
            )
    if input == "off":
        if event.is_group:
            chats = nightmod.find({})
            for c in chats:
                if event.chat_id == c["id"]:
                    nightmod.delete_one({"id": event.chat_id})
                    await event.reply("ηιgнтмσ∂є тυяηє∂ σƒƒ ƒσя тнιѕ cнαт.")
                    return
        await event.reply("ηιgнтмσ∂є ιѕη'т тυяηє∂ ση ƒσя тнιѕ cнαт.")
    if not input == "on" and not input == "off":
        await event.reply("ι σηℓу υη∂єяѕтαη∂ ву ση σя σƒƒ")
        return


@register(pattern="^/setnightmode (.*)")
async def _(event):
    try:
        if event.fwd_from:
            return
        if event.is_private:
            return
        if not await can_change_info(message=event):
            return
        quew = event.pattern_match.group(1)
        if "|" in quew:
            zone, ctime, otime = quew.split(":")
        zone = zone.strip()
        ctime = ctime.strip()
        otime = otime.strip()
        if len(ctime) != 11:
            await event.reply("ρℓєαѕє єηтєя ναℓι∂ ∂αтє αη∂ тιмє.")
            return
        if len(otime) != 11:
            await event.reply("ρℓєαѕє єηтєя ναℓι∂ ∂αтє αη∂ тιмє.")
            return
        if not zone and ctime and otime:
            await event.reply("мιѕѕιηg ѕσмє ραяαмєтєяѕ.")
            return
        ttime = dateparser.parse(
            "now", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "YMD"}
        )
        if ttime == None or otime == None or ctime == None:
            await event.reply("ρℓєαѕє єηтєя ναℓι∂ ∂αтє αη∂ тιмє αη∂ zσηє.")
            return
        cctime = dateparser.parse(
            f"{ctime}", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "DMY"}
        ) + timedelta(days=1)
        ootime = dateparser.parse(
            f"{otime}", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "DMY"}
        ) + timedelta(days=1)
        if cctime == ootime:
            await event.reply("cнαт σρєηιηg αη∂ cℓσѕιηg тιмє cαηησт вє ѕαмє..")
            return
        if not ootime > cctime and not cctime < ootime:
            await event.reply("cнαт σρєηιηg тιмє must вє greater тнαη cℓσѕιηg тιмє")
            return
        if cctime > ootime:
            await event.reply("cнαт cℓσѕιηg тιмє cant вє greater тнαη σρєηιηg тιмє")
            return
        # print (ttime)
        # print (cctime)
        # print (ootime)
        chats = nightmod.find({})
        for c in chats:
            if event.chat_id == c["id"] and c["valid"] == True:
                to_check = get_info(
                    id=event.chat_id,
                )
                nightmod.update_one(
                    {
                        "_id": to_check["_id"],
                        "id": to_check["id"],
                        "valid": to_check["valid"],
                        "zone": to_check["zone"],
                        "ctime": to_check["ctime"],
                        "otime": to_check["otime"],
                    },
                    {"$set": {"zone": zone, "ctime": cctime, "otime": ootime}},
                )
                await event.reply(
                    "ηιgнтмσ∂є αℓяєα∂у ѕєт.\nι αм υρ∂αтιηg тнє zσηє, cℓσѕιηg тιмє αη∂ σρєηιηg тιмє ωιтн тнє ηєω zσηє, cℓσѕιηg тιмє αη∂ σρєηιηg тιмє."
                )
                return
        nightmod.insert_one(
            {
                "id": event.chat_id,
                "valid": True,
                "zone": zone,
                "ctime": cctime,
                "otime": ootime,
            }
        )
        await event.reply("ηιgнтмσ∂є ѕєт ѕυccєѕѕƒυℓℓу !")
    except Exception as e:
        print(e)


@tbot.on(events.NewMessage(pattern=None))
async def _(event):
    try:
        if event.is_private:
            return
        chats = nightmod.find({})
        for c in chats:
            # print(c)
            id = c["id"]
            valid = c["valid"]
            zone = c["zone"]
            ctime = c["ctime"]
            c["otime"]
            present = dateparser.parse(
                f"now", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "YMD"}
            )
            if present > ctime and valid:
                await tbot.send_message(
                    id,
                    f"**ɴɪɢʜᴛʙᴏᴛ:** ιт'ѕ тιмє cℓσѕιηg тнє cнαт ησω ...",
                )
                await tbot(
                    functions.messages.EditChatDefaultBannedRightsRequest(
                        peer=id, banned_rights=closechat
                    )
                )
                newtime = ctime + timedelta(days=1)
                to_check = get_info(id=id)
                if not to_check:
                    return
                print(newtime)
                print(to_check)
                nightmod.update_one(
                    {
                        "_id": to_check["_id"],
                        "id": to_check["id"],
                        "valid": to_check["valid"],
                        "zone": to_check["zone"],
                        "ctime": to_check["ctime"],
                        "otime": to_check["otime"],
                    },
                    {"$set": {"ctime": newtime}},
                )
                break
                return
            continue
    except Exception as e:
        print(e)


@tbot.on(events.NewMessage(pattern=None))
async def _(event):
    try:
        if event.is_private:
            return
        chats = nightmod.find({})
        for c in chats:
            # print(c)
            id = c["id"]
            valid = c["valid"]
            zone = c["zone"]
            c["ctime"]
            otime = c["otime"]
            present = dateparser.parse(
                f"now", settings={"TIMEZONE": f"{zone}", "DATE_ORDER": "YMD"}
            )
            if present > otime and valid:
                await tbot.send_message(
                    id,
                    f"**ɴɪɢʜᴛʙᴏᴛ:** ιт'ѕ тιмє σρєηιηg тнє cнαт ησω ...",
                )
                await tbot(
                    functions.messages.EditChatDefaultBannedRightsRequest(
                        peer=id, banned_rights=openchat
                    )
                )
                newtime = otime + timedelta(days=1)
                to_check = get_info(id=id)
                if not to_check:
                    return
                print(newtime)
                print(to_check)
                nightmod.update_one(
                    {
                        "_id": to_check["_id"],
                        "id": to_check["id"],
                        "valid": to_check["valid"],
                        "zone": to_check["zone"],
                        "ctime": to_check["ctime"],
                        "otime": to_check["otime"],
                    },
                    {"$set": {"otime": newtime}},
                )
                break
                return
            continue
    except Exception as e:
        print(e)


