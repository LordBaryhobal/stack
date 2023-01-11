#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame, random, time
from math import copysign

WIDTH, HEIGHT = 800, 800

class Game:
    colours = [
        (150,40,20),
        (20,60,150),
        (20,120,40)
    ]

    height = 20
    margin = 10

    perfects_in_row = 8
    perfect_add = 10

    speed = 3

    bg_colour = (210,200,100)

    perfect_duration = 0.2
    perfect_last = 0.3

    first_size = 100

    def __init__(self, iso=False):
        self.rectangles = [
            [random.choice(self.colours), WIDTH//2-self.first_size//2, HEIGHT//2-self.first_size//2,self.first_size,self.first_size]
        ]

        #self.colour = [1,1,1]

        self.score = 0

        self.current = []

        self.gen_rect()

        self.iso = iso

        #self.font = pygame.font.SysFont("timesnewroman", 60)
        self.font = pygame.font.SysFont("dyuthi", 60)

        self.perfects = 0

        self.last_perfect = time.time()

    def loop(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.place()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.place()

        speed = self.speed * (1+self.score/20)

        if self.perfects >= self.perfects_in_row:
            speed *= 1.2

        if self.score % 2 == 0:
            self.current[1] += speed

        else:
            self.current[2] += speed

    def display(self, window):
        window.fill(self.bg_colour)

        if not self.iso:
            for rect in self.rectangles+[self.current]:
                pygame.draw.rect(window, rect[0], rect[1:])

            pygame.draw.rect(window, (255,255,255), self.current[1:], 1)

        else:
            z = -(len(self.rectangles)-10)*self.height if len(self.rectangles) > 10 else 0

            rects = self.rectangles+[self.current]

            for r in range(len(rects)):
                if r == len(rects)-2:
                    if self.perfects > 0:
                        diff = time.time()-self.last_perfect

                        if diff < self.perfect_duration+self.perfect_last:
                            rect = self.rectangles[-1]

                            margin = min(diff/self.perfect_duration,1) * 20

                            rect = [rect[0], rect[1]-margin,rect[2]-margin,rect[3]+2*margin,rect[4]+2*margin]
                            tl, tr, bl, br = [rect[1], rect[2]], [rect[1]+rect[3], rect[2]], [rect[1], rect[2]+rect[4]], [rect[1]+rect[3], rect[2]+rect[4]]

                            tl, tr, bl, br = [self.toIso(*point) for point in [tl,tr,bl,br]]
                            tl, tr, bl, br = [[p[0], p[1]-z+self.height] for p in [tl,tr,bl,br]]

                            surf = pygame.Surface([WIDTH, HEIGHT], pygame.SRCALPHA)

                            pygame.draw.polygon(surf, (255,255,255, 0.5*255), [tl,tr,br,bl])

                            window.blit(surf, [0,0])

                rect = rects[r]

                col = rect[0]
                tl, tr, bl, br = [rect[1], rect[2]], [rect[1]+rect[3], rect[2]], [rect[1], rect[2]+rect[4]], [rect[1]+rect[3], rect[2]+rect[4]]

                tl, tr, bl, br = [self.toIso(*point) for point in [tl,tr,bl,br]]
                tl, tr, bl, br = [[p[0], p[1]-z] for p in [tl,tr,bl,br]]

                tl2, tr2, bl2, br2 = [[p[0], p[1]+self.height] for p in [tl,tr,bl,br]]

                col2, col3 = pygame.Color(*col), pygame.Color(*col)
                hsva = list(col2.hsva)
                hsva[2] -= 10
                col2.hsva = hsva
                hsva[2] -= 10
                col3.hsva = hsva

                pygame.draw.polygon(window, col3, [bl, br, br2, bl2])
                pygame.draw.polygon(window, col2, [br, tr, tr2, br2])
                pygame.draw.polygon(window, col, [tl,tr,br,bl])

                """
                pygame.draw.aalines(window, (100,100,100), True, [tl,tr,br,bl],1)
                pygame.draw.aalines(window, (100,100,100), True, [bl, br, br2, bl2],1)
                pygame.draw.aalines(window, (100,100,100), True, [br, tr, tr2, br2],1)"""

                z += self.height

        text = self.font.render(str(self.score), True, (255,255,255))
        size = text.get_size()
        window.blit(text, [WIDTH/2-size[0]/2, HEIGHT/4-size[1]/2])

        #pygame.draw.line(window, (255,255,255), [WIDTH/2,0],[WIDTH/2,HEIGHT])
        #pygame.draw.line(window, (255,0,0), self.toIso(0,0), self.toIso(50,50))

        pygame.display.flip()

    def place(self):
        prev, cur = self.rectangles[-1][1:], self.current[1:]
        x1, y1, w1, h1 = prev
        x2, y2, w2, h2 = cur

        new_rect = None

        if abs(x2-x1) < self.margin and abs(y2-y1) < self.margin:
            new_rect = [self.current[0]]+self.rectangles[-1][1:]

            self.perfects += 1
            self.last_perfect = time.time()

        elif self.overlaps(prev, cur):
            x3, y3, x4, y4 = max(x1,x2), max(y1,y2), min(x1+w1,x2+w2), min(y1+h1,y2+h2)

            new_rect = [self.current[0], x3, y3, x4-x3, y4-y3]

            self.perfects = 0

        else:
            print(self.score)

            quit()
            #input()

        if not new_rect is None:
            if self.perfects >= self.perfects_in_row:
                if self.score % 2 == 0:
                    new_rect[3] += self.perfect_add

                else:
                    new_rect[4] += self.perfect_add

            self.rectangles.append(new_rect)
            self.score += 1

            self.gen_rect()

    def overlaps(self, r1, r2):
        tl1, br1, tl2, br2 = r1[:2], [r1[0]+r1[2],r1[1]+r1[3]], r2[:2], [r2[0]+r2[2],r2[1]+r2[3]]

        return not ( br2[0] < tl1[0] or br2[1] < tl1[1] or br1[0] < tl2[0] or br1[1] < tl2[1] )

    def gen_rect(self):
        prev = self.rectangles[-1]

        if self.score % 2 == 0:
            x, y = 0, prev[2]

        else:
            x, y = prev[1], 0

        self.current = [self.brighten(prev[0]), x, y, prev[3], prev[4]]


    def brighten(self, colour):
        #return [min(c+10, 240) for c in colour]

        col = pygame.Color(*colour)

        hsva = list(col.hsva)
        hsva[0] += 5
        hsva[0] %= 360

        col.hsva = hsva

        return [col.r,col.g,col.b]

        """
        colour = list(colour)

        for i in range(3):
            value = colour[i]

            c2 = (self.colour[i]+1)%len(self.colours)

            value += copysign(10, self.colours[c2][i]-value)

            if abs(self.colours[self.colour[i]][i]-value) < 10:
                self.colour[i] += 1
                self.colour[i] %= len(self.colours)

            colour[i] = value

        return colour"""

    def toIso(self, x, y):
        x2 = (x-y) * (1/2) + WIDTH/2
        y2 = (x+y) * (1/4) + HEIGHT/2

        return [x2, y2]

if __name__ == "__main__":
    pygame.init()

    w = pygame.display.set_mode([WIDTH, HEIGHT])

    clock = pygame.time.Clock()

    game = Game(True)

    while True:
        game.loop()
        game.display(w)

        clock.tick(60)
