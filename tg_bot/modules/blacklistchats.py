"""
MIT License

Copyright (C) 2021 Slient-Boy

This file is part of @ShokoGBot  (Elaina) [Telegram Bot]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from telegram import Bot, Update
from telegram.ext import MessageHandler, Filters, DispatcherHandlerStop
from telegram.error import TelegramError

from Elaina import dispatcher, BL_CHATS, LOGGER, OWNER_ID


BL_CHATS_GROUP = -1


def blacklist_chats(bot: Bot, update: Update):
    chat = update.effective_chat
    if not chat.id in BL_CHATS:
        return
    try:
        chat.send_message(
            "This chat has been blacklisted! Head over to @Elaina_Support_Chat to find out why!"
        )
        chat.leave()
        raise DispatcherHandlerStop
    except TelegramError as e:
        LOGGER.error(f"Couldn't leave blacklisted chat: {chat.id} due to:\n{e}")
            
            
BLACKLIST_CHATS_HANDLER = MessageHandler(
    Filters.group,
    blacklist_chats
)

dispatcher.add_handler(
    BLACKLIST_CHATS_HANDLER,
    group=BL_CHATS_GROUP
)
