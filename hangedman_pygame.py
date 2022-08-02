import pygame
from pygame.locals import *
import sys
import json
from random import choice, randint
from ctypes import windll

pygame.init()


def chose_word(difficulty):  # Рандомный выбор слова, считывание его темы и подсказки.
    if difficulty == 0:  # Выбор слова по сложности
        w = choice(words[randint(0, 4)])
    else:
        w = choice(words[difficulty - 1])
    secret_word = "_" * len(w)
    dash = w.find("-")
    if dash != -1:
        secret_word = secret_word[:dash] + "-" + secret_word[dash + 1:]  # Добавление дефиса
    return w.upper(), data[w]["definition"], secret_word.upper()


def read_json(language):  # Открытие json и считывание с файла.
    path = f"words_{lang}.json"
    with open(path, "r", encoding='utf-8') as file:
        data = json.load(file)

    # Создание списка со всеми словами, их темами и подсказками.
    words = [[], [], [], [], []]
    for i in data.keys():
        length = len(i)
        if length < 4:
            words[0].append(i)
        elif length < 7:
            words[1].append(i)
        elif length < 10:
            words[2].append(i)
        elif length < 14:
            words[3].append(i)
        else:
            words[4].append(i)
    return words, data


def alphabet():
    font = pygame.font.SysFont('Segoi Script.ttf', int(100 * relative_w))
    # Определение пределов для вывода алфавита
    surface = pygame.Rect(display_width - w_p * 57, display_height - h_p * 65, w_p * 50, h_p * 68)
    max_width, max_height = surface.right, surface.bottom
    # Начальные точки
    start_x = surface.left + w_p
    start_y = surface.top + h_p
    space = 0
    up_space = 0
    if lang in ["ru", "ua"]:
        letter_width, letter_height = font.render("Щ", False, (77, 85, 194)).get_size()[0], \
                                      font.render("Й", False, (77, 85, 194)).get_size()[1]
    else:
        letter_width, letter_height = font.render("W", False, (77, 85, 194)).get_size()
    # Вывод в цикле
    n = 0
    for letter in letters[lang]:
        letter_surface = font.render(letter, False, (77, 85, 194))
        if start_x + space + letter_width >= max_width:
            up_space += letter_height + h_p
            space = 0
        screen.blit(letter_surface, (start_x + space, start_y + up_space))
        keyboard[n] = Button(start_x + space, start_y + up_space, letter_width, letter_height)
        space += letter_width + 2 * w_p
        n += 1


def secret_word():
    font = pygame.font.SysFont('Segoi Script.ttf', int(110 * relative_w))

    surface = pygame.Rect(w_p * 5, h_p * 13, w_p * 90, h_p * 10)
    start_y = surface.top + h_p
    space = 0
    if lang in ["ru", "ua"]:
        letter_width, letter_height = font.render("Ш", False, (77, 85, 194)).get_size()[0], \
                                      font.render("Й", False, (77, 85, 194)).get_size()[1]
    else:
        letter_width, letter_height = font.render("W", False, (77, 85, 194)).get_size()
    word_width = len(secret) * (letter_width + w_p)
    # Вывод в цикле
    for letter in secret:
        letter_surface = font.render(letter, False, (77, 85, 194))
        screen.blit(letter_surface, ((display_width / 2) - (word_width / 2) + space, start_y))
        space += letter_width + w_p


