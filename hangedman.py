"""
1. Добавлена обработка слов с дефисом.
2. Добавлена обработка слов с буквой ё (ввод е = ввод ё).
3. Вывод загаданного слова при победе.
4. Добавлены очки.
5. Помощь стоит 2 очка.
"""

import json
from random import choice, randint


def chose_word():  # Рандомный выбор слова, считывание его темы и подсказки.
    w = choice(words)
    return w, data[w], data[w]["definition"]


def read_json(lang):  # Открытие json и считывание с файла.
    if lang == "ru":
        path = "words.json"
    elif lang == "ua":
        path = "words.json"
    else:
        path = "words.json"

    with open(path, "r", encoding='utf-8') as file:
        data = json.load(file)

    # Создание списка со всеми словами, их темами и подсказками.
    words = []
    for i in data.keys():
        words.append(i)
    return words, data


def validation():  # Обеспечевает правильность ввода
    while True:
        w = input(">>> ").lower()
        if w == "ё":
            w = "е"
        if len(w) != 1:
            print("Введите 1 букву.")
        elif w == "?" or w == "!":
            return w
        elif not w.isalpha():
            print("Введите букву, а не число или символ.")
        else:
            for j in alphabet[lang]:
                if w == j.lower():
                    return w


run = True
mistakes = 0  # Кол-во ошибок
score = 0  # Кол-во очков
lang = "ru"  # Язык
words, data = read_json(lang)
msg = 0
message = ["", "Недостаточно очков."]

# Основной цикл игры
while run:
    word, topic, prompt = chose_word()
    word = "якорёк"
    secret = "_" * len(word)  # Слово из прочерков
    dash = word.find("-")
    if dash != -1:
        secret = secret[:dash] + "-" + secret[dash + 1:]  # Добавление дефиса

    alphabet = {"en": """"
    A B C D E F G H I J K L M 
    N O P Q R S T U V W X Y Z
    """, "ru": ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "Й", "К",
                "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х",
                "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"]}
    letters = []  # Введенные буквы

    print("#" * 15)
    print(word)
    print(prompt)
    print("#" * 15)
    print()

    game = True

    # Раунд игры
    while game:
        # Вывод информации
        for i in secret:
            print(" " + i, end="")
        print("\n")
        n = 0
        for i in alphabet[lang]:
            if n == 10:
                print("")
                n = 0
            print(i, end=" ")
            n += 1
        print("")
        print(f"Ошибки: {mistakes}/7")
        print(f"Очки: {score}")
        print(message[msg])
        msg = 0
        print()

        # Пользовательский ввод и его обработка
        letters.append(validation())
        guessed = False
        if letters[-1] == "?":  # Помощь (открытие 1 буквы)
            if score > 1:
                print()
                score -= 3
                letters[-1] = word[secret.find("_")]
            else:
                msg = 1
                guessed = True
        if letters[-1] == "!":  # Подсказка
            print(prompt)
            letters.append(validation())

        for o in alphabet[lang]:  # Убирает букву из алфавита
            if o == letters[-1].upper():
                alphabet[lang][alphabet[lang].index(o)] = " "
        for i in range(len(word)):
            if word[i] == "ё" and letters[-1] == "е":  # Обрабатывает букву ё
                guessed = True
                secret = secret[:i] + "ё" + secret[i + 1:]
            elif word[i] == letters[-1]:
                guessed = True
                secret = secret[:i] + letters[-1] + secret[i + 1:]
        if not guessed:
            mistakes += 1
        else:
            score += 1

        # Победа.
        if secret.find("_") == -1:
            print("Вы победили!")
            print(f"Слово: {word}")
            game = False

        # Поражение
        if mistakes == 7:
            print("Вы проиграли...")
            print(f"Слово: {word}")
            game = False

    run = False
