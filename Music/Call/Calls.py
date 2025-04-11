from pytgcalls import PyTgCalls
from pyrogram import Client
from pytgcalls.types import MediaStream, VideoQuality, AudioQuality

class CallHandler:
    def __init__(self, client: Client):
        self.client = client
        self.pytgcalls = PyTgCalls(client)
        self.active_calls = {}  # Track active Call objects per chat
        self.current_track = {} # Track current playing track per chat

    async def start(self):
        await self.pytgcalls.start()
        print("PyTgCalls started!")

    async def join_call(self, chat_id: int):
        if chat_id not in self.active_calls:
            call = await self.pytgcalls.join(chat_id)
            self.active_calls[chat_id] = call
            return call
        return self.active_calls[chat_id]

    async def leave_call(self, chat_id: int):
        if chat_id in self.active_calls:
            call = self.active_calls.pop(chat_id)
            await call.leave()
            if chat_id in self.current_track:
                del self.current_track[chat_id]

    async def play_audio(self, chat_id: int, path: str, title: str = "Playing"):
        call = await self.join_call(chat_id)
        media_stream = MediaStream(path, title=title)
        await call.play(media_stream)
        self.current_track[chat_id] = {"title": title, "path": path}

    async def play_video(self, chat_id: int, video_path: str, audio_path: str = None, video_quality: VideoQuality = None, audio_quality: AudioQuality = None):
        call = await self.join_call(chat_id)
        media_stream = MediaStream(
            video=video_path,
            audio=audio_path,
            video_quality=video_quality,
            audio_quality=audio_quality
        )
        await call.play(media_stream)
        self.current_track[chat_id] = {"title": "Playing Video", "path": video_path} # Update as needed

    async def stop_audio(self, chat_id: int):
        if chat_id in self.active_calls:
            call = self.active_calls[chat_id]
            await call.stop()
            if chat_id in self.current_track:
                del self.current_track[chat_id]

    async def pause_audio(self, chat_id: int):
        if chat_id in self.active_calls:
            await self.active_calls[chat_id].pause()

    async def resume_audio(self, chat_id: int):
        if chat_id in self.active_calls:
            await self.active_calls[chat_id].resume()

    async def set_volume(self, chat_id: int, volume: int):
        if chat_id in self.active_calls:
            await self.active_calls[chat_id].set_volume(volume / 100)

    async def get_playback_status(self, chat_id: int):
        if chat_id in self.active_calls:
            return self.active_calls[chat_id].playback_status
        return None

    async def change_stream(self, chat_id: int, path: str, title: str = "Playing"):
        """
        Changes the currently playing stream. This now uses the play() method.
        """
        if chat_id in self.active_calls:
            call = self.active_calls[chat_id]
            media_stream = MediaStream(path, title=title)
            await call.play(media_stream)
            self.current_track[chat_id] = {"title": title, "path": path}
        else:
            print(f"No active call in chat {chat_id} to change stream.")

    async def change_video_stream(self, chat_id: int, video_path: str, audio_path: str = None, video_quality: VideoQuality = None, audio_quality: AudioQuality = None):
        """
        Changes the currently playing video stream. This now uses the play() method.
        """
        if chat_id in self.active_calls:
            call = self.active_calls[chat_id]
            media_stream = MediaStream(
                video=video_path,
                audio=audio_path,
                video_quality=video_quality,
                audio_quality=audio_quality
            )
            await call.play(media_stream)
            self.current_track[chat_id] = {"title": "Changing Video", "path": video_path} # Update as needed
        else:
            print(f"No active call in chat {chat_id} to change video stream.")
