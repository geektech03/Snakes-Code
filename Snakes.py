import pygame
import random
import os

pygame.mixer.init()
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0 , 225 , 0)
blue = (0 , 0 , 225)

# Creating window
screen_width = 1000
screen_height = 500
gameWindow = pygame.display.set_mode((screen_width, screen_height))

#Images
goimg = pygame.image.load("gameover.jpg")
goimg = pygame.transform.scale(goimg, (screen_width, screen_height)).convert_alpha()

wcimg = pygame.image.load("welcome.jpg")
wcimg = pygame.transform.scale(wcimg, (screen_width, screen_height)).convert_alpha()

pgimg = pygame.image.load("grass.jpg")
pgimg = pygame.transform.scale(pgimg, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snakes")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

#Welcome
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.blit(wcimg , (0 , 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    gameloop()
        text_screen("Welcome to snakes! Press enter to continue!" , blue , 70 , 250)
        text_screen("Developed by Kush-Jasrapuria" , blue , 695 , 475)
        pygame.display.update()

# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    if (not os.path.exists("High Score.txt")):
        with open("High Score.txt", "w") as f:
            f.write("0")
    with open("High Score.txt" , "r") as HScore:
        Hi_Score = HScore.read()
    food_x = random.randint(20, screen_width - 20)
    food_y = random.randint(20, screen_height - 20)
    food_size = 5
    score = 0
    init_velocity = 3
    snake_size = 10
    fps = 60
    absv = 6
    F1_pressed = False
    F2_pressed = False
    F3_pressed = False
    F4_pressed = False
    while not exit_game:
        if game_over:
            with open("High Score.txt" , "w") as HScore:
                HScore.write(str(Hi_Score))
            gameWindow.blit(goimg , (0 , 0))
            text_screen("Press Enter To Continue", white , 375 , 320 )
            text_screen("Score : " + str(score) , white , 455 , 360)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        F1_pressed = True

                    if event.key == pygame.K_F2:
                        F2_pressed = True

                    if event.key == pygame.K_F3:
                        F3_pressed = True

                    if event.key == pygame.K_F4:
                        F4_pressed = True

                    if event.key == pygame.K_RIGHT:
                        pygame.mixer.music.load('movements.mp3')
                        pygame.mixer.music.play()
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        pygame.mixer.music.load('movements.mp3')
                        pygame.mixer.music.play()
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        pygame.mixer.music.load('movements.mp3')
                        pygame.mixer.music.play()
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        pygame.mixer.music.load('movements.mp3')
                        pygame.mixer.music.play()
                        velocity_y = init_velocity
                        velocity_x = 0

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_F1:
                        F1_pressed = False

                    if event.key == pygame.K_F2:
                        F2_pressed = False

                    if event.key == pygame.K_F3:
                        F3_pressed = False

                    if event.key == pygame.K_F4:
                        F4_pressed = False

                if F1_pressed == True and F2_pressed == True:
                    score += 10

                if F2_pressed == True and F3_pressed == True:
                    food_size += 5

                if F3_pressed == True and F4_pressed == True:
                    food_size -= 5

                if F1_pressed == True and F3_pressed == True:
                    absv += 5

                if F2_pressed == True and F4_pressed == True:
                    absv -= 5

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<absv and abs(snake_y - food_y)<absv:
                score +=1
                pygame.mixer.music.load('eatingfood.mp3')
                pygame.mixer.music.play()
                food_x = random.randint(20, screen_width - 20)
                food_y = random.randint(20, screen_height - 20)
                snk_length +=5
                if score > int(Hi_Score):
                    Hi_Score = score

            gameWindow.blit(pgimg , (0 , 0))
            pygame.draw.rect(gameWindow, red, [food_x, food_y, food_size, food_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                with open("High Score.txt" , "w") as HScore:
                    HScore.write(str(Hi_Score))
                game_over = True
                pygame.mixer.music.load('gameover.wav')
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load('gameover.wav')
                pygame.mixer.music.play()
            plot_snake(gameWindow, black, snk_list, snake_size)
            text_screen("Score: " + str(score) + "  High Score : " + str(Hi_Score), blue, 5, 5)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()