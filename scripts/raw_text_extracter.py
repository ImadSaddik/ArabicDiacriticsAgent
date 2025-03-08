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
