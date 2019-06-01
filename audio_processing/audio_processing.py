# -*- coding: utf-8 -*-

import os
from pydub import AudioSegment

vocabulary = "аеёиоуыэюябвгджзйклмнпрстфхцчшщьъ-"
vowels = "аеёиоуыэюя"


class WordContain:
    isStress = False
    dbDiff = 0
    lenDiff = 0
    crossFade = 0

def find_phoneme(phoneme, dest):
    return AudioSegment.from_file(dest + phoneme + ".wav")


def speed_change(sound, speed=1.0):
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
         "frame_rate": int(sound.frame_rate * speed)
      })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)



def work_with_syllables(input_text_list):
    dest = os.getcwd() + "/static/sounds/all/"

    one_big_phoneme = AudioSegment.empty()
    silence = AudioSegment.silent(duration=250)

    for i in range(len(input_text_list)):
        analyze_counter = 0
        analyze_list = analyze(input_text_list[i])
        if i != 0:
            one_big_phoneme = one_big_phoneme.append(silence)
        for j in range(len(input_text_list[i])):
            if input_text_list[i][j][0] in vocabulary:
                phoneme = find_phoneme(input_text_list[i][j], dest)
                one_big_phoneme = phoneme_pre_processing(phoneme, analyze_list[analyze_counter], one_big_phoneme)
                analyze_counter += 1

    one_big_phoneme = speed_change(one_big_phoneme, 0.96)
    return one_big_phoneme


def phoneme_pre_processing(phoneme, analyze_info, one_big_phoneme):
    if len(phoneme)*analyze_info.lenDiff < analyze_info.crossFade:
        analyze_info.crossFade = len(phoneme)*analyze_info.lenDiff * 0.9

    return one_big_phoneme.append(phoneme[-(len(phoneme)*analyze_info.lenDiff):] - analyze_info.dbDiff, crossfade=analyze_info.crossFade)


def analyze(syllables_list):
    # syllables_list = ['ве', 'ли', '\'', 'ка', 'я']
    analyze_list = []
    prev_stress = False
    factor = 0

    if len(syllables_list) == 1:
        wc = WordContain()
        if not syllables_list[0] == 'ь' and not syllables_list[0] == 'ъ':
            wc.dbDiff = 5

        analyze_list.append(wc)
        return analyze_list

    stressed = 0
    for i in range(len(syllables_list)):
        if syllables_list[i][0] not in vocabulary:
            stressed = 1
            break

    if len(syllables_list) == 2 and stressed == 1:
        wc = WordContain()
        analyze_list.append(wc)
        return analyze_list

    for i in range(stressed, len(syllables_list)):
        if syllables_list[i][0] in vocabulary:

            only_consonants = True
            for j in range(len(syllables_list[i - 1 + factor])):
                if syllables_list[i - 1 + factor][j] in vowels:
                    only_consonants = False
                    break

            wc = WordContain()
            if prev_stress:
                if only_consonants:
                    wc.lenDiff = 1 #0.5
                else:
                    wc.lenDiff = 1 #0.7
                wc.crossFade = 35 #75
                wc.dbDiff = 5
                analyze_list.append(wc)
                prev_stress = False
            else:
                wc.dbDiff = 5
                if only_consonants:
                    wc.lenDiff = 1 # 0.5
                else:
                    wc.lenDiff = 1 # 0.9
                if stressed == 1:
                    if i != 1:
                        wc.crossFade = 35 # 300
                else:
                    if i != 0:
                        wc.crossFade = 35 # 300
                analyze_list.append(wc)
        else:
            wc = WordContain()
            if stressed == 1:
                if i != 1:
                    wc.crossFade = 35  # 300
            else:
                if i != 0:
                    wc.crossFade = 35  # 300
            wc.dbDiff = -1
            wc.lenDiff = 1
            wc.isStress = True
            prev_stress = True
            factor = 1
            analyze_list.append(wc)
    return analyze_list
