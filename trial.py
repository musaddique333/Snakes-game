import pygame
import random
import time
import os


def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def snake_print(color, snake_list, size):
    for x, y in snake_list:
        pygame.draw.rect(gameWindow, color, [x, y, size, size])


def welcome():
    exit_game = False
    vel = 5
    while not exit_game:
        gameWindow.fill(white)
        text_screen("Welcome to the SNAKES", red, (screen_width / 2) - 200, (screen_height / 2) - 75)
        text_screen("Enter SPACE to Play play the game", (255, 15, 150), (screen_width / 2) - 300, (screen_height / 2) - 25)
        text_screen("Enter l to choose difficulty level", (55, 140, 250), (screen_width / 2) - 280, (screen_height / 2) + 25)
        text_screen("Enter r to reset the high score", (100, 10, 110), (screen_width / 2) - 250, (screen_height / 2) + 75)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop(vel)
                if event.key == pygame.K_r:
                    reset("High_score.txt")
                if event.key == pygame.K_l:
                    vel = level()
        pygame.display.update()


def reset(file):
    with open(f"{file}", "w") as f:
        f.write("0")


def level():
    exit_game = False
    while not exit_game:
        gameWindow.fill(white)
        text_screen("1 = Easy", red, 270, 100)
        text_screen("2 = Medium", red, 250, 200)
        text_screen("3 = Hard", red, 270, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 5
                if event.key == pygame.K_3:
                    return 10
        pygame.display.update()
    return 1


def game_loop(init_velocity):
    # Game specific variables
    exit_game = False
    game_over = False
    size = 20
    snake_x = 100
    snake_y = 100
    food_x = random.randint(50, screen_width - 50)
    food_y = random.randint(50, screen_height - 50)
    velocity_x = 0
    velocity_y = 0
    score = 0
    fps = 30
    snake_list = []
    snake_len = 1
    precision = 20

    # High score
    if (not os.path.exists("High_score.txt")):
        with open("High_score.txt", "w") as f:
            f.write("0")
    with open("High_score.txt", "r") as f:
        high_score = f.read()

    while not exit_game:
        if game_over:
            pygame.draw.rect(gameWindow, white, [50, 50, screen_width - 100, screen_height - 100])
            text_screen("Game Over", red, (screen_width / 2) - 100, (screen_height / 2) - 75)
            text_screen("Press Enter", red, (screen_width / 2) - 100, (screen_height / 2) - 25)
            game_over = True

            with open("High_score.txt", "w") as f:
                f.write(high_score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_SPACE:
                        score += 50
                    if event.key == pygame.K_f:
                        precision += 20
            snake_x += velocity_x
            snake_y += velocity_y
            if abs(snake_x - food_x) < precision and abs(snake_y - food_y) < precision:
                score += 10
                food_x = random.randint(200, 500)
                food_y = random.randint(200, 500)
                snake_len += 10
                if score > int(high_score):
                    high_score = str(score)

            temp = [snake_x, snake_y]
            snake_list.append(temp)
            if len(snake_list) > snake_len:
                del snake_list[0]
            if temp in snake_list[:len(snake_list) - 1]:
                game_over = True
                time.sleep(3)

            gameWindow.fill(black)
            pygame.draw.rect(gameWindow, white, [50, 50, screen_width - 100, screen_height - 100])
            pygame.draw.rect(gameWindow, red, [food_x, food_y, size, size])

            snake_print(green, snake_list, size)

            text_screen(f"Score : {score} High Score : {high_score}", red, 10, 10)
            if snake_x == (screen_width - 50 - size) or snake_x == 50 or snake_y == (
                    screen_height - 50 - size) or snake_y == 50:
                game_over = True
                time.sleep(3)

        clock.tick(fps)
        pygame.display.update()


if __name__ == '__main__':
    os.system("clear")
    pygame.init()

    # Display
    screen_width = 700
    screen_height = 700
    gameWindow = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Kunika Loves Musaddique")
    pygame.display.update()

    # colors
    red = (255, 0, 0)
    white = (255, 255, 255)
    black = (0, 0, 0)
    green = (0, 255, 0)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 50)

    welcome()
    pygame.quit()
    quit()
