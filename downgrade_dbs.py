import os

from pydub import AudioSegment


def test_fade_in_out():
    audio = AudioSegment.from_file("/Users/ilya_lobanov/PycharmProjects/thesis_tts/generated_audios/2019-06-02/что_делать.wav")

    audio = audio.fade_out(1000)


    audio.export("/Users/ilya_lobanov/Desktop/kkk/fade_test.wav", format="wav")


def do_it_twice():
    audio = AudioSegment.from_file("/Users/ilya_lobanov/PycharmProjects/thesis_tts/static/sounds/all/ба.wav")
    audio.export("/Users/ilya_lobanov/Desktop/kkk/ба.wav", format="wav")


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


if __name__ == '__main__':
    test_fade_in_out()
