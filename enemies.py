import pygame, math, random #fine
from snake_player import * #fine
#from areas import * 
from collections import namedtuple #For assigning neighbors to Areas #fine
from colors import * #fine
from block import * #fine
from los import * #fine
from weapons import * #fine
from exclamation import * #fine
from collectibles import * #fine
import physical_objs

E_SNAKE_COLLIDE_DAM = 0.25
E_SB_STUN_TIME = 35
E_RB_STUN_TIME = 40
E_BP_STUN_TIME = 50
E_WB_STUN_TIME = 55

class Enemy(pygame.sprite.Sprite):
    def __init__(self: "Enemy", window: "Canvas", trigger_happiness: [int] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
                 keeps_dist: bool = False, chase_speed: int = 13, patrol_speed: int = 4, attack_box: (int) = (100, 100, 100, 100),
                 hover_dist: float = 0, color: str = "tan"):
        '''Initializes the attributes of a Snake Sprite.'''
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((width, height)) #Must set the image attribute so that the sprite appears
        self._color = color
        if self._color == "tan":
            self.image = pygame.image.load("tan_enemy_south0.png") #So they're looking south right off the bat...
        elif self._color == "blue":
            self.image = pygame.image.load("blue_enemy_south0.png") #So they're looking south right off the bat...
        elif self._color == "gray":
            self.image = pygame.image.load("gray_enemy_south0.png") #So they're looking south right off the bat...
        elif self._color == "green":
            self.image = pygame.image.load("green_enemy_south0.png") #So they're looking south right off the bat...

        
        #self.image.fill(color) #If you have an actual picture, don't fill!!!
        self.rect = self.image.get_rect() #Must set the rect attribute so that you can
                                          #"grab" the Sprite by coordinates on the rect
        
        self.patrol_route = [] #Will be set by an Area object
        self._instr_index = 0
        self._current_step_num = self._current_wait_num = \
                                 self._current_look_num = 0
        self._is_moving = False
        self._looking_north = self._looking_east = \
                            self._looking_south = self._looking_west = False

        self._cur_frame = 0
        if self._color == "tan":
            self._north_imgs = ["tan_enemy_north0.png", "tan_enemy_north1.png"]
            self._east_imgs = ["tan_enemy_east0.png", "tan_enemy_east1.png"]
            self._south_imgs = ["tan_enemy_south0.png", "tan_enemy_south1.png"]
            self._west_imgs = ["tan_enemy_west0.png", "tan_enemy_west1.png"]
            self._stunned_imgs = ["tan_enemy_stunned0.png", "tan_enemy_stunned1.png"]
        elif self._color == "blue":
            self._north_imgs = ["blue_enemy_north0.png", "blue_enemy_north1.png"]
            self._east_imgs = ["blue_enemy_east0.png", "blue_enemy_east1.png"]
            self._south_imgs = ["blue_enemy_south0.png", "blue_enemy_south1.png"]
            self._west_imgs = ["blue_enemy_west0.png", "blue_enemy_west1.png"]
            self._stunned_imgs = ["blue_enemy_stunned0.png", "blue_enemy_stunned1.png"]
        elif self._color == "gray":
            self._north_imgs = ["gray_enemy_north0.png", "gray_enemy_north1.png"]
            self._east_imgs = ["gray_enemy_east0.png", "gray_enemy_east1.png"]
            self._south_imgs = ["gray_enemy_south0.png", "gray_enemy_south1.png"]
            self._west_imgs = ["gray_enemy_west0.png", "gray_enemy_west1.png"]
            self._stunned_imgs = ["gray_enemy_stunned0.png", "gray_enemy_stunned1.png"]
        elif self._color == "green":
            self._north_imgs = ["green_enemy_north0.png", "green_enemy_north1.png"]
            self._east_imgs = ["green_enemy_east0.png", "green_enemy_east1.png"]
            self._south_imgs = ["green_enemy_south0.png", "green_enemy_south1.png"]
            self._west_imgs = ["green_enemy_west0.png", "green_enemy_west1.png"]
            self._stunned_imgs = ["green_enemy_stunned0.png", "green_enemy_stunned1.png"]
            
        
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


        ## ATTACKING STUFF ## I think I'll just let basically all of these be arguments. 6 args probably.
        self.is_firing = False #Do I even need this? So what if he's firing?
        self.trigger_happiness = trigger_happiness
        #^Could be set in an Area. More 1s means more trigger_happiness. More elements == more control over percentages?
        #1 == shoot. 0 == don't shoot. Should probably make Enemies chase more than shoot (more 0s than 1s)...The if there's
        #only one 1 out of, say, 20 elements, then the Enemy will fire 5% of the time for each individual iteration of the
        #game loop. However, since there may iterations of the game loop per second, the Enemy would be shooting quite often...
        
        #This attribute is here to avoid all Enemies from having the same AI (cuz then they'd eventually flock)
        self.keeps_dist = keeps_dist #(default will ultimately be false)...Might be renamed to keeps_distance...so distance value could be adjust too
        #^Could be set in an Area. To be a good aimer means to shoot more in the direction of Snake during chases
        #This attribute is here to avoid all Enemies from having the same AI (cuz then they'd eventually flock)
        #Perhaps could have an attribute to adjust the attack box of an enemy
        self.chase_speed = chase_speed #7 pixels per iteration
        #Would be set in Area. Default will ultimately be 7. Probably will only let this be between 7 and 9 (should never be faster than Snake)
        
        self.v_chase_move = 0 #FOR COLLISION STUFF
        self.h_chase_move = 0 #FOR COLLISON STUFF
        
        self.patrol_speed = patrol_speed
        #Would be set in Area. Default will ultimately be 4. Probably will only let this be between 4 and 6 

        self.ab_left_x, self.ab_right_x, self.ab_top_y, self.ab_bottom_y = attack_box[0], attack_box[1], attack_box[2], attack_box[3]
        #Would be set in Area. Default will ultimately be 0...Note that all these values must be the same to form the square!!!
        #Perhaps the sides of the attack box must be eat least as big as some value...100 maybe. Also, the value could only be
        #adjusted by 100 unit increments up to 300

        self.hover_dist = hover_dist #Used in conjunction with keeps_dist. was 320 before...think of this as a radius for an Enemy
        #Would be set in Area. Default will ultimately be (√(2)*s)/2 (described below). Dunno range yet. Must never be value inside attack box.
        #The minimum hover_dist must be the length of the circumradius for the circle circumscribing the attack box. circumradius = half the
        #attack box's diagonal length = (√(2)*s)/2 where s is the attack box's side length values. The hover_dist should typically
        #trace out a circle whose arcs are beyond the vertices of the attack box. --> Hmmm, 0 seems to be fine.


        self._collide_while_north = self._collide_while_east = self._collide_while_south = self._collide_while_west = False
        self._is_colliding = False

        self._nav_from_north_right = self._nav_from_north_left = False
        self._nav_from_south_right = self._nav_from_south_left = False
        self._nav_from_west_bottom = self._nav_from_west_top = False
        self._nav_from_east_bottom = self._nav_from_east_top = False

        self.spitball_stunned = self.rubberband_stunned = self.waterballoon_stunned = self.banana_peel_stunned = False
        self.stun_time = 0
        self.rubberband_hits = 0
        self.spitball_hits = 0
        self.wb_drench_time = 0

        self.is_boss = False

    def init_position(self: "Enemy", x: float, y: float):
        '''Initializes the position of Snake on the game display.'''
        self.rect.centerx = x
        self.rect.centery = y


    #In order to actually have the Sprite do anything, you need to call its update() method
    def update(self: "Enemy", collidables: "Group", snake_group: "Group", s_attack_obj_group: "Group"): #update could be where I increment the steps taken by the Enemy
        '''Sets all the necessary updates to the state of an Enemy Sprite.'''
        if not self.spitball_stunned and not self.rubberband_stunned and not self.waterballoon_stunned and not self.banana_peel_stunned:
            obj_collisions_lst = pygame.sprite.spritecollide(self, collidables, False)
            #^...Collisions between objects and Enemies...
            snake_collision_lst = pygame.sprite.spritecollide(self, snake_group, False)
            #^...Collisions between Snake and the Enemy...
            s_attack_obj_collision_lst = pygame.sprite.spritecollide(self, s_attack_obj_group, False)
            if not self.in_alert_phase: #self._follow_patrol_route()?
                current_instr = self.patrol_route[self._instr_index]
                movement = current_instr[0]
                units = current_instr[1]

                self._determine_movement(movement, units)
                self._determine_animation()        


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
                self._handle_collision_with_snake(snake_collision_lst, snake_group) #Could have one section in this method devoted to handling collisions
            else: #All of this could eventually be in a method _attack_ai() or something
                #Note that you're always guaranteed to have Snake in the snake_group cuz Snake always exists in the game display
                #You might need to reset certain attribute values of this Enemy when alert_phase is set to True
                self.is_firing = False
                snake = list(snake_group)[0]
                dist_from_snake = math.sqrt((snake.rect.centerx - self.rect.centerx)**2 + (snake.rect.centery - self.rect.centery)**2)
                #^Euclidean distance. Think of this as something that creates a circle around an Enemy. THIS DISTANCE VALUE MUST NOT BE WITHIN THE ATTACK SQUARE
                firing = random.choice(self.trigger_happiness)
                
                if obj_collisions_lst == []:
                    self._pursue_snake(snake, dist_from_snake, firing)
                elif obj_collisions_lst != []:
                    self._handle_physical_object_collisions(obj_collisions_lst, snake)
                    
                self._handle_collision_with_snake(snake_collision_lst, snake_group)                
                self._determine_animation()
        elif self.spitball_stunned and self.stun_time < E_SB_STUN_TIME:
            self.stun_time += 1
            stun_frame_index = self.stun_time % 2
            self.image = pygame.image.load(self._stunned_imgs[stun_frame_index])
            
        elif self.rubberband_stunned and self.stun_time < E_RB_STUN_TIME:
            self.stun_time += 1
            stun_frame_index = self.stun_time % 2
            self.image = pygame.image.load(self._stunned_imgs[stun_frame_index])
            
        elif self.waterballoon_stunned and self.stun_time < E_WB_STUN_TIME:
            self.stun_time += 1
            stun_frame_index = self.stun_time % 2
            self.image = pygame.image.load(self._stunned_imgs[stun_frame_index])

        elif self.banana_peel_stunned and self.stun_time < E_BP_STUN_TIME:
            self.stun_time += 1
            stun_frame_index = self.stun_time % 2
            self.image = pygame.image.load(self._stunned_imgs[stun_frame_index])
            
        elif self.spitball_stunned and self.stun_time == E_SB_STUN_TIME:
            self.spitball_hits = self.rubberband_hits = self.wb_drench_time = 0
            self.stun_time = 0
            self.spitball_stunned = False
            
        elif self.rubberband_stunned and self.stun_time == E_RB_STUN_TIME:
            self.spitball_hits = self.rubberband_hits = self.wb_drench_time = 0
            self.stun_time = 0
            self.rubberband_stunned = False
            
        elif self.waterballoon_stunned and self.stun_time == E_WB_STUN_TIME:
            self.spitball_hits = self.rubberband_hits = self.wb_drench_time = 0
            self.stun_time = 0
            self.waterballoon_stunned = False

        elif self.banana_peel_stunned and self.stun_time == E_BP_STUN_TIME:
            self.spitball_hits = self.rubberband_hits = self.wb_drench_time = 0
            self.stun_time = 0
            self.banana_peel_stunned = False


    def _pursue_snake(self: "Enemy", snake: "Snake", dist_from_snake: float, firing: int):
        '''Conducts the necessary checks for Snake's location to allow this Enemy to pursue him.'''
        if firing == 1:
            #print(self.area) #FOR TESTING
            self.is_firing = True #Do I even need this?
            #Also set is_moving to False?
            self._fire_weapon()
        else: #This else block will result in this Enemy moving in any ONE of the caridinal directions only
            self._is_moving = True
            if snake.rect.centery > self.rect.centery+self.ab_bottom_y:  #Snake is south of an Enemy's attack box
                if self.keeps_dist:
                    #if Snake is south and to the left/right of centerx and far away, then move left/right instead of down right away
                    self._keep_dist_for_north_or_south_snake("south", snake, dist_from_snake)
                else: #These lines are what was originally in: if snake.rect.centery > self.rect.centery+self.ab_bottom_y
                    self._go_chase_south()
            elif snake.rect.centery < self.rect.centery-self.ab_top_y: #Snake is north of an Enemy's attack box
                if self.keeps_dist:
                    #if Snake is north and to the left/right of centerx and far away, then move left/right instead of up right away
                    self._keep_dist_for_north_or_south_snake("north", snake, dist_from_snake)
                else:
                    self._go_chase_north()
            elif snake.rect.centerx > self.rect.centerx+self.ab_right_x: #Snake is east of an Enemy's attack box
                if self.keeps_dist:
                    #if Snake is east and to the top/bottom of centery and far away, then move up/down instead of right right away
                    self._keep_dist_for_east_or_west_snake("east", snake, dist_from_snake)
                else:
                    self._go_chase_east()
            elif snake.rect.centerx < self.rect.centerx-self.ab_left_x: #Snake is west of an Enemy's attack box
                if self.keeps_dist:
                    #if Snake is west and to the top/bottom of centery and far away, then move up/down instead of left right away
                    self._keep_dist_for_east_or_west_snake("west", snake, dist_from_snake)
                else:
                    self._go_chase_west()
            else: #Else, Snake is within the attack box
                self._is_moving = False
                self._turn_while_in_attack_box(snake)



    def _fire_weapon(self: "Enemy"):
        '''Creates a projectile that is fired from this Enemy's stun rifle.'''
        stun_bullet1 = StunBullet(None, 6, 6) #For bug fix of referencing before assignment
        #To fix that referencing before assignment thing, perhaps you can initialize.
        #the direction an Enemy is looking in in areas.py. Maybe this bug is happening
        #because this Enemy has decided to shoot before it has moved? Just construct a
        #stun bullet here. It'd be bad form in other programming languages if you didn't.
        stun_bullet2 = StunBullet(None, 6, 6)
        stun_bullet3 = StunBullet(None, 6, 6)
        stun_rifle_shoot = pygame.mixer.Sound("stun_rifle_shoot.wav")
        pygame.mixer.Sound.play(stun_rifle_shoot)
        if self._looking_north:
            #print("NORTH")
            stun_bullet1.orientation = "north"
            stun_bullet2.orientation = "northeast"
            stun_bullet3.orientation = "northwest"
        elif self._looking_south:
            #print("SOUTH")
            stun_bullet1.orientation = "south"
            stun_bullet2.orientation = "southeast"
            stun_bullet3.orientation = "southwest"
        elif self._looking_east:
            #print("EAST")
            stun_bullet1.orientation = "east"
            stun_bullet2.orientation = "northeast"
            stun_bullet3.orientation = "southeast"
        elif self._looking_west:
            #print("WEST")
            stun_bullet1.orientation = "west"
            stun_bullet2.orientation = "southwest"
            stun_bullet3.orientation = "northwest"
        stun_bullet1.rect.centerx = stun_bullet2.rect.centerx = stun_bullet3.rect.centerx = self.rect.centerx
        stun_bullet1.rect.centery = stun_bullet2.rect.centery = stun_bullet3.rect.centery = self.rect.centery
        #if stun_bullet.orientation != None: #For bug fix of referencing before assignment
        #self.area.e_attack_obj_group.add(stun_bullet1, stun_bullet2, stun_bullet3)
        if not (stun_bullet1.orientation == None or stun_bullet2.orientation == None or stun_bullet3.orientation == None):
            self.area.e_attack_obj_group.add(stun_bullet1, stun_bullet2, stun_bullet3)


    def _handle_physical_object_collisions(self: "Enemy", obj_collisions_lst: ["Sprites"], snake: "Snake"):
        '''Handles collisions between this Enemy and a physical object that is an obstacle in its path.'''
        obj = obj_collisions_lst[0]
        moving_south_obj_collide = (obj.rect.bottom > self.rect.bottom > obj.rect.top and obj.rect.bottom > self.rect.top < obj.rect.top and
            (obj.rect.right > self.rect.right > obj.rect.left and obj.rect.right > self.rect.left > obj.rect.left))
        moving_north_obj_collide = (obj.rect.top < self.rect.top < obj.rect.bottom and obj.rect.bottom < self.rect.bottom > obj.rect.top and
              (obj.rect.right > self.rect.right > obj.rect.left and obj.rect.right > self.rect.left > obj.rect.left))
        moving_west_obj_collide = (obj.rect.right > self.rect.left > obj.rect.left and obj.rect.left < self.rect.right > obj.rect.right and
              (obj.rect.top < self.rect.bottom < obj.rect.bottom and obj.rect.top < self.rect.top < obj.rect.bottom))
        moving_east_obj_collide = (obj.rect.left < self.rect.right < obj.rect.right and obj.rect.left > self.rect.left < obj.rect.right and
              (obj.rect.top < self.rect.bottom < obj.rect.bottom and obj.rect.top < self.rect.top < obj.rect.bottom))
        top_right_edge_case = (obj.rect.bottom > self.rect.bottom >= obj.rect.top and obj.rect.bottom > self.rect.top <= obj.rect.top and
             self.rect.right >= obj.rect.right)
        top_left_edge_case = (obj.rect.bottom > self.rect.bottom >= obj.rect.top and obj.rect.bottom > self.rect.top <= obj.rect.top and  
             self.rect.left <= obj.rect.left)
        bottom_left_edge_case = (obj.rect.bottom >= self.rect.top > obj.rect.top and obj.rect.top < self.rect.bottom >= obj.rect.bottom and  
              self.rect.left <= obj.rect.left)
        bottom_right_edge_case = (obj.rect.bottom >= self.rect.top > obj.rect.top and obj.rect.top < self.rect.bottom >= obj.rect.bottom and  
              self.rect.right >= obj.rect.right)

        self._navigate_around_objects(moving_south_obj_collide, moving_north_obj_collide, moving_east_obj_collide,
                                      moving_west_obj_collide, top_right_edge_case, top_left_edge_case, bottom_left_edge_case,
                                      bottom_right_edge_case, snake)



    def _navigate_around_objects(self: "Enemy", moving_south_obj_collide: bool, moving_north_obj_collide: bool,
                                 moving_east_obj_collide: bool, moving_west_obj_collide: bool, top_right_edge_case: bool,
                                 top_left_edge_case: bool, bottom_left_edge_case: bool, bottom_right_edge_case: bool, snake: "Snake"):
        '''Performs a series of checks that determine how this Enemy will navigate around an object
           that it has collided with.'''
        if (moving_south_obj_collide):
            self._navigate_obj_going_south(snake)
        elif (moving_north_obj_collide):
            self._navigate_obj_going_north(snake)
        elif (moving_west_obj_collide):
            self._navigate_obj_going_west(snake)
        elif (moving_east_obj_collide):
            self._navigate_obj_going_east(snake)
        elif (top_right_edge_case):
            self._navigate_top_right_edge()
        elif (top_left_edge_case):
            self._navigate_top_left_edge()
        elif (bottom_left_edge_case):
            self._navigate_bottom_left_edge()
        elif (bottom_right_edge_case):
            self._navigate_bottom_right_edge()
        else:
            self._navigate_smaller_objs(snake)    



    def _navigate_top_right_edge(self):
        '''Updates the necessary attributes to allow this Enemy to navigate around the top right edge
           of some physical object.'''
        #print("TOP RIGHT EDGE")
        if self.h_chase_move < 0:
            self.rect.centery -= 10
        elif self.v_chase_move > 0:
            self.rect.centerx += 10
        elif self._nav_from_south_right:
            self._go_chase_east()
        elif self._nav_from_west_top:
            self._go_chase_north()


    def _navigate_top_left_edge(self):
        '''Updates the necessary attributes to allow this Enemy to navigate around the top left edge
           of some physical object.'''
        #print("TOP LEFT EDGE")
        if self.h_chase_move > 0:
            self.rect.centery -= 10
        elif self.v_chase_move > 0:
            self.rect.centerx -= 10
        elif self._nav_from_south_left:
            self._go_chase_west()
        elif self._nav_from_east_top:
            self._go_chase_north()


    def _navigate_bottom_left_edge(self):
        '''Updates the necessary attributes to allow this Enemy to navigate around the bottom left edge
           of some physical object.'''
        #print("BOTTOM LEFT EDGE")
        if self.h_chase_move > 0:
            self.rect.centery += 10
        elif self.v_chase_move < 0:
            self.rect.centerx -= 10
        elif self._nav_from_north_left:
            self._go_chase_west()
        elif self._nav_from_east_bottom:
            self._go_chase_south()


    def _navigate_bottom_right_edge(self):
        '''Updates the necessary attributes to allow this Enemy to navigate around the bottom right edge
           of some physical object.'''
        #print("BOTTOM RIGHT EDGE")
        if self.h_chase_move < 0:
            self.rect.centery += 10
        elif self.v_chase_move < 0:
            self.rect.centerx += 10
        elif self._nav_from_north_right:
            self._go_chase_east()
        elif self._nav_from_west_bottom:
            self._go_chase_south()


    def _navigate_obj_going_south(self: "Enemy", snake):
        '''Updates the necessary attributes to allow this Enemy to navigate around a physical object
           while moving south.'''
        if snake.rect.centery > self.rect.centery: #If Snake is below the Enemy...
            #Watch out. Enemy will oscillate between these two if statements if Snake is on same vertical line as Enemy
            if snake.rect.centerx > self.rect.centerx:
                self._nav_from_south_right = True
                self._nav_from_south_left = False
                self._go_chase_east()
            elif snake.rect.centerx < self.rect.centerx:
                self._nav_from_south_left = True
                self_nav_from_south_right = False
                self._go_chase_west()
        elif snake.rect.centery <= self.rect.centery: #If Snake is above the Enemy...
            self._nav_from_south_left = self._nav_from_south_right = False
            self._go_chase_north()
            #Without this elif, this Enemy would keep on tracing the border of a physical object until it is no longer touching it.
            #This elif effectively aborts the tracing.


    def _navigate_obj_going_north(self: "Enemy", snake: "Snake"):
        '''Updates the necessary attributes to allow this Enemy to navigate around a physical object
           while moving north.'''
        if snake.rect.centery < self.rect.centery:
            if snake.rect.centerx > self.rect.centerx:
                self._nav_from_north_right = True
                self._nav_from_north_left = False
                self._go_chase_east()
            elif snake.rect.centerx < self.rect.centerx:
                self._nav_from_north_left = True
                self_nav_from_north_right = False
                self._go_chase_west()
        elif snake.rect.centery >= self.rect.centery:
            self._nav_from_north_left = self._nav_from_north_right = False
            self._go_chase_south()


    def _navigate_obj_going_west(self: "Enemy", snake: "Snake"):
        '''Updates the necessary attributes to allow this Enemy to navigate around a physical object
           while moving west.'''
        #print("snake's centery: ", snake.rect.centery)
        #print("self.rect.bottom: ", self.rect.bottom)
        #print("self.rect.top: ", self.rect.top)
        '''
        ##If statement for trying to fix the oscillating bug:
        if self.rect.bottom >= snake.rect.centery >= self.rect.top and snake.v_move == 0 and snake.h_move == 0:
            print("WOULD OSCILLATE")
            if snake.moving_north:
                self.rect.y -= 20
            elif snake.moving_south:
                self.rect.y += 20
            else:
                self.rect.y += 20
        '''
        if snake.rect.centerx < self.rect.centerx:
            if snake.rect.centery > self.rect.centery:
                #print("HERE1")
                self._nav_from_west_bottom = True
                self._nav_from_west_top = False
                self._go_chase_south()
            elif snake.rect.centery < self.rect.centery:
                #print("HERE2")
                self._nav_from_west_top = True
                self._nav_from_west_bottom = False
                self._go_chase_north()
        elif snake.rect.centerx >= self.rect.centerx:
            self._nav_from_west_top = self._nav_from_west_bottom = False
            self._go_chase_east()


    def _navigate_obj_going_east(self: "Enemy", snake: "Snake"):
        '''Updates the necessary attributes to allow this Enemy to navigate around a physical object
           while moving east.'''
        if snake.rect.centerx > self.rect.centerx: #If Snake is right of the Enemy...
            if snake.rect.centery > self.rect.centery: #Snake is bottom
                self._nav_from_east_top = False
                self._nav_from_east_bottom = True
                self._go_chase_south()
            elif snake.rect.centery < self.rect.centery: #Snake is Top
                self._nav_from_east_bottom = False
                self._nav_from_east_top = True
                self._go_chase_north()
        elif snake.rect.centerx <= self.rect.centerx: #If Snake is left of the Enemy...
            self._nav_from_east_top = self._nav_from_east_bottom = False
            self._go_chase_west()


    def _navigate_smaller_objs(self: "Enemy", snake: "Snake"): #Think about the problem you had with the smaller blue square
        '''Updates the necessary attributes for allowing enemies to navigate around objects smaller than them.'''
        if self._looking_east or self._looking_west:
            if snake.rect.y > self.rect.centery:
                self.rect.y += 10
            elif snake.rect.y <= self.rect.centery:
                self.rect.y -= 10
        elif self._looking_north or self._looking_south:
            if snake.rect.x > self.rect.centerx:
                self.rect.x += 10
            elif snake.rect.x <= self.rect.centerx:
                self.rect.x -= 10


    def _turn_while_in_attack_box(self, snake):
        '''Sets any attributes necessary for allowing an Enemy to turn towards Snake while Snake is in its attack box.'''        
        if ((snake.rect.centery < self.rect.centery or snake.rect.centery >= self.rect.centery)
            and (snake.rect.centerx > self.rect.centerx+0.75*self.ab_right_x)):
            #print("SHOOTING EAST")
            self._set_orientation("east")
            if self._color == "tan":
                self.image = pygame.image.load("tan_enemy_east0.png")
            elif self._color == "blue":
                self.image = pygame.image.load("blue_enemy_east0.png")
            elif self._color == "gray":
                self.image = pygame.image.load("gray_enemy_east0.png")
            elif self._color == "green":
                self.image = pygame.image.load("green_enemy_east0.png")
            #self._fire_weapon() #NO. Don't shoot here or else there'll be a constant line of bullets.
        elif (snake.rect.centery >= self.rect.centery and
              (self.rect.centerx-0.75*self.ab_left_x <= snake.rect.centerx <= self.rect.centerx+0.75*self.ab_right_x)):
            #print("SHOOTING SOUTH")
            self._set_orientation("south")
            if self._color == "tan":
                self.image = pygame.image.load("tan_enemy_south0.png")
            elif self._color == "blue":
                self.image = pygame.image.load("blue_enemy_south0.png")
            elif self._color == "gray":
                self.image = pygame.image.load("gray_enemy_south0.png")
            elif self._color == "green":
                self.image = pygame.image.load("green_enemy_south0.png")
        elif ((snake.rect.centery < self.rect.centery or snake.rect.centery >= self.rect.centery)
              and (snake.rect.centerx < self.rect.centerx-0.75*self.ab_left_x)):
            #print("SHOOTING WEST")
            self._set_orientation("west")
            if self._color == "tan":
                self.image = pygame.image.load("tan_enemy_west0.png")
            elif self._color == "blue":
                self.image = pygame.image.load("blue_enemy_west0.png")
            elif self._color == "gray":
                self.image = pygame.image.load("gray_enemy_west0.png")
            elif self._color == "green":
                self.image = pygame.image.load("green_enemy_west0.png")            
        elif (snake.rect.centery <= self.rect.centery and
              (self.rect.centerx-0.75*self.ab_left_x <= snake.rect.centerx <= self.rect.centerx+0.75*self.ab_right_x)):
            self._set_orientation("north")
            if self._color == "tan":
                self.image = pygame.image.load("tan_enemy_north0.png")
            elif self._color == "blue":
                self.image = pygame.image.load("blue_enemy_north0.png")
            elif self._color == "gray":
                self.image = pygame.image.load("gray_enemy_north0.png")
            elif self._color == "green":
                self.image = pygame.image.load("green_enemy_north0.png")             
        #print("FIRE!")
        #Create firing animation here...or could just set is_shooting to true?



    def _set_collision_dir(self, direction):
        '''Sets the collision_while_[direction] attribute according to what direction this Enemy
           was moving in when collision occurred.'''
        if direction == "north":
            self._collide_while_south = self._collide_while_east = self._collide_while_west = False
            self._collide_while_north = True
        elif direction == "east":
            self._collide_While_north = self._collide_while_south = self._collide_while_west = False
            self._collide_while_east = True
        elif direction == "south":
            self._collide_while_north = self._collide_while_east = self._collide_while_west = False
            self._collide_while_south = True          
        elif direction == "west":
            self._collide_while_north = self._collide_while_east = self._collide_while_south = False
            self._collide_while_west = True


    def _keep_dist_for_north_or_south_snake(self, direction, snake, dist_from_snake): #STILL NEEDED TO PASS dist_from_snake to here
        #print("KEEP DIST NORTH OR SOUTH")
        if snake.rect.centerx < self.rect.centerx and dist_from_snake > self.hover_dist: #Snake is left
            self._go_chase_west()
        elif snake.rect.centerx >= self.rect.centerx and dist_from_snake > self.hover_dist: #Snake is right
            self._go_chase_east()
        else: #Code here should be similar to code in the if/else statement this function is called from
            if direction == "south":
                self._go_chase_south()
            else:
                self._go_chase_north()


    def _keep_dist_for_east_or_west_snake(self, direction, snake, dist_from_snake): #STILL NEEDED TO PASS dist_from_snake to here
        #print("KEEP DIST EAST OR WEST")
        if snake.rect.centery < self.rect.centery and dist_from_snake > self.hover_dist: #Snake is top
            self._go_chase_north()
        elif snake.rect.centery >= self.rect.centery and dist_from_snake > self.hover_dist: #Snake is bottom
            self._go_chase_south()
        else:
            if direction == "east":
                self._go_chase_east()
            else:
                self._go_chase_west()

                            
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

            
    def _set_orientation(self, direction):
        '''Sets the directional orientation of an Enemy'''
        if direction == "north":
            self._looking_south = self._looking_east = self._looking_west = False
            self._looking_north = True
        elif direction == "east":
            self._looking_north = self._looking_south = self._looking_west = False
            self._looking_east = True
        elif direction == "south":
            self._looking_north = self._looking_east = self._looking_west = False
            self._looking_south = True          
        elif direction == "west":
            self._looking_north = self._looking_east = self._looking_south = False
            self._looking_west = True


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
        elif movement == "look_east":
            self._set_look_east_movement(units)
        elif movement == "look_west":
            self._set_look_west_movement(units)
        elif movement == "look_north":
            self._set_look_north_movement(units)
        elif movement == "look_south":
            self._set_look_south_movement(units)
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
            if isinstance(collided_object, pygame.sprite.Sprite) and type(collided_object) != self:
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
                    self.set_alert_phase(snake_group) #COMMENT OUT FOR NOW
                    #pass
        else:
            los_collision_lst_for_snake = pygame.sprite.spritecollide(self.los, snake_group, False)
            for collided_object in los_collision_lst_for_snake:  #for regular LOS collision list
                if type(collided_object) == Snake:
                    self.set_alert_phase(snake_group) #COMMENT OUT FOR NOW
                    #pass


    def set_alert_phase(self, snake_group):
        '''Sets all guards in the game to alert phase.'''
        #print("SPOTTED")
        exclaim = Exclamation()
        exclaim.set_position(self.rect.centerx, self.rect.top-25)
        self.area.obj_group.add(exclaim)
        snake = list(snake_group)[0]
        snake.merc_alerts += 1
        self.in_alert_phase = True
        self.area.root_alert_area = True
        self.area.in_alert_phase = True
        #alert = pygame.mixer.Sound("alert.wav")
        #pygame.mixer.Sound.play(alert)
        for enemy in self.area.e_group:
            enemy.in_alert_phase = True


    def _handle_collision_with_snake(self, snake_collision_lst, snake_group):
        if len(snake_collision_lst) > 0:
            #print("SPOTTED")
            if not self.in_alert_phase:
                self.set_alert_phase(snake_group) #COMMENT OUT FOR NOW
                #pass
            self.area.player_obj.health -= E_SNAKE_COLLIDE_DAM
            #print(self.area.player_obj.health) #FOR TESTING
                    

    def _create_LOS(self, width: float, height: float, x: float, y: float):
        '''Creates and positions a LOS with the given width, height, x-coordinate, and y-coordinate.'''
        self.los_group.remove(self.los) #Related to making LOS visible for testing
        self.los = LOS((self.rect.centerx, self.rect.centery), width, height)
        self.los.set_position(x, y)
        self.los_group.add(self.los) #Related to making LOS visible for testing    


    def TEST_draw_block(self):
        self.los_group.draw(self.window)
        #self.vert_los_group.draw(self.window)
        

    def _set_look_north_movement(self: "Enemy", units :int):
        '''Takes units of movement and sets the necessary attributes
           for a look north movement.'''
        if self._current_look_num <= units:
            if self._color == "tan":
                self.image = pygame.image.load("tan_enemy_north0.png")
            elif self._color == "blue":
                self.image = pygame.image.load("blue_enemy_north0.png")
            elif self._color == "gray":
                self.image = pygame.image.load("gray_enemy_north0.png")
            elif self._color == "green":
                self.image = pygame.image.load("green_enemy_north0.png")            
            self._looking_north = True
            self._current_look_num += 1
        else:
            self._instr_index += 1
            self._looking_north = False
            self._current_look_num = 0


    def _set_look_south_movement(self: "Enemy", units :int):
        '''Takes units of movement and sets the necessary attributes
           for a look south movement.'''
        if self._current_look_num <= units:
            if self._color == "tan":
                self.image = pygame.image.load("tan_enemy_south0.png")
            elif self._color == "blue":
                self.image = pygame.image.load("blue_enemy_south0.png")
            elif self._color == "gray":
                self.image = pygame.image.load("gray_enemy_south0.png")
            elif self._color == "green":
                self.image = pygame.image.load("green_enemy_south0.png") 
            self._looking_south = True
            self._current_look_num += 1
        else:
            self._instr_index += 1
            self._looking_south = False
            self._current_look_num = 0


    def _set_look_east_movement(self: "Enemy", units :int):
        '''Takes units of movement and sets the necessary attributes
           for a look east movement.'''
        if self._current_look_num <= units:
            if self._color == "tan":
                self.image = pygame.image.load("tan_enemy_east0.png")
            elif self._color == "blue":
                self.image = pygame.image.load("blue_enemy_east0.png")
            elif self._color == "gray":
                self.image = pygame.image.load("gray_enemy_east0.png")
            elif self._color == "green":
                self.image = pygame.image.load("green_enemy_east0.png")             
            self._looking_east = True
            self._current_look_num += 1
        else:
            self._instr_index += 1
            self._looking_east = False
            self._current_look_num = 0


    def _set_look_west_movement(self: "Enemy", units :int):
        '''Takes units of movement and sets the necessary attributes
           for a look west movement.'''
        if self._current_look_num <= units:
            if self._color == "tan":
                self.image = pygame.image.load("tan_enemy_west0.png")
            elif self._color == "blue":
                self.image = pygame.image.load("blue_enemy_west0.png")
            elif self._color == "gray":
                self.image = pygame.image.load("gray_enemy_west0.png")
            elif self._color == "green":
                self.image = pygame.image.load("green_enemy_west0.png")             
            self._looking_west = True
            self._current_look_num += 1
        else:
            self._instr_index += 1
            self._looking_west = False
            self._current_look_num = 0


    def _set_wait_movement(self: "Enemy", units: int):
        '''Takes units of movement and sets the necessary attributes
           for a wait movement.'''
        if self._current_wait_num <= units:
            self._current_wait_num += 1
        else:
            self._instr_index += 1
            self._current_wait_num = 0


    def _set_go_east_movement(self: "Enemy", units: int):
        '''Takes units of movement and sets the necessary attributes
           for an eastward movement.'''
        if self._current_step_num <= units:
            self._is_moving = True
            self._looking_east = True
            self.rect.x += self.patrol_speed
            self._current_step_num += 1
        else:
            self._is_moving = False
            self._looking_east = False
            self._instr_index += 1 #increment self._instr_index here
            self._current_step_num = 0 #reset the number of steps for an instruction
                

    def _set_go_west_movement(self: "Enemy", units: int):
        '''Takes units of movement and sets the necessary attributes
           for a westward movement.'''
        if self._current_step_num <= units:
            self._is_moving = True
            self._looking_west = True
            self.rect.x -= self.patrol_speed
            self._current_step_num += 1
        else:
            self._is_moving = False
            self._looking_west = False
            self._instr_index += 1 
            self._current_step_num = 0


    def _set_go_north_movement(self: "Enemy", units: int):
        '''Takes units of movement and sets the necessary attributes
           for a northward movement.'''
        if self._current_step_num <= units:
            self._is_moving = True
            self._looking_north = True
            self.rect.y -= self.patrol_speed
            self._current_step_num += 1
        else:
            self._is_moving = False
            self._looking_north = False
            self._instr_index += 1
            self._current_step_num = 0

    
    def _set_go_south_movement(self: "Enemy", units: int):
        '''Takes units of movement and sets ets the necessary attributes
           for a southward movement.'''
        if self._current_step_num <= units:
            self._is_moving = True
            self._looking_south = True
            self.rect.y += self.patrol_speed
            self._current_step_num += 1
        else:
            self._is_moving = False
            self._looking_south = False
            self._instr_index += 1
            self._current_step_num = 0

    
    def _animate(self: "Enemy", image_lst: [str]):
        '''Steps through an animation corresponding to the provided list of images.'''
        if self._cur_frame == 0:
            self._cur_frame += 1
            self.image = pygame.image.load(image_lst[self._cur_frame])
        elif self._cur_frame == 1: #Max offset value in images list is 1
            self._cur_frame = 0
            self.image = pygame.image.load(image_lst[self._cur_frame])
