class Params:
    data_set_path = "/Users/ilya_lobanov/Мои файлы/HSE/ВКР/datasets/data_5/LJSpeech-1.0"
    transcript_file_name = "transcript.csv"
    text_sentences = "/Users/ilya_lobanov/PycharmProjects/thesis_tts/example.txt"
    vocabulary = "E abcdefghijklmnopqrstuvwxyz'.?"
    audio_format = ".wav"

    # signal processing
    sr = 22050  # sampling rate.
    n_fft = 2048  # fft points (samples)
    n_mels = 80  # recommended value
    frame_shift = 0.0125  # seconds
    frame_length = 0.05  # seconds
    hop_length = int(sr * frame_shift)  # length of hop
    win_length = int(sr * frame_length)  # length of win
    pre_emphasis = .97  # recommended value
    n_iter = 50  # recommended value
    power = 1.5  # exponent for amplifying the predicted magnitude
    max_db = 50
    normalization_param_db = 10

    # Model
    r = 4  # reduction factor
