from colors import * #fine
import pygame #fine
import random #fine

P_SPEED = 50
HEART_SPEED = 25
OTHELLO_SPEED = 65
READINGS_SPEED = 25
SB_SPEED = 40
RB_SPEED = 60


##class Projectile(pygame.sprite.Sprite):
##    '''A class that represents a projectile.'''
##    def __init__(self, orientation=None, width=10, height=10):
##        pygame.sprite.Sprite(self)


class FrostSpark(pygame.sprite.Sprite):
    '''This class represents a Frost spark.'''
    def __init__(self, orientation = None, width = 10, height = 10):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
 
        #self.image = pygame.Surface((width, height)) #was (4, 10)
        #self.image.fill(WHITE)
        self.image = pygame.image.load("frost.png") 
        self.rect = self.image.get_rect()

        self.orientation = orientation
 
    def update(self):
        '''Moves the projectile.'''
        if self.orientation == "north":
            self.rect.y -= P_SPEED
        elif self.orientation == "northeast":
            self.rect.y -= P_SPEED
            self.rect.x += P_SPEED
        elif self.orientation == "east":
            self.rect.x += P_SPEED
        elif self.orientation == "southeast":
            self.rect.x += P_SPEED
            self.rect.y += P_SPEED
        elif self.orientation == "south":
            self.rect.y += P_SPEED
        elif self.orientation == "southwest":
            self.rect.y += P_SPEED
            self.rect.x -= P_SPEED
        elif self.orientation == "west":
            self.rect.x -= P_SPEED
        elif self.orientation == "northwest":
            self.rect.y -= P_SPEED
            self.rect.x -= P_SPEED


class Heart(pygame.sprite.Sprite):
    '''This class represents a heart.'''
    def __init__(self, orientation = None, width = 10, height = 10):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
 
        #self.image = pygame.Surface((width, height)) #was (4, 10)
        #self.image.fill(WHITE)
        self.image = pygame.image.load("heart.png") 
        self.rect = self.image.get_rect()

        self.orientation = orientation
 
    def update(self):
        '''Moves the projectile.'''
        if self.orientation == "north":
            self.rect.y -= HEART_SPEED
        elif self.orientation == "northeast":
            self.rect.y -= HEART_SPEED
            self.rect.x += HEART_SPEED
        elif self.orientation == "east":
            self.rect.x += HEART_SPEED
        elif self.orientation == "southeast":
            self.rect.x += HEART_SPEED
            self.rect.y += HEART_SPEED
        elif self.orientation == "south":
            self.rect.y += HEART_SPEED
        elif self.orientation == "southwest":
            self.rect.y += HEART_SPEED
            self.rect.x -= HEART_SPEED
        elif self.orientation == "west":
            self.rect.x -= HEART_SPEED
        elif self.orientation == "northwest":
            self.rect.y -= HEART_SPEED
            self.rect.x -= HEART_SPEED


class Readings(pygame.sprite.Sprite):
    '''This class represents a piece of reading material.'''
    def __init__(self, orientation = None, width = 10, height = 10):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
 
        #self.image = pygame.Surface((width, height)) #was (4, 10)
        #self.image.fill(WHITE)
        self.image = pygame.image.load("reading.png") 
        self.rect = self.image.get_rect()

        self.orientation = orientation

        self.tick_lim = random.randint(3, 9) #originally 3 to 8
        self.ticks = 0
        self.in_air = True
 
    def update(self):
        '''Moves the projectile.'''

        if self.orientation == "north" and self.ticks < self.tick_lim:
            self.rect.y -= READINGS_SPEED
        elif self.orientation == "northeast" and self.ticks < self.tick_lim:
            self.rect.y -= READINGS_SPEED
            self.rect.x += READINGS_SPEED
        elif self.orientation == "east" and self.ticks < self.tick_lim:
            self.rect.x += READINGS_SPEED
        elif self.orientation == "southeast" and self.ticks < self.tick_lim:
            self.rect.x += READINGS_SPEED
            self.rect.y += READINGS_SPEED
        elif self.orientation == "south" and self.ticks < self.tick_lim:
            self.rect.y += READINGS_SPEED
        elif self.orientation == "southwest" and self.ticks < self.tick_lim:
            self.rect.y += READINGS_SPEED
            self.rect.x -= READINGS_SPEED
        elif self.orientation == "west" and self.ticks < self.tick_lim:
            self.rect.x -= READINGS_SPEED
        elif self.orientation == "northwest" and self.ticks < self.tick_lim:
            self.rect.y -= READINGS_SPEED
            self.rect.x -= READINGS_SPEED
        elif self.ticks == self.tick_lim:
            self.in_air = False
            
        self.ticks += 1


