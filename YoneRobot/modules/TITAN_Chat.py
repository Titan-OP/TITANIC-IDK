# CREDITS GOES TO @daisyx and Daisyx's Developers
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import emoji
import aiohttp

# from google_trans_new import google_translator
from googletrans import Translator as google_translator
from pyrogram import filters

from YoneRobot import BOT_ID
from YoneRobot.modules.mongo.chatbot_mongo import add_chat, get_session, remove_chat
from YoneRobot import arq
from YoneRobot.utils.pluginhelp import admins_only, edit_or_reply
from YoneRobot import pbot as eren

translator = google_translator()
url = "https://acobot-brainshop-ai-v1.p.rapidapi.com/get"

async def lunaQuery(query: str, user_id: int):
    luna = await arq.luna(query, user_id)
    return luna.result


def extract_emojis(s):
    return "".join(c for c in s if c in emoji.UNICODE_EMOJI)


async def fetch(url):
    try:
        async with aiohttp.Timeout(10.0):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    try:
                        data = await resp.json()
                    except:
                        data = await resp.text()
            return data
    except:
        print("AI response Timeout")
        return


eren_chats = []
en_chats = []
# AI Chat (C) 2020-2021 by @InukaAsith


@eren.on_message(
    filters.command("chatbot") & ~filters.edited & ~filters.bot & ~filters.private
)
@admins_only
async def chat_bot_status(_, message):
    global eren_chats
    if len(message.command) != 2:
        await message.reply_text(
            "**Error**❌\n**No Command Found**\n➖➖➖➖➖➖➖➖➖\n**List Of Command in ChatBot Module:**\n- `/chatbot ON|On|on`\n- `/chatbot OFF|Off|off`\n\n**For Help Join** [**SUPPORT CHAT**](Https://t.me/TITANX_CHAT).", parse_mode="markdown"
        )
        message.continue_propagation()
    status = message.text.split(None, 1)[1]
    chat_id = message.chat.id
    if status == "ON" or status == "on" or status == "On":
        lel = await edit_or_reply(message, "**Checking AI..**")
        lul = await lel.edit("**Enabling AI Chat...**")
        lol = add_chat(int(message.chat.id))
        if not lol:
            await lel.edit("**AI is Already Enabled In This Chat**\n\n➖➖➖➖➖➖➖\n**For Help Join** [**SUPPORT CHAT**](Https://t.me/TITANX_CHAT).", parse_mode="markdown")
            return
        await lul.edit(
            f"**AI Successfully Enabled For this Chat**\n**Check it by reply `Hi` to bot Message**\n\n➖➖➖➖➖➖➖\n**For Help Join** [**SUPPORT CHAT**](Https://t.me/TITANX_CHAT).", parse_mode="markdown")
        )

    elif status == "OFF" or status == "off" or status == "Off":
        lel = await edit_or_reply(message, "**Checking AI..**")
        lul = await lel.edit("**Disabling AI Chat...**")
        Escobar = remove_chat(int(message.chat.id))
        if not Escobar:
            await lel.edit("**AI Was Not Enabled In This Chat**\n\n➖➖➖➖➖➖➖\n**For Help Join** [**SUPPORT CHAT**](Https://t.me/TITANX_CHAT).", parse_mode="markdown")
            return
        await lul.edit(
            f"**Successfully Disabled AI For This Chat**\n\n➖➖➖➖➖➖➖\n**For Help Join** [**SUPPORT CHAT**](Https://t.me/TITANX_CHAT).", parse_mode="markdown"
        )

    elif status == "EN" or status == "en" or status == "english":
        if not chat_id in en_chats:
            en_chats.append(chat_id)
            await message.reply_text("**English Only AI Enabled!\n\n➖➖➖➖➖➖➖\n**For Help Join** [**SUPPORT CHAT**](Https://t.me/TITANX_CHAT).", parse_mode="markdown")
            return
        await message.reply_text("**English Only AI Is Already Enabled in this chat.**\n\n➖➖➖➖➖➖➖\n**For Help Join** [**SUPPORT CHAT**](Https://t.me/TITANX_CHAT).", parse_mode="markdown")
        message.continue_propagation()
    else:
        await message.reply_text(
            "**Error**❌\n**No Command Found**\n➖➖➖➖➖➖➖➖➖\n**List Of Command in ChatBot Module:**\n- `/chatbot ON|On|on`\n- `/chatbot OFF|Off|off`\n- `/chatbot EN||en|english`\n\n**For Help Join** [**SUPPORT CHAT**](Https://t.me/TITANX_CHAT).", parse_mode="markdown"
        )


