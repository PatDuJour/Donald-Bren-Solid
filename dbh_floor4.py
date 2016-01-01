import pygame #fine
#from snake_player import * #fine
#from collections import namedtuple #For assigning neighbors to Areas #fine
from colors import * #fine
from block import * #fine
from weapons import * #fine
from collectibles import * #fine
#from area_base import *
import area_base
import physical_objs
import cameras


class Area4_1(area_base.Area):
    '''A class to represent Area4_1 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_1 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._initialize_area1_walls_and_railings()


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "peach background.png")
        self.obj_group.draw(window)
        self._draw_area1_stairs(window)
      
        window.blit(pygame.font.SysFont("Arial", 30).render("FLOOR 4", 1, BLACK), (self.width*0.77, self.height*0.70))
        
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
                print("in stairwell3_1_to_4_1")
                new_area = self._make_transition(self.width*0.80-70, self.height*0.65, area_dict, "inner1")
                '''
                print("in 3_1")
                new_area = self._make_transition(self.width*0.10+500, self.height*0.35, area_dict, "inner1")
                #new_area._reset_enemy_state()               
                #new_area._formation1()
                self.player_obj.moving_east = True
                '''

            elif (self.player_obj.rect.topright[0] >= self.width*0.90 and self.player_obj.rect.centery >= self.height*0.35
                  and self.player_obj.rect.centery <= self.height*0.60 and self.player_obj.moving_east):
                print("in 4_2")
                new_area = self._make_transition(40, self.height*0.725, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()

            elif (self.player_obj.rect.x <= self.width*0.10 and self.player_obj.rect.centery >= self.height*0.25
                  and self.player_obj.rect.centery <= self.height*0.45 and self.player_obj.moving_west):
                if self.player_obj.has_floor5_card_key:
                    print("in stairwell4_1_to_5_1")
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


class Stairwell4_1_to_5_1(area_base.Area):
    '''A class that represents the left inner Area of Area2_8.'''
    
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
                print("in 4_1")
                new_area = self._make_transition(self.width*0.10+70, self.height*0.35, area_dict, "inner1")
                #new_area._reset_enemy_state()
                #new_area._formation1()


            elif (self.player_obj.rect.topright[0] >= self.width*0.80 and self.player_obj.rect.centery >= self.height*0.55
                  and self.player_obj.rect.centery <= self.height*0.75 and self.player_obj.moving_east):
                print("in 5_1")
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
    

class Area4_2(area_base.Area):
    '''A class to represent Area4_2 of DBH.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: ["Enemy"]=None):
        '''Initializes the attributes of an Area4_2 object.'''
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


        straw = StrawPickUp()
        straw.init_position(self.width*0.45, self.height*0.23)
        self.obj_group.add(straw)

        rb = RubberBandPickUp()
        rb.init_position(self.width*0.45, self.height*0.18)
        self.obj_group.add(rb)

        straw = StrawPickUp()
        straw.init_position(self.width*0.45, self.height*0.10)
        self.obj_group.add(straw)

        '''
        blue_sofa_chair = physical_objs.GreenSofaChair("west")
        blue_sofa_chair.init_position(self.width*0.71, self.height*0.83)
        self.obj_group.add(blue_sofa_chair)

        square_table = physical_objs.SmallSquareTable()
        square_table.init_position(self.width*0.61, self.height*0.85)
        self.obj_group.add(square_table)
        '''

        green_sofa = physical_objs.GreenSofa("west")
        green_sofa.init_position(self.width*0.71, self.height*0.70)
        self.obj_group.add(green_sofa)

    ### begin
    #from 4_1
    def _formation1(self):
        if self.e_group != None:
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route3(list(self.e_group)[2]) #Enemy3
            self.gen_patrol_route4(list(self.e_group)[3]) #Enemy4
            self.gen_patrol_route5(list(self.e_group)[4]) #Enemy5
            self.gen_patrol_route6(list(self.e_group)[5]) #Enemy6
            self.gen_patrol_route7(list(self.e_group)[6]) #Enemy7

    #from 4_3
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route3(list(self.e_group)[2]) #Enemy3
            self.gen_patrol_route4(list(self.e_group)[3]) #Enemy4
            self.gen_patrol_route5(list(self.e_group)[4]) #Enemy5
            self.gen_patrol_route6(list(self.e_group)[5]) #Enemy6
            self.gen_patrol_route8(list(self.e_group)[6]) #Enemy7

    #from 4_10
    def _formation3(self):
        if self.e_group != None:
            self.gen_patrol_route5(list(self.e_group)[4]) #Enemy5
            self.gen_patrol_route8(list(self.e_group)[6]) #Enemy7
            self.gen_patrol_route9(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route10(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route11(list(self.e_group)[2]) #Enemy3
            self.gen_patrol_route12(list(self.e_group)[3]) #Enemy4
            self.gen_patrol_route13(list(self.e_group)[5]) #Enemy6



    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.18, self.height*0.12)
            enemy._looking_west = True
            enemy.patrol_route = [("look_west", 20), ("look_north", 20), ("look_east", 10), ("end", 0)]


    def gen_patrol_route9(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.18, self.height*0.12)
            enemy._looking_west = True
            enemy.patrol_route = [("look_west", 50), ("look_north", 20), ("look_east", 15), ("end", 0)]


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.72, self.height*0.12)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 20), ("look_north", 20), ("look_west", 10), ("end", 0)]


    def gen_patrol_route10(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.72, self.height*0.12)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 50), ("look_north", 20), ("look_west", 10), ("end", 0)]


    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.18, self.height*0.32)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 20), ("look_east", 20), ("look_south", 40), ("look_east", 20), ("end", 0)]

    def gen_patrol_route11(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.18, self.height*0.32)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 20), ("look_east", 20), ("look_south", 40), ("look_east", 20), ("end", 0)]
            

    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.72, self.height*0.32)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 20), ("look_west", 20), ("look_south", 40), ("look_west", 20), ("end", 0)]

    def gen_patrol_route12(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.72, self.height*0.32)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 20), ("look_west", 20), ("look_south", 40), ("look_west", 20), ("end", 0)]


    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.47, self.height*0.90)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 5), ("look_east", 40), ("end", 0)]


    def gen_patrol_route6(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.10, self.height*0.46)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 30), ("look_south", 70), ("end", 0)]

    def gen_patrol_route13(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.10, self.height*0.46)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 25), ("look_east", 70), ("end", 0)]


    def gen_patrol_route7(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.82, self.height*0.46)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 50), ("go_north", 25), ("look_north", 50),
                                  ("go_south", 25), ("end", 0)]

    def gen_patrol_route8(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.82, self.height*0.46)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 7), ("go_north", 25), ("look_north", 50),
                                  ("go_south", 25), ("end", 0)]
            
    ### End      

    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "peach background.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.20, self.height*0.98), (self.width*0.40, self.height*0.98), self.inner_door_thickness) #inner door
        

    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.25
                  and self.player_obj.rect.centery <= self.height*0.65 and self.player_obj.moving_east):
                print("in 4_3")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()
                

            elif (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.60
                and self.player_obj.rect.centery <= self.height*0.85 and self.player_obj.moving_west):
                print("in 4_1")
                new_area = self._make_transition(self.width*0.90-40, self.height*0.475, area_dict, "west1")
                #new_area._reset_enemy_state()
                #new_area._formation1()


            elif (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.02
                and self.player_obj.rect.centerx <= self.width*0.98 and self.player_obj.moving_north):
                print("in 4_10")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()

                
            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

        return new_area


