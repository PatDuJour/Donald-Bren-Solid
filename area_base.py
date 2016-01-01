import pygame #fine
#from snake_player import *
#from collections import namedtuple #For assigning neighbors to Areas
from colors import * #fine
from block import * #fine
from weapons import * #fine
from collectibles import * #fine
import enemies
import frost
import kay
import thornton
import pattis
import cameras
import exclamation
import physical_objs

E_STUNBULLET_DAM = 3 #originally 2
E_HEART_DAM = 5
E_OTHELLO_DAM = 4
E_READINGS_DAM = 9 #originally 5
E_LANDED_READINGS_DAM = 4
E_FROSTSPARK_DAM = 15 #originally 8

S_SPITBALL_DAM = 3 
S_RBAND_DAM = 5
S_BPEEL_DAM = 10 
S_WBALLOON_DAM = 2.4
#^Note that splash duration is 5 ticks, which multiplies this damage by 5
SB_HITS_TO_STUN_MERC = 3
RB_HITS_TO_STUN_MERC = 2
WB_DRENCH_TIME_TO_STUN_MERC = 5

class Area(object):
    '''A class for an Area'''

    def __init__(self: "Area", window_width: int = 500, window_height: int = 500, player_obj: "Snake"=None, enemies: "Group"=None):
        '''Initializes the attributes of an Area object.'''
        self.obj_group = pygame.sprite.Group()
        #^A list of all objects (other than the player object), which are Sprites, in the Area
        self.e_attack_obj_group = pygame.sprite.Group() #FOR PROJECTILES
        self.s_attack_obj_group = pygame.sprite.Group()
        self.width = window_width
        self.height = window_height*0.90
        self.player_obj = player_obj
        self.e_group = enemies

        #for Snake and colliding with LOS
        self.snake_group = pygame.sprite.Group()
        self.snake_group.add(self.player_obj)
        #self.obj_group.add(self.player_obj)
        #^NO. DON'T ADD SNAKE TO the obj_group. Keep Snake and physical objects within an Area separate

        self.in_alert_phase = False
        self.root_alert_area = False
        #^This is for not having to set all Areas to alert for each game loop iteration when there is an alert
        #Think: If an Area is in alert phase, then its Enemies must be in alert phase
        self.have_set_all_alerts = False
        self.is_safe_haven = False
        self.ticks = 0
        self.ticks_to_wait = 30

        #ADDED THESE FOR BOSSES
        self.is_boss_battle_arena = False #Used in main.py
        if enemies != None:
            for enemy in list(enemies):
                if type(enemy) == kay.Kay or type(enemy) == thornton.Thornton or type(enemy) == pattis.Pattis or type(enemy) == frost.Frost:
                    self.boss = enemy
                    self.is_boss_battle_arena = True #Used in main.py as a variable for testing
                    '''
                    if enemy.is_frost:
                        self.is_frost_battle = True #FOR TESTING FOR FROST BATTLE...will i need this in the final version?
                    '''
        '''
        else:
            self.boss = None
        '''

        self.stun_area = None

###Jeremy
        self.inner_door_thickness = 10
        self.stair_bar_thickness = 3
        #The next two attributes are mainly used for bathrooms and inner rooms
        #This makes it easy to adjust the thickness of the walls; just change the value of these variables and you're done!
        self.vertical_wall_thickness = window_width*0.03
        self.horizontal_wall_thickness = window_height*0.03