@eren.on_message(
    filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.edited
    & ~filters.via_bot
    & ~filters.forwarded,
    group=2,
)
async def chat_bot_function(client, message):
    if not get_session(int(message.chat.id)):
        return
    if not message.reply_to_message:
        return
    try:
        senderr = message.reply_to_message.from_user.id
    except:
        return
    if senderr != BOT_ID:
        return
    msg = message.text
    chat_id = message.chat.id
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    if chat_id in en_chats:
        test = msg
        test = test.replace("eren", "Aco")
        test = test.replace("Eren", "Aco")
        response = await lunaQuery(
            test, message.from_user.id if message.from_user else 0
        )
        response = response.replace("Aco", "Eren")
        response = response.replace("aco", "eren")
        response = response.replace("Luna", "Eren")
        response = response.replace("luna", "Eren")
        response = response.replace("female", "male")

        pro = response
        try:
            await eren.send_chat_action(message.chat.id, "typing")
            await message.reply_text(pro)
        except CFError:
            return

    else:
        u = msg.split()
        emj = extract_emojis(msg)
        msg = msg.replace(emj, "")
        if (
            [(k) for k in u if k.startswith("@")]
            and [(k) for k in u if k.startswith("#")]
            and [(k) for k in u if k.startswith("/")]
            and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
        ):

            h = " ".join(filter(lambda x: x[0] != "@", u))
            km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
            tm = km.split()
            jm = " ".join(filter(lambda x: x[0] != "#", tm))
            hm = jm.split()
            rm = " ".join(filter(lambda x: x[0] != "/", hm))
        elif [(k) for k in u if k.startswith("@")]:

            rm = " ".join(filter(lambda x: x[0] != "@", u))
        elif [(k) for k in u if k.startswith("#")]:
            rm = " ".join(filter(lambda x: x[0] != "#", u))
        elif [(k) for k in u if k.startswith("/")]:
            rm = " ".join(filter(lambda x: x[0] != "/", u))
        elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
            rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
        else:
            rm = msg
            # print (rm)
        try:
            lan = translator.detect(rm)
            lan = lan.lang
        except:
            return
        test = rm
        if not "en" in lan and not lan == "":
            try:
                test = translator.translate(test, dest="en")
                test = test.text
            except:
                return
        # test = emoji.demojize(test.strip())

        test = test.replace("Eren", "Aco")
        test = test.replace("eren", "Aco")
        response = await lunaQuery(
            test, message.from_user.id if message.from_user else 0
        )
        response = response.replace("Aco", "eren")
        response = response.replace("aco", "Eren")
        response = response.replace("Luna", "Eren")
        response = response.replace("luna", "Eren")
        response = response.replace("female", "male")
        pro = response
        if not "en" in lan and not lan == "":
            try:
                pro = translator.translate(pro, dest=lan)
                pro = pro.text
            except:
                return
        try:
            await eren.send_chat_action(message.chat.id, "typing")
            await message.reply_text(pro)
        except CFError:
            return


