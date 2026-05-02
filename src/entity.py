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

    def get_state(self, others: list['Entity']):
        if self.state == "reproduce":
            if not self.partner:
                self.state = ""
                return
            return

        if self.state == "wander":
            return

        for other in others:
            if(self!=other):
                if(math.dist(self.pos,other.pos)<=self.genome.vision):
                    if(self.genome.can_reproduce(other.genome) and other.partner is None):
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
        if self.state != "reproduce":
            return None

        if not self.partner:
            self.state = ""
            return None

        # partner drifted away → abort task
        if math.dist(self.pos, self.partner.pos) > (self.genome.size + self.partner.genome.size):
            self.state = ""
            self.partner.state = ""
            self.partner.partner = None
            self.partner = None
            return None

        # success condition → reproduce
        if math.dist(self.pos, self.partner.pos) <= (self.genome.size + self.partner.genome.size):
            child = self.genome.reproduce(self.partner.genome)

            # reset both entities cleanly
            self.state = ""
            self.partner.state = ""
            self.partner.partner = None
            self.partner = None

            return Entity(self.pos, self.colour, child)

        return None


        
    def update(self,others:list['Entity'],fps=60,dims=(1200,756)):
        self.get_state(others)
        self.destiny=(min(max(self.destiny[0],0),dims[0]),min(max(self.destiny[1],0),dims[1]))
        dx, dy = self.destiny[0]-self.pos[0], self.destiny[1]-self.pos[1]
        dist = (dx*dx + dy*dy)**0.5
        if dist > 0:
            step = min(self.genome.speed, dist) #learning from my mistakes this avoids jitter
            self.pos = (self.pos[0] + dx/dist*step, self.pos[1] + dy/dist*step)
        self.genome.energy-=2*(1/fps)
        self.genome.age+=(1/fps)
        self.pos=(min(max(self.pos[0],0),dims[0]),min(max(self.pos[1],0),dims[1]))
        if self.partner and math.dist(self.pos, self.partner.pos) <= (self.genome.size + self.partner.genome.size):
            return self.perform()
            
    def draw(self,Screen):
        pygame.draw.circle(Screen,self.colour,self.pos,self.genome.size)
