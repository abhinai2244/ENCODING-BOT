import asyncio
from asyncio import Event, wait_for
from time import time

from pyrogram.types import CallbackQuery

from ..utils.button_maker import ButtonMaker
from ..utils.display_progress import TimeFormatter
from .. import LOGGER

# Global registry for active sessions
sessions = {}

class AudioSelect:
    def __init__(self, client, message):
        self._is_cancelled = False
        self._reply = None
        self._time = time()
        self.client = client
        self.message = message
        self.aud_streams = {}
        self.event = Event()
        self.streams = -1
        self.stream_view_msg = None

    async def get_buttons(self, streams):
        self.streams = streams
        for stream in self.streams:
            if stream.get('codec_type') == 'audio':
                index = stream.get('index')
                tags = stream.get('tags', {})
                self.aud_streams[index] = {
                    'map': index,
                    'title': tags.get('title'),
                    'lang': tags.get('language')
                }

        if not self.aud_streams or len(self.aud_streams) < 2:
            LOGGER.info("AudioSelect: Not enough audio streams")
            return -1, -1

        user_id = self.message.from_user.id
        sessions[user_id] = self
        LOGGER.info(f"AudioSelect: Registered session for user {user_id}")

        try:
            # Send the initial message
            await self._send_message()

            LOGGER.info("AudioSelect: Waiting for event")
            await wait_for(self.event.wait(), timeout=180)
            LOGGER.info("AudioSelect: Event set or timeout reached")

        except asyncio.TimeoutError:
            LOGGER.warning("AudioSelect: Timeout")
            self._is_cancelled = True
        finally:
            if user_id in sessions:
                del sessions[user_id]
                LOGGER.info(f"AudioSelect: Unregistered session for user {user_id}")

        if self._is_cancelled:
            if self._reply:
                await self._reply.edit('Task has been cancelled!')
            return -1, -1

        if self._reply:
            await self._reply.delete()
        if self.stream_view_msg:
            await self.stream_view_msg.delete()

        maps = [i['map'] for i in self.aud_streams.values()]
        LOGGER.info(f"AudioSelect: Returning maps {maps}")
        return maps, self.aud_streams

    async def _send_message(self):
        buttons = ButtonMaker()
        text = f"<b>CHOOSE AUDIO STREAM TO SWAP</b>\n\n<b>Audio Streams: {len(self.aud_streams)}</b>"
        for index, stream in self.aud_streams.items():
            buttons.button_data(f"{stream['lang'] or 'und'} | {stream['title'] or 'No Title'}", f"audiosel none {index}")
            buttons.button_data("▲", f"audiosel up {index}")
            buttons.button_data("⇅", f"audiosel swap {index}")
            buttons.button_data("▼", f"audiosel down {index}")
        buttons.button_data('Done', 'audiosel done', 'footer')
        buttons.button_data('Cancel', 'audiosel cancel', 'footer')

        if not self._reply:
            self._reply = await self.message.reply(text, reply_markup=buttons.build_menu(4))
        else:
            await self._reply.edit(text, reply_markup=buttons.build_menu(4))
        await self._create_streams_view()

    async def _create_streams_view(self):
        text = f"<b>STREAMS ORDER</b>"
        for index, stream in self.aud_streams.items():
            text += f"\n{stream['lang'] or 'und'} | {stream['title'] or 'No Title'}"
        text += f'\n\nTime Out: {TimeFormatter(180 - (time()-self._time))}'

        if self.stream_view_msg and self.stream_view_msg.text != text:
            await self.stream_view_msg.edit(text)
        elif not self.stream_view_msg:
             self.stream_view_msg = await self.message.reply(text)

    async def resolve_callback(self, query: CallbackQuery):
        LOGGER.info(f"AudioSelect: Received callback {query.data}")
        data = query.data.split()
        cmd = data[1]

        if cmd == 'cancel':
            self._is_cancelled = True
            self.event.set()
            await query.answer()
            return
        elif cmd == 'done':
            self.event.set()
            await query.answer()
            return
        elif cmd == 'none':
            await query.answer("This is just a label")
            return

        await query.answer()

        try:
            target_idx = int(data[2])
        except (IndexError, ValueError):
            LOGGER.error("AudioSelect: Invalid index in callback data")
            return

        aud_list = list(self.aud_streams.keys())

        if target_idx not in aud_list:
            LOGGER.error(f"AudioSelect: Index {target_idx} not in aud_list {aud_list}")
            return

        pos = aud_list.index(target_idx)
        LOGGER.info(f"AudioSelect: Processing {cmd} for index {target_idx} at pos {pos}")

        if cmd == 'swap':
            if pos != 0:
                # Swap with previous
                temp = aud_list[pos]
                aud_list[pos] = aud_list[pos-1]
                aud_list[pos-1] = temp
        elif cmd == 'up':
            if pos != 0:
                aud_list.insert(pos-1, aud_list.pop(pos))
        elif cmd == 'down':
            if pos != len(aud_list)-1:
                aud_list.insert(pos+1, aud_list.pop(pos))

        # Reconstruct dict in new order
        new_aud_streams = {}
        for aud in aud_list:
            new_aud_streams[aud] = self.aud_streams[aud]
        self.aud_streams = new_aud_streams

        if not self._is_cancelled:
            await self._send_message()
        else:
            self.event.set()
