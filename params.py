class Params:
    data_set_path = "/Users/ilya_lobanov/Мои файлы/HSE/ВКР/datasets/data_5/LJSpeech-1.0"
    transcript_file_name = "transcript.csv"
    text_sentences = "/Users/ilya_lobanov/PycharmProjects/thesis_tts/example.txt"
    vocabulary = "E abcdefghijklmnopqrstuvwxyz'.?"
    audio_format = ".wav"

    # signal processing
    sr = 22050  # sampling rate.
    n_fft = 2048  # fft points (samples)
    frame_shift = 0.0125  # seconds
    frame_length = 0.05  # seconds
    pre_emphasis = .97
    max_db = 50

    # Model
    r = 4  # reduction factor
