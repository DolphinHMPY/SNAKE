import random
import itertools
import collections
import pygame

pygame.init()

MAP_X = 400 # длина карты
MAP_Y = 280 # высота карты
FIGURE_HEIGHT = 40 # длина фигуры (головы змеи)
FIGURE_WIDTH = 40 # высотв фигуры (головы змеи)
START_FIGURE_X = 0 # стартовое положение фигуры (головы змеи) по длине
START_FIGURE_Y = 120 # стартовое положение фигуры по высоте

win = pygame.display.set_mode((MAP_X, MAP_Y))
tmp_x = START_FIGURE_X # положение фигуры (головы змеи) в данный момент по длине
tmp_y = START_FIGURE_Y # положение фигуры (головы змеи) в данный момент по высоте
longs = collections.deque() # отвечает хвост змеи

def wide():
    '''Данная функция отвечает за разукрашивание окна в решетку'''
    num_x = int(MAP_Y / 40) # находим количество необходимых горизонтальных линий
    for i in range(1, num_x): # начинаем с одного и заканчиваем нереальным значением деления, т.к. 0 и частное - границы окна
        pygame.draw.line(win, (255, 255, 255), [0, 40 * i], [MAP_X, 40 * i], 3)
    num_y = int(MAP_X / 40) # находим количество необходимых вертикальных линий
    for i in range(1, num_y): # начинаем с одного и заканчиваем нереальным значением деления, т.к. 0 и частное - границы окна
        pygame.draw.line(win, (255, 255, 255), [40 * i, 0], [40 * i, MAP_X], 3)

def move(tmp_x, tmp_y):
    '''Данная функция отвечает за передвижение фигуры (головы змеи) по карте'''
    may_be = (tmp_x, tmp_y)
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        tmp_y = 0 if (tmp_y + FIGURE_HEIGHT) >= MAP_Y else (tmp_y + FIGURE_HEIGHT) # если вдруг новые значения координат больше размера самой карты то возвращаем 0, т.е. начало этой самой карты
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        tmp_x = 0 if (tmp_x + FIGURE_WIDTH) >= MAP_X else (tmp_x + FIGURE_WIDTH) # если вдруг новые значения координат больше размера самой карты то возвращаем 0, т.е. начало этой самой карты
    elif pygame.key.get_pressed()[pygame.K_UP]:
        tmp_y = MAP_Y - 40 if (tmp_y - FIGURE_HEIGHT) < 0 else (tmp_y - FIGURE_HEIGHT)
        # если вдруг новые значения координат меньше размера самой карты то возвращаем конечное значение, т.е. максимальный размер этой самой карты
    elif pygame.key.get_pressed()[pygame.K_LEFT]:
        tmp_x = MAP_X - 40 if (tmp_x - FIGURE_WIDTH) < 0 else (tmp_x - FIGURE_WIDTH)
        # если вдруг новые значения координат меньше размера самой карты то возвращаем конечное значение, т.е. максимальный размер этой самой карты
    if len(longs) > 0:
        if [tmp_x, tmp_y] == longs[0]:
            tmp_x, tmp_y = may_be
    return tmp_x, tmp_y

def for_longs(longs):
    '''Данная функция отвечает за разрисовку дополнительных блоков (хвоста змеи)'''
    for i, j in enumerate(longs):
        pygame.draw.rect(win, (0, 255, 0), (longs[i][0], longs[i][1], FIGURE_WIDTH, FIGURE_HEIGHT))

def random_block():
    '''Данная функция отвечает за рандомное появление фрукта на карте'''
    while True:
        for_x = random.choice([i * 40 for i in range(int(MAP_X / 40))])
        for_y = random.choice([i * 40 for i in range(int(MAP_Y / 40))])
        example = longs + collections.deque([[tmp_x, tmp_y]])
        some = True
        for i in example:
            if for_x == i[0] and for_y == i[1]:
                some = False
        if some == True:
            return (win, (255, 0, 255), (for_x, for_y, FIGURE_WIDTH, FIGURE_HEIGHT))

block = True # переменная для проверки наличия съеденного фрукта
while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            exit()
    win.fill((0, 0, 0))
    if block == True: # если фрукт съеден
        ret = random_block() # получаем координаты нового фрукта
        block = False
    pygame.draw.rect(*ret) # рисуем старый или уже новый фрукт
    pygame.draw.rect(win, (0, 255, 255), (tmp_x, tmp_y, FIGURE_WIDTH, FIGURE_HEIGHT))
    for_longs(longs)
    wide()
    res = move(tmp_x, tmp_y) # сохранение результатов новых координатов
    if res != (tmp_x, tmp_y): # если реезультаты хоть чем-то отличаются от прошлых значений
        if res == (ret[2][0], ret[2][1]): # если наши координаты - на координатах фрукта
            block = True
            longs.append([tmp_x, tmp_y])
        if len(longs) > 0:
            longs.rotate(1)
            longs[0] = [tmp_x, tmp_y]
    tmp_x, tmp_y = res
    try:
        ind = longs.index([tmp_x, tmp_y])
    except:
        ind = None
    if ind != None:
        for i, j in enumerate(longs[ind]):
            pygame.draw.rect(win, (255, 0, 0), (longs[i][0], longs[i][1], FIGURE_WIDTH, FIGURE_HEIGHT))
        longs.clear()
    pygame.display.update()
    pygame.time.delay(100)