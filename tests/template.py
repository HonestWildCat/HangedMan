import pygame
from datetime import datetime

WIDTH = 360  # ширина игрового окна
HEIGHT = 480  # высота игрового окна
FPS = 30  # частота кадров в секунду

# создаем игру и окно
pygame.init()
pygame.mixer.init()  # для звука
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Цвета
blue = (0, 48, 143)
yellow = (255, 191, 0)
red = (138, 3, 3)

start = datetime.now().second

# Цикл игры
running = True
while running:
    #  Установка FPS
    clock.tick(FPS)

    # Прохождение по списку событий
    for event in pygame.event.get():

        # Проверка закрытия окна
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
