 # created by @kaneki_ded2
import asyncio
from YoneRobot.events import register
from telegram import Update

@register(pattern=("/about"))
async def kaneki(event):
          await event.reply("hi")
