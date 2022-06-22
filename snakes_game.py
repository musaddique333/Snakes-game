import os
from numpy import random
import pygame


def text_screen(text, size, color, x, y):
    font = pygame.font.SysFont("papyrus", size)
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def snake_print(snake_list):
    for x, y in snake_list:
        gameWindow.blit(snake_body, (x, y))


def welcome():
    wc.play()
    exit_game = False
    vel = 3
    while not exit_game:
        # gameWindow.fill((255, 171, 87))
        gameWindow.blit(welcome_back, (0, 0))
        text_screen("SNAKES", 200, (0, 185, 255), 70, 20)
        text_screen("PLAY", 100, (174, 0, 178), 260, 250)
        text_screen("(SPACE)", 30, (174, 0, 178), 305, 350)
        text_screen("LEVEL", 100, (174, 0, 178), 240, 410)
        text_screen("(l)", 30, (174, 0, 178), 340, 510)
        text_screen("RESET HIGH SCORE", 50, (174, 0, 178), 180, 570)
        text_screen("(r)", 30, (174, 0, 178), 340, 620)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    wc.stop()
                    game_loop(vel)
                    wc.play()
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
        gameWindow.fill((255, 171, 87))
        text_screen("LEVELS", 200, (255, 0, 166), 80, 20)
        text_screen("EASY", 70, (255, 0, 166), 270, 300)
        text_screen("(1)", 30, (255, 15, 150), 330, 370)
        text_screen("MEDIUM", 70, (255, 0, 166), 240, 400)
        text_screen("(2)", 30, (255, 15, 150), 330, 470)
        text_screen("HARD", 70, (255, 0, 166), 270, 500)
        text_screen("(3)", 30, (255, 15, 150), 330, 570)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 3
                if event.key == pygame.K_2:
                    return 6
                if event.key == pygame.K_3:
                    return 10
        pygame.display.update()
    return 1


def game_loop(init_velocity):
    on.play()
    # Game specific variables
    exit_game = False
    game_over = False
    pl = 1
    size = 40
    snake_x = 100
    snake_y = 100
    food_x = random.randint(100, screen_width - 100)
    food_y = random.randint(100, screen_height - 100)
    velocity_x = 0
    velocity_y = 0
    score = 0
    fps = 60
    snake_list = []
    snake_len = 1
    precision = 20

    # High score
    if not os.path.exists("High_score.txt"):
        with open("High_score.txt", "w") as f:
            f.write("0")
    with open("High_score.txt", "r") as f:
        high_score = f.read()

    while not exit_game:
        if game_over:
            if pl == 1:
                over.play()
                pl += 1
            pygame.draw.rect(gameWindow, (217, 92, 38), [50, 50, screen_width - 100, screen_height - 100])
            text_screen("Game Over", 50, (255, 255, 255), (screen_width / 2) - 100, (screen_height / 2) - 75)
            text_screen("Press Enter", 50, (174, 255, 255), (screen_width / 2) - 105, (screen_height / 2) - 25)

            with open("High_score.txt", "w") as f:
                f.write(high_score)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    on.stop()
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        over.stop()
                        on.stop()
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    on.stop()
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        move.play()
                        velocity_x = init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_LEFT:
                        move.play()
                        velocity_x = -init_velocity
                        velocity_y = 0
                    if event.key == pygame.K_UP:
                        move.play()
                        velocity_y = -init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_DOWN:
                        move.play()
                        velocity_y = init_velocity
                        velocity_x = 0
                    if event.key == pygame.K_SPACE:
                        score += 50
                    if event.key == pygame.K_f:
                        precision += 20
            snake_x += velocity_x
            snake_y += velocity_y
            if abs(snake_x - food_x) < precision and abs(snake_y - food_y) < precision:
                eat.set_volume(10.0)
                eat.play()
                score += 10
                food_x = random.randint(100, screen_width - 100)
                food_y = random.randint(100, screen_height - 100)
                snake_len += 10
                if score > int(high_score):
                    high_score = str(score)

            temp = [snake_x, snake_y]
            snake_list.append(temp)
            if len(snake_list) > snake_len:
                del snake_list[0]
            if temp in snake_list[:len(snake_list) - 1]:
                game_over = True

            gameWindow.fill((0, 224, 255))
            gameWindow.blit(game_back, (50, 50))
            gameWindow.blit(apple, (food_x, food_y))

            snake_print(snake_list)

            text_screen(f"Score : {score} High Score : {high_score}", 30, (174, 0, 178), 5, 0)
            if snake_x >= (screen_width - 50 - size) or snake_x <= 50 or snake_y >= (
                    screen_height - 50 - size) or snake_y <= 50:
                game_over = True

        clock.tick(fps)
        pygame.display.update()


if __name__ == '__main__':
    os.system("clear")
    pygame.init()

    # Music
    os.getcwd()
    pygame.mixer.init()
    wc = pygame.mixer.Sound("sound_effects /welcome.mp3")
    over = pygame.mixer.Sound("sound_effects /over.mp3")
    eat = pygame.mixer.Sound("sound_effects /eat.wav")
    move = pygame.mixer.Sound("sound_effects /move.wav")
    on = pygame.mixer.Sound("sound_effects /game_run.mp3")

    # Display
    screen_width = 700
    screen_height = 700
    gameWindow = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("SNAKES BY MUSADDIQUE")
    pygame.display.update()

    # images
    welcome_back = pygame.image.load("images/welcome_back.jpeg")
    welcome_back = pygame.transform.scale(welcome_back, (screen_width, screen_height)).convert_alpha()
    game_back = pygame.image.load("images/game_back.jpeg")
    game_back = pygame.transform.scale(game_back, (screen_width - 100, screen_height - 100)).convert_alpha()
    snake_body = pygame.image.load("images/snake.png")
    snake_body = pygame.transform.scale(snake_body, (30, 30)).convert_alpha()
    apple = pygame.image.load("images/apple.png")
    apple = pygame.transform.scale(apple, (40, 40)).convert_alpha()

    clock = pygame.time.Clock()

    welcome()
    pygame.quit()
    quit()
