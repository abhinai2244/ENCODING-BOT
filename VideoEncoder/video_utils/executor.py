from __future__ import annotations

from ast import literal_eval
from asyncio import Event
from time import time

async def get_metavideo(video_file):
    stdout, stderr, rcode = await cmd_exec([
        'ffprobe',
        '-hide_banner',
        '-print_format', 'json',
        '-show_format',
        '-show_streams',
        video_file
    ])
    if rcode != 0:
        LOGGER.error(stderr)
        return {}, {}
    metadata = literal_eval(stdout)
    return metadata.get('streams', {}), metadata.get('format', {})


class VidEcxecutor(FFProgress):
    def __init__(self, listener: task.TaskListener, path: str, gid: str, metadata=False):
        self.data = None
        self.event = Event()
        self.listener = listener
        self.path = path
        self.name = ''
        self.outfile = ''
        self.size = 0
        self._metadata = metadata
        self._up_path = path
        self._gid = gid
        self._start_time = time()
        self._files = []
        self._qual = {
            '1080p': '1920',
            '720p': '1280',
            '540p': '960',
            '480p': '854',
            '360p': '640',
        }
        super().__init__()
        self.is_cancel = False
