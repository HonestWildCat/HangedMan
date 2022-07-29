import pygame
import random
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

# Группировка спрайтов
all_sprites = pygame.sprite.Group()

# Цвета
blue = (0, 48, 143)
yellow = (255, 191, 0)
red = (138, 3, 3)

start = datetime.now().second

# Цикл игры
running = True
while running:
    clock.tick(FPS)

    # Обновление
    all_sprites.update()
    all_sprites.draw(screen)

    now = datetime.now().second
    print(start, now)
    if now + 57 < start:
        start = now
    if now < start + 2:
        screen.fill(blue)
        pygame.display.flip()
    elif now < start + 4:
        screen.fill(yellow)
        pygame.display.flip()
    elif now < start + 6:
        screen.fill(red)
        pygame.display.flip()
    else:
        start = now

    for event in pygame.event.get():

        # проверить закрытие окна
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
