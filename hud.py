import pygame
from colors import *

class HUD(pygame.Surface):
    '''A class that represents the HUD for Snake.'''
    
    def __init__(self, width, height, snake):
        pygame.Surface.__init__(self, (width, height))
        self.width, self.height = width, height
        self.fill(GRAY)
        self.font = pygame.font.SysFont("ARMY RUST, Arial", 30)
        self.health_label = "HEALTH"
        self.lives_label = "LIVES"
        self.weapon_label = "WEAPON"
        self.item_label = "ITEM"
        self.snake_health = snake.health
        self.snake_weapon = snake.current_weapon
        self.snake_item = snake.current_item
        self.snake_lives = str(snake.lives)

    def draw(self):
        self.fill(GRAY) #Need this so that stuff in the HUD box can get updated

        #HEALTH DISPLAY
        rendered_health_label = self.font.render(self.health_label, True, WHITE, GRAY)
        self.blit(rendered_health_label, (self.width*0.05, self.height*0.20))
        #pygame.draw.rect(self, RED, (self.width*0.14, self.height*0.15, self.snake_health, 25), 0)
###JEREMY
        #this next variable is used for the x-coordinates of the second column of information: the health bar and the number of lives
        health_bar_x = self.width*0.05+self.font.size(self.health_label)[0]+self.width*0.02
        pygame.draw.rect(self, RED, (health_bar_x, self.height*0.20, self.snake_health, 25), 0)
###END JEREMY


        #LIVES DISPLAY
        rendered_lives_label = self.font.render(self.lives_label, True, WHITE, GRAY)
        rendered_lives_value = self.font.render(self.snake_lives, True, WHITE, GRAY)
        #self.blit(rendered_lives_label, (self.width*0.05, self.height*0.55))
        #self.blit(rendered_lives_value, (self.width*0.14, self.height*0.55))
###JEREMY
        #this next variable is used for the y-coordinates of the second row of information: information about the lives and the items
        lives_y = self.height*0.20+25+self.height*0.10
        self.blit(rendered_lives_label, (self.width*0.05, lives_y))
        self.blit(rendered_lives_value, (health_bar_x, lives_y))
###END JEREMY


        #WEAPON DISPLAY
        rendered_weapon_label = self.font.render(self.weapon_label, True, WHITE, GRAY)
        rendered_weapon_value = self.font.render(self.snake_weapon.name, True, WHITE, GRAY)
        rendered_weapon_stock = self.font.render(str(self.snake_weapon.stock), True, WHITE, GRAY)
        self.blit(rendered_weapon_label, (self.width*0.60, self.height*0.20))
        #self.blit(rendered_weapon_value, (self.width*0.80, self.height*0.20))
        #self.blit(rendered_weapon_stock, (self.width*0.95, self.height*0.20))
###JEREMY
        #this next variable is used for the x-coordinates of the fourth column of information: the weapon name and the item name
        weapon_value_x = self.width*0.60+self.font.size(self.weapon_label)[0]+self.width*0.02
        #this next variable is used for the x-coordinates of the fifth column of information: the weapon stock and the item stock
        weapon_stock_x = weapon_value_x+self.font.size(self.snake_weapon.name)[0]+self.width*0.02
        self.blit(rendered_weapon_value, (weapon_value_x, self.height*0.20))
        self.blit(rendered_weapon_stock, (weapon_stock_x, self.height*0.20))
###END JEREMY

        
        #ITEM DISPLAY
        rendered_item_label = self.font.render(self.item_label, True, WHITE, GRAY)
        rendered_item_value = self.font.render(self.snake_item.name, True, WHITE, GRAY)
        rendered_item_stock = self.font.render(str(self.snake_item.stock), True, WHITE, GRAY)
        #self.blit(rendered_item_label, (self.width*0.70, self.height*0.55))
        #self.blit(rendered_item_value, (self.width*0.80, self.height*0.55))
        #self.blit(rendered_item_stock, (self.width*0.95, self.height*0.55))
###JEREMY
        self.blit(rendered_item_label, (self.width*0.60, lives_y))
        self.blit(rendered_item_value, (weapon_value_x, lives_y))
        self.blit(rendered_item_stock, (weapon_stock_x, lives_y))
###END JEREMY


    def update(self, snake):
        if snake.health >= 0:
            self.snake_health = snake.health
        self.snake_weapon = snake.current_weapon
        self.snake_weapon_stock = snake.current_weapon            
        self.snake_item = snake.current_item
        self.snake_lives = str(snake.lives)
