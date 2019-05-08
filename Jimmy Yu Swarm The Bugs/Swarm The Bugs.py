'''Author: Jimmy Yu

   Date: May 31, 2017
   
   Description: Swarm the Bugs! is a top-down shooter game, that has features of the original space invaders game.
   Kill all the bugs to reach the boss level. The final score is based on time taken to kill the boss. For movement controls, use the mouse, to shoot, use mouse button.
'''

# I - IMPORT AND INITIALIZE
import pygame, MySprites, random
pygame.init()
pygame.mixer.init()

def instructions(highScore):
    '''This function shows the instructions to the player. If the player clicks q, the function returns True
    if the player clicks space, the function returns False.'''
    # DISPLAY
    #Set the screen's resolution 
    screen = pygame.display.set_mode((640, 480))    
    pygame.display.set_caption("Instructions!")
    
    #ENTITIES
    
    #Background 
    background = pygame.image.load("./Images/instructions.PNG")
    background = background.convert()    
    
    #Sound
    pygame.mixer.music.load("./Music/bgm.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)     
    
    #Sprites
    player = MySprites.Player(screen)
    highScore = MySprites.HighScore(highScore)
    
    #Sprite Groups
    bulletGroup = pygame.sprite.Group()
    allSprites = pygame.sprite.Group(player, bulletGroup, highScore)
    
    #ASSIGN
    clock = pygame.time.Clock()
    keepGoing = True    
    
    #Hide the mouse cursor
    pygame.mouse.set_visible(False)  
    
    # LOOP
    while keepGoing:    
        # TIME
            
        #Set the frames per second to 30
        clock.tick(30)  
        
        # EVENT HANDLING
            
        #Iterate through the list of events that occurred
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keepGoing = False   
            
            #If user releases mouse button, create a bullet at the position of the player
            elif event.type == pygame.MOUSEBUTTONUP:
            
                #Create a bullet at the midtop position of the player
                bullet = MySprites.Bullet()
                bullet.rect.center = player.rect.midtop
                
                #Add the bullet to the bulletGroup
                bulletGroup.add(bullet)
                allSprites = pygame.sprite.Group(player, bulletGroup, highScore)
            
            #If the user presses space, return False. If the User presses q, return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    keepGoing = False
                    return False
                elif event.key == pygame.K_q:
                    keepGoing = False
                    return True
      
        #REFRESH SCREEN
        
        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)
            
        pygame.display.flip()    
        
        screen.blit(background, (0, 0))
        
    
