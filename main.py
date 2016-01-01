import pygame, time
from collections import namedtuple
from snake_player import *
#from snake_player_test import *
#^allows snake to access everything without cardkeys. Enemies don't spot
#this version right away somehow.
import enemies
from colors import *
from hud import *
import cameras
import frost, kay, thornton, boo, pattis
import dbh_floor1, dbh_floor2, dbh_floor3,dbh_floor4, dbh_floor5

T_SCORE_VAL1 = 15000
T_SCORE_VAL2 = 8000
T_SCORE_VAL3 = 4000
MERC_ALERT_SCORE_DECREMENT = 200
MERC_ALERT_SCORE_VAL = 10000
MERC_STUN_SCORE_DECREMENT = 100
MERC_STUN_SCORE_VAL = 5000
MGS_GAME_SCORE_INCREMENT = 800
CONTINUES_SCORE_DECREMENT = 350
CONTINUES_SCORE_VAL = 10000
NOODLES_CONSUMED_SCORE_DECREMENT = 100
NOODLES_CONSUMED_SCORE_VAL = 10000

if __name__ == "__main__":
    pygame.mixer.init(44100, -16, 1, 512) #Needed for music and sound
    pygame.init() #IMPORTANT. MUST WRITE SO SUB MODULES CAN BE LOADED!!

    #---Music Initialization--
    current_song = "all along the watchtower"
    
    #---Window Intialization---
    window_width = 1100 
    window_height = 900
    window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    game_running = False
    clock = pygame.time.Clock()
    fps = 20
    game_data_loaded = False
    ## FOR HIGH SCORES ##
    showing_play_record = False

    #---Helper Functions---
    def _navigate_weapon_select_screen(event, weapons_index, weapon_cursor_pos, on_weapon_select_screen, snake):
        '''Updates the necessary variables for navigating a weapon selection screen.'''
        if event.key == pygame.K_w:
            cursor_select = pygame.mixer.Sound("cursor_select.wav")
            pygame.mixer.Sound.play(cursor_select)
            snake.current_weapon = snake.weapons_lst[weapons_index]
            on_weapon_select_screen = False
        elif event.key == pygame.K_DOWN:
            cursor_move = pygame.mixer.Sound("cursor_move.wav")
            pygame.mixer.Sound.play(cursor_move)
            weapons_index += 1
            weapon_cursor_pos[1] += window_height*0.05

            if weapons_index > len(snake.weapons_lst)-1:
                weapon_cursor_pos[1] = window_height*0.15
                weapons_index = 0
        elif event.key == pygame.K_UP:
            cursor_move = pygame.mixer.Sound("cursor_move.wav")
            pygame.mixer.Sound.play(cursor_move)
            weapons_index -= 1
            weapon_cursor_pos[1] -= window_height*0.05

            if weapons_index < 0:
                weapon_cursor_pos[1] = window_height*0.15 + len(snake.weapons_lst)*window_height*0.05 - window_height*0.05
                weapons_index = len(snake.weapons_lst)-1

        return weapons_index, weapon_cursor_pos, on_weapon_select_screen


    def _navigate_item_select_screen(event, items_index, item_cursor_pos, on_item_select_screen, snake):
        '''Updates the necessary variables for navigating an item selection screen.'''
        if event.key == pygame.K_q:
            cursor_select = pygame.mixer.Sound("cursor_select.wav")
            pygame.mixer.Sound.play(cursor_select)
            snake.current_item = snake.items_lst[items_index]
            on_item_select_screen = False
        elif event.key == pygame.K_e:
            #print("snake.current_item.name: ", snake.current_item.name)
            #print("snake.current_item.stock: ", snake.current_item.stock)
            if snake.current_item.name == "Instant Noodles" and snake.current_item.stock > 0:
                consumed = pygame.mixer.Sound("item_consumed.wav")
                pygame.mixer.Sound.play(consumed)
                snake.health += 50
                if snake.health > 100:
                    diff = snake.health - 100
                    snake.health = snake.health - diff
                snake.current_item.stock -= 1
                snake.noodles_consumed += 1
        elif event.key == pygame.K_DOWN:
            cursor_move = pygame.mixer.Sound("cursor_move.wav")
            pygame.mixer.Sound.play(cursor_move)
            items_index += 1
            item_cursor_pos[1] += window_height*0.05

            if items_index > len(snake.items_lst)-1:
                item_cursor_pos[1] = window_height*0.15
                items_index = 0
        elif event.key == pygame.K_UP:
            cursor_move = pygame.mixer.Sound("cursor_move.wav")
            pygame.mixer.Sound.play(cursor_move)
            items_index -= 1
            item_cursor_pos[1] -= window_height*0.05

            if items_index < 0:
                item_cursor_pos[1] = window_height*0.15 + len(snake.items_lst)*window_height*0.05 - window_height*0.05
                items_index = len(snake.items_lst)-1

        return items_index, item_cursor_pos, on_item_select_screen


    def _draw_weapon_select_screen(window: "Surface", snake: "Snake"):
        window.fill(BLACK)

        rendered_cursor = font.render(inventory_cursor, True, WHITE, BLACK)
        window.blit(rendered_cursor, weapon_cursor_pos)

        
        rendered_weapon_group = font.render("WEAPON SELECT", True, WHITE, BLACK)
        window.blit(rendered_weapon_group, (window_width*0.40, window_height*0.10))

        j = 0.15
        for i in range(len(snake.weapons_lst)):
            weapon = font.render(". " + snake.weapons_lst[i].name + "     " + str(snake.weapons_lst[i].stock), True, WHITE ,BLACK)
            window.blit(weapon, (window_width*0.10, window_height*j))
            j += 0.05

        rendered_tpp_doc_group = font.render("MGS GAMES OBTAINED: " + str(snake.mgs_games) + "/5", True, WHITE, BLACK)
        window.blit(rendered_tpp_doc_group, (window_width*0.10, window_height*0.85))


    def _draw_item_select_screen(window: "Surface", snake: "Snake"):
        window.fill(BLACK)

        rendered_cursor = font.render(inventory_cursor, True, WHITE, BLACK)
        window.blit(rendered_cursor, item_cursor_pos)

        rendered_item_group = font.render("ITEM SELECT", True, WHITE, BLACK)
        window.blit(rendered_item_group, (window_width*0.40, window_height*0.10))
        
        j = 0.15
        for i in range(len(snake.items_lst)):
            item = font.render(". " + snake.items_lst[i].name + "     " + str(snake.items_lst[i].stock), True, WHITE ,BLACK)
            window.blit(item, (window_width*0.10, window_height*j))
            j += 0.05
        
        rendered_tpp_doc_group = font.render("MGS GAMES OBTAINED: " + str(snake.mgs_games) + "/5", True, WHITE, BLACK)
        window.blit(rendered_tpp_doc_group, (window_width*0.10, window_height*0.85))

    #----FOR MUSIC----
    def _load_and_play_song(current_song, song_to_play: str):
        '''Loads and plays the given song to play.'''
        if current_song != song_to_play:
            current_song = song_to_play
            pygame.mixer.music.load(song_to_play + ".ogg")
            if song_to_play == "continue":
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.play(-1)
        return current_song
    #----^FOR MUSIC----

    def _write_score_to_file(time_score, merc_alerts_score, merc_stuns_score, mgs_games_score, continues_score, noodles_consumed_score):
        '''Takes all scores of the game and writes them to a file.'''
        outfile = open("best_playthrough.txt", "w")
        outfile.write("***BEST PLAYTHROUGH***\n")
        outfile.write("\n")
        outfile.write("Time:\n")

        time_min = snake.time//60
        time_min_str = "0" + str(time_min) if len(str(time_min)) == 1 else str(time_min)
        time_sec = snake.time%60
        time_sec_str = "0" + str(time_sec) if len(str(time_sec)) == 1 else str(time_sec) 
        time_value = "{}:{}".format(time_min_str, time_sec_str) + "  (+{})".format(time_score)
        outfile.write(time_value + "\n")

        outfile.write("Mercenary Alerts:\n")
        merc_alerts_sign = "+" if merc_alerts_score > 0 else ""
        merc_alerts_value = "{}  ({}{})".format(str(snake.merc_alerts), merc_alerts_sign, merc_alerts_score)
        outfile.write(merc_alerts_value + "\n")

        outfile.write("Mecenary Stuns:\n")
        merc_stuns_sign = "+" if merc_stuns_score > 0 else ""
        merc_stuns_value = "{}  ({}{})".format(str(snake.merc_stuns), merc_stuns_sign, merc_stuns_score)
        outfile.write(merc_stuns_value + "\n")

        outfile.write("MGS Games Collected:\n")
        mgs_games_sign = "+" if mgs_games_score > 0 else ""
        mgs_games_value = "{}  ({}{})".format(str(snake.mgs_games), mgs_games_sign, mgs_games_score)
        outfile.write(mgs_games_value + "\n")

        outfile.write("Continues:\n")
        continues_score_sign = "+" if continues_score > 0 else ""
        continues_value = "{}  ({}{})".format(str(snake.continues), continues_score_sign, continues_score)
        outfile.write(continues_value + "\n")

        outfile.write("Instant Noodles Consumed:\n")
        noodles_consumed_score_sign = "+" if noodles_consumed_score > 0 else ""
        noodles_consumed_value = "{}  ({}{})".format(str(snake.noodles_consumed), noodles_consumed_score_sign, noodles_consumed_score)
        outfile.write(noodles_consumed_value + "\n")

        outfile.write("\n")
        outfile.write("SCORE:\n")
        outfile.write(str(snake.score) + "\n")
        outfile.close()
        

    game_on = True
    counter = 0
    title_screen_cursor_pos = [window_width*0.42, window_height*0.597]
    on_start_game = True
    start_height = 1
    allow_scroll = True
    till_stop = 400 #Controls the distance for how much the title will scroll up
    cur_ticks = 0
    ## FOR END GAME STUFF ##
    display_game_results = False
    
    #---Game Loop---
    while game_on:
        '''
        #----FOR MUSIC----
        current_song = _load_and_play_song(current_song, "all_along_the_watchtower")
        #----^FOR MUSIC----
        '''
        #Let's load and play the song after all of the bigger pieces of game data is loaded
        #so that the music plays after the blank screen is gone
        if not game_data_loaded:
            #---Loading Screen---...thanks http://www.pygame.org/project-Splash+screen-1186-.html!
            background = pygame.Surface(window.get_size())
            background.fill(BLUE)
            window.blit(background, (0,0))
            window.blit(pygame.font.SysFont("Arial", 30).render('Loading...', 1, YELLOW), (20,20))
            pygame.display.update()
            
            #---Sprite initalization---
            snake = Snake()
            #snake.init_position(window_width/2+200, window_height/2+200)
            snake.init_position(window_width*0.65, window_height*0.55)
            #snake.init_position(window_width*0.50, window_height*0.72) #For the final game.
            s_group = pygame.sprite.Group()
            s_group.add(snake)
            #could be good idea to pass in window so that the enemy could "see" around the world...
            #frost = Frost(window)
            #b_group1 = pygame.sprite.Group()
            #b_group1.add(frost)
            #In the final game, there should be 4 b_groups -- one for each boss


            '''CONSTRUCTING ENEMIES'''
            a1_2_enemy1 = enemies.Enemy(window, chase_speed = 12, attack_box = (150, 150, 150, 150))
            a1_2_enemy2 = enemies.Enemy(window)
            e_group1_2 = pygame.sprite.Group()
            e_group1_2.add(a1_2_enemy1, a1_2_enemy2)

            a1_3_enemy1 = enemies.Enemy(window)
            a1_3_enemy2 = enemies.Enemy(window, attack_box = (170, 170, 170, 170))
            e_group1_3 = pygame.sprite.Group()
            e_group1_3.add(a1_3_enemy1, a1_3_enemy2)


            a1_4_enemy1 = enemies.Enemy(window)
            a1_4_enemy2 = enemies.Enemy(window)
            e_group1_4 = pygame.sprite.Group()
            e_group1_4.add(a1_4_enemy1, a1_4_enemy2)
        
            a1_5_enemy1 = enemies.Enemy(window)
            a1_5_enemy2 = enemies.Enemy(window)
            e_group1_5 = pygame.sprite.Group()
            e_group1_5.add(a1_5_enemy1, a1_5_enemy2)

            a1_7_enemy1 = enemies.Enemy(window)
            e_group1_7 = pygame.sprite.Group()
            e_group1_7.add(a1_7_enemy1)

            a1_8_enemy1 = enemies.Enemy(window)
            a1_8_enemy2 = enemies.Enemy(window)
            e_group1_8 = pygame.sprite.Group()
            e_group1_8.add(a1_8_enemy1, a1_8_enemy2)

            a1_9_enemy1 = enemies.Enemy(window)
            a1_9_enemy2 = enemies.Enemy(window)
            a1_9_enemy3 = enemies.Enemy(window)
            e_group1_9 = pygame.sprite.Group()
            e_group1_9.add(a1_9_enemy1, a1_9_enemy2, a1_9_enemy3)

            a1_10_enemy1 = enemies.Enemy(window)
            a1_10_enemy2 = enemies.Enemy(window)
            a1_10_enemy3 = enemies.Enemy(window)
            e_group1_10 = pygame.sprite.Group()
            e_group1_10.add(a1_10_enemy1, a1_10_enemy2, a1_10_enemy3)

            kay_boss = kay.Kay(window)
            kay_boss_group = pygame.sprite.Group()
            kay_boss_group.add(kay_boss)

            a2_2_enemy1 = enemies.Enemy(window, color="blue")
            a2_2_enemy2 = enemies.Enemy(window, color="blue")
            a2_2_enemy3 = enemies.Enemy(window, color="blue")
            a2_2_enemy4 = enemies.Enemy(window, color = "blue")
            e_group2_2 = pygame.sprite.Group()
            e_group2_2.add(a2_2_enemy1, a2_2_enemy2, a2_2_enemy3, a2_2_enemy4)


            a2_3_camera1 = cameras.Camera(window, "west")
            e_group2_3 = pygame.sprite.Group()
            e_group2_3.add(a2_3_camera1)
            
            a2_4_enemy1 = enemies.Enemy(window, color="blue")
            a2_4_enemy2 = enemies.Enemy(window, color="blue")
            #a2_4_enemy3 = enemies.Enemy(window, color="blue")
            e_group2_4 = pygame.sprite.Group()
            #e_group2_4.add(a2_4_enemy1, a2_4_enemy2, a2_4_enemy3)
            e_group2_4.add(a2_4_enemy1, a2_4_enemy2)

            a2_5_enemy1 = enemies.Enemy(window, color="blue")
            a2_5_enemy2 = enemies.Enemy(window, color="blue")
            e_group2_5 = pygame.sprite.Group()
            e_group2_5.add(a2_5_enemy1, a2_5_enemy2)

            a2_6_enemy1 = enemies.Enemy(window, color="blue")
            a2_6_enemy2 = enemies.Enemy(window, color="blue")
            a2_6_enemy3 = enemies.Enemy(window, color="blue")
            e_group2_6 = pygame.sprite.Group()
            e_group2_6.add(a2_6_enemy1, a2_6_enemy2, a2_6_enemy3)

            a2_7_enemy1 = enemies.Enemy(window, color="blue")
            a2_7_enemy2 = enemies.Enemy(window, color="blue")
            #a2_7_enemy3 = enemies.Enemy(window, color="blue")
            e_group2_7 = pygame.sprite.Group()
            #e_group2_7.add(a2_7_enemy1, a2_7_enemy2, a2_7_enemy3)
            e_group2_7.add(a2_7_enemy1, a2_7_enemy2)

            a2_8_enemy1 = enemies.Enemy(window, color="blue")
            a2_8_enemy2 = enemies.Enemy(window, color="blue")
            a2_8_enemy3 = enemies.Enemy(window, color="blue")
            #a2_8_enemy4 = enemies.Enemy(window, color="blue")
            #a2_8_enemy5 = enemies.Enemy(window, color="blue")
            e_group2_8 = pygame.sprite.Group()
            #e_group2_8.add(a2_8_enemy1, a2_8_enemy2, a2_8_enemy3, a2_8_enemy4, a2_8_enemy5)
            #e_group2_8.add(a2_8_enemy1, a2_8_enemy2, a2_8_enemy3, a2_8_enemy4)
            e_group2_8.add(a2_8_enemy1, a2_8_enemy2, a2_8_enemy3)

            a2_9_enemy1 = enemies.Enemy(window, color="blue")
            a2_9_enemy2 = enemies.Enemy(window, color="blue")
            e_group2_9 = pygame.sprite.Group()
            e_group2_9.add(a2_9_enemy1, a2_9_enemy2)

            a2_12_enemy1 = enemies.Enemy(window, color="blue")
            a2_12_enemy2 = enemies.Enemy(window, color="blue")
            e_group2_12 = pygame.sprite.Group()
            e_group2_12.add(a2_12_enemy1, a2_12_enemy2)

            a2_13_enemy1 = enemies.Enemy(window, color="blue")
            a2_13_enemy2 = enemies.Enemy(window, color="blue")
            e_group2_13 = pygame.sprite.Group()
            e_group2_13.add(a2_13_enemy1, a2_13_enemy2)

            a2_14_enemy1 = enemies.Enemy(window, color="blue")
            a2_14_enemy2 = enemies.Enemy(window, color="blue")
            #a2_14_enemy3 = enemies.Enemy(window, color="blue")
            e_group2_14 = pygame.sprite.Group()
            #e_group2_14.add(a2_14_enemy1, a2_14_enemy2, a2_14_enemy3)
            e_group2_14.add(a2_14_enemy1, a2_14_enemy2)

            a2_15_enemy1 = enemies.Enemy(window, color="blue")
            a2_15_enemy2 = enemies.Enemy(window, color="blue")
            #a2_15_enemy3 = enemies.Enemy(window, color="blue")
            e_group2_15 = pygame.sprite.Group()
            #e_group2_15.add(a2_15_enemy1, a2_15_enemy2, a2_15_enemy3)
            e_group2_15.add(a2_15_enemy1, a2_15_enemy2)

            a2_17_enemy1 = enemies.Enemy(window, color="blue")
            a2_17_enemy2 = enemies.Enemy(window, color="blue")
            a2_17_enemy3 = enemies.Enemy(window, color="blue")
            e_group2_17 = pygame.sprite.Group()
            e_group2_17.add(a2_17_enemy1, a2_17_enemy2, a2_17_enemy3)

            a2_18_enemy1 = enemies.Enemy(window, color="blue")
            a2_18_enemy2 = enemies.Enemy(window, color="blue")
            #a2_18_enemy3 = enemies.Enemy(window, color="blue")
            e_group2_18 = pygame.sprite.Group()
            #e_group2_18.add(a2_18_enemy1, a2_18_enemy2, a2_18_enemy3)
            e_group2_18.add(a2_18_enemy1, a2_18_enemy2)

            a2_19_enemy1 = enemies.Enemy(window, color="blue")
            a2_19_enemy2 = enemies.Enemy(window, color="blue")
            #a2_19_enemy3 = enemies.Enemy(window, color="blue")
            e_group2_19 = pygame.sprite.Group()
            #e_group2_19.add(a2_19_enemy1, a2_19_enemy2, a2_19_enemy3)
            e_group2_19.add(a2_19_enemy1, a2_19_enemy2)

            thornton_boss = thornton.Thornton(window)
            boo_companion = boo.Boo(window)
            boo_and_thornton_boss_group = pygame.sprite.Group()
            boo_and_thornton_boss_group.add(thornton_boss, boo_companion)

            a3_2_enemy1 = enemies.Enemy(window, color="gray")
            a3_2_enemy2 = enemies.Enemy(window, color="gray")
            a3_2_enemy3 = enemies.Enemy(window, color="gray")
            a3_2_enemy4 = enemies.Enemy(window, color = "gray")
            a3_2_enemy5 = enemies.Enemy(window, color = "gray")
            e_group3_2 = pygame.sprite.Group()
            e_group3_2.add(a3_2_enemy1, a3_2_enemy2, a3_2_enemy3, a3_2_enemy4, a3_2_enemy5)

            a3_3_enemy1 = enemies.Enemy(window, color="gray")
            a3_3_enemy2 = enemies.Enemy(window, color="gray")
            e_group3_3 = pygame.sprite.Group()
            e_group3_3.add(a3_3_enemy1, a3_3_enemy2)

            a3_4_enemy1 = enemies.Enemy(window, color="gray")
            a3_4_enemy2 = enemies.Enemy(window, color="gray")
            a3_4_enemy3 = enemies.Enemy(window, color="gray")
            e_group3_4 = pygame.sprite.Group()
            e_group3_4.add(a3_4_enemy1, a3_4_enemy2, a3_4_enemy3)

            a3_5_enemy1 = enemies.Enemy(window, color="gray")
            a3_5_enemy2 = enemies.Enemy(window, color="gray")
            a3_5_enemy3 = enemies.Enemy(window, color="gray")

            e_group3_5 = pygame.sprite.Group()
            e_group3_5.add(a3_5_enemy1, a3_5_enemy2, a3_5_enemy3)

            a3_6_enemy1 = enemies.Enemy(window, color="gray")
            a3_6_enemy2 = enemies.Enemy(window, color="gray")
            a3_6_enemy3 = enemies.Enemy(window, color="gray")
            e_group3_6 = pygame.sprite.Group()
            e_group3_6.add(a3_6_enemy1, a3_6_enemy2, a3_6_enemy3)

            a3_7_enemy1 = enemies.Enemy(window, color="gray")
            a3_7_enemy2 = enemies.Enemy(window, color="gray")
            a3_7_enemy3 = enemies.Enemy(window, color="gray")
            e_group3_7 = pygame.sprite.Group()
            e_group3_7.add(a3_7_enemy1, a3_7_enemy2, a3_7_enemy3)

            a3_8_enemy1 = enemies.Enemy(window, color="gray")
            a3_8_enemy2 = enemies.Enemy(window, color="gray")
            a3_8_enemy3 = enemies.Enemy(window, color="gray")
            a3_8_enemy4 = enemies.Enemy(window, color="gray")
            #a3_8_enemy5 = enemies.Enemy(window, color="gray")
            e_group3_8 = pygame.sprite.Group()
            #e_group3_8.add(a3_8_enemy1, a3_8_enemy2, a3_8_enemy3, a3_8_enemy4, a3_8_enemy5)
            e_group3_8.add(a3_8_enemy1, a3_8_enemy2, a3_8_enemy3, a3_8_enemy4)

            a3_9_enemy1 = enemies.Enemy(window, color="gray")
            a3_9_enemy2 = enemies.Enemy(window, color="gray")
            e_group3_9 = pygame.sprite.Group()
            e_group3_9.add(a3_9_enemy1, a3_9_enemy2)

            a3_10_enemy1 = enemies.Enemy(window, color="gray")
            a3_10_enemy2 = enemies.Enemy(window, color="gray")
            e_group3_10 = pygame.sprite.Group()
            e_group3_10.add(a3_10_enemy1, a3_10_enemy2)

            a3_12_enemy1 = enemies.Enemy(window, color="gray")
            a3_12_enemy2 = enemies.Enemy(window, color="gray")
            e_group3_12 = pygame.sprite.Group()
            e_group3_12.add(a3_12_enemy1, a3_12_enemy2)

            a3_13_enemy1 = enemies.Enemy(window, color="gray")
            a3_13_enemy2 = enemies.Enemy(window, color="gray")
            a3_13_enemy3 = enemies.Enemy(window, color="gray")
            e_group3_13 = pygame.sprite.Group()
            #e_group3_13.add(a3_13_enemy1, a3_13_enemy2)
            e_group3_13.add(a3_13_enemy1, a3_13_enemy2, a3_13_enemy3)

            a3_14_enemy1 = enemies.Enemy(window, color="gray")
            a3_14_enemy2 = enemies.Enemy(window, color="gray")
            a3_14_enemy3 = enemies.Enemy(window, color="gray")
            e_group3_14 = pygame.sprite.Group()
            e_group3_14.add(a3_14_enemy1, a3_14_enemy2, a3_14_enemy3)

            a3_15_enemy1 = enemies.Enemy(window, color="gray")
            a3_15_enemy2 = enemies.Enemy(window, color="gray")
            a3_15_enemy3 = enemies.Enemy(window, color="gray")
            e_group3_15 = pygame.sprite.Group()
            e_group3_15.add(a3_15_enemy1, a3_15_enemy2, a3_15_enemy3)

            a3_17_enemy1 = enemies.Enemy(window, color="gray")
            a3_17_enemy2 = enemies.Enemy(window, color="gray")
            a3_17_enemy3 = enemies.Enemy(window, color="gray")
            e_group3_17 = pygame.sprite.Group()
            e_group3_17.add(a3_17_enemy1, a3_17_enemy2, a3_17_enemy3)

            a3_18_enemy1 = enemies.Enemy(window, color="gray")
            a3_18_enemy2 = enemies.Enemy(window, color="gray")
            a3_18_enemy3 = enemies.Enemy(window, color="gray")
            e_group3_18 = pygame.sprite.Group()
            e_group3_18.add(a3_18_enemy1, a3_18_enemy2, a3_18_enemy3)

            a3_19_enemy1 = enemies.Enemy(window, color="gray")
            a3_19_enemy2 = enemies.Enemy(window, color="gray")
            a3_19_enemy3 = enemies.Enemy(window, color="gray")
            e_group3_19 = pygame.sprite.Group()
            e_group3_19.add(a3_19_enemy1, a3_19_enemy2, a3_19_enemy3)

            pattis_boss = pattis.Pattis(window)
            pattis_boss_group = pygame.sprite.Group()
            pattis_boss_group.add(pattis_boss)
            
            a4_2_enemy1 = enemies.Enemy(window, color="green")
            a4_2_enemy2 = enemies.Enemy(window, color="green")
            a4_2_enemy3 = enemies.Enemy(window, color="green")
            a4_2_enemy4 = enemies.Enemy(window, color = "green")
            a4_2_enemy5 = enemies.Enemy(window, color = "green")
            a4_2_enemy6 = enemies.Enemy(window, color = "green")
            a4_2_enemy7 = enemies.Enemy(window, color = "green")
            e_group4_2 = pygame.sprite.Group()
            e_group4_2.add(a4_2_enemy1, a4_2_enemy2, a4_2_enemy3, a4_2_enemy4,
                           a4_2_enemy5, a4_2_enemy6, a4_2_enemy7)

            a4_3_camera1 = cameras.Camera(window, "west")
            a4_3_enemy1 = enemies.Enemy(window, color="green")
            a4_3_enemy2 = enemies.Enemy(window, color="green")
            e_group4_3 = pygame.sprite.Group()
            e_group4_3.add(a4_3_camera1, a4_3_enemy1, a4_3_enemy2)
            
            a4_4_enemy1 = enemies.Enemy(window, color="green")
            a4_4_enemy2 = enemies.Enemy(window, color="green")
            a4_4_enemy3 = enemies.Enemy(window, color="green")
            e_group4_4 = pygame.sprite.Group()
            e_group4_4.add(a4_4_enemy1, a4_4_enemy2, a4_4_enemy3)

            a4_5_enemy1 = enemies.Enemy(window, color="green")
            a4_5_enemy2 = enemies.Enemy(window, color="green")
            a4_5_enemy3 = enemies.Enemy(window, color="green")
            e_group4_5 = pygame.sprite.Group()
            #e_group4_5.add(a4_5_enemy1, a4_5_enemy2)
            e_group4_5.add(a4_5_enemy1, a4_5_enemy2, a4_5_enemy3)

            a4_6_enemy1 = enemies.Enemy(window, color="green")
            a4_6_enemy2 = enemies.Enemy(window, color="green")
            a4_6_enemy3 = enemies.Enemy(window, color="green")
            e_group4_6 = pygame.sprite.Group()
            e_group4_6.add(a4_6_enemy1, a4_6_enemy2, a4_6_enemy3)

            a4_7_enemy1 = enemies.Enemy(window, color="green")
            a4_7_enemy2 = enemies.Enemy(window, color="green")
            a4_7_enemy3 = enemies.Enemy(window, color="green")
            e_group4_7 = pygame.sprite.Group()
            e_group4_7.add(a4_7_enemy1, a4_7_enemy2, a4_7_enemy3)

            a4_8_enemy1 = enemies.Enemy(window, color="green")
            a4_8_enemy2 = enemies.Enemy(window, color="green")
            a4_8_enemy3 = enemies.Enemy(window, color="green")
            a4_8_enemy4 = enemies.Enemy(window, color="green")
            #a4_8_enemy5 = enemies.Enemy(window, color="green")
            e_group4_8 = pygame.sprite.Group()
            #e_group4_8.add(a4_8_enemy1, a4_8_enemy2, a4_8_enemy3, a4_8_enemy4, a4_8_enemy5)
            e_group4_8.add(a4_8_enemy1, a4_8_enemy2, a4_8_enemy3, a4_8_enemy4)

            a4_9_enemy1 = enemies.Enemy(window, color="green")
            a4_9_enemy2 = enemies.Enemy(window, color="green")
            e_group4_9 = pygame.sprite.Group()
            e_group4_9.add(a4_9_enemy1, a4_9_enemy2)

            a4_10_camera1 = cameras.Camera(window, "south")
            a4_10_enemy1 = enemies.Enemy(window, color="green")
            e_group4_10 = pygame.sprite.Group()
            e_group4_10.add(a4_10_camera1, a4_10_enemy1)

            a4_12_enemy1 = enemies.Enemy(window, color="green")
            a4_12_enemy2 = enemies.Enemy(window, color="green")
            e_group4_12 = pygame.sprite.Group()
            e_group4_12.add(a4_12_enemy1, a4_12_enemy2)

            a4_13_enemy1 = enemies.Enemy(window, color="green")
            a4_13_enemy2 = enemies.Enemy(window, color="green")
            a4_13_enemy3 = enemies.Enemy(window, color="green")
            a4_13_enemy4 = enemies.Enemy(window, color="green")
            a4_13_enemy5 = enemies.Enemy(window, color="green")
            e_group4_13 = pygame.sprite.Group()
            e_group4_13.add(a4_13_enemy1, a4_13_enemy2, a4_13_enemy3, a4_13_enemy4, a4_13_enemy5)

            a4_14_enemy1 = enemies.Enemy(window, color="green")
            a4_14_enemy2 = enemies.Enemy(window, color="green")
            a4_14_enemy3 = enemies.Enemy(window, color="green")
            a4_14_enemy4 = enemies.Enemy(window, color="green")
            e_group4_14 = pygame.sprite.Group()
            #e_group4_14.add(a4_14_enemy1, a4_14_enemy2, a4_14_enemy3)
            e_group4_14.add(a4_14_enemy1, a4_14_enemy2, a4_14_enemy3, a4_14_enemy4)

            a4_15_enemy1 = enemies.Enemy(window, color="green")
            a4_15_enemy2 = enemies.Enemy(window, color="green")
            a4_15_enemy3 = enemies.Enemy(window, color="green")
            a4_15_enemy4 = enemies.Enemy(window, color="green")
            e_group4_15 = pygame.sprite.Group()
            #e_group4_15.add(a4_15_enemy1, a4_15_enemy2, a4_15_enemy3)
            e_group4_15.add(a4_15_enemy1, a4_15_enemy2, a4_15_enemy3, a4_15_enemy4)

            a4_15_inner_enemy1 = enemies.Enemy(window, color="green")
            a4_15_inner_enemy2 = enemies.Enemy(window, color="green")
            a4_15_inner_enemy3 = enemies.Enemy(window, color="green")
            a4_15_inner_enemy4 = enemies.Enemy(window, color="green")
            a4_15_inner_enemy5 = enemies.Enemy(window, color="green")
            a4_15_inner_enemy6 = enemies.Enemy(window, color="green")
            a4_15_inner_enemy7 = enemies.Enemy(window, color="green")
            a4_15_inner_enemy8 = enemies.Enemy(window, color="green")

            e_group_inner_4_15 = pygame.sprite.Group()
            e_group_inner_4_15.add(a4_15_inner_enemy1, a4_15_inner_enemy2, a4_15_inner_enemy3, a4_15_inner_enemy4,
                            a4_15_inner_enemy5, a4_15_inner_enemy6, a4_15_inner_enemy7, a4_15_inner_enemy8)
    
            a4_17_enemy1 = enemies.Enemy(window, color="green")
            a4_17_enemy2 = enemies.Enemy(window, color="green")
            a4_17_enemy3 = enemies.Enemy(window, color="green")
            a4_17_enemy4 = enemies.Enemy(window, color="green")
            e_group4_17 = pygame.sprite.Group()
            e_group4_17.add(a4_17_enemy1, a4_17_enemy2, a4_17_enemy3, a4_17_enemy4)

            a4_18_enemy1 = enemies.Enemy(window, color="green")
            a4_18_enemy2 = enemies.Enemy(window, color="green")
            a4_18_enemy3 = enemies.Enemy(window, color="green")
            e_group4_18 = pygame.sprite.Group()
            e_group4_18.add(a4_18_enemy1, a4_18_enemy2, a4_18_enemy3)

            a4_19_enemy1 = enemies.Enemy(window, color="green")
            a4_19_enemy2 = enemies.Enemy(window, color="green")
            a4_19_enemy3 = enemies.Enemy(window, color="green")
            a4_19_enemy4 = enemies.Enemy(window, color="green")
            e_group4_19 = pygame.sprite.Group()
            e_group4_19.add(a4_19_enemy1, a4_19_enemy2, a4_19_enemy3, a4_19_enemy4)

            frost_boss = frost.Frost(window)
            frost_boss_group = pygame.sprite.Group()
            frost_boss_group.add(frost_boss)
            
            #---Area initialization---
            Neighbors = namedtuple("Neighbors", "north1 north2 north3 north4 east1 east2 east3 east4 south1 south2 south3 south4 west1 west2 west3 west4 inner1 inner2 inner3 inner4")
            area_dict = {}
            
            area1_1 = dbh_floor1.Area1_1(window_width, window_height, snake, None)
            area1_2 = dbh_floor1.Area1_2(window_width, window_height, snake, e_group1_2)
            area1_3 = dbh_floor1.Area1_3(window_width, window_height, snake, e_group1_3)
            area1_3_upper_left_inner_area = dbh_floor1.Area1_3_UpperLeftInnerArea(window_width, window_height, snake, None)
            area1_4 = dbh_floor1.Area1_4(window_width, window_height, snake, e_group1_4)
            area1_5 = dbh_floor1.Area1_5(window_width, window_height, snake, e_group1_5)
            area1_5_bathroom_entrances = dbh_floor1.Area1_5_BathroomEntrances(window_width, window_height, snake, None)
            area1_5_girls_bathroom = dbh_floor1.Area1_5_GirlsBathroom(window_width, window_height, snake, None)
            area1_6 = dbh_floor1.Area1_6(window_width, window_height, snake, None)
            area1_6_lower_right_inner_area = dbh_floor1.Area1_6_LowerRightInnerArea(window_width, window_height, snake, None)
            area1_6_left_inner_area = dbh_floor1.Area1_6_LeftInnerArea(window_width, window_height, snake, None)
            area1_7 = dbh_floor1.Area1_7(window_width, window_height, snake, e_group1_7)
            area1_7_upper_inner_area = dbh_floor1.Area1_7_UpperInnerArea(window_width, window_height, snake, None)
            area1_8 = dbh_floor1.Area1_8(window_width, window_height, snake, e_group1_8)
            area1_8_boys_bathroom = dbh_floor1.Area1_8_BoysBathroom(window_width, window_height, snake, None)
            area1_9 = dbh_floor1.Area1_9(window_width, window_height, snake, e_group1_9)
            area1_10 = dbh_floor1.Area1_10(window_width, window_height, snake, e_group1_10)
            area1_11 = dbh_floor1.Area1_11(window_width, window_height, snake, None)
            area1_11_inner_area = dbh_floor1.Area1_11_InnerArea(window_width, window_height, snake, None)
            area2_1 = dbh_floor2.Area2_1(window_width, window_height, snake, None)
            stairwell2_1_to_3_1 = dbh_floor2.Stairwell2_1_to_3_1(window_width, window_height, snake, None)
            area2_2 = dbh_floor2.Area2_2(window_width, window_height, snake, e_group2_2)
            area2_3 = dbh_floor2.Area2_3(window_width, window_height, snake, e_group2_3)
            area2_3_left_inner_area = dbh_floor2.Area2_3_LeftInnerArea(window_width, window_height, snake, None)
            area2_3_right_inner_area = dbh_floor2.Area2_3_RightInnerArea(window_width, window_height, snake, None)
            area2_4 = dbh_floor2.Area2_4(window_width, window_height, snake, e_group2_4)
            area2_4_upper_right_inner_area = dbh_floor2.Area2_4_UpperRightInnerArea(window_width, window_height, snake, None)
            area2_5 = dbh_floor2.Area2_5(window_width, window_height, snake, e_group2_5)
            area2_5_middle_inner_area = dbh_floor2.Area2_5_MiddleInnerArea(window_width, window_height, snake, None)
            area2_6 = dbh_floor2.Area2_6(window_width, window_height, snake, e_group2_6)
            area2_6_middle_inner_area = dbh_floor2.Area2_6_MiddleInnerArea(window_width, window_height, snake, None)
            area2_7 = dbh_floor2.Area2_7(window_width, window_height, snake, e_group2_7)
            area2_7_upper_left_inner_area = dbh_floor2.Area2_7_UpperLeftInnerArea(window_width, window_height, snake, None)
            area2_8 = dbh_floor2.Area2_8(window_width, window_height, snake, e_group2_8)
            area2_8_left_inner_area = dbh_floor2.Area2_8_LeftInnerArea(window_width, window_height, snake, None)
            area2_8_upper_inner_area = dbh_floor2.Area2_8_UpperInnerArea(window_width, window_height, snake, None)
            area2_9 = dbh_floor2.Area2_9(window_width, window_height, snake, e_group2_9)
            area2_9_upper_left_inner_area = dbh_floor2.Area2_9_UpperLeftInnerArea(window_width, window_height, snake, None)            
            area2_10 = dbh_floor2.Area2_10(window_width, window_height, snake, None)
            area2_10_girls_bathroom = dbh_floor2.Area2_10_GirlsBathroom(window_width, window_height, snake, None)
            area2_11 = dbh_floor2.Area2_11(window_width, window_height, snake, None)
            area2_12 = dbh_floor2.Area2_12(window_width, window_height, snake, e_group2_12)
            area2_12_kay_boss_area = dbh_floor2.Area2_12_KayBossArea(window_width, window_height, snake, kay_boss_group)
            area2_13 = dbh_floor2.Area2_13(window_width, window_height, snake, e_group2_13)
            area2_13_boys_bathroom = dbh_floor2.Area2_13_BoysBathroom(window_width, window_height, snake, None)
            area2_14 = dbh_floor2.Area2_14(window_width, window_height, snake, e_group2_14)
            area2_14_upper_middle_inner_area = dbh_floor2.Area2_14_UpperMiddleInnerArea(window_width, window_height, snake, None)
            area2_14_lower_right_inner_area = dbh_floor2.Area2_14_LowerRightInnerArea(window_width, window_height, snake, None)
            area2_15 = dbh_floor2.Area2_15(window_width, window_height, snake, e_group2_15)
            area2_15_lower_inner_area = dbh_floor2.Area2_15_LowerInnerArea(window_width, window_height, snake, None)
            area2_16 = dbh_floor2.Area2_16(window_width, window_height, snake, None)
            area2_16_inner_area = dbh_floor2.Area2_16_InnerArea(window_width, window_height, snake, None)
            area2_17 = dbh_floor2.Area2_17(window_width, window_height, snake, e_group2_17)
            area2_18 = dbh_floor2.Area2_18(window_width, window_height, snake, e_group2_18)
            area2_19 = dbh_floor2.Area2_19(window_width, window_height, snake, e_group2_19)
            area2_19_lower_left_inner_area = dbh_floor2.Area2_19_LowerLeftInnerArea(window_width, window_height, snake, None)
            area2_19_right_inner_area = dbh_floor2.Area2_19_RightInnerArea(window_width, window_height, snake, None)
            area3_1 = dbh_floor3.Area3_1(window_width, window_height, snake, None)
            stairwell3_1_to_4_1 = dbh_floor3.Stairwell3_1_to_4_1(window_width, window_height, snake, None)
            area3_2 = dbh_floor3.Area3_2(window_width, window_height, snake, e_group3_2)
            area3_2_lower_inner_area = dbh_floor3.Area3_2_LowerInnerArea(window_width, window_height, snake, None)
            area3_3 = dbh_floor3.Area3_3(window_width, window_height, snake, e_group3_3)
            area3_3_left_inner_area = dbh_floor3.Area3_3_LeftInnerArea(window_width, window_height, snake, None)
            area3_3_right_inner_area = dbh_floor3.Area3_3_RightInnerArea(window_width, window_height, snake, None)
            area3_4 = dbh_floor3.Area3_4(window_width, window_height, snake, e_group3_4)
            area3_4_upper_right_inner_area = dbh_floor3.Area3_4_UpperRightInnerArea(window_width, window_height, snake, None)
            area3_5 = dbh_floor3.Area3_5(window_width, window_height, snake, e_group3_5)
            area3_5_middle_inner_area = dbh_floor3.Area3_5_MiddleInnerArea(window_width, window_height, snake, None)
            area3_6 = dbh_floor3.Area3_6(window_width, window_height, snake, e_group3_6)            
            area3_6_right_inner_area = dbh_floor3.Area3_6_RightInnerArea(window_width, window_height, snake, None)
            area3_6_middle_inner_area = dbh_floor3.Area3_6_MiddleInnerArea(window_width, window_height, snake, None)
            area3_7 = dbh_floor3.Area3_7(window_width, window_height, snake, e_group3_7)
            area3_7_upper_left_inner_area = dbh_floor3.Area3_7_UpperLeftInnerArea(window_width, window_height, snake, None)
            area3_8 = dbh_floor3.Area3_8(window_width, window_height, snake, e_group3_8)
            area3_8_left_inner_area = dbh_floor3.Area3_8_LeftInnerArea(window_width, window_height, snake, None)
            area3_8_thornton_boss_area = dbh_floor3.Area3_8_ThorntonBossArea(window_width, window_height, snake, boo_and_thornton_boss_group)
            area3_9 = dbh_floor3.Area3_9(window_width, window_height, snake, e_group3_9)
            area3_10 = dbh_floor3.Area3_10(window_width, window_height, snake, e_group3_10)
            area3_10_girls_bathroom = dbh_floor3.Area3_10_GirlsBathroom(window_width, window_height, snake, None)
            area3_11 = dbh_floor3.Area3_11(window_width, window_height, snake, None)
            area3_12 = dbh_floor3.Area3_12(window_width, window_height, snake, e_group3_12)
            area3_13_right_inner_area = dbh_floor3.Area3_13_RightInnerArea(window_width, window_height, snake, None)
            area3_13 = dbh_floor3.Area3_13(window_width, window_height, snake, e_group3_13)
            area3_13_boys_bathroom = dbh_floor3.Area3_13_BoysBathroom(window_width, window_height, snake, None)
            area3_14 = dbh_floor3.Area3_14(window_width, window_height, snake, e_group3_14)
            area3_14_upper_middle_inner_area = dbh_floor3.Area3_14_UpperMiddleInnerArea(window_width, window_height, snake, None)
            area3_14_lower_right_inner_area = dbh_floor3.Area3_14_LowerRightInnerArea(window_width, window_height, snake, None)
            area3_15 = dbh_floor3.Area3_15(window_width, window_height, snake, e_group3_15)
            area3_15_lower_inner_area = dbh_floor3.Area3_15_LowerInnerArea(window_width, window_height, snake, None)
            area3_16 = dbh_floor3.Area3_16(window_width, window_height, snake, None)
            area3_16_inner_area = dbh_floor3.Area3_16_InnerArea(window_width, window_height, snake, None)
            area3_17 = dbh_floor3.Area3_17(window_width, window_height, snake, e_group3_17)
            area3_18 = dbh_floor3.Area3_18(window_width, window_height, snake, e_group3_18)
            area3_19 = dbh_floor3.Area3_19(window_width, window_height, snake, e_group3_19)
            area3_19_lower_left_inner_area = dbh_floor3.Area3_19_LowerLeftInnerArea(window_width, window_height, snake, None)
            area3_19_right_inner_area = dbh_floor3.Area3_19_RightInnerArea(window_width, window_height, snake, None)
            area4_1 = dbh_floor4.Area4_1(window_width, window_height, snake, None)
            stairwell4_1_to_5_1 = dbh_floor4.Stairwell4_1_to_5_1(window_width, window_height, snake, None)
            area4_2 = dbh_floor4.Area4_2(window_width, window_height, snake, e_group4_2)
            area4_3 = dbh_floor4.Area4_3(window_width, window_height, snake, e_group4_3)
            area4_4_left_inner_area = dbh_floor4.Area4_4_LeftInnerArea(window_width, window_height, snake, None)
            area4_4_right_inner_area = dbh_floor4.Area4_4_RightInnerArea(window_width, window_height, snake, None)
            area4_4 = dbh_floor4.Area4_4(window_width, window_height, snake, e_group4_4)
            area4_4_upper_right_inner_area = dbh_floor4.Area4_4_UpperRightInnerArea(window_width, window_height, snake, None)
            area4_5 = dbh_floor4.Area4_5(window_width, window_height, snake, e_group4_5)
            area4_5_middle_inner_area = dbh_floor4.Area4_5_MiddleInnerArea(window_width, window_height, snake, None)
            area4_6 = dbh_floor4.Area4_6(window_width, window_height, snake, e_group4_6)

            area4_6_right_inner_area = dbh_floor4.Area4_6_RightInnerArea(window_width, window_height, snake, None)

            area4_6_middle_inner_area = dbh_floor4.Area4_6_MiddleInnerArea(window_width, window_height, snake, None)
            area4_7 = dbh_floor4.Area4_7(window_width, window_height, snake, e_group4_7)
            area4_7_upper_left_inner_area = dbh_floor4.Area4_7_UpperLeftInnerArea(window_width, window_height, snake, None)
            area4_8 = dbh_floor4.Area4_8(window_width, window_height, snake, e_group4_8)
            area4_8_left_inner_area = dbh_floor4.Area4_8_LeftInnerArea(window_width, window_height, snake, None)
            area4_8_upper_inner_area = dbh_floor4.Area4_8_UpperInnerArea(window_width, window_height, snake, None)
            area4_9 = dbh_floor4.Area4_9(window_width, window_height, snake, e_group4_9)
            area4_10 = dbh_floor4.Area4_10(window_width, window_height, snake, e_group4_10)
            area4_10_girls_bathroom = dbh_floor4.Area4_10_GirlsBathroom(window_width, window_height, snake, None)
            area4_11 = dbh_floor4.Area4_11(window_width, window_height, snake, None)
            area4_12 = dbh_floor4.Area4_12(window_width, window_height, snake, e_group4_12)
            area4_14_right_inner_area = dbh_floor4.Area4_14_RightInnerArea(window_width, window_height, snake, None)
            area4_13 = dbh_floor4.Area4_13(window_width, window_height, snake, e_group4_13)
            area4_13_boys_bathroom = dbh_floor4.Area4_13_BoysBathroom(window_width, window_height, snake, None)
            area4_14 = dbh_floor4.Area4_14(window_width, window_height, snake, e_group4_14)
            area4_14_upper_middle_inner_area = dbh_floor4.Area4_14_UpperMiddleInnerArea(window_width, window_height, snake, None)
            area4_14_lower_right_inner_area = dbh_floor4.Area4_14_LowerRightInnerArea(window_width, window_height, snake, None)
            area4_15 = dbh_floor4.Area4_15(window_width, window_height, snake, e_group4_15)
            area4_15_lower_inner_area = dbh_floor4.Area4_15_LowerInnerArea(window_width, window_height, snake, e_group_inner_4_15)
            area4_16 = dbh_floor4.Area4_16(window_width, window_height, snake, None)
            area4_16_inner_area = dbh_floor4.Area4_16_InnerArea(window_width, window_height, snake, None)
            area4_17 = dbh_floor4.Area4_17(window_width, window_height, snake, e_group4_17)
            area4_18 = dbh_floor4.Area4_18(window_width, window_height, snake, e_group4_18)
            area4_19 = dbh_floor4.Area4_19(window_width, window_height, snake, e_group4_19)
            area4_19_lower_left_inner_area = dbh_floor4.Area4_19_LowerLeftInnerArea(window_width, window_height, snake, None)
            area4_19_pattis_boss_area = dbh_floor4.Area4_19_PattisBossArea(window_width, window_height, snake, pattis_boss_group)           


            area5_1 = dbh_floor5.Area5_1(window_width, window_height, snake, None)
            area5_2 = dbh_floor5.Area5_2(window_width, window_height, snake, frost_boss_group)
            area5_3 = dbh_floor5.Area5_3(window_width, window_height, snake, frost_boss_group)
            area5_5_left_inner_area = dbh_floor5.Area5_5_LeftInnerArea(window_width, window_height, snake, None)
            area5_5_right_inner_area = dbh_floor5.Area5_5_RightInnerArea(window_width, window_height, snake, None)
            area5_4 = dbh_floor5.Area5_4(window_width, window_height, snake, frost_boss_group)
            area5_5_upper_right_inner_area = dbh_floor5.Area5_5_UpperRightInnerArea(window_width, window_height, snake, None)
            area5_5 = dbh_floor5.Area5_5(window_width, window_height, snake, frost_boss_group)
            area5_5_middle_inner_area = dbh_floor5.Area5_5_MiddleInnerArea(window_width, window_height, snake, None)
            area5_6 = dbh_floor5.Area5_6(window_width, window_height, snake, frost_boss_group)
            area5_6_middle_inner_area = dbh_floor5.Area5_6_MiddleInnerArea(window_width, window_height, snake, None)
            area5_7 = dbh_floor5.Area5_7(window_width, window_height, snake, frost_boss_group)
            area5_7_upper_left_inner_area = dbh_floor5.Area5_7_UpperLeftInnerArea(window_width, window_height, snake, None)
            area5_8 = dbh_floor5.Area5_8(window_width, window_height, snake, frost_boss_group)
            area5_8_left_inner_area = dbh_floor5.Area5_8_LeftInnerArea(window_width, window_height, snake, None)
            area5_8_upper_inner_area = dbh_floor5.Area5_8_UpperInnerArea(window_width, window_height, snake, None)
            area5_9 = dbh_floor5.Area5_9(window_width, window_height, snake, frost_boss_group)
            area5_10 = dbh_floor5.Area5_10(window_width, window_height, snake, frost_boss_group)
            area5_10_girls_bathroom = dbh_floor5.Area5_10_GirlsBathroom(window_width, window_height, snake, None)
            area5_11 = dbh_floor5.Area5_11(window_width, window_height, snake, frost_boss_group)
            area5_12 = dbh_floor5.Area5_12(window_width, window_height, snake, frost_boss_group)
            area5_15_right_inner_area = dbh_floor5.Area5_15_RightInnerArea(window_width, window_height, snake, None)
            area5_13 = dbh_floor5.Area5_13(window_width, window_height, snake, frost_boss_group)
            area5_15_boys_bathroom = dbh_floor5.Area5_15_BoysBathroom(window_width, window_height, snake, None)
            area5_14 = dbh_floor5.Area5_14(window_width, window_height, snake, frost_boss_group)
            area5_15_upper_middle_inner_area = dbh_floor5.Area5_15_UpperMiddleInnerArea(window_width, window_height, snake, None)
            area5_15_lower_right_inner_area = dbh_floor5.Area5_15_LowerRightInnerArea(window_width, window_height, snake, None)
            area5_15 = dbh_floor5.Area5_15(window_width, window_height, snake, frost_boss_group)
            area5_15_lower_inner_area = dbh_floor5.Area5_15_LowerInnerArea(window_width, window_height, snake, None)
            area5_16 = dbh_floor5.Area5_16(window_width, window_height, snake, frost_boss_group)
            area5_16_inner_area = dbh_floor5.Area5_16_InnerArea(window_width, window_height, snake, None)
            area5_17 = dbh_floor5.Area5_17(window_width, window_height, snake, frost_boss_group)
            area5_18 = dbh_floor5.Area5_18(window_width, window_height, snake, frost_boss_group)
            area5_19 = dbh_floor5.Area5_19(window_width, window_height, snake, frost_boss_group)
            area5_19_lower_left_inner_area = dbh_floor5.Area5_19_LowerLeftInnerArea(window_width, window_height, snake, None)
            area5_19_right_inner_area = dbh_floor5.Area5_19_RightInnerArea(window_width, window_height, snake, None)
            
            area_lst = [area1_1, area1_2, area1_3, area1_3_upper_left_inner_area, area1_4, area2_4_upper_right_inner_area, area1_5, area1_5_bathroom_entrances, area1_5_girls_bathroom, area1_6,
                        area1_6_lower_right_inner_area, area1_6_left_inner_area, area1_7, area1_7_upper_inner_area, area1_8, area1_8_boys_bathroom, area1_9, area1_10, area1_11, area1_11_inner_area, area2_1,
                        stairwell2_1_to_3_1, area2_2, area2_3, area2_3_left_inner_area, area2_3_right_inner_area, area2_4, area2_5, area2_5_middle_inner_area, area2_6, area2_6_middle_inner_area, area2_7,
                        area2_7_upper_left_inner_area, area2_8, area2_8_left_inner_area, area2_8_upper_inner_area, area2_9, area2_9_upper_left_inner_area, area2_10, area2_10_girls_bathroom, area2_11, area2_12,
                        area2_12_kay_boss_area, area2_13, area2_13_boys_bathroom, area2_14, area2_14_upper_middle_inner_area, area2_14_lower_right_inner_area, area2_15, area2_15_lower_inner_area, area2_16,
                        area2_16_inner_area, area2_17, area2_18, area2_19, area2_19_lower_left_inner_area, area2_19_right_inner_area, area3_1, stairwell3_1_to_4_1, area3_2, area3_2_lower_inner_area, area3_3,
                        area3_3_left_inner_area, area3_3_right_inner_area, area3_4, area3_5, area3_5_middle_inner_area, area3_6, area3_6_middle_inner_area, area3_6_right_inner_area, area3_7,
                        area3_7_upper_left_inner_area, area3_8, area3_8_left_inner_area, area3_8_thornton_boss_area, area3_9, area3_10, area3_10_girls_bathroom, area3_11, area3_12, area3_13_right_inner_area,
                        area3_13, area3_13_boys_bathroom, area3_14, area3_14_upper_middle_inner_area, area3_14_lower_right_inner_area, area3_15, area3_15_lower_inner_area, area3_16,
                        area3_16_inner_area, area3_17, area3_18, area3_19, area3_19_lower_left_inner_area, area3_19_right_inner_area, area4_1, stairwell4_1_to_5_1, area4_2, area4_3, area4_4_left_inner_area,
                        area4_4_right_inner_area, area4_4, area4_5, area4_5_middle_inner_area, area4_6, area4_6_right_inner_area, area4_6_middle_inner_area, area4_7, area4_7_upper_left_inner_area, area4_8,
                        area4_8_left_inner_area, area4_8_upper_inner_area, area4_9, area4_10, area4_10_girls_bathroom, area4_11, area4_12, area4_14_right_inner_area, area4_13,
                        area4_13_boys_bathroom, area4_14, area4_14_upper_middle_inner_area, area4_14_lower_right_inner_area, area4_15, area4_15_lower_inner_area, area4_16,
                        area4_16_inner_area, area4_17, area4_18, area4_19, area4_19_lower_left_inner_area, area4_19_pattis_boss_area, area5_1, area5_2, area5_3, area5_5_left_inner_area,
                        area5_5_right_inner_area, area5_4, area5_5, area5_5_middle_inner_area, area5_6, area5_6_middle_inner_area, area5_7, area5_7_upper_left_inner_area, area5_8,
                        area5_8_left_inner_area, area5_8_upper_inner_area, area5_9, area5_10, area5_10_girls_bathroom, area5_11, area5_12, area5_15_right_inner_area, area5_13,
                        area5_15_boys_bathroom, area5_14, area5_15_upper_middle_inner_area, area5_15_lower_right_inner_area, area5_15, area5_15_lower_inner_area, area5_16,
                        area5_16_inner_area, area5_17, area5_18, area5_19, area5_19_lower_left_inner_area, area5_19_right_inner_area]


            floor5_areas = area_lst[132:]


            '''Initializing Areas for Enemies'''

            for enemy in e_group1_2:
                enemy.area = area1_2
            for enemy in e_group1_3:
                enemy.area = area1_3
            for enemy in e_group1_4:
                enemy.area = area1_4
            for enemy in e_group1_5:
                enemy.area = area1_5
            for enemy in e_group1_7:
                enemy.area = area1_7
            for enemy in e_group1_8:
                enemy.area = area1_8
            for enemy in e_group1_9:
                enemy.area = area1_9
            for enemy in e_group1_10:
                enemy.area = area1_10


            kay_boss.area = area2_12_kay_boss_area
            thornton_boss.area = area3_8_thornton_boss_area
            boo_companion.area = area3_8_thornton_boss_area
            pattis_boss.area = area4_19_pattis_boss_area
            frost_boss.area = area5_2

            for enemy in e_group2_2:
                enemy.area = area2_2
            for enemy in e_group2_3:
                enemy.area = area2_3
            for enemy in e_group2_4:
                enemy.area = area2_4
            for enemy in e_group2_5:
                enemy.area = area2_5
            for enemy in e_group2_6:
                enemy.area = area2_6
            for enemy in e_group2_7:
                enemy.area = area2_7
            for enemy in e_group2_8:
                enemy.area = area2_8
            for enemy in e_group2_9:
                enemy.area = area2_9
            for enemy in e_group2_12:
                enemy.area = area2_12
            for enemy in e_group2_13:
                enemy.area = area2_13
            for enemy in e_group2_14:
                enemy.area = area2_14
            for enemy in e_group2_15:
                enemy.area = area2_15
            for enemy in e_group2_17:
                enemy.area = area2_17
            for enemy in e_group2_18:
                enemy.area = area2_18
            for enemy in e_group2_19:
                enemy.area = area2_19

            for enemy in e_group3_2:
                enemy.area = area3_2
            for enemy in e_group3_3:
                enemy.area = area3_3
            for enemy in e_group3_4:
                enemy.area = area3_4
            for enemy in e_group3_5:
                enemy.area = area3_5
            for enemy in e_group3_6:
                enemy.area = area3_6
            for enemy in e_group3_7:
                enemy.area = area3_7
            for enemy in e_group3_8:
                enemy.area = area3_8
            for enemy in e_group3_9:
                enemy.area = area3_9
            for enemy in e_group3_10:
                enemy.area = area3_10
            for enemy in e_group3_12:
                enemy.area = area3_12
            for enemy in e_group3_13:
                enemy.area = area3_13
            for enemy in e_group3_14:
                enemy.area = area3_14
            for enemy in e_group3_15:
                enemy.area = area3_15
            for enemy in e_group3_17:
                enemy.area = area3_17
            for enemy in e_group3_18:
                enemy.area = area3_18
            for enemy in e_group3_19:
                enemy.area = area3_19

            for enemy in e_group4_2:
                enemy.area = area4_2
            for enemy in e_group4_3:
                enemy.area = area4_3
            for enemy in e_group4_4:
                enemy.area = area4_4
            for enemy in e_group4_5:
                enemy.area = area4_5
            for enemy in e_group4_6:
                enemy.area = area4_6
            for enemy in e_group4_7:
                enemy.area = area4_7
            for enemy in e_group4_8:
                enemy.area = area4_8
            for enemy in e_group4_9:
                enemy.area = area4_9
            for enemy in e_group4_10:
                enemy.area = area4_10
            for enemy in e_group4_12:
                enemy.area = area4_12
            for enemy in e_group4_13:
                enemy.area = area4_13
            for enemy in e_group4_14:
                enemy.area = area4_14
            for enemy in e_group4_15:
                enemy.area = area4_15

            for enemy in e_group_inner_4_15:
                enemy.area = area4_15_lower_inner_area

            for enemy in e_group4_17:
                enemy.area = area4_17
            for enemy in e_group4_18:
                enemy.area = area4_18
            for enemy in e_group4_19:
                enemy.area = area4_19                                        
            
            area_dict[area1_1] = Neighbors(None, None, None, None, area1_2, None, None, None, None, None, None, None, None, None, None, None, area2_1, None, None, None)
            area_dict[area1_2] = Neighbors(area1_5, None, None, None, area1_3, None, None, None, None, None, None, None, area1_1, None, None, None, None, None, None, None)
            area_dict[area1_3] = Neighbors(None, None, None, None, area1_4, None, None, None, None, None, None, None, area1_2, None, None, None, area1_3_upper_left_inner_area, None, None, None)
            area_dict[area1_3_upper_left_inner_area] = Neighbors(None, None, None, None, None, None, None, None, area1_3, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area1_4] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area1_3, None, None, None, None, None, None, None)
            area_dict[area1_5] = Neighbors(area1_9, None, None, None, area1_5_bathroom_entrances, None, None, None, area1_2, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area1_5_bathroom_entrances] = Neighbors(area1_8, None, None, None, None, None, None, None, None, None, None, None, area1_5, None, None, None, area1_5_girls_bathroom, None, None, None)
            area_dict[area1_5_girls_bathroom] = Neighbors(area1_5_bathroom_entrances, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area1_6] = Neighbors(area1_10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, area1_6_lower_right_inner_area, area1_6_left_inner_area, None, None)
            area_dict[area1_6_lower_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area1_6, None, None, None, None, None, None, None)
            area_dict[area1_6_left_inner_area] = Neighbors(None, None, None, None, area1_6, None, None, None, None, None, None, None, area1_6, None, None, None, None, None, None, None)
            area_dict[area1_7] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area1_8, None, None, None, area1_7_upper_inner_area, None, None, None)
            area_dict[area1_7_upper_inner_area] = Neighbors(None, None, None, None, None, None, None, None, area1_7, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area1_8] = Neighbors(None, None, None, None, area1_7, None, None, None, area1_5_bathroom_entrances, None, None, None, area1_9, None, None, None, area1_8_boys_bathroom, None, None, None)
            area_dict[area1_8_boys_bathroom] = Neighbors(None, None, None, None, None, None, None, None, area1_8, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area1_9] = Neighbors(None, None, None, None, area1_8, None, None, None, area1_5, None, None, None, area1_10, None, None, None, None, None, None, None)
            area_dict[area1_10] = Neighbors(None, None, None, None, area1_9, None, None, None, area1_6, None, None, None, area1_11, None, None, None, None, None, None, None)
            area_dict[area1_11] = Neighbors(None, None, None, None, area1_10, None, None, None, None, None, None, None, None, None, None, None, area1_11_inner_area, None, None, None)
            area_dict[area1_11_inner_area] = Neighbors(None, None, None, None, area1_11, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area2_1] = Neighbors(None, None, None, None, area2_2, None, None, None, None, None, None, None, None, None, None, None, area1_1, stairwell2_1_to_3_1, None, None)
            area_dict[stairwell2_1_to_3_1] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, area2_1, area3_1, None, None)
            area_dict[area2_2] = Neighbors(area2_10, None, None, None, area2_3, None, None, None, None, None, None, None, area2_1, None, None, None, None, None, None, None)
            area_dict[area2_3] = Neighbors(area2_9, None, None, None, None, None, None, None, area2_4, None, None, None, area2_2, None, None, None, area2_3_left_inner_area, area2_3_right_inner_area, None, None)
            area_dict[area2_3_left_inner_area] = Neighbors(area2_3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area2_3_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area2_3, None, None, None, None, None, None, None)
            area_dict[area2_4] = Neighbors(area2_3, None, None, None, None, None, None, None, area2_5, None, None, None, None, None, None, None, area2_4_upper_right_inner_area, None, None, None)
            area_dict[area2_4_upper_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area2_4, None, None, None, None, None, None, None)
            area_dict[area2_5] = Neighbors(area2_4, None, None, None, None, None, None, None, area2_6, None, None, None, None, None, None, None, area2_5_middle_inner_area, None, None, None)
            area_dict[area2_5_middle_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area2_5, None, None, None, None, None, None, None)
            area_dict[area2_6] = Neighbors(area2_5, None, None, None, None, None, None, None, None, None, None, None, area2_7, None, None, None, area2_6_middle_inner_area, None, None, None)
            area_dict[area2_6_middle_inner_area] = Neighbors(area2_6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area2_7] = Neighbors(None, None, None, None, area2_6, None, None, None, None, None, None, None, area2_8, None, None, None, area2_7_upper_left_inner_area, None, None, None)
            area_dict[area2_7_upper_left_inner_area] = Neighbors(None, None, None, None, None, None, None, None, area2_7, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area2_8] = Neighbors(None, None, None, None, area2_7, None, None, None, None, None, None, None, None, None, None, None, area2_8_left_inner_area, area2_8_upper_inner_area, None, None)
            area_dict[area2_8_left_inner_area] = Neighbors(None, None, None, None, area2_8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area2_8_upper_inner_area] = Neighbors(None, None, None, None, None, None, None, None, area2_8, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area2_9] = Neighbors(area2_12, None, None, None, None, None, None, None, area2_3, None, None, None, None, None, None, None, area2_9_upper_left_inner_area, None, None, None)
            area_dict[area2_9_upper_left_inner_area] = Neighbors(None, None, None, None, area2_9, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)          
            area_dict[area2_10] = Neighbors(area2_13, None, None, None, None, None, None, None, area2_2, None, None, None, area2_11, None, None, None, area2_10_girls_bathroom, None, None, None)
            area_dict[area2_10_girls_bathroom] = Neighbors(area2_10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area2_11] = Neighbors(None, None, None, None, area2_10, None, None, None, None, None, None, None, None, None, None, None, area1_5, area1_5, None, None)
            area_dict[area2_12] = Neighbors(None, None, None, None, None, None, None, None, area2_9, None, None, None, area2_13, None, None, None, area2_12_kay_boss_area, None, None, None)
            area_dict[area2_12_kay_boss_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area2_12, None, None, None, None, None, None, None)
            area_dict[area2_13] = Neighbors(None, None, None, None, area2_12, None, None, None, area2_10, None, None, None, area2_14, None, None, None, area2_13_boys_bathroom, None, None, None)
            area_dict[area2_13_boys_bathroom] = Neighbors(None, None, None, None, None, None, None, None, area2_13, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area2_14] = Neighbors(None, None, None, None, area2_13, None, None, None, None, None, None, None, area2_15, None, None, None, area2_14_upper_middle_inner_area, area2_14_lower_right_inner_area, None, None)
            area_dict[area2_14_upper_middle_inner_area] = Neighbors(None, None, None, None, None, None, None, None, area2_14, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area2_14_lower_right_inner_area] = Neighbors(area2_14, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area2_15] = Neighbors(None, None, None, None, area2_14, None, None, None, area2_16, None, None, None, area2_17, None, None, None, area2_15_lower_inner_area, None, None, None)
            area_dict[area2_15_lower_inner_area] = Neighbors(area2_15, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area2_16] = Neighbors(area2_15, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, area2_16_inner_area, None, None, None)
            area_dict[area2_16_inner_area] = Neighbors(area2_16, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area2_17] = Neighbors(None, None, None, None, area2_15, None, None, None, None, None, None, None, area2_18, None, None, None, None, None, None, None)
            area_dict[area2_18] = Neighbors(None, None, None, None, area2_17, None, None, None, area2_19, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area2_19] = Neighbors(area2_18, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, area2_19_lower_left_inner_area, area2_19_right_inner_area, None, None)
            area_dict[area2_19_lower_left_inner_area] = Neighbors(None, None, None, None, area2_19, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area2_19_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area2_19, None, None, None, None, None, None, None)
            area_dict[area3_1] = Neighbors(None, None, None, None, area3_2, None, None, None, None, None, None, None, None, None, None, None, stairwell2_1_to_3_1, stairwell3_1_to_4_1, None, None)
            area_dict[stairwell3_1_to_4_1] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, area3_1, area4_1, None, None)
            area_dict[area3_2] = Neighbors(area3_10, None, None, None, area3_3, None, None, None, area3_2_lower_inner_area, None, None, None, area3_1, None, None, None, None, None, None, None)
            area_dict[area3_2_lower_inner_area] = Neighbors(area3_2, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area3_3] = Neighbors(area3_9, None, None, None, None, None, None, None, area3_4, None, None, None, area3_2, None, None, None, area3_3_left_inner_area, area3_3_right_inner_area, None, None)
            area_dict[area3_3_left_inner_area] = Neighbors(area3_3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area3_3_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area3_3, None, None, None, None, None, None, None)
            area_dict[area3_4] = Neighbors(area3_3, None, None, None, None, None, None, None, area3_5, None, None, None, None, None, None, None, area3_4_upper_right_inner_area, None, None, None)
            area_dict[area3_4_upper_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area3_4, None, None, None, None, None, None, None)
            area_dict[area3_5] = Neighbors(area3_4, None, None, None, None, None, None, None, area3_6, None, None, None, None, None, None, None, area3_5_middle_inner_area, None, None, None)
            area_dict[area3_5_middle_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area3_5, None, None, None, None, None, None, None)
            area_dict[area3_6] = Neighbors(area3_5, None, None, None, None, None, None, None, None, None, None, None, area3_7, None, None, None, area3_6_middle_inner_area, area3_6_right_inner_area, None, None)
            area_dict[area3_6_middle_inner_area] = Neighbors(area3_6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area3_6_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area3_6, None, None, None, None, None, None, None)
            area_dict[area3_7] = Neighbors(None, None, None, None, area3_6, None, None, None, None, None, None, None, area3_8, None, None, None, area3_7_upper_left_inner_area, None, None, None)
            area_dict[area3_7_upper_left_inner_area] = Neighbors(None, None, None, None, None, None, None, None, area3_7, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area3_8] = Neighbors(None, None, None, None, area3_7, None, None, None, None, None, None, None, None, None, None, None, area3_8_left_inner_area, area3_8_thornton_boss_area, None, None)
            area_dict[area3_8_left_inner_area] = Neighbors(None, None, None, None, area3_8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area3_8_thornton_boss_area] = Neighbors(None, None, None, None, None, None, None, None, area3_8, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area3_9] = Neighbors(area3_12, None, None, None, None, None, None, None, area3_3, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area3_10] = Neighbors(area3_13, None, None, None, None, None, None, None, area3_2, None, None, None, area3_11, None, None, None, area3_10_girls_bathroom, None, None, None)
            area_dict[area3_10_girls_bathroom] = Neighbors(area3_10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area3_11] = Neighbors(None, None, None, None, area3_10, None, None, None, None, None, None, None, None, None, None, None, area1_5, area1_5, None, None)
            area_dict[area3_12] = Neighbors(None, None, None, None, None, None, None, None, area3_9, None, None, None, area3_13, None, None, None, area3_13_right_inner_area, None, None, None)
            area_dict[area3_13_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area3_12, None, None, None, None, None, None, None)
            area_dict[area3_13] = Neighbors(None, None, None, None, area3_12, None, None, None, area3_10, None, None, None, area3_14, None, None, None, area3_13_boys_bathroom, None, None, None)
            area_dict[area3_13_boys_bathroom] = Neighbors(None, None, None, None, None, None, None, None, area3_13, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area3_14] = Neighbors(None, None, None, None, area3_13, None, None, None, None, None, None, None, area3_15, None, None, None, area3_14_upper_middle_inner_area, area3_14_lower_right_inner_area, None, None)
            area_dict[area3_14_upper_middle_inner_area] = Neighbors(None, None, None, None, None, None, None, None, area3_14, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area3_14_lower_right_inner_area] = Neighbors(area3_14, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area3_15] = Neighbors(None, None, None, None, area3_14, None, None, None, area3_16, None, None, None, area3_17, None, None, None, area3_15_lower_inner_area, None, None, None)
            area_dict[area3_15_lower_inner_area] = Neighbors(area3_15, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area3_16] = Neighbors(area3_15, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, area3_16_inner_area, None, None, None)
            area_dict[area3_16_inner_area] = Neighbors(area3_16, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area3_17] = Neighbors(None, None, None, None, area3_15, None, None, None, None, None, None, None, area3_18, None, None, None, None, None, None, None)
            area_dict[area3_18] = Neighbors(None, None, None, None, area3_17, None, None, None, area3_19, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area3_19] = Neighbors(area3_18, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, area3_19_lower_left_inner_area, area3_19_right_inner_area, None, None)
            area_dict[area3_19_lower_left_inner_area] = Neighbors(None, None, None, None, area3_19, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area3_19_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area3_19, None, None, None, None, None, None, None)
            area_dict[area4_1] = Neighbors(None, None, None, None, area4_2, None, None, None, None, None, None, None, None, None, None, None, stairwell3_1_to_4_1, stairwell4_1_to_5_1, None, None)
            area_dict[stairwell4_1_to_5_1] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, area4_1, area5_1, None, None)
            area_dict[area4_2] = Neighbors(area4_10, None, None, None, area4_3, None, None, None, None, None, None, None, area4_1, None, None, None, None, None, None, None)
            area_dict[area4_3] = Neighbors(area4_9, None, None, None, None, None, None, None, area4_4, None, None, None, area4_2, None, None, None, area4_4_left_inner_area, area4_4_right_inner_area, None, None)
            area_dict[area4_4_left_inner_area] = Neighbors(area4_3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area4_4_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area4_3, None, None, None, None, None, None, None)
            area_dict[area4_4] = Neighbors(area4_3, None, None, None, None, None, None, None, area4_5, None, None, None, None, None, None, None, area4_4_upper_right_inner_area, None, None, None)
            area_dict[area4_4_upper_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area4_4, None, None, None, None, None, None, None)
            area_dict[area4_5] = Neighbors(area4_4, None, None, None, None, None, None, None, area4_6, None, None, None, None, None, None, None, area4_5_middle_inner_area, None, None, None)
            area_dict[area4_5_middle_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area4_5, None, None, None, None, None, None, None)
            area_dict[area4_6] = Neighbors(area4_5, None, None, None, None, None, None, None, None, None, None, None, area4_7, None, None, None, area4_6_right_inner_area, None, None, None)
            area_dict[area4_6_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area4_6, None, None, None, None, None, None, None)
            area_dict[area4_6_middle_inner_area] = Neighbors(area4_6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area4_7] = Neighbors(None, None, None, None, area4_6, None, None, None, None, None, None, None, area4_8, None, None, None, area4_7_upper_left_inner_area, None, None, None)
            area_dict[area4_7_upper_left_inner_area] = Neighbors(None, None, None, None, None, None, None, None, area4_7, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area4_8] = Neighbors(None, None, None, None, area4_7, None, None, None, None, None, None, None, None, None, None, None, area4_8_left_inner_area, area4_8_upper_inner_area, None, None)
            area_dict[area4_8_left_inner_area] = Neighbors(None, None, None, None, area4_8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area4_8_upper_inner_area] = Neighbors(None, None, None, None, None, None, None, None, area4_8, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area4_9] = Neighbors(area4_12, None, None, None, None, None, None, None, area4_3, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area4_10] = Neighbors(area4_13, None, None, None, None, None, None, None, area4_2, None, None, None, area4_11, None, None, None, area4_10_girls_bathroom, None, None, None)
            area_dict[area4_10_girls_bathroom] = Neighbors(area4_10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area4_11] = Neighbors(None, None, None, None, area4_10, None, None, None, None, None, None, None, None, None, None, None, area1_5, area1_5, None, None)
            area_dict[area4_12] = Neighbors(None, None, None, None, None, None, None, None, area4_9, None, None, None, area4_13, None, None, None, area4_14_right_inner_area, None, None, None)
            area_dict[area4_14_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area4_12, None, None, None, None, None, None, None)
            area_dict[area4_13] = Neighbors(None, None, None, None, area4_12, None, None, None, area4_10, None, None, None, area4_14, None, None, None, area4_13_boys_bathroom, None, None, None)
            area_dict[area4_13_boys_bathroom] = Neighbors(None, None, None, None, None, None, None, None, area4_13, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area4_14] = Neighbors(None, None, None, None, area4_13, None, None, None, None, None, None, None, area4_15, None, None, None, area4_14_upper_middle_inner_area, area4_14_lower_right_inner_area, None, None)
            area_dict[area4_14_upper_middle_inner_area] = Neighbors(None, None, None, None, None, None, None, None, area4_14, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area4_14_lower_right_inner_area] = Neighbors(area4_14, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area4_15] = Neighbors(None, None, None, None, area4_14, None, None, None, area4_16, None, None, None, area4_17, None, None, None, area4_15_lower_inner_area, None, None, None)
            area_dict[area4_15_lower_inner_area] = Neighbors(area4_15, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area4_16] = Neighbors(area4_15, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, area4_16_inner_area, None, None, None)
            area_dict[area4_16_inner_area] = Neighbors(area4_16, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area4_17] = Neighbors(None, None, None, None, area4_15, None, None, None, None, None, None, None, area4_18, None, None, None, None, None, None, None)
            area_dict[area4_18] = Neighbors(None, None, None, None, area4_17, None, None, None, area4_19, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area4_19] = Neighbors(area4_18, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, area4_19_lower_left_inner_area, area4_19_pattis_boss_area, None, None)
            area_dict[area4_19_lower_left_inner_area] = Neighbors(None, None, None, None, area4_19, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area4_19_pattis_boss_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area4_19, None, None, None, None, None, None, None)
            area_dict[area5_1] = Neighbors(None, None, None, None, area5_2, None, None, None, None, None, None, None, None, None, None, None, stairwell4_1_to_5_1, None, None, None)
            area_dict[area5_2] = Neighbors(area5_10, None, None, None, area5_3, None, None, None, None, None, None, None, area5_1, None, None, None, None, None, None, None)
            area_dict[area5_3] = Neighbors(area5_9, None, None, None, None, None, None, None, area5_4, None, None, None, area5_2, None, None, None, area5_5_left_inner_area, area5_5_right_inner_area, None, None)
            area_dict[area5_5_left_inner_area] = Neighbors(area5_3, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area5_5_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area5_3, None, None, None, None, None, None, None)
            area_dict[area5_4] = Neighbors(area5_3, None, None, None, None, None, None, None, area5_5, None, None, None, None, None, None, None, area5_5_upper_right_inner_area, None, None, None)
            area_dict[area5_5_upper_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area5_4, None, None, None, None, None, None, None)
            area_dict[area5_5] = Neighbors(area5_4, None, None, None, None, None, None, None, area5_6, None, None, None, None, None, None, None, area5_5_middle_inner_area, None, None, None)
            area_dict[area5_5_middle_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area5_5, None, None, None, None, None, None, None)
            area_dict[area5_6] = Neighbors(area5_5, None, None, None, None, None, None, None, None, None, None, None, area5_7, None, None, None, area5_6_middle_inner_area, None, None, None)
            area_dict[area5_6_middle_inner_area] = Neighbors(area5_6, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area5_7] = Neighbors(None, None, None, None, area5_6, None, None, None, None, None, None, None, area5_8, None, None, None, area5_7_upper_left_inner_area, None, None, None)
            area_dict[area5_7_upper_left_inner_area] = Neighbors(None, None, None, None, None, None, None, None, area5_7, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area5_8] = Neighbors(None, None, None, None, area5_7, None, None, None, None, None, None, None, None, None, None, None, area5_8_left_inner_area, area5_8_upper_inner_area, None, None)
            area_dict[area5_8_left_inner_area] = Neighbors(None, None, None, None, area5_8, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area5_8_upper_inner_area] = Neighbors(None, None, None, None, None, None, None, None, area5_8, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area5_9] = Neighbors(area5_12, None, None, None, None, None, None, None, area5_3, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area5_10] = Neighbors(area5_13, None, None, None, None, None, None, None, area5_2, None, None, None, area5_11, None, None, None, area5_10_girls_bathroom, None, None, None)
            area_dict[area5_10_girls_bathroom] = Neighbors(area5_10, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area5_11] = Neighbors(None, None, None, None, area5_10, None, None, None, None, None, None, None, None, None, None, None, area1_5, area1_5, None, None)
            area_dict[area5_12] = Neighbors(None, None, None, None, None, None, None, None, area5_9, None, None, None, area5_13, None, None, None, area5_15_right_inner_area, None, None, None)
            area_dict[area5_15_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area5_12, None, None, None, None, None, None, None)
            area_dict[area5_13] = Neighbors(None, None, None, None, area5_12, None, None, None, area5_10, None, None, None, area5_14, None, None, None, area5_15_boys_bathroom, None, None, None)
            area_dict[area5_15_boys_bathroom] = Neighbors(None, None, None, None, None, None, None, None, area5_13, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area5_14] = Neighbors(None, None, None, None, area5_13, None, None, None, None, None, None, None, area5_15, None, None, None, area5_15_upper_middle_inner_area, area5_15_lower_right_inner_area, None, None)
            area_dict[area5_15_upper_middle_inner_area] = Neighbors(None, None, None, None, None, None, None, None, area5_14, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area5_15_lower_right_inner_area] = Neighbors(area5_14, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area5_15] = Neighbors(None, None, None, None, area5_14, None, None, None, area5_16, None, None, None, area5_17, None, None, None, area5_15_lower_inner_area, None, None, None)
            area_dict[area5_15_lower_inner_area] = Neighbors(area5_15, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area5_16] = Neighbors(area5_15, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, area5_16_inner_area, None, None, None)
            area_dict[area5_16_inner_area] = Neighbors(area5_16, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area5_17] = Neighbors(None, None, None, None, area5_15, None, None, None, None, None, None, None, area5_18, None, None, None, None, None, None, None)
            area_dict[area5_18] = Neighbors(None, None, None, None, area5_17, None, None, None, area5_19, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area5_19] = Neighbors(area5_18, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, area5_19_lower_left_inner_area, area5_19_right_inner_area, None, None)
            area_dict[area5_19_lower_left_inner_area] = Neighbors(None, None, None, None, area5_19, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)
            area_dict[area5_19_right_inner_area] = Neighbors(None, None, None, None, None, None, None, None, None, None, None, None, area5_19, None, None, None, None, None, None, None)
             
            current_area = area1_1 #cheat_lvl
            print("in 1_1")
            snake.area = current_area

            #---HUD Initializaton---
            hud = HUD(window_width, window_height*0.12, snake)


            #---Inventory Screen Initialization---
            on_weapon_select_screen = False
            on_item_select_screen = False
            inventory_cursor = continue_screen_cursor = title_screen_cursor = ">"
            weapon_cursor_pos = [window_width*0.08, window_height*0.15]
            item_cursor_pos = [window_width*0.08, window_height*0.15]
            continue_cursor_pos = [window_width*0.42, window_height*0.40]
            weapons_index = 0
            items_index = 0


            #---Text Initialization
            font = pygame.font.SysFont("Arial", 30)
            title_font = pygame.font.SysFont("Arial", 100, True)
            score_title_font = pygame.font.SysFont("Arial", 30, True)
            score_font = pygame.font.SysFont("Arial", 30, True)


            #---Continue Screen Initializaion---
            on_continue = True


            #---Game Exiting Initializaion---
            exiting_game = False


            #---Time Initializaion---
            time1, time2 = 0, 0
            time_recorded = False


            #---Score Initialization---
            time_score = merc_alerts_score = merc_stuns_score =\
            mgs_games_score = continues_score = noodles_consumed_score = 0


            #---Title Screen Initializaion---
            #on_start_game = True #Not here or it would be initialized to True constantly
            game_data_loaded = True

        #----FOR MUSIC----
        current_song = _load_and_play_song(current_song, "all_along_the_watchtower")
        #----^FOR MUSIC----
        
        events = pygame.event.get()
        for event in events:
            if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                event.key == pygame.K_ESCAPE)):
                game_on = False
            if not game_running:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN and on_start_game and not allow_scroll:
                        cursor_move = pygame.mixer.Sound("cursor_move.wav")
                        pygame.mixer.Sound.play(cursor_move)
                        title_screen_cursor_pos[1] += window_height*0.05
                        on_start_game = False
                    elif event.key == pygame.K_UP and not on_start_game and not allow_scroll:
                        cursor_move = pygame.mixer.Sound("cursor_move.wav")
                        pygame.mixer.Sound.play(cursor_move)
                        title_screen_cursor_pos[1] -= window_height*0.05
                        on_start_game = True
                    elif event.key == pygame.K_a and on_start_game and not allow_scroll:
                        cursor_select = pygame.mixer.Sound("cursor_select.wav")
                        pygame.mixer.Sound.play(cursor_select)
                        game_running = True
                        time1 = time.time()
                    ## FOR HIGH SCORES ##
                    elif event.key == pygame.K_a and not on_start_game and not allow_scroll:
                        cursor_select = pygame.mixer.Sound("cursor_select.wav")
                        pygame.mixer.Sound.play(cursor_select)
                        showing_play_record = True
                    elif event.key == pygame.K_SPACE and on_start_game:
                        allow_scroll = False

        if not game_running and not showing_play_record:
            if allow_scroll and cur_ticks < till_stop:
                window.fill(BLUE)
                title = title_font.render("DONALD BREN SOLID", True, YELLOW, BLUE)
                window.blit(title, (window_width*0.13, (window_height+50)*start_height)) #manipulate window_height to adjust starting pos
                start_height -= 0.00163 #Tweak this value to make the title scroll slower!
                cur_ticks += 1
            else:
                allow_scroll = False

            if not allow_scroll:
                window.fill(BLUE)
                title = title_font.render("DONALD BREN SOLID", True, YELLOW, BLUE)
                sub_title = font.render("T a c t i c a l   A n t e a t e r   A c t i o n", True, YELLOW, BLUE)
                start_game = font.render("Start Game", True, YELLOW, BLUE)
                play_record = font.render("Play Record", True, YELLOW, BLUE)
                cursor = font.render(title_screen_cursor, True, YELLOW, BLUE)
                window.blit(title, (window_width*0.13, window_height*0.37))
                #window.blit(sub_title, (window_width*0.34, window_height*0.45))
