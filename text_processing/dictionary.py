# -*- coding: utf-8 -*-

import re
from num2words import num2words
import pymorphy2 as pymorphy2

from ru_rules import apply_the_rules


class Preprocessing:
    global_map = {}
    global_stressed_map = {}
    vowels = "аеёиоуыэюя"
    consonants = "бвгджзйклмнпрстфхцчшщьъ"
    signs_of_softness = "ьъ"
    vocabulary = "аеёиоуыэюябвгджзйклмнпрстфхцчшщьъ1234567890 -,.:;!?#№$%&€"
    sings_for_divide = ".,:;!?№#$€%&"

    #     -             не выделять, как отдельный элемент
    #     ! ?           эмоциональная окраска речи
    #     . , : ;       пауза в речи
    #     № # $ € % &   озвучить как слова

    def process_input_text(self, input_text):
        words = self.preprocess_input_text(input_text)
        res = self.find_stress(words)
        res = apply_the_rules(res)
        res2 = self.wrapper_syllables(res)
        return res2

    def prepare_dictionaries(self):
        self.build_map(False)

    def build_map(self, flag):
        filepath = 'static/stress_forms.txt'
        with open(filepath, encoding="utf-8") as fp:
            line = fp.readline()
            cnt = 1
            while line:
                line = line.rstrip()
                line = line.replace('`', '')
                line = line.replace('€', 'я')
                line = line.replace('Є', 'ё')
                splited_line = line.split("#")
                splited_words = splited_line[1].split(",")
                self.global_stressed_map[splited_line[0]] = splited_words
                if flag:
                    print("Line {}: {}".format(cnt, line.strip()))

                line = line.replace('\'', '')
                splited_line = line.split("#")
                splited_words = splited_line[1].split(",")
                self.global_map[splited_line[0]] = splited_words

                line = fp.readline()
                cnt += 1
        print("Done")

    def find_stress(self, words):
        res = []
        for i in range(len(words)):
            if words[i] not in self.sings_for_divide:
                found = False
                for k in self.global_map:
                    if not found:
                        counter = 0
                        for v in self.global_map[k]:
                            if words[i] == v:
                                res.append(self.global_stressed_map[k][counter])
                                found = True
                                break
                            counter += 1
                if not found:
                    res.append(words[i])
            else:
                res.append(words[i])
        return res

    # обезьяна
    # облепиха
    # молоко
    # маалокс

    # осколок
    # особняк
    # аутист
    # трактор
    def break_into_syllables(self, word):
        last_vowel = False
        last_consonant = False
        syllables = []
        if len(word) < 2:
            syllables.append(word)
            return syllables
        current_chars = ""
        for i in range(len(word)):
            if word[i] == '\'':
                syllables.append(current_chars)
                syllables.append(word[i])
                current_chars = ""
                last_vowel = False
                last_consonant = False

            if word[i] in self.consonants:
                if word[i] in self.signs_of_softness:
                    current_chars += word[i]
                    syllables.append(current_chars)
                    current_chars = ""
                    last_vowel = False
                    last_consonant = False
                elif last_consonant:
                    syllables.append(current_chars)
                    current_chars = word[i]
                    last_vowel = False
                else:
                    last_consonant = True
                    current_chars += word[i]

            if word[i] in self.vowels:
                if last_vowel and last_consonant:
                    if self.is_vowel_first(current_chars):
                        if word[i] in self.consonants:
                            syllables.append(current_chars)
                            current_chars = word[i]
                            last_vowel = False
                            last_consonant = False
                        else:
                            syllables.append(current_chars[:1])
                            current_chars = current_chars[1:]
                            current_chars += word[i]
                    else:
                        if word[i] in self.consonants:
                            syllables.append(current_chars)
                            current_chars = word[i]
                            last_vowel = False
                        else:
                            syllables.append(current_chars)
                            current_chars = word[i]
                            last_consonant = False

                elif last_vowel:
                    syllables.append(current_chars)
                    current_chars = word[i]
                    last_consonant = False
                else:
                    last_vowel = True
                    current_chars += word[i]

        if current_chars != "":
            syllables.append(current_chars)

        is_triple_let = False
        for j in range(len(syllables)):
            if len(syllables[j]) > 2:
                is_triple_let = True
                break

        new_syll = []
        if is_triple_let:
            new_syll = []
            for j in range(len(syllables)):
                if len(syllables[j]) > 2:
                    new_syll.append(syllables[j][:1])
                    new_syll.append(syllables[j][1:])
                else:
                    new_syll.append(syllables[j])

        if len(new_syll) == 0:
            return syllables
        else:
            return new_syll

    def wrapper_syllables(self, words):
        res = []
        for i in range(len(words)):
            res.append(self.break_into_syllables(words[i]))
        return res

    def is_vowel_first(self, syllable):
        if syllable[0] in self.vowels:
            return True
        else:
            return False

    def preprocess_input_text(self, text):
        text = text.strip()
        text = text.lower()
        text = self.text_num_split(text)
        text = text.strip()
        text = re.sub("[^{}]".format(self.vocabulary), "", text)
        text = self.replace_digits(text)
        words_and_signs = text.split(" ")
        return self.mark_out(words_and_signs)

    # def get_number_and_noun(self, numeral, noun):
    #     morph = pymorphy2.MorphAnalyzer()
    #     word = morph.parse(noun)[0]
    #     v1, v2, v3 = word.inflect({'sing', 'nomn'}), word.inflect({'gent'}), word.inflect({'plur', 'gent'})
    #     return num2text(num=numeral, main_units=((v1.word, v2.word, v3.word), 'm'))

    # для числа
    def numbers_2_words(self, number):
        return num2words(number, lang='ru')

    def define_part_of_speech(self, word_parse):
        parts_of_speech = {}
        for i in range(len(word_parse.lexeme)):
            parts_of_speech[word_parse.lexeme[i].tag.POS] = 1
        return parts_of_speech

    def p_has_sing_and_plur(self, p):
        word = p.word
        has_sing = False
        has_plur = False
        for i in range(len(p.lexeme)):
            if p.lexeme[i].word == word:
                if p.lexeme[i].tag.number == "sing":
                    has_sing = True
                if p.lexeme[i].tag.number == "plur":
                    has_plur = True
                if has_sing and has_plur:
                    return True
        return False

    # если числительное количественное - True  (NUMR)
    # если числительное порядковое - False  (ADJF)
    def is_number_numr(self, p, number):
        plur_forms = []

        number_in_int = int(number)
        if number_in_int > 99:
            number_in_int = number_in_int % 100
        if number_in_int < 10 and (number_in_int == 2 or number_in_int == 3 or number_in_int == 4):
            if p.tag.case == "accs" or p.tag.case == "nomn":
                return False, "nomn"
            else:
                return True, "nomn"
        if number_in_int > 20 and (number_in_int % 10 == 2 or number_in_int % 10 == 3 or number_in_int % 10 == 4):
            if p.tag.case == "accs" or p.tag.case == "nomn":
                return False, "nomn"
            else:
                return True, "nomn"
        if self.p_has_sing_and_plur(p):
            return False, "gent"

        for i in range(len(p.lexeme)):
            if p.lexeme[i].tag.number != "sing":
                plur_forms.append(p.lexeme[i])
        for j in range(len(plur_forms)):
            if p.word == plur_forms[j].word:
                return True, plur_forms[j].tag.case

        cor = "1234"
        if len(number) != 0:
            if number[len(number) - 1] in cor:
                if p.tag.case == "gent" or "accs" or "nomn":
                    return False, p.tag.case

        return False, ""

    def numbers_2_words_case_matched(self, number, next_word):
        morph = pymorphy2.MorphAnalyzer()
        p = morph.parse(next_word)[0]
        words_string = num2words(number, lang='ru')
        words = words_string.split(" ")
        is_numr, case = self.is_number_numr(p, number)
        res = []
        res_string = ""
        need_change = False
        # if next_word == "года" and len(words) < 2:
        #     is_numr = True
        #     case = "nomn"
        if is_numr:
            need_change = False
        else:
            if len(words) > 1:
                for j in range(len(words) - 1):
                    res.append(words[j])
                last = words[len(words) - 1]
                words.clear()
                words.append(last)

        for i in range(len(words)):
            if len(words) > 1 and need_change:
                if i == len(words) - 1:
                    is_numr = False
            word_parse = morph.parse(words[i])[0]
            dict_s = self.define_part_of_speech(word_parse)
            try:
                try:
                    if is_numr:
                        if case == "gent":
                            case = "nomn"
                        if word_parse.inflect({"NUMR", p.tag.gender, case}) is None:
                            res.append(word_parse.inflect({"NUMR", case}).word)
                        else:
                            res.append(word_parse.inflect({"NUMR", p.tag.gender, case}).word)
                    else:
                        res.append(word_parse.inflect({"ADJF", p.tag.gender, p.tag.case}).word)
                except Exception:
                    res.append(word_parse.inflect({p.tag.case}).word)
            except Exception:
                res.append(words[i])

        for i in range(len(res)):
            res_string += res[i] + " "
        return res_string.strip()

    def replace_digits(self, text):
        if len(text) == 0:
            return ""
        words_and_digits = text.split(" ")
        for i in range(len(words_and_digits)):
            if words_and_digits[i] == "" or words_and_digits[i] == '':
                continue
            if words_and_digits[i][0].isdigit():
                if i < len(words_and_digits) - 1:
                    words_and_digits[i] = self.numbers_2_words_case_matched(words_and_digits[i], words_and_digits[i + 1])
                else:
                    words_and_digits[i] = self.numbers_2_words(words_and_digits[i])
        res = ""
        for i in range(len(words_and_digits)):
            res += words_and_digits[i]
            res += " "
        return res.strip()

    def text_num_split(self, item):
        before = ""
        prev_digit = False
        prev_space = False
        for index, letter in enumerate(item, 0):
            if letter.isdigit():
                if prev_digit:
                    before += letter
                else:
                    if not prev_space:
                        before += " "
                    before += letter
                    prev_digit = True
                    prev_space = False
            else:
                if letter == " ":
                    if prev_space:
                        continue
                    prev_space = True
                    prev_digit = False
                    before += letter
                    continue
                if prev_digit:
                    before += " " + letter
                    prev_digit = False
                    prev_space = False
                    continue
                prev_digit = False
                prev_space = False
                before += letter
        return before

    def mark_out(self, words_and_signs):
        res_objects = []
        temp_words = ""
        # [ привет, ]  [ как ] [ дела? ]
        for i in range(len(words_and_signs)):
            if temp_words != "":
                res_objects.append(temp_words)
            temp_words = ""
            for j in range(len(words_and_signs[i])):
                current_char = words_and_signs[i][j]
                if current_char in self.sings_for_divide:
                    if temp_words != "":
                        res_objects.append(temp_words)
                        temp_words = ""
                    res_objects.append(current_char)
                else:
                    temp_words += current_char
        if temp_words != "":
            res_objects.append(temp_words)
        return res_objects
