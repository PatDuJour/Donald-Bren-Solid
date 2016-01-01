import pygame #fine

STRAW_STOCK = 200
RUBBER_BAND_STOCK = 150
BANANA_PEEL_STOCK = 50
WATER_BALLOON_STOCK = 25
INSTANT_NOODLES_STOCK = 2

class Collectible(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class MGS5(Collectible):
    '''A class that represents the MGS5 game, which Snake can pick up for extra points.'''

    def __init__(self):
        Collectible.__init__(self)
        self.image = pygame.image.load("mgs5.png")
        self.rect = self.image.get_rect()


class MGS4(Collectible):
    '''A class that represents the MGS4 game, which Snake can pick up for extra points.'''

    def __init__(self):
        Collectible.__init__(self)
        self.image = pygame.image.load("mgs4.png")
        self.rect = self.image.get_rect()


class MGS3(Collectible):
    '''A class that represents the MGS3 game, which Snake can pick up for extra points.'''

    def __init__(self):
        Collectible.__init__(self)
        self.image = pygame.image.load("mgs3.png")
        self.rect = self.image.get_rect()


class MGS2(Collectible):
    '''A class that represents the MGS2 game, which Snake can pick up for extra points.'''

    def __init__(self):
        Collectible.__init__(self)
        self.image = pygame.image.load("mgs2.png")
        self.rect = self.image.get_rect()


class MGS1(Collectible):
    '''A class that represents the MGS1 game, which Snake can pick up for extra points.'''

    def __init__(self):
        Collectible.__init__(self)
        self.image = pygame.image.load("mgs1.png")
        self.rect = self.image.get_rect()


class Unequipped():
    '''A class to represent Snake's state of being unequipped for both
       weapons and items.'''
    def __init__(self):
        self.name = "None"
        self.stock = ""
        

class WaterBalloonPickUp(Collectible):
    '''A class to represent water balloons that Snake can use as a weapon.'''

    def __init__(self):
        Collectible.__init__(self)
        self.image = pygame.image.load("balloon-top.png")
        self.rect = self.image.get_rect()
        self.name = "Water Balloon"
        self.stock = WATER_BALLOON_STOCK


class BananaPeelPickUp(Collectible):
    '''A class to represent banana peels that Snake can use as a weapon.'''

    def __init__(self):
        Collectible.__init__(self)
        self.image = pygame.image.load("bananas_unpeeled.png")
        self.rect = self.image.get_rect()
        self.name = "Banana Peel"
        self.stock = BANANA_PEEL_STOCK


class RubberBandPickUp(Collectible):
    '''A class to represent rubber bands that Snake can use as a weapon.'''

    def __init__(self):
        Collectible.__init__(self)
        self.image = pygame.image.load("rubber_band.png")
        self.rect = self.image.get_rect()
        self.name = "Rubber Band"
        self.stock = RUBBER_BAND_STOCK


class StrawPickUp(Collectible):
    '''A class to represent straws that Snake can use as a weapon.'''

    def __init__(self):
        Collectible.__init__(self)
        self.image = pygame.image.load("straw.png")
        self.rect = self.image.get_rect()
        self.name = "Straw"
        self.stock = STRAW_STOCK


class InstantNoodlesPickUp(Collectible):
    '''A class to represent instant noodles that snake can use as in item to recover health.'''

    def __init__(self):
        Collectible.__init__(self)
        self.image = pygame.image.load("instant_noodles.png")
        self.rect = self.image.get_rect()
        self.name = "Instant Noodles"
        self.stock = INSTANT_NOODLES_STOCK


class GoogleJobOffer(Collectible): #Note how this won't show up in your inventory. It only increases your life by 1.
    '''A class to represent a Google job offer that serves as a one-up.'''
    def __init__(self):
        Collectible.__init__(self)
        self.image = pygame.image.load("google.png")
        self.rect = self.image.get_rect()
        

class CS113DataDisc(Collectible):
    '''A class to represent Snake's CS113 data disc.'''
    def __init__(self):
        Collectible.__init__(self)
        self.name = "CS 113 Data Disc"
        self.stock = 1


class CardKey(pygame.sprite.Sprite):
    '''A base class for the card keys in the game.'''
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("card_key.png")
        self.rect = self.image.get_rect()
        self.stock = ""

    def init_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


class Floor2CardKey(CardKey):
    '''A class that represent the card key for floor 2.'''
    
    def __init__(self):
        CardKey.__init__(self)
        self.name = "Floor 2 Card Key"



class Floor3CardKey(CardKey):
    '''A class that represent the card key for floor 3.'''
    
    def __init__(self):
        CardKey.__init__(self)
        self.name = "Floor 3 Card Key"



class Floor4CardKey(CardKey):
    '''A class that represent the card key for floor 4.'''
    
    def __init__(self):
        CardKey.__init__(self)
        self.name = "Floor 4 Card Key"



class Floor5CardKey(CardKey):
    '''A class that represent the card key for floor 5.'''
    
    def __init__(self):
        CardKey.__init__(self)
        self.name = "Floor 5 Card Key"


class ElevatorCardKey(CardKey):
    '''A class that represent the card key for the elevator.'''
    
    def __init__(self):
        CardKey.__init__(self)
        self.name = "Elevator Card Key"