###JEREMY
                #I only needed to move the "Tactical Anteater Action" down
                #window_height*0.37 is the y-coordinate of the top left corner of "Donald Bren Solid"
                #100 is the height of "Donald Bren Solid"
                #10 is an arbitrary number of pixels below "Donal Bren Solid"
                #adding those 3 things together gives the y-coordinate of "Tactical Anteater Action"
                window.blit(sub_title, (window_width*0.34, window_height*0.37+100+10))
###END JEREMY
                window.blit(start_game, (window_width*0.44, window_height*0.60))
                window.blit(play_record, (window_width*0.44, window_height*0.65))
                window.blit(cursor, title_screen_cursor_pos)

        pygame.display.update()

        ## FOR HIGH SCORES ##
        while showing_play_record:
            window.fill(BLUE)
            events = pygame.event.get()
            for event in events:
                #print(event)
                if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                    event.key == pygame.K_ESCAPE)):
                        showing_play_record = False
                        
            infile = open("best_playthrough.txt")
            content = infile.readlines()
            infile.close()
            
            header = score_title_font.render(content[0][:-1], True, YELLOW, BLUE)
            completion_time = score_font.render(content[2][:-1], True, YELLOW, BLUE)
            completion_time_value = font.render(content[3][:-1], True, YELLOW, BLUE)
            merc_alerts = score_font.render(content[4][:-1], True, YELLOW, BLUE)
            merc_alerts_value = font.render(content[5][:-1], True, YELLOW, BLUE)
            merc_stuns = score_font.render(content[6][:-1], True, YELLOW, BLUE)
            merc_stuns_value = font.render(content[7][:-1], True, YELLOW, BLUE)
            mgs_games = score_font.render(content[8][:-1], True, YELLOW, BLUE)
            mgs_games_value = font.render(content[9][:-1], True, YELLOW, BLUE)
            continues = score_font.render(content[10][:-1], True, YELLOW, BLUE)
            continues_value = font.render(content[11][:-1], True, YELLOW, BLUE)
            noodles_consumed = score_font.render(content[12][:-1], True, YELLOW, BLUE)
            noodles_consumed_value = font.render(content[13][:-1], True, YELLOW, BLUE)
            score = score_font.render(content[15][:-1], True, YELLOW, BLUE)
            score_value = font.render(content[16][:-1], True, YELLOW, BLUE)

            window.blit(header, (window_width*0.37, window_height*0.08))
