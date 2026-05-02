import pygame 
import random
pygame.init()



class Simulation:
    def __init__(self):
        self.entities=[]
        self.screen=pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.dimension=self.screen.get_size()
        self.clock=pygame.time.Clock()
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
        self.colour=((self.colour[0]+random.randint(-10,10))%256,(self.colour[1]+random.randint(-10,10))%256,(self.colour[2]+random.randint(-10,10))%256)
        for entity in self.entities:
            entity.update()#since i havent created it yet let entities be empty

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

        pygame.draw.circle(self.screen,"#041eb3",self.ballpos,50)
        for entity in self.entities:
            entity.draw()
        pygame.display.flip()
    def mainloop(self):
        running=True
        while running:
            running=self.update()
            self.draw()
            self.clock.tick(self.fps)