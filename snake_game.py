import pygame
import random

# Initializing the music
pygame.mixer.init()

# Initializing the pygame
pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (153,255,51)
blue = (51,0,102)

# Creating  game window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Title
pygame.display.set_caption("Snake_Game")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

# Defining Text written on screen
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

# Defining the snake
def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# Defining the welcome screen
def welcome():
    exit_game = False
    while not exit_game:

        # Forming the welcome screen
        gameWindow.fill((233,210,229))
        text_screen("Welcome to snakes",black,260,250)
        text_screen("Press Space Bar To Play",black,232,290)


        # making welcome window responsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("back.mp3")  # loading the music
                    pygame.mixer.music.play(5)  # Playing the music
                    gameloop() # Calling the game loop

        # updating the display
        pygame.display.update()
        clock.tick(30)

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

    with open("highscore.txt","r") as f: # Opening highscore file and reading highest score
        highscore = f.read()

    food_x = random.randint(20, screen_width / 2) # Creating  position of food for the snake
    food_y = random.randint(20, screen_height / 2) # Creating  position of food for the snake
    score = 0
    init_velocity = 10
    snake_size = 10

    fps = 30 # How much times the Game loop will be called

    while not exit_game:

        # When game will be over
        if game_over:

            # Updating high score once the game is over
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            # Writing the message of game over
            gameWindow.fill(white)
            text_screen("Game Over! Press Enter To Continue", red, 100, 250)

            # Quiting the game if the game is over
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                # Enter key for re-running the game loop once the game is over
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()

        else:

            # managing the events in the game window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                # Defining keys for the motion of snake and snake's velocity
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            # Snake's new position with velocity
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            # Making snake eat the food
            if abs(snake_x - food_x)<6 and abs(snake_y - food_y)<6:
                score +=10 # Increasing the score by 10

                # food's new position after the snake has eaten the previous food
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)

                # Increasing the length of snake after the snake has eaten the food
                snk_length +=5
                if score > int(highscore):
                    highscore = score

            # Filling the game window with color while playing
            gameWindow.fill(green)

            # Showing score and high score on the screen
            text_screen("Score: " + str(score), red, 5, 5)
            text_screen("High Score: " + str(highscore), red, 575, 5)

            # Creating food for the snake
            pygame.draw.rect(gameWindow, blue, [food_x, food_y, snake_size, snake_size])


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                

            # Making the game over if the snakes moves out of the game window
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True



            # Making snake in the game window
            plot_snake(gameWindow, black, snk_list, snake_size)

        # Updating the changes in game window
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
welcome()
