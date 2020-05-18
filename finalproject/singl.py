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