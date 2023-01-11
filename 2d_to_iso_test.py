#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame

WIDTH, HEIGHT = 800, 400

if __name__ == "__main__":
    pygame.init()
    
    w = pygame.display.set_mode([WIDTH, HEIGHT])
    
    clock = pygame.time.Clock()
    
    while True:
        w.fill(0)
        
        pygame.event.get()
        
        x, y = pygame.mouse.get_pos()
        
        #x2, y2 = (y*2 / 2) + (x*2 / 2), (x*1 / 2) - (y*1 / 2)
        
        x2 = (x-y) * (1/2) + 200
        y2 = (x+y) * (1/4) - 300
        
        pygame.draw.circle(w, (255,255,255), [int(x), int(y)], 10)
        pygame.draw.circle(w, (255,0,0), [int(x2+400), int(y2+400)], 10)
        
        pygame.draw.line(w, (255,255,255), [400,0],[400,400])
        
        pygame.display.flip()
        
        clock.tick(60)