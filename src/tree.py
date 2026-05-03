import random
import pygame
import math

class Tree:
    def __init__(self,pos:tuple[int,int]):
        self.pos=pos
        self.colour=(100,200,100)
        self.apples:list[tuple[int,int]]=[]
        self.cooldown=0
        self.range=10
        self.size=10
    def update(self,fps=60):
        self.cooldown+=(1/fps)
        if(len(self.apples)<3 and self.cooldown>=3):
            self.give_apple()
            self.cooldown=0

    def give_apple(self):
        # dont spawn on itself so 
        r = max(self.range * (random.random())**0.5,self.size*2)
        theta = random.uniform(0, 2*math.pi)
        apple = (int(self.pos[0] + r*math.cos(theta)), int(self.pos[1] + r*math.sin(theta)))
        self.apples.append(apple)
    def draw(self,screen):
        pygame.draw.circle(screen,self.colour,self.pos,self.size)
        for apple in self.apples:
            pygame.draw.circle(screen,'red',apple,self.size**0.5)
        