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
        self.age=0
    def update(self,fps=60):
        self.age+=(1/fps)
        self.cooldown+=(1/fps)
        if(self.cooldown>=3):
            if len(self.apples)<3:
                self.give_apple()
                self.cooldown=0
            else:
                # make a new tree and die
                return self.new_tree()
        return self.age>60

    def new_tree(self):
        r = max(self.range * (random.random())**0.5,self.size*3)
        theta = random.uniform(0, 2*math.pi)
        new_pos = (int(self.pos[0] + r*math.cos(theta)), int(self.pos[1] + r*math.sin(theta)))
        self.cooldown=0
        return Tree(new_pos)
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
        