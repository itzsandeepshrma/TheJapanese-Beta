from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream

# Initialize PyTgCalls client
tg_calls = PyTgCalls()

async def stream_to_voice(chat_id: int, file_path: str):
    """
    Stream a song to Telegram voice chat.
    :param chat_id: The ID of the group chat where the bot is added.
    :param file_path: The path to the audio file.
    """
    try:
        await tg_calls.join_group_call(
            chat_id,
            InputStream(InputAudioStream(file_path))
        )
        print(f"Streaming {file_path} to chat {chat_id}")
    except Exception as e:
        print(f"Error streaming audio: {e}")
