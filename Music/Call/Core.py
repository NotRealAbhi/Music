import yt_dlp
import os
from .Calls import CallHandler

TEMP_AUDIO_DIR = "temp_audio"
if not os.path.exists(TEMP_AUDIO_DIR):
    os.makedirs(TEMP_AUDIO_DIR)

class VoiceChatManager:
    def __init__(self, call_handler: CallHandler):
        self.call_handler = call_handler
        self.queue = {} # Queue per chat (chat_id: [track1, track2, ...])
        self.playing = {} # Currently playing per chat (chat_id: current_track_info)

    async def download_audio(self, query: str):
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': f'{TEMP_AUDIO_DIR}/%(title)s-%(id)s.%(ext)s',
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'auto',
            'cookiefile': 'cookies/cookies.txt',
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=True)
                if 'entries' in info:
                    info = info['entries'][0]
                audio_path = ydl.prepare_filename(info)
                title = info.get('title', 'Unknown')
                return audio_path, title
        except Exception as e:
            return None, f"Error downloading: {e}"

    async def enqueue(self, chat_id: int, query: str, requested_by: str):
        audio_path, title = await self.download_audio(query)
        if audio_path:
            if chat_id not in self.queue:
                self.queue[chat_id] = []
            self.queue[chat_id].append({"path": audio_path, "title": title, "requested_by": requested_by, "query": query})
            return f"Added '{title}' to the queue."
        else:
            return title

    async def play_next(self, chat_id: int):
        if chat_id in self.queue and self.queue[chat_id]:
            next_track = self.queue[chat_id].pop(0)
            self.playing[chat_id] = next_track
            await self.call_handler.play_audio(chat_id, next_track["path"], next_track["title"])
            return f"Now playing: {next_track['title']} (requested by {next_track['requested_by']})"
        else:
            if chat_id in self.call_handler.is_active and self.call_handler.is_active[chat_id]:
                await self.call_handler.leave_call(chat_id)
            if chat_id in self.playing:
                del self.playing[chat_id]
            return "Queue is empty. Leaving voice chat."

    async def skip(self, chat_id: int):
        if chat_id in self.call_handler.is_active and self.call_handler.is_active[chat_id]:
            await self.call_handler.stop_audio(chat_id) # Stop current
            return await self.play_next(chat_id)
        else:
            return "Nothing is playing to skip."

    async def stop(self, chat_id: int):
        if chat_id in self.call_handler.is_active and self.call_handler.is_active[chat_id]:
            await self.call_handler.stop_audio(chat_id)
            await self.call_handler.leave_call(chat_id)
        if chat_id in self.queue:
            self.queue[chat_id].clear()
        if chat_id in self.playing:
            del self.playing[chat_id]
        return "Playback stopped and queue cleared."

    def get_queue(self, chat_id: int):
        return self.queue.get(chat_id, [])

    def get_now_playing(self, chat_id: int):
        return self.playing.get(chat_id)

    async def pause(self, chat_id: int):
        await self.call_handler.pause_audio(chat_id)
        return "Playback paused."

    async def resume(self, chat_id: int):
        await self.call_handler.resume_audio(chat_id)
        return "Playback resumed."

    async def volume(self, chat_id: int, level: int):
        await self.call_handler.set_volume(chat_id, level)
        return f"Volume set to {level}%."

    # Implement other core logic (seek, etc.)
