import pygame #fine

class Exclamation(pygame.sprite.Sprite):
    '''A class the represents the exclamation point that shows up when
       a mercenary spots you.'''
    
    def __init__(self, eye_end = None):
        '''Initializes the attributes of an Exclamation.'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("!.png")
        self.rect = self.image.get_rect()
        self.lifespan = 9
        self.ticks = 0

    def set_position(self, x, y):
        '''Sets the position of an Exclamation.'''
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        '''Updates an Exclamation.'''
        self.ticks += 1