class Area4_3(area_base.Area):
    '''A class to represent Area4_3 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_3 object.'''
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

        #AREA4_3 PHYSICAL OBJECTS
        green_sofa = physical_objs.GreenSofa("east")
        green_sofa.init_position(self.width*0.55, self.height*0.30)
        self.obj_group.add(green_sofa)
        
        long_table = physical_objs.SmallLongTable("vertical")
        long_table.init_position(self.width*0.66, self.height*0.32)
        self.obj_group.add(long_table)
        

    def _formation1(self):
        #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
        if self.e_group != None:
            #self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            enemy_lst = list(self.e_group)

            non_cam_lst = []
            for enemy in enemy_lst:
                if type(enemy) == cameras.Camera:
                    self.gen_patrol_route1(enemy) #Camera Enemy
                else:
                    non_cam_lst.append(enemy)

            if non_cam_lst != []: #If a non-Camera Enemy exists in this Area
                self.gen_patrol_route3(non_cam_lst[0])
                self.gen_patrol_route5(non_cam_lst[1])

    def _formation2(self):
        #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
        if self.e_group != None:
            #self.gen_patrol_route2(list(self.e_group)[0]) #Enemy1
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            enemy_lst = list(self.e_group)

            non_cam_lst = []
            for enemy in enemy_lst:
                if type(enemy) == cameras.Camera:
                    self.gen_patrol_route2(enemy) #Camera Enemy
                else:
                    non_cam_lst.append(enemy)

            if non_cam_lst != []: #If a non-Camera Enemy exists in this Area
                self.gen_patrol_route4(non_cam_lst[0])
                self.gen_patrol_route5(non_cam_lst[1])


    def gen_patrol_route1(self, enemy): #For the Camera
        if self.e_group != None:
            enemy.init_position(self.width*0.83, self.height*0.10)
            enemy._looking_west = True
            enemy.patrol_route = [("go_south", 80), ("wait", 10),
                                  ("go_north", 80), ("wait", 10), ("end", 0)]


    def gen_patrol_route2(self, enemy): #For the Camera
        if self.e_group != None:
            enemy.init_position(self.width*0.83, self.height*0.60)
            enemy._looking_west = True
            enemy.patrol_route = [("wait", 10), ("go_north", 80),
                                  ("wait", 10), ("go_south", 80), ("end", 0)]

    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.45, self.height*0.90)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 20), ("look_east", 15), ("end", 0)]


    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.45, self.height*0.90)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 20), ("look_north", 10), ("end", 0)]

        
    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.81, self.height*0.90)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 20), ("look_west", 15), ("end", 0)]

        
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
                print("in 4_2")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation2()


            elif (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.40
                and self.player_obj.rect.centerx <= self.width*0.75 and self.player_obj.moving_north):
                print("in 4_9")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation2()


            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.50
                  and self.player_obj.rect.centerx <= self.width*0.85 and self.player_obj.moving_south):
                print("in 4_4")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()

            '''
            elif (self.player_obj.rect.topright[0] >= self.width*0.85 and self.player_obj.rect.topright[1] >= self.height*0.695
                  and self.player_obj.rect.bottomright[1] <= self.height*0.905 and self.player_obj.moving_east):
                print("in 4_4_right_inner_entrance")
                new_area = self._make_transition(40, self.height*0.50, area_dict, "inner2")
                new_area._reset_enemy_state()
                new_area._formation1()
            '''
                
            '''
            elif (self.player_obj.rect.bottomleft[1] >= self.height*0.645 and self.player_obj.rect.bottomleft[0] >= self.width*0.095
                  and self.player_obj.rect.bottomright[0] <= self.width*0.305 and self.player_obj.moving_south):
                print("in 4_4_left_inner_entrance")
                new_area = self._make_transition(self.width*0.50, 40, area_dict, "inner1")
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


class Area4_4_LeftInnerArea(area_base.Area):
    '''A class to represent a left inner Area of Area4_3'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_4_LeftInnerArea object'''
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
                print("in 4_3")
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


class Area4_4_RightInnerArea(area_base.Area):
    '''A class to represent a right inner Area of Area4_3'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_4_RightInnerArea object.'''
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
                print("in 4_3")
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
    

