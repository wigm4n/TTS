# -*- coding: utf-8 -*-

import librosa
import numpy as np
from audio_processing.audio import create_wav
from audio_processing.params import Params as params


def pr():
    file_path = "/Users/ilya_lobanov/Desktop/ko.wav"
    signal, sample_rate = librosa.load(file_path)
    signal, _ = librosa.effects.trim(signal)
    signal = np.append(signal[0], signal[1:] - 0.97 * signal[:-1])

    mag = np.abs(librosa.stft(y=signal,
                                  n_fft=params.n_fft,
                                  hop_length=params.hop_length,
                                  win_length=params.win_length))
    mag = librosa.power_to_db(mag, amin=1e-5)
    mag = np.clip((mag - params.normalization_param_db + params.max_db) / params.max_db, 1e-8, 1)
    mag = mag.T.astype(np.float32)

    mag_size = mag.shape[0]
    if mag_size % params.r != 0:
        num_paddings = params.r - (mag_size % params.r)
    else:
        num_paddings = 0
    mag = np.pad(mag, [[0, num_paddings], [0, 0]], mode="constant")

    create_wav(mag)



