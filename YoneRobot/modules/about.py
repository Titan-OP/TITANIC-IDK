 # created by @kaneki_ded2
import asyncio
from YoneRobot.events import register
from telegram import Update

@register(pattern=("/about"))
async def kaneki(event):
          await event.reply("Im *nezuko*, a powerful group management bot built to help you manage your group easily.
                 \n❍ I can restrict users.
                 \n❍ I can greet users with customizable welcome messages and even set a group's rules.
                 \n❍ I have an advanced anti-flood system.
                 \n❍ I can warn users until they reach max warns, with each predefined actions such as ban, mute, kick, etc.
                 \n❍ I check for admins' permissions before executing any command and more stuffs
                 \n\n_nezuko's licensed under the GNU General Public License v3.0_
                 \nany questions about *nezuko* come to [support](t.me/nezukosupport1) .
                 \n\nkeep updated about *nezuko* by joining [updates](t.me/nezukoupdates1) channel.")
