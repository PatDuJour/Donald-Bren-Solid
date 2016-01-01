import pygame #fine
from weapons import * #fine
from collectibles import * #fine
#from exclamation import *
import exclamation
import physical_objs

#This test version of snake_player.py grants snake access to entrances that
#would otherwise need card keys

#---Constants---
SPEED = 25 #CHANGE BACK TO 13

class Snake(pygame.sprite.Sprite):
    def __init__(self: "Snake", width=64, height=64): #won't need width and height...
        '''Initializes the attributes of a Snake Sprite.'''
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("south0.png") #By default, we're facing south
        self.rect = self.image.get_rect()
        self.origin_x = self.rect.centerx  #Was used for initializing Snake's position
        self.origin_y = self.rect.centery  #Was used for initializing Snake's position
        self.threw_punch = False
        self.punch_time = 0

        self.is_moving = False
        self.moving_north = self.moving_east = self.moving_west = False
        self.moving_south = True

        

        #Attributes involved with animation:
        self.cur_frame = 0
        self.north_imgs = ["north0.png", "north1.png", "north2.png"]
        self.east_imgs = ["east0.png", "east1.png", "east2.png"]
        self.south_imgs = ["south0.png", "south1.png", "south2.png"]
        self.west_imgs = ["west0.png", "west1.png", "west2.png"]

        self.area = None #Will be set in the main function

        self.h_move = 0
        self.v_move = 0

        self.health = 100
        self.current_weapon = Unequipped()
        self.current_item = Unequipped()
        self.lives = 3
        self.is_subdued = False
        self.reached_checkpoint = False

        self.has_floor2_card_key = True #TURN THIS BACK TO FALSE
        self.has_floor3_card_key = True #TURN THIS BACK TO FALSE
        self.has_floor4_card_key = True #TURN THIS BACK TO FALSE
        self.has_floor5_card_key = True #TURN THIS BACK TO FALSE
        self.has_elevator_card_key = True #TURN THIS BACK TO FALSE
        self.dropped_off_data_disc = False


        #Hard code weapons list and current weapon/item for now
        self.weapons_lst = [Unequipped(), RubberBandPickUp(), BananaPeelPickUp(), WaterBalloonPickUp()]
        self.items_lst = [Unequipped(), CS113DataDisc(), ElevatorCardKey(), InstantNoodlesPickUp()]

        self.time = 0
        self.merc_alerts = 0
        self.merc_stuns = 0
        self.mgs_games = 0
        self.continues = 0
        self.noodles_consumed = 0
        self.score = 0
        self.reached_end_of_game = False



    def change_move(self: "Snake", h_move: int, v_move: int):
        '''Changes the movement of a Snake Sprite.'''
        #print("(center_x, center_y): ", (self.rect.centerx, self.rect.centery))
        #print("topleft: ", (self.rect.topleft[0], self.rect.topleft[1]))
        #^Values should be the same as ones on the next line
        #print("(x, y): ", (self.rect.x, self.rect.y))
        if self.threw_punch: #If you threw punch, stop moving
            self.h_move = 0
            self.v_move = 0
        elif v_move == 0 and h_move != 0:
            self.h_move += h_move
            self.v_move = 0
        elif h_move == 0 and v_move != 0:
            self.v_move += v_move
            self.h_move = 0
        else:
            self.v_move = 0
            self.h_move = 0

            #The idea here was to reset the Sprite to the 0th "resting" Sprite when it stopped moving
            self.cur_frame = 0
            if self.moving_south:
                self.image = pygame.image.load(self.south_imgs[self.cur_frame])
            elif self.moving_north:
                self.image = pygame.image.load(self.north_imgs[self.cur_frame])
            elif self.moving_east:
                self.image = pygame.image.load(self.east_imgs[self.cur_frame])
            elif self.moving_west:
                self.image = pygame.image.load(self.west_imgs[self.cur_frame])
            
    
    def init_position(self: "Snake", x: int, y: int):
        '''Initializes the position of Snake on the game display.'''
        self.rect.x = x - self.origin_x
        self.rect.y = y - self.origin_y


    def update(self: "Snake", event = None, obj_group = None, e_group = None):
        '''Sets all the necessary updates to the state of a Snake Sprite given an event.'''
        #-----EVENT HANDLING-----
        self._event_handler(event)

        if not self.threw_punch and self.is_moving: #and self.key_pressed:
            #print("MOVING")
            #print("event: ", event)
            self.rect.x += self.h_move
            self.rect.y += self.v_move

        if self.punch_time < 3 and self.threw_punch:
            self.punch_time += 1
            #Note that by default, we're facing south
            if not (self.moving_south or self.moving_north or self.moving_east or self.moving_west):
                self.image = pygame.image.load("south_punch.png")
            if self.moving_south:
                self.image = pygame.image.load("south_punch.png")
            elif self.moving_north:
                self.image = pygame.image.load("north_punch.png")
            elif self.moving_east:
                self.image = pygame.image.load("east_punch.png")
            elif self.moving_west:
                self.image = pygame.image.load("west_punch.png")
        elif self.punch_time == 3:
            self.punch_time = 0
            self.threw_punch = False
            if not (self.moving_south or self.moving_north or self.moving_east or self.moving_west):
                self.image = pygame.image.load("south0.png")
            if self.moving_south:
                self.image = pygame.image.load("south0.png")
            elif self.moving_north:
                self.image = pygame.image.load("north0.png")
            elif self.moving_east:
                self.image = pygame.image.load("east0.png")
            elif self.moving_west:
                self.image = pygame.image.load("west0.png")

        #Process animation
        if self.is_moving and not self.threw_punch:
            if self.moving_south:
                self._animate(self.south_imgs)
            elif self.moving_north:
                self._animate(self.north_imgs)
            elif self.moving_east:
                self._animate(self.east_imgs)
            elif self.moving_west:
                self._animate(self.west_imgs)

        #CHECK IF SNAKE REACHED THE CHECKPOINT
        if self.area.is_checkpoint:
            #print("CHECKPOINT REACHED")
            self.reached_checkpoint = True

        #CHECK FOR COLLISIONS
        #Watch out, the obj_lst of the current Area sholdn't have Snake himself in it!!
        if obj_group != None:
            obj_collision_lst = pygame.sprite.spritecollide(self, obj_group, False)
            #^The rect information of all Sprites that Snake collided with is made
            #available in this list
            self._handle_obj_collisions(obj_collision_lst, obj_group)
        '''
        #Let the code in enemies.py handle Snake's damage when mercs collide with him
        if e_group != None:
            enemy_collision_lst = pygame.sprite.spritecollide(self, e_group, False)
            if len(enemy_collision_lst) != 0:
                self.health -= 1
            #print("Snake's health: ", self.health)
        '''


        #CHECK IF SNAKE HAS INSTANT NOODLES EQUIPPED WHEN HIS HEALTH IS 0
        if self.current_item.name == "Instant Noodles" and self.current_item.stock > 0 and self.health < 0:
            alert = pygame.mixer.Sound("item_consumed.wav")
            pygame.mixer.Sound.play(alert)
            self.health += 50
            self.current_item.stock -= 1
            self.noodles_consumed += 1
        elif self.health < 0:
            self.is_subdued = True



    def _handle_obj_collisions(self, collision_lst: ["Sprites"], obj_group: "Group"):
        '''Sets the necessary attributes for Snake when he collides with physical objects in an Area.'''
        for collided_object in collision_lst:
            if type(collided_object) != exclamation.Exclamation:
                if type(collided_object) == physical_objs.FrostDesk:
                    if (self.h_move > 0):  #Moving right (horizontal collision)
                        self.rect.right = collided_object.rect.left
                    elif (self.h_move < 0):  #Moving left (horizontal collision)
                        self.rect.left = collided_object.rect.right
                    elif (self.v_move > 0):  #Moving down (vertical collision)
                        self.rect.bottom = collided_object.rect.top
                    elif (self.v_move < 0):  #Moving up (vertical collision)
                        self.rect.top = collided_object.rect.bottom

                    #self.items_lst = [item for item in self.items_lst if item.name != "CS 113 Data Disc"]

                    if not self.dropped_off_data_disc:
                        for item in self.items_lst:
                            if item.name == "CS 113 Data Disc":
                                item.stock = 0
                        self.dropped_off_data_disc = True
                        #play a sound to indicate that you dropped it off

                elif (type(collided_object) == MGS1 or type(collided_object) == MGS2 or type(collided_object) == MGS3 or
                    type(collided_object) == MGS4 or type(collided_object) == MGS5):
                    self.mgs_games += 1
                    obj_group.remove(collided_object)
                elif (type(collided_object) == ElevatorCardKey):
                    self.has_elevator_card_key = True
                    self.items_lst.append(collided_object)
                    obj_group.remove(collided_object)
                elif (type(collided_object) == WaterBalloonPickUp or type(collided_object) == BananaPeelPickUp or
                      type(collided_object) == RubberBandPickUp or type(collided_object) == StrawPickUp):

                    have_weapon = False
                    for weapon in self.weapons_lst:
                        if weapon.name == collided_object.name:
                            have_weapon = True
                            if weapon.name == "Straw":
                                weapon.stock += 150
                            elif weapon.name == "Rubber Band":
                                weapon.stock += 100
                            elif weapon.name == "Banana Peel":
                                weapon.stock += 50
                            elif weapon.name == "Water Balloon":
                                weapon.stock += 25

                    if not have_weapon:
                        self.weapons_lst.append(collided_object)

                    obj_group.remove(collided_object)
                elif (type(collided_object) == Floor2CardKey or type(collided_object) == Floor3CardKey or
                      type(collided_object) == Floor4CardKey or type(collided_object) == Floor5CardKey or
                      type(collided_object) == InstantNoodlesPickUp):
                    
                    if collided_object.name == "Instant Noodles":
                        have_noodles = False
                        for item in self.items_lst:
                            if item.name == "Instant Noodles":
                                have_noodles = True
                                item.stock += 10
                        if not have_noodles:
                            self.items_lst.append(collided_object)
                    else:
                        if collided_object.name == "Floor 2 Card Key":
                            self.has_floor2_card_key = True
                        elif collided_object.name == "Floor 3 Card Key":
                            self.has_floor3_card_key = True
                        if collided_object.name == "Floor 4 Card Key":
                            self.has_floor4_card_key = True
                        if collided_object.name == "Floor 5 Card Key":
                            self.has_floor5_card_key = True
                        self.items_lst.append(collided_object)
                    
                    obj_group.remove(collided_object)
                elif (type(collided_object) == GoogleJobOffer):
                    obj_group.remove(collided_object)
                    self.lives += 1
                elif (self.h_move > 0):  #Moving right (horizontal collision)
                    self.rect.right = collided_object.rect.left
                elif (self.h_move < 0):  #Moving left (horizontal collision)
                    self.rect.left = collided_object.rect.right
                elif (self.v_move > 0):  #Moving down (vertical collision)
                    self.rect.bottom = collided_object.rect.top
                elif (self.v_move < 0):  #Moving up (vertical collision)
                    self.rect.top = collided_object.rect.bottom
            
                    
    def _animate(self: "Snake", image_lst: [str]):
        '''Steps through an animation corresponding to the provided list of images.'''
        if self.cur_frame == 0:
            self.cur_frame += 1
            self.image = pygame.image.load(image_lst[self.cur_frame])
        elif self.cur_frame == 1:
            self.cur_frame += 1
            self.image = pygame.image.load(image_lst[self.cur_frame])
        elif self.cur_frame == 2:
            self.image = pygame.image.load(image_lst[self.cur_frame])
            self.cur_frame = 0
        #You had it go up to three frames because Snake has three frames for each
        #directional movement


    def _handle_snake_movement_up(self: "Snake"):
        '''Handles an upward movement by a Snake Sprite.'''
        if not self.threw_punch:
            self.is_moving = True
            self.moving_south = self.moving_east = self.moving_west = False
            self.moving_north = True
            self.change_move(0, -SPEED)    


    def _handle_snake_movement_down(self: "Snake"):
        '''Handles a downward movement by a Snake Sprite.'''
        if not self.threw_punch:
            self.is_moving = True
            self.moving_north = self.moving_east = self.moving_west = False
            self.moving_south = True
            self.change_move(0, SPEED)


    def _handle_snake_movement_right(self: "Snake"):
        '''Handles a rightward movement by a Snake Sprite.'''
        if not self.threw_punch:
            self.is_moving = True
            self.moving_north = self.moving_south = self.moving_west = False
            self.moving_east = True
            self.change_move(SPEED, 0)


    def _handle_snake_movement_left(self: "Snake"):
        '''Handles a leftward movement by a Snake Sprite.'''
        if not self.threw_punch:
            self.is_moving = True
            self.moving_north = self.moving_south = self.moving_east = False
            self.moving_west = True
            self.change_move(-SPEED, 0)    


    def _event_handler(self: "Snake", event: "EventType"):
        '''Processes an event.'''
        if event != None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self._handle_snake_movement_up()
                if event.key == pygame.K_DOWN:
                    self._handle_snake_movement_down()
                if event.key == pygame.K_RIGHT:
                    self._handle_snake_movement_right()
                if event.key == pygame.K_LEFT:
                    self._handle_snake_movement_left()
                if event.key == pygame.K_SPACE:
                    self.threw_punch = True
                    self.is_moving = False
                    if self.current_weapon.name == "Straw" and self.current_weapon.stock > 0:
                        spitball = SpitBall()
                        if self.moving_north:
                            spitball.orientation = "north"
                        elif self.moving_south:
                            spitball.orientation = "south"
                        elif self.moving_east:
                            spitball.orientation = "east"
                        elif self.moving_west:
                            spitball.orientation = "west"
                        if self.moving_east or self.moving_west:
                            spitball.rect.centerx = self.rect.centerx
                            spitball.rect.centery = self.rect.centery - 40 #Shift the spitball up to where Snake's head would be
                        else:
                            spitball.rect.centerx = self.rect.centerx
                            spitball.rect.centery = self.rect.centery
                        self.area.s_attack_obj_group.add(spitball)
                        self.current_weapon.stock -= 1
                    elif self.current_weapon.name == "Water Balloon" and self.current_weapon.stock > 0:
                        water_balloon = WaterBalloon()
                        if self.moving_west:
                            water_balloon.orientation = "west"
                        elif self.moving_east:
                            water_balloon.orientation = "east"
                        elif self.moving_north:
                            water_balloon.orientation = "north"
                        elif self.moving_south:
                            water_balloon.orientation = "south"
                        water_balloon.rect.centerx = self.rect.centerx
                        water_balloon.rect.centery = self.rect.centery
                        self.area.s_attack_obj_group.add(water_balloon)
                        self.current_weapon.stock -= 1 #decrease the stock
                    elif self.current_weapon.name == "Banana Peel" and self.current_weapon.stock > 0:
                        banana_peel = BananaPeel()
                        if self.moving_west:
                            banana_peel.rect.centerx = self.rect.midleft[0]
                            banana_peel.rect.centery = self.rect.midleft[1]
                        elif self.moving_east:
                            banana_peel.rect.centerx = self.rect.midright[0]
                            banana_peel.rect.centery = self.rect.midright[1]
                        elif self.moving_north:
                            banana_peel.rect.centerx = self.rect.midtop[0]
                            banana_peel.rect.centery = self.rect.midtop[1]
                        elif self.moving_south:
                            banana_peel.rect.centerx = self.rect.midbottom[0]
                            banana_peel.rect.centery = self.rect.midbottom[1]
                        self.area.s_attack_obj_group.add(banana_peel)
                        self.current_weapon.stock -= 1
                    elif self.current_weapon.name == "Rubber Band" and self.current_weapon.stock > 0:
                        rubber_band = RubberBand()
                        if self.moving_north:
                            rubber_band.orientation = "north"
                        elif self.moving_south:
                            rubber_band.orientation = "south"
                        elif self.moving_east:
                            rubber_band.orientation = "east"
                        elif self.moving_west:
                            rubber_band.orientation = "west"
                        rubber_band.rect.centerx = self.rect.centerx
                        rubber_band.rect.centery = self.rect.centery
                        self.area.s_attack_obj_group.add(rubber_band)
                        self.current_weapon.stock -= 1

                    
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.is_moving = False
                    self.change_move(0, 0)
                if event.key == pygame.K_DOWN:
                    self.is_moving = False
                    self.change_move(0, 0)
                if event.key == pygame.K_RIGHT:
                    self.is_moving = False
                    self.change_move(0, 0)
                if event.key == pygame.K_LEFT:
                    self.is_moving = False
                    self.change_move(0, 0)
                if event.key == pygame.K_SPACE:
                    self.change_move(0, 0)
