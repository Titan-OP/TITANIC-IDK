import random, html

from YoneRobot import dispatcher
from YoneRobot.modules.disable import (
    DisableAbleCommandHandler,
    DisableAbleMessageHandler,
)
from YoneRobot.modules.sql import afk_sql as sql
from YoneRobot.modules.users import get_user_id
from telegram import MessageEntity, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, Filters, MessageHandler, run_async

MAFK_VID = "https://telegra.ph/file/c1151e4efbb0baf8eff51.mp4"
USER_BACK = "https://telegra.ph/file/7a05f54e91f895aac0487.mp4"
MAFK_REASON_VID = "CgACAgQAAx0CVTtJdwABBjt4YNv3F7bmbzNIFgFccx7ZDhrwVScAAiECAAK6E61Rt4B92ymItZ0gBA"
AFK_GROUP = 7
AFK_REPLY_GROUP = 8
chosen_vid = random.choice(MAFK_REASON_VID)

@run_async
def afk(update: Update, context: CallbackContext):
    args = update.effective_message.text.split(None, 1)
    user = update.effective_user

    if not user:  # ignore channels
        return

    if user.id in [777000, 1087968824]:
        return

    notice = ""
    if len(args) >= 2:
        reason = args[1]
        if len(reason) > 100:
            reason = reason[:100]
            notice = "\nYour afk reason was shortened to 100 characters."
    else:
        reason = ""

    sql.set_afk(update.effective_user.id, reason)
    fname = update.effective_user.first_name
    try:
        afk = [
                "{} is now AFK!",
                "bye bye, {}!",
                "{} is now away!",
        ]
        chosen_msg = random.choice(afk)
        update.effective_message.reply_animation(MAFK_VID, caption=chosen_msg.format(fname))
    except BadRequest:
        pass


@run_async
def no_longer_afk(update: Update, context: CallbackContext):
    user = update.effective_user
    message = update.effective_message

    if not user:  # ignore channels
        return

    res = sql.rm_afk(user.id)
    if res:
        if message.new_chat_members:  # dont say msg
            return
        firstname = update.effective_user.first_name
        try:
            options = [
                "{} is back!",
                "welcome back {}!",
                "Yo, {} is here!",
                "{} is online!",
                "{} is finally here!",
                "Welcome back! {}",
            ]
            chosen_option = random.choice(options)
            update.effective_message.reply_animation(USER_BACK, caption=chosen_option.format(firstname))
        except:
            return


@run_async
def reply_afk(update: Update, context: CallbackContext):
    bot = context.bot
    message = update.effective_message
    userc = update.effective_user
    userc_id = userc.id
    if message.entities and message.parse_entities(
        [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
    ):
        entities = message.parse_entities(
            [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]
        )

        chk_users = []
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

            if ent.type != MessageEntity.MENTION:
                return

            user_id = get_user_id(message.text[ent.offset : ent.offset + ent.length])
            if not user_id:
                # Should never happen, since for a user to become AFK they must have spoken. Maybe changed username?
                return

            if user_id in chk_users:
                return
            chk_users.append(user_id)

            try:
                chat = bot.get_chat(user_id)
            except BadRequest:
                print("Error: Could not fetch userid {} for AFK module".format(user_id))
                return
            fst_name = chat.first_name

            check_afk(update, context, user_id, fst_name, userc_id)

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        fst_name = message.reply_to_message.from_user.first_name
        check_mafk(update, context, user_id, fst_name, userc_id)


def check_afk(update, context, user_id, fst_name, userc_id):
    if sql.is_afk(user_id):
        user = sql.check_afk_status(user_id)
        if int(userc_id) == int(user_id):
            return
        if not user.reason:
            mess = "{} is afk".format(fst_name)
            update.effective_message.reply_animation(MAFK_REASON_VID, caption=mess)
        else:
            res = "{} is afk.\nReason: <code>{}</code>".format(
                html.escape(fst_name), html.escape(user.reason)
            )
            update.effective_message.reply_animation(MAFK_REASON_VID, caption=res, parse_mode="html")



# __help__ = """

# *THIS COMMANDS ARE USED WHEN YOU WANT TO GO AFK (AWAY FROM KEYBOARD).*

# ✮ /afk or brb *:* Normal AFK function.

# ✮ /mafk *:* Media AFK, Use it and get to know more ;)

# For any Type of Queries Join @TITANX_CHAT
# """


AFK_HANDLER = DisableAbleCommandHandler("afk", afk)
AFK_REGEX_HANDLER = DisableAbleMessageHandler(
    Filters.regex(r"^(?i)brb(.*)$"), afk, friendly="afk"
)
NO_AFK_HANDLER = MessageHandler(Filters.all & Filters.group, no_longer_afk)
AFK_REPLY_HANDLER = MessageHandler(Filters.all & Filters.group, reply_afk)

dispatcher.add_handler(AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REGEX_HANDLER, AFK_GROUP)
dispatcher.add_handler(NO_AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REPLY_HANDLER, AFK_REPLY_GROUP)

__mod_name__ = "AFK🏃"
__command_list__ = ["afk"]
__handlers__ = [
    AFK_HANDLER, AFK_GROUP,
    AFK_REGEX_HANDLER, AFK_GROUP,
    NO_AFK_HANDLER, AFK_GROUP,
    AFK_REPLY_HANDLER, AFK_REPLY_GROUP,
]
