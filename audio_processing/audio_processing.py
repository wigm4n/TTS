# -*- coding: utf-8 -*-

import os
from pydub import AudioSegment

from params import Params as params


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
    dest = os.getcwd() + params.path_to_audios

    all_text = AudioSegment.empty()
    silence = AudioSegment.silent(duration=params.silent_words)
    silence_x2 = AudioSegment.silent(duration=params.silent_sentenses)
    print("go phoneme progress")

    sentences_list = []
    curr_sentence = []
    for i in range(len(input_text_list)):
        if input_text_list[i][0] in params.end_marks:
            curr_sentence.append(input_text_list[i])
            sentences_list.append(curr_sentence)
            curr_sentence = []
        else:
            curr_sentence.append(input_text_list[i])
    if len(curr_sentence) != 0:
        sentences_list.append(curr_sentence)
    for u in range(len(sentences_list)):
        begin_q = 0
        end_q = 0
        one_sentence = AudioSegment.empty()
        for i in range(len(sentences_list[u])):
            begin = 0
            end = 0
            analyze_counter = 0
            analyze_list = analyze(sentences_list[u][i])
            if i != 0:
                one_sentence = one_sentence.append(silence)
            new_word = AudioSegment.empty()
            is_questionable = is_questionable_word(sentences_list[u][i])
            if is_questionable:
                begin_q = len(one_sentence)
            for j in range(len(sentences_list[u][i])):
                if sentences_list[u][i][j][0] in params.vocabulary:
                    phoneme = find_phoneme(sentences_list[u][i][j], dest)
                    print("we got it!")
                    if analyze_list[analyze_counter].isStress:
                        begin = len(new_word)
                    phoneme, crossfade = phoneme_pre_processing(phoneme, analyze_list[analyze_counter])
                    new_word = new_word.append(phoneme, crossfade=crossfade)
                    if analyze_list[analyze_counter].isStress:
                        end = len(new_word)
                    analyze_counter += 1
                else:
                    if sentences_list[u][i][j][0] in params.punctuation_marks:
                        one_sentence = one_sentence.append(silence)
            one_sentence = one_sentence.append(new_word, crossfade=0)
            if is_questionable:
                end_q = len(one_sentence)
            if end != 0:
                if begin == 0:
                    new_word = new_word.fade(to_gain=+params.fade_gain_words, start=0, end=end)
                else:
                    new_word = new_word.fade(to_gain=+params.fade_gain_words, start=0, end=begin)
                if end != len(new_word):
                    new_word = new_word.fade(to_gain=-params.fade_gain_words, start=end, end=len(new_word))

        if sentences_list[u][len(sentences_list[u]) - 1][0] in params.end_marks:
            if sentences_list[u][len(sentences_list[u]) - 1][0] == "?":
                if end_q != 0:
                    one_sentence = process_interrogative_sentence(one_sentence, begin_q, end_q)
                else:
                    one_sentence = one_sentence.fade(to_gain=+params.fade_gain_sentenses, start=0, end=len(one_sentence))
                all_text = all_text.append(one_sentence, crossfade=0)
            elif sentences_list[u][len(sentences_list[u]) - 1][0] == "!":
                one_sentence = one_sentence.fade(to_gain=+params.fade_gain_sentenses, start=0, end=len(one_sentence))
                all_text = all_text.append(one_sentence, crossfade=0)
            else:
                all_text = all_text.append(one_sentence, crossfade=0)
            all_text = all_text.append(silence_x2, crossfade=0)
        else:
            all_text = all_text.append(one_sentence, crossfade=0)

    all_text = speed_change(all_text, params.speed)
    return all_text


