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

from tg_bot import dispatcher, LOGGER
from telegram import Bot, Update
from telegram.ext.dispatcher import run_async
from tg_bot.modules.helper_funcs.chat_status import dev_user
from tg_bot.modules.helper_funcs.misc import sendMessage
from telegram.ext import CommandHandler
from subprocess import Popen, PIPE



def shell(command):
    process = Popen(command,stdout=PIPE,shell=True,stderr=PIPE)
    stdout,stderr = process.communicate()
    return (stdout,stderr)

@dev_user
@run_async
def shellExecute(bot: Bot, update: Update):
    cmd = update.message.text.split(' ',maxsplit=1)
    if len(cmd) == 1:
        sendMessage("No command provided!", bot, update)
        return
    LOGGER.info(cmd)
    output = shell(cmd[1])
    if output[1].decode():
        LOGGER.error(f"Shell: {output[1].decode()}")
    if len(output[0].decode()) > 4000:
        with open("shell.txt",'w') as f:
            f.write(f"Output\n-----------\n{output[0].decode()}\n")
            if output[1]:
                f.write(f"STDError\n-----------\n{output[1].decode()}\n")
        with open("shell.txt",'rb') as f:
            bot.send_document(document=f, filename=f.name,
                                  reply_to_message_id=update.message.message_id,
                                  chat_id=update.message.chat_id)  
    else:
        if output[1].decode():
            sendMessage(f"<code>{output[1].decode()}</code>", bot, update)
            return
        else:
            sendMessage(f"<code>{output[0].decode()}</code>", bot, update)
                                                                                                    

shell_handler = CommandHandler(('sh','shell'), shellExecute)
dispatcher.add_handler(shell_handler)
