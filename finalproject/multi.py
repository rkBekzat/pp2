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
end = pygame.image.load('C:/Users/User/Desktop/ICT2020/pp2/myfinalproject/img/end.jpg')
sound = pygame.mixer.Sound('C:/Users/User/Desktop/ICT2020/pp2/myfinalproject/sounds/snd.wav')
goal = pygame.mixer.Sound("C:/Users/User/Desktop/ICT2020/pp2/myfinalproject/sounds/goal.wav")


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
            routing_key='event.state.room-5'
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


UP = "UP"
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

MOVE_KEYS = {
    pygame.K_w: UP,
    pygame.K_a: LEFT,
    pygame.K_s: DOWN,
    pygame.K_d: RIGHT,
}


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

def TakeSecond(elem):
    return elem[1]



def game_start():
    mainLoop = True
    gameover = 0
    score = 0
    font = pygame.font.Font("freesansbold.ttf", 16)
    current = 0
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
        for hit in hits:
            if hit['destination'] == client.tank_id:
                goal.play()
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
            text = font.render("YOU ARE WIN!!!", True, (255, 0, 0))
            screen.blit(text, (300, 300))
            text1 = font.render("YOUR SCORE:" + str(score), True, (255, 0, 0))
            screen.blit(text1, (300, 330))
        elif gameover == 2:
            text = font.render("YOU ARE LOSE;(", True, (255, 0, 0))
            screen.blit(text, (300, 300))
            text1 = font.render("YOUR SCORE:" + str(score), True, (255, 0, 0))
            screen.blit(text1, (300, 330))
        elif gameover == 3:
            text = font.render("YOU ARE KICKED:(", True, (255, 0, 0))
            screen.blit(text, (300, 300))
            text1 = font.render("YOUR SCORE:" + str(score), True, (255, 0, 0))
            screen.blit(text1, (300, 330))
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    mainloop = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainloop = False
                    if event.key in MOVE_KEYS:
                        client.turn_tank(client.token, MOVE_KEYS[event.key])
                    if event.key == pygame.K_SPACE:
                        client.fire_bullet(client.token)
                        sound.play()
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
                        text = font.render('me', True, (255, 0, 0))
                    else:
                        text = font.render(i[0], True, (255, 0, 0))
                    text1 = font.render(str(i[2]), True, (255, 0, 0))
                    text2 = font.render(str(i[1]), True, (255, 0, 0))
                    screen.blit(text, (850, cur * 15))
                    screen.blit(text1, (930, cur * 15))
                    screen.blit(text2, (1000, cur * 15))
            except:
                text = font.render('WINNERS', True, (0, 0, 255))
                screen.blit(text, (500, 200))
                cur = 10
                for win in winners:
                    cur = cur + 1
                    text = font.render(win['tankId'], True, (0, 0, 255))
                    screen.blit(text, (500, cur * 20))

        pygame.display.flip()

    client.connection.close()
    pygame.quit()


client = TankRpcClient()

client.check_server_status()
client.obtain_token('room-5')
event_client = TankConsumerClient('room-5')
event_client.start()
game_start()

  
