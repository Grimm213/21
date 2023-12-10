import pygame
import time
import random

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 20

font_style = pygame.font.SysFont(None, 35)
score_font = pygame.font.SysFont(None, 35)

def your_score(score):
    value = score_font.render("Score: " + str(score), True, black)
    dis.blit(value, [0, 0])

def our_snake(snake_block, snake_List):
    for x in snake_List:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg1 = font_style.render(msg.split('\n')[0], True, color)
    mesg2 = font_style.render(msg.split('\n')[1], True, color)
    dis.blit(mesg1, [dis_width // 2.5, dis_height // 3])
    dis.blit(mesg2, [dis_width // 20, dis_height // 2.5])

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    score = 0

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("Вы проиграли!\nНажмите C чтобы играть снова или Q чтобы выйти", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0

        if x1 >= dis_width-snake_block:
            x1_change = 0
        if x1 < 0:
            x1_change = 0
        if y1 >= dis_height-snake_block:
            y1_change = 0
        if y1 < 0:
            y1_change = 0

        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        your_score(score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