##            window.blit(completion_time, (window_width*0.20, window_height*0.15))
##            window.blit(completion_time_value, (window_width*0.20, window_height*0.18))
##            window.blit(merc_alerts, (window_width*0.20, window_height*0.23))
##            window.blit(merc_alerts_value, (window_width*0.20, window_height*0.26))
##            window.blit(merc_stuns, (window_width*0.20, window_height*0.31))
##            window.blit(merc_stuns_value, (window_width*0.20, window_height*0.34))
##            window.blit(mgs_games, (window_width*0.20, window_height*0.39))
##            window.blit(mgs_games_value, (window_width*0.20, window_height*0.42))
##            window.blit(continues, (window_width*0.20, window_height*0.47))
##            window.blit(continues_value, (window_width*0.20, window_height*0.50))
##            window.blit(noodles_consumed, (window_width*0.20, window_height*0.55))
##            window.blit(noodles_consumed_value, (window_width*0.20, window_height*0.58))    
##            window.blit(score, (window_width*0.20, window_height*0.63))
##            window.blit(score_value, (window_width*0.20, window_height*0.66))

###JEREMY
            #I create this list called lines so i can use it for a for-loop.
            lines = [completion_time, completion_time_value, merc_alerts, merc_alerts_value,
                     merc_stuns, merc_stuns_value, mgs_games, mgs_games_value, continues,
                     continues_value, noodles_consumed, noodles_consumed_value, score, score_value]
            #current_height is like a running tally: it is used, then incremented
            current_height = window_height*0.15
            for line in lines:
                #the x-coordinate of the top left corner will be the same for each line since
                #the lines should be lined up nicely
                window.blit(line, (window_width*0.20, current_height))
                #must increment current_height so it can be the correct value for the next line
                #30 is the height of each line while 10 is an arbitrary number of pixels below
                #each line: sum those two numbers and you have the correct spot for the next line
                current_height += 30 + 10
