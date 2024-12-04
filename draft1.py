import pygame
import random
import time

from draft2 import basket_width, basket_height, basket_x

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лови яблоки!")

#загрузка изображений и хитбокса
background = pygame.image.load("images/background.jpg")
apple = pygame.image.load("images/apple2.png")
bomb = pygame.image.load("images/bomb.png")
basket = pygame.image.load("images/basket3.png")

apple_rect = apple.get_rect()
bomb_rect = bomb.get_rect()
basket_rect = basket.get_rect()


#Корзина
basket_rect_width = 80
basket_rect_height = 20
basket_x = WIDTH//2 - basket_rect_width // 2
basket_y = HEIGHT - basket_rect_height - 10
basket_speed = 10

#Спрайты
items = []
item_size = 40
item_speed = 5
pygame.transform.scale(apple, (item_size, item_size))
pygame.transform.scale(bomb, (item_size, item_size))
pygame.transform.scale(basket, (item_size, item_size))


#Игровые переменные
lives = 3
score = 0
target_score = 20

font = pygame.font.Font (None,36)

#Создание предметов
def spawn_item():
    x_pos = random.randint(0, WIDTH - item_size)
    return [x_pos, -item_size, random.choice(['apple', 'bomb'])]

#Создание корзины
def draw_basket():
    if basket_rect:
        screen.blit(basket, basket_rect, (basket_x, basket_y))
    else:
        pygame.draw.rect(screen, "black", (basket_x, basket_y, basket_width, basket_height))

#Рисуем предметы или их замену
def draw_items():
    for item in items:
        if item[2] == 'apple':
            if apple_rect:
                screen.blit(apple, apple_rect, (item[0], item[1]))
            else:
                pygame.draw.circle(screen, "red", (item[0], item[1], item_size, item_size), 20)
        else:
            if bomb_rect:
                screen.blit(bomb, bomb_rect, (item[0], item[1]))
            else:
                pygame.draw.circle(screen, 'black', (item[0], item[1], item_size, item_size), 20)

#Для текста в конце игры
def display_message(message):
    text_surface = font.render(message, True, "black")
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    time.sleep(10)  # Задержка на 10 секунд


clock = pygame.time.Clock()


run = True

# Начальная генерация предметов
for _ in range(5):
        items.append(spawn_item())

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    # Управление корзинкой
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and basket_x > 0:
        basket_x -= basket_speed
    if keys[pygame.K_RIGHT] and basket_x < WIDTH:
        basket_x += basket_speed

        # Обновление позиции предметов и проверка на столкновения
        for item in items[:]:
            item[1] += item_speed

            # Проверка на столкновение с корзинкой
            if (item[1] + item_size > basket_y and
                    item[1] < basket_y + basket_height and
                    item[0] + item_size > basket_x and
                    item[0] < basket_x + basket_width):

                if item[2] == 'apple':
                    score += 1
                else:
                    lives -= 1

                items.remove(item)

            # Если предмет вышел за пределы экрана
            if item[1] > HEIGHT:
                items.remove(item)

        # Спавн новых предметов
        if len(items) < 5:
            items.append(spawn_item())

        # Отображение элементов на экране
        screen.blit(background, (0, 0))
        draw_basket()
        draw_items()

        # Отображение счета и жизней
        score_text = font.render(f"Счет: {score}", True, 'black')
        lives_text = font.render(f"Жизни: {lives}", True, 'black')
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        # Проверка условий окончания игры
        if score >= target_score:
            display_message("Вы победили!")
            run = False

        if lives <= 0:
            display_message("Вы проиграли!")
            run = False


    clock.tick(15)
    pygame.display.flip()


pygame.quit()



