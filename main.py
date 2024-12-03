import pygame
import random

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лови яблоки!")

background = pygame.image.load("images/background.jpg")
apple = pygame.image.load("images/apple2.png")
bomb = pygame.image.load("images/bomb.png")
basket = pygame.image.load("images/basket3.png")

apple_rect = apple.get_rect()
bomb_rect = bomb.get_rect()
basket = basket.get_rect()




run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    keys = pygame.key.get_pressed()

    screen.blit(background, (0,0))

    pygame.display.flip()




pygame.quit()



