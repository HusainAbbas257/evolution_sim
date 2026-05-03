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
        self.entities=[entity.Entity((random.randint(0,self.dimension[0]),random.randint(0,self.dimension[1])),(200,150,100),genome.Genome('lions',1,random.uniform(25,50),random.uniform(50,150),random.uniform(5,7))) for i in range(100)]
        self.trees=[tree.Tree((random.randint(0,self.dimension[0]),random.randint(0,self.dimension[1]))) for i in range(25)]
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
        for entit in self.entities[:]:
            kid=entit.update(self.entities,self.trees,self.fps,self.dimension)#since i havent created it yet let entities be empty
            if(isinstance(kid,entity.Entity)):
                self.entities.append(kid)
            if(not entit.alive):
                self.entities.remove(entit)
        for tree in self.trees:
            tree.update()

        return events[0]
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
        pygame.display.flip()
    def mainloop(self):
        running=True
        while running:
            running=self.update()
            self.draw()
            self.clock.tick(self.fps)