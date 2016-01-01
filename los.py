import pygame #fine
blue = (0, 0, 255)

#Can think of a LOS as a really thin rectangle that can extend the length or height of the screen
class LOS(pygame.sprite.Sprite):
    def __init__(self, eye_end = None, width = 0, height = 0, color = blue):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.eye_end = eye_end


    #set_position could basically establish where the "eye end" of the LOS is if we play around
    #with the left or right attributes of its rect
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
