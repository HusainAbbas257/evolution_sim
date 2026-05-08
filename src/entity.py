from src import genome
import pygame
import math
import random
from src.tree import Tree

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
        self.target_tree=None

        # basic memory to remember where the tlast tree was
        self.last_tree_pos=None

    def get_state(self, others: list['Entity'],tree_list:list['Tree']):
        #priority --> eat>reproduce>wander
        
        if self.state == "reproduce":
            if not self.partner:
                self.state = ""
                return
            return

        if self.state == "wander" or self.state == "eat":
            return
        
        # do or die case :
        if self.genome.energy<=5:
            # dont check distance just rush to nearest tree
                nearest_tree=None
                nearest_dist=float('inf')
                for tree in tree_list:
                    dist=math.dist(self.pos, tree.pos)
                    if dist<nearest_dist and len(tree.apples)>0:
                        nearest_tree=tree
                        nearest_dist=dist
                if nearest_tree:
                    self.destiny=nearest_tree.apples[0]
                    self.state='eat'
                    self.target_tree=nearest_tree
                    self.last_tree_pos=nearest_tree.pos
                    return
                
        if self.genome.energy<75:
            for tree in tree_list:
                if math.dist(self.pos, tree.pos) <= self.genome.vision and len(tree.apples)>0 :
                    self.destiny =tree.apples[0]
                    self.state = "eat"
                    self.target_tree = tree
                    self.last_tree_pos=tree.pos
                    return
            # now go  back to the last tree if there is none near
            if self.last_tree_pos:
                self.destiny=self.last_tree_pos
                self.state='eat'
                return

        if(self.cooldown>2.5):
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

        if self.state=='eat': 
            if not self.target_tree:
                self.state=""
                return None
            if(math.dist(self.pos, self.destiny) <= self.genome.size+self.target_tree.size and self.destiny in self.target_tree.apples):
                self.genome.energy+=30
                self.state=""
                self.target_tree.apples.pop(self.target_tree.apples.index(self.destiny))
                self.target_tree=None
                return 

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


        
    def update(self,others:list['Entity'],tree_list:list['Tree'],fps=60,dims=(1200,756)):
        self.get_state(others, tree_list)
        self.destiny=(min(max(self.destiny[0],0),dims[0]),min(max(self.destiny[1],0),dims[1]))
        dx, dy = self.destiny[0]-self.pos[0], self.destiny[1]-self.pos[1]
        dist = (dx*dx + dy*dy)**0.5
        if dist > 0:
            step = min(self.genome.speed, dist) #learning from my mistakes this avoids jitter
            self.pos = (self.pos[0] + dx/dist*step, self.pos[1] + dy/dist*step)
        self.genome.energy-=self.genome.size*(1/fps)  #obese ones get tired faster
        self.genome.age+=(1/fps)
        self.cooldown+=(1/fps)
        if self.last_tree_pos:
            self.last_tree_pos=(self.last_tree_pos[0]+random.randint(-5,5),self.last_tree_pos[1]+random.randint(-5,5))
        original=self.pos
        if(self.pos[0]<0 or self.pos[0]>dims[0] or self.pos[1]<0 or self.pos[1]>dims[1]):
            self.pos=(min(max(self.pos[0],0),dims[0]),min(max(self.pos[1],0),dims[1]))
        
        if(self.pos!=original):
            return self.update(others,tree_list,fps,dims)
        
        if self.genome.energy<=0 or self.genome.age>=self.genome.max_age:
            self.alive=False
            return None
        if math.dist(self.pos, self.destiny) <= (self.genome.size ):
            return self.perform()

    def draw(self,Screen):
        pygame.draw.circle(Screen,self.colour,self.pos,self.genome.size)
