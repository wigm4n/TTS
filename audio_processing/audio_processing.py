# -*- coding: utf-8 -*-

import os
from pydub import AudioSegment
from text_processing.dictionary import Preprocessing as prp

vocabulary = "аеёиоуыэюябвгджзйклмнпрстфхцчшщьъ-"
vowels = "аеёиоуыэюя"
punctuation_marks = ",:;.-"
word_processing = prp()

class WordContain:
    isStress = False
    dbDiff = 0
    lenDiff = 0
    crossFade = 0


def find_phoneme(phoneme, dest):
    phoneme = phoneme.replace('й', 'j')
    phoneme = phoneme.replace('ё', 'u')
    phoneme = phoneme.replace('н', 'n')
    phoneme = phoneme.replace('к', 'k')
    print("trying to get: " + dest + phoneme + ".wav")
    return AudioSegment.from_file(dest + phoneme + ".wav")


def speed_change(sound, speed=1.0):
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    })
    return sound_with_altered_frame_rate.set_frame_rate(sound.frame_rate)


def work_with_syllables(input_text_list):

    dest = os.getcwd() + "/static/sounds/all/"

    one_big_phoneme = AudioSegment.empty()
    silence = AudioSegment.silent(duration=200)
    silence_x2 = AudioSegment.silent(duration=400)
    print("go phoneme progress")
    for i in range(len(input_text_list)):
        begin = 0
        end = 0
        analyze_counter = 0
        analyze_list = analyze(input_text_list[i])
        if i != 0:
            one_big_phoneme = one_big_phoneme.append(silence)
        new_word = AudioSegment.empty()
        for j in range(len(input_text_list[i])):
            if input_text_list[i][j][0] in vocabulary:
                phoneme = find_phoneme(input_text_list[i][j], dest)
                print("we got it!")
                if analyze_list[analyze_counter].isStress:
                    begin = len(new_word)
                phoneme, crossfade = phoneme_pre_processing(phoneme, analyze_list[analyze_counter])
                new_word = new_word.append(phoneme, crossfade=crossfade)
                if analyze_list[analyze_counter].isStress:
                    end = len(new_word)
                analyze_counter += 1
            else:
                if input_text_list[i][j][0] in punctuation_marks:
                    one_big_phoneme = one_big_phoneme.append(silence_x2)

        if begin != 0 and end != 0:
            new_word = new_word.fade(to_gain=+2, start=0, end=begin)
            if end != len(new_word):
                new_word = new_word.fade(to_gain=-2, start=end, end=len(new_word))

        one_big_phoneme = one_big_phoneme.append(new_word, crossfade=0)

    one_big_phoneme = speed_change(one_big_phoneme, 0.97)
    return one_big_phoneme


def phoneme_pre_processing(phoneme, analyze_info):
    phoneme_size = len(phoneme)

    # й
    if analyze_info.lenDiff == 0.2:
        curr_crossfade = 0
        if analyze_info.crossFade != 0:
            curr_crossfade = 15
        return phoneme[(len(phoneme) * 0.3):(len(phoneme) * 0.45)] - analyze_info.dbDiff, curr_crossfade

    # к
    if analyze_info.lenDiff == 0.3:
        curr_crossfade = 0
        if analyze_info.crossFade != 0:
            curr_crossfade = 15
        return phoneme[(len(phoneme) * 0.4):(len(phoneme) * 0.7)] - analyze_info.dbDiff, curr_crossfade

    # одиночный согласный
    if analyze_info.lenDiff == 0.5:
        curr_crossfade = 0
        if analyze_info.crossFade != 0:
            curr_crossfade = 15
        if phoneme_size > 130:
            cut_off = ((phoneme_size - 130) / 2) / phoneme_size
            return phoneme[(len(phoneme) * (cut_off - cut_off / 2)):(len(phoneme) * (1 - (cut_off - cut_off / 2)))] - analyze_info.dbDiff, curr_crossfade
        else:
            return phoneme - analyze_info.dbDiff, curr_crossfade

    if analyze_info.lenDiff == 0.9:
        if phoneme_size > 200:
            return phoneme[:(len(phoneme) * analyze_info.lenDiff)] - analyze_info.dbDiff, analyze_info.crossFade
        else:
            return phoneme - analyze_info.dbDiff, analyze_info.crossFade

    if len(phoneme) * analyze_info.lenDiff < analyze_info.crossFade:
        analyze_info.crossFade = len(phoneme) * analyze_info.lenDiff * 0.9

    return phoneme - analyze_info.dbDiff, analyze_info.crossFade


def analyze(syllables_list):
    # syllables_list = ['ве', 'ли', '\'', 'ка', 'я']
    analyze_list = []
    prev_stress = False
    factor = 0
    always = False

    if len(syllables_list) == 1:
        wc = WordContain()
        if not syllables_list[0] == 'ь' and not syllables_list[0] == 'ъ':
            wc.dbDiff = 4

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
            if i - 1 < 0 or always:
                always = True
                for j in range(len(syllables_list[i + factor])):
                    if syllables_list[i + factor][j] in vowels:
                        only_consonants = False
                        break
            else:
                for j in range(len(syllables_list[i - 1 + factor])):
                    if syllables_list[i - 1 + factor][j] in vowels:
                        only_consonants = False
                        break

            wc = WordContain()
            if prev_stress:
                if only_consonants:
                    wc.lenDiff = 0.5  # 0.5
                else:
                    wc.lenDiff = 1  # 0.7
                wc.crossFade = 30  # 75
                wc.dbDiff = 4
                analyze_list.append(wc)
                prev_stress = False
            else:
                wc.dbDiff = 4
                if only_consonants:
                    if not always:
                        if syllables_list[i - 1] == 'к' or syllables_list[i - 1] == 'п':
                            wc.lenDiff = 0.3  # 0.5
                        elif syllables_list[i - 1] == 'й':
                            wc.lenDiff = 0.2  # 0.5
                        else:
                            wc.lenDiff = 0.5  # 0.5
                    else:
                        if syllables_list[i] == 'к' or syllables_list[i] == 'п':
                            wc.lenDiff = 0.3  # 0.5
                        elif syllables_list[i] == 'й':
                            wc.lenDiff = 0.2  # 0.5
                        else:
                            wc.lenDiff = 0.5  # 0.5
                else:
                    wc.lenDiff = 0.9  # 0.9
                if stressed == 1:
                    if i != 1:
                        wc.crossFade = 30  # 300
                else:
                    if i != 0:
                        wc.crossFade = 30  # 300
                analyze_list.append(wc)
        else:
            wc = WordContain()
            if stressed == 1:
                if i != 1:
                    wc.crossFade = 30  # 300
            else:
                if i != 0:
                    wc.crossFade = 30  # 300
            wc.dbDiff = -1
            wc.lenDiff = 1
            wc.isStress = True
            prev_stress = True
            factor = 1
            analyze_list.append(wc)
    return analyze_list
