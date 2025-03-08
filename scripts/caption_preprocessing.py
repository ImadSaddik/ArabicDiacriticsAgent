import os

from dotenv import load_dotenv

from google import genai
from google.genai.types import GenerateContentConfig


class CaptionPreProcessor:
    def __init__(self, raw_captions: str) -> None:
        load_dotenv()

        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "gemini-2.0-pro-exp-02-05"
        self.system_prompt = self._get_system_prompt()
        self.raw_captions = raw_captions
        self.user_query = self._get_user_query()

    def process_captions(self) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=self.user_query,
            config=GenerateContentConfig(
                system_instruction=[
                    self.system_prompt
                ]
            )
        )
        return response.text

    def _get_system_prompt(self) -> str:
        return """You are a native Arabic speaker with a strong command of the language. Your task is to review and refine YouTube captions that were automatically generated for Arabic videos. As you go through the captions, please correct any mistakes you find, as automated transcription may contain errors, but stay as close as possible to the original text. Don't use diacritics, you should provide the user with raw Arabic text.

Additionally, remove any placeholders such as [موسيقى], [تصفيق], [ضحك], and similar tags, keeping only the spoken text.

Reply to the user directly with the corrected and cleaned-up captions. Try your best to reply with the full text before stopping the generation.
"""

    def _get_user_query(self) -> str:
        return f"""I have extracted captions from a YouTube video, and I need your help to merge them into a single, coherent sequence of text. Please correct any grammatical errors and improve sentence structure as needed, since automatic transcription can be unreliable. You have the full context, so feel free to adjust sentences for clarity and flow. Also, please answer directly with the corrected captions and don't use diacritics, I need just the raw Arabic text. Thanks in advance! Here are the captions for you to process:

{self.raw_captions}
"""
