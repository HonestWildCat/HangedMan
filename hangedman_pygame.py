import pygame
from pygame.locals import *
import sys
import json
from random import choice, randint
from ctypes import windll

# Иконка и название
pygame.display.set_caption("Hangedman")
pygame.display.set_icon(pygame.image.load("img/icon.ico"))

# Инициализация и музыка
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load('music/Embrace.ogg')
music_volume = pygame.mixer.music.get_volume()
click_sound = pygame.mixer.Sound('music/click.wav')
sound_volume = pygame.mixer.Sound.get_volume(click_sound)


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
        # r = pygame.Rect(start_x + space, start_y + up_space, letter_width, letter_height)
        # pygame.draw.rect(screen, (100, 50, 55), r, letter_height, 5)
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
    def __init__(self, x, y, width, height, color=(0, 0, 0), img="none.png", scale=1, inner_text="", text_color=(0, 0, 0)):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.color = color
        self.text = inner_text
        self.text_color = text_color
        self.rect = pygame.Rect(x, y, width, height)
        self.path = img
        self.scale = scale

    def create_button(self):
        self.write_text()
        pygame.draw.rect(screen, (100, 50, 55), self.rect, 5)
        if self.path == "sound_on.png" or \
                self.path == "sound_off.png" or \
                self.path == "settings.png" or \
                self.path == "music_off.png" or \
                self.path == "music.png":
            img = pygame.transform.scale(pygame.image.load(f'img/{self.path}'),
                                         (50 * relative_w * self.scale, 50 * relative_h * self.scale))
            screen.blit(img, (self.x + w_p * 0.5, self.y))
        elif self.path == "back.png":
            img = pygame.transform.scale(pygame.image.load(f'img/{self.path}'),
                                         (250 * relative_w * self.scale, 125 * relative_h * self.scale))
            screen.blit(img, (self.x, self.y - 2 * h_p))
        elif self.path != "none.png":
            img = pygame.transform.scale(pygame.image.load(f'img/{self.path}'),
                                         (80 * relative_w * self.scale, 80 * relative_h * self.scale))
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
    surface = pygame.Rect(w_p * 46, h_p * 3, w_p * 10, h_p * 8)
    letter_surface = font.render(f"Score: {score}", False, (77, 85, 194))
    screen.blit(letter_surface, surface)


def show_text(surface, text):
    words = text.split(" ")
    start_x, start_y = surface.left, surface.top
    max_width = surface.right
    space = 2 * w_p
    up_space = 13 * h_p
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


lang = "ua"
difficulty = 2
words, data = read_json(lang)
msg = "None"
word, prompt, secret = chose_word(difficulty)
print(word)
print(prompt)

mistakes = 0
b = 7
displayIndex = 0

# Разрешение экрана
display_width = 1600  # windll.user32.GetSystemMetrics(0)
display_height = 900   # windll.user32.GetSystemMetrics(1)
w_p = display_width // 100  # 1 процент от ширины екрана
h_p = display_height // 100  # 1 процент от высоты екрана
relative_w = display_width / 1600  # Относительная ширина
relative_h = display_height / 900  # Относительная высота
print(f"Display: {display_width}x{display_height}")

font = pygame.font.SysFont('Segoi Script.ttf', int(40 * relative_w))

