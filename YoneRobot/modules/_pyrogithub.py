# © @Mr_Dark_Prince
import aiohttp
from pyrogram import filters
from YoneRobot import pbot
from YoneRobot.pyrogramee.errors import capture_err


__mod_name__ = "Gɪᴛʜᴜʙ🐈"


@pbot.on_message(filters.command('github'))
@capture_err
async def github(_, message):
    if len(message.command) != 2:
        await message.reply_text("/git Username")
        return
    username = message.text.split(None, 1)[1]
    URL = f'https://api.github.com/users/{username}'
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await message.reply_text("404")

            result = await request.json()
            try:
                url = result['html_url']
                name = result['name']
                company = result['company']
                bio = result['bio']
                created_at = result['created_at']
                avatar_url = result['avatar_url']
                blog = result['blog']
                location = result['location']
                repositories = result['public_repos']
                followers = result['followers']
                following = result['following']
                caption = f"""**Info Of {name}**
✧ **𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞:** `{username}`

✧ **𝐁𝐢𝐨:** `{bio}`

✧ **𝐏𝐫𝐨𝐟𝐢𝐥𝐞 𝐋𝐢𝐧𝐤:** [Here]({url})

✧ **𝐂𝐨𝐦𝐩𝐚𝐧𝐲:** `{company}`

✧ **𝐂𝐫𝐞𝐚𝐭𝐞𝐝 𝐎𝐧:** `{created_at}`

✧ **𝐑𝐞𝐩𝐨𝐬𝐢𝐭𝐨𝐫𝐢𝐞𝐬:** `{repositories}`

✧ **𝐁𝐥𝐨𝐠:** `{blog}`

✧ **𝐋𝐨𝐜𝐚𝐭𝐢𝐨𝐧:** `{location}`

✧ **𝐅𝐨𝐥𝐥𝐨𝐰𝐞𝐫𝐬:** `{followers}`

✧ **𝐅𝐨𝐥𝐥𝐨𝐰𝐢𝐧𝐠:** `{following}`"""
            except Exception as e:
                print(str(e))
                pass
    await message.reply_photo(photo=avatar_url, caption=caption)
