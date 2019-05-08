'''Author: Jimmy Yu

   Date: May 31, 2017
   
   Decription: This is the module for the Swarm The Bugs! game
'''

import pygame

#MOB ENTITIES 

class Player(pygame.sprite.Sprite):
    '''This is the main sprite in the game, and is controlled by the player'''
    def __init__(self, screen):
        '''The initializer method takes the screen as a parameter and initializes
        all the instance variables. Also loads the player image'''
        #Call parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Set the image of our player and obtain the rect attributes
        self.image = pygame.image.load("./Images/tank.PNG")
        self.image.set_colorkey((255,255,255))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = (300,450)
        
        #Define instance variables
        self.__screen = screen
        
    def update(self):
        '''Update method will be called automatically to reposition the player
        on the screen.'''
        #The player will be controlled using mouse input
        #Extract the x value of the mouse position and assign it to the centerx of the paddle sprite
        self.rect.centerx = pygame.mouse.get_pos()[0]
        
        #Player can not move past the screen width
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > self.__screen.get_width():
            self.rect.right = 640

class Bug(pygame.sprite.Sprite):
    '''This is a class for a bug sprite, this will act as the monsters of the game
    that are trying to kill the player'''
    def __init__(self, screen, pos, distance_x, distance_y):
        '''Initializer method takes the screen, inital position of the bug, and distance that it will travel as parameters and initializes all the instance variables. Loads the bug image and gets the rect to use for positioning.'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Set the image for the bugs and obtain the rect attributes 
        self.image = pygame.image.load("./Images/bug.PNG")
        self.image.set_colorkey((255,255,255))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        #Define instance variables
        self.__dx = 5
        self.__screen = screen
        self.__distance_x = distance_x
        self.__distance_y = distance_y
        self.__pos = pos
        
    def move_down(self):
        '''This method of will move the bug sprite down 2 pixels'''
        self.rect.centery += 3
    
    def change_direction(self):
        '''This method is used for reversing the x direction of the bug sprite'''
        self.__dx = -self.__dx
        
    def update(self):
        '''This update method will automatically reposition the sprite. When it is in between 
        it's original position and the distance that it can travel, it will continue to move.
        If not, it means that the bug has reached the maximum distance that it can travel and must
        reverse it's direction.'''
        if ((self.rect.right < (self.__pos[0] + self.__distance_x)) and (self.__dx > 0)) or\
        ((self.rect.left > self.__pos[0]) and (self.__dx < 0)):
            self.rect.right += self.__dx

        else:
            self.__dx = -self.__dx
            #Check if the bug has reached it's maximum distance that it can travel downward. If it has not continue to move down 
            if self.rect.bottom <= (self.__pos[1] + self.__distance_y):
                self.move_down()
            
class Boss(pygame.sprite.Sprite):
    '''This class defines the boss of the game, and will show up after the first wave is defeated'''
    def __init__(self, screen):
        '''This initializer method takes the screen as a parameter. Loads the boss image and obtains the rect. As well as initializing all the instance variables.'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./Images/boss.PNG")
        self.image.set_colorkey((255,255,255))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        #Define instance variables
        self.__screen = screen
        self.__dx = 10
        self.__dy = 10
        
        self.rect.top = self.__screen.get_height()
        
    def change_direction(self):
        '''This method is used for reversing the x direction of the bug sprite'''
        self.__dx = -self.__dx    
        
    def update(self):
        '''This update method will automatically reposition the sprite. When it is in between 
        it's original position and the distance that it can travel, it will continue to move.
        If not, it means that the bug has reached the maximum distance that it can travel and must
        reverse it's direction.'''
        if ((self.rect.right <= self.__screen.get_width()) and (self.__dx > 0)) or\
           ((self.rect.left >= 0) and (self.__dx < 0)): 
            self.rect.right += self.__dx 
                
        else: 
            self.__dx = -self.__dx
               
                                  
