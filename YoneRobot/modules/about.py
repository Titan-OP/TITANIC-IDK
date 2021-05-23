 # created by @kaneki_ded2
import asyncio
from YoneRobot.events import register

@register(pattern=("/about"))
async def kaneki(event):
          msg = update.effective_message
          message = msg.reply_text("heyo there")

          message.edit_text("hey there")
