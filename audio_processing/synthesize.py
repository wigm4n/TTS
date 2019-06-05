# -*- coding: utf-8 -*-
import os
import datetime

from audio_processing.audio_processing import work_with_syllables


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
    try:
        save_path = os.getcwd() + "/generated_audios/" + curr_dir_name + "/" + norm_name + ".wav"
        result.export(save_path, format="wav")
    except:
        save_path = os.getcwd() + "/generated_audios/" + curr_dir_name + "/1.wav"
        result.export(save_path, format="wav")
    print("Аудиозапись сохранена по пути: ", save_path)

    return save_path, norm_name


def create_name(input_text):
    norm_name = input_text.replace(" ", "_")
    if len(norm_name) > 20:
        norm_name = norm_name[:40]
    return norm_name
