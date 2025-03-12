# Arabic diacritics agent

Training text to speech models on the Arabic language can be challenging. In Arabic, we have something called diacritics, these are symbols like fatha ( َ ), damma ( ُ ), kasra ( ِ ), and sukoon ( ْ ) that are placed above or below letters to indicate pronunciation.

Unlike many other languages, Arabic writing typically omits these diacritics in everyday texts, which can create ambiguity in pronunciation and meaning. This poses a significant challenge for training text-to-speech (TTS) models, as they rely on accurate phonetic representations to produce natural-sounding speech.

That's why I created this agent to add diacritics to raw Arabic text and make TTS models more accurate.

## The challenge of diacritic restoration  

Since most Arabic texts are written without diacritics, a TTS model must either infer them automatically or be trained on fully diacritized datasets. Manually annotating large corpora with diacritics is time-consuming and expensive. Moreover, diacritic restoration is not a trivial task, many words in Arabic can have different meanings and pronunciations depending on their diacritization. For example:

- (kataba) كَتَبَ means "he wrote"
- (kutub) كُتُبْ means "books"
- (kutiba) كُتِبَ means "it was written"

A TTS model without proper diacritic restoration may produce incorrect pronunciations, leading to unnatural or even misleading speech synthesis.  

## Pipeline

![pipeline](/images/pipeline.png)

Our pipeline can process two types of input: YouTube videos or audio files.  

1. **Extracting Text**  
   - If the YouTube video has subtitles, we take them and clean them by removing things like [music] and other non-speech captions.  
   - If there are no subtitles, we use a Speech-to-Text model to generate the text.  
   - At the end of this step, we have the Arabic text, but it has no diacritics.  

2. **Adding Diacritics**  
   - A language model (LLM) adds diacritics to the text.  
   - Another LLM reviews the output and checks if it looks correct.  
   - If the output is not good, we ask the first LLM to try again.  

3. **Preparing the Data**  
   - Once the text is correctly diacritized, we split the audio into smaller parts.  
   - This is necessary because training models on large audio files is difficult.  

At the end of the process, we have diacritized text and segmented audio, ready for training.
