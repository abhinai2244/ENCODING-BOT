

import asyncio
import math
import time

from .. import PROGRESS


async def progress_for_pyrogram(current, total, ud_type, message, start):
    now = time.time()
    diff = now - start
    if round(diff % 5.00) == 0 or current == total:
        try:
            percentage = current * 100 / total
            speed = current / diff
            elapsed_time = round(diff)
            time_to_completion = round((total - current) / speed)
            estimated_total_time = elapsed_time + time_to_completion
            elapsed_time = TimeFormatter(seconds=elapsed_time)
            estimated_total_time = TimeFormatter(seconds=estimated_total_time)
            progress = "{0}{1}".format(
                ''.join(["█" for i in range(math.floor(percentage / 10))]),
                ''.join(["░" for i in range(10 - math.floor(percentage / 10))])
            )
            tmp = progress + PROGRESS.format(
                humanbytes(current),
                humanbytes(total),
                humanbytes(speed) + "/s",
                estimated_total_time if estimated_total_time != '...' else "Calculating"
            )
            await message.edit(
                text="{}\n{}".format(
                    ud_type,
                    tmp
                )
            )
        except Exception:
            pass


async def progress_for_url(downloader, msg):
    total_length = downloader.filesize if downloader.filesize else 0
    downloaded = downloader.get_dl_size()
    speed = downloader.get_speed(human=True)
    estimated_total_time = downloader.get_eta(human=True)
    percentage = downloader.get_progress() * 100
    progress = "{0}{1}".format(
        ''.join(["█" for i in range(math.floor(percentage / 10))]),
        ''.join(["░" for i in range(10 - math.floor(percentage / 10))])
    )
    progress_str = "Downloading\n" + progress + PROGRESS.format(
        humanbytes(downloaded),
        humanbytes(total_length),
        speed,
        estimated_total_time)
    try:
        await msg.edit_text(progress_str)
    except Exception:
        pass


def humanbytes(size):
    """ humanize size """
    if not size:
        return ""
    power = 1024
    t_n = 0
    power_dict = {0: ' ', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
    while size > power:
        size /= power
        t_n += 1
    return "{:.2f} {}B".format(size, power_dict[t_n])


def TimeFormatter(seconds: float) -> str:
    """ humanize time """
    minutes, seconds = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "")
    return tmp[:-2]