class Button:  # Создает кнопку и выполняет действия при её нажатии
    def __init__(self, x, y, width, height, color=(0, 0, 0), img="none.png", inner_text="", text_color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.text = inner_text
        self.text_color = text_color
        self.rect = pygame.Rect(x, y, width, height)
        self.path = img

    def create_button(self):
        self.write_text()
        if self.path != "none.png":
            img = pygame.transform.scale(pygame.image.load(f'img/{self.path}'), (80 * relative_w, 80 * relative_h))
            screen.blit(img, (self.x, self.y - 0.2 * h_p))

    def write_text(self):
        pass

    def pressed(self, mouse):
        if self.rect.bottomright[0] > mouse[0] > self.rect.topleft[0]:
            if self.rect.bottomright[1] > mouse[1] > self.rect.topleft[1]:
                return True
            else:
                return False
        else:
            return False


def show_score():
    font = pygame.font.SysFont('Segoi Script.ttf', int(40 * relative_w))
    surface = pygame.Rect(w_p * 2, h_p * 3, w_p * 10, h_p * 8)
    letter_surface = font.render(f"Score: {score}", False, (77, 85, 194))
    screen.blit(letter_surface, surface)


def show_text(surface, text):
    font = pygame.font.SysFont('Segoi Script.ttf', int(40 * relative_w))
    words = text.split(" ")
    start_x, start_y = surface.left, surface.top
    max_width = surface.right
    space = 2 * w_p
    up_space = 5 * h_p
    letter_height = font.render("Й", False, (77, 85, 194)).get_size()[1]
    for word in words:
        word_width = font.render(word + " ", False, (77, 85, 194)).get_size()[0]
        if start_x + space + word_width >= max_width:
            up_space += letter_height + h_p
            space = 2 * w_p

        word_surface = font.render(word + " ", False, (77, 85, 194))
        screen.blit(word_surface, (start_x + space, start_y + up_space))
        space += word_width


def resizeDisplay(display_width, display_height):  # Изменение размера окна
    display_width = display_width + 16 * displayIndex
    display_height = display_height + 9 * displayIndex
    print(display_width, display_height)
    screen = pygame.display.set_mode((display_width, display_height))


def background():  # Фон
    bg_variations = ["blank_1.jpg", "blank_3.jpg", "blank_5.jpg", "blank_6.jpg",  # Простая
                     "crumpled_1.jpg", "crumpled_2.jpg",                          # Мятая
                     "squared_1.jpg", "squared_2.jpg", "squared_3.jpg",           # В клеточку
                     "cardboard_2.jpg", "cardboard_4.jpg", "cardboard_5.jpg"]     # Картон
    bg = pygame.transform.scale(pygame.image.load(f'img/bg/{bg_variations[b]}'), (display_width, display_height))
    screen.blit(bg, (0, 0))


def hangedman():  # Отображение виселицы
    animation = ["0.png", "1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png"]
    hangedman = pygame.image.load(f'img/animation/{animation[mistakes]}')
    hangedman_scaled = pygame.transform.scale(hangedman,
                                              (450 * relative_w,
                                               650 * relative_h))
    screen.blit(hangedman_scaled, (w_p * 7, display_height - 650 * relative_h - h_p * 2))


def markup():  # Разметка прямоугольниками
    # r = pygame.Rect(w_p * 1, h_p * 2, w_p * 10, h_p * 8)
    # pygame.draw.rect(screen, (100, 50, 55), r, 5)

    r1 = pygame.Rect(w_p * 25, h_p * 1, w_p * 50, h_p * 6)
    pygame.draw.rect(screen, (100, 50, 55), r1, 5)

    # r2 = pygame.Rect(display_width - w_p * 6, h_p * 2, w_p * 5, h_p * 8)
    # pygame.draw.rect(screen, (100, 50, 55), r2, 5)

    # r3 = pygame.Rect(w_p * 5, h_p * 13, w_p * 90, h_p * 10)
    # pygame.draw.rect(screen, (100, 50, 55), r3, 5)

    # r4 = pygame.Rect(w_p * 7, display_height - h_p * 72, w_p * 30, h_p * 68)
    # pygame.draw.rect(screen, (100, 50, 55), r4, 5)

    # r5 = pygame.Rect(display_width - w_p * 57, display_height - h_p * 72, w_p * 50, h_p * 68)
    # pygame.draw.rect(screen, (100, 50, 55), r5, 5)

    # r6 = pygame.Rect(w_p * 1, display_height - h_p * 10, w_p * 5, h_p * 8)
    # pygame.draw.rect(screen, (100, 50, 55), r6, 5)

    # r7 = pygame.Rect(display_width - w_p * 6, display_height - h_p * 10, w_p * 5, h_p * 8)
    # pygame.draw.rect(screen, (100, 50, 55), r7, 5)


lang = "ru"
difficulty = 2
words, data = read_json(lang)
msg = "None"
word, prompt, secret = chose_word(difficulty)
print(word)
print(prompt)

mistakes = 0
b = 4
displayIndex = 0

# Разрешение экрана
display_width = 1600  # windll.user32.GetSystemMetrics(0)
display_height = 900   # windll.user32.GetSystemMetrics(1)
w_p = display_width // 100  # 1 процент от ширины екрана
h_p = display_height // 100  # 1 процент от высоты екрана
relative_w = display_width / 1600  # Относительная ширина
relative_h = display_height / 900  # Относительная высота
print(f"Display: {display_width}x{display_height}")

# Сообщения
message = {"ru": {"None": "",
                  "NotEnoughScore": "Недостаточно очков.",
                  "TooManyLetters": "Введите 1 букву.",
                  "Invalid input": "Введите букву, а не число или символ.",
                  "Mistakes": "Ошибки",
                  "Points": "Очки",
                  "Victory": "Вы победили!",
                  "Defeat": "Вы проиграли...",
                  "Word": "Слово:",
                  "Replay": "Сыграть ещё?",
                  "SelectDifficulty": "Выберите сложность:",
                  "InvalidNumber": "Неверный ввод.",
                  "Difficulty": "  0: случайная длинна слова."
                                "\n  1: 1-3 буквы."
                                "\n  2: 4-6 буквы."
                                "\n  3: 7-9 буквы."
                                "\n  4: 10-13 буквы."
                                "\n  5: больше 13 букв."},
           "ua": {"None": "",
                  "NotEnoughScore": "No",
                  "TooManyLetters": "Введіть 1 літеру.",
                  "Invalid input": "Введіть літеру, а не число або символ.",
                  "Mistakes": "Помилки",
                  "Points": "Очки",
                  "Victory": "Вы виграли!",
                  "Defeat": "Вы програли...",
                  "Word": "Слово:",
                  "Replay": "Грати ще?",
                  "SelectDifficulty": "Оберіть складність:",
                  "InvalidNumber": "Неправильне введення.",
                  "Difficulty": "  0: випадкова довжина слова."
                                "\n  1: 1-3 літери."
                                "\n  2: 4-6 літер."
                                "\n  3: 7-9 літер."
                                "\n  4: 10-13 літер."
                                "\n  5: більше 13 літер."
                  },
           "en": {"None": "",
                  "NotEnoughScore": "Not enough points.",
                  "TooManyLetters": "Input 1 letter.",
                  "Invalid input": "Enter a letter, not a number or symbol.",
                  "Mistakes": "Mistakes",
                  "Points": "Points",
                  "Victory": "You won!",
                  "Defeat": "You lost...",
                  "Word": "Word:",
                  "Replay": "Play again?",
                  "SelectDifficulty": "Select difficulty:",
                  "InvalidNumber": "Invalid input.",
                  "Difficulty": "  0: random word length."
                                "\n  1: 1-3 letters."
                                "\n  2: 4-6 letters."
                                "\n  3: 7-9 letters."
                                "\n  4: 10-13 letters."
                                "\n  5: more than 13 letters."
                  }}

"""
Список шрифтов на букву 'Б'
lst = pygame.font.get_fonts()
for i in lst:
    if i[0] == "B" or i[0] == "b":
        print(i)"""

# Разрешение окна приложения
screen = pygame.display.set_mode((display_width, display_height))

letters = {"en": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
                  "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
                  "W", "X", "Y", "Z"],
           "ru": ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К",
                  "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х",
                  "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"],
           "ua": ["А", "Б", "В", "Г", "Ґ", "Д", "Е", "Є", "Ж", "З",
                  "И", "І", "Ї", "Й", "К", "Л", "М", "Н", "О", "П", "Р",
                  "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ь", "Ю", "Я"]}


