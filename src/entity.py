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
        self.alive=True
        # reproduction cooldown
        self.cooldown=0

    def get_state(self, others: list['Entity']):
        if self.state == "reproduce":
            if not self.partner:
                self.state = ""
                return
            return

        if self.state == "wander":
            return
        if(self.cooldown>5):
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
         
        if not self.state:
            raise Exception("perform called without a state")
        
        if self.state=='wander':
            self.state=""
            return None

        # only here for reproduce state

        # no partner
        if  not self.partner :
            self.state = ""
            return None

        # partner too away
        if math.dist(self.pos, self.partner.pos) > (self.genome.size + self.partner.genome.size):
            self.state = ""
            self.partner = None
            return None
        
        if math.dist(self.pos, self.partner.pos) <= (self.genome.size + self.partner.genome.size):
            child = self.genome.reproduce(self.partner.genome)
            if child:
                self.cooldown=0
                
            # reset both entities cleanly
            self.state = ""
            # self.partner.state = ""
            # self.partner.partner = None   ->i willl not update the state from here 
            self.partner = None

            return Entity(self.pos, self.colour, child) if child else None

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
        self.cooldown+=(1/fps)
        self.pos=(min(max(self.pos[0],0),dims[0]),min(max(self.pos[1],0),dims[1]))
        if self.genome.energy<=0 or self.genome.age>=self.genome.max_age:
            self.alive=False
            return None
        if math.dist(self.pos, self.destiny) <= (self.genome.size ):
            return self.perform()

    def draw(self,Screen):
        pygame.draw.circle(Screen,self.colour,self.pos,self.genome.size)