# Сообщения
message = {"ru": {"None": "",
                  "NotEnoughScore": "Недостаточно очков.",
                  "Invalid input": "Введите букву, а не число или символ.",
                  "Victory": "Вы победили!",
                  "Defeat": "Вы проиграли...",
                  "Replay": "Сыграть ещё?",
                  "SelectDifficulty": "Выберите сложность:",
                  "Difficulty": "  0: случайная длинна слова."
                                "\n  1: 1-3 буквы."
                                "\n  2: 4-6 буквы."
                                "\n  3: 7-9 буквы."
                                "\n  4: 10-13 буквы."
                                "\n  5: больше 13 букв."},
           "ua": {"None": "",
                  "NotEnoughScore": "Недостатньо очків.",
                  "Invalid input": "Введіть літеру, а не число або символ.",
                  "Victory": "Ви виграли!",
                  "Defeat": "Ви програли...",
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
                  "Invalid input": "Enter a letter, not a number or symbol.",
                  "Victory": "You won!",
                  "Defeat": "You lost...",
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
back_mode = "game"
victory = False
defeat = False
game_end = False
score = 0
desc = True
menu_opened = False
sound_on = True
music_on = True
keyboard = []
for i in range(len(letters[lang])):
    keyboard.append(f"{i}")

# Кнопки
description = Button(display_width - w_p * 6, display_height - h_p * 10, w_p * 5, h_p * 8.5, (57, 60, 182),
                     "description.png")
hint = Button(w_p * 1, display_height - h_p * 10, w_p * 5, h_p * 8.5, (57, 60, 182), "hint.png")
menu = Button(display_width - w_p * 6, h_p * 2, w_p * 5, h_p * 8.5, (57, 60, 182), "menu.png")
close_description = Button(w_p * 10, h_p * 30, w_p * 80, h_p * 60)
exit_button = Button(w_p * 1, h_p * 2, w_p * 5, h_p * 8.5, (57, 60, 182), "exit.png")
repeat = Button(display_width // 2 - w_p * 5, display_height // 2 + h_p * 15, w_p * 9.5, h_p * 17,
                (57, 60, 182), "repeat.png", 2)
sound_button = Button(display_width - w_p * 5.5, h_p * 11, w_p * 4, h_p * 6, (57, 60, 182), "sound_on.png")
music_button = Button(display_width - w_p * 5.5, h_p * 18, w_p * 4, h_p * 6, (57, 60, 182), "music.png")
settings_button = Button(display_width - w_p * 5.5, h_p * 25, w_p * 4, h_p * 6, (57, 60, 182), "settings.png")
back_button = Button(display_width // 2 - w_p * 6, display_height - 20 * h_p, w_p * 15.5, h_p * 11, (57, 60, 182), "back.png")

# Зацикленная музыка
pygame.mixer.music.play(-1)

while True:
    # Обработка событий
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
            if mode == "game":
                if description.pressed(event.pos):  # Описание
                    click_sound.play()
                    if desc:
                        desc = False
                    else:
                        desc = True
                elif hint.pressed(event.pos):  # Помощь
                    click_sound.play()
                    if mistakes < 7:
                        if score > 1:
                            place = secret.find("_")
                            if place != -1:
                                score -= 2
                                h = word[place]
                                print(h)
                                secret = secret[:place] + h + secret[place + 1:]
                                for i in letters[lang]:
                                    if i == h:
                                        i = " "
                elif exit_button.pressed(event.pos):  # Выход кнопкой
                    click_sound.play()
                    pygame.quit()
                    sys.exit()
                elif close_description.pressed(event.pos) and desc:  # Закрыть описание
                    click_sound.play()
                    desc = False
                elif menu.pressed(event.pos):  # Меню
                    click_sound.play()
                    if menu_opened:
                        menu_opened = False
                    else:
                        menu_opened = True
                else:  # Нажатие на алфавит
                    if not desc:
                        for j in range(len(keyboard)):
                            if keyboard[j].pressed(event.pos):
                                if letters[lang][j] != " ":
                                    click_sound.play()
                                    guesed = False
                                    for i in range(len(word)):
                                        if word[i] == letters[lang][j]:
                                            guesed = True
                                            secret = secret[:i] + letters[lang][j] + secret[i + 1:]
                                            score += 1
                                    print(letters[lang][j])
                                    letters[lang][j] = " "
                                    if not guesed:
                                        if mistakes < 7:
                                            mistakes += 1
                if menu_opened:
                    if sound_button.pressed(event.pos):  # Звук
                        click_sound.play()
                        if sound_on:
                            sound_button.path = "sound_off.png"
                            pygame.mixer.Sound.set_volume(click_sound, 0)
                            sound_on = False
                        else:
                            sound_button.path = "sound_on.png"
                            pygame.mixer.Sound.set_volume(click_sound, sound_volume)
                            sound_on = True
                    elif music_button.pressed(event.pos):  # Музыка
                        click_sound.play()
                        if music_on:
                            music_button.path = "music_off.png"
                            pygame.mixer.music.set_volume(0)
                            music_on = False
                        else:
                            music_button.path = "music.png"
                            pygame.mixer.music.set_volume(music_volume)
                            music_on = True
                    elif settings_button.pressed(event.pos):  # Настройки
                        click_sound.play()
                        back_mode = mode
                        mode = "settings"
                if game_end:  # Новая игра
                    if repeat.pressed(event.pos):
                        click_sound.play()
                        game_end = False
                        victory = False
                        defeat = False
                        mistakes = 0
                        words, data = read_json(lang)
                        word, prompt, secret = chose_word(difficulty)
                        print(word)
                        print(prompt)
                        desc = True
                        letters = {"en": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
                                          "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
                                          "W", "X", "Y", "Z"],
                                   "ru": ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К",
                                          "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х",
                                          "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"],
                                   "ua": ["А", "Б", "В", "Г", "Ґ", "Д", "Е", "Є", "Ж", "З",
                                          "И", "І", "Ї", "Й", "К", "Л", "М", "Н", "О", "П", "Р",
                                          "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ь", "Ю", "Я"]}
            elif mode == "settings":
                if back_button.pressed(event.pos):  # Назад
                    click_sound.play()
                    mode = back_mode
                    mode = "game"

    # Сама игра
    background()
    if mode == "game":
        if game_end:
            repeat.create_button()
            f = pygame.font.SysFont('Segoi Script.ttf', 100)
            if victory:
                w_width, w_height = (font.render(message[lang]["Victory"], False, (77, 85, 194)).get_size())
                screen.blit(f.render(message[lang]["Victory"], False, (77, 85, 194)),
                            (display_width // 2 - w_width - w_p * 2, display_height // 2 - w_height))
            else:
                w_width, w_height = (font.render(message[lang]["Defeat"], False, (77, 85, 194)).get_size())
                screen.blit(f.render(message[lang]["Defeat"], False, (77, 85, 194)),
                            (display_width // 2 - w_width - w_p * 2, display_height // 2 - w_height))

        else:
            alphabet()
            hangedman()
            # Описание
            if desc:
                description_rect = pygame.Rect(w_p * 10, h_p * 30, w_p * 80, h_p * 60)
                description_img = pygame.transform.scale(pygame.image.load('img/description/desc_bg1.png'),
                                                                          (w_p * 84, h_p * 65))
                screen.blit(description_img, (w_p * 8, h_p * 28))
                f = pygame.font.SysFont('Segoi Script.ttf', 30)
                h = f.render(prompt, True, (0, 0, 0))
                show_text(description_rect, prompt)
            # Конец раунда.
            if secret.find("_") == -1 or mistakes > 6:
                if mistakes > 6:
                    defeat = True
                else:
                    victory = True
                secret = word
                game_end = True
        secret_word()
        description.create_button()
        hint.create_button()
        menu.create_button()
        exit_button.create_button()
        show_score()
        if menu_opened:
            menu_img = pygame.transform.scale(pygame.image.load('img/menu_holder.png'),
                                                               (90 * relative_w, 250 * relative_h))
            screen.blit(menu_img, (display_width - w_p * 6.3, h_p * 7))
            sound_button.create_button()
            music_button.create_button()
            settings_button.create_button()
    elif mode == "settings":  # Настройки
        back_button.create_button()

    pygame.display.update()
    pygame.display.flip()