#PROJECTILES                                   
                                  
                                  
class Bullet(pygame.sprite.Sprite):
    '''This class will serve as the projectiles of the player'''
    def __init__(self):
        '''This initalizer method, initializes all the instance variables and loads the image of the bullet.'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load("./Images/tankbullet.PNG")
        self.rect = self.image.get_rect()
        
        #Define the instance variables
        self.__dy = 10
        
    def update(self):
        '''Automatically repositions the sprite downwards, if it reaches the top of the screen, kill itself'''
        self.rect.top -= self.__dy
        
        if self.rect.bottom <= 0:
            self.kill()
            
class Fireball(pygame.sprite.Sprite):
    '''This class will serve as the projectiles of the bugs'''
    def __init__(self, screen):
        '''This initalizer method, initializes all the instance variables and loads the image of the fireball.'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Load the image and obtain the rect
        self.image = pygame.image.load("./Images/fireball.PNG")
        self.image.set_colorkey((255,255,255))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        #Define the instance variables
        self.__screen = screen
        self.__dy = 6      
        
    def update(self):
        '''Automatically repositions the sprite downwards, if it reaches the bottom of the screen, kill itself'''
        self.rect.bottom += self.__dy
        
        if self.rect.top >= self.__screen.get_height():
            self.kill()

class BossFireball(pygame.sprite.Sprite):
    '''This class will serve as the projectiles of the bugs'''
    def __init__(self, screen):
        '''This initalizer method, initializes all the instance variables and loads the image of the fireball.'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Load the image and obtain the rect
        self.image = pygame.image.load("./Images/bossfireball.PNG")
        self.image.set_colorkey((255,255,255))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        
        #Define the instance variables
        self.__screen = screen
        self.__dy = 8   
        
    def update(self):
        '''Automatically repositions the sprite downwards, if it reaches the bottom of the screen, kill itself'''
        self.rect.bottom += self.__dy
        
        if self.rect.top >= self.__screen.get_height():
            self.kill()
        
        
#STATS
        
        
class ScoreKeeper(pygame.sprite.Sprite):
    '''This class defines the sprite for our ScoreKeeper'''
    def __init__(self):
        '''This initializer method creates a font object to be used to render text, as well as intializes the score variable'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Set a custom font, with a font size of 50
        self.__font = pygame.font.Font("customfont.ttf", 25)
        
        #Set the initial score to 0
        self.__score = 0
    
    def player_scored(self):
        '''This method increases the total score by one'''
        self.__score += 1
        
    def boss_score1(self):
        '''This method increases the score by 1000'''
        self.__score += 1000
    
    def boss_score2(self):
        '''This method increases the score by 800'''
        self.__score += 800
    
    def boss_score3(self):
        '''This method increases the score by 600'''
        self.__score += 600
    
    def boss_score4(self):
        '''This method increases the score by 400'''
        self.__score += 400
    
    def boss_score5(self):
        '''This method increases the score by 200'''
        self.__score += 200
    
    def boss_score6(self):
        '''This method increases the score by 1'''
        self.__score += 1
        
    def get_score(self):
        '''This method returns the total score'''
        return self.__score
    
    def update(self):
        '''This update method will be automatically called to update the score.'''
        #Create the string message for the score
        self.__scorelabel = "Score: " + str(self.__score)
        
        #Render that text with the custom font
        self.image = self.__font.render(self.__scorelabel, 1, (0,0,0))
        
        #Get the rect attributes and position the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (50,15)  
        
class HighScore(pygame.sprite.Sprite):
    ''' This class defines the sprite for the high score'''
    def __init__(self, highscore):
        '''This initializer method takes the highscore as a parameter and initializes all the instance variables'''
        pygame.sprite.Sprite.__init__(self)
        
        #Define the instance variables
        self.__font = pygame.font.Font("customfont.ttf", 25)
        self.__highScore = highscore
        
    def update(self):
        '''This update method will automatically be called to update the highscore'''
        #Create the string message for the highscore
        self.__highScoreLabel = "High Score: " + str(self.__highScore)
        
        #Render the text with the cutsom font
        self.image = self.__font.render(self.__highScoreLabel, 1, (0,0,0))
        
        #Obtain the rect and position the sprite
        self.rect = self.image.get_rect()
        self.rect.center = (60,15)
        
