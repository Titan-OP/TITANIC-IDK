from YoneRobot import telethn as tbot
import os

from gtts import gTTS
from gtts import gTTSError
from telethon import *
from telethon.tl import functions
from telethon.tl import types
from telethon.tl.types import *

from YoneRobot import *

from YoneRobot.events import register


async def is_register_admin(chat, user):
    if isinstance(chat, (types.InputPeerChannel, types.InputChannel)):
        return isinstance(
            (
                await tbot(functions.channels.GetParticipantRequest(chat, user))
            ).participant,
            (types.ChannelParticipantAdmin, types.ChannelParticipantCreator),
        )
    if isinstance(chat, types.InputPeerUser):
        return True


@register(pattern="^/tts (.*)")
async def _(event):
    if event.fwd_from:
        return
    if event.is_group:
     if not (await is_register_admin(event.input_chat, event.message.sender_id)):
       await event.reply("🚨 ηєє∂ α∂мιη ρσωєя.. уσυ cαη'т υѕє тнιѕ cσммαη∂.. вυт уσυ cαη υѕє ιη му PM|DM")
       return

    input_str = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str
    elif "|" in input_str:
        lan, text = input_str.split("|")
    else:
        await event.reply(
            "ɪηναℓι∂ ѕуηтαχ\nꜰσямαт `/tts lang | text`\nꜰᴏʀ ᴇɢ: `/tts en | hello`"
        )
        return
    text = text.strip()
    lan = lan.strip()
    try:
        tts = gTTS(text, tld="com", lang=lan)
        tts.save("k.mp3")
    except AssertionError:
        await event.reply(
            "тнє тєχт ιѕ ємρту.\n"
            "ησтнιηg ℓєƒт тσ ѕρєαк αƒтєя ρяє-ρяєcєѕѕιηg, "
            "тσкєηιzιηg αη∂ cℓєαηιηg."
        )
        return
    except ValueError:
        await event.reply("ℓαηgυαgє ιѕ ησт ѕυρρσятє∂.")
        return
    except RuntimeError:
        await event.reply("єяяσя ℓσα∂ιηg тнє ℓαηgυαgєѕ ∂ιcтισηαяу.")
        return
    except gTTSError:
        await event.reply("єяяσя ιη gσσgℓє ᴛᴇxᴛ-ᴛᴏ-ꜱᴘᴇᴇᴄʜ ᴀᴘɪ яєqυєѕт !")
        return
    with open("k.mp3", "r"):
        await tbot.send_file(
            event.chat_id, "k.mp3", voice_note=True, reply_to=reply_to_id
        )
        os.remove("k.mp3")
