# -*- coding: utf-8 -*-
import os
import re
import datetime

from pydub import AudioSegment

from audio_processing.audio_processing import work_with_syllables

vocabulary = "аеёиоуыэюябвгджзйклмнпрстфхцчшщьъ-"
consonants = "бвгджзйклмнпрстфхцчшщьъ"
vowels = "аеёиоуыэюя"


def start_process(input_text, input_text_list):

    # [["п", "ри", "ве", "'", "т"], ["к", "то"], ["ты"], ["?"]]

    print("in start_process, input_text: " + str(input_text_list))
    curr_dir_name = datetime.datetime.now().strftime("%Y-%m-%d")
    print("new dir name: " + curr_dir_name)
    if not os.path.exists("generated_audios/" + curr_dir_name):
        print("creating dir: " + curr_dir_name)
        os.mkdir("generated_audios/" + curr_dir_name)
    print("dir ok!")
    result = work_with_syllables(input_text_list)

    norm_name = create_name(input_text)
    save_path = os.getcwd() + "/generated_audios/" + curr_dir_name + "/" + norm_name + ".wav"
    result.export(save_path, format="wav")
    print("Аудиозапись сохранена по пути: ", save_path)

    return save_path, norm_name


def create_name(input_text):
    norm_name = input_text.replace(" ", "_")
    if len(norm_name) > 20:
        norm_name = norm_name[:40]
    return norm_name


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


def find_phoneme(phoneme, dest):
    return AudioSegment.from_file(dest + phoneme + ".wav")


def glue_the_text(phonemes):
    result = ""
    for i in range(len(phonemes)):
        result += phonemes[i]
    return result
