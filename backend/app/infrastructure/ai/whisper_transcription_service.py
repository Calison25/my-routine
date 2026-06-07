import openai


class AudioTranscriptionService:
    """Adapter para transcrição de áudio usando OpenAI Whisper."""

    def __init__(self, api_key: str) -> None:
        self._client = openai.AsyncOpenAI(api_key=api_key)

    async def transcribe(self, audio_bytes: bytes, filename: str) -> str:
        response = await self._client.audio.transcriptions.create(
            model="whisper-1",
            file=(filename, audio_bytes),
        )
        return response.text