###End Jeremy

    
    def update_objects(self: "Area"):
        '''Updates this Area's list of Sprite objects.'''
        #self.obj_group.update() #Call the update() function on all Sprites in obj_group
        for obj in self.obj_group:
            obj.update()
            if type(obj) == exclamation.Exclamation and obj.ticks == obj.lifespan:
                self.obj_group.remove(obj)

    #Think: If you've walked to a particular part of the game display, then draw a new Area. Drawing of
    #a new Area takes place inside the game loop.
    def draw(self: "Area", window: "Surface"):
        '''Draws the contents of this Area.'''
        window.fill(WHITE)
        self.obj_group.draw(window) #Note how Snake is drawn inside the game loop, not here

        '''
        #For when you actually have an image for the floor to each Area
        image = pygame.image.load("floor.png")
        scaled_image = pygame.transform.scale(image, (int(self.width), int(self.height)))
        window.blit(scaled_image, (0,0))
        self.obj_group.draw(window)
        '''

    def draw_enemies(self: "Area", window: "Surface"):
        if self.e_group != None:
            self.e_group.draw(window)
            
    def draw_e_attack_objects(self: "Area", window: "Surface"):
        if self.e_attack_obj_group != None:
            self.e_attack_obj_group.draw(window)


    def draw_s_attack_objects(self: "Area", window: "Surface"):
        if self.s_attack_obj_group != None:
            self.s_attack_obj_group.draw(window)
            

    def check_transtition(self: "Area", area_dict: dict):
        '''Determines if a transition to a new Area has been made. If no transition is made, then the player
           will simply be blocked by a 'wall'.'''
        #OVERRIDE THIS FUNCTION
        pass
    

    def _make_transition(self: "Area", x: float, y: float, area_dict: dict, direction: str):
        '''Makes the transition to a new Area starting from the given direction in the current Area. area_dict
           is a dictionary where the keys are Area objects and the values are namedtuples representing the set of
           neighbors of the key Area.'''
        self.player_obj.init_position(x, y)
        #^Illusion of transitioning is achieved by setting the player object to a new location
        if (direction == "north1"):
            return area_dict[self].north1
        elif (direction == "north2"):
            return area_dict[self].north2
        elif (direction == "north3"):
            return area_dict[self].north3
        elif (direction == "north4"):
            return area_dict[self].north4
        elif (direction == "east1"):
            return area_dict[self].east1
        elif (direction == "east2"):
            return area_dict[self].east2
        elif (direction == "east3"):
            return area_dict[self].east3
        elif (direction == "east4"):
            return area_dict[self].east4
        elif (direction == "south1"):
            return area_dict[self].south1
        elif (direction == "south2"):
            return area_dict[self].south2
        elif (direction == "south3"):
            return area_dict[self].south3
        elif (direction == "south4"):
            return area_dict[self].south4
        elif (direction == "west1"):
            return area_dict[self].west1
        elif (direction == "west2"):
            return area_dict[self].west2
        elif (direction == "west3"):
            return area_dict[self].west3
        elif (direction == "west4"):
            return area_dict[self].west4
        elif (direction == "inner1"):
            return area_dict[self].inner1
        elif (direction == "inner2"):
            return area_dict[self].inner2
        elif (direction == "inner3"):
            return area_dict[self].inner3
        elif (direction == "inner4"):
            return area_dict[self].inner4

    #Note how you didn't make helper functions for if statements that check the transition (i.e., door) boundaries
    #because in the final game, transition boundaries aren't going to be the same across all Areas

    def _handle_corners_and_boundaries(self: "Area"):
        '''Conducts checks on which corners or boundaries the player object happens upon and sets the player
           object's coordinate attributes appropriately.'''
        ## Corner Case: Top-Left ##
        if (self.player_obj.rect.x <= 0 and self.player_obj.rect.y <= 0):
            self.player_obj.rect.x = 0
            self.player_obj.rect.y = 0
        ## Corner Case: Top-Right ##
        elif (self.player_obj.rect.topright[0] >= self.width and self.player_obj.rect.topright[1] <= 0):
            self.player_obj.rect.x = self.width - (self.player_obj.rect.topright[0] - self.player_obj.rect.topleft[0])
            self.player_obj.rect.y = 0
        ## Corner Case: Bottom-Left ##
        elif (self.player_obj.rect.bottomleft[0] <= 0 and self.player_obj.rect.bottomright[1] >= self.height):
            self.player_obj.rect.x = 0
            self.player_obj.rect.y = self.height - (self.player_obj.rect.bottomleft[1] - self.player_obj.rect.topleft[1])
        ## Corner Case: Bottom-Right ##
        elif (self.player_obj.rect.bottomright[0] >= self.width and self.player_obj.rect.bottomright[1] >= self.height):
            self.player_obj.rect.x = self.width - (self.player_obj.rect.bottomright[0] - self.player_obj.rect.bottomleft[0])
            self.player_obj.rect.y = self.height - (self.player_obj.rect.bottomleft[1] - self.player_obj.rect.topleft[1])
            
        ## Boundary Cases ##
        elif (self.player_obj.rect.y <= 0): #Hitting the top boundary
            self.player_obj.rect.y = 0
        elif (self.player_obj.rect.x <= 0): #Hitting the left boundary
            self.player_obj.rect.x = 0
        elif (self.player_obj.rect.topright[0] >= self.width): #Hitting the right boundary
            self.player_obj.rect.x = self.width - (self.player_obj.rect.topright[0] - self.player_obj.rect.topleft[0])
        elif (self.player_obj.rect.bottomleft[1] >= self.height): #Hitting bottom boundary
            self.player_obj.rect.y = self.height - (self.player_obj.rect.bottomleft[1] - self.player_obj.rect.topleft[1])


    def _clean_up_attack_objects(self: "Area", new_area: "Area", old_area: "Area"): #Also made this remove exclamation points
        '''Clears an Area that was exited of any attack objects. This would be repeatedly called
           while in the game loop, so a check always needs to be made for if we're in a new Area.
           Only if we're in a new Area will the cleanup be made.'''
        if new_area != old_area:
            for attack_obj in old_area.e_attack_obj_group:
                if type(attack_obj) != Readings:
                    old_area.e_attack_obj_group.remove(attack_obj)
            for attack_obj in old_area.s_attack_obj_group:
                old_area.s_attack_obj_group.remove(attack_obj)
                
            #Remove exclamation points
            for obj in self.obj_group:
                if type(obj) == exclamation.Exclamation:
                    old_area.obj_group.remove(obj)


    def clean_up_attack_objects_after_continue(self: "Area", area_lst: ["Area"]): #Also made this remove exclamation points
        '''Clears all Areas of all attack objects. Used for when Snake continues after being subdued.'''
        for area in area_lst:
            for attack_obj in area.e_attack_obj_group:
                area.e_attack_obj_group.remove(attack_obj)
            for attack_obj in area.s_attack_obj_group:
                area.s_attack_obj_group.remove(attack_obj)

            #Remove exclamation points
            for obj in self.obj_group:
                if type(obj) == exclamation.Exclamation:
                    old_area.obj_group.remove(obj)

    ## For enemy movement ##:
    def update_enemies(self: "Area"):
        '''Updates the necessary attributes for all Enemy's in this Area.'''
        #print(self.in_alert_phase) #FOR TESTING
        #self.e_group.update() #Could do this for the entire without a loop, but what if an Enemy has no patrol route? Need loop.
        if self.e_group != None:
            for enemy in list(self.e_group):
                if enemy.patrol_route != [] or enemy.is_boss:
                    #enemy.update(self.obj_group, self.snake_group)
                    #Think: If it's in the obj_group, then do the blocking stuff. If it's snake, then raise alarm
                    enemy.update(self.obj_group, self.snake_group, self.s_attack_obj_group) #Send the object group and snake group to an Enemy's update() method


    ## For projectile movement ##
    ## When area transitions are made, projectiles must be removed ##
    def update_e_attack_objects(self: "Area"):
        '''Updates the necessary attributes for the attack objects of all Enemies in the Area.'''
        #print(len(self.e_attack_obj_group))
        #Have a loop that updates each projectile first
        for attack_obj in self.e_attack_obj_group:
            if (attack_obj.rect.y < -10 or attack_obj.rect.y > self.height or #This if statement is for testing in your Prototype Land
            attack_obj.rect.x < -10 or attack_obj.rect.x > self.width):
                self.e_attack_obj_group.remove(attack_obj)
            else:
                attack_obj.update()

        #Then look for collisions with physical objects
        for attack_obj in self.e_attack_obj_group:
            attack_obj_collision_lst = pygame.sprite.spritecollide(attack_obj, self.obj_group, False)
            #snake_collision_lst = pygame.sprite.spritecollide(projectile, self.snake_group, False)
            for obj in attack_obj_collision_lst:
                if type(obj) == Block:
                    self.e_attack_obj_group.remove(attack_obj)

        for attack_obj in self.e_attack_obj_group:
            snake_collision_lst = pygame.sprite.spritecollide(attack_obj, self.snake_group, False)
            if snake_collision_lst != []:
                if type(attack_obj) == FrostSpark:
                    self.player_obj.health -= E_FROSTSPARK_DAM
                    self.e_attack_obj_group.remove(attack_obj)
                elif type(attack_obj) == StunBullet:
                    self.player_obj.health -= E_STUNBULLET_DAM
                    self.e_attack_obj_group.remove(attack_obj)
                elif type(attack_obj) == Heart:
                    self.player_obj.health -= E_HEART_DAM
                    self.e_attack_obj_group.remove(attack_obj)
                elif type(attack_obj) == OthelloTile:
                    self.player_obj.health -= E_OTHELLO_DAM
                    self.e_attack_obj_group.remove(attack_obj)
                elif type(attack_obj) == Readings:
                    if attack_obj.in_air:
                        self.player_obj.health -= E_READINGS_DAM
                    else:
                        self.player_obj.health -= E_LANDED_READINGS_DAM
                        #print(self.player_obj.health)
                    self.e_attack_obj_group.remove(attack_obj)
                else: #Else, if the enemy attack object some other projectible unaccounted for...
                    self.player_obj.health -= 2
                    self.e_attack_obj_group.remove(attack_obj)
                    #print(self.player_obj.health)


    ## For projectile movement ##
    def update_s_attack_objects(self: "Area"):
        '''Updates the necessary attributes of all the attack objects for Snake.'''
        #Have a loop that updates each attack object first
        for attack_obj in self.s_attack_obj_group:
            if ((attack_obj.rect.y < -10 or attack_obj.rect.y > self.height or   #This if statement is for testing in your Prototype Land
                attack_obj.rect.x < -10 or attack_obj.rect.x > self.width) and
                (type(attack_obj) == SpitBall or type(attack_obj) == RubberBand)):
                self.s_attack_obj_group.remove(attack_obj)
            else:
                attack_obj.update()

        #Then look to remove certain projectiles
        #First, when colliding with physical objects
        for attack_obj in self.s_attack_obj_group:
            attack_obj_collision_lst = pygame.sprite.spritecollide(attack_obj, self.obj_group, False)
            #Returns a container of what projectile collided with
            for obj in attack_obj_collision_lst:
                if type(attack_obj) == SpitBall or type(attack_obj) == RubberBand: #Spitballs will disappear upon contact with physical objects
                    self.s_attack_obj_group.remove(attack_obj)

                    
            if type(attack_obj) == WaterBalloon:
                if attack_obj.ticks_for_splash > attack_obj.splash_duration:
                    self.s_attack_obj_group.remove(attack_obj)


        #Next for collisions with Enemy attack objects
        for attack_obj in self.s_attack_obj_group:
            attack_obj_collision_lst = pygame.sprite.spritecollide(attack_obj, self.e_attack_obj_group, False)
            for obj in attack_obj_collision_lst:
                if type(obj) == Readings and not obj.in_air:
                    if type(attack_obj) != WaterBalloon:
                        self.e_attack_obj_group.remove(obj) #Remove the reading
                        self.s_attack_obj_group.remove(attack_obj) #Remove snake's attack object
                    else:
                        if attack_obj.landed:
                            self.e_attack_obj_group.remove(obj)
                    

        #---CODE FOR SNAKE ATTACK DAMAGE---
        #Next, when colliding with Enemies (should I include this collision handling code in the Enemies class as well as this class?)
        if self.e_group != None:
            for attack_obj in self.s_attack_obj_group:
                attack_obj_collision_lst = pygame.sprite.spritecollide(attack_obj, self.e_group, False)
                for enemy in attack_obj_collision_lst:
                    if type(enemy) != cameras.Camera:
                        if type(attack_obj) == SpitBall and not enemy.is_boss:    #ADDED not enemy.is_boss FOR BOSS BATTLE
                            self.s_attack_obj_group.remove(attack_obj)
                            enemy.spitball_hits += 1
                            if enemy.spitball_hits == SB_HITS_TO_STUN_MERC:
                                self._set_stun_effect(enemy, "spitball")
                        elif type(attack_obj) == SpitBall and enemy.is_boss:       #ADDED TO TAKE AWAY BOSS' HEALTH
                            self._register_attack_obj(enemy, S_SPITBALL_DAM)
                            self.s_attack_obj_group.remove(attack_obj)
                            #print(enemy.health)
                        elif type(attack_obj) == RubberBand and not enemy.is_boss: #ADDED not enemy.is_boss FOR BOSS BATTLE
                            self.s_attack_obj_group.remove(attack_obj)
                            enemy.rubberband_hits += 1
                            if enemy.rubberband_hits == RB_HITS_TO_STUN_MERC:
                                self._set_stun_effect(enemy, "rubber band")
                        elif type(attack_obj) == RubberBand and enemy.is_boss:     #ADDED TO TAKE AWAY BOSS' HEALTH
                            self._register_attack_obj(enemy, S_RBAND_DAM)
                            self.s_attack_obj_group.remove(attack_obj)
                            #print(enemy.health)
                        elif type(attack_obj) == WaterBalloon and not enemy.is_boss: #ADDED not enemy.is_boss FOR BOSS BATTLE
                            if attack_obj.landed and not enemy.waterballoon_stunned:
                                enemy.wb_drench_time += 1
                            if attack_obj.landed and enemy.wb_drench_time == WB_DRENCH_TIME_TO_STUN_MERC and not enemy.waterballoon_stunned:
                                self._set_stun_effect(enemy, "water balloon")
                        elif type(attack_obj) == WaterBalloon and enemy.is_boss:    #ADDED TO TAKE AWAY BOSS' HEALTH
                            #self._register_attack_obj(enemy, S_WBALLOON_DAM)
                            if attack_obj.landed and not enemy.is_frost and not enemy.is_boo:
                                enemy.health -= S_WBALLOON_DAM
                                ktp_grunt = pygame.mixer.Sound("ktp_grunt.wav")
                                pygame.mixer.Sound.play(ktp_grunt)
                            elif attack_obj.landed and enemy.is_frost:
                                frost_laugh = pygame.mixer.Sound("frost_laugh.wav")
                                pygame.mixer.Sound.play(frost_laugh)
                            elif attack_obj.landed and enemy.is_boo:
                                boo_bark = pygame.mixer.Sound("boo_bark.wav")
                                pygame.mixer.Sound.play(boo_bark)
                            #print(enemy.health)
                        elif type(attack_obj) == BananaPeel and not enemy.is_boss:  #ADDED not enemy.is_boss FOR BOSS BATTLE
                            self.s_attack_obj_group.remove(attack_obj)
                            self._set_stun_effect(enemy, "water balloon")
                        elif type(attack_obj) == BananaPeel and enemy.is_boss:      #ADDED TO TAKE AWAY BOSS' HEALTH
                            if not enemy.is_boo:
                                enemy.health -= S_BPEEL_DAM
                                if not enemy.is_frost and not enemy.is_boo:
                                    ktp_grunt = pygame.mixer.Sound("ktp_grunt.wav")
                                    pygame.mixer.Sound.play(ktp_grunt)
                                elif enemy.is_frost:
                                    frost_grunt = pygame.mixer.Sound("frost_grunt.wav")
                                    pygame.mixer.Sound.play(frost_grunt)
                                if enemy.health <= 0 and enemy.is_frost:
                                    enemy.is_stunned = True
                                    enemy.stun_area = self
                                    enemy.stun_location = (enemy.rect.centerx, enemy.rect.centery)
                            else:
                                boo_bark = pygame.mixer.Sound("boo_bark.wav")
                                pygame.mixer.Sound.play(boo_bark)
                            self.s_attack_obj_group.remove(attack_obj)

                        #----STUFF FOR GETTING RID OF THE BOSS----                            
                        self._clear_boss(enemy)


    def _register_attack_obj(self: "Area", enemy: "Enemy", dam: int):
        '''Registers the damage/reaction for a boss after being hit with a Snake attack object.'''
        if not enemy.is_frost and not enemy.is_boo:
            enemy.health -= dam
            ktp_grunt = pygame.mixer.Sound("ktp_grunt.wav")
            pygame.mixer.Sound.play(ktp_grunt)
        elif enemy.is_frost:
            frost_laugh = pygame.mixer.Sound("frost_laugh.wav")
            pygame.mixer.Sound.play(frost_laugh)
        else:
            boo_bark = pygame.mixer.Sound("boo_bark.wav")
            pygame.mixer.Sound.play(boo_bark)


    #----STUFF FOR GETTING RID OF THE BOSS----                            
    def _clear_boss(self: "Area", enemy: "Enemy"):
        '''Clears away a boss when his health goes to/goes below 0 and replaces his Sprite with a key card.'''
        if type(enemy) != enemies.Enemy and not enemy.is_frost: #I.e., if the enemy is one of the bosses...
            if enemy.health <= 0:
                e_centerx, e_centery = enemy.rect.centerx, enemy.rect.centery
                #print(e_centerx, e_centery)
                self.e_group.remove(enemy)
                if type(enemy) == kay.Kay:
                    enemy.is_subdued = True
                    key_card = Floor3CardKey()
                    self.obj_group.add(key_card)
                    key_card.init_position(e_centerx, e_centery)
                elif type(enemy) == thornton.Thornton: #If the enemy is Thornton, then remove Boo also!
                    for boo in self.e_group:
                        self.e_group.remove(boo)
                    enemy.is_subdued = True
                    key_card = Floor4CardKey()
                    self.obj_group.add(key_card)
                    key_card.init_position(e_centerx, e_centery)
                elif type(enemy) == pattis.Pattis:
                    enemy.is_subdued = True
                    key_card = Floor5CardKey()
                    self.obj_group.add(key_card)
                    key_card.init_position(e_centerx, e_centery)

    
    def _set_stun_effect(self: "Area", enemy: "Enemy", weapon_type: str):
        '''Sets the stun effect for an enemy based on a given weapon of Snake's. Also creates a grunting noise.'''
        self.player_obj.merc_stuns += 1
        if weapon_type == "spitball":
            enemy.spitball_stunned = True
        elif weapon_type == "rubber band":
            enemy.rubberband_stunned = True
        elif weapon_type == "water balloon":
            enemy.waterballoon_stunned = True
        elif weapon_type == "banana peel":
            enemy.banana_peel_stunned = True
        grunt = pygame.mixer.Sound("grunt.wav")
        pygame.mixer.Sound.play(grunt)
        if not enemy.in_alert_phase:
            enemy.set_alert_phase(self.snake_group)
                                    

    def _reset_enemy_state(self: "Area"):
        '''Resets the state of enemes in an Area back to how it was when it was when the
           Enemy was first constructed.'''
        if self.e_group != None:
            for enemy in list(self.e_group):
                enemy._instr_index = 0
                enemy._current_step_num = 0 #For walking
                enemy._current_wait_num = 0 #For waiting
                enemy._current_look_num = 0 #For looking
                enemy._is_moving = False
                enemy._looking_north = enemy._looking_east = enemy._looking_south = enemy._looking_west = False
                enemy._cur_frame = 0
                enemy.spitball_stunned = enemy.rubberband_stunned = enemy.waterballoon_stunned = enemy.banana_peel_stunned = False
                enemy.stun_time = 0
                enemy.rubberband_hits = 0
                enemy.spitball_hits = 0
                enemy.wb_drench_time = 0


    def if_alert_then_propagate(self: "Area", area_lst: ["Areas"]):
        '''Checks if this Area is in alert phase. If it is, then sets the alert phase of all Areas to True.'''
        #print(self.root_alert_area)
        #This if statement prevents having to set all Areas to alert constantly
        if self.in_alert_phase and self.root_alert_area and not self.have_set_all_alerts:
            #print("BOOM")
            for area in area_lst:
                area.in_alert_phase = True
                if area.e_group != None:
                    for enemy in area.e_group:
                        enemy.in_alert_phase = True
            self.have_set_all_alerts = True


    def if_safe_haven_subside_alerts(self: "Area", area_lst: ["Area"]):
        '''Checks if this Area is a safe haven. If it is, then sets the alert phase of all Areas to False.
           It takes a certain number of ticks for the alert to subside.'''
        
        if self.is_safe_haven and self.in_alert_phase:
            #print(self.ticks)
            if self.ticks < self.ticks_to_wait:
                self.ticks += 1
            else:
                #print("CLEAR")
                ding = pygame.mixer.Sound("ding.wav")
                pygame.mixer.Sound.play(ding)
                self.ticks = 0
                for area in area_lst:
                    area.in_alert_phase = False
                    area.root_alert_area = False
                    area.have_set_all_alerts = False 
                    if area.e_group != None:
                        for enemy in area.e_group:
                            enemy.in_alert_phase = False


    def subside_all_alerts(self: "Area", area_lst: ["Area"]):
        '''Subsides alerts in all Areas for when the player decides to continue after being subdued.'''
        for area in area_lst:
            area.in_alert_phase = False
            area.root_alert_area = False
            area.have_set_all_alerts = False
            if area.e_group != None:
                for enemy in area.e_group:
                    enemy.in_alert_phase = False


    #Might only be necessary to reset the state of Enemies in the Area that Snake was subdued in
    def reset_enemy_state(self: "Area", area_lst: ["Area"]):
        '''Resets the states of all Enemies in all Areas of the game for when the player decides to continue after being subdued.'''
        for area in area_lst:
            if area.e_group != None:
                for enemy in list(self.e_group):
                    enemy._instr_index = 0
                    enemy._current_step_num = 0
                    enemy._current_wait_num = 0
                    enemy._is_moving = False
                    enemy._looking_north = enemy._looking_east = enemy._looking_south = enemy._looking_west = False #Hmm, does this cause an issue?
                    enemy._cur_frame = 0
                    enemy.spitball_stunned = enemy.rubberband_stunned = enemy.waterballoon_stunned = enemy.banana_peel_stunned = False
                    enemy.stun_time = 0
                    enemy.rubberband_hits = 0
                    enemy.spitball_hits = 0
                    enemy.wb_drench_time = 0


    def _set_background(self: "Area", window: "Surface", filename: str):
        '''Sets the background image for this Area.'''
        image = pygame.image.load(filename)
        scaled_image = pygame.transform.scale(image, (int(self.width), int(self.height)))
        window.blit(scaled_image, (0, 0))


    ## THIS METHOD SHOULD ONLY EVER BE CALLED IN AREAS THAT HAVE FROST!!! ##
    def _frost_transition(self: "Area", new_area: "Area", snake_spawn_point: (int, int), direction: str):
        '''Handles a transition for Frost during his boss battle.'''
        TAILING_DIST = 150
        if not self.boss.is_stunned:
            if direction == "north":
                self.boss.init_position(snake_spawn_point[0], snake_spawn_point[1]+TAILING_DIST)  #addition/subtraction depends on orientation of Snake's spawn
            elif direction == "east":
                self.boss.init_position(snake_spawn_point[0]-TAILING_DIST, snake_spawn_point[1])  #addition/subtraction depends on orientation of Snake's spawn
            elif direction == "south":
                self.boss.init_position(snake_spawn_point[0], snake_spawn_point[1]-TAILING_DIST)  #addition/subtraction depends on orientation of Snake's spawn
            elif direction == "west":
                self.boss.init_position(snake_spawn_point[0]+TAILING_DIST, snake_spawn_point[1])  #addition/subtraction depends on orientation of Snake's spawn
            self.boss.area = new_area
            #Perhaps I can pass on Frost's health here...WOW don't need to. His health is remembered
            #across the areas for me. Must be something to do with the pass-by-reference nature of Groups?
        elif self.boss.is_stunned and self.boss.stun_area != new_area:
            #Hide him offscreen
            if direction == "north":
                self.boss.init_position(snake_spawn_point[0], snake_spawn_point[1]+TAILING_DIST)  #addition/subtraction depends on orientation of Snake's spawn
            elif direction == "east":
                self.boss.init_position(snake_spawn_point[0]-TAILING_DIST, snake_spawn_point[1])  #addition/subtraction depends on orientation of Snake's spawn
            elif direction == "south":
                self.boss.init_position(snake_spawn_point[0], snake_spawn_point[1]-TAILING_DIST)  #addition/subtraction depends on orientation of Snake's spawn
            elif direction == "west":
                self.boss.init_position(snake_spawn_point[0]+TAILING_DIST, snake_spawn_point[1])  #addition/subtraction depends on orientation of Snake's spawn

            self.boss.area = new_area
        else:
            self.boss.init_position(self.boss.stun_location[0], self.boss.stun_location[1])
            self.boss.area = new_area