# Игровые переменные
mode = "game"
score = 0
desc = False
keyboard = []
for i in range(len(letters[lang])):
    keyboard.append(f"{i}")
f = pygame.font.SysFont('Segoi Script.ttf', 30)

# Кнопки
description = Button(display_width - w_p * 6, display_height - h_p * 10, w_p * 5, h_p * 8.5, (57, 60, 182),
                     "description.png")
hint = Button(w_p * 1, display_height - h_p * 10, w_p * 5, h_p * 8.5, (57, 60, 182), "hint.png")
menu = Button(display_width - w_p * 6, h_p * 2, w_p * 5, h_p * 8.5, (57, 60, 182), "menu.png")
close_description = Button(w_p * 10, h_p * 30, w_p * 80, h_p * 60)
while True:
    for event in pygame.event.get():
        # Выход
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:  # Если нажата кнопка
            # Изменение фона(вниз) и анимации(вверх)
            if event.key == K_UP:
                mistakes += 1
                if mistakes == 8:
                    mistakes = 0
            elif event.key == K_DOWN:
                b += 1
                if b == 12:
                    b = 0
            # Смена размера приложения
            elif event.key == K_LEFT:
                displayIndex -= 1
                resizeDisplay(display_width, display_height)
            elif event.key == K_RIGHT:
                displayIndex += 1
                resizeDisplay(display_width, display_height)
        elif event.type == MOUSEBUTTONDOWN:  # Если нажата кнопка мыши
            if description.pressed(event.pos):
                print("description")
                desc = True
            elif hint.pressed(event.pos):
                if score > 1:
                    score -= 2
                    place = secret.find("_")
                    h = word[place]
                    print(h)
                    secret = secret[:place] + h + secret[place + 1:]
                    for i in letters[lang]:
                        if i == h:
                            i = " "
            elif menu.pressed(event.pos):
                print("menu")
            elif close_description.pressed(event.pos) and desc:
                desc = False
            else:  # Нажатие на алфавит
                for j in range(len(keyboard)):
                    if keyboard[j].pressed(event.pos):
                        print(j)
                        guesed = False
                        for i in range(len(word)):
                            if word[i] == letters[lang][j]:
                                guesed = True
                                secret = secret[:i] + letters[lang][j] + secret[i + 1:]
                                score += 1
                        letters[lang][j] = " "
                        if not guesed:
                            if mistakes < 7:
                                mistakes += 1
    background()
    if mode == "game":
        markup()
        alphabet()
        secret_word()
        hangedman()
        description.create_button()
        hint.create_button()
        menu.create_button()
        show_score()
        # Описание
        if desc:
            description_rect = pygame.Rect(w_p * 10, h_p * 30, w_p * 80, h_p * 60)
            pygame.draw.rect(screen, (255, 255, 255), description_rect)
            f = pygame.font.SysFont('Segoi Script.ttf', 30)
            h = f.render(prompt, True, (0, 0, 0))
            show_text(description_rect, prompt)
        # Победа.
        if secret.find("_") == -1 and mistakes < 7:
            h = f.render(message[lang]["Victory"], True, (0, 0, 0))
            screen.blit(h, (w_p * 3, h_p * 25))

        # Поражение
        if mistakes == 7:
            h = f.render(message[lang]["Defeat"], True, (0, 0, 0))
            screen.blit(h, (w_p * 3, h_p * 25))

    pygame.display.update()
    pygame.display.flip()
