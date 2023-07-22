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
snake_block = 20

font_style = pygame.font.SysFont('Arial', 30)
score_font = pygame.font.SysFont('comicsansms', 35)


def addSnake(block, lit):
    for x in lit:
        pygame.draw.rect(screen, 'green', [x[0], x[1], block, block])


def setScore(score):
    value = score_font.render('Score: ' + str(score), True, 'orange')
    screen.blit(value, [0,0])


def message(msg, color):
    mess = font_style.render(msg, True, color)
    screen.blit(mess, [screen_width / 6, screen_height / 3])


def distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def gameLoop():
    game_over = False
    game_close = False

    x = screen_width / 2
    y = screen_height / 2

    x_change = 0
    y_change = 0

    snake_List = []
    snake_length = 1

    foodx = round(random.randrange(0, (screen_width - snake_block)))
    foody = round(random.randrange(0, (screen_height - snake_block)))

    while not game_over:

        # menu
        while game_close:
            screen.fill('white')
            message("You lost! Press Q to quit or P to play again", 'red')
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_p:
                        gameLoop()

        # quit game
        for event in pygame.event.get():
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

        screen.fill('white')
        pygame.draw.rect(screen, 'green', [x, y, snake_block, snake_block])
        pygame.draw.rect(screen, 'red', [foodx, foody, snake_block, snake_block])

        snake_head = [x, y]
        snake_List.append(snake_head)

        if len(snake_List) > snake_length:
            del snake_List[0]

        for i in snake_List[:-1]:
            if i == snake_head:
                game_close = True

        addSnake(snake_block, snake_List)
        setScore((snake_length - 1) * 10)


        pygame.display.update()

        # food collision detection
        if distance(snake_head[0], snake_head[1], foodx, foody) <= 25:
            foodx = round(random.randrange(0, (screen_width - snake_block)))
            foody = round(random.randrange(0, (screen_height - snake_block)))
            snake_length += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
