

import os
import time

from ... import app, download_dir, log
from ..database.access_db import db
from ..display_progress import progress_for_pyrogram
from ..encoding import get_duration, get_thumbnail, get_width_height


async def upload_to_tg(new_file, message, msg):
    # Variables
    c_time = time.time()
    filename = os.path.basename(new_file)
    duration = get_duration(new_file)

    # Thumbnail Logic
    custom_thumb = await db.get_thumbnail(message.from_user.id)
    if custom_thumb:
        thumb = await app.download_media(custom_thumb, file_name=os.path.join(download_dir, str(time.time()) + ".jpg"))
    else:
        thumb = get_thumbnail(new_file, download_dir, duration / 4)

    width, height = get_width_height(new_file)
    # Handle Upload
    if await db.get_upload_as_doc(message.from_user.id) is True:
        link = await upload_doc(message, msg, c_time, filename, new_file)
    else:
        link = await upload_video(message, msg, new_file, filename,
                                  c_time, thumb, duration, width, height)

    # Cleanup custom thumb download if it was used/downloaded
    if custom_thumb and thumb and os.path.isfile(thumb):
        try:
            os.remove(thumb)
        except Exception:
            pass

    return link


async def upload_video(message, msg, new_file, filename, c_time, thumb, duration, width, height):
    resp = await message.reply_video(
        new_file,
        supports_streaming=True,
        parse_mode=None,
        caption=filename,
        thumb=thumb,
        duration=duration,
        width=width,
        height=height,
        progress=progress_for_pyrogram,
        progress_args=("Uploading ...", msg, c_time)
    )
    if resp:
        await app.send_video(log, resp.video.file_id, thumb=thumb,
                             caption=filename, duration=duration,
                             width=width, height=height, parse_mode=None)

    return resp.link


async def upload_doc(message, msg, c_time, filename, new_file):
    resp = await message.reply_document(
        new_file,
        caption=filename,
        progress=progress_for_pyrogram,
        progress_args=("Uploading ...", msg, c_time)
    )

    if resp:
        await app.send_document(log, resp.document.file_id, caption=filename, parse_mode=None)

    return resp.link
