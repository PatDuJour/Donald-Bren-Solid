import pygame #fine
#from snake_player import *
#from collections import namedtuple #For assigning neighbors to Areas
from colors import * #fine
from block import * #fine
from weapons import * #fine
from collectibles import * #fine
#from area_base import *
import area_base
import physical_objs

class Area1_1(area_base.Area):
    '''A class to represent Area1_1 of DBH.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_1 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self.stair_bar_thickness = 3

        top_block = Block(BLACK, self.width, self.height*0.10-self.horizontal_wall_thickness)
        top_block.init_position(0, 0)

        bottom_block = Block(BLACK, self.width, self.height*0.10-self.horizontal_wall_thickness)
        bottom_block.init_position(0, self.height*0.90+self.horizontal_wall_thickness)

        left_block = Block(BLACK, self.width*0.10-self.vertical_wall_thickness, self.height*0.80+2.0*self.horizontal_wall_thickness)
        left_block.init_position(0, self.height*0.10-self.horizontal_wall_thickness)

        right_block = Block(BLACK, self.width*0.10-self.vertical_wall_thickness, self.height*0.80+2.0*self.horizontal_wall_thickness)
        right_block.init_position(self.width*0.90+self.vertical_wall_thickness, self.height*0.10-self.horizontal_wall_thickness)

        vertical_block = Block(LIGHT_YELLOW, self.width*0.05, self.height*0.25, "light yellow vertical wall.png")
        vertical_block.init_position(self.width*0.60, self.height*0.10)
        
        upper_stair_railing = Block(WOODEN_TAN, self.width*0.30, self.height*0.05, "railing.png")
        upper_stair_railing.init_position(self.width*0.30, self.height*0.30)
        
        lower_stair_railing = Block(WOODEN_TAN, self.width*0.50, self.height*0.05, "railing.png")
        lower_stair_railing.init_position(self.width*0.10, self.height*0.55)

        top_wall = Block(LIGHT_YELLOW, self.width*0.80+2.0*self.vertical_wall_thickness, self.horizontal_wall_thickness, "light yellow horizontal wall.png")
        top_wall.init_position(self.width*0.10-self.vertical_wall_thickness, self.height*0.10-self.horizontal_wall_thickness)

        bottom_wall = Block(LIGHT_YELLOW, self.width*0.80+2.0*self.vertical_wall_thickness, self.horizontal_wall_thickness, "light yellow horizontal wall.png")
        bottom_wall.init_position(self.width*0.10-self.vertical_wall_thickness, self.height*0.90)

        left_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.80, "light yellow vertical wall.png")
        left_wall.init_position(self.width*0.10-self.vertical_wall_thickness, self.height*0.10)

        upper_right_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.45, "light yellow vertical wall.png")
        upper_right_wall.init_position(self.width*0.90, self.height*0.10)

        lower_right_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.10, "light yellow vertical wall.png")
        lower_right_wall.init_position(self.width*0.90, self.height*0.80)

        self.obj_group.add(top_block, bottom_block, left_block, right_block, vertical_block, upper_stair_railing, lower_stair_railing,
                           top_wall, bottom_wall, left_wall, upper_right_wall, lower_right_wall)
        
        ## ---SET POSITION AND PATROL ROUTE FOR THE ENEMIES ##
        #self._formation1()
        #Hmm, I think ^writing code like this line^ in an Area's __init__ function for establishing
        #enemy patrols is only necessary if it's the absolute first place you start in the whole game...

        '''
        rb = RubberBandPickUp()
        rb.init_position(self.width*0.60, self.height*0.60)
        self.obj_group.add(rb)

        wb = WaterBalloonPickUp()
        wb.init_position(self.width*0.70, self.height*0.70)
        self.obj_group.add(wb)

        wb = WaterBalloonPickUp()
        wb.init_position(self.width*0.10, self.height*0.80)
        self.obj_group.add(wb)

        straw = StrawPickUp()
        straw.init_position(self.width*0.25, self.height*0.80)
        self.obj_group.add(straw)
        '''
            
    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "peach background.png")
        self.obj_group.draw(window)

        between_stairs = pygame.Rect((self.width*0.10, self.height*0.10), (self.width*0.20, self.height*0.45))
        pygame.draw.rect(window, LIGHT_GRAY, between_stairs)
        
        stairs_to_floor2 = pygame.Rect((self.width*0.30, self.height*0.10), (self.width*0.30, self.height*0.20))
        pygame.draw.rect(window, PEACH_PUFF, stairs_to_floor2)
        
        lower_stairs = pygame.Rect((self.width*0.30, self.height*0.35), (self.width*0.30, self.height*0.20))
        pygame.draw.rect(window, PEACH_PUFF, lower_stairs)

        '''
        upper_rug = pygame.Rect((self.width*0.40, self.height*0.70), (self.width*0.35, self.height*0.05))
        pygame.draw.rect(window, LIGHT_BLUE, upper_rug)
        
        lower_rug = pygame.Rect((self.width*0.45, self.height*0.80), (self.width*0.20, self.height*0.05))
        pygame.draw.rect(window, BROWN, lower_rug)
        '''
        pygame.draw.line(window, BLACK, (self.width*0.36, self.height*0.10), (self.width*0.36, self.height*0.30), self.stair_bar_thickness) #upper left stair bar
        pygame.draw.line(window, BLACK, (self.width*0.42, self.height*0.10), (self.width*0.42, self.height*0.30), self.stair_bar_thickness) #second upper stair bar
        pygame.draw.line(window, BLACK, (self.width*0.48, self.height*0.10), (self.width*0.48, self.height*0.30), self.stair_bar_thickness) #third upper stair bar
        pygame.draw.line(window, BLACK, (self.width*0.54, self.height*0.10), (self.width*0.54, self.height*0.30), self.stair_bar_thickness) #upper right stair bar

        pygame.draw.line(window, BLACK, (self.width*0.36, self.height*0.35), (self.width*0.36, self.height*0.55), self.stair_bar_thickness) #lower left stair bar
        pygame.draw.line(window, BLACK, (self.width*0.42, self.height*0.35), (self.width*0.42, self.height*0.55), self.stair_bar_thickness) #second lower stair bar
        pygame.draw.line(window, BLACK, (self.width*0.48, self.height*0.35), (self.width*0.48, self.height*0.55), self.stair_bar_thickness) #third lower stair bar
        pygame.draw.line(window, BLACK, (self.width*0.54, self.height*0.35), (self.width*0.54, self.height*0.55), self.stair_bar_thickness) #lower right stair bar

        pygame.draw.line(window, WOODEN, (self.width*0.40, self.height*0.90), (self.width*0.60, self.height*0.90), self.inner_door_thickness) #finish line door
        
        window.blit(pygame.font.SysFont("Arial", 30).render("FLOOR 1", 1, BLACK), (self.width*0.80, self.height*0.85))
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.topright[0] >= self.width*0.90+self.vertical_wall_thickness and self.player_obj.rect.centery >= self.height*0.55
                  and self.player_obj.rect.centery <= self.height*0.80 and self.player_obj.moving_east):
                print("in 1_2")
                new_area = self._make_transition(40, self.height*0.675, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()
                

            elif (self.player_obj.rect.topright[0] >= self.width*0.60 and self.player_obj.rect.topright[0] <= self.width*0.65 and self.player_obj.rect.centery >= self.height*0.10
                  and self.player_obj.rect.centery <= self.height*0.30 and self.player_obj.moving_east):
                #Perhaps I can say if you have the key, then transition. Else, play a bumping sound.
                if self.player_obj.has_floor2_card_key:
                    print("in 2_1")
                    new_area = self._make_transition(self.width*0.10+70, self.height*0.65, area_dict, "inner1") #+40 original
                    #new_area._reset_enemy_state()
                    #new_area._formation1()
                else:
                    if not pygame.mixer.get_busy():
                        denied = pygame.mixer.Sound("denied.wav")
                        pygame.mixer.Sound.play(denied)

            elif (self.player_obj.rect.bottomleft[1] >= self.height*0.90 and self.player_obj.rect.centerx <= self.width*0.60
                  and self.player_obj.rect.centerx >= self.width*0.40 and self.player_obj.moving_south):
                if self.player_obj.dropped_off_data_disc:
                    self.player_obj.reached_end_of_game = True
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
                    

class Area1_2(area_base.Area):
    '''A class to represent Area1_2 of DBH.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: ["Enemy"]=None):
        '''Initializes the attributes of an Area1_2 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_right_block = Block(LIGHT_YELLOW, self.width*0.60, self.height*0.10, "light yellow small horizontal.png")
        upper_right_block.init_position(self.width*0.40, 0)
        
        lower_right_block = Block(GREENISH_GRAY, self.width*0.20, self.height*0.50, "greenish gray small semi vertical.png")
        lower_right_block.init_position(self.width*0.80, self.height*0.50)

        top_wall = Block(LIGHT_YELLOW, self.width*0.05, self.height*0.02, "light yellow horizontal wall.png")
        top_wall.init_position(0, 0)

        upper_left_wall = Block(LIGHT_YELLOW, self.width*0.02, self.height*0.53, "light yellow vertical wall.png")
        upper_left_wall.init_position(0, self.height*0.02)

        lower_left_wall = Block(LIGHT_YELLOW, self.width*0.02, self.height*0.20, "light yellow vertical wall.png")
        lower_left_wall.init_position(0, self.height*0.80)
        
        self.obj_group.add(upper_right_block, lower_right_block, top_wall, upper_left_wall, lower_left_wall)

        #AREA 1_2 PHYSICAL OBJECT PLACEMENTS
        blue_chair1 = physical_objs.BlueChair("south")
        blue_chair1.init_position(self.width*0.40, self.height*0.095)
        blue_chair2 = physical_objs.BlueChair("south")
        blue_chair2.init_position(self.width*0.47, self.height*0.095)
        blue_chair3 = physical_objs.BlueChair("south")
        blue_chair3.init_position(self.width*0.54, self.height*0.095)

        self.obj_group.add(blue_chair1, blue_chair2, blue_chair3)

        green_chair1 = physical_objs.GreenChair("north")
        green_chair1.init_position(self.width*0.03, self.height*0.90)

        green_chair2 = physical_objs.GreenChair("north")
        green_chair2.init_position(self.width*0.11, self.height*0.90)

        green_chair3 = physical_objs.GreenChair("north")
        green_chair3.init_position(self.width*0.43, self.height*0.90)

        green_chair4 = physical_objs.GreenChair("north")
        green_chair4.init_position(self.width*0.51, self.height*0.90)

        green_chair5 = physical_objs.GreenChair("west")
        green_chair5.init_position(self.width*0.728, self.height*0.50)

        green_chair6 = physical_objs.GreenChair("west")
        green_chair6.init_position(self.width*0.728, self.height*0.61)

        self.obj_group.add(green_chair1, green_chair2, green_chair3, green_chair4, green_chair5, green_chair6)


        brown_chair1 = physical_objs.BrownSofaChair("north")
        brown_chair1.init_position(self.width*0.23, self.height*0.90)
        
        brown_chair2 = physical_objs.BrownSofaChair("north")
        brown_chair2.init_position(self.width*0.31, self.height*0.90)

        brown_chair3 = physical_objs.BrownSofaChair("north")
        brown_chair3.init_position(self.width*0.64, self.height*0.90)

        brown_chair4 = physical_objs.BrownSofaChair("north")
        brown_chair4.init_position(self.width*0.71, self.height*0.90)
        
        self.obj_group.add(brown_chair1, brown_chair2, brown_chair3, brown_chair4)


        rounded_edge_table = physical_objs.RoundedEdgeTable("horizontal")
        rounded_edge_table.init_position(self.width*0.35, self.height*0.55)
        self.obj_group.add(rounded_edge_table)

    #vu -- start of Enemies' patrol routes for area 1_2
    #From 1_1 (west)
    def _formation1(self):
        if self.e_group != None:
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2

    #From 1_5 (north)
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2

    #From 1_3 (east)
    def _formation3(self):
        if self.e_group != None:
            self.gen_patrol_route5(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route6(list(self.e_group)[1]) #Enemy2
            
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.20, self.height*0.70)
            enemy._looking_north = True
            enemy.patrol_route = [("go_north", 30), ("look_south", 20), ("go_north", 40),
                                   ("look_north", 15), ("go_south", 80), ("wait", 10), ("end", 0)]

    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.65, self.height*0.30)
            enemy._looking_west = True
            enemy.patrol_route = [("go_west", 30), ("look_east", 20),
                                  ("look_south", 20), ("look_west", 15), ("go_east", 20),
                                   ("look_north", 15), ("look_east", 15), ("look_south", 15), ("end", 0)]
            
    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.15, self.height*0.80)
            enemy._looking_south = True
            '''
            enemy.patrol_route = [("look_south", 30), ("go_north", 40), ("look_north", 15), ("go_south", 30),
                                  ("look_east", 15), ("end", 0)]
            '''
            enemy.patrol_route = [("look_south", 30), ("look_east", 30), ("go_north", 40), ("look_north", 15), ("go_south", 30),
                                  ("look_east", 15), ("end", 0)]

    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.65, self.height*0.30)
            enemy._looking_west = True
            enemy.patrol_route = [("go_west", 15), ("look_east", 20),
                                  ("look_south", 15), ("look_west", 15), ("go_east", 15),
                                   ("look_north", 15), ("look_east", 15), ("look_south", 15), ("wait", 10), ("end", 0)]

    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.15, self.height*0.80)
            enemy._looking_north = True
            enemy.patrol_route = [("go_north", 70), ("look_west", 10), ("look_east", 10),
                                  ("look_north", 15), ("wait", 10), ("look_south", 15), ("go_south", 70),
                                   ("look_north", 15), ("look_east", 15), ("wait", 10), ("end", 0)]

    def gen_patrol_route6(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.62, self.height*0.30)
            enemy._looking_west = True
            enemy.patrol_route = [("go_west", 20), ("look_east", 20), ("look_west", 15),
                                  ("look_north", 15), ("look_south", 15), ("go_east", 20),
                                   ("look_north", 15), ("look_east", 15), ("end", 0)]
            
    #vu -- end of Enemies' patrol routes for area 1_2
            

    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "peach background.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.65, self.height*0.10), (self.width*0.85, self.height*0.10), self.inner_door_thickness) #upper right inner door


    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.55
                and self.player_obj.rect.centery <= self.height*0.80 and self.player_obj.moving_west):
                print("in 1_1")
                new_area = self._make_transition(self.width*0.90+self.vertical_wall_thickness-50, self.height*0.675, area_dict, "west1")
                #new_area._reset_enemy_state()
                #new_area._formation1()
                

            elif (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.10
                  and self.player_obj.rect.centery <= self.height*0.50 and self.player_obj.moving_east):
                print("in 1_3")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.05
                and self.player_obj.rect.centerx <= self.width*0.40 and self.player_obj.moving_north):
                print("in 1_5")
                new_area = self._make_transition(self.player_obj.rect.centerx+self.width*0.55, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()

                
            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

        return new_area


class Area1_3(area_base.Area):
    '''A class to represent Area1_3 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_3 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = True ##FOR CHECKPOINTS

        bottom_left_block = Block(LIGHT_YELLOW, self.width*0.30, self.height*0.50, "light yellow small semi vertical.png")
        bottom_left_block.init_position(0, self.height*0.50)
        
        upper_left_block = Block(LIGHT_YELLOW, self.width*0.20, self.height*0.10, "light yellow small horizontal.png")
        upper_left_block.init_position(0, 0)
        
        upper_middle_block = Block(LIGHT_YELLOW, self.width*0.30, self.height*0.10, "light yellow small horizontal.png")
        upper_middle_block.init_position(self.width*0.20, 0)
        
        upper_right_block = Block(BRICK, self.width*0.50, self.height*0.20, "brick big horizontal.png")
        upper_right_block.init_position(self.width*0.50, 0)

        bottom_wall = Block(LIGHT_YELLOW, self.width*0.70, self.height*0.02, "light yellow horizontal wall.png")
        bottom_wall.init_position(self.width*0.30, self.height*0.98)
        
        right_wall = Block(LIGHT_YELLOW, self.width*0.02, self.height*0.38, "light yellow vertical wall.png")
        right_wall.init_position(self.width*0.98, self.height*0.60)

        self.obj_group.add(bottom_left_block, upper_left_block, upper_middle_block, upper_right_block, bottom_wall, right_wall)

        #AREA 1_3 PHYSICAL OBJECT PLACEMENTS
        copier1 = physical_objs.Copier()
        copier1.init_position(self.width*0.40, self.height*0.40)

        copier2 = physical_objs.Copier()
        copier2.init_position(self.width*0.40, self.height*0.70)

        copier3 = physical_objs.Copier()
        copier3.init_position(self.width*0.70, self.height*0.40)

        copier4 = physical_objs.Copier()
        copier4.init_position(self.width*0.70, self.height*0.70)

        self.obj_group.add(copier1, copier2, copier3, copier4)
        
    #vu -- start of Enemies' patrol routes for area 1_3
    #From 1_2
    def _formation1(self):
        if self.e_group != None:
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2

    #From 1_4
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2

    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            #enemy.assigned = True  #LOS STUFF. No need.
            enemy.init_position(self.width*0.60, self.height*0.85)
            #enemy.set_los(150, 500) #LOS STUFF. No need.
            enemy._looking_north = True
            enemy.patrol_route = [("go_north", 35), ("look_south", 15), ("look_west", 10), ("look_east", 15), ("wait", 10),
                                  ("look_north", 15), ("wait", 10), ("go_north", 35), ("look_south", 15), ("look_west", 10), ("look_east", 10),
                                  ("go_south", 70), ("look_north", 15), ("look_east", 15), ("wait", 10), ("end", 0)]

    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.85, self.height*0.85)
            enemy._looking_north = True
            enemy.patrol_route = [("go_north", 70), ("look_west", 10), ("look_east", 10),
                                  ("look_north", 15), ("wait", 20), ("look_south", 15), ("go_south", 70),
                                   ("look_north", 15), ("look_east", 15), ("wait", 20), ("end", 0)]

    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            #enemy.assigned = True  #LOS STUFF. No need.
            enemy.init_position(self.width*0.60, self.height*0.85)
            #enemy.set_los(150, 500) #LOS STUFF. No need.
            enemy._looking_north = True
            enemy.patrol_route = [("go_north", 35), ("look_south", 10), ("look_west", 10),
                                  ("look_north", 15), ("wait", 10), ("go_north", 35), ("look_south", 15), ("look_west", 10), ("look_east", 10),
                                  ("go_south", 70), ("look_north", 15), ("look_east", 15), ("wait", 10), ("end", 0)]

    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.20, self.height*0.30)
            enemy._looking_east = True
            enemy.patrol_route = [("go_east", 70), ("look_west", 10), ("look_east", 10), ("wait", 20),
                                  ("look_north", 15), ("look_south", 15), ("go_west", 70),
                                   ("look_north", 15), ("look_east", 15), ("look_south", 15), ("wait", 20), ("end", 0)]
            
     #vu -- end of Enemies' patrol for area 1_3
        
    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.05, self.height*0.50), (self.width*0.25, self.height*0.50), self.inner_door_thickness) #Bottom left inner door
        pygame.draw.line(window, PINK, (self.width*0.25, self.height*0.10), (self.width*0.45, self.height*0.10), self.inner_door_thickness) #Upper left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.65, self.height*0.20), (self.width*0.85, self.height*0.20), self.inner_door_thickness) #Upper right inner door


    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.10
                and self.player_obj.rect.centery <= self.height*0.50 and self.player_obj.moving_west):
                print("in 1_2")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation3()


            elif (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.20
                  and self.player_obj.rect.centery <= self.height*0.60 and self.player_obj.moving_east):
                print("in 1_4")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()

            elif (self.player_obj.rect.topright[1] <= self.height*0.10 and self.player_obj.rect.centerx >= self.width*0.25
                  and self.player_obj.rect.centerx <= self.width*0.45 and self.player_obj.moving_north):
                print("in 1_3_upper_left_inner")
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


