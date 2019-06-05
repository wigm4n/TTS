# -*- coding: utf-8 -*-


class Params:
    vocabulary_text = "аеёиоуыэюябвгджзйклмнпрстфхцчшщьъ1234567890 -,.:;!?#№$%&€+="
    vocabulary = "аеёиоуыэюябвгджзйклмнпрстфхцчшщьъ-№#$€%&+="
    consonants = "бвгджзйклмнпрстфхцчшщьъ"
    vowels = "аеёиоуыэюя"
    signs_of_softness = "ьъ"
    capitals = "ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТБЮ"
    punctuation_marks = ",:;-."
    end_marks = ":;.?!"
    sings_for_divide = ".,:;!?№#$€%&+="
    delete_signs = ".?!,;:"

    path_to_audios = "/static/sounds/all/"
    path_to_stress_dict = "static/stress_forms.txt"

    # speech processing
    speed = 1
    general_crossFade = 30
    silent_words = 125
    silent_sentenses = 275
    fade_gain_words = 2
    fade_gain_sentenses = 6
