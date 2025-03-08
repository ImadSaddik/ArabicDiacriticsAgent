import os

from dotenv import load_dotenv

from google import genai
from google.genai.types import GenerateContentConfig


class DiacriticsReviewer:
    def __init__(self, diacritized_text: str) -> None:
        load_dotenv()

        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "gemini-2.0-pro-exp-02-05"
        self.system_prompt = self._get_system_prompt()
        self.diacritized_text = diacritized_text

    def process_captions(self) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=self.diacritized_text,
            config=GenerateContentConfig(
                system_instruction=[
                    self.system_prompt
                ]
            )
        )
        return response.text

    def _get_system_prompt(self) -> str:
        return """You are an expert in Arabic linguistics with a strong command of grammar, syntax, and diacritics. Your task is to evaluate the diacritized Arabic text provided from the previous step, ensuring the diacritics are applied correctly and appropriately based on the context of each sentence.

Your evaluation should address:
1. **Correctness:** Are the diacritics applied in line with the grammar rules and the context?
2. **Consistency:** Are the diacritics applied consistently across similar words throughout the text?

Return the result as a JSON object using the following schema:

Decision = {'decision': bool}
Return: Decision

Example:

- Correct text:
اِسْمَعْ أَيُّهَا الإِنْسَانُ، وَشَاهِدْ وَتَمَعَّنْ أَيُّهَا الْمَوْصُوفُ بِالْعَقْلِ وَالْحِكْمَةِ. الْحَيَاةُ مُعْجِزَةٌ ظَهَرَتْ مُنْذُ أَرْبَعَةِ مَلَايِينِ مِنَ الأَعْوَامِ، وَنَحْنُ بَنِي الإِنْسَانِ لَمْ يَمْضِ عَلَى وُجُودِنَا سِوَى بِضْعَةِ آلافٍ مِنَ الأَعْوَامِ. إِنَّهَا حُقْبَةٌ قَصِيرَةٌ، لَكِنَّهَا كَانَتْ كَافِيَةً لاِخْتِلالِ تَوَازُنِ أَرْضِنَا حَتَّى بَاتَتْ حَيَاتُنَا عَلَى كَوْكَبِنَا الأَزْرَقِ مُهَدَّدَةً بِالزَّوَالِ. اِسْتَمِعُوا إِلَى هَذِهِ الْحِكَايَةِ، حِكَايَتِنَا، حِكَايَةُ الأَرْضِ.

Return {'decision': true}

- Incorrect text:
اسمع أيها الانسان، وشاهد وتمعن أيها الموصوف بالعقل والحكمة. الحياة معجزة ظهرت منذ أربعة ملايين من الأعوام، ونحن بني الانسان لم يمض على وجودنا سوى بضعة آلاف من الأعوام. إنها حقبة قصيرة، لكنها كانت كافية لاختلال توازن أرضنا حتى باتت حياتنا على كوكبنا الأزرق مهددة بالزوال. استمعوا إلى هذه الحكاية، حكايتنا، حكاية الأرض.

Return {'decision': false}
"""
