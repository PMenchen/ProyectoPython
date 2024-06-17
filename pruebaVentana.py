import pygame
from tkinter import *
from tkinter import messagebox as MessageBox

HEIGHT = 480
WIDTH = 640

pygame.init()

window = pygame.display.set_mode((WIDTH,HEIGHT))#, pygame.RESIZABLE)
pygame.display.set_caption("bola con colisiones")

ball = pygame.image.load("./img/ball.png")
ballrect = ball.get_rect()
#speed = [1,1]
speed = [4.5,4.5]
ballrect.move_ip(0,0)

platform = pygame.image.load("./img/platform.png")
platformrect = platform.get_rect()
platformrect.move_ip(240,450)

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        """if event.type == pygame.VIDEORESIZE:
            platformrect = platform.get_rect()  
            platformrect.move_ip(window.get_width()/2, window.get_height() - 30)
            
            ballrect.x = (ballrect.x*100)/window.get_width()
            ballrect.y = (ballrect.y*100)/window.get_height()"""
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and not(platformrect.left < 0):
        platformrect = platformrect.move(-3.5,0)
    if keys[pygame.K_RIGHT] and not(platformrect.right > window.get_width()):
        platformrect = platformrect.move(3.5,0)
    
    if platformrect.colliderect(ballrect):
        speed[1] = -speed[1]
    
    ballrect = ballrect.move(speed)
    
    if ballrect.left < 0 or ballrect.right > window.get_width():
        speed[0] = -speed[0]
            
    if ballrect.top < 0 or ballrect.bottom > window.get_height():
        speed[1] = -speed[1]
    
    if ballrect.bottom >= window.get_height():
        if MessageBox.askretrycancel("Game Over"):
            platformrect = platform.get_rect()  
            platformrect.move_ip(window.get_width()/2, window.get_height() - 30)
            
            ballrect = ball.get_rect()
            ballrect.move_ip(0,0)
            speed = [4.5,4.5]
        else:
            run = False
    
    window.fill((255,255,255))
    window.blit(ball, ballrect)
    window.blit(platform, platformrect)
    pygame.display.flip()
    pygame.time.Clock().tick(60)
    
pygame.quit()