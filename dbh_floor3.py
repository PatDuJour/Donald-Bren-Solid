import pygame #fine
#from snake_player import * #fine
#from collections import namedtuple #For assigning neighbors to Areas #fine
from colors import * #fine
from block import * #fine
from weapons import * #fine
from collectibles import * #fine
#from area_base import *
import area_base
import thornton
import physical_objs


class Area3_1(area_base.Area):
    '''A class to represent Area3_1 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_1 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = True
        self._initialize_area1_walls_and_railings()

    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "peach background.png")
        self.obj_group.draw(window)
        self._draw_area1_stairs(window)
        
        window.blit(pygame.font.SysFont("Arial", 30).render("FLOOR 3", 1, BLACK), (self.width*0.77, self.height*0.70))
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= self.width*0.10 and self.player_obj.rect.centery >= self.height*0.55
                and self.player_obj.rect.centery <= self.height*0.75 and self.player_obj.moving_west):
                print("in stairwell2_1_to_3_1")
                new_area = self._make_transition(self.width*0.80-70, self.height*0.65, area_dict, "inner1")

                '''
                print("in 2_1")
                new_area = self._make_transition(self.width*0.10+500, self.height*0.35, area_dict, "inner1")
                #new_area._reset_enemy_state()               
                #new_area._formation1()
                self.player_obj.moving_east = True
                '''

            elif (self.player_obj.rect.topright[0] >= self.width*0.90 and self.player_obj.rect.centery >= self.height*0.35
                  and self.player_obj.rect.centery <= self.height*0.60 and self.player_obj.moving_east):
                print("in 3_2")
                new_area = self._make_transition(40, self.height*0.725, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()

            elif (self.player_obj.rect.x <= self.width*0.10 and self.player_obj.rect.centery >= self.height*0.25
                  and self.player_obj.rect.centery <= self.height*0.45 and self.player_obj.moving_west):
                if self.player_obj.has_floor4_card_key:
                    print("in stairwell3_1_to_4_1")
                    new_area = self._make_transition(self.width*0.80-70, self.height*0.35, area_dict, "inner2")
                else:
                    if not pygame.mixer.get_busy():
                        denied = pygame.mixer.Sound("denied.wav")
                        pygame.mixer.Sound.play(denied)

            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)
           
        return new_area

###JEREMY
class Stairwell3_1_to_4_1(area_base.Area):
    '''A class that represents an intermediate stairwell between 3_1 and 4_1.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area2_8_LeftInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False
        self._initialize_stairwell_walls_and_railings()

        
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass

        
    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        self._draw_stairwell_stairs_and_landing(window)
                     

    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        #print("Snake's Health: ", self.player_obj.health)
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.topright[0] >= self.width*0.80 and self.player_obj.rect.centery >= self.height*0.25
                  and self.player_obj.rect.centery <= self.height*0.45 and self.player_obj.moving_east):
                print("in 3_1")
                new_area = self._make_transition(self.width*0.10+70, self.height*0.35, area_dict, "inner1")
                #new_area._reset_enemy_state()
                #new_area._formation1()


            elif (self.player_obj.rect.topright[0] >= self.width*0.80 and self.player_obj.rect.centery >= self.height*0.55
                  and self.player_obj.rect.centery <= self.height*0.75 and self.player_obj.moving_east):
                print("in 4_1")
                new_area = self._make_transition(self.width*0.10+70, self.height*0.65, area_dict, "inner2")
                #new_area._reset_enemy_state()
                #new_area._formation1()

                
            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area
###END JEREMY
    
class Area3_2(area_base.Area):
    '''A class to represent Area3_2 of DBH.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: ["Enemy"]=None):
        '''Initializes the attributes of an Area3_2 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        lower_right_block = Block(LIGHT_YELLOW, self.width*0.20, self.height*0.35, "light yellow small semi vertical.png")
        lower_right_block.init_position(self.width*0.80, self.height*0.65)
        
        upper_left_wall = Block(BRICK, self.width*0.02, self.height*0.60, "brick vertical wall.png")
        upper_left_wall.init_position(0, 0)
        
        upper_right_wall = Block(LIGHT_YELLOW, self.width*0.02, self.height*0.25, "light yellow vertical wall.png")
        upper_right_wall.init_position(self.width*0.98, 0)
        
        lower_left_wall = Block(LIGHT_YELLOW, self.width*0.02, self.height*0.15, "light yellow vertical wall.png")
        lower_left_wall.init_position(0, self.height*0.85)
        
        lower_right_wall = Block(LIGHT_YELLOW, self.width*0.78, self.height*0.02, "light yellow horizontal wall.png")
        lower_right_wall.init_position(self.width*0.02, self.height*0.98)
        
        self.obj_group.add(lower_right_block, upper_left_wall, upper_right_wall, lower_left_wall, lower_right_wall)

        mgs3 = MGS3()
        mgs3.init_position(self.width*0.43, self.height*0.40)
        self.obj_group.add(mgs3)

        red_sofa_chair = physical_objs.RedSofaChair("west")
        red_sofa_chair.init_position(self.width*0.71, self.height*0.83)
        self.obj_group.add(red_sofa_chair)

        square_table = physical_objs.SmallSquareTable()
        #square_table.init_position(self.width*0.61, self.height*0.85)
        square_table.init_position(self.width*0.60, self.height*0.85)
        self.obj_group.add(square_table)
        
    ### Vu formation & patrol route area3_2
    # formation from area3_1, 3_3, 3_10
    def _formation1(self):
        if self.e_group != None:
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route3(list(self.e_group)[2]) #Enemy3
            self.gen_patrol_route4(list(self.e_group)[3]) #Enemy4
            self.gen_patrol_route5(list(self.e_group)[4]) #Enemy5


    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            #enemy.init_position(200, 150)
            enemy.init_position(self.width*0.18, self.height*0.16)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 10), ("look_south", 10), ("look_east", 10), ("look_west", 10), ("end", 0)]


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            #enemy.init_position(800, 150)
            enemy.init_position(self.width*0.72, self.height*0.16)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 10), ("look_west", 10), ("look_north", 10), ("look_east", 10), ("end", 0)]


    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            #enemy.init_position(200, 600)
            enemy.init_position(self.width*0.18, self.height*0.66)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 10), ("look_south", 10), ("look_east", 10), ("look_west", 10), ("end", 0)]


    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            #enemy.init_position(800, 600)
            enemy.init_position(self.width*0.72, self.height*0.66)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 10), ("look_west", 10), ("look_north", 10), ("look_east", 10), ("end", 0)]


    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            #enemy.init_position(200, 150)
            enemy.init_position(self.width*0.45, self.height*0.90)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 10), ("look_east", 15), ("end", 0)]
    ### End Vu formation & patrol route area2_2        

    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "peach background.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, BLACK, (self.width*0.20, self.height*0.98), (self.width*0.40, self.height*0.98), self.inner_door_thickness) #inner door
        

    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.25
                  and self.player_obj.rect.centery <= self.height*0.65 and self.player_obj.moving_east):
                print("in 3_3")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()
                

            elif (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.60
                and self.player_obj.rect.centery <= self.height*0.85 and self.player_obj.moving_west):
                print("in 3_1")
                new_area = self._make_transition(self.width*0.90-40, self.height*0.475, area_dict, "west1")
                

            elif (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.02
                and self.player_obj.rect.centerx <= self.width*0.98 and self.player_obj.moving_north):
                print("in 3_10")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()

            elif (self.player_obj.rect.bottomleft[1] >= self.height*0.97 and self.player_obj.rect.bottomleft[0] >= self.width*0.20
                and self.player_obj.rect.bottomleft[0] <= self.width*0.40 and self.player_obj.moving_south):
                print("in 3_2_lower_inner_area")
                new_area = self._make_transition(self.width*0.50, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()

                
            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

        return new_area


class Area3_2_LowerInnerArea(area_base.Area):
    '''A class that represents the lower inner Area of Area2_15.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area2_15_LowerInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_south_inner_room()

        rb = RubberBandPickUp()
        rb.init_position(self.width*0.50, self.height*0.45)
        self.obj_group.add(rb)

        straw = StrawPickUp()
        straw.init_position(self.width/2, self.height/2)
        self.obj_group.add(straw)

    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.35
                and self.player_obj.rect.centerx <= self.width*0.65 and self.player_obj.moving_north):
                print("in 3_2")
                new_area = self._make_transition(self.width*0.30, self.height*0.97-60, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_3(area_base.Area):
    '''A class to represent Area3_3 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_3 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ##FOR CHECKPOINTS

        upper_left_block = Block(DARK_TEAL, self.width*.4, self.height*.25, "dark teal small semi horizontal.png")
        upper_left_block.init_position(0,0)

        lower_left_block = Block(LIGHT_YELLOW, self.width*.4, self.height*.35, "light yellow small semi horizontal.png")
        lower_left_block.init_position(0, self.height*.65)

        right_block = Block(LIGHT_YELLOW, self.width*.15, self.height, "light yellow big vertical.png")
        right_block.init_position(self.width*.85, 0)

        upper_wall = Block(DARK_TEAL, self.width*0.10, self.height*0.02, "dark teal horizontal wall.png")
        upper_wall.init_position(self.width*0.75, 0)

        lower_wall = Block(LIGHT_YELLOW, self.width*0.10, self.height*0.02, "light yellow horizontal wall.png")
        lower_wall.init_position(self.width*0.40, self.height*0.98)

        self.obj_group.add(upper_left_block, lower_left_block, right_block, upper_wall, lower_wall)

        #AREA3_3 PHYSICAL OBJECTS
        green_sofa = physical_objs.GreenSofa("east")
        green_sofa.init_position(self.width*0.55, self.height*0.30)
        self.obj_group.add(green_sofa)
        
        long_table = physical_objs.SmallLongTable("vertical")
        long_table.init_position(self.width*0.66, self.height*0.32)
        self.obj_group.add(long_table)        

    def _formation1(self):
        #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
        if self.e_group != None:
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2

    def _formation2(self):
        #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
        if self.e_group != None:
            self.gen_patrol_route2(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route3(list(self.e_group)[1]) #Enemy2


    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.45, self.height*0.90)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 20), ("look_east", 26), ("end", 0)]


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.81, self.height*0.10)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 20), ("look_west", 15), ("end", 0), ("wait", 10), ("end", 0)]

    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.45, self.height*0.90)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 20), ("look_north", 15), ("end", 0)]

        
    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.10, self.height*0.65), (self.width*0.30, self.height*0.65), self.inner_door_thickness) #upper inner door
        pygame.draw.line(window, WOODEN, (self.width*0.85, self.height*0.70), (self.width*0.85, self.height*0.90), self.inner_door_thickness) #lower inner door
        

    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.25
                and self.player_obj.rect.centery <= self.height*0.65 and self.player_obj.moving_west):
                print("in 3_2")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.40
                and self.player_obj.rect.centerx <= self.width*0.75 and self.player_obj.moving_north):
                print("in 3_9")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation2()


            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.50
                  and self.player_obj.rect.centerx <= self.width*0.85 and self.player_obj.moving_south):
                print("in 3_4")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()

            '''
            elif (self.player_obj.rect.bottomleft[1] >= self.height*0.645 and self.player_obj.rect.bottomleft[0] >= self.width*0.095
                  and self.player_obj.rect.bottomright[0] <= self.width*0.305 and self.player_obj.moving_south):
                print("in 3_3_left_inner_entrance")
                new_area = self._make_transition(self.width*0.50, 40, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.topright[0] >= self.width*0.85 and self.player_obj.rect.topright[1] >= self.height*0.695
                  and self.player_obj.rect.bottomright[1] <= self.height*0.905 and self.player_obj.moving_east):
                print("in 3_3_right_inner_entrance")
                new_area = self._make_transition(40, self.height*0.50, area_dict, "inner2")
                new_area._reset_enemy_state()
                new_area._formation1()
            '''


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

        return new_area


