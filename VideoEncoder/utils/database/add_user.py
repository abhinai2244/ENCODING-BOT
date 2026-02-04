

from pyrogram import Client
from pyrogram.types import Message

from ... import log
from .access_db import db


async def AddUserToDatabase(bot: Client, cmd: Message):
    if not await db.is_user_exist(cmd.from_user.id):
        await db.add_user(cmd.from_user.id)
        if log is not None:
            await bot.send_message(
                int(log),
                f"<b>New User</b> \n\n<a href=f'tg://user?id={cmd.from_user.id}'>{cmd.from_user.first_name}</a> started @{(await bot.get_me()).username}!!"
            )
