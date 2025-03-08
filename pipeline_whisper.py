import json
import time
import os

from scripts.add_diacritics_to_text import DiacriticAdder
from scripts.diacritics_reviewer import DiacriticsReviewer
from scripts.caption_preprocessing import CaptionPreProcessor
from scripts.raw_text_extracter import WhisperArabicCaptionExtractor


class Pipeline:
    def __init__(self, video_url: str, max_review_steps: int = 3) -> None:
        self.video_url = video_url
        self.captions = None
        self.diacritized_text = None
        self.max_review_steps = max_review_steps

        self.validate_parameters()

    def validate_parameters(self) -> None:
        print("Validating parameters...")
        assert self.max_review_steps > 0
        assert self.max_review_steps is not None
        assert self.video_url is not None
        print("Parameters validated successfully.")

    def run(self) -> None:
        print("Starting the pipeline")

        # Step 1: Extract captions
        print("Step 1: Extracting captions...")
        captions_extractor = WhisperArabicCaptionExtractor(self.video_url)
        self.captions = captions_extractor.extract_captions()
        print(f"Captions extracted: Length = {len(self.captions)}.")

        # Step 2: Preprocess captions
        print("Step 2: Preprocessing captions...")
        caption_preprocessor = CaptionPreProcessor(self.captions)
        self.captions = caption_preprocessor.process_captions()
        print("Captions preprocessing completed.")
        print("Sleeping for 60 seconds to allow for any potential API rate limits...")
        time.sleep(60)

        # Step 3: Add diacritics
        print("Step 3: Adding diacritics to the text...")
        diacritic_adder = DiacriticAdder(self.captions)
        self.diacritized_text = diacritic_adder.add_diacritics()
        print("Diacritics added successfully.")
        print("Sleeping for 60 seconds to allow for any potential API rate limits...")
        time.sleep(60)

        # Step 4: Review diacritics
        print("Step 4: Reviewing diacritics ...")
        diacritics_reviewer = DiacriticsReviewer(self.diacritized_text)
        for i in range(self.max_review_steps):
            print(f"Review step {i+1}...")
            decision = diacritics_reviewer.review_text()
            if decision["decision"]:
                print("Diacritics review passed.")
                break
            else:
                print("Diacritics review failed, retrying...")
                self.diacritized_text = diacritic_adder.add_diacritics()
                print(
                    "Sleeping for 60 seconds to allow for any potential API rate limits...")
                time.sleep(60)

        # Step 5: Save diacritized text to JSON file
        self.save_to_json()
        print("Pipeline execution completed.")

    def save_to_json(self):
        output_data = {
            "video_url": self.video_url,
            "diacritized_text": self.diacritized_text
        }
        file_path = "output.json"
        try:
            data = []
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, "r", encoding="utf-8") as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        print(
                            "Warning: Existing file is not valid JSON. Creating a new list.")
                        data = []

            if not isinstance(data, list):
                data = []

            data.append(output_data)
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print("Diacritized text appended to output.json.")
        except Exception as e:
            print(f"Error saving to JSON: {e}")


if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=K33kH58qE_I"
    pipeline = Pipeline(video_url)
    pipeline.run()