class Area4_4(area_base.Area):
    '''A class to represent Area4_4 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_4 object.'''
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


    #vu -- start of enemies' patrol routes for area4_4
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
            enemy.init_position(self.width*.30, self.height*.23)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 10), ("look_east", 10), ("look_north", 10),
                                  ("look_east", 10), ("wait", 10), ("end", 0)]


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

    #vu -- end of enemies' patrol routes for area4_4
            
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
                print("in 4_3")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.50
                  and self.player_obj.rect.centerx <= self.width*0.85 and self.player_obj.moving_south):
                print("in 4_5")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()

            '''
            elif (self.player_obj.rect.topright[0] >= self.width*0.85 and self.player_obj.rect.topright[1] >= self.height*0.145
                  and self.player_obj.rect.bottomright[1] <= self.height*0.355 and self.player_obj.moving_east):
                print("in 4_4_upper_right_inner_entrance")
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


class Area4_4_UpperRightInnerArea(area_base.Area):
    '''A class to represent an upper right inner Area of Area4_4'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_4_UpperRightInnerArea object.'''
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
                print("in 4_4")
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


class Area4_5(area_base.Area):
    '''A class to represent Area4_5 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_5 object.'''
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


    #vu -- start of enemies's patrol routes for area4_5
    # formation from area4_4 to area4_5
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route5(list(self.e_group)[2]) #Enemy3

    # formation from area4_6 to area4_5
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route6(list(self.e_group)[2]) #Enemy3


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.68, self.height*.11) #use to be 0.20
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 10), ("look_east", 10), ("look_west", 10), ("end", 0)]

    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.68, self.height*.88) #use to be 0.80
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 12), ("look_west", 10), ("wait", 10), ("look_east", 10),
                                  ("look_east", 10), ("wait", 10), ("end", 0)]

    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.68, self.height*.11) #use to be 0.25
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 15), ("look_east", 10), ("wait", 10), ("look_south", 15),
                                  ("look_west", 15), ("look_south", 5), ("wait", 10), ("end", 0)]
    
    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.68, self.height*.88)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 10), ("look_east", 10), ("look_west", 10), ("end", 0)]


    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.68, self.height*.50)
            enemy._looking_west = True
            enemy.patrol_route = [("go_west", 20), ("look_north", 10), ("look_east", 10), ("go_east", 40), ("look_north", 10),
                                  ("look_east", 10), ("go_west", 20), ("look_south", 10), ("end", 0)]

    def gen_patrol_route6(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.68, self.height*.50)
            enemy._looking_east = True
            enemy.patrol_route = [("go_east", 20), ("look_south", 10), ("look_west", 10), ("go_west", 40), ("look_south", 10),
                                  ("look_east", 10), ("go_east", 20), ("look_north", 10), ("end", 0)]

            
    #vu -- end of enemies's patrol routes for area4_5             

    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.50, self.height*0.15), (self.width*0.50, self.height*0.35), self.inner_door_thickness) #upper left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.50, self.height*0.65), (self.width*0.50, self.height*0.85), self.inner_door_thickness) #lower left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.85, self.height*0.07), (self.width*0.85, self.height*0.27), self.inner_door_thickness) #upper right inner door
        pygame.draw.line(window, WOODEN, (self.width*0.85, self.height*0.40), (self.width*0.85, self.height*0.60), self.inner_door_thickness) #middle right inner door
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
                print("in 4_4")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation2()

                
            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.50
                  and self.player_obj.rect.centerx <= self.width*0.85 and self.player_obj.moving_south):
                print("in 4_6")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()

            '''
            elif (self.player_obj.rect.topright[0] >= self.width*0.85 and self.player_obj.rect.topright[1] >= self.height*0.395
                  and self.player_obj.rect.bottomright[1] <= self.height*0.605 and self.player_obj.moving_east):
                print("in 4_5_middle_inner_entrance")
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


class Area4_5_MiddleInnerArea(area_base.Area):
    '''A class that represents the middle inner Area of Area4_5'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_5_MiddleInnerArea object.'''
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
                print("in 4_5")
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

    
class Area4_6(area_base.Area):
    '''A class to represent Area 4_6 of DBH'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_6 object.'''
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


    #vu -- start of enemies's patrol routes for area4_6
    # formation from area4_5 to area4_6
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route3(list(self.e_group)[2]) #Enemy3

    # formation from area4_7 to area4_6
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
            
    #vu -- end of enemies's patrol routes for area4_6


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.03, self.height*0.75), (self.width*0.23, self.height*0.75), self.inner_door_thickness) #left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.40, self.height*0.75), (self.width*0.60, self.height*0.75), self.inner_door_thickness) #middle inner door
        pygame.draw.line(window, PINK, (self.width*0.85, self.height*0.25), (self.width*0.85, self.height*0.45), self.inner_door_thickness) #right inner door

        
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
                print("in 4_5")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation2()

                
            elif (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.30
                and self.player_obj.rect.centery <= self.height*0.75 and self.player_obj.moving_west):
                print("in 4_7")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()
            elif (self.player_obj.rect.topright[0] >= self.width*0.85 and self.player_obj.rect.centery >= self.height*0.25
                  and self.player_obj.rect.centery <= self.height*0.45 and self.player_obj.moving_east):
                print("in 4_6_right_inner_area")
                new_area = self._make_transition(40, self.height*0.50, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()

            '''
            elif (self.player_obj.rect.bottomleft[1] >= self.height*0.745 and self.player_obj.rect.bottomleft[0] >= self.width*0.395
                  and self.player_obj.rect.bottomright[0] <= self.width*0.605 and self.player_obj.moving_south):
                print("in 4_6_middle_inner_entrance")
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

class Area4_6_RightInnerArea(area_base.Area):
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
    

class Area4_6_MiddleInnerArea(area_base.Area):
    '''A class to represent a middle inner Area of Area4_6'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_6_MiddleInnerArea object.'''
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
                print("in 4_6")
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
    

class Area4_7(area_base.Area):
    '''A class to represent Area4_7 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_7 object.'''
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
    # formation from area4_6 to area4_7
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route3(list(self.e_group)[2]) #Enemy3

    # formation from area4_8 to area4_7
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route4(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route5(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route6(list(self.e_group)[2]) #Enemy3


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.15, self.height*.50)
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
            enemy.init_position(self.width*.35, self.height*.63)
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

    #vu -- end of enemies's patrol routes


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.07, self.height*0.30), (self.width*0.27, self.height*0.30), self.inner_door_thickness) #upper left inner door
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
                print("in 4_6")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation2()


            elif (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.30
                and self.player_obj.rect.centery <= self.height*0.75 and self.player_obj.moving_west):
                print("in 4_8")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery+self.height*0.23, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()

            '''
            elif (self.player_obj.rect.y <= self.height*0.30 and self.player_obj.rect.x >= self.width*0.065
                and self.player_obj.rect.topright[0] <= self.width*0.275 and self.player_obj.moving_north):
                print("in 4_7_upper_left_inner_entrance")
                new_area = self._make_transition(self.width*0.50, self.height-40, area_dict, "inner1")
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


class Area4_7_UpperLeftInnerArea(area_base.Area):
    '''A class that represents the upper left inner Area of Area4_7.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_7_UpperLeftInnerArea object.'''
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
                print("in 4_7")
                new_area = self._make_transition(self.width*0.17, self.height*0.30+70, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area4_8(area_base.Area):
    '''A class to represent Area4_8 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_8 object.'''
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
        

    #vu -- start of enemies' patrol routes area4_8
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
            enemy.init_position(self.width*.50, self.height*.45)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 10), ("look_south", 15), ("end", 0)]
            
            
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
            enemy.patrol_route = [("look_south", 30), ("look_east", 20), ("end", 0)]

    #vu -- end of enemies' patrol routes area4_8
            

    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, BLACK, (self.width*0.45, self.height*0.05), (self.width*0.65, self.height*0.05), self.inner_door_thickness) #upper inner door
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
                print("in 4_7")
                new_area = self._make_transition(40, self.player_obj.rect.centery-self.height*0.229, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation2()
            elif (self.player_obj.rect.y <= self.height*0.05 and self.player_obj.rect.x >= self.width*0.445
                and self.player_obj.rect.topright[0] <= self.width*0.655 and self.player_obj.moving_north):
                print("in 4_8_upper_inner_entrance")
                new_area = self._make_transition(self.width*0.50, self.height-40, area_dict, "inner2")
                new_area._reset_enemy_state()
                new_area._formation1()

            '''
            elif (self.player_obj.rect.x <= self.width*0.40 and self.player_obj.rect.y >= self.height*0.195
                and self.player_obj.rect.bottomleft[1] <= self.height*0.405 and self.player_obj.moving_west):
                print("in 4_8_left_inner_entrance")
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


