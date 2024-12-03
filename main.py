import pygame
import random

# Инициализация Pygame
pygame.init()


# Настройки экрана
window_size = 800, 600
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Лови яблоки!")

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Игрок
basket_width = 100
basket_height = 20
basket_x = WIDTH // 2 - basket_width // 2
basket_y = HEIGHT - basket_height - 10
basket_speed = 10

# Предметы
items = []
item_size = 30
item_speed = 5

# Игровые переменные
score = 0
lives = 3
target_score = 20

# Шрифты
font = pygame.font.Font(None, 36)


def spawn_item():
    x_pos = random.randint(0, WIDTH - item_size)
    return [x_pos, -item_size, random.choice(['apple', 'other'])]


def draw_basket():
    pygame.draw.rect(screen, GREEN, (basket_x, basket_y, basket_width, basket_height))


def draw_items():
    for item in items:
        if item[2] == 'apple':
            pygame.draw.rect(screen, RED, (item[0], item[1], item_size, item_size))
        else:
            pygame.draw.rect(screen, BLACK, (item[0], item[1], item_size, item_size))


def main():
    global basket_x, score, lives

    clock = pygame.time.Clock()
    running = True

    # Начальная генерация предметов
    for _ in range(5):
        items.append(spawn_item())

    while running:
        screen.fill(WHITE)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление корзинкой
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and basket_x > 0:
            basket_x -= basket_speed
        if keys[pygame.K_RIGHT] and basket_x < WIDTH - basket_width:
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
        draw_basket()
        draw_items()

        # Отображение счета и жизней
        score_text = font.render(f"Счет: {score}", True, BLACK)
        lives_text = font.render(f"Жизни: {lives}", True, BLACK)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        # Проверка условий окончания игры
        if score >= target_score:
            print("Вы выиграли!")
            running = False

        if lives <= 0:
            print("Вы проиграли!")
            running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()