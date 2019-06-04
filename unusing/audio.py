# -*- coding: utf-8 -*-

from params import Params as params
import librosa
import copy
import numpy as np
from scipy.io.wavfile import write
from scipy import signal


def griffin_lim_algorithm(spectrogram):
    x_best = copy.deepcopy(spectrogram)

    for i in range(params.n_iter):
        x_temp = librosa.istft(x_best,
                               hop_length=params.hop_length,
                               win_length=params.win_length)
        linear = librosa.stft(y=x_temp,
                              n_fft=params.n_fft,
                              hop_length=params.hop_length,
                              win_length=params.win_length)

        phase = linear / np.maximum(1e-8, np.abs(linear))
        x_best = spectrogram * phase

    return np.real(librosa.istft(x_best,
                                 hop_length=params.hop_length,
                                 win_length=params.win_length))


def spectrogram_to_wav(mag):
    # transpose
    mag = mag.T

    # de-normalize
    mag = (np.clip(mag, 0, 1) * params.max_db) - params.max_db + params.normalization_param_db

    # to amplitude
    mag = np.power(20.0, mag * 0.05)

    # wav reconstruction
    wav = griffin_lim_algorithm(mag**params.power)

    # de-pre-emphasis
    wav = signal.lfilter([1], [1, -params.pre_emphasis], wav)

    # trim
    wav, _ = librosa.effects.trim(wav)

    return wav.astype(np.float32)


def create_wav(mag):
    write("test_asds.wav", params.sr, spectrogram_to_wav(mag))


def pr():
    file_path = "/Users/ilya_lobanov/Desktop/ko.wav"
    sig, sample_rate = librosa.load(file_path)
    sig, _ = librosa.effects.trim(sig)
    sig = np.append(sig[0], sig[1:] - 0.97 * sig[:-1])

    mag = np.abs(librosa.stft(y=sig,
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

