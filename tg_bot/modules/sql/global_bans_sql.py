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

import threading

from sqlalchemy import Column, UnicodeText, Integer, String, Boolean

from Elaina.modules.database_ptb_funcs.sql import BASE, SESSION


class GloballyBannedUsers(BASE):
    __tablename__ = "gbans"
    user_id = Column(Integer, primary_key=True)
    name = Column(UnicodeText, nullable=False)
    reason = Column(UnicodeText)

    def __init__(self, user_id, name, reason=None):
        self.user_id = user_id
        self.name = name
        self.reason = reason

    def __repr__(self):
        return "<GBanned User {} ({})>".format(self.name, self.user_id)

    def to_dict(self):
        return {"user_id": self.user_id,
                "name": self.name,
                "reason": self.reason}


class GbanSettings(BASE):
    __tablename__ = "gban_settings"
    chat_id = Column(String(14), primary_key=True)
    setting = Column(Boolean, default=True, nullable=False)

    def __init__(self, chat_id, enabled):
        self.chat_id = str(chat_id)
        self.setting = enabled

    def __repr__(self):
        return "<Gban setting {} ({})>".format(self.chat_id, self.setting)


GloballyBannedUsers.__table__.create(checkfirst=True)
GbanSettings.__table__.create(checkfirst=True)

GBANNED_USERS_LOCK = threading.RLock()
GBAN_SETTING_LOCK = threading.RLock()
GBANNED_LIST = set()
GBANSTAT_LIST = set()


def gban_user(user_id, name, reason=None):
    with GBANNED_USERS_LOCK:
        user = SESSION.query(GloballyBannedUsers).get(user_id)
        if not user:
            user = GloballyBannedUsers(user_id, name, reason)
        else:
            user.name = name
            user.reason = reason

        SESSION.merge(user)
        SESSION.commit()
        __load_gbanned_userid_list()


def update_gban_reason(user_id, name, reason=None):
    with GBANNED_USERS_LOCK:
        user = SESSION.query(GloballyBannedUsers).get(user_id)
        if not user:
            return None
        old_reason = user.reason
        user.name = name
        user.reason = reason

        SESSION.merge(user)
        SESSION.commit()
        return old_reason


def ungban_user(user_id):
    with GBANNED_USERS_LOCK:
        user = SESSION.query(GloballyBannedUsers).get(user_id)
        if user:
            SESSION.delete(user)

        SESSION.commit()
        __load_gbanned_userid_list()


def is_user_gbanned(user_id):
    return user_id in GBANNED_LIST


def get_gbanned_user(user_id):
    try:
        return SESSION.query(GloballyBannedUsers).get(user_id)
    finally:
        SESSION.close()


def get_gban_list():
    try:
        return [x.to_dict() for x in SESSION.query(GloballyBannedUsers).all()]
    finally:
        SESSION.close()


def enable_gbans(chat_id):
    with GBAN_SETTING_LOCK:
        chat = SESSION.query(GbanSettings).get(str(chat_id))
        if not chat:
            chat = GbanSettings(chat_id, True)

        chat.setting = True
        SESSION.add(chat)
        SESSION.commit()
        if str(chat_id) in GBANSTAT_LIST:
            GBANSTAT_LIST.remove(str(chat_id))


def disable_gbans(chat_id):
    with GBAN_SETTING_LOCK:
        chat = SESSION.query(GbanSettings).get(str(chat_id))
        if not chat:
            chat = GbanSettings(chat_id, False)

        chat.setting = False
        SESSION.add(chat)
        SESSION.commit()
        GBANSTAT_LIST.add(str(chat_id))


def does_chat_gban(chat_id):
    return str(chat_id) not in GBANSTAT_LIST


def num_gbanned_users():
    return len(GBANNED_LIST)


def __load_gbanned_userid_list():
    global GBANNED_LIST
    try:
        GBANNED_LIST = {x.user_id for x in SESSION.query(GloballyBannedUsers).all()}
    finally:
        SESSION.close()


def __load_gban_stat_list():
    global GBANSTAT_LIST
    try:
        GBANSTAT_LIST = {x.chat_id for x in SESSION.query(GbanSettings).all() if not x.setting}
    finally:
        SESSION.close()


def migrate_chat(old_chat_id, new_chat_id):
    with GBAN_SETTING_LOCK:
        chat = SESSION.query(GbanSettings).get(str(old_chat_id))
        if chat:
            chat.chat_id = new_chat_id
            SESSION.add(chat)

        SESSION.commit()


# Create in memory userid to avoid disk access
__load_gbanned_userid_list()
__load_gban_stat_list()
