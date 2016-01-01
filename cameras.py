import pygame, math, random #fine
from snake_player import * #fine
#from areas import * #don't think this is needed...
from collections import namedtuple #For assigning neighbors to Areas #fine
from colors import * #fine
from block import * #fine
from los import * #fine
from weapons import * #fine
import physical_objs
import enemies

#In this version, began writing code that has this Enemy respond to attacks from Snake


class Camera(pygame.sprite.Sprite):
    def __init__(self: "Enemy", window: "Canvas", orientation: str, patrol_speed: int = 5):
        '''Initializes the attributes of a Snake Sprite.'''
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((width, height)) #Must set the image attribute so that the sprite appears
        image = None
        if orientation == "north":
            image = "cam_north.png"
            self._looking_north = True
            self._looking_east = self._looking_south = self._looking_west = False
        elif orientation == "east":
            image = "cam_east.png"
            self._looking_east = True
            self._looking_north = self._looking_south = self._looking_west = False
        elif orientation == "south":
            image = "cam_south.png"
            self._looking_south = True
            self._looking_east = self._looking_north = self._looking_west = False
        elif orientation == "west":
            image = "cam_west.png"
            self._looking_west = True
            self._looking_east = self._looking_south = self._looking_north = False
        self.image = pygame.image.load(image)
        
        #self.image.fill(color) #If you have an actual picture, don't fill!!!
        self.rect = self.image.get_rect() #Must set the rect attribute so that you can
                                          #"grab" the Sprite by coordinates on the rect
        
        self.patrol_route = [] #Will be set by an Area object
        self._instr_index = 0
        self._current_step_num = self._current_wait_num = \
                                 self._current_look_num = 0
        self._is_moving = False
        self._cur_frame = 0
        
        self._view_obstructed = False
        self.in_alert_phase = False
        #self.in_alert_phase = True #Set this to True for testing

        self.area = None
        #You'll probably end up setting an _area attribute as well for initiating alert phases. E.g., if
        #an Enemy detects you, then the area of this Enemy (note how particular Enemies belong to only one
        #Area) will be set to an alert phase so that alerts can propagate from Area to Area. We'd also need
        #a handle on the Area so that we can set on the alert phases of all the Enemies in the Area as well.

        ## LINE OF SIGHT STUFF ##
        self.window = window
        self.los = LOS() #a new LOS would be created in _create_LOS to account for LOS changing in size
        self.los_group = pygame.sprite.Group() #HAVE GROUP FOR TESTING
        self.los_group.add(self.los) #HAVE GROUP FOR TESTING

        self.patrol_speed = patrol_speed

        self.is_boss = False

        self.spitball_stunned = self.rubberband_stunned = self.waterballoon_stunned = self.banana_peel_stunned = False
        self.stun_time = 0
        self.rubberband_hits = 0
        self.spitball_hits = 0
        self.wb_drench_time = 0

        

    def init_position(self: "Enemy", x: float, y: float):
        '''Initializes the position of Snake on the game display.'''
        self.rect.centerx = x
        self.rect.centery = y


    #In order to actually have the Sprite do anything, you need to call its update() method
    def update(self: "Enemy", collidables: "Group", snake_group: "Group", s_attack_obj_group: "Group"): #update could be where I increment the steps taken by the Enemy
        '''Sets all the necessary updates to the state of an Enemy Sprite.'''
        obj_collisions_lst = pygame.sprite.spritecollide(self, collidables, False)
        #^...Collisions between objects and Enemies...
        if not self.in_alert_phase: #self._follow_patrol_route()?
            current_instr = self.patrol_route[self._instr_index]
            movement = current_instr[0]
            units = current_instr[1]

            self._determine_movement(movement, units)
            #self._determine_animation()        


            ## LINE OF SIGHT STUFF ## Establish initial LOS...self._initial_LOS
            self._construct_initial_LOS()
            los_collision_lst = pygame.sprite.spritecollide(self.los, collidables, False)
            #^...Collisions associated with the initial LOS...

            #First, determine if an Enemy's LOS hits any physical objects in the area, in which case
            #the LOS would become obstructed
            self._view_obstructed = False
            self._handle_LOS_collision_with_obj(los_collision_lst)
            
            #Next, "look" for Snake with an LOS that may or may not have been obstructed
            self._handle_LOS_collision_with_snake(snake_group)
            #self._handle_collision_with_snake(snake_collision_lst) #Could have one section in this method devoted to handling collisions

                            
    def _go_chase_north(self):
        self._set_orientation("north")
        self.h_chase_move = 0 #To ensure no diagonal movements
        self.v_chase_move = -self.chase_speed
        self.rect.y += self.v_chase_move
        #self.rect.y -= self.chase_speed #move up
    
    def _go_chase_east(self):
        self._set_orientation("east")
        self.v_chase_move = 0
        self.h_chase_move = self.chase_speed
        self.rect.x += self.h_chase_move #move right
        #self.rect.x += self.chase_speed #move right

    def _go_chase_south(self):
        self._set_orientation("south")
        self.h_chase_move = 0
        self.v_chase_move = self.chase_speed
        self.rect.y += self.v_chase_move
        #self.rect.y += self.chase_speed #move down

    def _go_chase_west(self):
        self._set_orientation("west")
        self.v_chase_move = 0
        self.h_chase_move = -self.chase_speed
        self.rect.x += self.h_chase_move #move left
        #self.rect.x -= self.chase_speed #move left    


    def _determine_movement(self, movement, units):
        '''Determines the movement to be processed for an Enemy on patrol.'''
        if movement == "go_east":
            self._set_go_east_movement(units)
        elif movement == "go_west":
            self._set_go_west_movement(units)
        elif movement == "go_north":
            self._set_go_north_movement(units)
        elif movement == "go_south":
            self._set_go_south_movement(units)
        elif movement == "wait":
            self._set_wait_movement(units)
        elif movement == "end":
            self._instr_index = 0
                

    def _determine_animation(self):
        '''Determines the appropriate animation for this Enemy based on the direction in which
           it is facing.'''
        if self._is_moving:
            if self._looking_south:
                self._animate(self._south_imgs)
            elif self._looking_north:
                self._animate(self._north_imgs)
            elif self._looking_east:
                self._animate(self._east_imgs)
            elif self._looking_west:
                self._animate(self._west_imgs)    


    def _construct_initial_LOS(self):
        '''Constructs the initial LOS of an Enemy, which isn't shortened to account for obstructions. This
           initial LOS must be constructed in order to determine what those obsructions are.'''
        if self._looking_east:
            self._create_LOS(self.window.get_width(), 1,
                             self.rect.centerx, self.rect.centery)
        elif self._looking_west:
            self._create_LOS(self.window.get_width(), 1,
                             self.rect.centerx - self.window.get_width(), self.rect.centery)
        elif self._looking_north:            
            self._create_LOS(1, self.window.get_height(),
                             self.rect.centerx, self.rect.centery - self.window.get_height())
        elif self._looking_south:
            self._create_LOS(1, self.window.get_height(),
                             self.rect.centerx, self.rect.centery)

            

    def _handle_LOS_collision_with_obj(self, los_collision_lst: ["Sprite"]):
        '''Creates a LOS based on collisions with any objects. The orientation of the LOS
           is adjusted based on the direction this Enemy is facing.'''
        for collided_object in los_collision_lst:
            #if type(collided_object) == Block or type(collided_object) == physical_objs.GreenSofa: #HERE'S THE ISSUE. YOU NEED TO ACCOUNT FOR OTHER TYPES OF COLLIDED OBJECTS!
            if isinstance(collided_object, pygame.sprite.Sprite) and type(collided_object) != enemies.Enemy:
                self._view_obstructed = True
                if self._looking_south:
                    self._create_LOS(1, collided_object.rect.top - self.rect.top,
                                     self.rect.centerx, self.rect.centery)
                elif self._looking_north:
                    self._create_LOS(1, self.rect.bottom - collided_object.rect.bottom,
                                     self.rect.centerx, self.rect.centery - (self.rect.bottom - collided_object.rect.bottom))
                elif self._looking_east:
                    self._create_LOS(collided_object.rect.right - self.rect.right, 1,
                                     self.rect.centerx, self.rect.centery)
                elif self._looking_west:
                    self._create_LOS(self.rect.left - collided_object.rect.left, 1,
                                     self.rect.centerx - (self.rect.left - collided_object.rect.left), self.rect.centery)


    def _handle_LOS_collision_with_snake(self, snake_group):
        '''Handles a collision between Snake and a LOS that may or may not have been obstructed.'''
        if self._view_obstructed:  #If view had been obstructed, check if Snake collides with the modified los
            mod_los_collision_lst_for_snake = pygame.sprite.spritecollide(self.los, snake_group, False)
            for collided_object in mod_los_collision_lst_for_snake:  #For modified LOS collision list
                if type(collided_object) == Snake:
                    #print("SPOTTED")
                    '''
                    #print("SPOTTED")
                    self.in_alert_phase = True
                    self.area.root_alert_area = True
                    self.area.in_alert_phase = True
                    alert = pygame.mixer.Sound("alert.wav")
                    pygame.mixer.Sound.play(alert)
                    for enemy in self.area.e_group:
                        enemy.in_alert_phase = True
                    '''
                    self._set_alert_phase(snake_group)
        else:
            los_collision_lst_for_snake = pygame.sprite.spritecollide(self.los, snake_group, False)
            for collided_object in los_collision_lst_for_snake:  #for regular LOS collision list
                if type(collided_object) == Snake:
                    #print("SPOTTED")
                    '''
                    #print("SPOTTED")
                    self.in_alert_phase = True
                    self.area.root_alert_area = True
                    self.area.in_alert_phase = True
                    alert = pygame.mixer.Sound("alert.wav")
                    pygame.mixer.Sound.play(alert)
                    for enemy in self.area.e_group:
                        enemy.in_alert_phase = True
                    '''
                    self._set_alert_phase(snake_group)


    def _set_alert_phase(self, snake_group):
        '''Sets all guards in the game to alert phase.'''
        #print("SPOTTED")
        snake = list(snake_group)[0]
        snake.merc_alerts += 1
        self.in_alert_phase = True
        self.area.root_alert_area = True
        self.area.in_alert_phase = True
        #alert = pygame.mixer.Sound("alert.wav")
        #pygame.mixer.Sound.play(alert)
        for enemy in self.area.e_group:
            enemy.in_alert_phase = True
                    

    def _create_LOS(self, width: float, height: float, x: float, y: float):
        '''Creates and positions a LOS with the given width, height, x-coordinate, and y-coordinate.'''
        self.los_group.remove(self.los) #Related to making LOS visible for testing
        self.los = LOS((self.rect.centerx, self.rect.centery), width, height)
        self.los.set_position(x, y)
        self.los_group.add(self.los) #Related to making LOS visible for testing    


    def TEST_draw_block(self):
        self.los_group.draw(self.window)
        #self.vert_los_group.draw(self.window)


    def _set_wait_movement(self: "Enemy", units: int):
        '''Takes units of movement and sets the necessary attributes
           for a wait movement.'''
        if self._current_wait_num <= units:
            self._current_wait_num += 1
        else:
            self._instr_index += 1
            self._current_wait_num = 0

    #For these go_[direction]_movement methods, the camera will only ever look in the direction that it
    #was initialized to, so don't set it to look in another direction in these methods!
    def _set_go_east_movement(self: "Enemy", units: int):
        '''Takes units of movement and sets the necessary attributes
           for an eastward movement.'''
        if self._current_step_num <= units:
            self._is_moving = True
            #self._looking_east = True
            self.rect.x += self.patrol_speed
            self._current_step_num += 1
        else:
            self._is_moving = False
            #self._looking_east = False
            self._instr_index += 1 #increment self._instr_index here
            self._current_step_num = 0 #reset the number of steps for an instruction
                

    def _set_go_west_movement(self: "Enemy", units: int):
        '''Takes units of movement and sets the necessary attributes
           for a westward movement.'''
        if self._current_step_num <= units:
            self._is_moving = True
            #self._looking_west = True
            self.rect.x -= self.patrol_speed
            self._current_step_num += 1
        else:
            self._is_moving = False
            #self._looking_west = False
            self._instr_index += 1 
            self._current_step_num = 0


    def _set_go_north_movement(self: "Enemy", units: int):
        '''Takes units of movement and sets the necessary attributes
           for a northward movement.'''
        if self._current_step_num <= units:
            self._is_moving = True
            #self._looking_north = True
            self.rect.y -= self.patrol_speed
            self._current_step_num += 1
        else:
            self._is_moving = False
            #self._looking_north = False
            self._instr_index += 1
            self._current_step_num = 0

    
    def _set_go_south_movement(self: "Enemy", units: int):
        '''Takes units of movement and sets the necessary attributes
           for a southward movement.'''
        if self._current_step_num <= units:
            self._is_moving = True
            #self._looking_south = True
            self.rect.y += self.patrol_speed
            self._current_step_num += 1
        else:
            self._is_moving = False
            #self._looking_south = False
            self._instr_index += 1
            self._current_step_num = 0

    
    def _animate(self: "Enemy", image_lst: [str]):
        '''Steps through an animation corresponding to the provided list of images.'''
        if self._cur_frame == 0:
            self._cur_frame += 1
            self.image = pygame.image.load(image_lst[self._cur_frame])
        elif self._cur_frame == 1:
            self._cur_frame = 0
            self.image = pygame.image.load(image_lst[self._cur_frame])