class Area1_3_UpperLeftInnerArea(area_base.Area):
    '''A class to represent an upper inner Area of Area1_3.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_7_UpperInnerArea object.'''
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

        window.blit(pygame.font.SysFont("Arial", 50).render("Spotted?", 1, BLACK), (self.width*0.45, self.height*0.48))
        window.blit(pygame.font.SysFont("Arial", 50).render("Wait for the *ding*!", 1, BLACK), (self.width*0.37, self.height*0.53))

        
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
                print("in 1_3")
                new_area = self._make_transition(self.width*0.35, self.height*0.20+5, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area

class Area1_4(area_base.Area):
    '''A class to represent Area1_4 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_4 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_block = Block(BRICK, self.width, self.height*0.20, "brick big horizontal.png")
        upper_block.init_position(0, 0)

        lower_block = Block(LIGHT_YELLOW, self.width, self.height*0.40, "light yellow big horizontal.png")
        lower_block.init_position(0, self.height*0.60)
        
        hallway_end = Block(LIGHT_YELLOW, self.width*0.05, self.height*0.40, "light yellow vertical wall.png")
        hallway_end.init_position(self.width*0.95, self.height*0.20)
        
        self.obj_group.add(upper_block, lower_block, hallway_end)

        mgs1_game = MGS1()
        mgs1_game.init_position(self.width*0.90, self.height*0.55)
        self.obj_group.add(mgs1_game)
        

    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here?
            #list(self.e_group)[1].keeps_distance = True #Configure AI settings here?
            self.gen_patrol_route1(list(self.e_group)[0])
            self.gen_patrol_route2(list(self.e_group)[1])
            

    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.25, self.height*0.30)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 15), ("look_south", 10), ("look_west", 10), ("look_south", 10), ("end", 0)]


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.70, self.height*0.30)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 15), ("look_west", 10), ("look_south", 10), ("look_east", 10), ("end", 0)]


            
    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.20, self.height*0.60), (self.width*0.40, self.height*0.60), self.inner_door_thickness) #inner door
        

    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.20
                and self.player_obj.rect.centery <= self.height*0.60 and self.player_obj.moving_west):
                print("in 1_3")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation2()


        self._handle_corners_and_boundaries()

        #For resetting the ticks to safety. This is for Areas right next to safe havens
        if new_area != old_area and old_area.is_safe_haven:
            old_area.ticks = 0

        #FOR PROJECTICLES
        self._clean_up_attack_objects(new_area, old_area)

        return new_area


class Area1_5(area_base.Area):
    '''A class to represent Area1_5 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_5 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False

        upper_left_block = Block(LIGHT_YELLOW, self.width*0.60, self.height*0.40, "light yellow big semi horizontal.png")
        upper_left_block.init_position(0, 0)

        bar = Block(LIGHT_YELLOW, self.width*0.05, self.height*0.70, "light yellow vertical wall.png")
        bar.init_position(self.width*0.95, self.height*0.30)

        hallway_end = Block(LIGHT_YELLOW, self.width*0.05, self.height*0.60, "light yellow vertical wall.png")
        hallway_end.init_position(0, self.height*0.40)

        elevator_wall = Block(LIGHT_YELLOW, self.width*0.10, self.height*0.30, "light yellow small semi vertical.png")
        elevator_wall.init_position(self.width*0.50, self.height*0.70)
        
        elevator = Block(LIGHT_GRAY, self.width*0.45, self.height*0.30)
        elevator.init_position(self.width*0.05, self.height*0.70)
        
        self.obj_group.add(upper_left_block, bar, hallway_end, elevator_wall, elevator)
        
        
    #vu -- start of Enemies' patrol for area 1_5       
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2

    def _formation2(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route2(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2

    def _formation3(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2

    def _formation4(self):
        if self.e_group != None:
            self.gen_patrol_route5(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route6(list(self.e_group)[1]) #Enemy2            
    
            
    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.78, self.height*0.25)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 15), ("go_south", 75), ("look_west", 10), ("look_east", 10),
                                  ("look_south", 15), ("wait", 10), ("look_north", 15), ("go_north", 75),
                                   ("look_south", 15), ("look_east", 15), ("wait", 10), ("end", 0)]

    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            #enemy.assigned = True  #LOS STUFF. No need.
            enemy.init_position(self.width*0.78, self.height*0.70)
            #enemy.set_los(150, 500) #LOS STUFF. No need.
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 15), ("go_north", 30), ("look_west", 10), ("look_east", 10), ("wait", 10), ("look_south", 15),
                                  ("go_north", 30), ("look_west", 15), ("look_east", 10), ("look_south", 10), ("look_north", 10),
                                  ("go_south", 30), ("look_north", 10), ("wait", 10), ("look_west", 15), ("wait", 10), ("look_east", 10),
                                  ("look_south", 10), ("go_south", 30), ("wait", 10), ("look_north", 10), ("wait", 10), ("look_west", 15),
                                  ("wait", 10), ("look_east", 10), ("look_south", 10), ("end", 0)]


    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            #enemy.assigned = True  #LOS STUFF. No need.
            enemy.init_position(self.width*0.78, self.height*0.70)
            #enemy.set_los(150, 500) #LOS STUFF. No need.
            enemy._looking_north = True
            enemy.patrol_route = [("go_north", 30), ("look_west", 10), ("look_east", 10), ("wait", 10), ("look_south", 15),
                                  ("go_north", 30), ("look_west", 15), ("look_east", 10), ("look_south", 10), ("look_north", 10),
                                  ("go_south", 30), ("look_north", 10), ("wait", 10), ("look_west", 15), ("wait", 10), ("look_east", 10),
                                  ("look_south", 10), ("go_south", 30), ("wait", 10), ("look_north", 10), ("wait", 10), ("look_west", 15),
                                  ("wait", 10), ("look_east", 10), ("look_south", 10), ("end", 0)]


    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.25, self.height*0.55)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 15), ("look_west", 10), ("look_north", 10), ("wait", 10), ("look_south", 15), ("end", 0)]


    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.65, self.height*0.55)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 8), ("go_south", 50), ("look_south", 16),
                                  ("look_east", 15), ("go_north", 50), ("end", 0)]


    def gen_patrol_route6(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.72, self.height*0.55)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 8), ("go_north", 50), ("look_north", 16),
                                  ("look_west", 15), ("go_south", 50), ("end", 0)]

    
    #vu -- end of Enemies' patrol for area 1_5

        
    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "peach background.png")
        self.obj_group.draw(window)
        
        #pygame.draw.line(window, LIGHT_GRAY, (self.width*0.95, self.height*0.50), (self.width*0.95, self.height*0.65), self.inner_door_thickness) # upper TV
        #pygame.draw.line(window, LIGHT_GRAY, (self.width*0.95, self.height*0.70), (self.width*0.95, self.height*0.85), self.inner_door_thickness) # lower TV

        pygame.draw.line(window, BLACK, (self.width*0.275, self.height*0.70), (self.width*0.275, self.height), 10) #elevator division
                      

    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        #print("Snake's Health: ", self.player_obj.health)
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.60
                and self.player_obj.rect.centerx <= self.width and self.player_obj.moving_north):
                print("in 1_9")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()

                
            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.60
                  and self.player_obj.rect.centerx <= self.width*0.95 and self.player_obj.moving_south):
                print("in 1_2")
                new_area = self._make_transition(self.player_obj.rect.centerx-self.width*0.55, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation2()

                
            elif (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= 0
                  and self.player_obj.rect.centery <= self.height*0.30 and self.player_obj.moving_east):
                print("in 1_5_bathroom_entrances")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()

                
            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area
    

class Area1_5_BathroomEntrances(area_base.Area):
    '''A class to represent the entrances to the bathrooms adjacent to Area1_5'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_5_BathroomEntrances object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_block = Block(DARK_TEAL, self.width*0.70, self.height*0.30, "dark teal big horizontal.png")
        upper_block.init_position(self.width*0.30, 0)

        lower_block = Block(LIGHT_YELLOW, self.width, self.height*0.70, "light yellow big semi horizontal.png")
        lower_block.init_position(0, self.height*0.30)

        self.obj_group.add(upper_block, lower_block)


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

        pygame.draw.line(window, PINK, (self.width*0.05, self.height*0.30), (self.width*0.25, self.height*0.30), self.inner_door_thickness) #door to girl's bathroom

        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= 0
                and self.player_obj.rect.centery <= self.height*0.30 and self.player_obj.moving_west):
                print("in 1_5")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation3()


            elif (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= 0
                and self.player_obj.rect.centerx <= self.width*0.30 and self.player_obj.moving_north):
                print("in 1_8")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.bottomleft[1] >= self.height*0.30 and self.player_obj.rect.bottomleft[0] >= self.width*0.045
                  and self.player_obj.rect.bottomright[0] <= self.width*0.255 and self.player_obj.moving_south):
                print("in 1_5_girls_bathroom")
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


class Area1_5_GirlsBathroom(area_base.Area):
    '''A class to represent the girl's bathroom adjacent to Area1_5'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_5_GirlsBathroom object.'''
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
                print("in 1_5_bathroom_entrances")
                new_area = self._make_transition(self.width*0.15, self.height*0.30-70, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area

    
class Area1_6(area_base.Area):
    '''A class to represent Area1_6 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_6 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        left_block = Block(LIGHT_YELLOW, self.width*0.10, self.height, "light yellow big vertical.png")
        left_block.init_position(0, 0)
        
        upper_right_block = Block(LIGHT_YELLOW, self.width*0.55, self.height*0.60, "light yellow big square.png")
        upper_right_block.init_position(self.width*0.45, 0)
        
        lower_right_block = Block(LIGHT_YELLOW, self.width*0.55, self.height*0.40, "light yellow big semi horizontal.png")
        lower_right_block.init_position(self.width*0.45, self.height*0.60)
        
        hallway_end = Block(LIGHT_YELLOW, self.width*0.35, self.height*0.05, "light yellow horizontal wall.png")
        hallway_end.init_position(self.width*0.10, self.height*0.95)
        
        self.obj_group.add(left_block, upper_right_block, lower_right_block, hallway_end)

        straw = StrawPickUp()
        straw.init_position(self.width*0.10, self.height*0.88)
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
        
        pygame.draw.line(window, WOODEN, (self.width*0.45, self.height*0.35), (self.width*0.45, self.height*0.55), self.inner_door_thickness) #Upper inner door
        pygame.draw.line(window, PINK, (self.width*0.10, self.height*0.50), (self.width*0.10, self.height*0.70), self.inner_door_thickness) #left inner door
        pygame.draw.line(window, BLACK, (self.width*0.45, self.height*0.70), (self.width*0.45, self.height*0.90), self.inner_door_thickness) #lower inner door

        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.y <= 0 and self.player_obj.rect.centerx >= self.width*0.10
                and self.player_obj.rect.centerx <= self.width*0.45 and self.player_obj.moving_north):
                print("in 1_10")
                new_area = self._make_transition(self.player_obj.rect.centerx, self.height-40, area_dict, "north1")
                new_area._reset_enemy_state()
                new_area._formation2()
            elif (self.player_obj.rect.topright[0] >= self.width*0.45 and self.player_obj.rect.centery >= self.height*0.70
                  and self.player_obj.rect.centery <= self.height*0.90 and self.player_obj.moving_east):
                print("in 1_6_lower_right_inner")
                new_area = self._make_transition(40, self.height*0.50, area_dict, "inner1")
                #new_area._reset_enemy_state()
                #new_area._formation1()
            elif (self.player_obj.rect.x <= self.width*0.10 and self.player_obj.rect.centery >= self.height*0.50
                and self.player_obj.rect.centery <= self.height*0.75 and self.player_obj.moving_west):
                print("in 1_6_left_inner")
                new_area = self._make_transition(self.width-40, self.height*0.50, area_dict, "inner2")
                new_area._reset_enemy_state()
                new_area._formation1()

            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area

