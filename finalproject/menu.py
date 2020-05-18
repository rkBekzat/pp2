import pygame

pygame.init()


screen = pygame.display.set_mode((800, 600))
font = pygame.font.SysFont(None, 55)
moon = pygame.image.load('moon.jpg')

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
            	import singl
            if event.key == pygame.K_2:
            	import multi
            if event.key == pygame.K_3:
            	import ai
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