 # created by @kaneki_ded2
import asyncio
from YoneRobot.events import register
from telegram import Update

@register(pattern=("/about"))
async def kaneki(update: Update):
          msg = update.effective_message
          message = msg.reply_text("heyo there")

          message.edit_text("hey there")
