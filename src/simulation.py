import math

import pygame 
import random
from src import entity,genome,tree
pygame.init()



class Simulation:
    def __init__(self):
        self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.dimension=self.screen.get_size()
        self.clock=pygame.time.Clock()
        self.entities=[entity.Entity((random.randint(0,self.dimension[0]),random.randint(0,self.dimension[1])),(200,150,100),genome.Genome('lions',random.randint(3,7),random.randint(50,100),random.randint(50,100),6)) for i in range(10)]
        self.trees=[tree.Tree((random.randint(0,self.dimension[0]),random.randint(0,self.dimension[1]))) for i in range(100)]
        self.colour=(100,100,100)
        self.fps=60
        # test variable for now
        self.ballpos=[100,100]
    def update(self):
        events=self.listen_events()
        if(events[1]):
            self.ballpos[1]-=5
        if(events[3]):
            self.ballpos[1]+=5
        if(events[2]):
            self.ballpos[0]-=5
        if(events[4]):
            self.ballpos[0]+=5

        data={'running':1,'avg_speed':0,'avg_size':0,'avg_energy':0,'avg_age':0,'avg_vision':0,'trees':0,'entities':0,'avg_apples':0}
        for entit in self.entities[:]:
            kid=entit.update(self.entities,self.trees,self.fps,self.dimension)#since i havent created it yet let entities be empty
            data['avg_speed']+=entit.genome.speed
            data['avg_size']+=entit.genome.size
            data['avg_energy']+=entit.genome.energy
            data['avg_age']+=entit.genome.age
            data['avg_vision']+=entit.genome.vision

            if(isinstance(kid,entity.Entity)):
                self.entities.append(kid)
            if(not entit.alive):
                self.entities.remove(entit)
        for tre in self.trees:
            output=tre.update(self.dimension,self.fps)
            data['trees']+=1
            data['avg_apples']+=len(tre.apples)
            if(isinstance(output,tree.Tree)):
                self.trees.append(output)
            elif output:
                self.trees.remove(tre)
        entities_count=max(1,len(self.entities))
        data['entities']=entities_count
        data['avg_speed']/=entities_count
        data['avg_size']/=entities_count
        data['avg_energy']/=entities_count
        data['avg_age']/=entities_count
        data['avg_vision']/=entities_count
        data['avg_apples']/=max(1,data['trees'])
        data['running']=events[0] 
        return data
    def listen_events(self):
        running = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        return [ running, keys[pygame.K_UP], keys[pygame.K_LEFT], keys[pygame.K_DOWN], keys[pygame.K_RIGHT]]
    def draw(self):
        self.screen.fill(self.colour)
        for entity in self.entities:
            kid=entity.draw(self.screen)
            if(kid):
                self.entities.append(kid)
        for tree in self.trees:
            tree.draw(self.screen)
        
        self.screen.blit(pygame.font.SysFont(None, 36).render(f"entities:{len(self.entities)}", True, (255, 200, 200)),(50,50))
        self.screen.blit(pygame.font.SysFont(None, 36).render(f"fps:{self.clock.get_fps():.1f}", True, (255, 200, 200)),(50,80))
        
        pygame.display.flip()
    def mainloop(self):
        data=[]
        running=True
        while running:
            d=self.update()
            running=d['running']
            data.append(d)
            self.draw()
            self.clock.tick(self.fps)
        return data