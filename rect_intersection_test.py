#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame

WIDTH, HEIGHT = 800, 800

if __name__ == "__main__":
    pygame.init()
    
    w = pygame.display.set_mode([WIDTH, HEIGHT])
    
    clock = pygame.time.Clock()
    
    r1 = [0,0,0,0]
    r2 = [0,0,0,0]
    
    while True:
        events = pygame.event.get()
        
        mousePos = list(pygame.mouse.get_pos())
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    r1 = mousePos + r1[2:]
                
                elif event.button == 3:
                    r2 = mousePos + r2[2:]
        
        if pygame.mouse.get_pressed()[0]:
            r1 = r1[:2] + [mousePos[0]-r1[0], mousePos[1]-r1[1]]
        
        elif pygame.mouse.get_pressed()[2]:
            r2 = r2[:2] + [mousePos[0]-r2[0], mousePos[1]-r2[1]]
        
        w.fill(0)
        
        prev, cur = r1, r2
        x1, y1, w1, h1 = prev
        x2, y2, w2, h2 = cur
        
        
        x3, y3, x4, y4 = max(x1,x2), max(y1,y2), min(x1+w1,x2+w2), min(y1+h1,y2+h2)
        
        r3 = [x3, y3, x4-x3, y4-y3]
        
        pygame.draw.rect(w, (255,0,0), r1)
        pygame.draw.rect(w, (0,255,0), r2)
        pygame.draw.rect(w, (255,255,0), r3)
        
        pygame.display.flip()
        
        clock.tick(60)