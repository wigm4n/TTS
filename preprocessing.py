from params import Params as params
import numpy as np
import os
import re
import codecs
import unicodedata
import librosa


def get_char_ids():
    ids = {}
    for i in range(len(params.vocabulary)):
        ids[params.vocabulary[i]] = i
    return ids


def get_id_chars():
    chars = {}
    for i in range(len(params.vocabulary)):
        chars[i] = params.vocabulary[i]
    return chars


def de_accent(some_unicode_string):
    return u''.join(c for c in unicodedata.normalize('NFD', some_unicode_string)
                    if unicodedata.category(c) != 'Mn')


def text_normalize(text):
    text = de_accent(text)
    text = text.lower()
    text = re.sub("[^{}]".format(params.vocabulary), "", text)
    return text


def read_transcript():
    transcript = os.path.join(params.data_set_path, params.transcript_file_name)
    return codecs.open(transcript, 'r', 'utf-8').readlines()


def text_processing():
    ids = get_char_ids()
    text_lengths, texts = [], []
    lines = read_transcript()

    for line in lines:
        text = text_normalize(line.strip().split("|")[2]) + "E"  # EOS
        text_in_ids = []
        for i in range(len(text)):
            text_in_ids.append(ids[text[i]])
        text_lengths.append(len(text_in_ids))
        texts.append(np.array(text_in_ids, np.int32).tostring())

    return texts, text_lengths


def get_paths():
    file_paths = []
    lines = read_transcript()

    for line in lines:
        file_path = os.path.join(params.data_set_path, "wavs", line.strip().split("|")[0] + params.audio_format)
        file_paths.append(file_path)

    return file_paths


def save_spectrograms(file_name, mel, mag):
    np.save("spectrograms/mels/{}".format(file_name.replace("wav", "npy")), mel)
    np.save("spectrograms/mags/{}".format(file_name.replace("wav", "npy")), mag)


def spectrograms_reduction(mel, mag):
    mel_size = mel.shape[0]
    if mel_size % params.r != 0:
        num_paddings = params.r - (mel_size % params.r)
    else:
        num_paddings = 0

    mel = np.pad(mel, [[0, num_paddings], [0, 0]], mode="constant")
    mag = np.pad(mag, [[0, num_paddings], [0, 0]], mode="constant")

    mel = mel[::params.r, :]

    return mel, mag


def audio_preprocessing(file_path):
    mel, mag = get_spectrograms(file_path)
    return os.path.basename(file_path), mel, mag


def get_spectrograms(file_path):
    # Parse the wave file and returns normalized mel spectrogram and magnitude spectrogram.

    signal, sample_rate = librosa.load(file_path)

    # trimming and pre-emphasis filter to high frequency booster.
    signal, _ = librosa.effects.trim(signal)
    signal = np.append(signal[0], signal[1:] - params.pre_emphasis * signal[:-1])

    # getting magnitude spectrogram from stft
    mag = np.abs(librosa.stft(y=signal,
                              n_fft=params.n_fft,
                              hop_length=int(params.sr * params.frame_shift),
                              win_length=int(params.sr * params.frame_length)))

    # mel spectrogram (n_mels=80)
    mel = librosa.feature.melspectrogram(y=signal,
                                         sr=params.sr,
                                         hop_length=int(params.sr * params.frame_shift))

    # to decibel
    mel = librosa.power_to_db(mel, amin=1e-5)
    mag = librosa.power_to_db(mag, amin=1e-5)

    # normalize (mel = np.clip((mel - 10 + params.max_db) / params.max_db, 1e-8, 1))
    mel = np.clip((mel + params.max_db) / params.max_db, 1e-8, 1)
    mag = np.clip((mag + params.max_db) / params.max_db, 1e-8, 1)

    # transpose
    mel = mel.T.astype(np.float32)
    mag = mag.T.astype(np.float32)

    mel, mag = spectrograms_reduction(mel, mag)

    return mel, mag


def start_preprocessing():
    file_paths = get_paths()

    _, _ = text_processing()

    if len(file_paths) != 0:
        if not os.path.exists("spectrograms"):
            os.mkdir("spectrograms")
        if not os.path.exists("spectrograms/mels"):
            os.mkdir("spectrograms/mels")
        if not os.path.exists("spectrograms/mags"):
            os.mkdir("spectrograms/mags")

    for each_file in file_paths:
        file_name, mel, mag = audio_preprocessing(each_file)
        save_spectrograms(file_name, mel, mag)
        print("File {} processed".format(file_name))
