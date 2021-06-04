 # created by @kaneki_ded2
import asyncio
from YoneRobot.events import register
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, Update
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async


buttons = [
    [
        InlineKeyboardButton(
            text="T&C", callback_data="terms_"),
    ],
    [
        InlineKeyboardButton(text="updates", url="https://t.me/nezukoupdates1"),
        InlineKeyboardButton(
            text="support", url=f"https://t.me/nezukosupport1"
        ),
    ],
    [
        InlineKeyboardButton(text="Demon Arts", callback_data="help_back"),
    ],
]


@run_async
def yone_about_callback(update, context):
    query = update.callback_query
    if query.data == "terms_":
        query.message.edit_text(
            text="""Terms and Conditions:
                  \n• Only your first name, last name(if any) and username(if any) is stored.
                  \n• No group ID or it's messages are stored, We respect everyone's privacy.
                  \n• Don't spam commands, buttons, or anything in bot PM, if we found anyone doing than he will probhited.
                  \n• Messages between Bot & you is only infront of your eyes and there is no backuse of it..
                  \n• NSFW will get permanent global ban in Nezuko  which never removes, report spammers here -> @nezukosupport1.

                  \nNOTE: Terms and Conditions will be change anytime.

                  \nJoin @nezukoupdates1 for Updates.
                  \nJoin @nezukosupport1 to get answer of yours questions""",
           parse_mode=ParseMode.MARKDOWN,
           disable_web_page_preview=True,
           reply_markup=InlineKeyboardMarkup(
                [
                 [
                    InlineKeyboardButton(text="Back", callback_data="terms_back")
                 ]
                ]
            ),
        )
    elif query.data == "terms_back":
        query.message.edit_text("""Heyo, im NEZUKO from kimestu no yaiba.
                             \nA powerful bot to help you manage your group.
                             \nHit /help to know my features.
                             \nI can restrict users.
                             \nI can warn users when they reach max warns I will ban or kick them.
                             \nI can keep filters and notes and many more to know all of them hit /help.
                             \nAny questions regarding me head to [support group](t.me/nezukosupport1)
                             \nKeep updated about nezuko by joining [updates](t.me/nezukoupdates1) channel""")




@register(pattern=("/about"))
async def _(event):
          await event.reply("""Heyo, im NEZUKO from kimestu no yaiba.
                             \nA powerful bot to help you manage your group.
                             \nHit /help to know my features.
                             \nI can restrict users.
                             \nI can warn users when they reach max warns I will ban or kick them.
                             \nI can keep filters and notes and many more to know all of them hit /help.
                             \nAny questions regarding me head to [support group](t.me/nezukosupport1)
                             \nKeep updated about nezuko by joining [updates](t.me/nezukoupdates1) channel""",
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=buttons
                          )