class OthelloTile(pygame.sprite.Sprite):
    '''This class represents an othello tile.'''
    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("othello_black.png") if color=="black" else\
                     pygame.image.load("othello_white.png")
        self.rect = self.image.get_rect()

 
    def update(self):
        '''Moves the projectile.'''
        self.rect.y += OTHELLO_SPEED


class StunBullet(pygame.sprite.Sprite):
    '''This class represents a stun bullet.'''
    def __init__(self, orientation = None, width = 10, height = 10):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
 
        #self.image = pygame.Surface((width, height)) #was (4, 10)
        #self.image.fill(WHITE)
        self.image = pygame.image.load("spark.png") 
        self.rect = self.image.get_rect()

        self.orientation = orientation
 
    def update(self):
        '''Moves the StunBullet.'''
        if self.orientation == "north":
            self.rect.y -= P_SPEED
        elif self.orientation == "northeast":
            self.rect.y -= P_SPEED
            self.rect.x += P_SPEED
        elif self.orientation == "east":
            self.rect.x += P_SPEED
        elif self.orientation == "southeast":
            self.rect.x += P_SPEED
            self.rect.y += P_SPEED
        elif self.orientation == "south":
            self.rect.y += P_SPEED
        elif self.orientation == "southwest":
            self.rect.y += P_SPEED
            self.rect.x -= P_SPEED
        elif self.orientation == "west":
            self.rect.x -= P_SPEED
        elif self.orientation == "northwest":
            self.rect.y -= P_SPEED
            self.rect.x -= P_SPEED



class SpitBall(StunBullet):
    '''This class represents a spit ball.'''
    def __init__(self, orientation = None, width = 10, height = 10):
        StunBullet.__init__(self)
        self.image = pygame.Surface((width, height)) #was (4, 10)
        self.image.fill(WHITE)

    def update(self):
        '''Moves the projectile.'''
        if self.orientation == "north":
            self.rect.y -= SB_SPEED
        elif self.orientation == "northeast":
            self.rect.y -= SB_SPEED
            self.rect.x += SB_SPEED
        elif self.orientation == "east":
            self.rect.x += SB_SPEED
        elif self.orientation == "southeast":
            self.rect.x += SB_SPEED
            self.rect.y += SB_SPEED
        elif self.orientation == "south":
            self.rect.y += SB_SPEED
        elif self.orientation == "southwest":
            self.rect.y += SB_SPEED
            self.rect.x -= SB_SPEED
        elif self.orientation == "west":
            self.rect.x -= SB_SPEED
        elif self.orientation == "northwest":
            self.rect.y -= SB_SPEED
            self.rect.x -= SB_SPEED