###END JEREMY


            pygame.display.update()

        
        while game_running:
            #----FOR MUSIC----
            if current_song == "all_along_the_watchtower": #Don't ever play title screen music in-game
                pygame.mixer.music.stop()
            #----FOR MUSIC----
                
            events = pygame.event.get()
            for event in events:
                #QUIT is the only event that this loop looks for...
                if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                    event.key == pygame.K_ESCAPE) and not snake.reached_end_of_game):
                    game_running = False
                    #pygame.mixer.music.play(1)
                    pygame.mixer.music.stop()
                    game_data_loaded = False
                elif (event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_w and not on_weapon_select_screen and not on_item_select_screen and not snake.is_subdued:
                        snake.is_moving = False
                        snake.change_move(0, 0)
                        on_weapon_select_screen = True
                    elif event.key == pygame.K_q and not on_item_select_screen and not on_weapon_select_screen and not snake.is_subdued:
                        snake.is_moving = False
                        snake.change_move(0, 0)
                        on_item_select_screen = True
                    elif on_weapon_select_screen:
                        weapons_index, weapon_cursor_pos, on_weapon_select_screen = _navigate_weapon_select_screen(event, weapons_index, weapon_cursor_pos,
                                                                                                            on_weapon_select_screen, snake) 
                    elif on_item_select_screen:
                        items_index, item_cursor_pos, on_item_select_screen = _navigate_item_select_screen(event, items_index, item_cursor_pos,
                                                                                                            on_item_select_screen, snake)
                    elif snake.is_subdued and snake.lives > 1: #Then must be on continue screen
                        if event.key == pygame.K_DOWN and on_continue:
                            cursor_move = pygame.mixer.Sound("cursor_move.wav")
                            pygame.mixer.Sound.play(cursor_move)
                            continue_cursor_pos[1] += window_height*0.05
                            on_continue = False
                        elif event.key == pygame.K_UP and not on_continue:
                            cursor_move = pygame.mixer.Sound("cursor_move.wav")
                            pygame.mixer.Sound.play(cursor_move)
                            continue_cursor_pos[1] -= window_height*0.05
                            on_continue = True
                        elif event.key == pygame.K_a and on_continue:
                            cursor_select = pygame.mixer.Sound("cursor_select.wav")
                            pygame.mixer.Sound.play(cursor_select)
                            snake.continues += 1 #FOR HIGH SCORES
                            snake.is_subdued = False
                            snake.health = 100
                            snake.lives -= 1
                            snake.is_moving = False
                            snake.change_move(0, 0)
                            if snake.reached_checkpoint:
                                current_area = area3_1
                            else:
                                current_area = area1_1
                            snake.area = current_area
                            snake.init_position(window_width*0.65, window_height*0.55)
                            current_area.subside_all_alerts(area_lst)
                            current_area.clean_up_attack_objects_after_continue(area_lst)
                            frost_boss.area = area5_2 #for Frost battle. Original starting position
                            frost_boss.health = frost.FROST_START_HEALTH #for Frost battle
                            #Perhaps need re-initialize his starting position also?
                            frost_boss.init_position(window_width/2, window_height/2)
                            if not kay_boss.is_subdued:
                                #kay_boss.health = kay.KAY_START_HEALTH
                                kay_boss.init_position(window_width/2, window_height/2)
                            if not thornton_boss.is_subdued:
                                #thornton_boss.health = thornton.THORNTON_START_HEALTH
                                thornton_boss.init_position(window_width/2, window_height/2)
                            if not pattis_boss.is_subdued:
                                #pattis_boss.health = pattis.PATTIS_START_HEALTH
                                pattis_boss.init_position(window_width/2, window_height/2)
                        elif event.key == pygame.K_a and not on_continue:
                            cursor_select = pygame.mixer.Sound("cursor_select.wav")
                            pygame.mixer.Sound.play(cursor_select)
                            game_running = False
                            game_data_loaded = False
                            pygame.mixer.music.stop()
                    elif snake.is_subdued and snake.lives == 1: #on the game over screen
                        if event.key == pygame.K_SPACE:
                            game_running = False
                            game_data_loaded = False
                            pygame.mixer.music.stop()
                    ## END GAME STUFF ##
                    elif snake.reached_end_of_game and not display_game_results:
                        if event.key == pygame.K_SPACE:
                            display_game_results = True
                    elif snake.reached_end_of_game and display_game_results:
                        if event.key == pygame.K_SPACE:
                            #I would calculate and save game results to a file here (if the new score is better than the old score)
                            infile = open("best_playthrough.txt")
                            content = infile.readlines()
                            infile.close()
                            
                            if content[-1][:-1] != "--":
                                if snake.score > int(content[-1][:-1]):
                                    _write_score_to_file(time_score, merc_alerts_score, merc_stuns_score,
                                                         mgs_games_score, continues_score, noodles_consumed_score)
                            else:
                                _write_score_to_file(time_score, merc_alerts_score, merc_stuns_score,
                                                     mgs_games_score, continues_score, noodles_consumed_score)

                            display_game_results = False
                            exiting_game = True #So you don't go into any of those if statements below                           
                            game_running = False
                            game_data_loaded = False
                            pygame.mixer.music.stop()
        
                                
            if not on_weapon_select_screen and not on_item_select_screen and not snake.is_subdued and not snake.reached_end_of_game and not exiting_game:
                #-----Update Functions-----
                snake.update(event, current_area.obj_group, current_area.e_group)
                event = None
                current_area.update_objects()
                current_area.update_enemies()
                current_area.update_e_attack_objects()
                current_area.update_s_attack_objects()
                hud.update(snake) #Should be last thing that is updated to register attacks


                #-----Logic Testing-----
                current_area = current_area.check_transition(area_dict)
                if not snake.reached_end_of_game:
                    snake.area = current_area
                    current_area.if_alert_then_propagate(area_lst)
                    current_area.if_safe_haven_subside_alerts(area_lst)


                    #-----Draw (blit) Everything-----
                    current_area.draw(window)
                    s_group.draw(window)
                    current_area.draw_enemies(window)
                    current_area.draw_e_attack_objects(window)
                    current_area.draw_s_attack_objects(window)
                    window.blit(hud, (0, window_height*0.90))
                    hud.draw()
                    #a2_3_camera1.TEST_draw_block() #FOR TESTING so you can see the LOS


                    #-----Update Screen-----
                    pygame.display.update()


                    #-----Delay Framerate (or iteration of game loop)-----
                    clock.tick(fps)
                #----FOR MUSIC----
                #Note that the music stream can only play one song at a time, so calling music.play() while a song is already playing
                #will cause the currently playing song to be replaced by the newly played song.
                if snake.is_subdued and snake.lives == 1:
                    current_song = _load_and_play_song(current_song, "comfortably_numb_solo")
                elif snake.is_subdued and snake.lives > 1:
                    current_song = _load_and_play_song(current_song, "continue")
                elif snake.reached_end_of_game:
                    current_song = _load_and_play_song(current_song, "snake_eater")
                elif current_area == area2_12_kay_boss_area: #will possibly add "and kay.is_not_subdued to stop boss music
                    current_song = _load_and_play_song(current_song, "separate_ways")
                elif current_area == area3_8_thornton_boss_area: #will possibly add "and thornton.is_not_subdued
                    current_song = _load_and_play_song(current_song, "knight_rider_theme")
                elif current_area == area4_19_pattis_boss_area: #will possibly add "and pattis.is_not_subdued
                    current_song = _load_and_play_song(current_song, "immigrant_song")
                elif current_area in floor5_areas:  #How to get music for particular areas
                    current_song = _load_and_play_song(current_song, "ballroom_blitz")
                elif current_area.in_alert_phase:
                    current_song = _load_and_play_song(current_song, "alert")
                else:
                    current_song = _load_and_play_song(current_song, "theme_of_tara")
                #----^FOR MUSIC----
            elif on_weapon_select_screen and not snake.reached_end_of_game and not exiting_game:
                _draw_weapon_select_screen(window, snake)
            elif on_item_select_screen and not snake.reached_end_of_game and not exiting_game:
                _draw_item_select_screen(window, snake)
            elif snake.is_subdued and snake.lives > 1 and not snake.reached_end_of_game and not exiting_game:
                window.fill(BLACK)

                subdued_msg = font.render("YOU HAVE BEEN SUBDUED", True, WHITE, BLACK)
                select_continue = font.render("Continue", True, WHITE, BLACK)
                select_quit = font.render("Quit", True, WHITE, BLACK)
                rendered_cursor = font.render(continue_screen_cursor, True, WHITE, BLACK)

                window.blit(subdued_msg, (window_width*0.35, window_height*0.35))
                window.blit(select_continue, (window_width*0.44, window_height*0.40))
                window.blit(select_quit, (window_width*0.44, window_height*0.45))
                window.blit(rendered_cursor, continue_cursor_pos)
            elif snake.is_subdued and snake.lives == 1 and not snake.reached_end_of_game and not exiting_game:
                window.fill(BLACK)
                game_over_msg = font.render("GAME OVER", True, WHITE, BLACK)
                window.blit(game_over_msg, (window_width*0.43, window_height*0.45))
            elif snake.reached_end_of_game and not display_game_results and not exiting_game:
                window.fill(BLACK)
                if not time_recorded:
                    time2 = time.time()
                    snake.time = int(time2 - time1) #Just make the time elapsed a whole number for easier management
                    time_recorded = True
                game_over_msg = font.render("CONGRATULATIONS! You helped Snake graduate!", True, WHITE, BLACK)
                window.blit(game_over_msg, (window_width*0.28, window_height*0.45))
            elif snake.reached_end_of_game and display_game_results and not exiting_game: #last two booleans not needed but there for extra clarity
                ## CALCULATE SCORE AND DISPLAY RESULTS
                window.fill(BLACK)
                
                mission_results = font.render("MISSION RESULTS", True, WHITE, BLACK)
                
                completion_time = score_font.render("Time:", True, WHITE, BLACK)
                time_min = snake.time//60
                time_min_str = "0" + str(time_min) if len(str(time_min)) == 1 else str(time_min)
                time_sec = snake.time%60
                time_sec_str = "0" + str(time_sec) if len(str(time_sec)) == 1 else str(time_sec)
                if snake.time < 600: #time is less than 10 minutes
                    time_score = T_SCORE_VAL1 #VALUE TO ADD
                elif 600 <= snake.time <= 1200: #time is between 10 and 20 minutes
                    time_score = T_SCORE_VAL2 #VALUE TO ADD
                else:
                    time_score = T_SCORE_VAL3  #VALUE TO ADD
                completion_time_value = font.render("{}:{}".format(time_min_str, time_sec_str) + "  (+{})".format(time_score), True, WHITE, BLACK)
                
                merc_alerts = score_font.render("Mercenary Alerts:", True, WHITE, BLACK)
                merc_alerts_score = -snake.merc_alerts*MERC_ALERT_SCORE_DECREMENT #VALUE TO ADD
                if merc_alerts_score == 0:
                    merc_alerts_score = MERC_ALERT_SCORE_VAL #VALUE TO ADD
                merc_alerts_score_sign = "+" if merc_alerts_score > 0 else ""
                merc_alerts_value = font.render(str(snake.merc_alerts) + "  ({}{})".format(merc_alerts_score_sign, merc_alerts_score), True, WHITE, BLACK)

                
                merc_stuns = score_font.render("Mercenary Stuns:", True, WHITE, BLACK)
                merc_stuns_score = -snake.merc_stuns*MERC_STUN_SCORE_DECREMENT #VALUE TO ADD
                if merc_stuns_score == 0:
                    merc_stuns_score = MERC_STUN_SCORE_VAL #VALUE TO ADD
                merc_stuns_score_sign = "+" if merc_stuns_score > 0 else ""
                merc_stuns_value = font.render(str(snake.merc_stuns) + "  ({}{})".format(merc_stuns_score_sign, merc_stuns_score), True, WHITE, BLACK)


                mgs_games = score_font.render("MGS Games Collected:", True, WHITE, BLACK)
                mgs_games_score = snake.mgs_games*MGS_GAME_SCORE_INCREMENT #VALUE TO ADD
                mgs_games_score_sign = "+" if snake.mgs_games > 0 else ""
                mgs_games_value = font.render(str(snake.mgs_games) + "  ({}{})".format(mgs_games_score_sign, mgs_games_score), True, WHITE, BLACK)

                
                continues = score_font.render("Continues:", True, WHITE, BLACK)
                continues_score = -snake.continues*CONTINUES_SCORE_DECREMENT  #VALUE TO ADD
                if continues_score == 0:
                    continues_score = CONTINUES_SCORE_VAL #VALUE TO ADD
                continues_score_sign = "+" if continues_score > 0 else ""
                continues_value = font.render(str(snake.continues) + "  ({}{})".format(continues_score_sign, continues_score), True, WHITE, BLACK)


                noodles_consumed = score_font.render("Instant Noodles Consumed:", True, WHITE, BLACK)
                noodles_consumed_score = -snake.noodles_consumed*NOODLES_CONSUMED_SCORE_DECREMENT #VALUE TO ADD
                if noodles_consumed_score == 0:
                    noodles_consumed_score = NOODLES_CONSUMED_SCORE_VAL #VALUE TO ADD
                noodles_consumed_sign = "+" if noodles_consumed_score > 0 else ""
                noodles_consumed_value = font.render(str(snake.noodles_consumed) + " ({}{})".format(noodles_consumed_sign, noodles_consumed_score), True, WHITE, BLACK)
                
                score = score_font.render("SCORE:", True, WHITE, BLACK)
                snake.score = time_score + merc_alerts_score + merc_stuns_score + mgs_games_score + continues_score + noodles_consumed_score
                score_value = font.render(str(snake.score), True, WHITE, BLACK)
                

                window.blit(mission_results, (window_width*0.40, window_height*0.10))
                window.blit(completion_time, (window_width*0.20, window_height*0.17))
                window.blit(completion_time_value, (window_width*0.20, window_height*0.20))
                window.blit(merc_alerts, (window_width*0.20, window_height*0.25))
                window.blit(merc_alerts_value, (window_width*0.20, window_height*0.28))
                window.blit(merc_stuns, (window_width*0.20, window_height*0.33))
                window.blit(merc_stuns_value, (window_width*0.20, window_height*0.35))
                window.blit(mgs_games, (window_width*0.20, window_height*0.40))
                window.blit(mgs_games_value, (window_width*0.20, window_height*0.43))
                window.blit(noodles_consumed, (window_width*0.20, window_height*0.48))
                window.blit(noodles_consumed_value, (window_width*0.20, window_height*0.51))
                window.blit(continues, (window_width*0.20, window_height*0.56))
                window.blit(continues_value, (window_width*0.20, window_height*0.59))
                window.blit(score, (window_width*0.20, window_height*0.64))
                window.blit(score_value, (window_width*0.20, window_height*0.67))
                
                

            pygame.display.update()

    pygame.quit()
