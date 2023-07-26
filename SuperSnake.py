import pygame
import random

pygame.init()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))  # screen size width, height
pygame.display.update()
pygame.display.set_caption('Super Snake')

clock = pygame.time.Clock()
snake_speed = 10
snake_block = 21

font_style = pygame.font.SysFont('Arial', 30)
score_font = pygame.font.SysFont('comicsansms', 25)
hs_font = pygame.font.SysFont('comicsansms', 15)


class Food:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    def set_position(self, ex, why):
        self.x = ex
        self.y = why


apple = Food('red', 0, 0)
grape = Food('green', 0, 0)
orange = Food('orange', 0, 0)
plum = Food('magenta', 0, 0)
banana = Food('yellow', 0, 0)
berry = Food('cyan', 0, 0)
pink = Food('pink', 0, 0)
brownie = Food('dimgrey', 0, 0)
chalk = Food('white', 0, 0)
blue = Food('blue', 0, 0)


foods = [apple, grape, orange, plum, banana, berry, pink, brownie, chalk, blue]


def get_highscore():
    try:
        with open('highScore.txt', 'r') as file:
            hs = file.readline()
            return int(hs)
    except FileNotFoundError:
        # If the file is not found, return a default high score of 0
        return 0


def new_highscore(score):
    try:
        with open('highScore.txt', 'w') as file:
            file.write(str(score))
            file.close()
    except FileNotFoundError:
        # If the file is not found, return a default high score of 0
        return 0



def placeFood():
    x = round(random.randrange(0, (screen_width - snake_block)))
    y = round(random.randrange(0, (screen_height - snake_block)))
    return x, y


def genFood(level):
    # spawn x random foods
    sample = random.sample(foods, level)

    for food in sample:
        food.set_position(placeFood()[0], placeFood()[1])
        pygame.draw.rect(screen, food.color, [food.x, food.y, snake_block, snake_block])

    return sample


def addSnake(block, lit, color):
    for x in lit:
        pygame.draw.rect(screen, color, [x[0], x[1], block, block])


def setScore(score, hscore):
    score_value = score_font.render('Score: ' + str(score), True, 'white')
    screen.blit(score_value, [0, 0])

    hs_value = hs_font.render('High-score: ' + str(hscore), True, 'white')
    screen.blit(hs_value, [0, hs_value.get_height()+7])


def you_Lost(score):
    num = font_style.render("SCORE: " + str(score), True, 'red')
    press = font_style.render("PRES Q TO QUIT OR P TO PLAY AGAIN", True, 'red')

    screen.blit(num, [screen_width / 10, screen_height / 2.5])
    screen.blit(press, [screen_width / 10, screen_height / 2])


def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def check_collision(snake_head, food):
    if distance(snake_head[0], snake_head[1], food.x, food.y) <= 25:
        return True
    return False


def gameLoop():
    level = 1
    game_over = False
    game_close = False

    x = screen_width / 2
    y = screen_height / 2

    x_change = 0
    y_change = 0

    snake_List = []
    snake_length = 1

    feed = genFood(level)
    target = random.choice(feed)
    pygame.draw.rect(screen, target.color, [0, 0, snake_block, snake_block])

    while not game_over:
        hs = get_highscore()

        # menu
        while game_close:
            screen.fill('black')

            # msg = 'You lost!, Score:' + str(snake_length) + ' Press Q to quit or P to play again'
            you_Lost(snake_length - 1)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_p:
                        gameLoop()

        for event in pygame.event.get():
            # quit game
            if event.type == pygame.QUIT:
                game_over = True

            # snake movements based on keystroke
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change != snake_block:
                    x_change = -snake_block
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change != -snake_block:
                    x_change = snake_block
                    y_change = 0
                elif event.key == pygame.K_UP and y_change != snake_block:
                    x_change = 0
                    y_change = -snake_block
                elif event.key == pygame.K_DOWN and y_change != -snake_block:
                    x_change = 0
                    y_change = snake_block

        x += x_change
        y += y_change

        # no game borders
        if x <= 0:
            x = 800
        elif x >= 800:
            x = 0

        if y <= 0:
            y = 600
        elif y >= 600:
            y = 0

        screen.fill('black')
        addSnake(snake_block, snake_List, target.color)
        setScore((snake_length - 1), hs)

        for food in feed:
            pygame.draw.rect(screen, food.color, [food.x, food.y, snake_block, snake_block])

        pygame.display.update()

        snake_head = [x, y]
        snake_List.append(snake_head)

        if len(snake_List) > snake_length:
            del snake_List[0]

        for i in snake_List[:-1]:
            if i == snake_head:
                game_close = True

        pygame.display.update()

        for food in feed:
            if check_collision(snake_head, food):
                if food == target:
                    snake_length += 1
                    feed = genFood(level)
                    target = random.choice(feed)

                    if (snake_length-1) > get_highscore():
                        new_highscore(snake_length-1)
                        setScore((snake_length - 1), hs)

                    elif (snake_length-1) % 1 == 0:  # Check if points is a multiple of 7
                        if level < 10:
                            level += 1
                        print(str(level))

                else:
                    game_close = True

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
