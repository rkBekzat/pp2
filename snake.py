import pygame
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))


class Snake:

    def __init__(self):
        self.size = 1
        self.elements = [[100, 100]]
        self.radius = 10
        self.dx = 5  # right
        self.dy = 0
        self.is_add = False

    def draw(self):
        for element in self.elements:
            pygame.draw.circle(screen, (255, 0, 0), element, self.radius)

    def add_to_snake(self):
        self.size += 1
        self.elements.append([0, 0])
        self.is_add = False

    def move(self):
        if self.is_add:
            self.add_to_snake()

        for i in range(self.size - 1, 0, -1):
            self.elements[i][0] = self.elements[i - 1][0]
            self.elements[i][1] = self.elements[i - 1][1]

        self.elements[0][0] += self.dx
        self.elements[0][1] += self.dy


snake = Snake()

def dist(a, b, c, d):
    return ((a - c) ** 2 + (b - d) ** 2)**0.5

def okay(x, y):
    if x < 20 or x > 780:
        return 0
    if y < 20 or y > 580:
        return 0;
    return 1;


class FOOD:
	def __init__(self):
		self.pos = [0, 0]

	def draw(self):
		pygame.draw.circle(screen, (0, 255, 0), self.pos, 10)

	def change_pos(self):
		t = True

		while t:
			ok = True
			self.pos[0] = random.randint(0, 800)
			self.pos[1] = random.randint(0, 600)
			for element in snake.elements:
				if dist(element[0], element[1], self.pos[0], self.pos[1]) <= 10 or not okay(self.pos[0], self.pos[1]):
					ok = False
					break
			if ok:
				break;



running = True

food = FOOD()
food.change_pos()

d = 5

FPS = 30

clock = pygame.time.Clock()

k1_pressed = False
print(food.pos)

while running:
    mill = clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_RIGHT:
                snake.dx = d
                snake.dy = 0
            if event.key == pygame.K_LEFT:
                snake.dx = -d
                snake.dy = 0
            if event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -d
            if event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = d

    if dist(snake.elements[0][0] + snake.dx , snake.elements[0][1] + snake.dy, food.pos[0],  food.pos[1]) < 10:
        snake.is_add = True
        food.change_pos()
    if not okay(snake.elements[0][0] + snake.dx , snake.elements[0][1] + snake.dy):
        running = False
    snake.move()
    screen.fill((0, 0, 0))
    snake.draw()
    food.draw()
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(0, 0, 20, 600))
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(780, 0, 20, 600))
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(0, 0, 800, 20))
    pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(0, 580, 800, 20))
    
    pygame.display.flip()
