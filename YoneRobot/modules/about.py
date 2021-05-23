 # created by @kaneki_ded2
import asyncio
from YoneRobot.events import register

@register(pattern=("/about"))
async def kaneki(event):
  await event.reply("hey there")