###Jeremy
    #These next 6 helper methods draw all of the black Blocks and insert all of the sprites for every type of inner room and bathroom
    def _draw_north_inner_room(self: "Area"):
        left_block = Block(BLACK, self.width*0.20-self.vertical_wall_thickness, self.height)
        left_block.init_position(0, 0)

        right_block = Block(BLACK, self.width*0.20-self.vertical_wall_thickness, self.height)
        right_block.init_position(self.width*0.80+self.vertical_wall_thickness, 0)

        top_block = Block(BLACK, self.width*0.60+2.0*self.vertical_wall_thickness, self.height*0.20-self.horizontal_wall_thickness)
        top_block.init_position(self.width*0.20-self.vertical_wall_thickness, 0)

        lower_left_block = Block(BLACK, self.width*0.15, self.height*0.205-self.horizontal_wall_thickness)
        lower_left_block.init_position(self.width*0.20-self.vertical_wall_thickness, self.height*0.80+self.horizontal_wall_thickness)

        lower_right_block = Block(BLACK, self.width*0.15, self.height*0.205-self.horizontal_wall_thickness)
        lower_right_block.init_position(self.width*0.65+self.vertical_wall_thickness, self.height*0.80+self.horizontal_wall_thickness)

        top_wall = Block(LIGHT_YELLOW, self.width*0.60+2.0*self.vertical_wall_thickness, self.horizontal_wall_thickness, "light yellow horizontal wall.png")
        top_wall.init_position(self.width*0.20-self.vertical_wall_thickness, self.height*0.20-self.horizontal_wall_thickness)

        left_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.60, "light yellow vertical wall.png")
        left_wall.init_position(self.width*0.20-self.vertical_wall_thickness, self.height*0.20)

        right_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.60, "light yellow vertical wall.png")
        right_wall.init_position(self.width*0.80, self.height*0.20)

        lower_left_wall = Block(LIGHT_YELLOW, self.width*0.15+self.vertical_wall_thickness, self.horizontal_wall_thickness, "light yellow horizontal wall.png")
        lower_left_wall.init_position(self.width*0.20-self.vertical_wall_thickness, self.height*0.80)

        lower_right_wall = Block(LIGHT_YELLOW, self.width*0.15+self.vertical_wall_thickness, self.horizontal_wall_thickness, "light yellow horizontal wall.png")
        lower_right_wall.init_position(self.width*0.65, self.height*0.80)

        left_entrance_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.20-self.horizontal_wall_thickness, "light yellow vertical wall.png")
        left_entrance_wall.init_position(self.width*0.35-self.vertical_wall_thickness, self.height*0.80+self.horizontal_wall_thickness)

        right_entrance_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.20-self.horizontal_wall_thickness, "light yellow vertical wall.png")
        right_entrance_wall.init_position(self.width*0.65, self.height*0.80+self.horizontal_wall_thickness)

        self.obj_group.add(left_block, right_block, top_block, lower_left_block, lower_right_block, top_wall, left_wall, right_wall, lower_left_wall,
                           lower_right_wall, left_entrance_wall, right_entrance_wall)

        #PHYSICAL OBJECTS IN ROOM
        book_counter1 = physical_objs.BookCounter("south")
        book_counter1.init_position(self.width*0.20, self.height*0.20)
        self.obj_group.add(book_counter1)

        book_counter2 = physical_objs.BookCounter("south")
        book_counter2.init_position(self.width*0.40, self.height*0.20)
        self.obj_group.add(book_counter2)

        book_counter3 = physical_objs.BookCounter("south")
        book_counter3.init_position(self.width*0.60, self.height*0.20)
        self.obj_group.add(book_counter3)

        '''
        red_sofa_chair = physical_objs.RedSofaChair("north")
        red_sofa_chair.init_position(self.width*0.21, self.height*0.67)
        self.obj_group.add(red_sofa_chair)
        '''
        red_sofa_chair = physical_objs.RedSofaChair("east")
        red_sofa_chair.init_position(self.width*0.21, self.height*0.65)
        self.obj_group.add(red_sofa_chair)

        square_table = physical_objs.SmallSquareTable()
        square_table.init_position(self.width*0.21, self.height*0.52)
        self.obj_group.add(square_table)

        long_table = physical_objs.SmallLongTable("vertical")
        long_table.init_position(self.width*0.72, self.height*0.56)
        self.obj_group.add(long_table)

        
    def _draw_east_inner_room(self: "Area"):
        top_block = Block(BLACK, self.width, self.height*0.20-self.horizontal_wall_thickness)
        top_block.init_position(0, 0)

        bottom_block = Block(BLACK, self.width, self.height*0.205-self.horizontal_wall_thickness)
        bottom_block.init_position(0, self.height*0.80+self.horizontal_wall_thickness)

        upper_left_block = Block(BLACK, self.width*0.20-self.vertical_wall_thickness, self.height*0.15)
        upper_left_block.init_position(0, self.height*0.20-self.horizontal_wall_thickness)

        lower_left_block = Block(BLACK, self.width*0.20-self.vertical_wall_thickness, self.height*0.155)
        lower_left_block.init_position(0, self.height*0.65+self.horizontal_wall_thickness)

        right_block = Block(BLACK, self.width*0.20-self.vertical_wall_thickness, self.height*0.605+2.0*self.horizontal_wall_thickness)
        right_block.init_position(self.width*0.80+self.vertical_wall_thickness, self.height*0.20-self.horizontal_wall_thickness)

        upper_entrance_wall = Block(LIGHT_YELLOW, self.width*0.20-self.vertical_wall_thickness, self.horizontal_wall_thickness, "light yellow horizontal wall.png")
        upper_entrance_wall.init_position(0, self.height*0.35-self.horizontal_wall_thickness)

        lower_entrance_wall = Block(LIGHT_YELLOW, self.width*0.20-self.vertical_wall_thickness, self.horizontal_wall_thickness, "light yellow horizontal wall.png")
        lower_entrance_wall.init_position(0, self.height*0.65)

        upper_left_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.15+self.horizontal_wall_thickness, "light yellow vertical wall.png")
        upper_left_wall.init_position(self.width*0.20-self.vertical_wall_thickness, self.height*0.20-self.horizontal_wall_thickness)

        lower_left_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.15+self.horizontal_wall_thickness, "light yellow vertical wall.png")
        lower_left_wall.init_position(self.width*0.20-self.vertical_wall_thickness, self.height*0.65)

        top_wall = Block(LIGHT_YELLOW, self.width*0.60, self.horizontal_wall_thickness, "light yellow horizontal wall.png")
        top_wall.init_position(self.width*0.20, self.height*0.20-self.horizontal_wall_thickness)

        bottom_wall = Block(LIGHT_YELLOW, self.width*0.60, self.horizontal_wall_thickness, "light yellow horizontal wall.png")
        bottom_wall.init_position(self.width*0.20, self.height*0.80)

        right_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.60+2.0*self.horizontal_wall_thickness, "light yellow vertical wall.png")
        right_wall.init_position(self.width*0.80, self.height*0.20-self.horizontal_wall_thickness)

        self.obj_group.add(top_block, bottom_block, upper_left_block, lower_left_block, right_block, upper_entrance_wall, lower_entrance_wall,
                           upper_left_wall, lower_left_wall, top_wall, bottom_wall, right_wall)

        #INITIALIZE PHYSICAL OBJECTS
        book_counter1 = physical_objs.BookCounter("west")
        book_counter1.init_position(self.width*0.745, self.height*0.22)
        self.obj_group.add(book_counter1)

        book_counter2 = physical_objs.BookCounter("west")
        book_counter2.init_position(self.width*0.745, self.height*0.52)
        self.obj_group.add(book_counter2)

        rounded_edge_table = physical_objs.RoundedEdgeTable("horizontal")
        rounded_edge_table.init_position(self.width*0.20, self.height*0.68)
        self.obj_group.add(rounded_edge_table )

        square_table = physical_objs.SmallSquareTable()
        square_table.init_position(self.width*0.20, self.height*0.20)
        self.obj_group.add(square_table)

        red_sofa = physical_objs.RedSofa("south")
        red_sofa.init_position(self.width*0.29, self.height*0.20)
        self.obj_group.add(red_sofa)

        wooden_counter = physical_objs.WoodenCounter("north")
        wooden_counter.init_position(self.width*0.40, self.height*0.725)
        self.obj_group.add(wooden_counter)

        

    def _draw_south_inner_room(self: "Area"):
        left_block = Block(BLACK, self.width*0.20-self.vertical_wall_thickness, self.height)
        left_block.init_position(0, 0)

        right_block = Block(BLACK, self.width*0.20-self.vertical_wall_thickness, self.height)
        right_block.init_position(self.width*0.80+self.vertical_wall_thickness, 0)

        upper_left_block = Block(BLACK, self.width*0.15, self.height*0.20-self.horizontal_wall_thickness)
        upper_left_block.init_position(self.width*0.20-self.vertical_wall_thickness, 0)

        upper_right_block = Block(BLACK, self.width*0.15, self.height*0.20-self.horizontal_wall_thickness)
        upper_right_block.init_position(self.width*0.65+self.vertical_wall_thickness, 0)

        bottom_block = Block(BLACK, self.width*0.60+2.0*self.vertical_wall_thickness, self.height*0.205-self.horizontal_wall_thickness)
        bottom_block.init_position(self.width*0.20-self.vertical_wall_thickness, self.height*0.80+self.horizontal_wall_thickness)

        left_entrance_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.20-self.horizontal_wall_thickness, "light yellow vertical wall.png")
        left_entrance_wall.init_position(self.width*0.35-self.vertical_wall_thickness, 0)

        right_entrance_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.20-self.horizontal_wall_thickness, "light yellow vertical wall.png")
        right_entrance_wall.init_position(self.width*0.65, 0)

        upper_left_wall = Block(LIGHT_YELLOW, self.width*0.15+self.vertical_wall_thickness, self.horizontal_wall_thickness, "light yellow horizontal wall.png")
        upper_left_wall.init_position(self.width*0.20-self.vertical_wall_thickness, self.height*0.20-self.horizontal_wall_thickness)

        upper_right_wall = Block(LIGHT_YELLOW, self.width*0.15+self.vertical_wall_thickness, self.horizontal_wall_thickness, "light yellow horizontal wall.png")
        upper_right_wall.init_position(self.width*0.65, self.height*0.20-self.horizontal_wall_thickness)

        left_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.60, "light yellow vertical wall.png")
        left_wall.init_position(self.width*0.20-self.vertical_wall_thickness, self.height*0.20)

        right_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.60, "light yellow vertical wall.png")
        right_wall.init_position(self.width*0.80, self.height*0.20)

        bottom_wall = Block(LIGHT_YELLOW, self.width*0.60+2.0*self.vertical_wall_thickness, self.horizontal_wall_thickness, "light yellow horizontal wall.png")
        bottom_wall.init_position(self.width*0.20-self.vertical_wall_thickness, self.height*0.80)

        self.obj_group.add(left_block, right_block, upper_left_block, upper_right_block, bottom_block, left_entrance_wall, right_entrance_wall,
                           upper_left_wall, upper_right_wall, left_wall, right_wall, bottom_wall)

        book_counter1 = physical_objs.BookCounter("east")
        book_counter1.init_position(self.width*0.20, self.height*0.22)
        self.obj_group.add(book_counter1)

        book_counter2 = physical_objs.BookCounter("east")
        book_counter2.init_position(self.width*0.20, self.height*0.52)
        self.obj_group.add(book_counter2)

        red_sofa = physical_objs.RedSofa("north")
        red_sofa.init_position(self.width*0.35, self.height*0.68)
        self.obj_group.add(red_sofa)

        end_table = physical_objs.EndTable("north")
        end_table.init_position(self.width*0.548, self.height*0.70)
        self.obj_group.add(end_table)

        small_long_table = physical_objs.SmallLongTable("vertical")
        small_long_table.init_position(self.width*0.72, self.height*0.22)
        self.obj_group.add(small_long_table)

        pink_counter = physical_objs.PinkCounter("west")
        pink_counter.init_position(self.width*0.73, self.height*0.50)
        self.obj_group.add(pink_counter)


    def _draw_west_inner_room(self: "Area"):
        top_block = Block(BLACK, self.width, self.height*0.20-self.horizontal_wall_thickness)
        top_block.init_position(0, 0)

        bottom_block = Block(BLACK, self.width, self.height*0.205-self.horizontal_wall_thickness)
        bottom_block.init_position(0, self.height*0.80+self.horizontal_wall_thickness)

        left_block = Block(BLACK, self.width*0.20-self.vertical_wall_thickness, self.height*0.605+2.0*self.horizontal_wall_thickness)
        left_block.init_position(0, self.height*0.20-self.horizontal_wall_thickness)

        upper_right_block = Block(BLACK, self.width*0.20-self.vertical_wall_thickness, self.height*0.15)
        upper_right_block.init_position(self.width*0.80+self.vertical_wall_thickness, self.height*0.20-self.horizontal_wall_thickness)

        lower_right_block = Block(BLACK, self.width*0.20-self.vertical_wall_thickness, self.height*0.155)
        lower_right_block.init_position(self.width*0.80+self.vertical_wall_thickness, self.height*0.65+self.horizontal_wall_thickness)

        left_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.60+2.0*self.horizontal_wall_thickness, "light yellow vertical wall.png")
        left_wall.init_position(self.width*0.20-self.vertical_wall_thickness, self.height*0.20-self.horizontal_wall_thickness)

        top_wall = Block(LIGHT_YELLOW, self.width*0.60, self.horizontal_wall_thickness, "light yellow horizontal wall.png")
        top_wall.init_position(self.width*0.20, self.height*0.20-self.horizontal_wall_thickness)

        bottom_wall = Block(LIGHT_YELLOW, self.width*0.60, self.horizontal_wall_thickness, "light yellow horizontal wall.png")
        bottom_wall.init_position(self.width*0.20, self.height*0.80)

        upper_right_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.15+self.horizontal_wall_thickness, "light yellow vertical wall.png")
        upper_right_wall.init_position(self.width*0.80, self.height*0.20-self.horizontal_wall_thickness)

        lower_right_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.15+self.horizontal_wall_thickness, "light yellow vertical wall.png")
        lower_right_wall.init_position(self.width*0.80, self.height*0.65)

        upper_entrance_wall = Block(LIGHT_YELLOW, self.width*0.20-self.vertical_wall_thickness, self.horizontal_wall_thickness, "light yellow horizontal wall.png")
        upper_entrance_wall.init_position(self.width*0.80+self.vertical_wall_thickness, self.height*0.35-self.horizontal_wall_thickness)

        lower_entrance_wall = Block(LIGHT_YELLOW, self.width*0.20-self.vertical_wall_thickness, self.horizontal_wall_thickness, "light yellow horizontal wall.png")
        lower_entrance_wall.init_position(self.width*0.80+self.vertical_wall_thickness, self.height*0.65)

        self.obj_group.add(top_block, bottom_block, left_block, upper_right_block, lower_right_block, left_wall, top_wall, bottom_wall,
                           upper_right_wall, lower_right_wall, upper_entrance_wall, lower_entrance_wall)

        #PHYSICAL OBJECTS
        book_counter1 = physical_objs.BookCounter("south")
        book_counter1.init_position(self.width*0.20, self.height*0.20)
        self.obj_group.add(book_counter1)

        book_counter2 = physical_objs.BookCounter("north")
        book_counter2.init_position(self.width*0.20, self.height*0.73)
        self.obj_group.add(book_counter2)

        pink_counter = physical_objs.PinkCounter("north")
        pink_counter.init_position(self.width*0.60, self.height*0.73)
        self.obj_group.add(pink_counter)

        blue_sofa = physical_objs.BlueSofa("south")
        blue_sofa.init_position(self.width*0.61, self.height*0.20)
        self.obj_group.add(blue_sofa)

        end_table = physical_objs.EndTable("south")
        end_table.init_position(self.width*0.51, self.height*0.20)
        self.obj_group.add(end_table)

        long_table = physical_objs.SmallLongTable("vertical")
        long_table.init_position(self.width*0.20, self.height*0.40)
        self.obj_group.add(long_table)


    def _draw_boys_bathroom(self: "Area"):
        top_block = Block(BLACK, self.width, self.height*0.25-self.horizontal_wall_thickness)
        top_block.init_position(0, 0)

        bottom_block = Block(BLACK, self.width, self.height*0.25)
        bottom_block.init_position(0, self.height*0.75)

        left_block = Block(BLACK, self.width*0.25-self.vertical_wall_thickness, self.height*0.50+self.horizontal_wall_thickness)
        left_block.init_position(0, self.height*0.25-self.horizontal_wall_thickness)

        right_block = Block(BLACK, self.width*0.25-self.vertical_wall_thickness, self.height*0.50+self.horizontal_wall_thickness)
        right_block.init_position(self.width*0.75+self.vertical_wall_thickness, self.height*0.25-self.horizontal_wall_thickness)

        middle_block = Block(BLACK, self.width*0.30, self.height*0.15-self.horizontal_wall_thickness)
        middle_block.init_position(self.width*0.45+self.vertical_wall_thickness, self.height*0.60+self.horizontal_wall_thickness)

        left_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.50+self.horizontal_wall_thickness, "bathroom wall vertical.png")
        left_wall.init_position(self.width*0.25-self.vertical_wall_thickness, self.height*0.25-self.horizontal_wall_thickness)

        middle_vertical_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.15, "bathroom wall vertical.png")
        middle_vertical_wall.init_position(self.width*0.45, self.height*0.60)

        right_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.35+2.0*self.horizontal_wall_thickness, "bathroom wall vertical.png")
        right_wall.init_position(self.width*0.75, self.height*0.25-self.horizontal_wall_thickness)

        upper_wall = Block(LIGHT_YELLOW, self.width*0.50, self.horizontal_wall_thickness, "bathroom wall horizontal.png")
        upper_wall.init_position(self.width*0.25, self.height*0.25-self.horizontal_wall_thickness)

        lower_wall = Block(LIGHT_YELLOW, self.width*0.30-self.vertical_wall_thickness, self.horizontal_wall_thickness, "bathroom wall horizontal.png")
        lower_wall.init_position(self.width*0.45+self.vertical_wall_thickness, self.height*0.60)

        self.obj_group.add(top_block, bottom_block, left_block, right_block, middle_block, left_wall, middle_vertical_wall, right_wall,
                           upper_wall, lower_wall)

        toilet = physical_objs.Toilet("north")
        toilet.init_position(self.width*0.67, self.height*0.47)
        self.obj_group.add(toilet)

        bathroom_counter = physical_objs.BathroomCounter("north")       
        bathroom_counter.init_position(self.width*0.45, self.height*0.51)
        self.obj_group.add(bathroom_counter)


    def _draw_girls_bathroom(self: "Area"):
        top_block = Block(BLACK, self.width, self.height*0.25)
        top_block.init_position(0, 0)

        bottom_block = Block(BLACK, self.width, self.height*0.25-self.horizontal_wall_thickness)
        bottom_block.init_position(0, self.height*0.75+self.horizontal_wall_thickness)

        left_block = Block(BLACK, self.width*0.25-self.vertical_wall_thickness, self.height*0.50+self.horizontal_wall_thickness)
        left_block.init_position(0, self.height*0.25)

        right_block = Block(BLACK, self.width*0.25-self.vertical_wall_thickness, self.height*0.50+self.horizontal_wall_thickness)
        right_block.init_position(self.width*0.75+self.vertical_wall_thickness, self.height*0.25)

        middle_block = Block(BLACK, self.width*0.30, self.height*0.15-self.horizontal_wall_thickness)
        middle_block.init_position(self.width*0.45+self.vertical_wall_thickness, self.height*0.25)

        left_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.50+self.horizontal_wall_thickness, "bathroom wall vertical.png")
        left_wall.init_position(self.width*0.25-self.vertical_wall_thickness, self.height*0.25)

        middle_vertical_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.15-self.horizontal_wall_thickness, "bathroom wall vertical.png")
        middle_vertical_wall.init_position(self.width*0.45, self.height*0.25)

        right_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.35+self.horizontal_wall_thickness, "bathroom wall vertical.png")
        right_wall.init_position(self.width*0.75, self.height*0.40)

        upper_wall = Block(LIGHT_YELLOW, self.width*0.30+self.vertical_wall_thickness, self.horizontal_wall_thickness, "bathroom wall horizontal.png")
        upper_wall.init_position(self.width*0.45, self.height*0.40-self.horizontal_wall_thickness)
        
        lower_wall = Block(LIGHT_YELLOW, self.width*0.50, self.horizontal_wall_thickness, "bathroom wall horizontal.png")
        lower_wall.init_position(self.width*0.25, self.height*0.75)

        self.obj_group.add(top_block, bottom_block, left_block, right_block, middle_block, left_wall, middle_vertical_wall, right_wall,
                           upper_wall, lower_wall)

        toilet = physical_objs.Toilet("south")
        toilet.init_position(self.width*0.67, self.height*0.40)
        self.obj_group.add(toilet)

        bathroom_counter = physical_objs.BathroomCounter("south")
        bathroom_counter.init_position(self.width*0.45, self.height*0.40) #use to be self.width*0.47
        self.obj_group.add(bathroom_counter)
        

    def _initialize_area1_walls_and_railings(self: "Area"):
        top_block = Block(BLACK, self.width, self.height*0.20)
        top_block.init_position(0, 0)

        bottom_block = Block(BLACK, self.width, self.height*0.20)
        bottom_block.init_position(0, self.height*0.80)

        left_block = Block(BLACK, self.width*0.10, self.height*0.60)
        left_block.init_position(0, self.height*0.20)

        right_block = Block(BLACK, self.width*0.10, self.height*0.60)
        right_block.init_position(self.width*0.90, self.height*0.20)

        top_wall = Block(BRICK, self.width*0.80, self.height*0.05, "brick horizontal wall.png")
        top_wall.init_position(self.width*0.10, self.height*0.20)

        bottom_wall = Block(LIGHT_GRAY, self.width*0.80, self.height*0.05, "light gray horizontal wall.png")
        bottom_wall.init_position(self.width*0.10, self.height*0.75)

        upper_right_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.10, "light yellow vertical wall.png")
        upper_right_wall.init_position(self.width*0.90-self.vertical_wall_thickness, self.height*0.25)

        lower_right_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.15, "light yellow vertical wall.png")
        lower_right_wall.init_position(self.width*0.90-self.vertical_wall_thickness, self.height*0.60)

        upper_railing = Block(WOODEN_TAN, self.width*0.50, self.height*0.05, "railing.png")
        upper_railing.init_position(self.width*0.10, self.height*0.45)

        lower_railing = Block(WOODEN_TAN, self.width*0.50, self.height*0.05, "railing.png")
        lower_railing.init_position(self.width*0.10, self.height*0.50)

        self.obj_group.add(top_block, bottom_block, left_block, right_block, top_wall, bottom_wall, upper_right_wall, lower_right_wall, upper_railing, lower_railing)


    def _draw_area1_stairs(self: "Area", window: "Surface"):
        stairs_to_stairwell = pygame.Rect((self.width*0.10, self.height*0.25), (self.width*0.50, self.height*0.20))
        pygame.draw.rect(window, PEACH_PUFF, stairs_to_stairwell)

        stairs_to_stairwell_below = pygame.Rect((self.width*0.10, self.height*0.55), (self.width*0.50, self.height*0.20))
        pygame.draw.rect(window, PEACH_PUFF, stairs_to_stairwell_below)

        pygame.draw.line(window, BLACK, (self.width*0.20, self.height*0.25), (self.width*0.20, self.height*0.45), self.stair_bar_thickness) #upper left stair bar
        pygame.draw.line(window, BLACK, (self.width*0.30, self.height*0.25), (self.width*0.30, self.height*0.45), self.stair_bar_thickness) #second upper stair bar
        pygame.draw.line(window, BLACK, (self.width*0.40, self.height*0.25), (self.width*0.40, self.height*0.45), self.stair_bar_thickness) #third upper stair bar
        pygame.draw.line(window, BLACK, (self.width*0.50, self.height*0.25), (self.width*0.50, self.height*0.45), self.stair_bar_thickness) #upper right stair bar

        pygame.draw.line(window, BLACK, (self.width*0.20, self.height*0.55), (self.width*0.20, self.height*0.75), self.stair_bar_thickness) #lower left stair bar
        pygame.draw.line(window, BLACK, (self.width*0.30, self.height*0.55), (self.width*0.30, self.height*0.75), self.stair_bar_thickness) #second lower stair bar
        pygame.draw.line(window, BLACK, (self.width*0.40, self.height*0.55), (self.width*0.40, self.height*0.75), self.stair_bar_thickness) #third lower stair bar
        pygame.draw.line(window, BLACK, (self.width*0.50, self.height*0.55), (self.width*0.50, self.height*0.75), self.stair_bar_thickness) #lower right stair bar


    def _initialize_stairwell_walls_and_railings(self: "Area"):
        top_block = Block(BLACK, self.width, self.height*0.20)
        top_block.init_position(0, 0)

        bottom_block = Block(BLACK, self.width, self.height*0.20)
        bottom_block.init_position(0, self.height*0.80)

        left_block = Block(BLACK, self.width*0.20-self.vertical_wall_thickness, self.height*0.60)
        left_block.init_position(0, self.height*0.20)

        right_block = Block(BLACK, self.width*0.20, self.height*0.60)
        right_block.init_position(self.width*0.80, self.height*0.20)

        top_wall = Block(BRICK, self.width*0.60+self.vertical_wall_thickness, self.height*0.05, "brick horizontal wall.png")
        top_wall.init_position(self.width*0.20-self.vertical_wall_thickness, self.height*0.20)

        bottom_wall = Block(LIGHT_GRAY, self.width*0.60+self.vertical_wall_thickness, self.height*0.05, "light gray horizontal wall.png")
        bottom_wall.init_position(self.width*0.20-self.vertical_wall_thickness, self.height*0.75)

        left_wall = Block(LIGHT_YELLOW, self.vertical_wall_thickness, self.height*0.50, "light yellow vertical wall.png")
        left_wall.init_position(self.width*0.20-self.vertical_wall_thickness, self.height*0.25)

        upper_railing = Block(WOODEN_TAN, self.width*0.30, self.height*0.05, "railing.png")
        upper_railing.init_position(self.width*0.50, self.height*0.45)

        lower_railing = Block(WOODEN_TAN, self.width*0.30, self.height*0.05, "railing.png")
        lower_railing.init_position(self.width*0.50, self.height*0.50)

        self.obj_group.add(top_block, bottom_block, left_block, right_block, top_wall, bottom_wall, left_wall, upper_railing, lower_railing)


    def _draw_stairwell_stairs_and_landing(self: "Area", window: "Surface"):
        landing = pygame.Rect((self.width*0.20, self.height*0.25), (self.width*0.30, self.height*0.50))
        pygame.draw.rect(window, LIGHT_GRAY, landing)

        stairs_to_same_floor = pygame.Rect((self.width*0.50, self.height*0.25), (self.width*0.30, self.height*0.20))
        pygame.draw.rect(window, PEACH_PUFF, stairs_to_same_floor)

        stairs_to_floor_above = pygame.Rect((self.width*0.50, self.height*0.55), (self.width*0.30, self.height*0.20))
        pygame.draw.rect(window, PEACH_PUFF, stairs_to_floor_above)

        pygame.draw.line(window, BLACK, (self.width*0.60, self.height*0.25), (self.width*0.60, self.height*0.45), self.stair_bar_thickness) #upper left stair bar
        pygame.draw.line(window, BLACK, (self.width*0.70, self.height*0.25), (self.width*0.70, self.height*0.45), self.stair_bar_thickness) #upper right stair bar

        pygame.draw.line(window, BLACK, (self.width*0.60, self.height*0.55), (self.width*0.60, self.height*0.75), self.stair_bar_thickness) #lower left stair bar
        pygame.draw.line(window, BLACK, (self.width*0.70, self.height*0.55), (self.width*0.70, self.height*0.75), self.stair_bar_thickness) #lower right stair bar

###End Jeremy
