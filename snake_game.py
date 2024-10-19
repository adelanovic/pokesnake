import time
import pygame
import random
import os

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
BLUE = (50, 153, 213)

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000
SNAKE_SIZE = 100
SNAKE_SPEED = 7

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pokesnake')

try:
    pygame.mixer.music.load('music/tiesto1.mp3')
    pygame.mixer.music.play(-1)
except Exception as e:
    print(e)
    pygame.mixer.music.load('music/loop.wav')
    pygame.mixer.music.play(-1)

clock = pygame.time.Clock()

icon_image_path = 'images/pikachu.png'
icon_image = pygame.image.load(icon_image_path)
pygame.display.set_icon(icon_image)

food_image_directory = 'pokemon'
food_images = [f for f in os.listdir(food_image_directory) if f.endswith('.png')]

NEW_FOOD_SIZE = 100

snake_head_image_path = 'images/poke-ball.png'
snake_head_image = pygame.transform.scale(pygame.image.load(snake_head_image_path), (SNAKE_SIZE, SNAKE_SIZE))


def get_random_food_image():
    image_file = random.choice(food_images)
    image_path = os.path.join(food_image_directory, image_file)
    return pygame.transform.scale(pygame.image.load(image_path), (
        NEW_FOOD_SIZE, NEW_FOOD_SIZE)), image_file


# Snake and food behavior
def draw_snake(snake_body, captured_images):
    screen.blit(snake_head_image, (snake_body[0][0], snake_body[0][1]))

    for index, block in enumerate(snake_body[1:]):
        if index < len(captured_images):
            snake_image = pygame.image.load(
                os.path.join(food_image_directory, captured_images[index]))
            snake_image = pygame.transform.scale(snake_image, (SNAKE_SIZE, SNAKE_SIZE))
            screen.blit(snake_image, (block[0], block[1]))


def create_food():
    food_pos = [random.randrange(0, SCREEN_WIDTH // NEW_FOOD_SIZE) * NEW_FOOD_SIZE,
                random.randrange(0, SCREEN_HEIGHT // NEW_FOOD_SIZE) * NEW_FOOD_SIZE]
    food_image, image_name = get_random_food_image()
    return food_pos, food_image, image_name


def display_images(images):
    image_width, image_height = NEW_FOOD_SIZE * 3, NEW_FOOD_SIZE * 3
    x, y = 0, 0
    margin = 10

    for image_name in images:
        image, image_name = get_random_food_image()
        image = pygame.transform.scale(image, (image_width, image_height))

        screen.blit(image, (x, y))

        x += image_width + margin
        if x + image_width > SCREEN_WIDTH:
            x = 0
            y += image_height + margin


# Main game loop
def game_loop():
    game_over = False
    game_close = False

    x = SCREEN_WIDTH // 2
    y = SCREEN_HEIGHT // 2
    x_change = 0
    y_change = 0

    snake_body = [[x, y]]
    snake_length = 1

    captured_images = []

    food_pos, food_image, food_image_name = create_food()
    captured_images.append(food_image_name)

    while not game_over:

        while game_close:
            screen.fill(BLUE)
            font = pygame.font.SysFont("bahnschrift", 35, bold=True)
            display_images(food_images)
            game_over_message = font.render(
                f"You captured {len(captured_images) - 1} Pokemon Mayla or Aydin! Press Q-Quit or C-Play Again. You can do it! I love you!",
                False, BLACK)
            text_width, text_height = game_over_message.get_size()
            x_position = (SCREEN_WIDTH - text_width) // 2
            y_position = (SCREEN_HEIGHT - text_height) // 2
            screen.blit(game_over_message, [x_position, y_position])
            pygame.display.update()
            time.sleep(5)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -SNAKE_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = SNAKE_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP:
                    x_change = 0
                    y_change = -SNAKE_SIZE
                elif event.key == pygame.K_DOWN:
                    x_change = 0
                    y_change = SNAKE_SIZE

        x += x_change
        y += y_change

        # Game over if the snake hits the wall
        if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
            game_close = True

        screen.fill(BLACK)

        screen.blit(food_image, (food_pos[0], food_pos[1]))

        snake_body.insert(0, [x, y])
        if len(snake_body) > snake_length:
            del snake_body[-1]

        for block in snake_body[1:]:
            if block == [x, y]:
                game_close = True

        draw_snake(snake_body, captured_images)

        if abs(x - food_pos[0]) < SNAKE_SIZE and abs(y - food_pos[1]) < SNAKE_SIZE:
            food_pos, food_image, food_image_name = create_food()
            captured_images.append(food_image_name)
            snake_length += 1

        pygame.display.update()

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()


game_loop()
