import pygame
from pygame.locals import *
import sys
from ctypes import windll
from datetime import datetime


def show_text(surface, text, pos, font, color=pygame.Color('black')):
    max_width, max_height = surface.get_size()
    x, y = pos
    words = []
    w = ""
    for i in text:
        w = w + " " + i
        if len(w) == 20 or i == "Я":
            words.append(w)
            w = ""
    for word in words:
        word_surface = font.render(word, 0, color)
        word_width, word_height = word_surface.get_size()
        if x + word_width >= max_width:
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
        surface.blit(word_surface, (x, y))
        x += word_width + w_p
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def resizeDisplay(display_width, display_height):
    display_width = display_width + 16 * displayIndex
    display_height = display_height + 9 * displayIndex
    print(display_width, display_height)
    screen = pygame.display.set_mode((display_width, display_height))


pygame.init()
mistakes = 0
displayIndex = 0

# Разрешение экрана
display_width = 1600  # windll.user32.GetSystemMetrics(0)
display_height = 900   # windll.user32.GetSystemMetrics(1)
w_p = display_width // 100  # 1 процент от ширины екрана
h_p = display_height // 100  # 1 процент от высоты екрана
relative_w = display_width / 1600  # Относительная ширина
relative_h = display_height / 900  # Относительная высота
print(f"Display: {display_width}x{display_height}")
"""
Список шрифтов на букву 'Б'
lst = pygame.font.get_fonts()
for i in lst:
    if i[0] == "B" or i[0] == "b":
        print(i)"""

# Разрешеное окна приложения
screen = pygame.display.set_mode((display_width, display_height))

alphabet = {"en": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
                   "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
                   "W", "X", "Y", "Z"],
            "ru": ["А", "Б", "В", "Г", "Д", "Е", "Ё", "Ж", "З", "И", "Й", "К",
                   "Л", "М", "Н", "О", "П", "Р", "С", "Т", "У", "Ф", "Х",
                   "Ц", "Ч", "Ш", "Щ", "Ъ", "Ы", "Ь", "Э", "Ю", "Я"],
            "ua": ["А", "Б", "В", "Г", "Ґ", "Д", "Е", "Є", "Ж", "З",
                   "И", "І", "Ї", "Й", "К", "Л", "М", "Н", "О", "П", "Р",
                   "С", "Т", "У", "Ф", "Х", "Ц", "Ч", "Ш", "Щ", "Ь", "Ю", "Я"]}

# Фон
bg_variations = ["blank_1.jpg", "blank_2.jpg", "purple.jpg", "squared_1.jpg"]
bg = pygame.transform.scale(pygame.image.load(f'img/bg/{bg_variations[3]}'), (display_width, display_height))
screen.blit(bg, (0, 0))

# Виселица
animation = ["0.png", "1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png"]
hangedman = pygame.image.load(f'img/animation/{animation[mistakes]}')
hangedman_scaled = pygame.transform.scale(hangedman,
                                          (450 * relative_w,
                                           650 * relative_h))
screen.blit(hangedman_scaled, (w_p * 7, display_height - 650 * relative_h - h_p * 2))

# Шрифт
t = ""
for i in alphabet["ru"]:
    t = t + " " + i
font = pygame.font.SysFont('Segoi Script.ttf', 80)
text = font.render(t, True, (0, 250, 20))
# screen.blit(text, (display_width - w_p * 55, display_height // 3))

# Прямоугольник
r = pygame.Rect(w_p * 1, h_p * 2, w_p * 10, h_p * 8)
pygame.draw.rect(screen, (100, 50, 55), r, 5)

r1 = pygame.Rect(w_p * 25, h_p * 1, w_p * 50, h_p * 6)
pygame.draw.rect(screen, (100, 50, 55), r1, 5)

r2 = pygame.Rect(display_width - w_p * 6, h_p * 2, w_p * 5, h_p * 8)
pygame.draw.rect(screen, (100, 50, 55), r2, 5)

r3 = pygame.Rect(w_p * 5, h_p * 13, w_p * 90, h_p * 10)
pygame.draw.rect(screen, (100, 50, 55), r3, 5)

r4 = pygame.Rect(w_p * 7, display_height - h_p * 72, w_p * 30, h_p * 68)
pygame.draw.rect(screen, (100, 50, 55), r4, 5)

r5 = pygame.Rect(display_width - w_p * 57, display_height - h_p * 72, w_p * 50, h_p * 68)
pygame.draw.rect(screen, (100, 50, 55), r5, 5)

r6 = pygame.Rect(w_p * 1, display_height - h_p * 10, w_p * 5, h_p * 8)
pygame.draw.rect(screen, (100, 50, 55), r6, 5)

r7 = pygame.Rect(display_width - w_p * 6, display_height - h_p * 10, w_p * 5, h_p * 8)
pygame.draw.rect(screen, (100, 50, 55), r7, 5)

# Игровые переменные
mistakes = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                displayIndex -= 1
                if displayIndex < 0:
                    displayIndex = 0
                resizeDisplay(display_width, display_height)
            elif event.key == K_RIGHT:
                displayIndex += 1
                resizeDisplay(display_width, display_height)
    show_text(screen, alphabet["ru"], (display_width - w_p * 55, display_height // 3), font)
    pygame.display.update()
    pygame.display.flip()
