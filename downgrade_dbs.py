import os

from pydub import AudioSegment


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
    do_it()
