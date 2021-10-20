
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import os
import asyncio
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.raw.functions.messages import UpdatePinnedMessage


stoptimer = False


@bot.on_message(filters.command('settimer'))
async def set_timer(client, message):
    global stoptimer
    try:
        if message.chat.id>0:
            return await message.reply('⛔️ Try this command in a **group chat**.')
        elif not (await client.get_chat_member(message.chat.id,message.from_user.id)).can_manage_chat:
            return await message.reply('👮🏻‍♂️ Sorry, **only admins** can execute this command.')    
        elif len(message.command)<3:
            return await message.reply('❌ **Incorrect format.**\n\n✅ Format should be like,\n<code> /set seconds "event"</code>\n\n**Example**:\n <code>/set 86400 "TIME LEFT UNTIL NEW YEAR"</code>')    
        else:
            user_input_time = int(message.command[1])
            user_input_event = str(message.command[2])
            get_user_input_time = await bot.send_message(message.chat.id, user_input_time)
            await get_user_input_time.pin()
            if stoptimer: stoptimer = False
            if 0<user_input_time<=10:
                while user_input_time and not stoptimer:
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**s**\n\n<i>"Your **Time** Is Limited, So Don\'t Waste It Living Someone Else\'s Life"</i>\n      - Steve Jobs'.format(user_input_event, s)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(1)
                    user_input_time -=1
                await finish_countdown.edit("🚨 Beep! Beep!! **TIME'S UP!!!**")
            elif 10<user_input_time<60:
                while user_input_time>0 and not stoptimer:
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**s**\n\n<i>"Your **Time** Is Limited, So Don\'t Waste It Living Someone Else\'s Life"</i>\n      - Steve Jobs'.format(user_input_event, s)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(3)
                    user_input_time -=3
                await finish_countdown.edit("🚨 Beep! Beep!! **TIME'S UP!!!**")
            elif 60<=user_input_time<3600:
                while user_input_time>0 and not stoptimer:
                    m=user_input_time%3600//60
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**m** : {:02d}**s**\n\n<i>"Your **Time** Is Limited, So Don\'t Waste It Living Someone Else\'s Life"</i>\n      - Steve Jobs'.format(user_input_event, m, s)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(3)
                    user_input_time -=3
                await finish_countdown.edit("🚨 Beep! Beep!! **TIME'S UP!!!**")
            elif 3600<=user_input_time<86400:
                while user_input_time>0 and not stoptimer:
                    h=user_input_time%(3600*24)//3600
                    m=user_input_time%3600//60
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**h** : {:02d}**m** : {:02d}**s**\n\n<i>"Your **Time** Is Limited, So Don\'t Waste It Living Someone Else\'s Life"</i>\n      - Steve Jobs'.format(user_input_event, h, m, s)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(7)
                    user_input_time -=7
                await finish_countdown.edit("🚨 Beep! Beep!! **TIME'S UP!!!**")
            elif user_input_time>=86400:
                while user_input_time>0 and not stoptimer:
                    d=user_input_time//(3600*24)
                    h=user_input_time%(3600*24)//3600
                    m=user_input_time%3600//60
                    s=user_input_time%60
                    Countdown_TeLe_TiPs='{}\n\n⏳ {:02d}**d** : {:02d}**h** : {:02d}**m** : {:02d}**s**\n\n<i>"Your **Time** Is Limited, So Don\'t Waste It Living Someone Else\'s Life"</i>\n      - Steve Jobs'.format(user_input_event, d, h, m, s)
                    finish_countdown = await get_user_input_time.edit(Countdown_TeLe_TiPs)
                    await asyncio.sleep(9)
                    user_input_time -=9
                await finish_countdown.edit("🚨 Beep! Beep!! **TIME'S UP!!!**")
            else:
                await get_user_input_time.edit(f"🤷🏻‍♂️ I can't countdown from {user_input_time}")
                await get_user_input_time.unpin()
    except FloodWait as e:
        await asyncio.sleep(e.x)

@bot.on_message(filters.command('stoptimer'))
async def stop_timer(Client, message):
    global stoptimer
    try:
        if (await bot.get_chat_member(message.chat.id,message.from_user.id)).can_manage_chat:
            stoptimer = True
            await message.reply('🛑 Countdown stopped.')
        else:
            await message.reply('👮🏻‍♂️ Sorry, **only admins** can execute this command.')
    except FloodWait as e:
        await asyncio.sleep(e.x)

print("Countdown Timer is alive!")
