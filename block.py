import pygame #fine
from colors import * #fine

class Block(pygame.sprite.Sprite):
    def __init__(self, color = BLUE, width = 64, height = 64, filename = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        if filename != None:
            image = pygame.image.load(filename)
            scaled_image = pygame.transform.scale(image, (int(width), int(height)))
            self.image.blit(scaled_image, (0,0))
        else:
            self.image.fill(color)
        '''
        self.image.fill(color)
        #Note that self.image is now a Surface object. We can blit images onto
        #Surface objects with pygame.Surface.blit(). This blit() function takes
        #the Surface object that you want to blit on, which would be self.image
        #in this case.
        '''

        '''
        #How you could possibly set an image to a Block
        temp = pygame.image.load("east0.png").convert()
        #Note that "east0.png" is a transparent image!
        pic = pygame.transform.scale(temp, (int(width), int(height)))
        self.image.blit(pic, (0,0))
        '''

        #self._set_attributes()

        self.rect = self.image.get_rect()
        self.origin_x = self.rect.centerx #Didn't use this for the line of sight
        self.origin_y = self.rect.centery #Didn't use this for the line of sight


    def init_position(self, x, y):
        #self.rect.x = x - self.origin_x
        #self.rect.y = y - self.origin_y
        self.rect.x = x
        self.rect.y = y

    
    def set_image(self, filename = None):
        if filename != None:
            self.image = pygame.image.load(filename)
            self._set_attributes()

    def _set_attributes(self):  #For updating the rect and origin
        self.rect = self.image.get_rect()
        self.origin_x = self.rect.centerx #Didn't use this for the line of sight
        self.origin_y = self.rect.centery #Didn't use this for the line of sight