class Area4_8_LeftInnerArea(area_base.Area):
    '''A class that represents the left inner Area of Area4_8.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_8_LeftInnerArea object.'''
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
                print("in 4_8")
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


class Area4_8_UpperInnerArea(area_base.Area):
    '''A class thar repesents the upper inner Area of Area4_8.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_8_UpperInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_north_inner_room()

        noodles1 = InstantNoodlesPickUp()
        noodles1.init_position(self.width*0.46, self.height*0.28)

        noodles2 = InstantNoodlesPickUp()
        noodles2.init_position(self.width*0.51, self.height*0.28)
        
        b1 = BananaPeelPickUp()
        b1.init_position(self.width*0.32, self.height*0.33)

        b2 = BananaPeelPickUp()
        b2.init_position(self.width*0.41, self.height*0.33)

        b3 = BananaPeelPickUp()
        b3.init_position(self.width*0.50, self.height*0.33)

        b4 = BananaPeelPickUp()
        b4.init_position(self.width*0.59, self.height*0.33)

        b5 = BananaPeelPickUp()
        b5.init_position(self.width*0.68, self.height*0.33)

        b6 = BananaPeelPickUp()
        b6.init_position(self.width*0.32, self.height*0.68)

        b7 = BananaPeelPickUp()
        b7.init_position(self.width*0.41, self.height*0.68)

        b8 = BananaPeelPickUp()
        b8.init_position(self.width*0.50, self.height*0.68)

        b9 = BananaPeelPickUp()
        b9.init_position(self.width*0.59, self.height*0.68)

        b10 = BananaPeelPickUp()
        b10.init_position(self.width*0.68, self.height*0.68)

        b11 = BananaPeelPickUp()
        b11.init_position(self.width*0.32, self.height*0.44)

        b12 = BananaPeelPickUp()
        b12.init_position(self.width*0.32, self.height*0.55)

        b13 = BananaPeelPickUp()
        b13.init_position(self.width*0.68, self.height*0.44)

        b14 = BananaPeelPickUp()
        b14.init_position(self.width*0.68, self.height*0.55)
        
        self.obj_group.add(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14, noodles1, noodles2)
        

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
        window.blit(pygame.font.SysFont("Arial", 50).render("SNAKE!", 1, BLACK), (self.width*0.47, self.height*0.40))
        window.blit(pygame.font.SysFont("Arial", 50).render("You can only defeat", 1, BLACK), (self.width*0.37, self.height*0.50))
        window.blit(pygame.font.SysFont("Arial", 50).render("Frost with bananas!", 1, BLACK), (self.width*0.37, self.height*0.60))



        
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
                print("in 4_8")
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


class Area4_9(area_base.Area):
    '''A class to represent Area4_9 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_9 object.'''
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


    #vu -- start of enemies's patrol routes for area4_9
    # formation from 4_12 to 4_9
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2

    # formation from 4_3 to 4_9
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

    #vu -- end of enemies's patrol routes for area4_9


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
                print("in 4_12")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()

                
            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.40
                  and self.player_obj.rect.centerx <= self.width*0.75 and self.player_obj.moving_south):
                print("in 4_3")
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

    
class Area4_10(area_base.Area):
    '''A class to represent Area4_10 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_10 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_block = Block(DARK_TEAL, self.width*0.45, self.height*0.30, "dark teal big semi horizontal.png")
        upper_block.init_position(self.width*0.55, 0)

        middle_block = Block(DARK_TEAL, self.width*0.80, self.height*0.20, "dark teal big horizontal.png")
        middle_block.init_position(self.width*0.20, self.height*0.30)

        #upper_left_wall = Block(BRICK, self.width*0.02, self.height*0.40, "brick vertical wall.png")
        upper_left_wall = Block(BRICK, self.width*0.08, self.height*0.40, "brick vertical wall.png")
        upper_left_wall.init_position(0-self.width*0.06, 0)

        lower_left_wall = Block(BRICK, self.width*0.02, self.height*0.25, "brick vertical wall.png")
        lower_left_wall.init_position(0, self.height*0.75)

        right_wall = Block(LIGHT_YELLOW, self.width*0.02, self.height*0.50, "light yellow vertical wall.png")
        right_wall.init_position(self.width*0.98, self.height*0.50)

        self.obj_group.add(upper_block, middle_block, upper_left_wall, lower_left_wall, right_wall)

        #AREA4_10 PHYSICAL OBJECTS
        sofa_chair1 = physical_objs.GreenSofaChair("east")
        sofa_chair1.init_position(self.width*0.39, self.height*0.65)
        self.obj_group.add(sofa_chair1)

        sofa_chair2 = physical_objs.GreenSofaChair("west")
        sofa_chair2.init_position(self.width*0.61, self.height*0.65)
        self.obj_group.add(sofa_chair2)

        sofa_chair3 = physical_objs.GreenSofaChair("south")
        sofa_chair3.init_position(self.width*0.492, self.height*0.52)
        self.obj_group.add(sofa_chair3)

        square_table = physical_objs.SmallSquareTable()
        square_table.init_position(self.width*0.50, self.height*0.67)
        self.obj_group.add(square_table)

        green_sofa_chair = physical_objs.GreenSofaChair("south")
        green_sofa_chair.init_position(self.width*0.86, self.height*0.52)
        self.obj_group.add(green_sofa_chair)

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
            '''
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            #self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            '''
            #self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            enemy_lst = list(self.e_group)

            non_cam_lst = []
            for enemy in enemy_lst:
                if type(enemy) == cameras.Camera:
                    self.gen_patrol_route1(enemy) #Camera Enemy
                else:
                    non_cam_lst.append(enemy)

            if non_cam_lst != []: #If a non-Camera Enemy exists in this Area
                self.gen_patrol_route2(non_cam_lst[0])

    def _formation2(self):
        if self.e_group != None:
            '''
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2
            '''
            #self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            enemy_lst = list(self.e_group)

            non_cam_lst = []
            for enemy in enemy_lst:
                if type(enemy) == cameras.Camera:
                    self.gen_patrol_route1(enemy) #Camera Enemy
                else:
                    non_cam_lst.append(enemy)

            if non_cam_lst != []: #If a non-Camera Enemy exists in this Area
                self.gen_patrol_route2(non_cam_lst[0])


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy): #For the Camera
        if self.e_group != None:
            enemy.init_position(self.width*0.23, self.height*0.53)
            enemy._looking_south = True
            enemy.patrol_route = [("wait", 10), ("go_east", 50),
                                  ("wait", 10), ("go_west", 50), ("end", 0)]
            

    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.03, self.height*0.49)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 15), ("look_west", 20),
                                  ("look_south", 20), ("end", 0)]


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
                print("in 4_11")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.02
                and self.player_obj.rect.centerx <= self.width*0.55 and self.player_obj.moving_north):
                print("in 4_13")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.02
                  and self.player_obj.rect.centerx <= self.width*0.98 and self.player_obj.moving_south):
                print("in 4_2")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation3()


            elif (self.player_obj.rect.bottomleft[1] >= self.height*0.30 and self.player_obj.rect.bottomleft[1] <= self.height*0.50 and self.player_obj.rect.bottomleft[0] >= self.width*0.295
                  and self.player_obj.rect.bottomright[0] <= self.width*0.555 and self.player_obj.moving_south):
                print("in 4_10_girls_bathroom")
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


