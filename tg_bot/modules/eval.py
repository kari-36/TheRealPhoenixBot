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

import logging
import sys
from contextlib import contextmanager, redirect_stdout
from telegram import Update, Bot, ParseMode
from telegram.ext import run_async

from telegram.ext import Updater, CommandHandler
from telegram.error import TimedOut, NetworkError
from telegram import ParseMode

from Elaina.modules.disable import DisableAbleCommandHandler
from telegram.ext.dispatcher import run_async
from Elaina.modules.database_ptb_funcs.python_telegram_bot.chat_status import bot_admin, can_promote, user_admin, can_pin, dev_user
from Elaina import dispatcher, LOGGER

from requests import get

# Common imports for eval
import sys
import inspect
import os
import shutil
import glob
import math
import textwrap
import os
import requests
import json
import gc
import datetime
import time
import traceback
import re
import io
import asyncio
import random
import subprocess
import urllib
import psutil

namespaces = {}

def namespace_of(chat, update, bot):
    if chat not in namespaces:
        namespaces[chat] = {
            '__builtins__': globals()['__builtins__'],
            'bot': bot,
            'effective_message': update.effective_message,
            'effective_user': update.effective_user,
            'effective_chat': update.effective_chat,
            'update': update
        }

    return namespaces[chat]


def log_input(update):
    user = update.effective_user.id
    chat = update.effective_chat.id
    LOGGER.info("IN: {} (user={}, chat={})".format(update.effective_message.text, user, chat))

def send(msg, bot, update):
    LOGGER.info("OUT: '{}'".format(msg))
    if len(msg) < 4000:
        bot.send_message(chat_id=update.effective_chat.id, text="`{}`".format(msg), parse_mode=ParseMode.MARKDOWN)
    else:
        with open("output.txt", 'w') as o:
            o.write(f"{msg}\n\n\nUwU OwO OmO")
        with open("output.txt", 'rb') as o:
            bot.send_document(document=o, filename=o.name,
                                          reply_to_message_id=update.message.message_id,
                                          chat_id=update.effective_chat.id)

@dev_user
@run_async
def evaluate(bot, update):
    send(do(eval, bot, update), bot, update)

@dev_user
@run_async
def execute(bot, update):
    send(do(exec, bot, update), bot, update)

def cleanup_code(code):
    if code.startswith('```') and code.endswith('```'):
        return '\n'.join(code.split('\n')[1:-1])
    return code.strip('` \n')


def do(func, bot, update):
    log_input(update)
    content = update.message.text.split(' ', 1)[-1]
    body = cleanup_code(content)
    env = namespace_of(update.message.chat_id, update, bot)

    os.chdir(os.getcwd())
    with open('%s/tg_bot/modules/helper_funcs/temp.txt' % os.getcwd(), 'w') as temp:
        temp.write(body)

    stdout = io.StringIO()

    to_compile = 'def func():\n{}'.format(textwrap.indent(body, "  "))

    try:
        exec(to_compile, env)
    except Exception as e:
        return '{}: {}'.format(e.__class__.__name__, e)

    func = env['func']

    try:
        with redirect_stdout(stdout):
            func_return = func()
    except Exception as e:
        value = stdout.getvalue()
        return '{}{}'.format(value, traceback.format_exc())
    else:
        value = stdout.getvalue()
        result = None
        if func_return is None:
            if value:
                result = '{}'.format(value)
            else:
                try:
                    result = '{}'.format(repr(eval(body, env)))
                except:
                    pass
        else:
            result = '{}{}'.format(value, func_return)
        if result:
            return result
               

@dev_user
@run_async
def clear(bot, update):
    log_input(update)
    global namespaces
    if update.message.chat_id in namespaces:
        del namespaces[update.message.chat_id]
    send("Cleared locals.", bot, update)


def error_callback(bot, update, error):
    try:
        raise error
    except (TimedOut, NetworkError):
        log.debug(error, exc_info=True)
    except:
        log.info(error, exc_info=True)

__mod_name__ = "Eval"

eval_handle = CommandHandler(('e', 'ev', 'eva', 'eval'), evaluate)
exec_handle = CommandHandler(('x', 'ex', 'exe', 'exec', 'py'), execute)
clear_handle = CommandHandler('clearlocals', clear)

dispatcher.add_handler(eval_handle)
dispatcher.add_handler(exec_handle)
dispatcher.add_handler(clear_handle)

