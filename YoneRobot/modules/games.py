from telethon.tl.types import InputMediaDice

from YoneRobot.events import register


@register(pattern="^/dice(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    r = await event.reply(file=InputMediaDice(""))
    input_int = int(input_str)
    if input_int > 6:
        await event.reply("hey nigga use number 1 to 6 only")


@register(pattern="^/dart(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    r = await event.reply(file=InputMediaDice("🎯"))
    input_int = int(input_str)
    if input_int > 6:
        await event.reply("hey nigga use number 1 to 6 only")


@register(pattern="^/ball(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    r = await event.reply(file=InputMediaDice("🏀"))
    input_int = int(input_str)
    if input_int > 5:
        await event.reply("hey nigga use number 1 to 6 only")


__help__ = """
 *Play Game With Emojis:*
  
  ✮ /dice σя /dice 1 тσ 6 αηу ναℓυє
 
  ✮ /ball σя /ball 1 тσ 5 αηу ναℓυє

  ✮ /dart σя /dart 1 тσ 6 αηу ναℓυє
       `𝚄𝚜𝚊𝚐𝚎: 𝚑𝚊𝚑𝚊𝚑𝚊 𝚓𝚞𝚜𝚝 𝚊 𝚖𝚊𝚐𝚒𝚌.`

  `⚠️ᴡᴀʀɴɪɴɢ: ʏᴏᴜ ᴡᴏᴜʟᴅ ʙᴇ ɪɴ ᴛʀᴏᴜʙʟᴇ ɪꜰ ʏᴏᴜ ɪɴᴘᴜᴛ ᴀɴʏ ᴏᴛʜᴇʀ ᴠᴀʟᴜᴇ ᴛʜᴀɴ ᴍᴇɴᴛɪᴏɴᴇᴅ.`
"""

__mod_name__ = "Gᴀᴍᴇꜱ🎮"