class Area4_10_GirlsBathroom(area_base.Area):
    '''A class to represent the girl's bathroom adjacent to Area4_10'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_10_GirlsBathroom object.'''
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
                print("in 4_10")
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


class Area4_11(area_base.Area):
    '''A class to represent Area4_11 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_11 object.'''
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
                print("in 4_10")
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


class Area4_12(area_base.Area):
    '''A class to represent Area4_12 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_12 object.'''
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
        pygame.draw.line(window, WOODEN, (self.width*0.75, self.height*0.35), (self.width*0.75, self.height*0.55), self.inner_door_thickness) #lower right inner door

        
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
                print("in 4_13")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.40
                  and self.player_obj.rect.centerx <= self.width*0.75 and self.player_obj.moving_south):
                print("in 4_9")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()

            '''
            elif (self.player_obj.rect.topright[0] >= self.width*0.75 and self.player_obj.rect.topright[1] >= self.height*0.345
                  and self.player_obj.rect.bottomright[1] <= self.height*0.555 and self.player_obj.moving_east):
                print("in 4_14_right_inner_entrance")
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


class Area4_14_RightInnerArea(area_base.Area):
    '''A class that represents the right inner Area of Area4_12.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_14_RightInnerArea object.'''
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
                print("in 4_12")
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


class Area4_13(area_base.Area):
    '''A class to represent Area4_13 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_13 object.'''
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
 
        mgs4_game = MGS4()
        mgs4_game.init_position(self.width*0.55, self.height*0.20)
        self.obj_group.add(mgs4_game)

        
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
            enemy.init_position(self.width*0.17, self.height*0.23)
            enemy._looking_west = True
            enemy.patrol_route = [("look_west", 90), ("look_east", 15), ("end", 0)]


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            #enemy.init_position(800, 150)
            enemy.init_position(self.width*0.94, self.height*0.23)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 90), ("look_west", 15), ("end", 0)]


    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            #enemy.init_position(200, 600)
            enemy.init_position(self.width*0.36, self.height*0.47)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 20), ("look_south", 30), ("look_north", 15), ("look_east", 30), ("look_west", 20), ("end", 0)]


    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            #enemy.init_position(800, 600)
            enemy.init_position(self.width*0.74, self.height*0.47)
            enemy._looking_south = True
            #enemy.patrol_route = [("look_south", 20), ("look_west", 20), ("look_north", 15), ("look_south", 20), ("look_east", 20), ("end", 0)]
            enemy.patrol_route = [("look_south", 20), ("look_east", 20), ("look_north", 15), ("look_south", 20), ("west_east", 12), ("end", 0)]

    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.55, self.height*0.40)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 20), ("end", 0)]


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)

        pygame.draw.line(window, WOODEN, (self.width*0.30, self.height*0.70), (self.width*0.50, self.height*0.70), self.inner_door_thickness) #door to boys' bathroom
        
        
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
                print("in 4_12")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.15
                and self.player_obj.rect.centery <= self.height*0.55 and self.player_obj.moving_west):
                print("in 4_14")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.02
                  and self.player_obj.rect.centerx <= self.width*0.55 and self.player_obj.moving_south):
                print("in 4_10")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()

            '''
            elif (self.player_obj.rect.y <= self.height*0.70 and self.player_obj.rect.y >= self.height*0.55 and self.player_obj.rect.x >= self.width*0.295
                and self.player_obj.rect.topright[0] <= self.width*0.555 and self.player_obj.moving_north):
                print("in 4_14_boys_bathroom")
                new_area = self._make_transition(self.width*0.35, self.height*0.75-70, area_dict, "inner1")
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


