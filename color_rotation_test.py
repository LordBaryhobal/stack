#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame

WIDTH, HEIGHT = 800, 800

if __name__ == "__main__":
    pygame.init()
    
    w = pygame.display.set_mode([WIDTH, HEIGHT])
    
    clock = pygame.time.Clock()
    
    col = pygame.Color(150,40,20)
    
    while True:
        w.fill(col)
        
        pygame.display.flip()
        
        clock.tick(60)
        
        hsva = list(col.hsva)
        hsva[0] += 1
        hsva[0] %= 360
        
        col.hsva = hsva