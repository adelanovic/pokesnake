import time

import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
BLUE = (50, 153, 213)

# Set screen dimensions and snake size
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1000
SNAKE_SIZE = 100
SNAKE_SPEED = 6

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pokesnake')
pygame.mixer.music.load('music/tiesto.mp3')
pygame.mixer.music.play(-1)
clock = pygame.time.Clock()

icon_image_path = 'images/pikachu.png'
icon_image = pygame.image.load(icon_image_path)
pygame.display.set_icon(icon_image)

food_image_directory = 'pokemon'
food_images = [f for f in os.listdir(food_image_directory) if f.endswith('.png')]

# Define the new food image size
# Food size and snake size will probably always be the same
NEW_FOOD_SIZE = 100

snake_head_image_path = 'images/poke-ball.png'
snake_head_image = pygame.transform.scale(pygame.image.load(snake_head_image_path), (SNAKE_SIZE, SNAKE_SIZE))

# Function to load and scale a random food image
def get_random_food_image():
    image_file = random.choice(food_images)  # Pick a random food image from the directory
    image_path = os.path.join(food_image_directory, image_file)  # Get the full path to the food image
    return pygame.transform.scale(pygame.image.load(image_path), (
    NEW_FOOD_SIZE, NEW_FOOD_SIZE)), image_file  # Scale the food image and return the file name


# Snake and food behavior
def draw_snake(snake_body, captured_images):
    screen.blit(snake_head_image, (snake_body[0][0], snake_body[0][1]))

    for index, block in enumerate(snake_body[1:]):  # Start from the second segment
        if index < len(captured_images):  # Ensure there is an image for this segment
            snake_image = pygame.image.load(
                os.path.join(food_image_directory, captured_images[index]))  # Load the image for this segment
            snake_image = pygame.transform.scale(snake_image, (SNAKE_SIZE, SNAKE_SIZE))  # Scale the image
            screen.blit(snake_image, (block[0], block[1]))  # Draw the image at the segment's position


def create_food():
    food_pos = [random.randrange(0, SCREEN_WIDTH // NEW_FOOD_SIZE) * NEW_FOOD_SIZE,
                random.randrange(0, SCREEN_HEIGHT // NEW_FOOD_SIZE) * NEW_FOOD_SIZE]
    food_image, image_name = get_random_food_image()  # Get a random food image and its name
    return food_pos, food_image, image_name  # Return position, image, and image name

def display_images(images):
    image_width, image_height = NEW_FOOD_SIZE, NEW_FOOD_SIZE  # Size of food images
    x, y = 0, 0  # Starting position for drawing images
    margin = 10  # Margin between images

    for image_name in images:
        image_path = os.path.join(food_image_directory, image_name)
        image, image_name = get_random_food_image()  # Get a random food image and its name
        image = pygame.transform.scale(image, (image_width, image_height))

        screen.blit(image, (x, y))  # Draw the image

        # Update position for next image
        x += image_width + margin
        if x + image_width > SCREEN_WIDTH:  # Move to the next row if exceeding screen width
            x = 0
            y += image_height + margin

# Main game loop
def game_loop():
    game_over = False
    game_close = False

    # Initial position and movement of the snake
    x = SCREEN_WIDTH // 2
    y = SCREEN_HEIGHT // 2
    x_change = 0
    y_change = 0

    snake_body = [[x, y]]  # Start with one segment
    snake_length = 1

    # List to keep track of captured images
    captured_images = []

    # Create the first food
    food_pos, food_image, food_image_name = create_food()
    captured_images.append(food_image_name)

    while not game_over:

        # Game over handling
        while game_close:
            screen.fill(BLUE)
            font = pygame.font.SysFont("bahnschrift", 35, bold=True)
            display_images(food_images)
            game_over_message = font.render(f"You captured {len(captured_images)-1} Pokemon Mayla or Aydin! Press Q-Quit or C-Play Again. You can do it! I love you!", False, BLACK)
            text_width, text_height = game_over_message.get_size()
            x_position = (SCREEN_WIDTH - text_width) // 2
            y_position = (SCREEN_HEIGHT - text_height) // 2
            screen.blit(game_over_message, [x_position, y_position])
            pygame.display.update()
            time.sleep(1)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Event handling
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

        # Snake position update
        x += x_change
        y += y_change

        # Game over if the snake hits the wall
        if x >= SCREEN_WIDTH or x < 0 or y >= SCREEN_HEIGHT or y < 0:
            game_close = True

        # Update the screen
        screen.fill(BLACK)

        # Draw the food image
        screen.blit(food_image, (food_pos[0], food_pos[1]))

        # Update the snake
        snake_body.insert(0, [x, y])
        if len(snake_body) > snake_length:
            del snake_body[-1]

        # Game over if the snake hits itself
        for block in snake_body[1:]:
            if block == [x, y]:
                game_close = True

        draw_snake(snake_body, captured_images)  # Draw the snake

        # Snake eats food
        if abs(x - food_pos[0]) < SNAKE_SIZE and abs(y - food_pos[1]) < SNAKE_SIZE:
            food_pos, food_image, food_image_name = create_food()
            captured_images.append(food_image_name)
            snake_length += 1

        pygame.display.update()

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()


# Run the game
game_loop()
