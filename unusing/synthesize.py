# -*- coding: utf-8 -*-

import re
import unicodedata

from pydub import AudioSegment

data_set_path = "/Users/ilya_lobanov/Desktop/звуки/all/"
dest_path = "/Users/ilya_lobanov/Desktop/processed/"

vocabulary = "аеёиоуыэюябвгджзйклмнпрстфхцчшщьъ-"
consonants = "бвгджзйклмнпрстфхцчшщьъ"
vowels = "аеёиоуыэюя"


def de_accent(some_unicode_string):
    return u''.join(c for c in unicodedata.normalize('NFD', some_unicode_string)
                    if unicodedata.category(c) != 'Mn')


def text_normalize(text):
    text = de_accent(text)
    text = text.lower()
    text = re.sub("[^{}]".format(vocabulary), "", text)
    return text


def start_process(input_text):
    input_text = text_normalize(input_text)
    allophones = str.split(input_text, "-")
    phonemes = []

    for i in range(len(allophones)):
        phoneme = find_phoneme(allophones[i])
        phoneme = phoneme_pre_processing(phoneme, allophones[i])
        phonemes.append(phoneme)

    result = append_phonemes(phonemes)

    norm_name = glue_the_text(allophones)
    save_path = dest_path + norm_name + ".wav"
    result.export(save_path, format="wav")
    print("Аудиозапись сохранена по пути: ", save_path)


def append_phonemes(phonemes):
    result = AudioSegment.empty()

    if len(phonemes) == 1:
        return phonemes[0]

    if len(phonemes) == 2:
        return phonemes[0].append(phonemes[1], 0)

    for i in range(len(phonemes)):
        if i == 0:
            result = phonemes[i].append(phonemes[i+1], 0)
        elif i == len(phonemes) - 1:
            result = result.append(phonemes[i], 0)
        elif i == 1:
            continue
        else:
            result = result.append(phonemes[i], 0)
    return result


def phoneme_pre_processing(phoneme, phoneme_name, silence_threshold=-50.0, chunk_size=10):
    result = AudioSegment.empty()
    sound_size = len(phoneme)
    assert chunk_size > 0  # to avoid infinite loop
    stop_size = 0
    start_size = 0
    outside = False

    if len(phoneme_name) == 1:
        if len(re.sub("[^{}]".format(consonants), "", phoneme_name)) == len(phoneme_name):
            start_size = sound_size * 0.3
            stop_size = sound_size * 0.7
            outside = True
        else:
            start_size = sound_size * 0.1
            stop_size = sound_size * 0.60

    if len(phoneme_name) > 1:
        if phoneme_name[0] in consonants:
            stop_size = sound_size * 0.65
            start_size = sound_size * 0.07

        elif phoneme_name[0] in vowels:
            start_size = sound_size * 0.2
            stop_size = sound_size * 0.7

    trim_ms = start_size  # ms

    if not outside:
        while trim_ms < stop_size:
            trim_ms += chunk_size
            if phoneme[trim_ms:trim_ms + chunk_size].dBFS >= silence_threshold:
                result = result.append(phoneme[trim_ms:trim_ms + chunk_size], 0)
    else:
        trim_ms = 20
        while trim_ms < start_size:
            trim_ms += chunk_size
            if phoneme[trim_ms:trim_ms + chunk_size].dBFS >= silence_threshold:
                result = result.append(phoneme[trim_ms:trim_ms + chunk_size], 0)
        while stop_size < sound_size * 0.9:
            stop_size += chunk_size
            if phoneme[stop_size:stop_size + chunk_size].dBFS >= silence_threshold:
                result = result.append(phoneme[stop_size:stop_size + chunk_size], 0)

    return result


def find_phoneme(phoneme):
    return AudioSegment.from_file(data_set_path + phoneme + ".wav")


def glue_the_text(phonemes):
    result = ""
    for i in range(len(phonemes)):
        result += phonemes[i]
    return result
