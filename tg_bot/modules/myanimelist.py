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

from typing import List
from malclient import Client
from malclient.exceptions import APIException

from telegram import Bot, Update, Message, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import run_async
from Elaina import OWNER_ID, MAL_CLIENT_ID, MAL_ACCESS_TOKEN, MAL_REFRESH_TOKEN, dispatcher
from Elaina.modules.disable import DisableAbleCommandHandler


client = Client()
client.init(access_token=MAL_ACCESS_TOKEN)


def refresh_token(msg: Message, error: APIException) -> None:
    if str(error.response) == "<Response [401]>":
        client.refresh_bearer_token(
            client_id=MAL_CLIENT_ID,
            refresh_token=MAL_REFRESH_TOKEN,
            client_secret=None
        )
        new_access_token = client.bearer_token
        new_refresh_token = client.refresh_token
        MSG_TEXT = (f"Your MAL access token has expired.\n*New Access Token*: `{new_access_token}`\n"
            f"*New Refresh Token*: `{new_refresh_token}`")
        bot.send_message(OWNER_ID, MSG_TEXT, parse_mode="MARKDOWN")
    else:
        msg.reply_text(f"An error occurred:\n`{error}`", parse_mode="MARKDOWN")


@run_async
def search_anime(bot: Bot, update: Update, args: List[str]) -> None:
    msg = update.effective_message
    query = " ".join(args)
    if not query:
        msg.reply_text("I can't search for nothing...")
        return
    try:
        anime = client.search_anime(query)
    except APIException as e:
        refresh_token(msg, e)
    if not anime:
        msg.reply_text("Not found!")
        return
    anime_id = anime[0].id
    res = client.get_anime_details(anime_id)
    if res.status == "finished_airing":
        status = "Finished Airing"
        episodes = res.num_episodes
    else:
        episodes = None
    genres_list = []
    for i in res.genres:
        genres_list.append(i.name)
    genres = ", ".join(genres_list)
    studio_list = []
    for i in res.studios:
        studio_list.append(i.name)
    studios = ", ".join(studio_list)
    if res.status == "currently_airing":
        status = "Currently Airing"
    if res.start_season:
        premier = res.start_season
    premiered = f"{premier.year} {premier.season.capitalize()}"
    image = res.main_picture.large
    text = f"<b>{res.title} ({res.alternative_titles.ja})</b>\n"
    text += f"<b>Type</b>: <code>{res.media_type.upper()}</code>\n"
    text += f"<b>Source</b>: <code>{res.source.replace('_', ' ').capitalize()}</code>\n"
    text += f"<b>Status</b>: <code>{status}</code>\n"
    text += f"<b>Genres</b>: <code>{genres}</code>\n"
    if episodes:
        text += f"<b>Episodes</b>: <code>{episodes}</code>\n"
    text += f"<b>Score</b>: <code>{res.mean}</code>\n"
    text += f"<b>Ranked</b>: <code>#{res.rank}</code>\n"
    text += f"<b>Studio(s)</b>: <code>{studios}</code>\n"
    text += f"<b>Premiered</b>: <code>{premiered}</code>\n\n"
    text += f"<a href='{image}'>\u200c</a>"
    text += res.synopsis
    keyb = [
        [InlineKeyboardButton("More Information", url=f"https://myanimelist.net/anime/{anime_id}")]
    ]
    
    msg.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyb))


@run_async
def search_manga(bot: Bot, update: Update, args: List[str]) -> None:
    msg = update.effective_message
    query = " ".join(args)
    if not query:
        msg.reply_text("I can't search for nothing...")
        return
    try:
        manga = client.search_manga(query)
    except APIException as e:
        refresh_token(msg, e)
    if not manga:
        msg.reply_text("Not found!")
        return
    manga_id = manga[0].id
    res = client.get_manga_details(manga_id)
    genres_list = []
    for i in res.genres:
        genres_list.append(i.name)
    genres = ", ".join(genres_list)
    image = res.main_picture.large
    
    text = f"<b>{res.title} ({res.alternative_titles.ja})</b>\n"
    text += f"<b>Type</b>: <code>{res.media_type.capitalize()}</code>\n"
    text += f"<b>Status</b>: <code>{res.status.replace('_', ' ').capitalize()}</code>\n"
    text += f"<b>Genres</b>: <code>{genres}</code>\n"
    text += f"<b>Score</b>: <code>{res.mean}</code>\n"
    text += f"<b>Ranked</b>: <code>#{res.rank}</code>\n"
    if res.num_volumes:
        text += f"<b>Volumes</b>: <code>{res.num_volumes}</code>\n"
    if res.num_chapters:
        text += f"<b>Chapters</b>: <code>{res.num_chapters}</code>\n"
    text += f"<a href='{image}'>\u200c</a>"
    text += f"\n{res.synopsis}"
    keyb = [
        [InlineKeyboardButton("More Information", url=f"https://myanimelist.net/manga/{manga_id}")]
    ]
    
    msg.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyb))


__help__ = """
Get information about anime and manga with the help of this module! All data is fetched from [MyAnimeList](https://myanimelist.net).
*Available commands:*
 - /anime <anime>: returns information about the anime.
 - /manga <manga>: returns information about the manga.
 """


__mod_name__ = "MyAnimeList"


ANIME_HANDLER = DisableAbleCommandHandler("anime", search_anime, pass_args=True)
MANGA_HANDLER = DisableAbleCommandHandler("manga", search_manga, pass_args=True)

dispatcher.add_handler(ANIME_HANDLER)
dispatcher.add_handler(MANGA_HANDLER)
