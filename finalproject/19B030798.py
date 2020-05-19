import pygame

pygame.init()


screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont(None, 55)
moon = pygame.image.load('C:/Users/User/Desktop/ICT2020/pp2/myfinalproject/img/moon.jpg')

running = 1

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_1:
                import pygame
                from enum import Enum
                import random

                pygame.init()
                screen = pygame.display.set_mode((800, 600))
                font = pygame.font.SysFont(None, 55)
                back = pygame.image.load("C:/Users/User/Desktop/ICT2020/pp2/myfinalproject/img/back2.jpg")
                pp = pygame.image.load('C:/Users/User/Desktop/ICT2020/pp2/myfinalproject/img/power.png')
                brick = pygame.image.load('C:/Users/User/Desktop/ICT2020/pp2/myfinalproject/img/brick.png')
                win = pygame.image.load('C:/Users/User/Desktop/ICT2020/pp2/myfinalproject/img/win2.jpg')

                sound = pygame.mixer.Sound('C:/Users/User/Desktop/ICT2020/pp2/myfinalproject/sounds/snd.wav')
                goal = pygame.mixer.Sound("C:/Users/User/Desktop/ICT2020/pp2/myfinalproject/sounds/goal.wav")
                music = pygame.mixer.music.load("C:/Users/User/Desktop/ICT2020/pp2/myfinalproject/sounds/win.mp3")



                class Direction(Enum):
                    UP = 1
                    DOWN = 2
                    LEFT = 3
                    RIGHT = 4


                class Tank:

                    def __init__(self, x, y, speed, color, d_right=pygame.K_RIGHT, d_left=pygame.K_LEFT, d_up=pygame.K_UP, d_down=pygame.K_DOWN):
                        self.x = x
                        self.y = y
                        self.speed = speed
                        self.color = color
                        self.width = 40
                        self.direction = Direction.RIGHT

                        self.KEY = {d_right: Direction.RIGHT, d_left: Direction.LEFT,
                                    d_up: Direction.UP, d_down: Direction.DOWN}

                    def draw(self):
                        tank_c = (self.x + int(self.width / 2), self.y + int(self.width / 2))
                        pygame.draw.rect(screen, self.color,
                                         (self.x, self.y, self.width, self.width))
                        new = (max(0, self.color[0] - 70), max(0, self.color[1] - 70), max(0, self.color[2] - 70))

                        pygame.draw.circle(screen, (new), tank_c, int(self.width / 4))
                 
                        if self.direction == Direction.RIGHT:
                            pygame.draw.line(screen, self.color, tank_c, (self.x + self.width + int(self.width / 2), self.y + int(self.width / 2)), 4)

                        if self.direction == Direction.LEFT:
                            pygame.draw.line(screen, self.color, tank_c, (
                            self.x - int(self.width / 2), self.y + int(self.width / 2)), 4)

                        if self.direction == Direction.UP:
                            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width / 2), self.y - int(self.width / 2)), 4)

                        if self.direction == Direction.DOWN:
                            pygame.draw.line(screen, self.color, tank_c, (self.x + int(self.width / 2), self.y + self.width + int(self.width / 2)), 4)


                    def change_direction(self, direction):
                        self.direction = direction

                    def change_color(self, color):
                        self.color = color

                    def change_speed(self, speed):
                        self.speed = speed

                    def change_pos(self, x, y):
                        self.x = x
                        self.y = y

                    def move(self):
                        if self.direction == Direction.LEFT:
                            self.x -= self.speed
                        if self.direction == Direction.RIGHT:
                            self.x += self.speed
                        if self.direction == Direction.UP:
                            self.y -= self.speed
                        if self.direction == Direction.DOWN:
                            self.y += self.speed
                        if self.x > screen.get_size()[0] + 1:
                            self.x = -20
                        if self.y > screen.get_size()[1] - 10:
                            self.y = -20
                        if self.x < -30:
                            self.x = screen.get_size()[0]
                        if self.y < -30:
                            self.y = screen.get_size()[1] - 10
                        
                        self.draw()


                class Shot:

                    def __init__(self, x, y, speed, color):
                        self.x = x
                        self.y = y
                        self.speed = speed
                        self.color = color

                        self.direction = Direction.RIGHT

                    def draw(self):
                        pygame.draw.rect(screen, self.color, (self.x, self.y, 7, 7))

                    def change(self, x, y, direction):
                        self.x = x
                        self.y = y
                        self.direction = direction

                    def change_color(self, color):
                        self.color = color

                    def move(self):
                        if self.direction == Direction.LEFT:
                            self.x -= self.speed
                        if self.direction == Direction.RIGHT:
                            self.x += self.speed
                        if self.direction == Direction.UP:
                            self.y -= self.speed
                        if self.direction == Direction.DOWN:
                            self.y += self.speed
                        self.draw()


                class WALL:    
                    def __init__(self, x, y):
                        self.x = x
                        self.y = y

                    def draw(self):
                        screen.blit(brick, (self.x, self.y))

                    def change(self, x, y):
                        self.x = x
                        self.y = y

                class Power:
                    def __init__(self, x, y):
                        self.x = x
                        self.y = y

                    def draw(self):
                        screen.blit(pp, (self.x, self.y))

                    def change(self, x, y):
                        self.x = x
                        self.y = y


                def draw(x, y, color, width, direction):
                    tank_c = (x + int(width / 2), y + int(width / 2))
                    pygame.draw.rect(screen, color,
                                     (x, y, width, width))

                    new = (max(0, color[0] - 70), max(0, color[1] - 70), max(0, color[2] - 70))

                    pygame.draw.circle(screen, (new), tank_c, int(width / 4))
                    if direction == Direction.RIGHT:
                        pygame.draw.line(screen, color, tank_c, (x + width + int(width / 2), y + int(width / 2)), 4)

                    if direction == Direction.LEFT:
                        pygame.draw.line(screen, color, tank_c, (
                        x - int(width / 2), y + int(width / 2)), 4)

                    if direction == Direction.UP:
                        pygame.draw.line(screen, color, tank_c, (x + int(width / 2), y - int(width / 2)), 4)

                    if direction == Direction.DOWN:
                        pygame.draw.line(screen, color, tank_c, (x + int(width / 2), y + width + int(width / 2)), 4)    


                mainloop = True
                tank1 = Tank(300, 300, 2, (255, 123, 100))
                tank2 = Tank(100, 100, 2, (100, 230, 40), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)

                shot1 = Shot(800, 800, 10, (255, 123, 100))
                shot2 = Shot(800, 800, 10, (100, 230, 40))

                tanks = [tank1, tank2]
                shots = [shot1, shot2]

                power = Power(random.randint(0, 600), random.randint(0, 800))

                FPS = 60
                clock = pygame.time.Clock()

                gameover = 0
                res1 = 3
                res2 = 3
                start = 1

                walls = list()

                for i in range(10):
                    new_wall1 = WALL(random.randint(0, 600), random.randint(0, 600))
                    new_wall2 = WALL(new_wall1.x + 30, new_wall1.y)
                    new_wall3 = WALL(new_wall1.x, new_wall1.y + 30)
                    new_wall4 = WALL(new_wall1.x + 30, new_wall1.y + 30)
                    walls.append(new_wall1)
                    walls.append(new_wall2)
                    walls.append(new_wall3)
                    walls.append(new_wall4)


                def intersec(x, y, w, a, b, c):
                    for i in range(a, a + c + 1):
                        for j in range(b, b + c + 1):
                            if x <= i and i <= x + 30 and y <= j and j <= y + 30:
                                return 1
                    return 0
                    

                timer = 0
                cur = 0
                q = random.randint(2, 6)
                while mainloop:
                    mills = clock.tick(FPS)

                    if gameover == 1:
                        screen.fill((0,0,0))
                        screen.blit(win, (0, 0))
                        string = font.render("Game Is Over", True, (255, 0, 0))
                        cont = font.render("Press ENTER to continue", True, (255, 0, 0))
                        screen.blit(string, (200, 200))
                        screen.blit(cont, (150, 240))

                        if res1 == 0:
                            lst = font.render("Second Player win", True, (255, 0, 0))
                            screen.blit(lst, (200, 280))
                        if res2 == 0:
                            lst = font.render("First Player win", True, (255, 0, 0))
                            screen.blit(lst, (200, 280))
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                mainloop = False
                            if event.type == pygame.KEYDOWN:  
                                if event.key == pygame.K_RETURN:
                                    gameover = 0
                                    res1 = 3
                                    res2 = 3
                                    start = 1   
                                for i in range(10):
                                    walls[i*4].change(random.randint(0, 800), random.randint(0, 600))
                                    walls[i*4 + 1].change(walls[i*4].x + 30, walls[i*4].y)
                                    walls[i*4 + 2].change(walls[i*4].x, walls[i*4].y + 30)
                                    walls[i*4 + 3].change(walls[i*4].x + 30, walls[i*4].y + 30)
                    else:
                        if start > 0:
                            pygame.mixer.music.stop()   
                            screen.fill((0, 0, 0))
                            if start == 1:
                                Text = font.render("First Player choose your color", True, (0, 255, 0))
                            else:
                                Text = font.render("Second Player choose your color", True, (0, 255, 0))
                            screen.blit(Text, (150, 150))
                            txt1 = font.render("Push 1", True, (255, 0, 0))
                            txt2 = font.render("Push 2", True, (0, 255, 0))
                            txt3 = font.render("Push 3", True, (0, 0, 255))
                            screen.blit(txt1, (100, 300))
                            screen.blit(txt2, (300, 300))
                            screen.blit(txt3, (500, 300))
                            draw(150, 400, (255, 0, 0), 40, Direction.UP) 
                            draw(350, 400, (0, 255, 0), 40, Direction.UP)
                            draw(550, 400, (0, 0, 255), 40, Direction.UP)
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    mainloop = False
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        mainloop = False
                                    if start == 1:
                                        tanks[0].change_speed(2)
                                        pos = (random.randint(0, 800), random.randint(0, 600))
                                        while True:
                                            ok = 1
                                            for wall in walls:
                                                if intersec(wall.x, wall.y, 60, pos[0], pos[1], 40):
                                                    ok = 0
                                                    break
                                            if ok:
                                                break
                                            else:
                                                pos = (random.randint(0, 800), random.randint(0, 600))
                                        tanks[0].change_pos(pos[0], pos[1])
                                        if event.key == pygame.K_1:
                                            tanks[0].change_color((255, 0, 0))
                                            start = 2
                                        
                                        if event.key == pygame.K_2:
                                            tanks[0].change_color((0, 255, 0))
                                            start = 2
                                        
                                        if event.key == pygame.K_3:    
                                            tanks[0].change_color((0, 0, 255))
                                            start = 2
                                    else:
                                        tanks[1].change_speed(2)
                                        pos = (random.randint(0, 800), random.randint(0, 600))
                                        while True:
                                            ok = 1
                                            for wall in walls:
                                                if intersec(wall.x, wall.y, 60, pos[0], pos[1], 40):
                                                    ok = 0
                                                    break
                                            if ok:
                                                break
                                            else:
                                                pos = (random.randint(0, 800), random.randint(0, 600))
                                        tanks[1].change_pos(pos[0], pos[1])
                                        if event.key == pygame.K_1:
                                            tanks[1].change_color((255, 0, 0))
                                            start = 0
                                        if event.key == pygame.K_2:
                                            tanks[1].change_color((0, 255, 0))
                                            start = 0
                                        if event.key == pygame.K_3:
                                            tanks[1].change_color((0, 0, 255))
                                            start = 0
                        else:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    mainloop = False
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_ESCAPE:
                                        mainloop = False
                                    if event.key == pygame.K_SPACE:
                                        if shots[1].x > screen.get_size()[0] or  shots[1].x < 0 or shots[1].y > screen.get_size()[0] or  shots[1].y < 0:
                                            shots[1].change(tank2.x + tank2.width / 2, tank2.y + tank2.width / 2, tank2.direction)
                                            sound.play()
                                    if event.key == pygame.K_RETURN:
                                        if shots[0].x > screen.get_size()[0] or  shots[0].x < 0 or shots[0].y > screen.get_size()[0] or  shots[0].y < 0:
                                            shots[0].change(tank1.x + tank1.width / 2, tank1.y + tank1.width / 2, tank1.direction)
                                            sound.play()
                                    for tank in tanks:
                                        if event.key in tank.KEY.keys():
                                            tank.change_direction(tank.KEY[event.key])
                            screen.fill((0, 0, 0))
                            
                            screen.blit(back, (-250, -250))
                            
                            if res1 + res2 == q:
                                cur = cur + 1
                                power.draw()
                                if intersec(power.x, power.y, 20, tanks[0].x, tanks[0].y, tanks[0].width):
                                    tanks[0].change_speed(5)
                                    timer = 0
                                    for wall in walls:
                                        while  power == wall:
                                            power.change(random.randint(0, 600), random.randint(0, 800))
                                    q = random.randint(2, 6)

                                if intersec(power.x, power.y, 20, tanks[1].x, tanks[1].y, tanks[1].width):
                                    tanks[1].change_speed(5)
                                    timer = 0
                                    q = random.randint(2, 6)
                                    for wall in walls:
                                        while  power == wall:
                                            power.change(random.randint(0, 600), random.randint(0, 800))
                                if cur > 700 and q == res1 + res2:
                                    q = random.randint(2, 6)
                            else:
                                cur = 0

                            timer = timer + 1

                            if timer > 400:
                                for tank in tanks:
                                    tank.change_speed(2)

                            for wall in walls:
                                if intersec(wall.x, wall.y, 30, tanks[0].x, tanks[0].y, 40):
                                    res1 = res1 - 1
                                    wall.change(800, 800)
                                if intersec(wall.x, wall.y, 30, tanks[1].x, tanks[1].y, 40):
                                    res2 = res2 - 1
                                    wall.change(800, 800)
                                for shot in shots:
                                    if intersec(wall.x, wall.y, 30, shot.x, shot.y, 7): 
                                        wall.change(800, 800)
                                        shot.change(800, 800, Direction.DOWN)              


                            if tanks[0].x <= shots[1].x and tanks[0].x + tanks[0].width >= shots[1].x and tanks[0].y <= shots[1].y and tanks[0].y + tanks[0].width >= shots[1].y :
                                res1 = res1 - 1
                                shots[1].change(800, 800, Direction.DOWN)
                                goal.play()
                            if tanks[1].x <= shots[0].x and tanks[1].x + tanks[1].width >= shots[0].x and tanks[1].y <= shots[0].y and tanks[1].y + tanks[1].width >= shots[0].y :
                                res2 = res2 - 1
                                goal.play()
                                shots[0].change(800, 800, Direction.DOWN)

                            Text1 = font.render("Player1: " + str(res1), True, (0, 255, 0))
                            Text2 = font.render("Player2: " + str(res2), True, (0, 255, 0))
                            
                            screen.blit(Text1, (5, 5))
                            screen.blit(Text2, (600, 5))
                            
                            if res1 == 0 or res2 == 0:  
                                pygame.mixer.music.play()
                                gameover = 1        
                            for shot in shots:
                                shot.move()
                            for tank in tanks:
                                tank.move()
                            for wall in walls:
                                wall.draw()

                    pygame.display.flip()

                pygame.quit()
                
            if event.key == pygame.K_2:
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

              

                  

            if event.key == pygame.K_3:
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



                def calc(x, y, direction, bullet):
                    to_x = x
                    to_y = y
                    if direction == 'UP':
                        to_y = to_y - 20
                    if direction == 'DOWN':
                        to_y = to_y + 20
                    if direction == 'LEFT':
                        to_x = to_x - 20
                    if direction == 'RIGHT':
                        to_x = to_x + 20
                    if to_x <= bullet['x'] and bullet['x'] <= to_x + 30:
                        if to_y < bullet['y']:
                            if bullet['direction'] == 'UP':
                                return 0
                        else:
                            if bullet['direction'] == 'DOWN':
                                return 0

                    if to_y <= bullet['y'] and bullet['y'] <= to_y + 30:
                        if to_x < bullet['x']:
                            if bullet['direction'] == 'LEFT':
                                return 0
                        else:
                            if bullet['direction'] == 'RIGHT':
                                return 0
                    return 1  

                def intersec(x, y, w, a, b, c):
                    for i in range(a, a + c + 1):
                        for j in range(b, b + c + 1):
                            if x <= i and i <= x + 30 and y <= j and j <= y + 30:
                                return 1
                    return 0
                    

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
                    if intersec(to_x, to_y, 40, int(tanchik['x']), int(tanchik['y']), 40):
                        return 0
                    return 1


                def choose_dir():
                    bullets = event_client.response['gameField']['bullets']
                    tanks = event_client.response['gameField']['tanks']
                    ok = 0
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
                        ok = 1
                        for bullet in bullets:
                            if bullet['owner'] != my_tank['id']:
                                if calc(my_tank['x'], my_tank['y'], my_tank['direction'], bullet) == 0:
                                    ok = 0
                        for tank in tanks:
                            if my_tank != tank:
                                if calc_tank(my_tank['x'], my_tank['y'], my_tank['direction'], tank) == 1:
                                    ok = 0
                        if ok == 0:  
                            for direc in all_dir:
                                ok = 1
                                for bullet in bullets:
                                    if bullet['owner'] != my_tank['id']:
                                        if calc(my_tank['x'], my_tank['y'], direc, bullet) == 0:
                                            ok = 0
                                if ok:
                                    for tank in tanks:
                                        if my_tank != tank:
                                            if calc_tank(my_tank['x'], my_tank['y'], direc, tank) == 1:
                                                ok = 0
                                    if ok:
                                        client.turn_tank(client.token, direc)
                                        break


                def fire():
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

                                if my_tank['x'] + 15 >= tank['x'] and my_tank['x'] + 15 <= tank['x'] + 30 and abs(my_tank['y'] - tank['y']) < 600:
                                    if my_tank['y'] < tank['y']:
                                        if calc_tank(my_tank['x'], my_tank['y'], 'DOWN', tank) == 1:
                                            client.turn_tank(client.token, 'DOWN')
                                            client.fire_bullet(client.token)
                                        else:
                                            client.turn_tank(client.token, 'UP')
                                            client.fire_bullet(client.token)
                                    else:
                                        if calc_tank(my_tank['x'], my_tank['y'], 'UP', tank) == 1:
                                            client.turn_tank(client.token, 'UP')
                                            client.fire_bullet(client.token)
                                        else:
                                            client.turn_tank(client.token, 'DOWN')
                                            client.fire_bullet(client.token)


                                if my_tank['y'] + 15 >= tank['y'] and my_tank['y'] + 15 <= tank['y'] + 30 and abs(my_tank['x'] - tank['x']) < 600:
                                    if my_tank['x'] < tank['x']:
                                        if calc_tank(my_tank['x'], my_tank['y'], 'RIGHT', tank) == 1:
                                            client.turn_tank(client.token, 'RIGHT')
                                            client.fire_bullet(client.token)
                                        else:
                                            client.turn_tank(client.token, 'LEFT')
                                            client.fire_bullet(client.token)
                                            
                                    else:
                                        if calc_tank(my_tank['x'], my_tank['y'], 'LEFT', tank) == 1:
                                            client.turn_tank(client.token, 'LEFT')
                                            client.fire_bullet(client.token)
                                        else:
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
                            fire()
                            choose_dir()
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
                client.obtain_token('room-5')
                event_client = TankConsumerClient('room-5')
                event_client.start()
                game_start()


    screen.blit(moon, (-150, 0))	
    text = font.render("Menu", True, (125, 125, 125))
    screen.blit(text, (250, 200))
    text1 = font.render("Single Player - push 1", True, (255, 0, 0))
    screen.blit(text1, (150, 250))
    text2 = font.render("MultiPlayer - push 2", True, (0, 255, 0))
    screen.blit(text2, (150, 300))
    text3 = font.render('AI mode - push 3', True, (0, 0, 255))
    screen.blit(text3, (150, 350))
    pygame.display.flip()

pygame.quit()