class Area4_13_BoysBathroom(area_base.Area):
    '''A class to represent the boy's bathroom adjacent to Area4_13'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_14_BoysBathroom object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_boys_bathroom()
        

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
                print("in 4_13")
                new_area = self._make_transition(self.width*0.40, self.height*0.70+70, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area4_14(area_base.Area):
    '''A class to represent Area4_14 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_14 object.'''
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


    ### Vu formation & patrol route area4_14
    # formation from area4_13
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route3(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route4(list(self.e_group)[2]) #Enemy3
            self.gen_patrol_route5(list(self.e_group)[3]) #Enemy4


    # formation from area4_15
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route2(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route3(list(self.e_group)[1]) #Enemy2        
            self.gen_patrol_route4(list(self.e_group)[2]) #Enemy3
            self.gen_patrol_route6(list(self.e_group)[3]) #Enemy4


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?

    # Enemy #1 when Snake comes from area4_13
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.1, self.height*.25)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 25), ("go_east", 50), ("look_south", 10),
                                  ("go_east", 50), ("look_east", 10), ("go_east", 50), ("look_south", 10),
                                  ("go_west", 50), ("look_west", 10), ("go_west", 50), ("look_west", 10),
                                  ("go_west", 50), ("look_west", 10), ("end", 0)]


    # Enemy #1 when Snake comes from area4_15
    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.87, self.height*.25) #use to be self.width*.9
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 15), ("go_west", 50), ("look_west", 10),
                                  ("go_west", 50), ("look_west", 10), ("go_west", 50), ("look_south", 10),
                                  ("go_east", 50), ("look_east", 10), ("go_east", 50), ("look_east", 10),
                                  ("go_east", 50), ("look_east", 10), ("end", 0)]

    # Enemy #2 when Snake comes from area4_13
    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.4, self.height*.25)
            enemy._looking_north = True
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
                                  ("look_east", 25), ("go_south", 35), ("end", 0)]


    # Enemy #1 when Snake comes from area4_15
    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.87, self.height*.45) #use to be self.width*.9
            enemy._looking_west = True
            #enemy.patrol_route = [("look_west", 15), ("look_north", 15), ("end", 0)]
            enemy.patrol_route = [("look_west", 15), ("look_north", 20), ("go_north", 30), ("look_west", 15), ("go_south", 30), ("end", 0)]


    def gen_patrol_route6(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.05, self.height*.25)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 15), ("look_south", 20), ("end", 0)]

    ### End Vu formation & patrol route area4_14


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
                print("in 4_13")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.15
                and self.player_obj.rect.centery <= self.height*0.60 and self.player_obj.moving_west):
                print("in 4_15")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation2()
                
            '''
            elif (self.player_obj.rect.y <= self.height*0.15 and self.player_obj.rect.x >= self.width*0.395
                and self.player_obj.rect.topright[0] <= self.width*0.605 and self.player_obj.moving_north):
                print("in 4_14_upper_middle_inner_entrance")
                new_area = self._make_transition(self.width*0.50, self.height-40, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.bottomleft[1] >= self.height*0.545 and self.player_obj.rect.bottomleft[0] >= self.width*0.695
                  and self.player_obj.rect.bottomright[0] <= self.width*0.905 and self.player_obj.moving_south):
                print("in 4_14_lower_right_inner_entrance")
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


class Area4_14_UpperMiddleInnerArea(area_base.Area):
    '''A class that represents the upper middle inner Area of Area4_14.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_14_UpperMiddleInnerArea object.'''
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
                print("in 4_14")
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


class Area4_14_LowerRightInnerArea(area_base.Area):
    '''A class that represents the lower right inner Area of Area4_14.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_14_LowerRightInnerArea object.'''
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
                print("in 4_14")
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


