from text_processing.dictionary import Preprocessing as prp
from audio_processing.synthesize import start_process

word_processing = prp()


class Controller:
    @staticmethod
    def process_text(input_text):
        return word_processing.process_input_text(input_text)

    @staticmethod
    def process_audio(input_text, list_of_syllables):
        return start_process(input_text, list_of_syllables)