class Area3_3_LeftInnerArea(area_base.Area):
    '''A class to represent a left inner Area of Area3_3'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_3_LeftInnerArea object'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_south_inner_room()
        

    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.35
                and self.player_obj.rect.centerx <= self.width*0.65 and self.player_obj.moving_north):
                print("in 3_3")
                new_area = self._make_transition(self.width*0.20, self.height*0.65-70, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_3_RightInnerArea(area_base.Area):
    '''A class to represent a right inner Area of Area3_3'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_3_RightInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False
        self._draw_east_inner_room()

        
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass

        
    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
                     

    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        #print("Snake's Health: ", self.player_obj.health)
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.35
                and self.player_obj.rect.centery <= self.height*0.65 and self.player_obj.moving_west):
                print("in 3_3")
                new_area = self._make_transition(self.width*0.85-40, self.height*0.80, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()

                
            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area
    

class Area3_4(area_base.Area):
    '''A class to represent Area3_4 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_4 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        top_block = Block(DARK_TEAL, self.width*0.35, self.height*0.10, "dark teal small horizontal.png")
        top_block.init_position(self.width*0.15, 0)

        upper_left_block = Block(DARK_TEAL, self.width*0.15, self.height*0.35, "dark teal small semi vertical.png")
        upper_left_block.init_position(0, 0)

        lower_left_block = Block(LIGHT_YELLOW, self.width*.50, self.height*0.65, "light yellow big semi vertical.png")
        lower_left_block.init_position(0, self.height*0.35)

        upper_right_block = Block(LIGHT_YELLOW, self.width*0.15, self.height*0.50, "light yellow small semi vertical.png")
        upper_right_block.init_position(self.width*0.85, 0)

        lower_right_block = Block(LIGHT_YELLOW, self.width*0.15, self.height*0.50, "light yellow small semi vertical.png")
        lower_right_block.init_position(self.width*0.85, self.height*0.50)

        self.obj_group.add(top_block, upper_left_block, lower_left_block, upper_right_block, lower_right_block)


    #vu -- start of enemies' patrol routes for area3_4
    #formation from 3 to 4
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here?
            self.gen_patrol_route1(list(self.e_group)[0])
            self.gen_patrol_route2(list(self.e_group)[1])
            self.gen_patrol_route3(list(self.e_group)[2])
            
    #formation from 5 to 4           
    def _formation2(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here?
            self.gen_patrol_route4(list(self.e_group)[0])
            self.gen_patrol_route2(list(self.e_group)[1])
            self.gen_patrol_route5(list(self.e_group)[2])


    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.75, self.height*.20)
            enemy._looking_south = True
            enemy.patrol_route = [("go_south", 50), ("look_west", 10), ("look_east", 10),
                                  ("look_north", 15), ("wait", 10), ("look_south", 15), ("go_north", 50),
                                   ("look_north", 15), ("look_east", 15), ("wait", 10), ("end", 0)]


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.30, self.height*.23) #use to be self.height*.25
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 10), ("look_east", 10), ("look_north", 10),
                                  ("look_east", 10), ("end", 0)]


    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.65, self.height*.80)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 10), ("look_west", 10), ("wait", 10), ("look_east", 10),
                                  ("wait", 10), ("look_north", 10), ("end", 0)]


    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.75, self.height*.75)
            enemy._looking_north = True
            enemy.patrol_route = [("go_north", 40), ("look_west", 10), ("look_east", 10),
                                  ("look_north", 15), ("wait", 10), ("look_south", 15), ("go_south", 40),
                                   ("look_north", 15), ("look_east", 15), ("wait", 10), ("end", 0)]

    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.65, self.height*.20)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 10), ("look_south", 10), ("wait", 10), ("look_east", 10),
                                  ("look_west", 10), ("wait", 10), ("end", 0)]

    #vu -- end of enemies' patrol routes for area3_4
            
    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.85, self.height*0.15), (self.width*0.85, self.height*0.35), self.inner_door_thickness) #upper inner door
        pygame.draw.line(window, WOODEN, (self.width*0.50, self.height*0.45), (self.width*0.50, self.height*0.65), self.inner_door_thickness) #middle inner door
        pygame.draw.line(window, WOODEN, (self.width*0.85, self.height*0.60), (self.width*0.85, self.height*0.80), self.inner_door_thickness) #lower inner door


    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.50
                and self.player_obj.rect.centerx <= self.width*0.85 and self.player_obj.moving_north):
                print("in 3_3")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.50
                  and self.player_obj.rect.centerx <= self.width*0.85 and self.player_obj.moving_south):
                print("in 3_5")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()

            '''
            elif (self.player_obj.rect.topright[0] >= self.width*0.85 and self.player_obj.rect.topright[1] >= self.height*0.145
                  and self.player_obj.rect.bottomright[1] <= self.height*0.355 and self.player_obj.moving_east):
                print("in 3_4_upper_right_inner_entrance")
                new_area = self._make_transition(40, self.height*0.50, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()
            '''


        self._handle_corners_and_boundaries()

        #For resetting the ticks to safety. This is for Areas right next to safe havens
        if new_area != old_area and old_area.is_safe_haven:
            old_area.ticks = 0

        #FOR PROJECTICLES
        self._clean_up_attack_objects(new_area, old_area)

        return new_area


class Area3_4_UpperRightInnerArea(area_base.Area):
    '''A class to represent an upper right inner Area of Area3_4'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_4_UpperRightInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False
        self._draw_east_inner_room()

        
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass

        
    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        

    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        #print("Snake's Health: ", self.player_obj.health)
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.35
                and self.player_obj.rect.centery <= self.height*0.65 and self.player_obj.moving_west):
                print("in 3_4")
                new_area = self._make_transition(self.width*0.85-40, self.height*0.25, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()

                
            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_5(area_base.Area):
    '''A class to represent Area3_5 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_5 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False

        upper_left_block = Block(LIGHT_YELLOW, self.width*0.50, self.height*0.50, "light yellow big semi horizontal.png")
        upper_left_block.init_position(0, 0)

        lower_left_block = Block(LIGHT_YELLOW, self.width*0.50, self.height*0.50, "light yellow big semi horizontal.png")
        lower_left_block.init_position(0, self.height*0.50)

        upper_right_block = Block(LIGHT_YELLOW, self.width*0.15, self.height*0.33, "light yellow small semi vertical.png")
        upper_right_block.init_position(self.width*0.85, 0)

        middle_right_block = Block(LIGHT_YELLOW, self.width*0.15, self.height*0.33, "light yellow small semi vertical.png")
        middle_right_block.init_position(self.width*0.85, self.height*0.33)

        lower_right_block = Block(LIGHT_YELLOW, self.width*0.15, self.height*0.34, "light yellow small semi vertical.png")
        lower_right_block.init_position(self.width*0.85, self.height*0.66)

        self.obj_group.add(upper_left_block, lower_left_block, upper_right_block, middle_right_block, lower_right_block)


    #vu -- start of enemies's patrol routes for area3_5
    # formation from area3_4 to area3_5
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route3(list(self.e_group)[2]) #Enemy3

    # formation from area3_6 to area3_5
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route4(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route5(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route6(list(self.e_group)[2]) #Enemy3        

    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.68, self.height*.25) #use to be 20
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 7), ("look_east", 20), ("look_west", 20), ("look_north", 20), ("end", 0)]

    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.54, self.height*.80)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 15), ("look_south", 20), ("look_north", 20), ("end", 0)]


    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.81, self.height*.80)
            enemy._looking_west = True
            enemy.patrol_route = [("look_west", 15), ("look_south", 20), ("look_north", 20), ("end", 0)]

    
    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.68, self.height*.75)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 7), ("look_west", 20), ("look_east", 20), ("look_south", 20), ("end", 0)]


    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.54, self.height*.25)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 15), ("look_north", 20), ("look_south", 20), ("end", 0)]


    def gen_patrol_route6(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.81, self.height*.25)
            enemy._looking_west = True
            enemy.patrol_route = [("look_west", 15), ("look_north", 20), ("look_south", 20), ("end", 0)]

            
    #vu -- end of enemies's patrol routes for area3_5             

    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.50, self.height*0.15), (self.width*0.50, self.height*0.35), self.inner_door_thickness) #upper left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.50, self.height*0.65), (self.width*0.50, self.height*0.85), self.inner_door_thickness) #lower left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.85, self.height*0.07), (self.width*0.85, self.height*0.27), self.inner_door_thickness) #upper right inner door
        pygame.draw.line(window, BLACK, (self.width*0.85, self.height*0.40), (self.width*0.85, self.height*0.60), self.inner_door_thickness) #middle right inner door
        pygame.draw.line(window, WOODEN, (self.width*0.85, self.height*0.73), (self.width*0.85, self.height*0.93), self.inner_door_thickness) #lower right inner door

        
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        #print("Snake's Health: ", self.player_obj.health)
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.50
                and self.player_obj.rect.centerx <= self.width*0.85 and self.player_obj.moving_north):
                print("in 3_4")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation2()

                
            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.50
                  and self.player_obj.rect.centerx <= self.width*0.85 and self.player_obj.moving_south):
                print("in 3_6")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.topright[0] >= self.width*0.85 and self.player_obj.rect.centery >= self.height*0.40
                  and self.player_obj.rect.centery <= self.height*0.60 and self.player_obj.moving_east):
                print("in 3_5_middle_inner_entrance")
                new_area = self._make_transition(40, self.height*0.50, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()

                
            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_5_MiddleInnerArea(area_base.Area):
    '''A class that represents the middle inner Area of Area3_5'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_5_MiddleInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False
        self._draw_east_inner_room()

        banana = BananaPeelPickUp()
        banana.init_position(self.width/2, self.height/2)
        self.obj_group.add(banana)
        
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass

        
    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
                     

    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        #print("Snake's Health: ", self.player_obj.health)
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.35
                and self.player_obj.rect.centery <= self.height*0.65 and self.player_obj.moving_west):
                print("in 3_5")
                new_area = self._make_transition(self.width*0.85-40, self.height*0.50, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()

                
            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area

    
class Area3_6(area_base.Area):
    '''A class to represent Area 3_6 of DBH'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_6 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_left_block = Block(LIGHT_YELLOW, self.width*0.50, self.height*0.30, "light yellow big horizontal.png")
        upper_left_block.init_position(0,0)

        upper_right_block = Block(LIGHT_YELLOW, self.width*0.15, self.height*0.75, "light yellow big vertical.png")
        upper_right_block.init_position(self.width*0.85, 0)

        lower_left_block = Block(LIGHT_YELLOW, self.width*.25, self.height*.25, "light yellow small semi horizontal.png")
        lower_left_block.init_position(0, self.height*.75)

        lower_right_block = Block(LIGHT_YELLOW, self.width*.75, self.height*.25, "light yellow big horizontal.png")
        lower_right_block.init_position(self.width*.25, self.height*.75)

        self.obj_group.add(upper_left_block, upper_right_block, lower_left_block, lower_right_block)


    #vu -- start of enemies's patrol routes for area3_6
    # formation from area3_5 to area3_6
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route3(list(self.e_group)[2]) #Enemy3

    # formation from area3_7 to area3_6
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route3(list(self.e_group)[2]) #Enemy3


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.65, self.height*.25)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 15), ("look_west", 10), ("wait", 10), ("look_north", 15),
                                  ("look_east", 15), ("look_south", 5), ("wait", 10), ("end", 0)]
    
    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.35, self.height*.50)
            enemy._looking_east = True
            enemy.patrol_route = [("go_east", 40), ("look_west", 10), ("look_south", 10),
                                  ("look_north", 15), ("wait", 10), ("look_east", 15), ("go_west", 40),
                                  ("look_south", 15), ("look_east", 15), ("look_north", 10),
                                  ("wait", 10), ("look_west", 15), ("end", 0)]

    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.14, self.height*.50)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 15), ("look_west", 10), ("wait", 10), ("look_south", 15),
                                  ("look_east", 15), ("look_south", 7), ("look_east", 5), ("wait", 10), ("end", 0)]

    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.50, self.height*.60)
            enemy._looking_north = True
            enemy.patrol_route = [("go_north", 20), ("look_west", 10), ("look_south", 10),
                                  ("look_north", 15), ("go_south", 20), ("look_north", 15),
                                  ("look_east", 15), ("look_west", 10), ("go_south", 10),
                                  ("look_north", 15), ("look_east", 15), ("look_north", 10),
                                  ("look_west", 15), ("wait", 10), ("look_west", 15), ("end", 0)]
            
    #vu -- end of enemies's patrol routes for area3_6


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.03, self.height*0.75), (self.width*0.23, self.height*0.75), self.inner_door_thickness) #left inner door
        pygame.draw.line(window, BLACK, (self.width*0.40, self.height*0.75), (self.width*0.60, self.height*0.75), self.inner_door_thickness) #middle inner door
        pygame.draw.line(window, WOODEN, (self.width*0.85, self.height*0.25), (self.width*0.85, self.height*0.45), self.inner_door_thickness) #right inner door

        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.50
                and self.player_obj.rect.centerx <= self.width*0.85 and self.player_obj.moving_north):
                print("in 3_5")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation2()

            elif (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.30
                and self.player_obj.rect.centery <= self.height*0.75 and self.player_obj.moving_west):
                print("in 3_7")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()

            elif (self.player_obj.rect.bottomleft[1] >= self.height*0.745 and self.player_obj.rect.bottomleft[0] >= self.width*0.395
                  and self.player_obj.rect.bottomright[0] <= self.width*0.605 and self.player_obj.moving_south):
                print("in 3_6_middle_inner_entrance")
                new_area = self._make_transition(self.width*0.50, 40, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()
            '''
            elif (self.player_obj.rect.topright[0] >= self.width*0.85 and self.player_obj.rect.centery >= self.height*0.25
                  and self.player_obj.rect.centery <= self.height*0.45 and self.player_obj.moving_east):
                print("in 3_6_right_inner_area")
                new_area = self._make_transition(40, self.height*0.50, area_dict, "inner2")
                new_area._reset_enemy_state()
                new_area._formation1()
            '''

            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_6_MiddleInnerArea(area_base.Area):
    '''A class to represent a middle inner Area of Area3_6'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_6_MiddleInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_south_inner_room()

        banana = BananaPeelPickUp()
        banana.init_position(self.width/2, self.height/2)
        self.obj_group.add(banana)
        

    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)

        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.35
                and self.player_obj.rect.centerx <= self.width*0.65 and self.player_obj.moving_north):
                print("in 3_6")
                new_area = self._make_transition(self.width*0.50, self.height*0.75-70, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_6_RightInnerArea(area_base.Area):
    '''A class to represent a right inner Area of Area3_6'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_3_RightInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_safe_haven = True
        self.is_checkpoint = False
        self._draw_east_inner_room()

        
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass

        
    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)

        window.blit(pygame.font.SysFont("Arial", 50).render("Spotted?", 1, BLACK), (self.width*0.45, self.height*0.45))
        window.blit(pygame.font.SysFont("Arial", 50).render("Wait for the *ding*!", 1, BLACK), (self.width*0.37, self.height*0.50))

    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        #print("Snake's Health: ", self.player_obj.health)
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.35
                and self.player_obj.rect.centery <= self.height*0.65 and self.player_obj.moving_west):
                print("in 3_6")
                new_area = self._make_transition(self.width*0.85-50, self.height*0.35, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation2()

                
            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area
    

class Area3_7(area_base.Area):
    '''A class to represent Area3_7 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_7 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_left_block = Block(DARK_TEAL, self.width*0.33, self.height*0.30, "dark teal small semi horizontal.png")
        upper_left_block.init_position(0,0)

        upper_middle_block = Block(LIGHT_YELLOW, self.width*0.57, self.height*0.30, "light yellow big horizontal.png")
        upper_middle_block.init_position(self.width*0.33, 0)

        upper_right_block = Block(LIGHT_YELLOW, self.width*0.10, self.height*0.30, "light yellow small semi vertical.png")
        upper_right_block.init_position(self.width*0.90, 0)

        lower_left_block = Block(LIGHT_YELLOW, self.width*0.33, self.height*0.25, "light yellow small semi horizontal.png")
        lower_left_block.init_position(0, self.height*0.75)

        lower_middle_block = Block(LIGHT_YELLOW, self.width*0.33, self.height*0.25, "light yellow small semi horizontal.png")
        lower_middle_block.init_position(self.width*0.33, self.height*0.75)

        lower_right_block = Block(LIGHT_YELLOW, self.width*0.34, self.height*0.25, "light yellow small semi horizontal.png")
        lower_right_block.init_position(self.width*0.66, self.height*0.75)

        self.obj_group.add(upper_left_block, upper_middle_block, upper_right_block, lower_left_block, lower_middle_block, lower_right_block)


    #vu -- start of enemies's patrol routes
    # formation from area3_6 to area3_7
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route3(list(self.e_group)[2]) #Enemy3

    # formation from area3_8 to area3_7
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route4(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route5(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route6(list(self.e_group)[2]) #Enemy3

    # from upper left inner
    def _formation3(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route7(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route3(list(self.e_group)[2]) #Enemy3


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.30, self.height*.50)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 15), ("look_west", 10), ("wait", 10), ("look_north", 15),
                                  ("look_east", 15), ("look_south", 5), ("wait", 10), ("end", 0)]
    
    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.80, self.height*.50)
            enemy._looking_west = True
            enemy.patrol_route = [("go_west", 30), ("look_west", 10), ("look_south", 10),
                                  ("look_north", 15), ("wait", 10), ("look_east", 15), ("go_east", 30),
                                  ("look_south", 15), ("look_east", 15), ("look_north", 10),
                                  ("wait", 10), ("look_west", 15), ("end", 0)]
            
    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.45, self.height*.63)
            enemy._looking_north = True
            enemy.patrol_route = [("go_north", 30), ("look_west", 10), ("look_south", 10),
                                  ("look_north", 15), ("wait", 10), ("look_east", 15), ("go_south", 30),
                                  ("look_south", 15), ("look_east", 15), ("look_north", 10),
                                  ("wait", 10), ("look_west", 15), ("end", 0)]

    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.15, self.height*.50)
            enemy._looking_east = True
            enemy.patrol_route = [("go_east", 30), ("look_west", 10), ("look_south", 10),
                                  ("look_north", 15), ("wait", 10), ("look_east", 15), ("go_west", 30),
                                  ("look_south", 15), ("look_east", 15), ("look_north", 10),
                                  ("wait", 10), ("look_west", 15), ("end", 0)]
    
    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.80, self.height*.50)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 15), ("look_west", 10), ("wait", 10), ("look_north", 15),
                                  ("look_south", 15), ("look_south", 5), ("wait", 10), ("end", 0)]
            
    def gen_patrol_route6(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.65, self.height*.63)
            enemy._looking_north = True
            enemy.patrol_route = [("go_north", 30), ("look_west", 10), ("look_south", 10),
                                  ("look_north", 15), ("wait", 10), ("look_east", 15), ("go_south", 30),
                                  ("look_south", 15), ("look_east", 15), ("look_north", 10),
                                  ("wait", 10), ("look_west", 15), ("end", 0)]

    def gen_patrol_route7(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.80, self.height*.50)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 15), ("look_east", 25), ("end", 0)]
    #vu -- end of enemies's patrol routes


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, PINK, (self.width*0.07, self.height*0.30), (self.width*0.27, self.height*0.30), self.inner_door_thickness) #upper left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.45, self.height*0.30), (self.width*0.65, self.height*0.30), self.inner_door_thickness) #upper right inner door
        pygame.draw.line(window, WOODEN, (self.width*0.07, self.height*0.75), (self.width*0.27, self.height*0.75), self.inner_door_thickness) #lower left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.40, self.height*0.75), (self.width*0.60, self.height*0.75), self.inner_door_thickness) #lower middle inner door
        pygame.draw.line(window, WOODEN, (self.width*0.73, self.height*0.75), (self.width*0.93, self.height*0.75), self.inner_door_thickness) #lower right inner door
        
       
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.30
                  and self.player_obj.rect.centery <= self.height*0.75 and self.player_obj.moving_east):
                print("in 3_6")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation2()


            elif (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.30
                and self.player_obj.rect.centery <= self.height*0.75 and self.player_obj.moving_west):
                print("in 3_8")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery+self.height*0.23, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.y <= self.height*0.30 and self.player_obj.rect.x >= self.width*0.065
                and self.player_obj.rect.topright[0] <= self.width*0.275 and self.player_obj.moving_north):
                print("in 3_7_upper_left_inner_entrance")
                new_area = self._make_transition(self.width*0.50, self.height-40, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()
    

            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_7_UpperLeftInnerArea(area_base.Area):
    '''A class that represents the upper left inner Area of Area3_7.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_7_UpperLeftInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_safe_haven = True
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_north_inner_room()
        

    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)

        window.blit(pygame.font.SysFont("Arial", 50).render("Spotted?", 1, BLACK), (self.width*0.45, self.height*0.45))
        window.blit(pygame.font.SysFont("Arial", 50).render("Wait for the *ding*!", 1, BLACK), (self.width*0.37, self.height*0.50))        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.bottomright[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.35
                  and self.player_obj.rect.centerx <= self.width*0.65 and self.player_obj.moving_south):
                print("in 3_7")
                new_area = self._make_transition(self.width*0.17, self.height*0.30+70, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation3()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_8(area_base.Area):
    '''A class to represent Area3_8 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_8 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        left_block = Block(LIGHT_YELLOW, self.width*0.40, self.height*0.53, "light yellow medium square.png")
        left_block.init_position(0,0)

        right_block = Block(DARK_TEAL, self.width*0.30, self.height*0.53, "dark teal small semi vertical.png")
        right_block.init_position(self.width*0.70, 0)

        top_hallway_end = Block(LIGHT_YELLOW, self.width*0.30, self.height*0.05, "light yellow horizontal wall.png")
        top_hallway_end.init_position(self.width*0.40, 0)

        left_hallway_end = Block(LIGHT_YELLOW, self.width*0.05, self.height*0.45, "light yellow vertical wall.png")
        left_hallway_end.init_position(0, self.height*0.53)

        bottom_wall = Block(LIGHT_YELLOW, self.width, self.height*0.02, "light yellow horizontal wall.png")
        bottom_wall.init_position(0, self.height*0.98)

        self.obj_group.add(left_block, right_block, top_hallway_end, left_hallway_end, bottom_wall)
        

    #vu -- start of enemies' patrol routes area3_8
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route3(list(self.e_group)[2]) #Enemy3
            self.gen_patrol_route4(list(self.e_group)[3]) #Enemy4
            #self.gen_patrol_route5(list(self.e_group)[4]) #Enemy5

    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.47, self.height*.45)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 10), ("look_south", 20), ("end", 0)]
            
            
    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.75, self.height*.62)
            enemy.patrol_speed = 6
            enemy._looking_south = True
            enemy.patrol_route = [("go_south", 35), ("wait", 15), ("go_north", 35),
                                  ("look_south", 15), ("end", 0)]

            
    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.40, self.height*.90)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 30), ("look_east", 30), ("end", 0)]

    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.10, self.height*.62)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 50), ("look_east", 10), ("end", 0)]

    #vu -- end of enemies' patrol routes area3_8
            

    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, YELLOW, (self.width*0.45, self.height*0.05), (self.width*0.65, self.height*0.05), self.inner_door_thickness) #upper inner door
        pygame.draw.line(window, WOODEN, (self.width*0.40, self.height*0.20), (self.width*0.40, self.height*0.40), self.inner_door_thickness) #left inner door
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.53
                  and self.player_obj.rect.centery <= self.height*0.98 and self.player_obj.moving_east):
                print("in 3_7")
                new_area = self._make_transition(40, self.player_obj.rect.centery-self.height*0.229, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation2()
                
            elif (self.player_obj.rect.y <= self.height*0.05 and self.player_obj.rect.x >= self.width*0.445
                and self.player_obj.rect.topright[0] <= self.width*0.655 and self.player_obj.moving_north):
                print("in 3_8_thornton_boss_area")
                new_area = self._make_transition(self.width*0.50, self.height-40, area_dict, "inner2")
                '''
                if not new_area.boss.is_subdued:
                    new_area.boss.health = 300 #set the boss' health to 100 each time snake goes in the area as long as it exists
                '''
            '''
            elif (self.player_obj.rect.x <= self.width*0.40 and self.player_obj.rect.y >= self.height*0.195
                and self.player_obj.rect.bottomleft[1] <= self.height*0.405 and self.player_obj.moving_west):
                print("in 3_8_left_inner_entrance")
                new_area = self._make_transition(self.width-40, self.height*0.50, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()
            '''
                
            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_8_LeftInnerArea(area_base.Area):
    '''A class that represents the left inner Area of Area3_8.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_8_LeftInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False
        self._draw_west_inner_room()

        
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass

        
    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
                     

    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        #print("Snake's Health: ", self.player_obj.health)
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.35
                  and self.player_obj.rect.centery <= self.height*0.65 and self.player_obj.moving_east):
                print("in 3_8")
                new_area = self._make_transition(self.width*0.40+40, self.height*0.30, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()

                
            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_8_ThorntonBossArea(area_base.Area):
    '''A class that represents the Area for Thornton's boss battle from Area3_8.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_8_UpperInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        for enemy in list(enemies):
            if type(enemy) == thornton.Thornton:
                enemy.init_position(window_width/2, window_height*0.10)
            else: #Else, the enemy must be Boo
                enemy.init_position(window_width/4, window_height/4)


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "yellow_background.png")
        self.obj_group.draw(window)

        pygame.draw.line(window, BLACK, (self.width*0.40, self.height*0.995), (self.width*0.60, self.height*0.995), 10) #South door
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.bottomright[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.35
                  and self.player_obj.rect.centerx <= self.width*0.65 and self.player_obj.moving_south):
                print("in 3_8")
                new_area = self._make_transition(self.width*0.55, self.height*0.05+70, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_9(area_base.Area):
    '''A class to represent Area3_9 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_9 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_left_block = Block(LIGHT_YELLOW, self.width*0.40, self.height*0.20, "light yellow small semi horizontal.png")
        upper_left_block.init_position(0,0)

        middle_left_block = Block(LIGHT_YELLOW, self.width*0.40, self.height*0.50, "light yellow big semi vertical.png")
        middle_left_block.init_position(0, self.height*0.20)

        lower_left_block = Block(LIGHT_YELLOW, self.width*0.40, self.height*0.30, "light yellow small semi horizontal.png")
        lower_left_block.init_position(0, self.height*0.70)

        right_block = Block(LIGHT_YELLOW, self.width*0.25, self.height, "light yellow big vertical.png")
        right_block.init_position(self.width*0.75, 0)

        self.obj_group.add(upper_left_block, middle_left_block, lower_left_block, right_block)


    #vu -- start of enemies's patrol routes for area3_9
    # formation from 3_12 to 3_9
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2

    # formation from 3_3 to 3_9
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.58, self.height*.25)
            enemy._looking_south = True
            enemy.patrol_route = [("go_south", 40), ("look_west", 10), ("look_east", 10),
                                  ("look_north", 15), ("wait", 10), ("look_south", 15), ("go_north", 40),
                                   ("look_north", 15), ("look_east", 15), ("wait", 10),
                                  ("look_west", 15), ("look_south", 15), ("end", 0)]

    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.58, self.height*.80)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 10), ("wait", 10), ("look_east", 10),
                                  ("look_west", 10), ("wait", 10), ("end", 0)]
    

    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.58, self.height*.70)
            enemy._looking_north = True
            enemy.patrol_route = [("go_north", 40), ("look_west", 10), ("look_east", 10),
                                  ("look_north", 15), ("wait", 10), ("look_south", 15), ("go_south", 40),
                                  ("look_north", 15), ("look_east", 15), ("wait", 10), ("look_west", 15),
                                  ("look_south", 10), ("end", 0)]

    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.58, self.height*.20)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 10), ("wait", 10), ("look_east", 10), ("wait", 10), ("look_south", 10),
                                  ("look_west", 10), ("wait", 10), ("end", 0)]

    #vu -- end of enemies's patrol routes for area3_9


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.40, self.height*0.35), (self.width*0.40, self.height*0.55), self.inner_door_thickness) #upper left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.40, self.height*0.75), (self.width*0.40, self.height*0.95), self.inner_door_thickness) #lower left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.75, self.height*0.25), (self.width*0.75, self.height*0.45), self.inner_door_thickness) #upper right inner door
        pygame.draw.line(window, WOODEN, (self.width*0.75, self.height*0.60), (self.width*0.75, self.height*0.80), self.inner_door_thickness) #lower right inner door
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.40
                and self.player_obj.rect.centerx <= self.width*0.75 and self.player_obj.moving_north):
                print("in 3_12")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()

                
            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.40
                  and self.player_obj.rect.centerx <= self.width*0.75 and self.player_obj.moving_south):
                print("in 3_3")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation2()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area

    
class Area3_10(area_base.Area):
    '''A class to represent Area3_10 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_10 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_block = Block(DARK_TEAL, self.width*0.45, self.height*0.30, "dark teal big semi horizontal.png")
        upper_block.init_position(self.width*0.55, 0)

        middle_block = Block(DARK_TEAL, self.width*0.80, self.height*0.20, "dark teal big horizontal.png")
        middle_block.init_position(self.width*0.20, self.height*0.30)

        upper_left_wall = Block(BRICK, self.width*0.02, self.height*0.40, "brick vertical wall.png")
        upper_left_wall.init_position(0, 0)

        lower_left_wall = Block(BRICK, self.width*0.02, self.height*0.25, "brick vertical wall.png")
        lower_left_wall.init_position(0, self.height*0.75)

        right_wall = Block(LIGHT_YELLOW, self.width*0.02, self.height*0.50, "light yellow vertical wall.png")
        right_wall.init_position(self.width*0.98, self.height*0.50)

        self.obj_group.add(upper_block, middle_block, upper_left_wall, lower_left_wall, right_wall)

        #AREA3_10 PHYSICAL OBJECTS
        green_sofa = physical_objs.GreenSofa("south")
        green_sofa.init_position(self.width*0.50, self.height*0.50)
        self.obj_group.add(green_sofa)

        round_seat1 = physical_objs.RoundSeat()
        round_seat1.init_position(self.width*0.43, self.height*0.50)

        round_seat2 = physical_objs.RoundSeat()
        round_seat2.init_position(self.width*0.69, self.height*0.50)

        self.obj_group.add(round_seat1, round_seat2)

        red_sofa_chair = physical_objs.RedSofaChair("south")
        red_sofa_chair.init_position(self.width*0.86, self.height*0.52)
        self.obj_group.add(red_sofa_chair)

        '''
        square_table = physical_objs.SmallSquareTable()
        square_table.init_position(self.width*0.875, self.height*0.65)
        self.obj_group.add(square_table)
        '''

        round_seat = physical_objs.RoundSeat()
        round_seat.init_position(self.width*0.885, self.height*0.65)
        self.obj_group.add(round_seat)

    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.558, self.height*.70)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 15), ("look_south", 25), ("end", 0)]

    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.64, self.height*.70)
            enemy._looking_west = True
            enemy.patrol_route = [("look_west", 15), ("look_south", 25), ("end", 0)]

    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "peach background.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, PINK, (self.width*0.30, self.height*0.30), (self.width*0.50, self.height*0.30), self.inner_door_thickness) #door to girls' bathroom
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.40
                and self.player_obj.rect.centery <= self.height*0.75 and self.player_obj.moving_west):
                print("in 3_11")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.02
                and self.player_obj.rect.centerx <= self.width*0.55 and self.player_obj.moving_north):
                print("in 3_13")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation3()


            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.02
                  and self.player_obj.rect.centerx <= self.width*0.98 and self.player_obj.moving_south):
                print("in 3_2")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.bottomleft[1] >= self.height*0.30 and self.player_obj.rect.bottomleft[1] <= self.height*0.50 and self.player_obj.rect.bottomleft[0] >= self.width*0.295
                  and self.player_obj.rect.bottomright[0] <= self.width*0.555 and self.player_obj.moving_south):
                print("in 3_10_girls_bathroom")
                new_area = self._make_transition(self.width*0.35, self.height*0.25+70, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_10_GirlsBathroom(area_base.Area):
    '''A class to represent the girl's bathroom adjacent to Area3_10'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_10_GirlsBathroom object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_safe_haven = True
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_girls_bathroom()
        

    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)

        window.blit(pygame.font.SysFont("Arial", 50).render("Spotted?", 1, BLACK), (self.width*0.45, self.height*0.55))
        window.blit(pygame.font.SysFont("Arial", 50).render("Wait for the *ding*!", 1, BLACK), (self.width*0.37, self.height*0.60))        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.y <= self.height*0.25 and self.player_obj.rect.centerx >= self.width*0.25
                and self.player_obj.rect.centerx <= self.width*0.45 and self.player_obj.moving_north):
                print("in 3_10")
                new_area = self._make_transition(self.width*0.40, self.height*0.30-70, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_11(area_base.Area):
    '''A class to represent Area3_11 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_11 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_block = Block(LIGHT_YELLOW, self.width, self.height*0.40, "light yellow big semi horizontal.png")
        upper_block.init_position(0,0)

        left_block = Block(GREENISH_GRAY, self.width*0.25, self.height*0.60, "greenish gray small semi vertical.png")
        left_block.init_position(0, self.height*0.40)

        right_block = Block(LIGHT_YELLOW, self.width*0.15, self.height*0.25, "light yellow small vertical.png")
        right_block.init_position(self.width*0.85, self.height*0.75)

        elevator = Block(LIGHT_GRAY, self.width*0.60, self.height*0.25)
        elevator.init_position(self.width*0.25, self.height*0.75)

        self.obj_group.add(upper_block, left_block, right_block, elevator)


    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "peach background.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, BLACK, (self.width*0.55, self.height*0.75), (self.width*0.55, self.height), 10) #elevator division

        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.40
                  and self.player_obj.rect.centery <= self.height*0.75 and self.player_obj.moving_east):
                print("in 3_10")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()
            elif (self.player_obj.rect.bottomright[1] >= self.height*0.74 and self.player_obj.rect.centerx >= self.width*0.25
                  and self.player_obj.rect.centerx <= self.width*0.50 and self.player_obj.moving_south):
                if self.player_obj.has_elevator_card_key:
                    print("in 1_5")
                    new_area = self._make_transition(self.width*0.15, self.player_obj.rect.centery-60, area_dict, "inner1")
                    elevator_hum = pygame.mixer.Sound("elevator_hum.wav")
                    pygame.mixer.Sound.play(elevator_hum)
                    self.player_obj.facing_north = True
                    new_area._reset_enemy_state()
                    new_area._formation4()
                else:
                    if not pygame.mixer.get_busy():
                        denied = pygame.mixer.Sound("denied.wav")
                        pygame.mixer.Sound.play(denied)
            elif (self.player_obj.rect.bottomright[1] >= self.height*0.74 and self.player_obj.rect.centerx >= self.width*0.50
                  and self.player_obj.rect.centerx <= self.width*0.85 and self.player_obj.moving_south):
                if self.player_obj.has_elevator_card_key:
                    print("in 1_5")
                    new_area = self._make_transition(self.width*0.38, self.player_obj.rect.centery-60, area_dict, "inner2")
                    elevator_hum = pygame.mixer.Sound("elevator_hum.wav")
                    pygame.mixer.Sound.play(elevator_hum)
                    self.player_obj.facing_north = True
                    new_area._reset_enemy_state()
                    new_area._formation4()
                else:
                    if not pygame.mixer.get_busy():
                        denied = pygame.mixer.Sound("denied.wav")
                        pygame.mixer.Sound.play(denied)

            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_12(area_base.Area):
    '''A class to represent Area3_12 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_12 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_left_block = Block(LIGHT_YELLOW, self.width*0.25, self.height*0.15, "light yellow small semi horizontal.png")
        upper_left_block.init_position(0, 0)

        upper_middle_block = Block(LIGHT_YELLOW, self.width*0.25, self.height*0.15, "light yellow small semi horizontal.png")
        upper_middle_block.init_position(self.width*0.25, 0)

        upper_right_block = Block(LIGHT_YELLOW, self.width*0.50, self.height*0.15, "light yellow big horizontal.png")
        upper_right_block.init_position(self.width*0.50, 0)

        lower_left_block = Block(LIGHT_YELLOW, self.width*0.40, self.height*0.45, "light yellow medium square.png")
        lower_left_block.init_position(0, self.height*0.55)

        lower_right_block = Block(LIGHT_YELLOW, self.width*0.25, self.height*0.85, "light yellow big semi vertical.png")
        lower_right_block.init_position(self.width*0.75, self.height*0.15)

        self.obj_group.add(upper_left_block, upper_middle_block, upper_right_block, lower_left_block, lower_right_block)


    def _formation1(self):
        if self.e_group != None:
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.30, self.height*.30)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 20), ("look_east", 20), ("end", 0)]


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.60, self.height*.60)
            enemy._looking_west = True
            enemy.patrol_route = [("look_west", 15), ("look_north", 20), ("end", 0)]


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.03, self.height*0.15), (self.width*0.23, self.height*0.15), self.inner_door_thickness) #upper left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.28, self.height*0.15), (self.width*0.48, self.height*0.15), self.inner_door_thickness) #upper middle inner door
        pygame.draw.line(window, WOODEN, (self.width*0.53, self.height*0.15), (self.width*0.73, self.height*0.15), self.inner_door_thickness) #upper right inner door
        pygame.draw.line(window, WOODEN, (self.width*0.40, self.height*0.65), (self.width*0.40, self.height*0.85), self.inner_door_thickness) #lower left inner door
        pygame.draw.line(window, BLACK, (self.width*0.75, self.height*0.35), (self.width*0.75, self.height*0.55), self.inner_door_thickness) #lower right inner door

        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.15
                and self.player_obj.rect.centery <= self.height*0.55 and self.player_obj.moving_west):
                print("in 3_13")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation2()


            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.40
                  and self.player_obj.rect.centerx <= self.width*0.75 and self.player_obj.moving_south):
                print("in 3_9")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.topright[0] >= self.width*0.75 and self.player_obj.rect.centery >= self.height*0.35
                  and self.player_obj.rect.centery <= self.height*0.55 and self.player_obj.moving_east):
                print("in 3_13_right_inner_entrance")
                new_area = self._make_transition(40, self.height*0.50, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_13_RightInnerArea(area_base.Area):
    '''A class that represents the right inner Area of Area3_12.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_13_RightInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False
        self._draw_east_inner_room()

        rb = RubberBandPickUp()
        rb.init_position(self.width/2-100, self.height/2)
        self.obj_group.add(rb)

        straw = StrawPickUp()
        straw.init_position(self.width/2+100, self.height/2)
        self.obj_group.add(straw)

        
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass

        
    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
                      

    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        #print("Snake's Health: ", self.player_obj.health)
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.35
                and self.player_obj.rect.centery <= self.height*0.65 and self.player_obj.moving_west):
                print("in 3_12")
                new_area = self._make_transition(self.width*0.75-40, self.height*0.45, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()

                
            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_13(area_base.Area):
    '''A class to represent Area3_13 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_13 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_left_block = Block(LIGHT_YELLOW, self.width*0.33, self.height*0.15, "light yellow small semi horizontal.png")
        upper_left_block.init_position(0, 0)

        upper_middle_block = Block(LIGHT_YELLOW, self.width*0.33, self.height*0.15, "light yellow small semi horizontal.png")
        upper_middle_block.init_position(self.width*0.33, 0)

        upper_right_block = Block(LIGHT_YELLOW, self.width*0.34, self.height*0.15, "light yellow small semi horizontal.png")
        upper_right_block.init_position(self.width*0.66, 0)

        middle_block = Block(LIGHT_YELLOW, self.width*0.80, self.height*0.15, "light yellow big horizontal.png")
        middle_block.init_position(self.width*0.20, self.height*0.55)

        lower_block = Block(DARK_TEAL, self.width*0.45, self.height*0.30, "dark teal big semi horizontal.png")
        lower_block.init_position(self.width*0.55, self.height*0.70)

        left_wall = Block(BRICK, self.width*0.02, self.height*0.45, "brick vertical wall.png")
        left_wall.init_position(0, self.height*0.55)

        self.obj_group.add(upper_left_block, upper_middle_block, upper_right_block, middle_block, lower_block, left_wall)
        

    ### Vu formation & patrol route area3_13 zaza
    #formation from 3_14
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route5(list(self.e_group)[2]) #Enemy3


    #formation from 3_12
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route2(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route3(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route6(list(self.e_group)[2]) #Enemy3
            

    #formation from 3_10
    def _formation3(self):
        if self.e_group != None:
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route3(list(self.e_group)[1]) #Enemy2 
            self.gen_patrol_route4(list(self.e_group)[2]) #Enemy3

    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?

    #Enemy #1 when Snake comes from area3_14, 3_10
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.9, self.height*.23)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 15), ("go_west", 30), ("look_south", 35), ("look_east", 35), ("go_west", 30), ("look_south", 35),
                                  ("go_east", 30), ("look_east", 25), ("go_east", 30), ("end", 0)]


    #Enemy #1 when Snake comes from area 3_12
    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.40, self.height*.23)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 15), ("go_east", 30), ("look_south", 25),
                                  ("go_west", 30), ("end", 0)]
            
    #Enemy #2 when Snake comes from area 3_14, 3_12, 3_10
    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.25, self.height*.45)
            enemy._looking_west = True
            enemy.patrol_route = [("go_west", 20), ("look_south", 20), ("go_east", 25),
                                  ("look_east", 20), ("end", 0)]

    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.80, self.height*.47)
            enemy._looking_west = True
            enemy.patrol_route = [("look_west", 25), ("look_east", 40), ("end", 0)]

    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.80, self.height*.47)
            enemy._looking_north = True
            #enemy.patrol_route = [("look_east", 40), ("look_west", 25), ("end", 0)]
            enemy.patrol_route = [("look_north", 25), ("look_east", 25), ("end", 0)]


    def gen_patrol_route6(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.80, self.height*.47)
            enemy._looking_west = True
            enemy.patrol_route = [("look_west", 25), ("look_east", 60), ("end", 0)]
            
    '''
    # Enemy #3 when Snake comes from 3_10
    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.3, self.height*.45)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 25), ("look_east", 25),
                                  ("go_east", 50), ("wait", 10), ("go_west", 50),
                                  ("look_north", 25), ("look_east", 25), ("end", 0)]
    '''

    '''
    # Enemy #3 when Snake comes from 3_12, 3_14
    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.15, self.height*.6)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 20), ("look_south", 25),
                                  ("go_south", 35), ("look_west", 50), ("go_north", 35),
                                  ("look_west", 25), ("look_south", 25), ("end", 0)]
    '''
    ### End Vu formation & patrol route area3_13


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)

        pygame.draw.line(window, BLACK, (self.width*0.30, self.height*0.70), (self.width*0.50, self.height*0.70), self.inner_door_thickness) #door to boys' bathroom
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.15
                  and self.player_obj.rect.centery <= self.height*0.55 and self.player_obj.moving_east):
                print("in 3_12")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.15
                and self.player_obj.rect.centery <= self.height*0.55 and self.player_obj.moving_west):
                print("in 3_14")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.02
                  and self.player_obj.rect.centerx <= self.width*0.55 and self.player_obj.moving_south):
                print("in 3_10")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.y <= self.height*0.70 and self.player_obj.rect.y >= self.height*0.55 and self.player_obj.rect.x >= self.width*0.295
                and self.player_obj.rect.topright[0] <= self.width*0.555 and self.player_obj.moving_north):
                print("in 3_13_boys_bathroom")
                new_area = self._make_transition(self.width*0.35, self.height*0.75-70, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_13_BoysBathroom(area_base.Area):
    '''A class to represent the boy's bathroom adjacent to Area3_13'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_13_BoysBathroom object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_boys_bathroom()
        
        wb = WaterBalloonPickUp()
        wb.init_position(self.width*0.50, self.height*0.40)
        self.obj_group.add(wb)

    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.bottomright[1] >= self.height*0.745 and self.player_obj.rect.centerx >= self.width*0.25
                  and self.player_obj.rect.centerx <= self.width*0.45 and self.player_obj.moving_south):
                print("in 3_13")
                new_area = self._make_transition(self.width*0.40, self.height*0.70+70, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation3()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_14(area_base.Area):
    '''A class to represent Area3_14 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_14 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_left_block = Block(LIGHT_YELLOW, self.width*0.33, self.height*0.15, "light yellow small semi horizontal.png")
        upper_left_block.init_position(0, 0)

        upper_middle_block = Block(LIGHT_YELLOW, self.width*0.33, self.height*0.15, "light yellow small semi horizontal.png")
        upper_middle_block.init_position(self.width*0.33, 0)

        upper_right_block = Block(LIGHT_YELLOW, self.width*0.34, self.height*0.15, "light yellow small semi horizontal.png")
        upper_right_block.init_position(self.width*0.66, 0)

        lower_right_block = Block(BRICK, self.width*0.40, self.height*0.45, "brick small square.png")
        lower_right_block.init_position(self.width*.60, self.height*.55)
        
        lower_left_block = Block(LIGHT_YELLOW, self.width*0.60, self.height*0.40, "light yellow big semi horizontal.png")
        lower_left_block.init_position(0, self.height*0.60)
        
        self.obj_group.add(upper_left_block, upper_middle_block, upper_right_block, lower_right_block, lower_left_block)


    ### Vu formation & patrol route area3_14
    # formation from area3_13
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route3(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route4(list(self.e_group)[2]) #Enemy3


    # formation from area3_15
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route2(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route3(list(self.e_group)[1]) #Enemy2        
            self.gen_patrol_route4(list(self.e_group)[2]) #Enemy3


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?

    # Enemy #1 when Snake comes from area3_13
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.1, self.height*.25)
            enemy._looking_south = True
            '''
            enemy.patrol_route = [("look_south", 15), ("go_east", 50), ("look_south", 10),
                                  ("go_east", 50), ("wait", 10), ("go_east", 50), ("look_south", 10),
                                  ("go_west", 50), ("wait", 10), ("go_west", 50), ("wait", 10),
                                  ("go_west", 50), ("wait", 10), ("end", 0)]
            '''
            enemy.patrol_route = [("look_south", 25), ("go_east", 50), ("look_south", 10),
                                  ("go_east", 50), ("look_east", 10), ("go_east", 50), ("look_south", 10),
                                  ("go_west", 50), ("look_west", 10), ("go_west", 50), ("look_west", 10),
                                  ("go_west", 50), ("look_west", 10), ("end", 0)]


    # Enemy #1 when Snake comes from area3_15
    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.9, self.height*.25)
            enemy._looking_south = True
            '''
            enemy.patrol_route = [("look_south", 15), ("go_west", 50), ("wait", 10),
                                  ("go_west", 50), ("wait", 10), ("go_west", 50), ("wait", 10),
                                  ("go_east", 50), ("wait", 10), ("go_east", 50), ("wait", 10),
                                  ("go_east", 50), ("wait", 10), ("end", 0)]
            '''
            enemy.patrol_route = [("look_south", 15), ("go_west", 50), ("look_west", 10),
                                  ("go_west", 50), ("look_west", 10), ("go_west", 50), ("look_south", 10),
                                  ("go_east", 50), ("look_east", 10), ("go_east", 50), ("look_east", 10),
                                  ("go_east", 50), ("look_east", 10), ("end", 0)]

    # Enemy #2 when Snake comes from area3_13
    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.4, self.height*.25)
            enemy._looking_north = True
            '''
            enemy.patrol_route = [("look_north", 20), ("look_west", 15),
                                  ("go_west", 50), ("wait", 10), ("look_south", 50),
                                  ("look_east", 50), ("go_east", 50), ("end", 0)]
            '''
            enemy.patrol_route = [("look_north", 20), ("look_west", 15),
                                  ("go_west", 50), ("look_west", 10), ("look_south", 20),
                                  ("look_east", 20), ("go_east", 50), ("end", 0)]

    # Enemy #3
    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.455, self.height*.52)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 15), ("look_west", 20),
                                  ("go_north", 35), ("wait", 10), ("look_south", 30),
                                  ("look_east", 25), ("go_south", 30), ("end", 0)]


    ### End Vu formation & patrol route area3_14


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.07, self.height*0.15), (self.width*0.27, self.height*0.15), self.inner_door_thickness) #upper left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.40, self.height*0.15), (self.width*0.60, self.height*0.15), self.inner_door_thickness) #upper middle inner door
        pygame.draw.line(window, WOODEN, (self.width*0.73, self.height*0.15), (self.width*0.93, self.height*0.15), self.inner_door_thickness) #upper right inner door
        pygame.draw.line(window, WOODEN, (self.width*0.20, self.height*0.60), (self.width*0.40, self.height*0.60), self.inner_door_thickness) #lower left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.70, self.height*0.55), (self.width*0.90, self.height*0.55), self.inner_door_thickness) #lower right inner door

                
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.15
                  and self.player_obj.rect.centery <= self.height*0.55 and self.player_obj.moving_east):
                print("in 3_13")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.15
                and self.player_obj.rect.centery <= self.height*0.60 and self.player_obj.moving_west):
                print("in 3_15")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation2()

            '''
            elif (self.player_obj.rect.y <= self.height*0.15 and self.player_obj.rect.x >= self.width*0.395
                and self.player_obj.rect.topright[0] <= self.width*0.605 and self.player_obj.moving_north):
                print("in 3_14_upper_middle_inner_entrance")
                new_area = self._make_transition(self.width*0.50, self.height-40, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()
            '''

            '''
            elif (self.player_obj.rect.bottomleft[1] >= self.height*0.545 and self.player_obj.rect.bottomleft[0] >= self.width*0.695
                  and self.player_obj.rect.bottomright[0] <= self.width*0.905 and self.player_obj.moving_south):
                print("in 3_14_lower_right_inner_entrance")
                new_area = self._make_transition(self.width*0.50, 40, area_dict, "inner2")
                new_area._reset_enemy_state()
                new_area._formation1()
            '''

            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_14_UpperMiddleInnerArea(area_base.Area):
    '''A class that represents the upper middle inner Area of Area3_14.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_14_UpperMiddleInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_north_inner_room()
        

    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.bottomright[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.35
                  and self.player_obj.rect.centerx <= self.width*0.65 and self.player_obj.moving_south):
                print("in 3_14")
                new_area = self._make_transition(self.width*0.50, self.height*0.15+70, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_14_LowerRightInnerArea(area_base.Area):
    '''A class that represents the lower right inner Area of Area3_14.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_14_LowerRightInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_south_inner_room()
        

    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)

                
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.35
                and self.player_obj.rect.centerx <= self.width*0.65 and self.player_obj.moving_north):
                print("in 3_14")
                new_area = self._make_transition(self.width*0.80, self.height*0.55-70, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_15(area_base.Area):
    '''A class to represent Area3_15 of DBH.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_15 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_left_block = Block(LIGHT_YELLOW, self.width*0.33, self.height*0.15, "light yellow small semi horizontal.png")
        upper_left_block.init_position(0, 0)

        upper_middle_block = Block(LIGHT_YELLOW, self.width*0.33, self.height*0.15, "light yellow small semi horizontal.png")
        upper_middle_block.init_position(self.width*0.33, 0)

        upper_right_block = Block(LIGHT_YELLOW, self.width*0.34, self.height*0.15, "light yellow small semi horizontal.png")
        upper_right_block.init_position(self.width*0.66, 0)

        lower_right_block = Block(LIGHT_YELLOW, self.width*0.35, self.height*0.40, "light yellow medium square.png")
        lower_right_block.init_position(self.width*0.65, self.height*0.60)
        
        lower_left_block = Block(LIGHT_YELLOW, self.width*0.35, self.height*0.45, "light yellow medium square.png")
        lower_left_block.init_position(self.width*0.30, self.height*0.55)

        left_wall = Block(LIGHT_YELLOW, self.width*0.02, self.height*0.45, "light yellow vertical wall.png")
        left_wall.init_position(0, self.height*0.55)
        
        self.obj_group.add(upper_left_block, upper_middle_block, upper_right_block, lower_right_block, lower_left_block, left_wall)


    ### Vu formation & patrol route area3_15
    # formation from area3_17, 3_16
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route5(list(self.e_group)[2]) #Enemy3

    # formation from area3_14
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route2(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route3(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route5(list(self.e_group)[2]) #Enemy3

    def _formation3(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route6(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route5(list(self.e_group)[2]) #Enemy3


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?

    # Enemy #1 when Snake comes from area3_17, 3_16
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.25, self.height*.25)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 25), ("look_south", 25), ("end", 0)]


    # Enemy #1 when Snake comes from area3_14
    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.50, self.height*.3)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 15), ("look_south", 10), ("go_east", 50), ("wait", 10), ("look_south", 20),
                                  ("go_west", 50), ("end", 0)]
            
    #Enemy #2 when Snake comes from area3_14
    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.30, self.height*.4)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 20), ("look_west", 15), ("end", 0)]
            

    #Enemy #2 when Snake comes from area3_17, 3_16
    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.80, self.height*.45)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 20), ("look_east", 20), ("end", 0)]

    
    #Enemy #3 when Snake comes from area3_16
    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.15, self.height*.6)
            enemy._looking_west = True
            enemy.patrol_route = [("look_west", 20), ("look_north", 20), ("look_east", 20), ("end", 0)]


    def gen_patrol_route6(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.80, self.height*.25)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 20), ("look_east", 20), ("end", 0)]

    
    ### End Vu formation & patrol route area3_15


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)

        pygame.draw.line(window, WOODEN, (self.width*0.07, self.height*0.15), (self.width*0.27, self.height*0.15), self.inner_door_thickness) #upper left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.40, self.height*0.15), (self.width*0.60, self.height*0.15), self.inner_door_thickness) #upper middle inner door
        pygame.draw.line(window, WOODEN, (self.width*0.73, self.height*0.15), (self.width*0.93, self.height*0.15), self.inner_door_thickness) #upper right inner door
        pygame.draw.line(window, PINK, (self.width*0.35, self.height*0.55), (self.width*0.55, self.height*0.55), self.inner_door_thickness) #lower inner door
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.15
                  and self.player_obj.rect.centery <= self.height*0.60 and self.player_obj.moving_east):
                print("in 3_14")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation2()

                
            elif (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.15
                and self.player_obj.rect.centery <= self.height*0.55 and self.player_obj.moving_west):
                print("in 3_17")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.02
                  and self.player_obj.rect.centerx <= self.width*0.30 and self.player_obj.moving_south):
                print("in 3_16")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.bottomleft[1] >= self.height*0.545 and self.player_obj.rect.bottomleft[0] >= self.width*0.345
                  and self.player_obj.rect.bottomright[0] <= self.width*0.555 and self.player_obj.moving_south):
                print("in 3_15_lower_inner_entrance")
                new_area = self._make_transition(self.width*0.50, 40, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_15_LowerInnerArea(area_base.Area):
    '''A class that represents the lower inner Area of Area3_15.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_15_LowerInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_safe_haven = True
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_south_inner_room()
        

    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)

        window.blit(pygame.font.SysFont("Arial", 50).render("Spotted?", 1, BLACK), (self.width*0.45, self.height*0.45))
        window.blit(pygame.font.SysFont("Arial", 50).render("Wait for the *ding*!", 1, BLACK), (self.width*0.37, self.height*0.50))        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.35
                and self.player_obj.rect.centerx <= self.width*0.65 and self.player_obj.moving_north):
                print("in 3_15")
                new_area = self._make_transition(self.width*0.45, self.height*0.55-70, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation3()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_16(area_base.Area):
    '''A class to represent Area3_16 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_16 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        left_block = Block(LIGHT_YELLOW, self.width*0.30, self.height*0.50, "light yellow small semi vertical.png")
        left_block.init_position(0, self.height*0.50)

        right_block = Block(LIGHT_YELLOW, self.width*0.70, self.height, "light yellow big square.png")
        right_block.init_position(self.width*0.30, 0)

        left_wall = Block(LIGHT_YELLOW, self.width*0.02, self.height*0.50, "light yellow vertical wall.png")
        left_wall.init_position(0, 0)

        self.obj_group.add(left_block, right_block, left_wall)
        

    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, BLACK, (self.width*0.06, self.height*0.50), (self.width*0.26, self.height*0.50), self.inner_door_thickness) #inner door
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.02
                and self.player_obj.rect.centerx <= self.width*0.30 and self.player_obj.moving_north):
                print("in 3_15")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.bottomleft[1] >= self.height*0.50 and self.player_obj.rect.bottomleft[0] >= self.width*0.055
                  and self.player_obj.rect.bottomright[0] <= self.width*0.265 and self.player_obj.moving_south):
                print("in 3_16_inner_entrance")
                new_area = self._make_transition(self.width*0.50, 40, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_16_InnerArea(area_base.Area):
    '''A class that represents the inner Area of Area3_16.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_16_InnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_south_inner_room()

        straw = StrawPickUp()
        straw.init_position(self.width/2, self.height/2)
        self.obj_group.add(straw)

        
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.35
                and self.player_obj.rect.centerx <= self.width*0.65 and self.player_obj.moving_north):
                print("in 3_16")
                new_area = self._make_transition(self.width*0.16, self.height*0.50-70, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_17(area_base.Area):
    '''A class to represent Area3_17 of DBH.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_17 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_left_block = Block(LIGHT_YELLOW, self.width*0.33, self.height*0.15, "light yellow small semi horizontal.png")
        upper_left_block.init_position(0, 0)

        upper_middle_block = Block(LIGHT_YELLOW, self.width*0.33, self.height*0.15, "light yellow small semi horizontal.png")
        upper_middle_block.init_position(self.width*0.33, 0)

        upper_right_block = Block(LIGHT_YELLOW, self.width*0.34, self.height*0.15, "light yellow small semi horizontal.png")
        upper_right_block.init_position(self.width*0.66, 0)

        lower_right_block = Block(LIGHT_YELLOW, self.width*0.40, self.height*0.45, "light yellow medium square.png")
        lower_right_block.init_position(self.width*0.60, self.height*0.55)
        
        lower_left_block = Block(DARK_TEAL, self.width*0.60, self.height*0.10, "dark teal small horizontal.png")
        lower_left_block.init_position(0, self.height*0.90)

        left_wall = Block(DARK_TEAL, self.width*0.02, self.height*0.45, "dark teal vertical wall.png")
        left_wall.init_position(0, self.height*0.45)
        
        self.obj_group.add(upper_left_block, upper_middle_block, upper_right_block, lower_right_block, lower_left_block, left_wall)


    ### Vu formation & patrol route area3_17
    #formation from area3_15
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route3(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route4(list(self.e_group)[2]) #Enemy3

    #formation from area3_18
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route2(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route3(list(self.e_group)[1]) #Enemy2        
            self.gen_patrol_route4(list(self.e_group)[2]) #Enemy3


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?

    # Enemy #1 when Snake comes from area3_15
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.10, self.height*.25)
            enemy._looking_west = True
            enemy.patrol_route = [("look_west", 25), ("go_east", 60), ("look_south", 10),
                                  ("go_east", 50), ("look_east", 10), ("go_east", 50), ("wait", 10),
                                  ("go_west", 50), ("wait", 10), ("go_west", 50), ("look_north", 10),
                                  ("go_west", 50), ("wait", 10), ("end", 0)]

    # Enemy #1 when Snake comes from area3_18
    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.35, self.height*.23)
            enemy._looking_south = True
            '''
            enemy.patrol_route = [("look_north", 25), ("go_west", 50), ("look_north", 10),
                                  ("go_west", 50), ("look_east", 10), ("go_west", 50), ("wait", 10),
                                  ("go_east", 50), ("wait", 10), ("go_east", 50), ("look_north", 10),
                                  ("go_east", 50), ("wait", 10), ("end", 0)]
            '''
            enemy.patrol_route = [("look_south", 15), ("look_east", 35), ("end", 0)]


    # Enemy #2 when Snake comes from area3_18, 3_15
    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.55, self.height*.75)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 20), ("look_east", 20), ("look_north", 25),
                                  ("go_west", 40), ("look_north", 15), ("look_east", 20),
                                  ("go_east", 40), ("end", 0)]
    # Enemy #3
    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.15, self.height*.72)
            enemy._looking_west = True
            enemy.patrol_route = [("look_west", 30), ("look_north", 20),
                                  ("go_north", 20), ("look_south", 20), ("go_north", 40), ("look_east", 25),
                                  ("look_south", 15), ("go_south", 60), ("look_east", 25), ("end", 0)]


    ### End Vu formation & patrol route area3_17

    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.07, self.height*0.15), (self.width*0.27, self.height*0.15), self.inner_door_thickness) #upper left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.40, self.height*0.15), (self.width*0.60, self.height*0.15), self.inner_door_thickness) #upper middle inner door
        pygame.draw.line(window, WOODEN, (self.width*0.73, self.height*0.15), (self.width*0.93, self.height*0.15), self.inner_door_thickness) #upper right inner door
        pygame.draw.line(window, WOODEN, (self.width*0.20, self.height*0.90), (self.width*0.40, self.height*0.90), self.inner_door_thickness) #lower left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.70, self.height*0.55), (self.width*0.90, self.height*0.55), self.inner_door_thickness) #lower right inner door
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.15
                  and self.player_obj.rect.centery <= self.height*0.55 and self.player_obj.moving_east):
                print("in 3_15")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.15
                and self.player_obj.rect.centery <= self.height*0.45 and self.player_obj.moving_west):
                print("in 3_18")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery-self.height*0.129, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_18(area_base.Area):
    '''A class to represent Area3_18 of DBH.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_18 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_left_block = Block(LIGHT_YELLOW, self.width*0.25, self.height*0.45, "light yellow big vertical.png")
        upper_left_block.init_position(0, 0)

        middle_left_block = Block(LIGHT_YELLOW, self.width*0.25, self.height*0.35, "light yellow small semi vertical.png")
        middle_left_block.init_position(0, self.height*0.45)

        lower_left_block = Block(LIGHT_YELLOW, self.width*0.25, self.height*0.20, "light yellow small semi horizontal.png")
        lower_left_block.init_position(0, self.height*0.80)

        right_block = Block(GREENISH_GRAY, self.width*0.45, self.height*0.68, "greenish gray big semi vertical.png")
        right_block.init_position(self.width*0.55, self.height*0.32)

        upper_wall = Block(LIGHT_YELLOW, self.width*0.75, self.height*0.02, "light yellow horizontal wall.png")
        upper_wall.init_position(self.width*0.25, 0)

        self.obj_group.add(upper_left_block, middle_left_block, lower_left_block, right_block, upper_wall)
        

    ### Vu formation & patrol route area3_18
    # formation from area3_17
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route4(list(self.e_group)[2]) #Enemy3

    # formation from area3_19
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2        
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[2]) #Enemy3


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    # Enemy #1 when Snake comes from area3_17
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.44, self.height*.26)
            enemy._looking_south = True
            '''
            enemy.patrol_route = [("look_south", 25), ("go_east", 50), ("look_west", 25),
                                  ("go_east", 15), ("wait", 10), ("go_west", 10),
                                  ("look_south", 15), ("look_west", 15), ("go_west", 50), ("end", 0)]
            '''
            enemy.patrol_route = [("look_south", 25), ("go_west", 30), ("look_west", 25),
                                  ("go_east", 30), ("look_east", 15), ("end", 0)]


    # Enemy #2 when Snake comes from area3_17
    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.3, self.height*.52)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 25), ("go_south", 50), ("look_north", 10),
                                  ("look_north", 15), ("go_north", 50), ("end", 0)]

    # Enemy #1 when Snake comes from area3_19
    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.44, self.height*.23)
            '''
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 25), ("go_west", 30), ("look_north", 15),
                                  ("look_west", 25), ("go_east", 30), ("end", 0)]
            '''
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 25), ("go_west", 30), ("look_south", 25),
                                  ("go_east", 30), ("look_west", 10), ("end", 0)]

    # Enemy #3
    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.51, self.height*.75)
            enemy._looking_west = True
            enemy.patrol_route = [("look_west", 20), ("go_north", 20), ("look_east", 25),
                                  ("look_south", 15), ("go_south", 20), ("end", 0)]
    
    
    ### End Vu formation & patrol route area3_18



    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.25, self.height*0.15), (self.width*0.25, self.height*0.35), self.inner_door_thickness) #upper inner door
        pygame.draw.line(window, WOODEN, (self.width*0.25, self.height*0.53), (self.width*0.25, self.height*0.73), self.inner_door_thickness) #middle inner door
        pygame.draw.line(window, WOODEN, (self.width*0.25, self.height*0.80), (self.width*0.25, self.height), self.inner_door_thickness) #lower inner door
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.02
                  and self.player_obj.rect.centery <= self.height*0.32 and self.player_obj.moving_east):
                print("in 3_17")
                new_area = self._make_transition(40, self.player_obj.rect.centery+self.height*0.13, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation2()


            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.25
                  and self.player_obj.rect.centerx <= self.width*0.55 and self.player_obj.moving_south):
                print("in 3_19")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_19(area_base.Area):
    '''A class to represent Area3_19 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_19 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_left_block = Block(LIGHT_YELLOW, self.width*0.25, self.height*0.20, "light yellow small semi horizontal.png")
        upper_left_block.init_position(0, 0)

        middle_left_block = Block(LIGHT_YELLOW, self.width*0.25, self.height*0.40, "light yellow small semi vertical.png")
        middle_left_block.init_position(0, self.height*0.20)

        lower_left_block = Block(LIGHT_YELLOW, self.width*0.25, self.height*0.40, "light yellow small semi vertical.png")
        lower_left_block.init_position(0, self.height*0.60)

        upper_right_block = Block(LIGHT_YELLOW, self.width*0.45, self.height*0.36, "light yellow medium square.png")
        upper_right_block.init_position(self.width*0.55, 0)

        lower_right_block = Block(GREENISH_GRAY, self.width*0.45, self.height*0.30, "greenish gray small semi horizontal.png")
        lower_right_block.init_position(self.width*0.55, self.height*0.70)

        right_hallway_end = Block(LIGHT_YELLOW, self.width*0.05, self.height*0.34, "light yellow vertical wall.png")
        right_hallway_end.init_position(self.width*0.95, self.height*0.36)

        bottom_hallway_end = Block(LIGHT_YELLOW, self.width*0.30, self.height*0.05, "light yellow horizontal wall.png")
        bottom_hallway_end.init_position(self.width*0.25, self.height*0.95)

        self.obj_group.add(upper_left_block, middle_left_block, lower_left_block, upper_right_block, lower_right_block, right_hallway_end, bottom_hallway_end)


     ### Vu formation & patrol route area3_19
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route3(list(self.e_group)[2]) #Enemy3



    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    # Enemy #1 when Snake comes from area2_18
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.60, self.height*.44)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 20), ("look_west", 20), ("end", 0)]


    # Enemy #2 when Snake comes from area2_18
    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.5, self.height*.75)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 8), ("go_north", 100), ("wait", 50), ("go_south", 100), ("end", 0)]

    # Enemy #3
    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.3, self.height*.30)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 8), ("go_south", 80), ("wait", 50), ("go_north", 80), ("end", 0)]

    ### End Vu formation & patrol route area3_19


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.25, self.height*0.30), (self.width*0.25, self.height*0.50), self.inner_door_thickness) #upper left inner door
        pygame.draw.line(window, BLACK, (self.width*0.25, self.height*0.70), (self.width*0.25, self.height*0.90), self.inner_door_thickness) #lower left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.95, self.height*0.42), (self.width*0.95, self.height*0.63), self.inner_door_thickness) #right inner door
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.25
                and self.player_obj.rect.centerx <= self.width*0.55 and self.player_obj.moving_north):
                print("in 3_18")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation2()


            elif (self.player_obj.rect.x <= self.width*0.25 and self.player_obj.rect.centery >= self.height*0.70
                and self.player_obj.rect.centery <= self.height*0.90 and self.player_obj.moving_west):
                print("in 3_19_lower_left_inner_entrance")
                new_area = self._make_transition(self.width-40, self.height*0.50, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()

            '''
            elif (self.player_obj.rect.topright[0] >= self.width*0.95 and self.player_obj.rect.topright[1] >= self.height*0.445
                  and self.player_obj.rect.bottomright[1] <= self.height*0.655 and self.player_obj.moving_east):
                print("in 3_19_right_inner_entrance")
                new_area = self._make_transition(40, self.height*0.50, area_dict, "inner2")
                new_area._reset_enemy_state()
                new_area._formation1()
            '''

            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_19_LowerLeftInnerArea(area_base.Area):
    '''A class that represents the lower left inner Area of Area 3_19.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_19_LowerLeftInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_west_inner_room()

        wb = WaterBalloonPickUp()
        wb.init_position(self.width*0.45, self.height*0.43)
        self.obj_group.add(wb)

        wb = WaterBalloonPickUp()
        wb.init_position(self.width*0.53, self.height*0.43)
        self.obj_group.add(wb)

        wb = WaterBalloonPickUp()
        wb.init_position(self.width*0.61, self.height*0.43)
        self.obj_group.add(wb)

        wb = WaterBalloonPickUp()
        wb.init_position(self.width*0.45, self.height*0.50)
        self.obj_group.add(wb)

        wb = WaterBalloonPickUp()
        wb.init_position(self.width*0.53, self.height*0.50)
        self.obj_group.add(wb)

        wb = WaterBalloonPickUp()
        wb.init_position(self.width*0.61, self.height*0.50)
        self.obj_group.add(wb)


    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.35
                  and self.player_obj.rect.centery <= self.height*0.65 and self.player_obj.moving_east):
                print("in 3_19")
                new_area = self._make_transition(self.width*0.25+40, self.height*0.80, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area3_19_RightInnerArea(area_base.Area):
    '''A class that represents the right inner Area of Area3_19.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area3_19_RightInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False
        self._draw_east_inner_room()

        
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2        


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            pass


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            pass

        
    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
                     

    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        #print("Snake's Health: ", self.player_obj.health)
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.35
                and self.player_obj.rect.centery <= self.height*0.65 and self.player_obj.moving_west):
                print("in 3_19")
                new_area = self._make_transition(self.width*0.95-40, self.height*0.55, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()

                
            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area
