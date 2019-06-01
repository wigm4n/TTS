# -*- coding: utf-8 -*-

import math

from pydub import AudioSegment
import wave
import numpy as np

vocabulary = "аеёиоуыэюябвгджзйклмнпрстфхцчшщьъ-"
vowels = "аеёиоуыэюя"


class WordContain:
    isStress = False
    dbDiff = 0
    lenDiff = 0
    crossFade = 0


def format_db(x, pos=None):
    peak = 512
    if pos == 0:
        return ""
    if x == 0:
        return "-inf"

    db = 20 * math.log10(abs(x) / float(peak))
    return int(db)


def analyze(syllables_list):
    # syllables_list = ['ве', 'ли', '\'', 'ка', 'я']
    syllables_list = ['во', 'й', 'на', '\'']
    syllables_list = ['ве', 'н', 'ти', 'ля', '\'', 'то', 'р']
    syllables_list = ['ме', '\'', 'че', 'н', 'ны', 'й']
    analyze_list = []
    prev_stress = False
    factor = 0

    for i in range(1, len(syllables_list)):
        if syllables_list[i][0] in vocabulary:

            only_consonants = True
            for j in range(len(syllables_list[i - 1 + factor])):
                if syllables_list[i - 1 + factor][j] in vowels:
                    only_consonants = False
                    break

            wc = WordContain()
            if prev_stress:
                if only_consonants:
                    wc.lenDiff = 0.5
                else:
                    wc.lenDiff = 0.7
                wc.crossFade = 75
                wc.dbDiff = 5
                analyze_list.append(wc)
                prev_stress = False
            else:
                wc.dbDiff = 5
                if only_consonants:
                    wc.lenDiff = 0.5
                else:
                    wc.lenDiff = 0.9
                if i != 1:
                    wc.crossFade = 300
                analyze_list.append(wc)
        else:
            wc = WordContain()
            wc.crossFade = 300
            wc.dbDiff = -1
            wc.lenDiff = 1
            wc.isStress = True
            prev_stress = True
            factor = 1
            analyze_list.append(wc)


if __name__ == '__main__':
    analyze([])
    # audio = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/великая_война.wav")
    wav = wave.open("/Users/ilya_lobanov/Desktop/великая_война.wav", mode="r")
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
    content = wav.readframes(nframes)

    types = {
        1: np.int8,
        2: np.int16,
        4: np.int32
    }
    samples = np.fromstring(content, dtype=types[sampwidth])

    channel = None
    for n in range(nchannels):
        channel = samples[n::nchannels]

    dbs = []
    for n in range(len(channel)):
        dbs.append(format_db(channel[n]))

    audio = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/великая_война.wav")

    audio2 = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/sounds/new_all/ве.wav")
    audio3 = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/sounds/new_all/ли.wav")
    audio4 = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/sounds/new_all/ка.wav")
    audio5 = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/sounds/new_all/я.wav")
    sadf = AudioSegment.empty()
    sadf = sadf.append(audio2[-(len(audio2)*0.9):] - 5, crossfade=0)
    sadf = sadf.append(audio3 + 1, crossfade=300)
    sadf = sadf.append(audio4[-(len(audio4)*0.70):] - 5, crossfade=75)
    sadf = sadf.append(audio5[-(len(audio5)*0.9):] - 8, crossfade=300)
    # sadf.export("/Users/ilya_lobanov/Desktop/crossfade.wav", format="wav")

    audio6 = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/sounds/super_new_all/ва.wav")
    audio7 = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/sounds/super_new_all/й.wav")
    audio8 = AudioSegment.from_file("/Users/ilya_lobanov/Desktop/sounds/super_new_all/на.wav")

    len2 = len(audio6)
    len3 = len(audio7)
    len4 = len(audio8)

    sad = AudioSegment.empty()
    crossFade_sogl = len(audio7)*0.5*0.9
    sad = sad.append(audio6 - 5, crossfade=0)
    sad = sad.append(audio7 - 7, crossfade=35)
    sad = sad.append(audio8, crossfade=35)
    sad.export("/Users/ilya_lobanov/Desktop/война.wav", format="wav")


    len2 = len(audio2)
    len3 = len(audio3)
    len4 = len(audio4)
    len5 = len(audio5)


    audio2_db = -19.5

    dlina = len(audio2)
    d = audio2[0:30]
    f = audio2[30:60]
    g = audio2[60:90]
    h = audio2[90:120]
    j = audio2[120:150]

    summm = AudioSegment.empty()

    zz = audio2[-150:]

    asf = 0
    step = 0
    dfs_m = []
    while asf < dlina:
        cur_chunk = audio2[asf:asf + 30]
        if cur_chunk.dBFS > audio2_db:
            cur_chunk = cur_chunk - ((abs(audio2_db) - abs(cur_chunk.dBFS)) * 0.75)
        else:
            cur_chunk = cur_chunk + abs((abs(cur_chunk.dBFS) - abs(audio2_db)) * 0.75)
        summm = summm.append(cur_chunk, crossfade=0)
        asf += 30

    summm.export("/Users/ilya_lobanov/Desktop/ве_new.wav", format="wav")

    e = audio2[-250:]
    end = e - 6
    with_style1 = audio2[:(dlina-250)].append(end, crossfade=0)

    dlina = len(audio3)
    i = audio3[-250:]
    end = i - 6
    with_style2 = audio3[:(dlina-250)].append(end, crossfade=0)

    dlina = len(audio4)
    a = audio4[-250:]
    end = a - 6
    with_style3 = audio4[:(dlina-250)].append(end, crossfade=0)

    audio5 = audio5 - 6

    summ = with_style1.append(with_style2, crossfade=10)
    summ = summ.append(with_style3, crossfade=10)
    summ = summ.append(audio5, crossfade=10)

    first_10_seconds = audio[:700]
    last_5_seconds = audio[-700:]

    # boost volume by 6dB
    beginning = first_10_seconds + 10
    end = last_5_seconds - 10

    with_style = beginning.append(end, crossfade=200)

    summ.export("/Users/ilya_lobanov/Desktop/великая_война_3.wav", format="wav")


    print("done")


