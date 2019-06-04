# -*- coding: utf-8 -*-
import os

from pydub import AudioSegment


def do_it_twice():
    audio = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/sounds/super_new_all/ню.wav")
    audio.export("/Users/ilya_lobanov/Desktop/sounds/super_new_all/ню.wav", format="wav")


def do_it():
    sounds = os.listdir(os.getcwd() + "/static/sounds/all/")

    for i in range(len(sounds)):
        if sounds[i][3:] == "wav":
            audio = AudioSegment.from_file(os.getcwd() + "/static/sounds/all/" + sounds[i])
            diff = abs(audio.dBFS + 20)
            if audio.dBFS > -20:
                audio = audio - diff
            else:
                audio = audio + diff

            audio.export(os.getcwd() + "/static/sounds/all/" + sounds[i], format="wav")
            print(sounds[i] + " done")
    print("done")


def change_db():
    audio222 = AudioSegment.from_file("/Users/ilya_lobanov/PycharmProjects/thesis_tts/static/sounds/all/ле.wav")
    audio222 = audio222 - 1
    audio222.export("/Users/ilya_lobanov/PycharmProjects/thesis_tts/static/sounds/all/ле.wav", format="wav")


if __name__ == '__main__':
    change_db()