class BananaPeel(pygame.sprite.Sprite):
    '''This class reprsents a banana peel'''
    def __init__(self, orientation = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("banana_peel.png")
        self.rect = self.image.get_rect()
        self.orientation = orientation


class RubberBand(StunBullet):
    '''This class represents a rubber band.'''
    def __init__(self, orientation = None, width = 10, height = 10):
        StunBullet.__init__(self)
        self.image = pygame.image.load("rubber_band.png")
        self.rect = self.image.get_rect()
        self.orientaiton = orientation

    def update(self):
        '''Moves the projectile.'''
        if self.orientation == "north":
            self.rect.y -= RB_SPEED
        elif self.orientation == "northeast":
            self.rect.y -= RB_SPEED
            self.rect.x += RB_SPEED
        elif self.orientation == "east":
            self.rect.x += RB_SPEED
        elif self.orientation == "southeast":
            self.rect.x += RB_SPEED
            self.rect.y += RB_SPEED
        elif self.orientation == "south":
            self.rect.y += RB_SPEED
        elif self.orientation == "southwest":
            self.rect.y += RB_SPEED
            self.rect.x -= RB_SPEED
        elif self.orientation == "west":
            self.rect.x -= RB_SPEED
        elif self.orientation == "northwest":
            self.rect.y -= RB_SPEED
            self.rect.x -= RB_SPEED
        


class WaterBalloon(pygame.sprite.Sprite):
    def __init__(self, orientation = None, width = 20, height = 20):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
 
        #self.image = pygame.Surface((width, height)) #was (4, 10)
        #self.image.fill(WHITE)

        self.image = pygame.image.load("balloon-top.png") #looks weird if I say .convert()... 
        self.rect = self.image.get_rect()

        #self.orientation = orientation

        #I think the number of ticks will control how far/how high/how long the projectile sails
        #through the air while the movement units will control the speed. If you want to increase
        #the speed, you better be sure to also increase the number of ticks
        self.ticks_so_far_for_h = 0
        self.ticks_till_hdir_c1 = 2 #originally 2
        self.ticks_till_hdir_c2 = 4 #originally 6
        self.ticks_till_hdir_c3 = 6 #The zenith. originally 10
        self.ticks_till_hdir_c4 = 8 #originally 14
        self.ticks_till_hdir_c5 = 11 #originally 18

        self.ticks_so_far_for_v = 0 #originally 0
        self.ticks_till_vdir_c1 = 7 #originally 12
        self.ticks_till_vdir_c2 = 8 #originally 14
        
        self.splash_duration = 5 #The splash will stick around for 5 ticks
        self.ticks_for_splash = 0

        self.landed = False
        self.orientation = orientation

        self.splash_sound_playing = False

    def update(self):
        '''Move the waterballoon.'''
        if self.orientation == "west" or self.orientation == "east":
            self._move_throwable_east_or_west(self.orientation)
        elif self.orientation == "north" or self.orientation == "south":
            self._move_throwable_north_or_south(self.orientation)
            

    def _move_throwable_north_or_south(self, direction):
        self.image = pygame.image.load("balloon-top.png") if direction == "north" \
                     else pygame.image.load("balloon-bottom.png")
        if self.ticks_so_far_for_v < self.ticks_till_vdir_c1:
            self.rect.y = self.rect.y-40 if direction == "north" else self.rect.y+40 #originally 25
            self.ticks_so_far_for_v += 1
        elif self.ticks_so_far_for_v < self.ticks_till_vdir_c2:
            self.rect.y = self.rect.y+40 if direction == "north" else self.rect.y-40
            self.ticks_so_far_for_v += 1
        else:
            self.landed = True
            if not self.splash_sound_playing:
                balloon_splash = pygame.mixer.Sound("balloon_splash.wav")
                pygame.mixer.Sound.play(balloon_splash)
                self.splash_sound_playing = True
            center = self.rect.center
            self.image = pygame.transform.scale(pygame.image.load("splash.png"), (90, 90))
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.ticks_for_splash += 1 #For clean up when we update sprites
            

    def _move_throwable_east_or_west(self, direction):
        '''Performs a series of checks that traces the trajectory of the throwable towards the east or west.'''
        self.image = pygame.image.load("balloon-left.png") if direction == "west" \
                     else pygame.image.load("balloon-right.png")
        if self.ticks_so_far_for_h < self.ticks_till_hdir_c1:
            self.rect.x = self.rect.x-20 if direction == "west" else self.rect.x+20 #affects distance #original: 15
            self.rect.y -= 50 #affects steepness of ascent/descent #original: 30
            self.ticks_so_far_for_h += 1
        elif self.ticks_so_far_for_h < self.ticks_till_hdir_c2:
            self.rect.x = self.rect.x-20 if direction == "west" else self.rect.x+20
            self.rect.y -= 45 #original: 25
            self.ticks_so_far_for_h += 1
        elif self.ticks_so_far_for_h < self.ticks_till_hdir_c3: #The crest
            #print("IN CREST")
            self.rect.x = self.rect.x-20 if direction == "west" else self.rect.x+20
            self.rect.y -= 20 #original: 5
            self.ticks_so_far_for_h += 1
        elif self.ticks_so_far_for_h < self.ticks_till_hdir_c4:
            self.rect.x = self.rect.x-20 if direction == "west" else self.rect.x+20
            self.rect.y += 45 #original: 25
            self.ticks_so_far_for_h += 1
        elif self.ticks_so_far_for_h < self.ticks_till_hdir_c5:
            self.rect.x = self.rect.x-20 if direction == "west" else self.rect.x+20
            self.rect.y += 50 #original: 30
            self.ticks_so_far_for_h += 1
        else:
            #self.ticks_so_far_for_h = 0
            self.landed = True
            if not self.splash_sound_playing:
                balloon_splash = pygame.mixer.Sound("balloon_splash.wav")
                pygame.mixer.Sound.play(balloon_splash)
                self.splash_sound_playing = True
            center = self.rect.center
            self.image = pygame.transform.scale(pygame.image.load("splash.png"), (100, 100))
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.ticks_for_splash += 1 #For clean up when we update sprites
