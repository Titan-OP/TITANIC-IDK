__help__ = """

*Antiflood* allows you to take action on users that send more than x messages in a row. Exceeding the set flood \
will result in restricting that user.
 This will mute users if they send more than 10 messages in a row, bots are ignored.
 ✮ /flood*:* Get the current flood control setting

• *Admins only:*
 ✮ /setflood <int/'no'/'off'>*:* enables or disables flood control
 *Example:* `/setflood 10`

 ✮ /setfloodmode <ban/kick/mute/tban/tmute> <value>*:* Action to perform when user have exceeded flood limit. ban/kick/mute/tmute/tban

• *Note:*
 • Value must be filled for tban and tmute!!
 It can be:
 `5m` = 5 minutes
 `6h` = 6 hours
 `3d` = 3 days
 `1w` = 1 week
 """

__mod_name__ = "Aɴᴛɪꜰʟᴏᴏᴅ⚔️"