def game():
    '''This function controls the main game, and returns the score of the player'''
    # DISPLAY
    #Set the screen's resolution 
    screen = pygame.display.set_mode((640, 480))    
    pygame.display.set_caption("Swarm: The Bugs!") 
    
    # ENTITIES
    
    #Background 
    background = pygame.image.load("./Images/background.PNG")
    background = background.convert()

    gameover = pygame.image.load("./Images/gameover.jpg")
    gameover = gameover.convert()
    
    #Sound
    pygame.mixer.music.load("./Music/bgm.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)  
    
    bulletSound = pygame.mixer.Sound("./Music/shoot.wav")
    bulletSound.set_volume(0.06)
    
    splat = pygame.mixer.Sound("./Music/splat.wav")
    splat.set_volume(0.15)
    
    lose_life = pygame.mixer.Sound("./Music/lose_life.wav")
    lose_life.set_volume(0.2)
    
    #Sprites
    player = MySprites.Player(screen)
    scorekeeper = MySprites.ScoreKeeper()
    lifekeeper = MySprites.LifeKeeper()
    boss = MySprites.Boss(screen)
    bossHp = MySprites.bossHP()
    timer = MySprites.Timer()
    
    bugs = []
    ypos = 200
    
    for row in range(5):
        ypos -= 30
        xpos = 20
        for col in range(14):
            bug = MySprites.Bug(screen, (xpos, ypos), 150, 135)
            xpos += 35
            bugs.append(bug)
       
    walls = []
    wall_xpos = 65
    for i in range(6):
        wall = MySprites.Wall((wall_xpos, 370))
        wall_xpos += 100
        walls.append(wall)
        
    #Sprite Groups    
    wallGroup = pygame.sprite.Group(walls)
    bugGroup = pygame.sprite.Group(bugs)
    bulletGroup = pygame.sprite.Group()
    fireballGroup = pygame.sprite.Group()
    bossFireballGroup = pygame.sprite.Group()
    allSprites = pygame.sprite.OrderedUpdates(player, wallGroup, bugGroup, boss, fireballGroup, bossFireballGroup, bulletGroup, scorekeeper, lifekeeper, timer, bossHp)


    # ASSIGN 
    clock = pygame.time.Clock()
    keepGoing = True
    timeCount = 0
    reloading = False
    
    #Hide the mouse cursor
    pygame.mouse.set_visible(False)
    
    # LOOP
    while keepGoing:   
         
        # TIME
        
        #Set the frames per second to 30
        clock.tick(30)
        
        #Player can shoot once every second
        timeCount += 1
        if timeCount % 15 == 0:
            reloading = True
        
        #Add one to the timer every second
        if timeCount % 30 == 0:
            timer.add_time()
            
        # EVENT HANDLING
            
        #Iterate through the list of events that occurred
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.fadeout(2000)
                keepGoing = False   
            
            #If user releases mouse button, create a bullet at the position of the player
            elif event.type == pygame.MOUSEBUTTONUP:
                if reloading:
                    #Create a bullet at the midtop position of the player
                    bullet = MySprites.Bullet()
                    bullet.rect.center = player.rect.midtop
                    bulletSound.play()
                
                    #Add the bullet to the bulletGroup
                    bulletGroup.add(bullet)
                    allSprites = pygame.sprite.OrderedUpdates(player, wallGroup, bugGroup, boss, fireballGroup, bossFireballGroup, bulletGroup, scorekeeper, lifekeeper, timer, bossHp)
                    reloading = False
        
        #Randomly shoot a bug fireball            
        for bug in bugGroup:
            if (random.randrange(400) == 8):
                #Create a fireball at the midbottom of the bug
                fireball = MySprites.Fireball(screen)
                fireball.rect.center = bug.rect.midbottom
                
                #Add the fireball to the sprite groups
                fireballGroup.add(fireball)
                allSprites = pygame.sprite.OrderedUpdates(player, wallGroup, bugGroup, boss, fireballGroup, bossFireballGroup, bulletGroup, scorekeeper, lifekeeper, timer, bossHp)
        
        
        #BOSS         
        #If no more bugs remaining, move the boss inside the playable screen           
        if not len(bugGroup):
            boss.rect.bottom = 225
            #Randomly shoot a boss fireball
            if bossHp.get_hp() > 0:
                if (random.randrange(8) == 2):
                    #Create the fireball at the midbottom position of the boss
                    bossFireball = MySprites.BossFireball(screen)
                    bossFireball.rect.center = boss.rect.midbottom
                
                    #Add the fireball to the sprite groups
                    bossFireballGroup.add(bossFireball)
                    allSprites = pygame.sprite.OrderedUpdates(player, wallGroup, bugGroup, boss, fireballGroup, bossFireballGroup, bulletGroup, scorekeeper, lifekeeper, timer, bossHp)
        
        #Check if the player has killed the boss
        if bossHp.get_hp() <= 0:
            boss.kill()
            splat.play()
            
            #Boss score
            #1000 points
            if (timer.get_time() <= 60):
                scorekeeper.boss_score1()
                pygame.mixer.music.fadeout(2000)
                keepGoing = False
            
            #800 points
            elif (timer.get_time() > 60) and (timer.get_time() <= 70):
                scorekeeper.boss_score2()
                pygame.mixer.music.fadeout(2000)
                keepGoing = False
            
            #600 points
            elif (timer.get_time() > 70) and (timer.get_time() <= 80):
                scorekeeper.boss_score3()
                pygame.mixer.music.fadeout(2000)
                keepGoing = False
                
            #400 points
            elif (timer.get_time() > 80) and (timer.get_time() <= 90):
                scorekeeper.boss_score4()
                pygame.mixer.music.fadeout(2000)
                keepGoing = False
                
            #200 points
            elif (timer.get_time() > 90) and (timer.get_time() <= 100):
                scorekeeper.boss_score5()
                pygame.mixer.music.fadeout(2000)
                keepGoing = False
                
            #1 point
            elif (timer.get_time() > 100):
                scorekeeper.boss_score6()
                pygame.mixer.music.fadeout(2000)
                keepGoing = False
            
        #COLLISION DETECTION   
        
        #Player and fireball
        player_hit_list = pygame.sprite.spritecollide(player, fireballGroup, False)
        for fireball in player_hit_list:
            fireball.kill()
            lose_life.play()
            lifekeeper.lose_life() 
            
            if lifekeeper.get_lives() <= 0:
                pygame.mixer.music.fadeout(2000)
                keepGoing = False
            
        #Fireball and wall
        for fireball in fireballGroup:
            wall_hit_list = pygame.sprite.spritecollide(fireball, wallGroup, False)
            for wall in wall_hit_list:
                fireball.kill()
                wall.decrease_wallHP()
                
        #Player and boss fireball
        player_hit_list2 = pygame.sprite.spritecollide(player, bossFireballGroup, False)
        for bossFireball in player_hit_list2:
            bossFireball.kill()
            lose_life.play()
            lifekeeper.lose_life()    
            
            if lifekeeper.get_lives() <= 0:
                pygame.mixer.music.fadeout(2000)
                keepGoing = False            
        
        #Boss fireball and wall
        for bossFireball in bossFireballGroup:
            wall_hit_list2 = pygame.sprite.spritecollide(bossFireball, wallGroup, False)
            for wall in wall_hit_list2:
                bossFireball.kill()
                wall.decrease_wallHP()            
        
        #Bullet and bug. Bullet and wall. Bullet and boss.
        for bullet in bulletGroup:
            #Check if any bullets in bulletGroup has collided with a bug in bugGroup and store it in a variable
            bug_hit_list = pygame.sprite.spritecollide(bullet, bugGroup, False)
            wall_hit_list = pygame.sprite.spritecollide(bullet, wallGroup, False)
            
            if bullet.rect.colliderect(boss.rect):
                bullet.kill()
                bossHp.lose_hp()
                                         
            for bug in bug_hit_list:                
                bug.kill()
                bullet.kill()
                splat.play()
                scorekeeper.player_scored()
            
            for wall in wall_hit_list:
                bullet.kill()
                wall.decrease_wallHP()       
  
  
        # REFRESH SCREEN

        allSprites.clear(screen, background)
        allSprites.update()
        allSprites.draw(screen)

        pygame.display.flip()  
        
        screen.blit(background, (0, 0))
        
    screen.blit(gameover, (0,0))
    pygame.display.flip()
    
    #Make the mouse cursor visible again
    pygame.mouse.set_visible(True)    

    #Delay for 2 seconds so the music can fadeout
    pygame.time.delay(2000)
    
    return scorekeeper.get_score()


def main():
    '''This function controls the mainline logic of the game'''
    quitGame = False
    highScore = 0
    
    while not quitGame:
        #Call the instructions function that will return True or False
        quitGame = instructions(highScore)

        #If quitGame is False, the player wants to play. Therefore call the game function which returns the last score the player got
        if not quitGame:
            lastScore = game()
            #Check which is greater between the current highscore and the last score, and store that number in the variable highScore
            highScore = max(highScore, lastScore)
    
    #If instructions returns True, the player wants to quit the game. Therefore call pygame.quit()
    pygame.quit()

#Call the main function
main()