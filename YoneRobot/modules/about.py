 # created by @kaneki_ded2
import asyncio
from YoneRobot.events import register
from telegram import Update

@register(pattern=("/about"))
async def kaneki(event):
          await event.reply("Heyo, im *nezuko* from kimestu no yaiba.
                             A powerful bot to help you manage your group.
                             Hit /help to know my features.
                             I can restrict users.
                             I can warn users when they reach max warns I will ban or kick them.
                             I can keep filters and notes and many more to know all of them hit /help
                             Any questions regarding me head to [support group](t.me/nezukosupport1)
                             Keep updated about nezuko by joining [updates](t.me/nezukoupdates1) channel")
