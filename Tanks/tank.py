import pygame
from enum import Enum

pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont(None, 55)
back = pygame.image.load("back.jpg")


sound = pygame.mixer.Sound('snd.wav')
goal = pygame.mixer.Sound("goal.wav")
music = pygame.mixer.music.load("win.mp3")



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
        pygame.draw.circle(screen, self.color, tank_c, int(self.width / 2))

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
        	self.x = -30
        if self.y > screen.get_size()[1] + 1:
        	self.y = -30
        if self.x < -30:
        	self.x = screen.get_size()[0]
        if self.y < -30:
        	self.y = screen.get_size()[1]
        
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

mainloop = True
tank1 = Tank(300, 300, 2, (255, 123, 100))
tank2 = Tank(100, 100, 2, (100, 230, 40), pygame.K_d, pygame.K_a, pygame.K_w, pygame.K_s)

shot1 = Shot(800, 800, 10, (255, 123, 100))
shot2 = Shot(800, 800, 10, (100, 230, 40))

tanks = [tank1, tank2]
shots = [shot1, shot2]

FPS = 60
clock = pygame.time.Clock()

gameover = 0
res1 = 3
res2 = 3
while mainloop:
    mills = clock.tick(FPS)
    if gameover == 1:

        screen.fill((0,0,0))
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
    else:

        pygame.mixer.music.stop()
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
        
        if tank1.x <= shots[1].x and tank1.x + tank1.width >= shots[1].x and tank1.y <= shots[1].y and tank1.y + tank1.width >= shots[1].y :
            res1 = res1 - 1
            shots[1].change(800, 800, Direction.DOWN)
            goal.play()
        if tank2.x <= shots[0].x and tank2.x + tank2.width >= shots[0].x and tank2.y <= shots[0].y and tank2.y + tank2.width >= shots[0].y :
            res2 = res2 - 1
            goal.play()
            shots[0].change(800, 800, Direction.DOWN)
        
        Text1 = font.render("Player1: " + str(res1), True, (0, 255, 0))
        Text2 = font.render("Player2: " + str(res2), True, (0, 255, 0))
        
        screen.blit(back, (0, 0))
        screen.blit(Text1, (5, 5))
        screen.blit(Text2, (600, 5))
        
        if res1 == 0 or res2 == 0:  
                pygame.mixer.music.play()
                gameover = 1        
        for shot in shots:
            shot.move()
        for tank in tanks:
            tank.move()

    pygame.display.flip()

pygame.quit()
