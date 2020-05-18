import json
from threading import Thread
import pika
import uuid
import pygame

IP = '34.254.177.17'
PORT = 5672
VIRTUAL_HOST = 'dar-tanks'
USERNAME = 'dar-tanks'
PASSWORD = '5orPLExUYnyVYZg48caMpX'

pygame.init()
screen = pygame.display.set_mode((1100, 600))
my_tankid = 0
back = pygame.image.load('C:/Users/User/Desktop/ICT2020/pp2/myfinalproject/img/background.jpg')
win = pygame.image.load('C:/Users/User/Desktop/ICT2020/pp2/myfinalproject/img/win2.jpg')
end = pygame.image.load('C:/Users/User/Desktop/ICT2020/pp2/myfinalproject/img/end.jpg')


class TankRpcClient:

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,
                port=PORT,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=USERNAME,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue='',
                                           auto_delete=True,
                                           exclusive=True
                                           )
        self.callback_queue = queue.method.queue
        self.channel.queue_bind(
            exchange='X:routing.topic',
            queue=self.callback_queue
        )

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.corr_id = None
        self.token = None
        self.tank_id = None
        self.room_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = json.loads(body)


    def call(self, key, message=''):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='X:routing.topic',
            routing_key=key,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(message)
        )
        while self.response is None:
            self.connection.process_data_events()

    def check_server_status(self):
        self.call('tank.request.healthcheck')

    def obtain_token(self, room_id):
        message = {
            'roomId': room_id
        }
        self.call('tank.request.register', message)
        if 'token' in self.response:
            self.token = self.response['token']
            self.tank_id = self.response['tankId']
            self.room_id = self.response['roomId']
            return True
        return False

    def turn_tank(self, token, direction):
        message = {
            'token': token,
            'direction': direction
        }
        self.call('tank.request.turn', message)

    def fire_bullet(self, token):
        message = {
            'token' : token
        }
        self.call('tank.request.fire', message)