@eren.on_message(
    filters.text & filters.private & ~filters.edited & filters.reply & ~filters.bot
)
async def sasuke(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    u = msg.split()
    emj = extract_emojis(msg)
    msg = msg.replace(emj, "")
    if (
        [(k) for k in u if k.startswith("@")]
        and [(k) for k in u if k.startswith("#")]
        and [(k) for k in u if k.startswith("/")]
        and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
    ):

        h = " ".join(filter(lambda x: x[0] != "@", u))
        km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
        tm = km.split()
        jm = " ".join(filter(lambda x: x[0] != "#", tm))
        hm = jm.split()
        rm = " ".join(filter(lambda x: x[0] != "/", hm))
    elif [(k) for k in u if k.startswith("@")]:

        rm = " ".join(filter(lambda x: x[0] != "@", u))
    elif [(k) for k in u if k.startswith("#")]:
        rm = " ".join(filter(lambda x: x[0] != "#", u))
    elif [(k) for k in u if k.startswith("/")]:
        rm = " ".join(filter(lambda x: x[0] != "/", u))
    elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
        rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
    else:
        rm = msg
        # print (rm)
    try:
        lan = translator.detect(rm)
        lan = lan.lang
    except:
        return
    test = rm
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, dest="en")
            test = test.text
        except:
            return

    # test = emoji.demojize(test.strip())

    # Kang with the credits bitches @InukaASiTH
    test = test.replace("Eren", "Aco")
    test = test.replace("eren", "Aco")

    response = await lunaQuery(test, message.from_user.id if message.from_user else 0)
    response = response.replace("Aco", "eren")
    response = response.replace("aco", "Eren")
    response = response.replace("Luna", "Eren")
    response = response.replace("luna", "Eren")
    response = response.replace("female", "male")
    pro = response
    if not "en" in lan and not lan == "":
        pro = translator.translate(pro, dest=lan)
        pro = pro.text
    try:
        await eren.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return


@eren.on_message(
    filters.regex("Eren")
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded
    & ~filters.reply
    & ~filters.channel
    & ~filters.edited
)
async def sasuke(client, message):
    msg = message.text
    if msg.startswith("/") or msg.startswith("@"):
        message.continue_propagation()
    u = msg.split()
    emj = extract_emojis(msg)
    msg = msg.replace(emj, "")
    if (
        [(k) for k in u if k.startswith("@")]
        and [(k) for k in u if k.startswith("#")]
        and [(k) for k in u if k.startswith("/")]
        and re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []
    ):

        h = " ".join(filter(lambda x: x[0] != "@", u))
        km = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", h)
        tm = km.split()
        jm = " ".join(filter(lambda x: x[0] != "#", tm))
        hm = jm.split()
        rm = " ".join(filter(lambda x: x[0] != "/", hm))
    elif [(k) for k in u if k.startswith("@")]:

        rm = " ".join(filter(lambda x: x[0] != "@", u))
    elif [(k) for k in u if k.startswith("#")]:
        rm = " ".join(filter(lambda x: x[0] != "#", u))
    elif [(k) for k in u if k.startswith("/")]:
        rm = " ".join(filter(lambda x: x[0] != "/", u))
    elif re.findall(r"\[([^]]+)]\(\s*([^)]+)\s*\)", msg) != []:
        rm = re.sub(r"\[([^]]+)]\(\s*([^)]+)\s*\)", r"", msg)
    else:
        rm = msg
        # print (rm)
    try:
        lan = translator.detect(rm)
        lan = lan.lang
    except:
        return
    test = rm
    if not "en" in lan and not lan == "":
        try:
            test = translator.translate(test, dest="en")
            test = test.text
        except:
            return

    # test = emoji.demojize(test.strip())

    test = test.replace("Eren", "Aco")
    test = test.replace("eren", "Aco")
    response = await lunaQuery(test, message.from_user.id if message.from_user else 0)
    response = response.replace("Aco", "Eren")
    response = response.replace("aco", "eren")
    response = response.replace("Luna", "Eren")
    response = response.replace("luna", "Eren")
    response = response.replace("female", "male")

    pro = response
    if not "en" in lan and not lan == "":
        try:
            pro = translator.translate(pro, dest=lan)
            pro = pro.text
        except Exception:
            return
    try:
        await eren.send_chat_action(message.chat.id, "typing")
        await message.reply_text(pro)
    except CFError:
        return

__help__ = """
**Cʜᴀᴛʙᴏᴛ**
𝐓𝐈𝐓𝐀𝐍 𝟐.𝟎 AI 3.0 cαη ∂єтє¢т & яєρℓу υρтσ 200 ℓαηgυαgєѕ
 
 ✮ /chatbot `[ON|On|on]` *:* Enables ChatBot Mode in the Chat.

 ✮ /chatbot `[OFF|Off|off]` *:* Disables ChatBot Mode in the Chat.

 ✮ /chatbot `[EN|en|english]` *:* Enables English Only AI in the Chat.
"""

__mod_name__ = "AI CʜᴀᴛBᴏᴛ🤖"
