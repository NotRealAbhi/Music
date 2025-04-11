from pytgcalls import PyTgCalls
from pyrogram import Client
from pytgcalls.types import MediaStream, VideoQuality, AudioQuality
from pytgcalls.types.input_stream import InputAudio  # Updated import

class CallHandler:
    def __init__(self, client: Client):
        self.client = client
        self.pytgcalls = PyTgCalls(client)
        self.is_active = {}  # Track active calls per chat
        self.current_track = {} # Track current playing track per chat
        self.active_streams = {} # Track active MediaStream objects

    async def start(self):
        await self.pytgcalls.start()
        print("PyTgCalls started!")

    async def join_call(self, chat_id: int):
        if chat_id not in self.is_active or not self.is_active[chat_id]:
            await self.pytgcalls.join_group_call(chat_id)
            self.is_active[chat_id] = True

    async def leave_call(self, chat_id: int):
        if chat_id in self.is_active and self.is_active[chat_id]:
            await self.pytgcalls.leave_group_call(chat_id)
            self.is_active[chat_id] = False
            if chat_id in self.current_track:
                del self.current_track[chat_id]
            if chat_id in self.active_streams:
                stream = self.active_streams[chat_id]
                await stream.stop()
                del self.active_streams[chat_id]

    async def play_audio(self, chat_id: int, path: str, title: str = "Playing"):
        await self.join_call(chat_id)
        audio_stream = InputAudio(path)  # Using InputAudio
        await self.pytgcalls.play_media(chat_id, audio_stream)
        self.current_track[chat_id] = {"title": title, "path": path}
        self.active_streams[chat_id] = audio_stream # Store the stream object

    async def stop_audio(self, chat_id: int):
        if chat_id in self.active_streams:
            stream = self.active_streams[chat_id]
            await stream.stop()
            del self.active_streams[chat_id]
        await self.leave_call(chat_id)

    async def pause_audio(self, chat_id: int):
        if chat_id in self.active_streams:
            await self.pytgcalls.pause(chat_id)  # Using the renamed method

    async def resume_audio(self, chat_id: int):
        if chat_id in self.active_streams:
            await self.pytgcalls.resume(chat_id)  # Using the renamed method

    async def set_volume(self, chat_id: int, volume: int):
        await self.pytgcalls.change_stream_volume(chat_id, volume / 100)

    async def get_playback_status(self, chat_id: int):
        if chat_id in self.pytgcalls.call_info:
            return self.pytgcalls.call_info[chat_id].capture  # Using the renamed field
        return None

    # Example of using VideoQuality and AudioQuality (you'll need to adapt this
    # based on how you handle video playback if you implement it)
    async def play_video(self, chat_id: int, video_path: str, audio_path: str):
        await self.join_call(chat_id)
        video_quality = VideoQuality(height=720, width=1280)
        audio_quality = AudioQuality(bitrate=128)
        media_stream = MediaStream(
            video=video_path,
            audio=audio_path,
            video_quality=video_quality,
            audio_quality=audio_quality
        )
        await self.pytgcalls.play_media(chat_id, media_stream)
        # ... other video playback related logic
