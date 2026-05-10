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
        self.max_age=random.randint(30,75)
        self.max_apples=random.randint(1,7)
        self.max_cd=random.randint(1,10)
    def update(self,dims,fps):
        self.age+=(1/fps)
        self.cooldown+=(1/fps)
        if(self.cooldown>=self.max_cd):
            if len(self.apples)<self.max_apples:
                self.give_apple()
                self.age+=1
                self.cooldown=0
            else:
                if(self.cooldown>2*self.max_cd):
                    self.cooldown=0
                    # make a new tree
                    self.age+=10
                    return self.new_tree(dims)
        return self.age>=self.max_age

    def new_tree(self,dims=[1200,720]):
        r = max(self.range * (random.random())**0.5,self.size*5)
        theta = random.uniform(0, 2*math.pi)
        new_pos = (int(self.pos[0] + r*math.cos(theta)), int(self.pos[1] + r*math.sin(theta)))
        while new_pos[0]<0 or new_pos[0]>dims[0] or new_pos[1]<0 or new_pos[1]>dims[1]:
            r = max(self.range * (random.random())**0.5,self.size*5)
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
        