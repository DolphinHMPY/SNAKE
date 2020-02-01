import json
import time
import random
import socket
import threading
import itertools
import collections
import pygame

MAP_X = 800
MAP_Y = 400
FIGURE_HEIGHT = 40
FIGURE_WIDTH = 40
START_FIGURE_X = random.choice([i * FIGURE_WIDTH for i in range(int(MAP_X / FIGURE_WIDTH))])
START_FIGURE_Y = random.choice([i * FIGURE_HEIGHT for i in range(int(MAP_Y / FIGURE_HEIGHT))]) if START_FIGURE_X in [0, MAP_X - 40] else random.choice([0, MAP_Y - 40])
SERVER = ("192.168.0.6", 8080)
COLOR = random.choice([(255, 162, 55), (20, 255, 40), (255, 15, 111), (179, 78, 233)])

pygame.init()
sock = socket.socket(socket.SOCK_DGRAM, socket.AF_INET)
sock.connect(SERVER)
win = pygame.display.set_mode((MAP_X, MAP_Y))
tmp_x = START_FIGURE_X
tmp_y = START_FIGURE_Y
longs = collections.deque()
other = []

def recving():
    global ret
    while True:
        try:
            msg = json.loads(sock.recv(8192).decode("utf-8"))
        except:
            break
        if msg['block'] is not None:
            ret = (win,) + tuple(msg['block'])
        if msg.get('snake') is not None:
            other.append((msg['snake'], tuple(msg['color'])))
thread = threading.Thread(target=recving)
thread.start()

def wide():
    num_x = int(MAP_Y / 40)
    for i in range(1, num_x):
        pygame.draw.line(win, (255, 255, 255), [0, 40 * i], [MAP_X, 40 * i], 3)
    num_y = int(MAP_X / 40)
    for i in range(1, num_y):
        pygame.draw.line(win, (255, 255, 255), [40 * i, 0], [40 * i, MAP_X], 3)

def move(tmp_x, tmp_y):
    may_be = (tmp_x, tmp_y)
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        tmp_y = 0 if (tmp_y + FIGURE_HEIGHT) >= MAP_Y else (tmp_y + FIGURE_HEIGHT)
    elif pygame.key.get_pressed()[pygame.K_RIGHT]:
        tmp_x = 0 if (tmp_x + FIGURE_WIDTH) >= MAP_X else (tmp_x + FIGURE_WIDTH)
    elif pygame.key.get_pressed()[pygame.K_UP]:
        tmp_y = MAP_Y - 40 if (tmp_y - FIGURE_HEIGHT) < 0 else (tmp_y - FIGURE_HEIGHT)
    elif pygame.key.get_pressed()[pygame.K_LEFT]:
        tmp_x = MAP_X - 40 if (tmp_x - FIGURE_WIDTH) < 0 else (tmp_x - FIGURE_WIDTH)
    if len(longs) > 0:
        if [tmp_x, tmp_y] == longs[0]:
            tmp_x, tmp_y = may_be
    return tmp_x, tmp_y

def for_longs(longs, color):
    for i, j in enumerate(longs):
        pygame.draw.rect(win, color, (longs[i][0], longs[i][1], FIGURE_WIDTH, FIGURE_HEIGHT))

def sending():
    msg = json.dumps({'block': block, 'snake': [[tmp_x, tmp_y]] + list(longs), 'color': COLOR}).encode('utf-8')
    sock.sendto(msg, SERVER)

def end():
    pygame.quit()
    sock.close()
    thread.join()
    exit()

block = True
ret = None
sending()

while ret is None:
    pass

while True:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            end()

    win.fill((0, 0, 0))
    if block == True:
        block = False
    pygame.draw.rect(*ret)
    if len(other) > 0:
        for i in other:
            for_longs(*i)   
    pygame.draw.rect(win, COLOR, (tmp_x, tmp_y, FIGURE_WIDTH, FIGURE_HEIGHT))
    try:
        for_longs(longs, COLOR)
    except:
        pass
    wide()

    res = move(tmp_x, tmp_y)
    if res != (tmp_x, tmp_y):
        if res == (ret[2][0], ret[2][1]):
            block = True
            longs.append([tmp_x, tmp_y])
        if len(longs) > 0:
            longs.rotate(1)
            longs[0] = [tmp_x, tmp_y]
        try:
            ind = longs.index([res[0], res[1]])
        except:
            if len(other) > 0:
                for i in (lambda: [i[0] for i in other])():
                    try:
                        ind = i.index([res[0], res[1]])
                    except:
                        ind = None
                    else:
                        break
            else:
                ind = None
        if ind is not None:
            longs.clear()

    other.clear()
    tmp_x, tmp_y = res
    sending()

    pygame.display.update()
    pygame.time.delay(100)