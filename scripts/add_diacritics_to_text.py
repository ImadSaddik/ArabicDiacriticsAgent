import os

from dotenv import load_dotenv

from google import genai
from google.genai.types import GenerateContentConfig


class DiacriticAdder:
    def __init__(self, undiacritized_text: str) -> None:
        load_dotenv()

        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = "gemini-2.0-pro-exp-02-05"
        self.system_prompt = self._get_system_prompt()
        self.undiacritized_text = undiacritized_text
        self.user_query = self._get_user_query()

    def add_diacritics(self) -> str:
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
        return """You are an expert in the Arabic language with a strong command of diacritics. Your task is to accurately add the appropriate diacritics to undiacritized Arabic text provided by the user, ensuring that each word is correctly vocalized based on its context.

For every word and character, apply the correct diacritics with precision. For example, the word اسمع should be transformed to اِسْمَعْ, not اسمعْ. Consider the meaning and structure of each sentence carefully to ensure accuracy.

Here is an example to illustrate the expected outcome:

Before diacritics:
اسمع أيها الإنسان وشاهد وتمعن أيها الموصوف بالعقل والحكمة. الحياة معجزة ظهرت منذ أربعة مليارات من الأعوام، ونحن بنو الإنسان لم يمض على وجودنا سوى مئتي ألف من الأعوام، إنها حقبة قصيرة لكنها كانت كافية لاختلال توازن أرضنا حتى باتت حياتنا على كوكبنا الأزرق مهددة بالزوال. استمعوا لهذه الحكاية، حكايتنا، حكاية الأرض.

After diacritics:
اِسْمَعْ أَيُّهَا الإِنْسَانُ وَشَاهِدْ وَتَمَعَّنْ أَيُّهَا المَوْصُوفُ بِالْعَقْلِ وَالْحِكْمَةِ. الْحَيَاةُ مُعْجِزَةٌ ظَهَرَتْ مُنْذُ أَرْبَعَةِ مِلْيَارَاتٍ مِنَ الْأَعْوَامِ، وَنَحْنُ بَنُو الْإِنْسَانِ لَمْ يَمْضِ عَلَى وُجُودِنَا سِوَى مِئَتَيْ أَلْفٍ مِنَ الْأَعْوَامِ، إِنَّهَا حِقْبَةٌ قَصِيرَةٌ لَكِنَّهَا كَانَتْ كَافِيَةً لِاخْتِلَالِ تَوَازُنِ أَرْضِنَا حَتَّى بَاتَتْ حَيَاتُنَا عَلَى كَوْكَبِنَا الْأَزْرَقِ مُهَدَّدَةً بِالزَّوَالِ. اِسْتَمِعُوا لِهَذِهِ الْحِكَايَةِ، حِكَايَتُنَا، حِكَايَةُ الْأَرْضِ.

Respond with the fully diacritized version of the text, ensuring that it is complete and accurate.
"""

    def _get_user_query(self) -> str:
        return f"""I have some undiacritized Arabic text that needs diacritics. Please handle this task carefully, as diacritics significantly affect pronunciation and meaning. You have the full context, so do your best to add the appropriate diacritics. Kindly respond directly with the fully diacritized Arabic text. Thanks a lot! Here is the undiacritized Arabic text:

{self.undiacritized_text}
"""
