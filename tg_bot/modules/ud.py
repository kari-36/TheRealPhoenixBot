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

from telegram import Update, Bot, ParseMode
from telegram.ext import run_async

from Elaina.modules.disable import DisableAbleCommandHandler
from Elaina import dispatcher

from requests import get

@run_async
def ud(bot: Bot, update: Update):
    msg = update.effective_message.reply_to_message if update.message.reply_to_message else update.effective_message
    if msg == update.effective_message:
        text = msg.text[len('/ud '):]
    # Args should take more precedence. Hence even if it's a reply, it'll query what you typed
    elif msg == update.effective_message.reply_to_message and len(update.effective_message.text) > 3:
        text = update.effective_message.text[len('/ud '):]
    else:
        text = msg.text
    if text == "":
        update.message.reply_text("Please enter a query to look up on Urban Dictionary!")
    else:
        results = get(f'http://api.urbandictionary.com/v0/define?term={text}').json()
    try:
        reply_text = f'*{text}*\n\n{results["list"][0]["definition"]}\n\n_{results["list"][0]["example"]}_'
    except IndexError:
        reply_text = None
    if reply_text:
        update.message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)
    else:
        update.message.reply_text("No results found!")

__help__ = """
 - /ud <expression> :- Returns the top definition of the word or expression on Urban Dictionary.
"""

__mod_name__ = "Urban Dictionary"
  
ud_handle = DisableAbleCommandHandler("ud", ud)

dispatcher.add_handler(ud_handle)
