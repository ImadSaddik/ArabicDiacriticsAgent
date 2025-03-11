import torch
import whisper

from pytubefix import YouTube


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
        self.model = whisper.load_model('turbo')

    def extract_captions(self) -> str:
        self.download_audio_from_youtube(self.video_url)
        result = self.model.transcribe(
            audio="../audio/audio.mp3", language="ar")
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
