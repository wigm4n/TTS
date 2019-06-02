# -*- coding: utf-8 -*-

from os import walk
from pydub import AudioSegment
import sys


# pr.pr()
# pp.start_preprocessing()
# y, sr = librosa.load("/Users/ilya_lobanov/Desktop/ko.wav")
# Trim the beginning and ending silence
# yt, index = librosa.effects.trim(y)
# Print the durations
# print(librosa.get_duration(y), librosa.get_duration(yt))
# print("Done")

def detect_and_remove_silence(path, path_to_save, file_name, silence_threshold=-50.0, chunk_size=10):
    sound = AudioSegment.from_file(path + file_name)

    result = AudioSegment.empty()
    sound_size = len(sound)
    trim_ms = 0  # ms
    assert chunk_size > 0  # to avoid infinite loop

    while trim_ms < sound_size:
        trim_ms += chunk_size
        # if sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        if sound[trim_ms:trim_ms + chunk_size].dBFS >= silence_threshold:
            result = result.append(sound[trim_ms:trim_ms + chunk_size], 0)
    file_names = file_name.split('.')
    result.export(path_to_save + file_name.split('.')[0] + ".wav", format="wav")

def prepo():
    data_set_path = "/Users/ilya_lobanov/Desktop/sounds/записи"
    path_to_save = "/Users/ilya_lobanov/Desktop/sounds/обработанные"

    file_paths = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
                'у', 'ф', 'х', 'ш', 'щ', 'ц', 'ч', 'э', 'ю', 'я']

    f = []
    for (dirpath, dirnames, asd) in walk(data_set_path):
        for i in range(len(dirnames)):
            for (filenames) in walk(data_set_path + "/" + dirnames[i]):
                for j in range(len(filenames[2])):
                    if filenames[2][j][0] == ".":
                        continue
                    detect_and_remove_silence(data_set_path, path_to_save, "/" + dirnames[i] + "/" + filenames[2][j])
        break

    # for line in lines:
    #     file_path = os.path.join("/Users/ilya_lobanov/Desktop/звуки/записи", "wavs", line.strip().split("|")[0] + "m4a")
    #     file_paths.append(file_path)
    #
    # return file_paths

    def append():
        sound1 = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/звуки/обработанные/п/п.wav")
        sound2 = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/звуки/обработанные/р/ри.wav")
        sound3 = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/звуки/обработанные/в/ве.wav")
        sound4 = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/звуки/обработанные/т/т.wav")
        sound5 = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/звуки/обработанные/к/ка.wav")
        sound6 = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/звуки/обработанные/к/к.wav")
        sound7 = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/звуки/обработанные/д/де.wav")

        result = sound1.append(sound2, 0)
        result = result.append(sound3, 20)
        result = result.append(sound4, 20)
        result = result.append(sound5, 20)
        result = result.append(sound6, 20)
        result = result.append(sound7, 0)


        result.export("/Users/ilya_lobanov/Desktop/privet_kakdela.wav", format="wav")

        return result




    def detect_leading_silence(sound, silence_threshold=-50.0, chunk_size=10):
        result = AudioSegment.empty()
        sound_size = len(sound)
        trim_ms = 0  # ms
        current_count = 0
        assert chunk_size > 0  # to avoid infinite loop

        while trim_ms < sound_size:
            trim_ms += chunk_size
            if sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(sound):


                print('current:', sound[trim_ms:trim_ms + chunk_size].dBFS, ' | ', trim_ms, 'ms - silence')
            else:
                temp = sound[trim_ms:trim_ms + chunk_size]
                result = result.append(temp, 0)

        # while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        #     trim_ms += chunk_size

        result.export("/Users/ilya_lobanov/Desktop/full_res.wav", format="wav")
        return trim_ms


    #pre_sound = append()
    #pre_sound = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/звуки/ко уд.m4a")
    #pre_sound.export("/Users/ilya_lobanov/Desktop/pre.wav", format="wav")
    #start_trim = detect_leading_silence(pre_sound)

    #sound = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/res.wav")

    #end_trim = 10

    #end_trim = detect_leading_silence(sound.reverse())

    #duration = len(pre_sound)
    #trimmed_sound = pre_sound[start_trim:duration - end_trim]

    #trimmed_sound.export("/Users/ilya_lobanov/Desktop/res3.wav", format="wav")
    #append()


if __name__ == '__main__':
    prepo()