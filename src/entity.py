from src import genome
import pygame
import math
import random
class Entity:
    def __init__(self,pos,colour,genom:genome.Genome):
        self.genome=genom
        self.pos=pos
        self.colour=colour
        # it will be in 2 state either wander or reproduce
        self.state=""
        self.destiny=(-1,-1)
        self.partner=None

    def get_state(self,others:list['Entity']):
        if(self.state):
            return 
        for other in others:
            if(self!=other):
                if(math.dist(self.pos,other.pos)<=self.genome.vision):
                    if(self.genome.can_reproduce(other.genome)):
                        self.destiny=other.pos
                        self.state='reproduce'
                        self.partner=other
                        return
        # pick a random point in range
        # finnaly a use to coordinate geomatry i learned
        self.state='wander'
        r = self.genome.vision * (random.random())**0.5
        theta = random.uniform(0, 2*math.pi)
        self.destiny = (int(self.pos[0] + r*math.cos(theta)), int(self.pos[1] + r*math.sin(theta)))
    def perform(self):
        match self.state:
            case 'reproduce':
                if(not self.partner):
                    raise ValueError('partner not defined')
                
                if(math.dist(self.pos,self.partner.pos)<5):
                    return Entity(self.pos,self.colour,self.genome.reproduce(self.partner.genome))
                else:
                    # partner went somewhere else so find a new one
                    self.state=""
                    self.destiny=(-1,-1)
                    self.partner=None
                    return None
            case 'wander':
                # reached the destiny update the state
                self.state=""
                self.destiny=(-1,-1)



        
    def update(self,others:list['Entity'],fps=60):
        self.get_state(others)
        dx, dy = self.destiny[0]-self.pos[0], self.destiny[1]-self.pos[1]
        dist = (dx*dx + dy*dy)**0.5
        if dist > 0:
            step = min(self.genome.speed, dist) #learning from my mistakes this avoids jitter
            self.pos = (self.pos[0] + dx/dist*step, self.pos[1] + dy/dist*step)
        self.genome.energy-=2*(1/fps)
        self.genome.age+=(1/fps)
        if(self.pos==self.destiny):
            return self.perform()
        
    def draw(self,Screen):
        pygame.draw.circle(Screen,self.colour,self.pos,self.genome.size)