class Area1_6_LowerRightInnerArea(area_base.Area):
    '''A class to represent an inner Area of Area1_6'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area2_4_UpperRightInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False
        self._draw_east_inner_room()

        noodles = InstantNoodlesPickUp()
        noodles.init_position(self.width/2, self.height/2)
        self.obj_group.add(noodles)

               
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
                print("in 1_6")
                new_area = self._make_transition(self.width*0.45-40, self.height*0.80, area_dict, "west1")
                #new_area._reset_enemy_state()
                #new_area._formation3()

                
            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area1_6_LeftInnerArea(area_base.Area):
    '''A class to represent an inner Area of Area1_6'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_11_InnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_safe_haven = True
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_west_inner_room()
        

    def _formation1(self):
        if self.e_group != None:
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
            if (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.35
                  and self.player_obj.rect.centery <= self.height*0.65 and self.player_obj.moving_east):
                print("in 1_6")
                new_area = self._make_transition(self.width*0.10+50, self.height*0.60, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area1_7(area_base.Area):
    '''A class to represent Area1_7 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_7 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_left_block = Block(LIGHT_YELLOW, self.width*0.10, self.height*0.20, "light yellow small square.png")
        upper_left_block.init_position(0, 0)
        
        upper_right_block = Block(LIGHT_YELLOW, self.width*0.90, self.height*0.20, "light yellow big horizontal.png")
        upper_right_block.init_position(self.width*0.10, 0)
        
        lower_left_block = Block(LIGHT_YELLOW, self.width*0.25, self.height*0.40, "light yellow small semi vertical.png")
        lower_left_block.init_position(0, self.height*0.60)
        
        lower_right_block = Block(LIGHT_YELLOW, self.width*0.75, self.height*0.45, "light yellow big semi horizontal.png")
        lower_right_block.init_position(self.width*0.25, self.height*0.55)
        
        hallway_end = Block(LIGHT_YELLOW, self.width*0.05, self.height*0.35, "light yellow vertical wall.png")
        hallway_end.init_position(self.width*0.95, self.height*0.20)
        
        self.obj_group.add(upper_left_block, upper_right_block, lower_left_block, lower_right_block, hallway_end)


    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*0.90, self.height*0.28)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 20), ("look_west", 15), ("end", 0)]


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, BLACK, (self.width*0.40, self.height*0.20), (self.width*0.60, self.height*0.20), self.inner_door_thickness) #upper inner door
        pygame.draw.line(window, WOODEN, (self.width*0.55, self.height*0.55), (self.width*0.75, self.height*0.55), self.inner_door_thickness) #lower inner door

        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.20
                and self.player_obj.rect.centery <= self.height*0.60 and self.player_obj.moving_west):
                print("in 1_8")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation2()


            elif (self.player_obj.rect.y <= self.height*0.20 and self.player_obj.rect.x >= self.width*0.395
                and self.player_obj.rect.topright[0] <= self.width*0.605 and self.player_obj.moving_north):
                print("in 1_7_upper_inner_entrance")
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


class Area1_7_UpperInnerArea(area_base.Area):
    '''A class to represent an upper inner Area of Area1_7.'''
    
    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_7_UpperInnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_north_inner_room()

        rb = RubberBandPickUp()
        rb.init_position(self.width/2, self.height/2)
        self.obj_group.add(rb)        

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
                print("in 1_7")
                new_area = self._make_transition(self.width*0.50, self.height*0.20+70, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area1_8(area_base.Area):
    '''A class to represent Area1_8 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_8 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_left_block = Block(LIGHT_YELLOW, self.width*0.20, self.height*0.20, "light yellow small square.png")
        upper_left_block.init_position(0, 0)
        
        upper_right_block = Block(LIGHT_YELLOW, self.width*0.80, self.height*0.20, "light yellow big horizontal.png")
        upper_right_block.init_position(self.width*0.20, 0)
        
        lower_left_block = Block(DARK_TEAL, self.width*0.75, self.height*0.10, "dark teal small horizontal.png")
        lower_left_block.init_position(0, self.height*0.60)

        lower_middle_block = Block(DARK_TEAL, self.width*0.45, self.height*0.30, "dark teal small semi horizontal.png")
        lower_middle_block.init_position(self.width*0.30, self.height*0.70)
        
        lower_right_block = Block(LIGHT_YELLOW, self.width*0.25, self.height*0.40, "light yellow small semi vertical.png")
        lower_right_block.init_position(self.width*0.75, self.height*0.60)
        
        self.obj_group.add(upper_left_block, upper_right_block, lower_left_block, lower_middle_block, lower_right_block)
        

    ### Kha area1_8
    # formation when Snake comes from area1_9
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2

    # formation when Snake comes from area1_7
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.20, self.height*.35)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 15), ("look_west", 10), ("look_north", 10),                                 
                                  ("look_east", 15), ("end", 0)]


    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.80, self.height*.35)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 15), ("look_east", 10), ("look_north", 10),                                 
                                  ("look_west", 15), ("end", 0)]
            
    ### end Kha area1_8


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)

        pygame.draw.line(window, BLACK, (self.width*0.05, self.height*0.70), (self.width*0.25, self.height*0.70), self.inner_door_thickness) #door to boys' bathroom
        
        pygame.draw.line(window, WOODEN, (self.width*0.35, self.height*0.20), (self.width*0.55, self.height*0.20), self.inner_door_thickness) #upper inner door
        pygame.draw.line(window, WOODEN, (self.width*0.77, self.height*0.60), (self.width*0.97, self.height*0.60), self.inner_door_thickness) #lower inner door

        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.x <= 0 and ((self.player_obj.rect.centery >= self.height*0.20
                and self.player_obj.rect.centery <= self.height*0.60) or (self.player_obj.rect.centery >= self.height*0.70
                and self.player_obj.rect.centery <= self.height)) and self.player_obj.moving_west):
                print("in 1_9")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation2()
                #new_area._formation1()
                

            elif (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.20
                  and self.player_obj.rect.centery <= self.height*0.60 and self.player_obj.moving_east):
                print("in 1_7")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()

            elif (self.player_obj.rect.y <= self.height*0.70 and self.player_obj.rect.y >= self.height*0.60 and self.player_obj.rect.x >= self.width*0.045
                and self.player_obj.rect.topright[0] <= self.width*0.255 and self.player_obj.moving_north):
                print("in 1_8_boys_bathroom")
                new_area = self._make_transition(self.width*0.35, self.height*0.75-70, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()

            elif (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= 0
                  and self.player_obj.rect.centerx <= self.width*0.30 and self.player_obj.moving_south):
                print("in 1_5_bathroom_entrances")
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


class Area1_8_BoysBathroom(area_base.Area):
    '''A class to represent the boy's bathroom adjacent to Area1_8'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_8_BoysBathroom object.'''
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
                print("in 1_8")
                new_area = self._make_transition(self.width*0.15, self.height*0.70+70, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area1_9(area_base.Area): #zazaza
    '''A class to represent Area1_9 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_9 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_left_block = Block(LIGHT_YELLOW, self.width*0.35, self.height*0.20, "light yellow small semi horizontal.png")
        upper_left_block.init_position(0, 0)
        
        upper_right_block = Block(LIGHT_YELLOW, self.width*0.65, self.height*0.20, "light yellow big horizontal.png")
        upper_right_block.init_position(self.width*0.35, 0)
        
        lower_left_block = Block(BRICK, self.width*0.60, self.height*0.20, "brick big horizontal.png")
        lower_left_block.init_position(0, self.height*0.80)
        
        #lower_right_block = Block(DARK_TEAL, self.width*0.05, self.height*0.10, "dark teal small vertical.png")
        lower_right_block = Block(DARK_TEAL, self.width*0.07, self.height*0.10, "dark teal small vertical.png")
        lower_right_block.init_position(self.width*0.95, self.height*0.60)

        '''
        drinking_fountain = Block(GRAY, self.width*0.05, self.height*0.20)
        drinking_fountain.init_position(0, self.height*0.60)
        '''
        
        pole = Block(LIGHT_YELLOW, self.width*0.15, self.height*0.15, "light yellow medium square.png")
        #pole = Block(LIGHT_YELLOW, self.width*0.10, self.height*0.115, "light yellow medium square.png")
        pole.init_position(self.width*0.50, self.height*0.42)

        '''
        bottom_left_block = Block(LIGHT_YELLOW, self.width*0.08, self.height*0.06)
        bottom_left_block.init_position(0, self.height*0.73)
        '''
        
        self.obj_group.add(upper_left_block, upper_right_block, lower_left_block, lower_right_block, pole)

        '''
        #trash_can = Block(GREEN, self.width*0.08, self.height*0.10, "trash can.png")
        trash_can = physical_objs.TrashCan()
        trash_can.init_position(self.width*0.45, self.height*0.45)
        self.obj_group.add(trash_can)
        '''
        
        water_fountain1 = physical_objs.WaterFountain("east")
        water_fountain1.init_position(0, self.height*0.60)
        self.obj_group.add(water_fountain1)

        water_fountain2 = physical_objs.WaterFountain("east")
        water_fountain2.init_position(0, self.height*0.70)
        self.obj_group.add(water_fountain2)

    ### Kha area1_9
    # formation when Snake comes from area1_5
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route4(list(self.e_group)[2]) #Enemy3
    '''
    # formation when Snake comes from 1_10
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route2(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route4(list(self.e_group)[2]) #Enemy3
    '''
    # formation when Snake comes from 1_8
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route5(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route6(list(self.e_group)[2]) #Enemy3


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
     # Enemy #1 when Snake comes from area1_5, 1_8, 1_10
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.2, self.height*.7)
            enemy._looking_north = True
            enemy.patrol_route = [("go_north", 55), ("look_west", 10), ("look_east", 10),
                                  ("look_north", 15), ("wait", 10), ("look_south", 15), ("go_south", 55),
                                   ("look_north", 15), ("look_east", 15), ("look_west", 15), ("wait", 10), ("end", 0)]

    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.75, self.height*.3)
            enemy._looking_west = True
            enemy.patrol_route = [("go_west", 90), ("look_north", 10), ("look_east", 10),
                                  ("look_south", 15), ("look_west", 15), ("go_east", 90),
                                   ("look_north", 15), ("look_east", 15), ("look_south", 15), ("wait", 10), ("end", 0)]

    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.8, self.height*.9)
            enemy._looking_north = True
            enemy.patrol_route = [("go_north", 75), ("look_west", 10), ("look_east", 10),
                                  ("look_north", 15), ("wait", 10), ("look_south", 15), ("go_south", 75),
                                   ("look_north", 15), ("look_east", 15), ("look_west", 15), ("wait", 10), ("end", 0)]

    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.8, self.height*.50)
            enemy._looking_east = True
            enemy.patrol_route = [("look_east", 15), ("look_north", 25), ("look_east", 15),
                                   ("look_west", 25), ("end", 0)]
            
    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.75, self.height*.50)
            enemy._looking_north = True
            enemy.patrol_route = [("go_north", 43), ("look_west", 10), ("look_east", 10),
                                  ("look_north", 15), ("wait", 10), ("look_south", 15), ("go_south", 43),
                                   ("look_north", 15), ("look_east", 15), ("look_west", 15), ("wait", 10), ("end", 0)]
            
    def gen_patrol_route6(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.80, self.height*.85)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 15), ("wait", 10), ("look_north", 10), ("look_east", 15),
                                   ("look_west", 10), ("end", 0)]
    ### end Kha area1_9


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.60, self.height*0.20), (self.width*0.80, self.height*0.20), self.inner_door_thickness) #upper inner door
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.60
                  and self.player_obj.rect.centerx <= self.width and self.player_obj.moving_south):
                print("in 1_5")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation2()

                
            elif (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.20
                and self.player_obj.rect.centery <= self.height*0.60 and self.player_obj.moving_west):
                print("in 1_10")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()

                
            elif (self.player_obj.rect.topright[0] >= self.width and ((self.player_obj.rect.centery >= self.height*0.20
                  and self.player_obj.rect.centery <= self.height*0.60) or (self.player_obj.rect.centery >= self.height*0.70
                  and self.player_obj.rect.centery <= self.height)) and self.player_obj.moving_east):
                print("in 1_8")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area

    
class Area1_10(area_base.Area):
    '''A class to represent Area1_10 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_10 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_left_block = Block(LIGHT_YELLOW, self.width*0.50, self.height*0.20, "light yellow small semi horizontal.png")
        upper_left_block.init_position(0, 0)
        
        upper_right_block = Block(LIGHT_YELLOW, self.width*0.50, self.height*0.20, "light yellow small semi horizontal.png")
        upper_right_block.init_position(self.width*0.50, 0)
        
        lower_left_block = Block(LIGHT_YELLOW, self.width*0.10, self.height*0.40, "light yellow small semi vertical.png")
        lower_left_block.init_position(0, self.height*0.60)
        
        lower_right_block = Block(LIGHT_YELLOW, self.width*0.55, self.height*0.40, "light yellow big semi horizontal.png")
        lower_right_block.init_position(self.width*0.45, self.height*0.60)
        
        self.obj_group.add(upper_left_block, upper_right_block, lower_left_block, lower_right_block)


    ###Kha area1_10
    # formation when Snake comes from area1_9
    def _formation1(self):
        if self.e_group != None:
            #list(self.e_group)[0].keeps_distance = True #Configure AI settings here
            self.gen_patrol_route1(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route5(list(self.e_group)[2]) #Enemy3

    # formation when Snake comes from area1_6
    def _formation2(self):
        if self.e_group != None:
            self.gen_patrol_route2(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route4(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route6(list(self.e_group)[2]) #Enemy3
            
    # formation when Snake comes from area1_11
    def _formation3(self):
        if self.e_group != None:
            self.gen_patrol_route3(list(self.e_group)[0]) #Enemy1
            self.gen_patrol_route7(list(self.e_group)[1]) #Enemy2
            self.gen_patrol_route5(list(self.e_group)[2]) #Enemy3


    #Perhaps I could set the Area attribute of Enemies here in the gen_patrol_route methods instead of in main?
    # Enemy #1 when Snake comes from area1_9
    def gen_patrol_route1(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.25, self.height*.8)
            enemy._looking_north = True
            enemy.patrol_route = [("go_north", 60), ("look_west", 10), ("look_east", 10),
                                  ("look_north", 15), ("wait", 10), ("look_south", 15), ("go_south", 60),
                                   ("look_north", 15), ("look_east", 15), ("wait", 10), ("end", 0)]

    # Enemy #1 when Snake comes from area1_6
    def gen_patrol_route2(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.55, self.height*.30)
            enemy._looking_west = True
            enemy.patrol_route = [("go_west", 45), ("look_east", 10), ("look_west", 10),
                                  ("look_north", 15), ("wait", 10), ("look_south", 15), ("go_east", 45),
                                   ("look_north", 15), ("look_west", 15), ("look_south", 15), ("wait", 10), ("end", 0)]

    # Enemy #1 when Snake comes from area1_11
    def gen_patrol_route3(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.25, self.height*.8)
            enemy._looking_north = True
            enemy.patrol_route = [("go_north", 60), ("look_west", 15), ("look_north", 15),
                                  ("look_east", 15), ("look_south", 15), ("go_south", 60),
                                   ("look_north", 15), ("look_east", 15), ("look_west", 15), ("end", 0)]

    def gen_patrol_route4(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.06, self.height*.30)
            enemy._looking_west = True
            enemy.patrol_route = [("look_west", 15), ("look_east", 15), ("look_south", 10), ("look_north", 15),
                                   ("look_east", 10), ("end", 0)]
            
    def gen_patrol_route5(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.80, self.height*.35)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 15), ("look_north", 10), ("look_east", 15),
                                   ("look_west", 10), ("end", 0)]

    def gen_patrol_route6(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.25, self.height*.75)
            enemy._looking_north = True
            enemy.patrol_route = [("look_north", 15), ("wait", 10), ("look_north", 10), ("look_east", 15),
                                   ("look_west", 10), ("end", 0)]


    def gen_patrol_route7(self, enemy):
        if self.e_group != None:
            enemy.init_position(self.width*.48, self.height*.28)
            enemy._looking_south = True
            enemy.patrol_route = [("look_south", 20), ("look_west", 50), ("end", 0)]
    
    ### end Kha area1_10


    def draw(self: "Area", window: "Surface"):
        '''Draws shapes and sets the background within the Area.'''
        self._set_background(window, "floor.png")
        self.obj_group.draw(window)
        
        pygame.draw.line(window, WOODEN, (self.width*0.10, self.height*0.70), (self.width*0.10, self.height*0.90), self.inner_door_thickness) #lower inner door
        pygame.draw.line(window, WOODEN, (self.width*0.10, self.height*0.20), (self.width*0.30, self.height*0.20), self.inner_door_thickness) #upper left inner door
        pygame.draw.line(window, WOODEN, (self.width*0.65, self.height*0.20), (self.width*0.85, self.height*0.20), self.inner_door_thickness) #upper right inner door
        
        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.bottomleft[1] >= self.height and self.player_obj.rect.centerx >= self.width*0.10
                  and self.player_obj.rect.centerx <= self.width*0.45 and self.player_obj.moving_south):
                print("in 1_6")
                new_area = self._make_transition(self.player_obj.rect.centerx, 40, area_dict, "south1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.x <= 0 and self.player_obj.rect.centery >= self.height*0.20
                and self.player_obj.rect.centery <= self.height*0.60 and self.player_obj.moving_west):
                print("in 1_11")
                new_area = self._make_transition(self.width-40, self.player_obj.rect.centery, area_dict, "west1")
                new_area._reset_enemy_state()
                new_area._formation1()


            elif (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.20
                  and self.player_obj.rect.centery <= self.height*0.60 and self.player_obj.moving_east):
                print("in 1_9")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area1_11(area_base.Area):
    '''A class to represent Area1_11 of DBH.'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_11 object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS

        upper_left_block = Block(LIGHT_YELLOW, self.width*0.60, self.height*0.60, "light yellow big square.png")
        upper_left_block.init_position(0, 0)
        
        upper_right_block = Block(LIGHT_YELLOW, self.width*0.40, self.height*0.20, "light yellow small semi horizontal.png")
        upper_right_block.init_position(self.width*0.60, 0)
        
        lower_block = Block(LIGHT_YELLOW, self.width, self.height*0.40, "light yellow big semi horizontal.png")
        lower_block.init_position(0, self.height*0.60)
        
        self.obj_group.add(upper_left_block, upper_right_block, lower_block)


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
        
        pygame.draw.line(window, BLACK, (self.width*0.60, self.height*0.30), (self.width*0.60, self.height*0.50), self.inner_door_thickness) #inner door

        
    #When a transition is made, be sure to reset the state of the Enemies in the transitioned-to Area as they were
    #when the Area was first created. If you don't, then unwanted behavior will occur. Next, set a patrol route that
    #is specific to that new Area.
    def check_transition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        new_area = old_area = self #For alerts/projectiles
        if self.player_obj != None:
            ## CHECK FOR TRANSITIONS (would nullify effects of boundary/corner checks. Good) ##
            if (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.centery >= self.height*0.20
                  and self.player_obj.rect.centery <= self.height*0.60 and self.player_obj.moving_east):
                print("in 1_10")
                new_area = self._make_transition(40, self.player_obj.rect.centery, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation3()


            elif (self.player_obj.rect.x <= self.width*0.60 and self.player_obj.rect.centery >= self.height*0.295
                and self.player_obj.rect.centery <= self.height*0.505 and self.player_obj.moving_west):
                print("in 1_11_inner_entrance")
                new_area = self._make_transition(self.width-40, self.height*0.50, area_dict, "inner1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area


class Area1_11_InnerArea(area_base.Area):
    '''A class to represent an inner Area of Area1_11'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area1_11_InnerArea object.'''
        area_base.Area.__init__(self, window_width, window_height, player_obj, enemies)
        self.is_checkpoint = False ## FOR CHECKPOINTS
        self._draw_west_inner_room()

        ckf2 = Floor2CardKey()
        ckf2.init_position(self.width/2, self.height/2)
        self.obj_group.add(ckf2)

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
                print("in 1_11")
                new_area = self._make_transition(self.width*0.60+40, self.height*0.40, area_dict, "east1")
                new_area._reset_enemy_state()
                new_area._formation1()


            self._handle_corners_and_boundaries()

            #For resetting the ticks to safety. This is for Areas right next to safe havens
            if new_area != old_area and old_area.is_safe_haven:
                old_area.ticks = 0

            #FOR PROJECTICLES
            self._clean_up_attack_objects(new_area, old_area)

            
        return new_area