class LifeKeeper(pygame.sprite.Sprite):
    '''This class defines the sprite for our life keeper label.'''
    def __init__(self):
        '''This initializer method will initialize two unique variables used for the life keeper label.
        Also, initializes the lives to 3.'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Set the custom font with a font size of 50
        self.__font = pygame.font.Font("customfont.ttf", 25)
        
        #Set the lives to a starting value of 3
        self.__lives = 3
        
    def lose_life(self):
        '''This method decreases the number of lives the player has.'''
        self.__lives -= 1
    
    def get_lives(self):
        '''Returns the number of lives the player has.'''
        return self.__lives
        
    def update(self):
        '''This update method will be automatically called. This method will render the text
        for the number of lives remaining.'''
        #Create the text for the lives remaining
        self.__lifelabel = "Lives: " + str(self.__lives)
        
        #Render the text with the custom font
        self.image = self.__font.render(self.__lifelabel, 1, (0,0,0))
        
        #Get the rect attributes for the sprite and position it
        self.rect = self.image.get_rect()
        self.rect.center = (150, 15)

class bossHP(pygame.sprite.Sprite):
    '''This class defines the sprite for the hp meter of the boss'''
    def __init__(self):
        '''This initializer method initializes all the instance variables'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Define the instance variables
        self.__font = pygame.font.Font("customfont.ttf", 25)
        self.__hp = 200
        
    def lose_hp(self):
        '''This method decreases the hp by 5'''
        self.__hp -= 5
        
    def get_hp(self):
        '''Returns the value of self.__hp'''
        return self.__hp
    
    def update(self):
        '''This update method will be automatically called to update the boss hp'''
        #Create the text for the boss hp remaining
        self.__hplabel = "Boss Hp: " + str(self.__hp)
        
        #Render the text with the custom font
        self.image = self.__font.render(self.__hplabel, 1, (0,0,0))
        
        #Get the rect attributes for the sprite and position it 
        self.rect = self.image.get_rect()
        self.rect.center = (580, 15)        
        
class Timer(pygame.sprite.Sprite):
    '''This class will serve as a timer for the game'''
    def __init__(self):
        '''This initializer method will initializes the instance variables'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Define all the instance variables
        self.__font = pygame.font.Font("customfont.ttf", 25)
        self.__time = 0 
    
    def add_time(self):
        '''This method increases the self.__time by 1'''
        self.__time += 1
        
    def get_time(self):
        '''This method returns the vale of self.__time'''
        return self.__time
        
    def update(self):
        '''This update method will be automatically called to update the time'''
        #Create a string message for the time
        self.__timelabel = "Time: " + str(self.__time)
        
        #Render the message with the custom font
        self.image = self.__font.render(self.__timelabel, 1, (0,0,0))
        
        #Obtain the rect and position it accordingly 
        self.rect = self.image.get_rect()
        self.rect.center = (460, 15)           
        
    
class Wall(pygame.sprite.Sprite):
    '''This is a class for the wall sprite. The purpose of this class is to act 
    as a shield for the player. As the wall loses hit points, the wall image will 
    change as if it is deteriorating.'''
    def __init__(self, pos):
        '''This initializer method takes pos as a parameter, and initializes all the instance variables'''
        #Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Load the image and obtain the rect
        self.image = pygame.image.load("./Images/wall.PNG")
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        #Define the instance variable
        self.__wallHP = 16
        
    def decrease_wallHP(self):
        '''This method decreases the wallHp by 1'''
        self.__wallHP -= 1
        
    def wall_phase2(self):
        ''' This method changes the image of the wall'''
        self.image = pygame.image.load("./Images/wall2.PNG")
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert()
        
    def wall_phase3(self):
        ''' This method changes the image of the wall'''
        self.image = pygame.image.load("./Images/wall3.PNG")
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert()
        
    def wall_phase4(self):
        ''' This method changes the image of the wall'''
        self.image = pygame.image.load("./Images/wall4.PNG")
        self.image.set_colorkey((0,0,0))
        self.image = self.image.convert()
    
    def update(self):
        '''This update method will be automatically called. According to the wallHp, the image of the walls will change'''
        if self.__wallHP == 12:
            self.wall_phase2()
        if self.__wallHP == 8:
            self.wall_phase3()  
        if self.__wallHP == 4:
            self.wall_phase4() 
        if self.__wallHP == 0:
            self.kill()