class Area4_15(area_base.Area):
    '''A class to represent Area4_15 of DBH.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_15 object.'''
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


    ### Vu formation & patrol route area4_15
    # formation from area4_17
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route5(list(self.e_group)[2]) #Enemy3
            self.gen_patrol_route7(list(self.e_group)[3]) #Enemy4

    # formation from area4_14
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route2(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route3(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route5(list(self.e_group)[2]) #Enemy3
            self.gen_patrol_route6(list(self.e_group)[3]) #Enemy4

    # formation from 4_16
    def _formation3(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route8(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route9(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route5(list(self.e_group)[2]) #Enemy3
            self.gen_patrol_route7(list(self.e_group)[3]) #Enemy4

    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?

    # Enemy #1 when Snake comes from area4_17, 4_16
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.25, self.height*.25)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 25), ("look_south", 25), ("end", 0)]


    # Enemy #1 when Snake comes from area4_14
    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.50, self.height*.3)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 15), ("look_south", 10), ("go_east", 50), ("wait", 10), ("look_south", 20),
                                  ("go_west", 50), ("end", 0)]
            
    #Enemy #2 when Snake comes from area4_14
    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.30, self.height*.25)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 7), ("look_west", 30), ("end", 0)]
            

    #Enemy #2 when Snake comes from area4_17, 4_16
    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.80, self.height*.50)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 10), ("look_east", 20), ("end", 0)]

    
    #Enemy #3 when Snake comes from area4_16
    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.15, self.height*.63)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 20), ("look_west", 20), ("look_north", 25), ("end", 0)]


    def gen_patrol_route6(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.15, self.height*.25)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 7), ("look_east", 30), ("end", 0)]


    def gen_patrol_route7(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.05, self.height*.25)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 20), ("look_south", 15), ("end", 0)]

    def gen_patrol_route8(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.35, self.height*.25)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 25), ("look_south", 25), ("end", 0)]


    def gen_patrol_route9(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.80, self.height*.25)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 10), ("look_east", 20), ("end", 0)]

    ### End Vu formation & patrol route area4_15


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)

        pygame.draw.line(window, WOODEN, (self.width*0.07, self.height*0.15), (self.width*0.27, self.height*0.15), self.inner_door_thickness) #upper left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.40, self.height*0.15), (self.width*0.60, self.height*0.15), self.inner_door_thickness) #upper middle inner door
        pygame.draw.line(window, WOODEN, (self.width*0.73, self.height*0.15), (self.width*0.93, self.height*0.15), self.inner_door_thickness) #upper right inner door
        pygame.draw.line(window, BLACK, (self.width*0.35, self.height*0.55), (self.width*0.55, self.height*0.55), self.inner_door_thickness) #lower inner door
        
        
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
                print("in 4_14")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation2()

                
            elif (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.15
                and self.player_obj.rect.centery <= self.height*0.55 and self.player_obj.moving_west):
                print("in 4_17")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.02
                  and self.player_obj.rect.centerx <= self.width*0.30 and self.player_obj.moving_south):
                print("in 4_16")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()

            elif (self.player_obj.rect.bottomleft[1] >= self.height*0.545 and self.player_obj.rect.bottomleft[0] >= self.width*0.345
                  and self.player_obj.rect.bottomright[0] <= self.width*0.555 and self.player_obj.moving_south):
                print("in 4_15_lower_inner_entrance")
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


class Area4_15_LowerInnerArea(area_base.Area):
    '''A class that represents the lower inner Area of Area4_15.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_15_LowerInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_south_inner_room()
        

    def _formation1(self): #zazaza
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route3(list(self.e_group)[2]) #Enemy2       
            self.gen_patrol_route4(list(self.e_group)[3]) #Enemy2       
            self.gen_patrol_route5(list(self.e_group)[4]) #Enemy2       
            self.gen_patrol_route6(list(self.e_group)[5]) #Enemy2       
            self.gen_patrol_route7(list(self.e_group)[6]) #Enemy2       
            self.gen_patrol_route8(list(self.e_group)[7]) #Enemy2
            '''
            self.gen_patrol_route9(list(self.e_group)[8]) #Enemy2       
            self.gen_patrol_route10(list(self.e_group)[9]) #Enemy2       
            self.gen_patrol_route11(list(self.e_group)[10]) #Enemy2       
            self.gen_patrol_route12(list(self.e_group)[11]) #Enemy2
            '''


    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.35, self.height*.39)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 7), ("look_north", 7), ("end", 0)]
            

    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.45, self.height*.39)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 7), ("look_north", 7), ("end", 0)]
            
    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.55, self.height*.39)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 7), ("look_north", 7), ("end", 0)]
            
    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.65, self.height*.39)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 7), ("look_north", 7), ("end", 0)]
            
    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.35, self.height*.59)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 7), ("look_north", 7), ("end", 0)]
            
    def gen_patrol_route6(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.45, self.height*.59)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 7), ("look_north", 7), ("end", 0)]
            
    def gen_patrol_route7(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.55, self.height*.59)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 7), ("look_north", 7), ("end", 0)]
            
    def gen_patrol_route8(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.65, self.height*.59)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 7), ("look_north", 7), ("end", 0)]


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
                print("in 4_15")
                new_area = self._make_transition(self.width*0.45, self.height*0.55-70, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation2()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area4_16(area_base.Area):
    '''A class to represent Area4_16 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_16 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        left_block = Block(LIGHT_YELLOW, self.width*0.30, self.height*0.50, "light yellow small semi vertical.png")
        left_block.init_position(0, self.height*0.50)

        right_block = Block(LIGHT_YELLOW, self.width*0.70, self.height, "light yellow big square.png")
        right_block.init_position(self.width*0.30, 0)

        left_wall = Block(LIGHT_YELLOW, self.width*0.02, self.height*0.50, "light yellow vertical wall.png")
        left_wall.init_position(0, 0)

        self.obj_group.add(left_block, right_block, left_wall)

        straw = StrawPickUp()
        straw.init_position(self.width*0.03, self.height*0.43)
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
        
        pygame.draw.line(window, PINK, (self.width*0.06, self.height*0.50), (self.width*0.26, self.height*0.50), self.inner_door_thickness) #inner door
        
        
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
                print("in 4_15")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation3()

            elif (self.player_obj.rect.bottomleft[1] >= self.height*0.50 and self.player_obj.rect.bottomleft[0] >= self.width*0.055
                  and self.player_obj.rect.bottomright[0] <= self.width*0.265 and self.player_obj.moving_south):
                print("in 4_16_inner_entrance")
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


class Area4_16_InnerArea(area_base.Area):
    '''A class that represents the inner Area of Area4_16.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_16_InnerArea object.'''
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
                print("in 4_16")
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


