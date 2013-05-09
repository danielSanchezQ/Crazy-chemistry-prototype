#-------------------------------------------------------------------------------
# Name:        testballs.py
# Purpose:
#
# Author:      daniel.sanchez
#
# Created:     15/03/2013
# Copyright:   (c) daniel.sanchez 2013
#-------------------------------------------------------------------------------

import pygame, sys, math
from Vector3D import Vector3D
from pygame.locals import *
from pygame.color import THECOLORS
from pygame.time import Clock
from random import randint



colors = ["red", "green", "blue", "yellow"]


##b1 = pygame.image.load("BOTON1.jpg").convert()
##b2 = pygame.image.load("BOTON2.jpg").convert()
##b3 = pygame.image.load("BOTON3.jpg").convert()
##b4 = pygame.image.load("BOTON4.jpg").convert()


##images = {THECOLORS["red"]:b1, THECOLORS["green"]:b2, THECOLORS["blue"]:b3, THECOLORS["yellow"]:b4}



def randColor():
    return THECOLORS[colors[randint(0,len(colors)-1)]]


class Ball:
    def __init__(self, color = None, radious = 20):
        self.color = color
        self.radious = radious

    def bePainted(self, surface, pos):
         pygame.draw.circle(surface, self.color, pos, self.radious)
         #surface.blit(image[self.color], pos)



class SBall(pygame.sprite.Sprite):
    def __init__(self,name):
        self.image = pygame.image.load(name)
        self.rect = self.image.get_rect()
        pygame.sprite.Sprite.__init__(self)

    def update(self, pos):
        self.rect.center = self.pos

class Ring:
    def __init__(self, size, radious):
        self.size = size
        self.balls = self.initRing()
        self.radious = radious

    def initRing(self):
        tmplst = []
        for i in range(self.size):
            color = randColor()
            tmplst.append(Ball(color))
        return tmplst

    def isOk(self):
        return all(self.ring)

    def rshift(self):
        last = self.balls.pop(-1)
        self.balls.insert(0,last)

    def lshift(self):
        fst = self.balls.pop(0)
        self.balls.append(fst)

    def __lshift__(self, num):
        toshift = num%self.size
        for i in range(toshift):
            self.lshift()

    def __rshift__(self, num):
        toshift = num%self.size
        for i in range(toshift):
            self.rshift()

class RingManager:
    def __init__(self, width, height, center = (0,0), depth = 4, start = 2):
        self.total = pow(start,depth)
        self.depth = depth
        self.start = start
        self.screenSize = width, height
        self.screenAxpect = float(width)/float(height)
        self.center = Vector3D(self.screenSize[0]/2,self.screenSize[1]/2)
        self.rings = self.initRings()
        self.ballPositions = self.initPos()


    def getMidRad(self):
        if self.screenSize[0] < self.screenSize[1]:
            return (self.screenSize[0]/(self.depth+1))/2
        else:
            return (self.screenSize[1]/(self.depth+1))/2

    def initRings(self):
        tmplst = []
        midRad = self.getMidRad()
        for i in range(1,self.depth+1):
            tmplst.append(Ring(pow(self.start, i+1), i*midRad))
        return tmplst

    def initPos(self):
        tmplst = []
        for ring in self.rings:
            ringlst = []
            rad = ring.radious
            ang = 360.0/ring.size
            for i in range(ring.size):
                xVector = Vector3D(1)
                xVector.normalize()
                xVector.place2angle(ang*i)
                xVector *= rad
                xVector.x *= self.screenAxpect
                finalV = self.center + xVector
                ringlst.append(finalV)
            tmplst.append(ringlst)
        return tmplst

    def paintAll(self, surface):
##        if len(self.rings) != len(self.ballPositions):
##            raise ValueError("Not enough postions for balls")
        for ring in range(len(self.rings)):
            for ball in range(len(self.rings[ring].balls)):
                ring_obj = self.rings[ring]
                ball_obj = ring_obj.balls[ball]
                balpos = self.ballPositions[ring][ball]
                ball_obj.bePainted(surface, (int(balpos.x),int(balpos.y)))

    def checkCollide(self):
        for ring in self.rings:
            for ball in range(ring.size):
                if ring.balls[ball%ring.size].color == ring.balls[(ball+1)%ring.size].color == ring.balls[(ball+2)%ring.size].color:
                    ring.balls[ball].color = randColor()
                    ring.balls[(ball+1)%ring.size].color = randColor()
                    ring.balls[(ball+2)%ring.size].color = randColor()
        for ring in range(len(self.rings) - 1):
            for ball in range(self.rings[ring].size):
                self.checkTriangleColl(ring, ball)

    def checkTriangleColl(self,ring, ball):
        ballColor = self.rings[ring].balls[ball].color
        upperball1 = self.rings[ring+1].balls[ball*2-1].color
        upperball2 = self.rings[ring+1].balls[ball*2].color
        upperball3 = self.rings[ring+1].balls[ball*2+1].color
        if ballColor == upperball1 == upperball2 == upperball3:
            self.rings[ring].balls[ball].color = randColor()
            self.rings[ring+1].balls[ball*2-1].color = randColor()
            self.rings[ring+1].balls[ball*2].color = randColor()
            self.rings[ring+1].balls[ball*2+1].color = randColor()
        elif ballColor == upperball1 == upperball2:
            self.rings[ring].balls[ball].color = randColor()
            self.rings[ring+1].balls[ball*2-1].color = randColor()
            self.rings[ring+1].balls[ball*2].color = randColor()
        elif ballColor == upperball2 == upperball3:
            self.rings[ring].balls[ball].color = randColor()
            self.rings[ring+1].balls[ball*2].color = randColor()
            self.rings[ring+1].balls[ball*2+1].color = randColor()
def main():
    pygame.init()

    size = width, height = 1280, 720
    speed = [2,2]
    black = 0, 0, 0
    pos = posx, posy = width/2, height/2
    radius = 20
    color = THECOLORS["red"]
    clock = Clock()
    screen = pygame.display.set_mode(size)
    surface = pygame.display.get_surface()
    rmanager = RingManager( width, height, center = pos)
    r = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            elif event.type == KEYDOWN:
                if pygame.key.get_pressed()[K_1]:
                    r = 0
                if pygame.key.get_pressed()[K_2]:
                    r = 1
                if pygame.key.get_pressed()[K_3]:
                    r = 2
                if pygame.key.get_pressed()[K_4]:
                    r = 3
                if pygame.key.get_pressed()[K_LEFT]:
                    rmanager.rings[r] << 1
                elif pygame.key.get_pressed()[K_RIGHT]:
                    rmanager.rings[r] >> 1
        rmanager.checkCollide()
        rmanager.paintAll(surface)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
