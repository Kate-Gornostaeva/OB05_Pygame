import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Лови яблоки!")

# Загрузка изображений
background = pygame.image.load("images/background.jpg")
apple = pygame.image.load("images/apple2.png")
bomb = pygame.image.load("images/bomb.png")
basket = pygame.image.load("images/basket.png")

# Изменение размера изображений
item_size = 50
apple = pygame.transform.scale(apple, (item_size, item_size))
bomb = pygame.transform.scale(bomb, (item_size, item_size))
basket = pygame.transform.scale(basket, (120, 50))  # Размер корзины

# Корзина
basket_x = WIDTH // 2 - 50  # Центрируем корзину
basket_y = HEIGHT - 50
basket_speed = 15
basket_height = 20

# Спрайты
items = []
item_speed = 13

# Игровые переменные
lives = 3
score = 0
target_score = 20

font = pygame.font.Font(None, 36)

# Создание предметов
def spawn_item():
    x_pos = random.randint(0, WIDTH - item_size)
    return [x_pos, -item_size, random.choice(['apple', 'bomb'])]

# Создание корзины
def draw_basket():
    screen.blit(basket, (basket_x, basket_y))

# Рисуем предметы или их замену
def draw_items():
    for item in items:
        if item[2] == 'apple':
            screen.blit(apple, (item[0], item[1]))
        else:
            screen.blit(bomb, (item[0], item[1]))

# Для текста в конце игры
def display_message(message):
    text_surface = font.render(message, True, "black")
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    time.sleep(3)  # Задержка на 3 секунды

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
    if keys[pygame.K_RIGHT] and basket_x < WIDTH - 100:  # Учитываем ширину корзины
        basket_x += basket_speed

    # Обновление позиции предметов и проверка на столкновения
    for item in items[:]:
        item[1] += item_speed

        # Проверка на столкновение с корзинкой
        if (item[1] + item_size > basket_y and
                item[1] < basket_y + basket_height and
                item[0] + item_size > basket_x and
                item[0] < basket_x + 100):  # Учитываем ширину корзины

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
    screen.blit(background, (0, 0))  # Сначала рисуем фон
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

    pygame.display.flip()
    clock.tick(20)

pygame.quit()