class Area4_17(area_base.Area):
    '''A class to represent Area4_17 of DBH.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_17 object.'''
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


    ### Vu formation & patrol route area4_17
    #formation from area4_15
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route3(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route4(list(self.e_group)[2]) #Enemy3
            self.gen_patrol_route5(list(self.e_group)[3]) #Enemy4

    #formation from area4_18
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route2(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route3(list(self.e_group)[1]) #Enemy2        
            self.gen_patrol_route4(list(self.e_group)[2]) #Enemy3
            self.gen_patrol_route5(list(self.e_group)[3]) #Enemy4


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?

    # Enemy #1 when Snake comes from area4_15
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.10, self.height*.25)
            enemy._looking_west = True
            enemy.patrol_route = [("look_west", 25), ("go_east", 60), ("look_south", 10),
                                  ("go_east", 50), ("look_east", 10), ("go_east", 50), ("wait", 10),
                                  ("go_west", 50), ("wait", 10), ("go_west", 50), ("look_north", 10),
                                  ("go_west", 50), ("wait", 10), ("end", 0)]

    # Enemy #1 when Snake comes from area4_18
    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.55, self.height*.25)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 25), ("go_west", 50), ("look_north", 10),
                                  ("go_west", 50), ("look_east", 10), ("go_west", 50), ("wait", 10),
                                  ("go_east", 50), ("wait", 10), ("go_east", 50), ("look_north", 10),
                                  ("go_east", 50), ("wait", 10), ("end", 0)]

    # Enemy #2 when Snake comes from area4_18, 4_15
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

    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.80, self.height*.25)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 15), ("look_west", 15), ("end", 0)]

    ### End Vu formation & patrol route area4_17

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
                print("in 4_15")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.15
                and self.player_obj.rect.centery <= self.height*0.45 and self.player_obj.moving_west):
                print("in 4_18")
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


class Area4_18(area_base.Area):
    '''A class to represent Area4_18 of DBH.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_18 object.'''
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
        

    ### Vu formation & patrol route area4_18
    # formation from area4_17
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route4(list(self.e_group)[2]) #Enemy3

    # formation from area4_19
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route5(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2        
            self.gen_patrol_route4(list(self.e_group)[2]) #Enemy3


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    # Enemy #1 when Snake comes from area4_17
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.44, self.height*.23)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 25), ("go_west", 30), ("look_north", 25),
                                  ("go_east", 30), ("look_west", 10), ("end", 0)]


    # Enemy #2 when Snake comes from area4_17
    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.3, self.height*.52)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 25), ("go_south", 50), ("look_north", 10),
                                  ("look_north", 15), ("go_north", 50), ("end", 0)]

    # Enemy #1 when Snake comes from area4_19
    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.9, self.height*.23)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 25), ("go_west", 30), ("look_north", 15),
                                  ("look_west", 25), ("go_east", 30), ("end", 0)]

    # Enemy #3
    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.51, self.height*.75) #use to be self.width*.52
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 20), ("go_north", 20), ("look_east", 25),
                                  ("look_south", 15), ("go_south", 20), ("end", 0)]
    
    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.44, self.height*.23)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 25), ("go_west", 30), ("look_north", 25),
                                  ("go_east", 30), ("look_west", 10), ("end", 0)]
    ### End Vu formation & patrol route area4_18



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
                print("in 4_17")
                new_area = self._make_transition(40, self.player_obj.rect.centery+self.height*0.13, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation2()


            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.25
                  and self.player_obj.rect.centerx <= self.width*0.55 and self.player_obj.moving_south):
                print("in 4_19")
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


class Area4_19(area_base.Area):
    '''A class to represent Area4_19 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_19 object.'''
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


     ### Vu formation & patrol route area2_19
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route3(list(self.e_group)[2]) #Enemy3
            self.gen_patrol_route4(list(self.e_group)[3]) #Enemy4



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
            enemy._looking_west = True
            enemy.patrol_route = [("look_west", 8), ("go_north", 100), ("wait", 50), ("go_south", 100), ("end", 0)]


    # Enemy #3
    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.3, self.height*.30)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 8), ("go_south", 80), ("wait", 50), ("go_north", 80), ("end", 0)]


    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.3, self.height*.85)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 20), ("end", 0)]

    ### End Vu formation & patrol route area2_19


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.25, self.height*0.30), (self.width*0.25, self.height*0.50), self.inner_door_thickness) #upper left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.25, self.height*0.70), (self.width*0.25, self.height*0.90), self.inner_door_thickness) #lower left inner door
        pygame.draw.line(window, GREEN, (self.width*0.95, self.height*0.42), (self.width*0.95, self.height*0.63), self.inner_door_thickness) #right inner door
        
        
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
                print("in 4_18")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation2()
                
            elif (self.player_obj.rect.topright[0] >= self.width*0.95 and self.player_obj.rect.centery >= self.height*0.42
                  and self.player_obj.rect.centery <= self.height*0.63 and self.player_obj.moving_east):
                print("in 4_19_pattis_boss_area")
                new_area = self._make_transition(40, self.height*0.50, area_dict, "inner2")
                '''
                if not new_area.boss.is_subdued:
                    new_area.boss.health = 300 #set the boss' health to 100 each time snake goes in the area as long as it exists
                '''
            '''
            elif (self.player_obj.rect.x <= self.width*0.25 and self.player_obj.rect.y >= self.height*0.695
                and self.player_obj.rect.bottomleft[1] <= self.height*0.905 and self.player_obj.moving_west):
                print("in 4_19_lower_left_inner_entrance")
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


class Area4_19_LowerLeftInnerArea(area_base.Area):
    '''A class that represents the lower left inner Area of Area 4_19.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_19_LowerLeftInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS
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
                print("in 4_19")
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


class Area4_19_PattisBossArea(area_base.Area):
    '''A class that represents the Area for Pattis' boss battle from Area4_19.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area4_19_PattisBossArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False
        #self._draw_east_inner_room()

        self.boss.init_position(window_width/2, window_height/2)

        
    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "green_background.png")
        self.obj_group.draw(window)
        pygame.draw.line(window, BLACK, (5, self.height*0.40), (5, self.height*0.60), 10)
                     

    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        #print("Snake's Health: ", self.player_obj.health)
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.35
                and self.player_obj.rect.centery <= self.height*0.65 and self.player_obj.moving_west):
                print("in 4_19")
                new_area = self._make_transition(self.width*0.95-40, self.height*0.52, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()

                
            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area
