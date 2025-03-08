import torch

from pytubefix import YouTube
from transformers import pipeline


class YouTubeArabicCaptionExtractor:
    def __init__(self, video_url: str) -> None:
        self.video_url = video_url

    def extract_captions(self) -> str:
        youtube = YouTube(self.video_url)
        arabic_captions = youtube.captions['a.ar']
        if arabic_captions is None:
            raise ValueError("No Arabic captions found for this video.")

        captions_text = arabic_captions.generate_srt_captions()
        return captions_text


class WhisperArabicCaptionExtractor:
    def __init__(self, video_url: str) -> None:
        self.video_url = video_url

    def extract_captions(self) -> str:
        model_id = "openai/whisper-large-v3-turbo"
        pipe = pipeline(
            "automatic-speech-recognition",
            model=model_id,
            torch_dtype=torch.float16,
            device="cuda"
        )

        self.download_audio_from_youtube(self.video_url)
        result = pipe("../audio/audio.mp3", return_timestamps=True)
        captions_text = result["text"]
        return captions_text

    def download_audio_from_youtube(self, video_url: str) -> str:
        youtube = YouTube(video_url)
        audio_stream = youtube.streams.filter(
            adaptive=True,
            file_extension='mp4',
            only_audio=True
        ).order_by('abr').desc().first()
        audio_stream.download(filename="audio.mp3", output_path="../audio")
        return "audio.mp3"
