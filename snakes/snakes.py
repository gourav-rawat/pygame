import pygame
import random
import os

# initialising pygame
pygame.init()
pygame.mixer.init()

# colour
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 200, 55)
black = (0, 0, 0)
blue = (0, 0, 255)

# initialising font and clock
font = pygame.font.SysFont(None, 30)
font1 = pygame.font.SysFont(None, 60)
clock = pygame.time.Clock()

screen_width = 900
screen_height = 600


# creating game window
gameWindow = pygame.display.set_mode((screen_width, screen_height))  # it takes tuple
pygame.display.set_caption("Snake")

welimg = pygame.image.load("welcome.jpg")
endimg = pygame.image.load("gameover.jpg")
bgimg = pygame.image.load("bgimg.jpg")
skin = pygame.image.load("snake_skin.png")
welimg = pygame.transform.scale(welimg, (screen_width, screen_height)).convert_alpha()
endimg = pygame.transform.scale(endimg, (screen_width, screen_height)).convert_alpha()
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_height)).convert_alpha()
skin = pygame.transform.scale(skin, (12, 12)).convert_alpha()

# def plot_snake(window, color, snake_list, size):


def plot_snake(snake_list):
    for x, y in snake_list:
        # pygame.draw.rect(window, color, (x, y, size, size))
        # pygame.draw.circle(window, color, (x, y), size)
        gameWindow.blit(skin, (x, y))


def screen_text(text, color, x, y):
    text_screen = font.render(text, True, color)
    gameWindow.blit(text_screen, [x, y])


def welcome():
    game_exit = False

    while not game_exit:
        gameWindow.blit(welimg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()

            pygame.display.update()
            clock.tick(30)


def game_loop():

    # specific variable
    game_exit = False
    game_over = False
    back_key = 0
    snake_x = 450
    snake_y = 300
    snake_size = 7
    init_velocity = 5
    velocity_x = 0
    velocity_y = 0
    fps = 30
    score = 0
    food_x = random.randint(30, int(screen_width / 1.03))
    food_y = random.randint(30, int(screen_height / 1.03))
    snake_list = []
    snake_length = 1

    if not os.path.exists("high_score.txt"):
        with open("high_score.txt", "w") as f:
            f.write("0")

    with open("high_score.txt", "r") as f:
        high_score = int(f.read())

    while not game_exit:
        if game_over:
            with open("high_score.txt", "w") as f:
                f.write(str(high_score))

            gameWindow.blit(endimg, (0, 0))
            screen_text("Your Score: " + str(score) + "    High Score: " + str(high_score), red, 320, 320)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if back_key != pygame.K_LEFT:
                            velocity_x = init_velocity
                            velocity_y = 0
                            back_key = pygame.K_RIGHT

                    if event.key == pygame.K_LEFT:
                        if back_key != pygame.K_RIGHT:
                            velocity_x = - init_velocity
                            velocity_y = 0
                            back_key = pygame.K_LEFT

                    if event.key == pygame.K_UP:
                        if back_key != pygame.K_DOWN:
                            velocity_y = - init_velocity
                            velocity_x = 0
                            back_key = pygame.K_UP

                    if event.key == pygame.K_DOWN:
                        if back_key != pygame.K_UP:
                            velocity_y = init_velocity
                            velocity_x = 0
                            back_key = pygame.K_DOWN

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                score += 1
                food_x = random.randint(30, int(screen_width / 1.1))
                food_y = random.randint(30, int(screen_height / 1.1))
                snake_length += 5
                pygame.mixer.music.load('eat.mp3')
                pygame.mixer.music.play()

                if score > high_score:
                    high_score = score

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            if snake_x < 0 or snake_y < 0 or snake_x > screen_width or snake_y > screen_height:
                pygame.mixer.music.load('game_over.mp3')
                pygame.mixer.music.play()
                game_over = True

            if head in snake_list[:-1]:
                pygame.mixer.music.load('game_over.mp3')
                pygame.mixer.music.play()
                game_over = True

            gameWindow.blit(bgimg, (0, 0))
            screen_text("Score: " + str(score) + "    High Score: " + str(high_score), green, 5, 5)
            plot_snake(snake_list)
            # pygame.draw.rect(gameWindow, red, (food_x, food_y, snake_size, snake_size))
            pygame.draw.circle(gameWindow, red, (food_x, food_y), snake_size)
            pygame.draw.rect(gameWindow, blue, (0, 0, 900, 600), 3)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


if __name__ == '__main__':
    welcome()