def process_interrogative_sentence(sentence_audio, begin, end):
    if begin != 0 and end != 0:
        sentence_audio = sentence_audio.fade(to_gain=+params.fade_gain_sentenses, start=0, end=begin)
        if end != len(sentence_audio):
            sentence_audio = sentence_audio.fade(to_gain=-params.fade_gain_sentenses, start=end, end=len(sentence_audio))
    elif end != 0:
        sentence_audio = sentence_audio.fade(to_gain=+params.fade_gain_sentenses, start=0, end=end)
        sentence_audio = sentence_audio.fade(to_gain=-params.fade_gain_sentenses, start=end, end=len(sentence_audio))
    return sentence_audio


def norm_word(syllables_list):
    word = ""
    for i in range(len(syllables_list)):
        if syllables_list[i][0] in params.vocabulary:
            word += syllables_list[i]
    return word


def is_questionable_word(syllables_list):
    word = norm_word(syllables_list)
    questionable_dict = {"как", "где", "зачем", "почему", "кому", "откуда", "куда", "што", "кто"}
    if word in questionable_dict:
        return True
    else:
        return False


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
            return phoneme[(len(phoneme) * (cut_off - cut_off / 2)):(
                    len(phoneme) * (1 - (cut_off - cut_off / 2)))] - analyze_info.dbDiff, curr_crossfade
        else:
            return phoneme - analyze_info.dbDiff, curr_crossfade

    if analyze_info.lenDiff == 0.85:
        if phoneme_size > 200:
            return phoneme[:(len(phoneme) * analyze_info.lenDiff)] - analyze_info.dbDiff, analyze_info.crossFade
        else:
            return phoneme - analyze_info.dbDiff, analyze_info.crossFade

    if len(phoneme) * analyze_info.lenDiff < analyze_info.crossFade:
        analyze_info.crossFade = len(phoneme) * analyze_info.lenDiff * 0.88

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
        if syllables_list[i][0] not in params.vocabulary:
            stressed = 1
            break

    if len(syllables_list) == 2 and stressed == 1:
        wc = WordContain()
        analyze_list.append(wc)
        return analyze_list

    for i in range(stressed, len(syllables_list)):
        if syllables_list[i][0] in params.vocabulary:

            only_consonants = True
            if i - 1 < 0 or always:
                always = True
                for j in range(len(syllables_list[i + factor])):
                    if syllables_list[i + factor][j] in params.vowels:
                        only_consonants = False
                        break
            else:
                for j in range(len(syllables_list[i - 1 + factor])):
                    if syllables_list[i - 1 + factor][j] in params.vowels:
                        only_consonants = False
                        break

            wc = WordContain()
            if prev_stress:
                if only_consonants:
                    wc.lenDiff = 0.5
                else:
                    wc.lenDiff = 1
                wc.crossFade = params.general_crossFade
                wc.dbDiff = 4
                analyze_list.append(wc)
                prev_stress = False
            else:
                wc.dbDiff = 4
                if only_consonants:
                    if not always:
                        if syllables_list[i - 1] == 'к' or syllables_list[i - 1] == 'п':
                            wc.lenDiff = 0.3
                        elif syllables_list[i - 1] == 'й':
                            wc.lenDiff = 0.2
                        else:
                            wc.lenDiff = 0.5
                    else:
                        if syllables_list[i] == 'к' or syllables_list[i] == 'п':
                            wc.lenDiff = 0.3
                        elif syllables_list[i] == 'й':
                            wc.lenDiff = 0.2
                        else:
                            wc.lenDiff = 0.5
                else:
                    wc.lenDiff = 0.88
                if stressed == 1:
                    if i != 1:
                        wc.crossFade = params.general_crossFade
                else:
                    if i != 0:
                        wc.crossFade = params.general_crossFade
                analyze_list.append(wc)
        else:
            wc = WordContain()
            if stressed == 1:
                if i != 1:
                    wc.crossFade = params.general_crossFade
            else:
                if i != 0:
                    wc.crossFade = params.general_crossFade
            wc.dbDiff = -1
            wc.lenDiff = 1
            wc.isStress = True
            prev_stress = True
            factor = 1
            analyze_list.append(wc)
    return analyze_list
