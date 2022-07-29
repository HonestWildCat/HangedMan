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
lang = "ru"  # Язык
words, data = read_json(lang)

# Основной цикл игры
while run:
    word, topic, prompt = chose_word()
    alphabet = {"en": """"
    A B C D E F G H I J K L M 
    N O P Q R S T U V W X Y Z
    """, "ru": ["А", "Б", "В", "Г", "Д", "Е", "Ж", "З", "И", "Й", "К",
                "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х",
                "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"]}
    secret = "_" * len(word)  # Слово из прочерков
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
        print()

        # Пользовательский ввод и его обработка
        letters.append(validation())
        guessed = False
        if letters[-1] == "?":
            print()
            letters[-1] = word[randint(0, len(word) - 1)]
        if letters[-1] == "!":
            print(prompt)
            letters.append(validation())

        for o in alphabet[lang]:
            if o == letters[-1].upper():
                alphabet[lang][alphabet[lang].index(o)] = " "
        for i in range(len(word)):
            if word[i] == letters[-1]:
                guessed = True
                secret = secret[:i] + letters[-1] + secret[i + 1:]
        if not guessed:
            mistakes += 1

        # Победа.
        if secret.find("_") == -1:
            print("Вы победили!")
            game = False

        # Поражение
        if mistakes == 7:
            print("Вы проиграли...")
            print(f"Слово: {word}")
            game = False

    run = False
