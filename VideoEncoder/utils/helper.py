

import asyncio
import os
import shutil

from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pySmartDL import SmartDL

from .. import all, everyone, owner, sudo_users, download_dir, encode_dir
from .database.access_db import db
from .display_progress import progress_for_url
from .encoding import encode, extract_subs
from .uploads import upload_worker

output = InlineKeyboardMarkup([
    [InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/akaza7902"),
     InlineKeyboardButton("RexBots", url="https://t.me/RexBots_Official")]
])

start_but = InlineKeyboardMarkup([
    [InlineKeyboardButton("sᴛᴀᴛs", callback_data="stats"), InlineKeyboardButton("Settings", callback_data="OpenSettings")],
    [InlineKeyboardButton("ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/akaza7902"), InlineKeyboardButton("RexBots", url="https://t.me/RexBots_Official")]])


async def check_chat(message, chat):
    ''' Authorize User! '''
    chat_id = message.chat.id
    user_id = message.from_user.id
    get_sudo = await db.get_sudo()
    get_auth = await db.get_chat()
    if user_id in owner or user_id == 885190545:
        title = 'God'
    elif user_id in sudo_users or chat_id in sudo_users:
        title = 'Sudo'
    elif chat_id in everyone or user_id in everyone:
        title = 'Auth'
    elif str(user_id) in get_sudo or str(chat_id) in get_sudo:
        title = 'Sudo'
    elif str(chat_id) in get_auth or str(user_id) in get_auth:
        title = 'Auth'
    else:
        title = None
    if title == 'God':
        return True
    if not chat == 'Owner':
        if title == 'Sudo':
            return True
        if chat == 'Both':
            if title == 'Auth':
                return True
    return None


async def handle_url(url, filepath, msg):
    downloader = SmartDL(url, filepath, progress_bar=False, threads=10)
    downloader.start(blocking=False)
    while not downloader.isFinished():
        await progress_for_url(downloader, msg)


async def handle_encode(filepath, message, msg, audio_map=None):
    if await db.get_hardsub(message.from_user.id):
        subs = await extract_subs(filepath, msg, message.from_user.id)
        if not subs:
            await msg.edit("Something went wrong while extracting the subtitles!")
            return
    new_file = await encode(filepath, message, msg, audio_map=audio_map)
    if new_file:
        await msg.edit("<code>Video Encoded, getting metadata...</code>")
        try:
            link = await upload_worker(new_file, message, msg)
            await msg.edit('Video Encoded Successfully! Link: {}'.format(link))
        except Exception as e:
            await msg.edit(f"Error while uploading: {e}")
            link = None

        # Immediate cleanup after upload
        try:
            os.remove(new_file)
            os.remove(filepath)
        except Exception:
            pass

    else:
        await message.reply("<code>Something wents wrong while encoding your file.</code>")
        try:
            os.remove(filepath)
        except Exception:
            pass
        link = None

    return link


async def handle_extract(archieve):
    # get current directory
    path = os.getcwd()
    archieve = os.path.join(path, archieve)
    cmd = [f'./extract', archieve]
    rio = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await rio.communicate()
    os.remove(archieve)
    return path


async def get_zip_folder(orig_path: str):
    if orig_path.endswith(".tar.bz2"):
        return orig_path.rsplit(".tar.bz2", 1)[0]
    elif orig_path.endswith(".tar.gz"):
        return orig_path.rsplit(".tar.gz", 1)[0]
    elif orig_path.endswith(".bz2"):
        return orig_path.rsplit(".bz2", 1)[0]
    elif orig_path.endswith(".gz"):
        return orig_path.rsplit(".gz", 1)[0]
    elif orig_path.endswith(".tar.xz"):
        return orig_path.rsplit(".tar.xz", 1)[0]
    elif orig_path.endswith(".tar"):
        return orig_path.rsplit(".tar", 1)[0]
    elif orig_path.endswith(".tbz2"):
        return orig_path.rsplit("tbz2", 1)[0]
    elif orig_path.endswith(".tgz"):
        return orig_path.rsplit(".tgz", 1)[0]
    elif orig_path.endswith(".zip"):
        return orig_path.rsplit(".zip", 1)[0]
    elif orig_path.endswith(".7z"):
        return orig_path.rsplit(".7z", 1)[0]
    elif orig_path.endswith(".Z"):
        return orig_path.rsplit(".Z", 1)[0]
    elif orig_path.endswith(".rar"):
        return orig_path.rsplit(".rar", 1)[0]
    elif orig_path.endswith(".iso"):
        return orig_path.rsplit(".iso", 1)[0]
    elif orig_path.endswith(".wim"):
        return orig_path.rsplit(".wim", 1)[0]
    elif orig_path.endswith(".cab"):
        return orig_path.rsplit(".cab", 1)[0]
    elif orig_path.endswith(".apm"):
        return orig_path.rsplit(".apm", 1)[0]
    elif orig_path.endswith(".arj"):
        return orig_path.rsplit(".arj", 1)[0]
    elif orig_path.endswith(".chm"):
        return orig_path.rsplit(".chm", 1)[0]
    elif orig_path.endswith(".cpio"):
        return orig_path.rsplit(".cpio", 1)[0]
    elif orig_path.endswith(".cramfs"):
        return orig_path.rsplit(".cramfs", 1)[0]
    elif orig_path.endswith(".deb"):
        return orig_path.rsplit(".deb", 1)[0]
    elif orig_path.endswith(".dmg"):
        return orig_path.rsplit(".dmg", 1)[0]
    elif orig_path.endswith(".fat"):
        return orig_path.rsplit(".fat", 1)[0]
    elif orig_path.endswith(".hfs"):
        return orig_path.rsplit(".hfs", 1)[0]
    elif orig_path.endswith(".lzh"):
        return orig_path.rsplit(".lzh", 1)[0]
    elif orig_path.endswith(".lzma"):
        return orig_path.rsplit(".lzma", 1)[0]
    elif orig_path.endswith(".lzma2"):
        return orig_path.rsplit(".lzma2", 1)[0]
    elif orig_path.endswith(".mbr"):
        return orig_path.rsplit(".mbr", 1)[0]
    elif orig_path.endswith(".msi"):
        return orig_path.rsplit(".msi", 1)[0]
    elif orig_path.endswith(".mslz"):
        return orig_path.rsplit(".mslz", 1)[0]
    elif orig_path.endswith(".nsis"):
        return orig_path.rsplit(".nsis", 1)[0]
    elif orig_path.endswith(".ntfs"):
        return orig_path.rsplit(".ntfs", 1)[0]
    elif orig_path.endswith(".rpm"):
        return orig_path.rsplit(".rpm", 1)[0]
    elif orig_path.endswith(".squashfs"):
        return orig_path.rsplit(".squashfs", 1)[0]
    elif orig_path.endswith(".udf"):
        return orig_path.rsplit(".udf", 1)[0]
    elif orig_path.endswith(".vhd"):
        return orig_path.rsplit(".vhd", 1)[0]
    elif orig_path.endswith(".xar"):
        return orig_path.rsplit(".xar", 1)[0]
    else:
        raise IndexError("File format not supported for extraction!")


def delete_downloads():
    dir = encode_dir
    dir2 = download_dir
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            try:
                os.remove(path)
            except PermissionError:
                pass
    for files in os.listdir(dir2):
        path = os.path.join(dir2, files)
        try:
            shutil.rmtree(path)
        except OSError:
            try:
                os.remove(path)
            except PermissionError:
                pass
