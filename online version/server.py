import json
import socket
import random

MAP_X = 800
MAP_Y = 400
FIGURE_HEIGHT = 40
FIGURE_WIDTH = 40

sock = socket.socket(socket.SOCK_DGRAM, socket.AF_INET)
sock.bind(('192.168.0.6', 8080))
users = []

def random_block():
    for_x = random.choice([i * 40 for i in range(int(MAP_X / 40))])
    for_y = random.choice([i * 40 for i in range(int(MAP_Y / 40))])
    return ((255, 0, 255), (for_x, for_y, FIGURE_WIDTH, FIGURE_HEIGHT))

while True:
    msg, addr = sock.recvfrom(8192)
    if addr not in users:
        users.append(addr)
    msg = json.loads(msg.decode('utf-8'))

    ret = random_block() if msg['block'] == True else None

    for user in users:
        if user != addr:
            sock.sendto(json.dumps({'block': ret, 'snake': msg["snake"], 'color': msg["color"]}).encode('utf-8'), user)
        else:
            sock.sendto(json.dumps({'block': ret}).encode('utf-8'), user)
sock.close()