

from ..database.access_db import db
from .drive.upload import Uploader
from .telegram import upload_to_tg


async def upload_worker(new_file, message, msg):
    if await db.get_drive(message.from_user.id):
        link = await Uploader().upload_to_drive(new_file, message, msg)
    else:
        link = await upload_to_tg(new_file, message, msg)
    return link
