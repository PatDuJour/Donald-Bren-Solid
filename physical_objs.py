import pygame #fine
from colors import *

class TrashCan(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("trash can.png")
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Bed(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bed.png")
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class WaterFountain(pygame.sprite.Sprite):

    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        
        if orientation == "north":
            self.image = pygame.image.load("water_fountain_north.png")
        elif orientation == "west":
            self.image = pygame.image.load("water_fountain_west.png")
        elif orientation == "south":
            self.image = pygame.image.load("water_fountain_south.png")
        elif orientation == "east":
            self.image = pygame.image.load("water_fountain_east.png")
            
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Toilet(pygame.sprite.Sprite):
    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        if orientation == "south":
            self.image = pygame.image.load("toilet_south.png")
        elif orientation == "north":
            self.image = pygame.image.load("toilet_north.png")

        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class BlueSofa(pygame.sprite.Sprite):

    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        
        if orientation == "north":
            self.image = pygame.image.load("blue_sofa_north.png")
        elif orientation == "west":
            self.image = pygame.image.load("blue_sofa_west.png")
        elif orientation == "south":
            self.image = pygame.image.load("blue_sofa_south.png")
        elif orientation == "east":
            self.image = pygame.image.load("blue_sofa_east.png")
            
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class RedSofa(pygame.sprite.Sprite):

    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        
        if orientation == "north":
            self.image = pygame.image.load("red_sofa_north.png")
        elif orientation == "west":
            self.image = pygame.image.load("red_sofa_west.png")
        elif orientation == "south":
            self.image = pygame.image.load("red_sofa_south.png")
        elif orientation == "east":
            self.image = pygame.image.load("red_sofa_east.png")
            
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

class EndTable(pygame.sprite.Sprite):

    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        
        if orientation == "north":
            self.image = pygame.image.load("end_table_north.png")
        elif orientation == "west":
            self.image = pygame.image.load("end_table_west.png")
        elif orientation == "south":
            self.image = pygame.image.load("end_table_south.png")
        elif orientation == "east":
            self.image = pygame.image.load("end_table_east.png")
            
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class PinkCounter(pygame.sprite.Sprite):

    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        
        if orientation == "north":
            self.image = pygame.image.load("pink_counter_north.png")
        elif orientation == "west":
            self.image = pygame.image.load("pink_counter_west.png")
        elif orientation == "south":
            self.image = pygame.image.load("pink_counter_south.png")
        elif orientation == "east":
            self.image = pygame.image.load("pink_counter_east.png")
            
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class BookCounter(pygame.sprite.Sprite):
    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        if orientation == "south":
            self.image = pygame.image.load("book_counter_south.png")
        elif orientation == "north":
            self.image = pygame.image.load("book_counter_north.png")
        elif orientation == "east":
            self.image = pygame.image.load("book_counter_east.png")
        elif orientation == "west":
            self.image = pygame.image.load("book_counter_west.png")

        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class WoodenCounter(pygame.sprite.Sprite):
    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        if orientation == "south":
            self.image = pygame.image.load("wooden_counter_south.png")
        elif orientation == "north":
            self.image = pygame.image.load("wooden_counter_north.png")
        elif orientation == "east":
            self.image = pygame.image.load("wooden_counter_east.png")
        elif orientation == "west":
            self.image = pygame.image.load("wooden_counter_west.png")

        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class RedSofaChair(pygame.sprite.Sprite):

    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        if orientation == "north":
            self.image = pygame.image.load("red_sofa_chair_north.png")
        elif orientation == "west":
            self.image = pygame.image.load("red_sofa_chair_west.png")
        elif orientation == "south":
            self.image = pygame.image.load("red_sofa_chair_south.png")
        elif orientation == "east":
            self.image = pygame.image.load("red_sofa_chair_east.png")
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class RoundedEdgeTable(pygame.sprite.Sprite):

    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        if orientation == "horizontal":
            self.image = pygame.image.load("rounded_edge_table_horizontal.png")
        elif orientation == "vertical":
            self.image = pygame.image.load("rounded_edge_table_vertical.png")

        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class BathroomCounter(pygame.sprite.Sprite):
    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        if orientation == "south":
            self.image = pygame.image.load("bathroom_counter_south.png")
        elif orientation == "north":
            self.image = pygame.image.load("bathroom_counter_north.png")

        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

class RoundSeat(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("round_seat.png")
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

class GreenChair(pygame.sprite.Sprite):

    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        if orientation == "north":
            self.image = pygame.image.load("green_chair_north.png")
        elif orientation == "west":
            self.image = pygame.image.load("green_chair_west.png")
        elif orientation == "south":
            self.image = pygame.image.load("green_chair_south.png")
        elif orientation == "east":
            self.image = pygame.image.load("green_chair_east.png")
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        


class GreenSofa(pygame.sprite.Sprite):

    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        
        if orientation == "north":
            self.image = pygame.image.load("green_sofa_north.png")
        elif orientation == "west":
            self.image = pygame.image.load("green_sofa_west.png")
        elif orientation == "south":
            self.image = pygame.image.load("green_sofa_south.png")
        elif orientation == "east":
            self.image = pygame.image.load("green_sofa_east.png")
            
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class GreenSofaChair(pygame.sprite.Sprite):

    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        if orientation == "north":
            self.image = pygame.image.load("green_sofa_chair_north.png")
        elif orientation == "west":
            self.image = pygame.image.load("green_sofa_chair_west.png")
        elif orientation == "south":
            self.image = pygame.image.load("green_sofa_chair_south.png")
        elif orientation == "east":
            self.image = pygame.image.load("green_sofa_chair_east.png")
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class BlueSofaChair(pygame.sprite.Sprite):

    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        if orientation == "north":
            self.image = pygame.image.load("blue_sofa_chair_north.png")
        elif orientation == "west":
            self.image = pygame.image.load("blue_sofa_chair_west.png")
        elif orientation == "south":
            self.image = pygame.image.load("blue_sofa_chair_south.png")
        elif orientation == "east":
            self.image = pygame.image.load("blue_sofa_chair_east.png")
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        

class SmallSquareTable(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("small_square_table.png")
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

class SmallLongTable(pygame.sprite.Sprite):

    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        if orientation == "vertical":
            self.image = pygame.image.load("small_long_table_vertical.png")
        elif orientation == "horizontal":
            self.image = pygame.image.load("small_long_table_horizontal.png")

        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class BlueChair(pygame.sprite.Sprite):

    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        if orientation == "north":
            self.image = pygame.image.load("blue_chair_north.png")
        elif orientation == "west":
            self.image = pygame.image.load("blue_chair_west.png")
        elif orientation == "south":
            self.image = pygame.image.load("blue_chair_south.png")
        elif orientation == "east":
            self.image = pygame.image.load("blue_chair_east.png")
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class BrownSofaChair(pygame.sprite.Sprite):

    def __init__(self, orientation):
        pygame.sprite.Sprite.__init__(self)
        if orientation == "north":
            self.image = pygame.image.load("brown_sofa_chair_north.png")
        elif orientation == "west":
            self.image = pygame.image.load("brown_sofa_chair_west.png")
        elif orientation == "south":
            self.image = pygame.image.load("brown_sofa_chair_south.png")
        elif orientation == "east":
            self.image = pygame.image.load("brown_sofa_chair_east.png")
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

class Copier(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("copier.png")
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class FrostDesk(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("frost_desk.png")
        self.rect = self.image.get_rect()

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