class TankConsumerClient(Thread):

    def __init__(self, room_id):
        super().__init__()
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=IP,
                port=PORT,
                virtual_host=VIRTUAL_HOST,
                credentials=pika.PlainCredentials(
                    username=USERNAME,
                    password=PASSWORD
                )
            )
        )
        self.channel = self.connection.channel()
        queue = self.channel.queue_declare(queue='',
                                           auto_delete=True,
                                           exclusive=True
                                           )
        event_listener = queue.method.queue
        self.channel.queue_bind(
            exchange='X:routing.topic',
            queue=event_listener,
            routing_key='event.state.room-14'
        )

        self.channel.basic_consume(
            queue=event_listener,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None

    def on_response(self, ch, method, props, body):
        self.response = json.loads(body)

    def run(self):
        self.channel.start_consuming()


import math

def TakeSecond(elem):
    return elem[1]


def draw_tank(id, x, y, width, height, direction, **kwargs):
    if id == client.tank_id:
        color = (0, 255, 0)
    else:
        color = (255, 0, 0)
    tank_c = (x + int(width / 2), y + int(width / 2))
    pygame.draw.rect(screen, color,
                     (x, y, width, width))

    new = (max(0, color[0] - 70), max(0, color[1] - 70), max(0, color[2] - 70))

    pygame.draw.circle(screen, (new), tank_c, int(width / 4))

    if direction == 'RIGHT':
        pygame.draw.line(screen, color, tank_c, (x + width + int(width / 2), y + int(height / 2)), 4)
    if direction == 'LEFT':
        pygame.draw.line(screen, color, tank_c, (x - int(width / 2), y + int(height / 2)), 4)
    if direction == 'UP':
        pygame.draw.line(screen, color, tank_c, (x + int(width / 2), y - int(height / 2)), 4)
    if direction == 'DOWN':
        pygame.draw.line(screen, color, tank_c, (x + int(width / 2), y + height + int(height / 2)), 4)



def draw_bullet(owner, x, y, width, height, direction, **kwargs):
    if owner == client.tank_id:
        color = (0, 255, 0)
    else:
        color = (255, 0, 0)
    pygame.draw.rect(screen, color, (x, y, width, height))


def dist(x, y, bulx, buly, direction):
    if x <= bulx and bulx <= x + 30:
        if direction == 'LEFT' or direction == 'RIGHT':
            return 200
        if direction == 'UP':
            if y < buly:
                return buly - y
            else:
                return buly + 631 - y
        else:
            if y > buly:
                return  y - buly
            else:
                return y + 631 - buly
    if y <= buly and buly <= y + 30:
        if direction == 'UP' or direction == 'DOWN':
            return 200
        if direction == 'LEFT':
            if x < bulx:
                return bulx - x
            else:
                return bulx + 631 - x
        else:
            if x > bulx:
                return  x - bulx
            else:
                return x + 631 - bulx
    return 200


def calc(x, y, direction, bullet):
    to_x = x
    to_y = y
    if direction == 'UP':
        to_y = to_y - 40
        to_y = (to_y + 631) % 631
    if direction == 'DOWN':
        to_y = to_y + 40
        to_y = to_y % 631
    if direction == 'LEFT':
        to_x = to_x - 40
        to_x = (to_x + 631) % 631
    if direction == 'RIGHT':
        to_x = to_x + 40
        to_x = to_x % 631
    if dist(to_x, to_y, bullet['x'], bullet['y'], bullet['direction']) < 100:
        return 0
    return 1  

def intersec(x, y, w, a, b, c):
    for i in range(a, a + c + 1):
        for j in range(b, b + c + 1):
            if x <= i and i <= x + 30 and y <= j and j <= y + 30:
                return 1
    return 0


possible_direction = list()    

def calc_tank(x, y, direction, tanchik):
    to_x = x
    to_y = y
    if direction == 'UP':
        to_y = to_y - 40
        to_y = (to_y + 631) % 631
    if direction == 'DOWN':
        to_y = to_y + 40
        to_y = to_y % 631
    if direction == 'LEFT':
        to_x = to_x - 40
        to_x = (to_x + 631) % 631
    if direction == 'RIGHT':
        to_x = to_x + 40
        to_x = to_x % 631
    if intersec(to_x, to_y, 40, int(tanchik['x']), int(tanchik['y']), 40) == 1:
        return 0
    return 1


def choose_dir():
    global possible_direction
    bullets = event_client.response['gameField']['bullets']
    tanks = event_client.response['gameField']['tanks']
    ok = 0
    del possible_direction
    for tank in tanks:
        if tank['id'] == client.tank_id:
            my_tank = tank
            ok = 1
    all_dir = list()    
    all_dir.append('DOWN')
    all_dir.append('UP')
    all_dir.append('LEFT')
    all_dir.append('RIGHT')
    if ok:
        for direc in all_dir:
            ok = 1
            for bullet in bullets:
                if bullet['owner'] != my_tank['id']:
                    if calc(my_tank['x'], my_tank['y'], direc, bullet) == 0:
                        ok = 0
                        break
            if ok:
                for tank in tanks:
                    if my_tank != tank:
                        if calc_tank(my_tank['x'], my_tank['y'], direc, tank) == 0:
                            ok = 0
                            break
                if ok:
                    possible_direction.append(direc)
                



def fire():
    global possible_direction
    bullets = event_client.response['gameField']['bullets']
    tanks = event_client.response['gameField']['tanks']
    ok = 0
    for tank in tanks:
        if tank['id'] == client.tank_id:
            my_tank = tank
            ok = 1
    if ok :
        for tank in tanks:
            if tank != my_tank:
                if tank['x'] <= my_tank['x'] + 15 and my_tank['x'] + 15 <= tank['x'] + 30:

                    if 'DOWN' in possible_direction and 'UP' in possible_direction:
                        if tank['y'] < my_tank['y']:
                            if my_tank['y'] - tank['y'] > tank['y'] + 631 - my_tank['y']:
                                client.turn_tank(client.token, 'DOWN')
                                client.fire_bullet(client.token)
                            else:
                                client.turn_tank(client.token, 'UP')
                                client.fire_bullet(client.token)
                        else:
                            if tank['y'] - my_tank['y'] > my_tank['y'] + 631 - tank['y']:
                                client.turn_tank(client.token, 'UP')
                                client.fire_bullet(client.token)
                            else:
                                client.turn_tank(client.token, 'DOWN')
                                client.fire_bullet(client.token)

                    elif 'DOWN' in possible_direction:    
                        client.turn_tank(client.token, 'DOWN')
                        client.fire_bullet(client.token)

                    elif 'UP' in possible_direction:
                        client.turn_tank(client.token, 'UP')
                        client.fire_bullet(client.token)

                if tank['y'] <= my_tank['y'] + 15 and my_tank['y'] + 15 <= tank['y'] + 30:

                    if 'LEFT' in possible_direction and 'RIGHT' in possible_direction:
                        if tank['x'] < my_tank['x']:
                            if my_tank['x'] - tank['x'] > tank['x'] + 631 - my_tank['x']:
                                client.turn_tank(client.token, 'RIGHT')
                                client.fire_bullet(client.token)
                            else:
                                client.turn_tank(client.token, 'LEFT')
                                client.fire_bullet(client.token)
                        else:
                            if tank['x'] - my_tank['x'] > my_tank['x'] + 631 - tank['x']:
                                client.turn_tank(client.token, 'LEFT')
                                client.fire_bullet(client.token)
                            else:
                                client.turn_tank(client.token, 'RIGHT')
                                client.fire_bullet(client.token)

                    elif 'LEFT' in possible_direction:    
                        client.turn_tank(client.token, 'LEFT')
                        client.fire_bullet(client.token)

                    elif 'RIGHT' in possible_direction:
                        client.turn_tank(client.token, 'RIGHT')
                        client.fire_bullet(client.token)




def game_start():
    mainLoop = True
    gameover = 0
    score = 0
    font = pygame.font.Font("freesansbold.ttf", 16)
    client.turn_tank(client.token, 'UP')
    while mainLoop:

        hits = event_client.response['hits']
        bullets = event_client.response['gameField']['bullets']
        winners = event_client.response['winners']
        losers = event_client.response['losers']
        kicked = event_client.response['kicked']
        tanks = event_client.response['gameField']['tanks']
        
        screen.fill((0, 0, 0))
        
        for win in winners:
            if win['tankId'] == client.tank_id:
                gameover = 1
                score = win['score']
        
        for win in losers:
            if win['tankId'] == client.tank_id:
                gameover = 2
                score = win['score']

        for win in kicked:
            if win['tankId'] == client.tank_id:
                gameover = 3
                score = win['score']

        if gameover > 0:
            text = font.render("FOR RESTART GAME PLEASE PUSH R", True, (255, 0, 0))
            screen.blit(text, (250, 270))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False
                    if event.key == pygame.K_r:
                        client.obtain_token('room-5')
                        game_start()


        if gameover == 1:
            text = font.render("YOUR AI WIN!!!", True, (255, 0, 0))
            screen.blit(text, (300, 300))
            text1 = font.render("YOUR AI SCORE:" + str(score), True, (255, 0, 0))
            screen.blit(text1, (300, 330))
        elif gameover == 2:
            text = font.render("YOUR AI LOSE;(", True, (255, 0, 0))
            screen.blit(text, (300, 300))
            text1 = font.render("YOUR AI SCORE:" + str(score), True, (255, 0, 0))
            screen.blit(text1, (300, 330))
        elif gameover == 3:
            text = font.render("YOUR AI KICKED:(", True, (255, 0, 0))
            screen.blit(text, (300, 300))
            text1 = font.render("YOUR AI SCORE:" + str(score), True, (255, 0, 0))
            screen.blit(text1, (300, 330))
        else:
            choose_dir()
            fire()
            try:
                remaining_time = event_client.response['remainingTime']
                text = font.render('Remaining time: {}'.format(remaining_time), True, (255, 255, 255))
                textRect = text.get_rect()
                textRect.center = (400, 20)

                screen.blit(back, (0, 0))
                a = list()
                screen.blit(text, textRect)
                for tank in tanks:
                    draw_tank(**tank)
                    a.append((tank['id'],  tank['score'], tank['health']))
                for bullet in bullets:
                    draw_bullet(**bullet) 
                a.sort(key=TakeSecond, reverse=True)
                
                screen.blit(end, (800, 0))
                cur = 1
                text = font.render('Who', True, (255, 0, 0))
                text1 = font.render("Live", True, (255, 0, 0))
                text2 = font.render("Score", True, (255, 0, 0))
                screen.blit(text, (850, cur * 15))
                screen.blit(text1, (930, cur * 15))
                screen.blit(text2, (1000, cur * 15))
                for i in a:
                    cur = cur + 1
                    if i[0] == client.tank_id:
                        text = font.render('MY AI', True, (255, 0, 0))
                    else:
                        text = font.render(i[0], True, (255, 0, 0))
                    text1 = font.render(str(i[2]), True, (255, 0, 0))
                    text2 = font.render(str(i[1]), True, (255, 0, 0))
                    screen.blit(text, (850, cur * 15))
                    screen.blit(text1, (930, cur * 15))
                    screen.blit(text2, (1000, cur * 15))
            except:
                pass
        pygame.display.flip()

    client.connection.close()
    pygame.quit()    


client = TankRpcClient()

client.check_server_status()
client.obtain_token('room-14')
event_client = TankConsumerClient('room-14')
event_client.start()
game_start()
