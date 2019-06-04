# -*- coding: utf-8 -*-

from params import Params as params


def apply_the_rules(words):
    for i in range(len(words)):
        last_consonant = False

        # ещё
        if words[i] == "еще":
            words[i] = "ещё\'"
        if words[i] == "того\'":
            words[i] = "тово\'"
        # синтезатор
        words[i] = words[i].replace('синтез', 'синтэз')
        # солнце
        words[i] = words[i].replace('лнц', 'нц')
        # что
        words[i] = words[i].replace('что', 'што')
        # явства
        words[i] = words[i].replace('вств', 'ств')
        # лестница
        words[i] = words[i].replace('стн', 'сн')
        words[i] = words[i].replace('стл', 'сл')
        words[i] = words[i].replace('здн', 'зн')
        # сердце
        words[i] = words[i].replace('рдц', 'рц')
        words[i] = words[i].replace('рдч', 'рч')
        words[i] = words[i].replace('стц', 'сц')
        words[i] = words[i].replace('здц', 'зц')
        # агентские
        words[i] = words[i].replace('нтск', 'нск')
        words[i] = words[i].replace('ндск', 'нск')
        words[i] = words[i].replace('ндц', 'нц')
        # предантство
        words[i] = words[i].replace('нтств', 'нств')
        # абстракционистский
        words[i] = words[i].replace('стск', 'ск')
        # счастье
        words[i] = words[i].replace('сч', 'щ')
        # девятнадцать
        words[i] = words[i].replace('а\'дцат', 'а\'цат')
        # претворятся
        words[i] = words[i].replace('тся', 'ца')
        # кидаться
        words[i] = words[i].replace('ться', 'ца')

        # премудрая
        if len(words[i]) > 3 and words[i][:3] == 'пре' and (
                words[i][3] in params.consonants or words[i][3] in params.vowels):
            words[i] = 'при' + words[i][3:]
        if len(words[i]) > 1:
            # порог
            if words[i][len(words[i]) - 1] == 'г':
                words[i] = words[i][:len(words[i]) - 1] + 'к'
            # дуб
            elif words[i][len(words[i]) - 1] == 'б':
                words[i] = words[i][:len(words[i]) - 1] + 'п'
            # Крылов
            elif words[i][len(words[i]) - 1] == 'в':
                words[i] = words[i][:len(words[i]) - 1] + 'ф'
            # Крылов
            elif words[i][len(words[i]) - 1] == 'д':
                words[i] = words[i][:len(words[i]) - 1] + 'т'
            # Крылов
            elif words[i][len(words[i]) - 1] == 'ж':
                words[i] = words[i][:len(words[i]) - 1] + 'ш'
            # Крылов
            elif words[i][len(words[i]) - 1] == 'з':
                words[i] = words[i][:len(words[i]) - 1] + 'с'

        if len(words[i]) > 2:
            # порог
            if words[i][len(words[i]) - 2:] == 'гь':
                words[i] = words[i][:len(words[i]) - 2] + 'кь'
            # дуб
            elif words[i][len(words[i]) - 2:] == 'бь':
                words[i] = words[i][:len(words[i]) - 2] + 'пь'
            # Крылов
            elif words[i][len(words[i]) - 2:] == 'вь':
                words[i] = words[i][:len(words[i]) - 2] + 'фь'
            # Крылов
            elif words[i][len(words[i]) - 2:] == 'дь':
                words[i] = words[i][:len(words[i]) - 2] + 'ть'
            # Крылов
            elif words[i][len(words[i]) - 2:] == 'жь':
                words[i] = words[i][:len(words[i]) - 2] + 'шь'
            # Крылов
            elif words[i][len(words[i]) - 2:] == 'зь':
                words[i] = words[i][:len(words[i]) - 2] + 'сь'

        double_list = ['сс', 'нн', 'мм', 'лл', 'пп', 'зз', 'дд', 'фф', 'тт', 'рр', 'кк']
        single_list = ['с', 'н', 'м', 'л', 'п', 'з', 'д', 'ф', 'т', 'р', 'к']
        for k in range(len(double_list)):
            if double_list[k] in words[i]:
                index = words[i].find(double_list[k])
                if len(words[i]) > index + 2:
                    if words[i][index + 2] in params.consonants:
                        words[i] = words[i].replace(double_list[k], single_list[k])
                if len(words[i]) == index + 2:
                    words[i] = words[i].replace(double_list[k], single_list[k])

        stressed = False
        for j in range(len(words[i])):
            if words[i][j] == '\'':
                stressed = True
                break

        if not stressed:
            vowel_counter = 0
            vowel_index = 0
            for l in range(len(words[i])):
                if words[i][l] in params.vowels:
                    vowel_index = l
                    if vowel_counter > 1:
                        break
                    vowel_counter += 1
            if vowel_counter == 1:
                if len(words[i]) - 1 > vowel_index:
                    words[i] = words[i][:vowel_index + 1] + '\'' + words[i][vowel_index + 1:]
                else:
                    words[i] += '\''

        if stressed:
            for j in range(len(words[i])):
                if j == 0 and len(words[i]) > 1 and words[i][j] == 'о':
                    if words[i][1] in params.consonants or words[i][1] in params.vowels:
                        words[i] = 'а' + words[i][1:]

                curr_letter = words[i][j]
                if last_consonant and (words[i][j] in params.consonants or words[i][j] in params.vowels):
                    # молоко
                    if words[i][j - 1] == 'о':
                        words[i] = words[i][:j - 1] + 'а' + words[i][j:]
                    # тысячи
                    if words[i][j] != 'м':
                        if words[i][j - 1] == 'я':
                            if len(words[i]) > j + 1:
                                if words[i][j + 1] != 'ь':
                                    words[i] = words[i][:j - 1] + 'и' + words[i][j:]

                if curr_letter in params.consonants:
                    last_consonant = True
                    continue
        if words[i][len(words[i]) - 1] == 'о':
            words[i] = words[i][:-1] + 'а'

    return words
