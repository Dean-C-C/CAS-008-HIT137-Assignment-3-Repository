#Importations
#Voice-acted by my talented friend, Scott
import pygame
from pygame import mixer
mixer.init()
import random
import os
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

#Setting screen parameters
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

#use os to set working directory to game folder
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Initialisations
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode ([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.DOUBLEBUF)
screen.set_alpha(None)
screen.fill((0,0,0))
running = True
gamewin = False
gamelose = False
#Enemy spawn timer initialisation
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 3000)
#Obstruction spawn location list
obstruction_interval_list = [1000, 2000, 4000, 6000, 7000, 8000, 10000, 11000, 13000, 15000, 17000, 18000, 20000]
#Collectable spawn location list
collectable_interval_list = [1000, 3500, 5000, 7000, 8500, 9000, 10000, 11500, 12000, 15000, 17500, 18000, 20500]
scorecounter = 0
scorevalue = 0
playerhp = 10

#Music and some sound initialisation **
collectablesound = pygame.mixer.Sound("Gamesounds/collectable.wav")
bgmusictrack = pygame.mixer.music.load("Gamesounds/domainofdarkness.wav")
pygame.mixer.music.play(-1)
#Setting a variable for floor height to make spawning enemies easier
floorheight = 150

#Level initialisations for later triggering level changes
#Wait. Should I put in a += level counter instead?
#Otherwise I have to put in if level_1 = true for the level change conditions
level_1_start = True
level_1 = True
level_2_start = False
level_2 = False
level_3_start = False
level_3 = False
boss_level_start = False
boss_level = False
Levelcounter = 1

victorylevel1 = pygame.mixer.Sound("Gamesounds/victorylevel1.wav")
victorylevel2 = pygame.mixer.Sound("Gamesounds/victorylevel2.wav")
victorylevel3 = pygame.mixer.Sound("Gamesounds/victorylevel3.wav")
victoryboss = pygame.mixer.Sound("Gamesounds/knightgamefinish.wav")

#Initialising timers
enemy_spawn_time = pygame.time.get_ticks()
enemy_update_time = pygame.time.get_ticks()

#Caption and screen background initialisations
pygame.display.set_caption("Castle Knight")
background = pygame.image.load("Assets/backgroundlevel1.png").convert()
bg_image = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

#Backgrounds level 2
background_level_2 = pygame.image.load("Assets/backgroundlevel2.png").convert()

#Backgrounds level 3
background_level_3 = pygame.image.load("Assets/backgroundlevel3.png").convert()
background_entrance_level_3 = pygame.image.load("Assets/background_entrance_level_3.png").convert()
background_exit_level_3 = pygame.image.load("Assets/background_exit_level_3.png").convert()

#Background for boss arena
background_boss_arena = pygame.image.load("Assets/boss_arena.png").convert()

#Sidescrolling effect on background initialisation
background_offset = 0
#Sidescrolling background setup
bg_x_1 = 0
bg_x_2 = SCREEN_WIDTH

#Sidescrolling camera
def update_camera():
    global camera_x
    camera_x = player.rect.centerx - SCREEN_WIDTH / 2

#Level initialisation
LEVEL_LEFT_BOUND = 0
LEVEL_RIGHT_BOUND = 32000
playerposition = SCREEN_WIDTH / 2

#Player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("Assets/castleknight.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (60, 100))
        self.rect = self.surf.get_rect()
        #Make player by default appear at a certain height
        self.rect.center = (250, SCREEN_HEIGHT - floorheight)
        self.facing_right = True
        self.spearcd = False
        self.spearcdms = 500
        self.hp = 10
        self.movement_speed = 14
        self.immunity = False
        self.immunitycdms = 2000
        self.immunitycdstart = 0
        self.immunitycdend = 0
        self.spearcdstart = 0
        self.spearcdend = 0
        self.playeralive = True
        self.onground = True
        self.gravity = 1
        self.velocity_y = 0
        self.jump_speed = -22.5

        #Sounds:
        self.damagesound = pygame.mixer.Sound("Gamesounds/knightdamage1.wav")
        self.damagesound2 = pygame.mixer.Sound("Gamesounds/knightdamage2.wav")
        self.damagesound3 = pygame.mixer.Sound("Gamesounds/knightdamage3.wav")
        self.deathsound = pygame.mixer.Sound("Gamesounds/epicknightdeathaudio.wav")
        self.spearthrow = pygame.mixer.Sound("Gamesounds/spearthrow.wav")

    #Set up controls
    def update(self, pressed_keys):
        self.spearcdend = pygame.time.get_ticks()
        self.immunitycdend = pygame.time.get_ticks()
        if self.spearcdend > self.spearcdstart + self.spearcdms:
                self.spearcd = False

        if self.immunitycdend > self.immunitycdstart + self.immunitycdms:
                self.immunity = False
        
        if self.playeralive:
            if pressed_keys[K_UP] and self.onground:
                    self.onground = False
                    self.velocity_y = self.jump_speed
            if pressed_keys[K_LEFT]:
                    self.rect.move_ip(-self.movement_speed, 0)
                    if self.facing_right:
                        self.surf = pygame.transform.flip(self.surf, True, False)
                        self.facing_right = False
            if pressed_keys[K_RIGHT]:
                    self.rect.move_ip(self.movement_speed, 0)
                    if self.facing_right == False:
                        self.surf = pygame.transform.flip(self.surf, True, False)
                        self.facing_right = True
            if pressed_keys[K_SPACE] and self.spearcd == False:
                if self.facing_right:
                    self.spearcdstart = pygame.time.get_ticks()
                    playerspear = Spear(player.rect.centerx + 20, player.rect.centery, "right")
                    projectilesgroup.add(playerspear)
                    playerprojectilesgroup.add(playerspear)
                    self.spearcd = True
                    pygame.mixer.Sound.play(self.spearthrow)
                elif self.facing_right == False:
                    self.spearcdstart = pygame.time.get_ticks()
                    playerspear = Spear(player.rect.centerx - 140, player.rect.centery, "left")
                    projectilesgroup.add(playerspear)
                    playerprojectilesgroup.add(playerspear)
                    self.spearcd = True
                    pygame.mixer.Sound.play(self.spearthrow)

        #Stops the player from moving out of bounds
        if self.rect.left < LEVEL_LEFT_BOUND:
             self.rect.left = 0
        if self.rect.right > LEVEL_RIGHT_BOUND - SCREEN_WIDTH / 2:
             self.rect.right = LEVEL_RIGHT_BOUND - SCREEN_WIDTH / 2
        if self.rect.bottom > SCREEN_HEIGHT - floorheight:
             self.rect.bottom = SCREEN_HEIGHT - floorheight
             self.onground = True
             self.velocity_y = 0

        if not self.onground:
            self.velocity_y += self.gravity
            self.rect.move_ip(0, self.velocity_y)

    def losehp(self):
        if self.immunity == False and self.hp > 0:
            self.hp -= 1
            self.immunity = True
            self.immunitycdstart = pygame.time.get_ticks()
            pygame.mixer.Sound.play(random.choice([self.damagesound, self.damagesound2, self.damagesound3]))
            if self.hp == 0 and self.hp > -1:
                self.playeralive = False
                pygame.mixer.Sound.play(self.deathsound)
                self.damagesound.stop()
                self.damagesound2.stop()
                self.damagesound3.stop()
                self.surf = pygame.image.load("Assets/castleknightdead.png").convert_alpha()
                self.surf = pygame.transform.scale(self.surf, (100, 60))
                self.rect = self.surf.get_rect(midbottom=self.rect.midbottom)
                global gamelose
                gamelose = True
            print(self.hp)
#Obstacle class for defining obstacles and enemies
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, image_path, width, height, x, y):
        super(Obstacle, self).__init__()
        self.image_path = image_path
        self.width = width
        self.height = height
        self.surf = pygame.image.load(self.image_path).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, (width, height))
        self.rect = self.surf.get_rect(topleft=(x, y))

#Projectle classes

class Knife(Obstacle):
    def __init__(self, x, y, facing):
        super().__init__("Assets/knife.png", 40, 25, x, y)
        self.speed = 2
        self.velocity = 0
        self.facing = facing
        self.facingleft = False
        self.facingright = False

        if self.facing == "left":
            self.facingleft = True
            self.surf = pygame.transform.flip(self.surf, True, False)
        elif self.facing == "right":
            self.facingright = True

    def update(self, playerposition):
        if self.facingleft:
            self.velocity = -14 - self.speed
        elif self.facingright:
            self.velocity = 14 + self.speed
        self.rect.x += self.velocity
        if self.rect.centerx > playerposition + SCREEN_WIDTH / 2:
            self.kill()
        elif self.rect.centerx < playerposition - SCREEN_WIDTH / 2:
            self.kill()

class Spear(Obstacle):
    def __init__(self, x, y, facing):
        super().__init__("Assets/spear.png", 112, 21, x, y)
        self.speed = 2
        self.velocity = 0
        self.facing = facing
        self.facingleft = False
        self.facingright = False

        if self.facing == "left":
            self.facingleft = True
            self.surf = pygame.transform.flip(self.surf, True, False)
        elif self.facing == "right":
            self.facingright = True

    def update(self, playerposition):
        if self.facingleft:
            self.velocity = -20 - self.speed
        elif self.facingright:
            self.velocity = 20 + self.speed
        self.rect.x += self.velocity
        if self.rect.centerx > playerposition + SCREEN_WIDTH / 2:
            self.kill()
        elif self.rect.centerx < playerposition - SCREEN_WIDTH / 2:
            self.kill() 

#Enemy subclasses
class Bandit(Obstacle):
    def __init__(self, x):
        super().__init__("Assets/bandit.png", 60, 100, x, SCREEN_HEIGHT - floorheight - 100)
        self.facing_right = True
        self.speed = 6
        self.hp = 1
        self.deathsound1 = pygame.mixer.Sound("Gamesounds/Banditdeathsound1.wav")
        self.deathsound2 = pygame.mixer.Sound("Gamesounds/Banditdeathsound2.wav")
        self.deathsound3 = pygame.mixer.Sound("Gamesounds/Banditdeathsound3.wav")
        self.deathsound1.set_volume(0.6)
        self.deathsound2.set_volume(0.6)
        self.deathsound3.set_volume(0.6)
    #Bandit behaviour
    def update(self, playerposition):
        if self.hp <= 0:
           pygame.mixer.Sound.play(random.choice([self.deathsound1, self.deathsound2, self.deathsound3]))
           self.kill()
        if self.rect.centerx < playerposition - 700 or self.rect.centerx > playerposition + 700:
            self.speed = 16
        else: self.speed = 6
        
        if self.rect.centerx < playerposition:
            self.rect.x += self.speed
            if self.facing_right == False:
                self.surf = pygame.transform.flip(self.surf, True, False)
                self.facing_right = True
        elif self.rect.centerx > playerposition:
            self.rect.x -= self.speed
            if self.facing_right:
                self.surf = pygame.transform.flip(self.surf, True, False)
                self.facing_right = False

    def losehp(self):
        self.hp -= 1
        global scorecounter
        scorecounter += 1

class Knifethrowerbandit(Obstacle):
    def __init__(self, x):
        super().__init__("Assets/knifethrowerbandit.png", 60, 100, x, SCREEN_HEIGHT - floorheight - 100)
        self.facing_right = True
        self.knifecdstart = pygame.time.get_ticks()
        self.speed = 6
        self.hp = 2
        self.knifethrowingcd = True
        self.knifethrowingcdms = 4000
        self.inrange = False
        self.deathsound1 = pygame.mixer.Sound("Gamesounds/Knifebanditdeath1.wav")
        self.deathsound2 = pygame.mixer.Sound("Gamesounds/Knifebanditdeath2.wav")
        self.deathsound3 = pygame.mixer.Sound("Gamesounds/Knifebanditdeath3.wav")
        self.damagetaken = pygame.mixer.Sound("Gamesounds/Knifebanditdamagetake.wav")
        self.knifethrow = pygame.mixer.Sound("Gamesounds/knifethrow.wav")
        self.deathsound1.set_volume(0.6)
        self.deathsound2.set_volume(0.6)
        self.deathsound3.set_volume(0.5)
        self.damagetaken.set_volume(0.6)

    #Knifethrowerbandit behaviour
    def update(self, playerposition):
        self.knifetimerend = pygame.time.get_ticks()
        if self.hp <= 0:
           self.damagetaken.stop()
           pygame.mixer.Sound.play(random.choice([self.deathsound1, self.deathsound2, self.deathsound3]))
           self.kill()
        if self.rect.centerx < playerposition - 720 or self.rect.centerx > playerposition + 720:
            self.speed = 16
        else: self.speed = 6

        
        if self.knifetimerend > self.knifecdstart + self.knifethrowingcdms:
            self.knifethrowingcd = False

        if self.rect.centerx > playerposition - 410 and self.rect.centerx < playerposition + 410:
            self.inrange = True
        else: self.inrange = False

        if self.rect.centerx < playerposition:
            if self.facing_right == False:
                self.surf = pygame.transform.flip(self.surf, True, False)
                self.facing_right = True
        elif self.rect.centerx > playerposition:
            if self.facing_right:
                self.surf = pygame.transform.flip(self.surf, True, False)
                self.facing_right = False
        if self.rect.centerx <= playerposition - 400:
            self.rect.x += self.speed
        if self.rect.centerx > playerposition - 400 and self.rect.centerx < playerposition:
            self.rect.x -= self.speed
        if self.rect.centerx >= playerposition + 400:
            self.rect.x -= self.speed
        if self.rect.centerx < playerposition - 400 and self.rect.centerx > playerposition:
            self.rect.x = 0
        
        if self.knifethrowingcd == False:
                if self.inrange:
                    if self.rect.centerx < playerposition and self.facing_right:
                        newknife = Knife(self.rect.centerx + 20, self.rect.centery, "right")
                        pygame.mixer.Sound.play(self.knifethrow)
                        projectilesgroup.add(newknife)
                        enemyprojectilesgroup.add(newknife)
                        self.knifethrowingcd = True
                        self.knifecdstart = pygame.time.get_ticks()
                    elif self.rect.centerx > playerposition and self.facing_right == False:
                        newknife = Knife(self.rect.centerx - 20, self.rect.centery, "left")
                        pygame.mixer.Sound.play(self.knifethrow)
                        projectilesgroup.add(newknife)
                        enemyprojectilesgroup.add(newknife)
                        self.knifethrowingcd = True
                        self.knifecdstart = pygame.time.get_ticks()
            
    def losehp(self):
        self.hp -= 1
        global scorecounter
        scorecounter += 1
        if self.hp >= 1:
            pygame.mixer.Sound.play(self.damagetaken)

class Funsizedbandit(Obstacle):
    def __init__(self, x):
        super().__init__("Assets/funsizedbandit.png", 160, 160, x, SCREEN_HEIGHT - floorheight - 160)
        self.facing_right = True
        self.hp = 3
        self.speed = 6
        self.maxspeed = 15
        self.inertia = 0.2
        self.bootstepcdstart = 0
        self.bootstepcdend = 0
        self.bootstepcdms = 3500
        self.bootstepcd = False
        self.screech1 = pygame.mixer.Sound("Gamesounds/screech1.wav")
        self.screech2 = pygame.mixer.Sound("Gamesounds/screech2.wav")
        self.screech3 = pygame.mixer.Sound("Gamesounds/screech3.wav")
        self.heavybootstep = pygame.mixer.Sound("Gamesounds/heavybootstep.wav")
        self.damagetaken = pygame.mixer.Sound("Gamesounds/funsizedbanditdamagetaken.wav")
        self.death1 = pygame.mixer.Sound("Gamesounds/funsizedbanditdeath1.wav")
        self.death2 = pygame.mixer.Sound("Gamesounds/funsizedbanditdeath2.wav")
        self.death3 = pygame.mixer.Sound("Gamesounds/funsizedbanditdeath3.wav")
        self.heavybootstep.set_volume(0.5)

    def update(self, playerposition):
        if self.hp <= 0:
           self.screech1.stop()
           self.screech2.stop()
           self.screech3.stop()
           self.heavybootstep.stop()
           self.damagetaken.stop()
           pygame.mixer.Sound.play(random.choice([self.death1, self.death2, self.death3]))
           self.kill()
        self.bootstepcdend = pygame.time.get_ticks()
        if self.rect.centerx < playerposition - 720 or self.rect.centerx > playerposition + 720:
            self.maxspeed = 20
        else: self.maxspeed = 15
        if self.bootstepcdend > self.bootstepcdstart + self.bootstepcdms:
            self.bootstepcd = False
        if self.rect.centerx <= playerposition:
            self.speed += self.inertia
            self.rect.x += self.speed
            if self.facing_right == False:
                self.surf = pygame.transform.flip(self.surf, True, False)
                self.facing_right = True
                pygame.mixer.Sound.play(random.choice([self.screech1, self.screech2, self.screech3]))
        if self.rect.centerx > playerposition:
            self.speed -= self.inertia
            self.rect.x += self.speed
            if self.facing_right:
                self.surf = pygame.transform.flip(self.surf, True, False)
                self.facing_right = False
                pygame.mixer.Sound.play(random.choice([self.screech1, self.screech2, self.screech3]))
        if self.speed > 0 and self.speed > self.maxspeed:
            self.speed = self.maxspeed
        if self.speed < 0 and self.speed < -self.maxspeed:
            self.speed = -self.maxspeed
        if self.bootstepcd == False:
            if self.speed > 0 and self.speed > 4:
                pygame.mixer.Sound.play(self.heavybootstep)
                self.bootstepcd = True
                self.bootstepcdstart = pygame.time.get_ticks()
            if self.speed < 0 and self.speed < 4:
                pygame.mixer.Sound.play(self.heavybootstep)
                self.bootstepcd = True
                self.bootstepcdstart = pygame.time.get_ticks()

    def losehp(self):
        self.hp -= 1
        pygame.mixer.Sound.play(self.damagetaken)
        global scorecounter
        scorecounter += 1

class Bossbandit(Obstacle):
    def __init__(self):
        super().__init__("Assets/bossbandit.png", 200, 180, 3000, SCREEN_HEIGHT - floorheight - 180)
        self.hp = 25
        self.speed = 8
        self.maxspeed = 16
        self.inertia = 0.5
        self.bootstepcdstart = 0
        self.bootstepcdend = 0
        self.bootstepcdms = 3500
        self.bootstepcd = False
        self.facing_right = True
        self.spearthrowing = False
        self.spearthrowingcd = True
        self.spearthrowingcdms = 5000
        self.spearcdstart = pygame.time.get_ticks()
        self.inrange = False
        global bgmusictrack
        bgmusictrack = pygame.mixer.music.load("Gamesounds/bossmusic.wav")
        pygame.mixer.music.play(1)
        
        #Sounds:
        self.damage1 = pygame.mixer.Sound("Gamesounds/bossdamage1.wav")
        self.damage2 = pygame.mixer.Sound("Gamesounds/bossdamage2.wav")
        self.damage3 = pygame.mixer.Sound("Gamesounds/bossdamage3.wav")
        self.damage4 = pygame.mixer.Sound("Gamesounds/bossdamage4.wav")
        self.knifethrow = pygame.mixer.Sound("Gamesounds/knifethrow.wav")
        self.screech1 = pygame.mixer.Sound("Gamesounds/screech1.wav")
        self.screech2 = pygame.mixer.Sound("Gamesounds/screech2.wav")
        self.screech3 = pygame.mixer.Sound("Gamesounds/screech3.wav")
        self.heavybootstep = pygame.mixer.Sound("Gamesounds/heavybootstep.wav")
        self.heavybootstep.set_volume(0.5)

    def update(self, playerposition):
        if self.hp <= 0:
            self.kill()
            self.damage1.stop()
            self.damage2.stop()
            self.damage3.stop()
            self.damage4.stop()
            self.screech1.stop()
            self.screech2.stop()
            self.screech3.stop()
            self.heavybootstep.stop()
            pygame.mixer.Sound.play(victoryboss)
            global gamewin
            gamewin = True
        self.speartimerend = pygame.time.get_ticks()
        if self.speartimerend > self.spearcdstart + self.spearthrowingcdms:
            self.spearthrowingcd = False
        if self.rect.centerx < playerposition - 720 or self.rect.centerx > playerposition + 720:
            self.maxspeed = 20
        else:
            self.maxspeed = 16
        if self.bootstepcdend > self.bootstepcdstart + self.bootstepcdms:
            self.bootstepcd = False
        if self.rect.centerx <= playerposition:
            self.speed += self.inertia
            self.rect.x += self.speed
            if self.facing_right == False:
                self.surf = pygame.transform.flip(self.surf, True, False)
                self.facing_right = True
                pygame.mixer.Sound.play(random.choice([self.screech1, self.screech2, self.screech3]))
        if self.rect.centerx > playerposition:
            self.speed -= self.inertia
            self.rect.x += self.speed
            if self.facing_right:
                self.surf = pygame.transform.flip(self.surf, True, False)
                self.facing_right = False
                pygame.mixer.Sound.play(random.choice([self.screech1, self.screech2, self.screech3]))
        if self.speed > 0 and self.speed > self.maxspeed:
            self.speed = self.maxspeed
        if self.speed < 0 and self.speed < -self.maxspeed:
            self.speed = -self.maxspeed
        if self.bootstepcd == False:
            if self.speed > 0 and self.speed > 4:
                pygame.mixer.Sound.play(self.heavybootstep)
                self.bootstepcd = True
                self.bootstepcdstart = pygame.time.get_ticks()
            if self.speed < 0 and self.speed < 4:
                pygame.mixer.Sound.play(self.heavybootstep)
                self.bootstepcd = True
                self.bootstepcdstart = pygame.time.get_ticks()
        if self.rect.centerx > playerposition - 510 and self.rect.centerx < playerposition + 510:
            self.inrange = True
        else: self.inrange = False
        if self.spearthrowingcd == False:
                if self.inrange:
                    if self.rect.centerx < playerposition and self.facing_right:
                        newbossspear = Spear(self.rect.centerx + 40, self.rect.centery, "right")
                        pygame.mixer.Sound.play(self.knifethrow)
                        projectilesgroup.add(newbossspear)
                        enemyprojectilesgroup.add(newbossspear)
                        self.spearthrowingcd = True
                        self.spearcdstart = pygame.time.get_ticks()
                    elif self.rect.centerx > playerposition and self.facing_right == False:
                        newspear = Spear(self.rect.centerx - 40, self.rect.centery, "left")
                        pygame.mixer.Sound.play(self.knifethrow)
                        projectilesgroup.add(newspear)
                        enemyprojectilesgroup.add(newspear)
                        self.spearthrowingcd = True
                        self.spearcdstart = pygame.time.get_ticks()

    def losehp(self):
        self.hp -= 1
        pygame.mixer.Sound.play(random.choice([self.damage1, self.damage2, self.damage3, self.damage4]))
        global scorecounter
        scorecounter += 1

#Obstruction subclasses

class Spikes(Obstacle):
    def __init__(self, x):
        super().__init__("Assets/spikes.png", 200, 50, x, SCREEN_HEIGHT - floorheight - 50)
    def update(self, playerposition):
        pass

    def losehp(self):
        pass

class Barrel(Obstacle):
    def __init__(self, x):
        super().__init__("Assets/barrel.png", 80, 100, x, SCREEN_HEIGHT - floorheight - 100)

class Crate(Obstacle):
    def __init__(self, x):
        super().__init__("Assets/crate.png", 120, 120, x, SCREEN_HEIGHT - floorheight - 120)

#Collectable subclasses

class Chalice(Obstacle):
    def __init__(self, x, y):
        super().__init__("Assets/chalice.png", 40, 60, x, y)

class Coin(Obstacle):
    def __init__(self, x, y):
        super().__init__("Assets/coin.png", 40, 40, x, y)


#Background classes for ease of placing start/end backgrounds
class Background(Obstacle):
    def __init__(self, image_path, x, y):
        super().__init__(image_path, 960, 720, x, y)

#Enemy list, groups and initialisation
player = Player()
enemies = pygame.sprite.Group()
obstaclesprites = pygame.sprite.Group()
obstructionsprites = pygame.sprite.Group()
collectablesprites = pygame.sprite.Group()
projectilesgroup = pygame.sprite.Group()
enemyprojectilesgroup = pygame.sprite.Group()
playerprojectilesgroup = pygame.sprite.Group()
endbackgroundgroup = pygame.sprite.Group()

#Start/end backgrounds
startbackground = Background("Assets/background_entrance_level_1.png", -720, 0)
obstaclesprites.add(startbackground)
endbackground = Background("Assets/background_exit_level_1.png", 21000, 0)
obstaclesprites.add(endbackground)
endbackgroundgroup.add(endbackground)

#Enemy lists
enemies_level_1 = [
    Bandit
]

enemies_level_2 = [
    Bandit,
    Knifethrowerbandit,
    Knifethrowerbandit
]

enemies_level_3 = [
    Bandit,
    Bandit,
    Knifethrowerbandit,
    Knifethrowerbandit,
    Funsizedbandit
]

boss_enemy = [
    Bossbandit
]

#Obstruction list
obstruction_list = [
    Barrel,
    Crate,
    Spikes
]

#Collectable list
collectable_list = [
    Chalice,
    Coin
]

#Enemy spawns
def spawn_enemy_level_1():
    if playerposition > 1000:
        random_enemy = random.choice(enemies_level_1)
        if random_enemy == Bandit:
            new_enemy = Bandit(random.choice([playerposition - 800, playerposition + 800]))
        # Add the enemy to the enemies group
        enemies.add(new_enemy)
        obstaclesprites.add(new_enemy)

def spawn_enemy_level_2():
    if playerposition > 1000:
        random_enemy = random.choice(enemies_level_2)
        if random_enemy == Bandit:
            new_enemy = Bandit(playerposition + SCREEN_WIDTH)
        if random_enemy == Knifethrowerbandit:
            new_enemy = Knifethrowerbandit(random.choice([playerposition - SCREEN_WIDTH, playerposition + SCREEN_WIDTH]))
        # Add the enemy to the enemies group
        enemies.add(new_enemy)
        obstaclesprites.add(new_enemy)

def spawn_enemy_level_3():
    if playerposition > 1000:
        random_enemy = random.choice(enemies_level_3)
        if random_enemy == Bandit:
            new_enemy = Bandit(random.choice([playerposition - SCREEN_WIDTH, playerposition + SCREEN_WIDTH]))
        if random_enemy == Knifethrowerbandit:
            new_enemy = Knifethrowerbandit(random.choice([playerposition - SCREEN_WIDTH, playerposition + SCREEN_WIDTH]))
        if random_enemy == Funsizedbandit:
            new_enemy = Funsizedbandit(random.choice([playerposition - SCREEN_WIDTH, playerposition + SCREEN_WIDTH]))
        # Add the enemy to the enemies group
        enemies.add(new_enemy)
        obstaclesprites.add(new_enemy)

def spawn_boss():
    if playerposition > 1000:
        new_enemy = Bossbandit()
        # Add the boss to the enemies group
        enemies.add(new_enemy)
        obstaclesprites.add(new_enemy)
        pygame.time.set_timer(ADDENEMY, 0)

#Obstruction spawns
def populate_obstructions():
        obstruction_entity_list = []
        for obstruction_location in obstruction_interval_list:
            obstruction_choice = random.choice(obstruction_list)
            if obstruction_choice == Barrel:
                new_obstruction = Barrel(obstruction_location)
                obstruction_entity_list.append(new_obstruction)
                obstaclesprites.add(new_obstruction)
                obstructionsprites.add(new_obstruction)
            elif obstruction_choice == Crate:
                new_obstruction = Crate(obstruction_location)
                obstruction_entity_list.append(new_obstruction)
                obstaclesprites.add(new_obstruction)
                obstructionsprites.add(new_obstruction)
            elif obstruction_choice == Spikes:
                new_obstruction = Spikes(obstruction_location)
                obstruction_entity_list.append(new_obstruction)
                obstaclesprites.add(new_obstruction)
                obstructionsprites.add(new_obstruction)
                enemies.add(new_obstruction)
            
#Collectable spawns
def populate_collections():
        collectable_entity_list = []
        random_collectable_height = random.choice([SCREEN_HEIGHT - floorheight - 180, SCREEN_HEIGHT - floorheight - 250])
        for collectable_location in collectable_interval_list:
            collectable_choice = random.choice(collectable_list)
            if collectable_choice == Coin:
                new_collectable = Coin(collectable_location, random_collectable_height)
                random_collectable_height = random.choice([SCREEN_HEIGHT - floorheight - 180, SCREEN_HEIGHT - floorheight - 250])
                collectable_entity_list.append(new_collectable)
                obstaclesprites.add(new_collectable)
                collectablesprites.add(new_collectable)
            elif collectable_choice == Chalice:
                new_collectable = Chalice(collectable_location, random_collectable_height)
                random_collectable_height = random.choice([SCREEN_HEIGHT - floorheight - 180, SCREEN_HEIGHT - floorheight - 250])
                collectable_entity_list.append(new_collectable)
                obstaclesprites.add(new_collectable)
                collectablesprites.add(new_collectable)

#Collectable score text
def render_collectable_score(scorevalue):
    collectable_text = f"Score: {scorevalue}"
    text_surface = font.render(collectable_text, True, (255, 255, 255))
    return text_surface

#Controls text
textcontrols = font.render(f"Controls: Arrow keys to move and jump, Spacebar to throw spear.", True, (255, 255, 255))

#Hp bar def
def playerhpbar():
    player_max_hp = 10
    player_current_hp = playerhp
    hp_bar_width = 200
    hp_bar_height = 25
    hp_bar_x = SCREEN_WIDTH - hp_bar_width - 20
    hp_bar_y = 20
    hp_portion = player_current_hp / player_max_hp
    pygame.draw.rect(screen, (0, 0, 0), (hp_bar_x, hp_bar_y, hp_bar_width, hp_bar_height))
    pygame.draw.rect(screen, (255, 0, 0), (hp_bar_x, hp_bar_y, hp_bar_width * hp_portion, hp_bar_height))
#Game loop
while running:
    #Setup clock for 60 FPS
    clock = pygame.time.Clock() 
    clock.tick(30)
    #playerposition get
    if not gamelose:
        playerposition = player.rect.centerx
    elif gamelose:
        playerposition = 35000
    #player hp get
    playerhp = player.hp
    #Camera update
    update_camera()
    #Update score
    scorevalue = scorecounter * 10
    #Levelcounter regulator just in case
    if Levelcounter > 4:
        Levelcounter = 4
    #Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        #Enemy spawn event
        if event.type == ADDENEMY and Levelcounter == 1:
            spawn_enemy_level_1()
        if event.type == ADDENEMY and Levelcounter == 2:
            spawn_enemy_level_2()
        if event.type == ADDENEMY and Levelcounter == 3:
            spawn_enemy_level_3()
        if event.type == ADDENEMY and Levelcounter == 4:
            spawn_boss()
    #Initiate non-enemy spawns for levels and initiating background variable swaps
    if pygame.sprite.spritecollideany(player, endbackgroundgroup):
        Levelcounter += 1
        player.rect.centerx = 250
        if Levelcounter == 2:
            level_2_start = True
        if Levelcounter == 3:
            level_3_start = True
        if Levelcounter == 4:
            boss_level_start = True
    if level_1_start:
        populate_obstructions()
        populate_collections()
        level_1_start = False
    if level_2_start:
        player.hp = 10
        pygame.time.set_timer(ADDENEMY, 0)
        level_1 = False
        enemies.empty()
        obstaclesprites.empty()
        obstructionsprites.empty()
        collectablesprites.empty()
        projectilesgroup.empty()
        playerprojectilesgroup.empty()
        endbackgroundgroup.empty()
        projectilesgroup.empty()
        playerprojectilesgroup.empty()
        enemyprojectilesgroup.empty()
        obstruction_entity_list = []
        collectable_entity_list = []
        pygame.mixer.Sound.play(victorylevel1)
        populate_obstructions()
        bg_image = pygame.transform.scale(background_level_2, (SCREEN_WIDTH, SCREEN_HEIGHT))
        startbackground = Background("Assets/background_entrance_level_2.png", -720, 0)
        obstaclesprites.add(startbackground)
        endbackground = Background("Assets/background_exit_level_2.png", 21000, 0)
        obstaclesprites.add(endbackground)
        endbackgroundgroup.add(endbackground)
        level_2_start = False
        Levelcounter = 2
        pygame.time.set_timer(ADDENEMY, 3000)
        pygame.mixer.Sound.play(victorylevel2)
    #Placing background swaps into the loop for rendering backgrounds on subsequent levels
    if level_3_start:
        player.hp = 10
        pygame.time.set_timer(ADDENEMY, 0)
        level_2 = False
        enemies.empty()
        obstaclesprites.empty()
        obstructionsprites.empty()
        collectablesprites.empty()
        projectilesgroup.empty()
        playerprojectilesgroup.empty()
        endbackgroundgroup.empty()
        projectilesgroup.empty()
        playerprojectilesgroup.empty()
        enemyprojectilesgroup.empty()
        obstruction_entity_list = []
        collectable_entity_list = []
        populate_obstructions()
        populate_collections()
        bg_image = pygame.transform.scale(background_level_3, (SCREEN_WIDTH, SCREEN_HEIGHT))
        startbackground = Background("Assets/background_entrance_level_3.png", -720, 0)
        obstaclesprites.add(startbackground)
        endbackground = Background("Assets/background_exit_level_3.png", 21000, 0)
        endbackgroundgroup.add(endbackground)
        level_3_start = False
        Levelcounter = 3
        pygame.time.set_timer(ADDENEMY, 3000)
        pygame.mixer.Sound.play(victorylevel3)
    if boss_level_start:
        player.hp = 10
        pygame.time.set_timer(ADDENEMY, 0)
        level_3 = False
        enemies.empty()
        obstaclesprites.empty()
        obstructionsprites.empty()
        collectablesprites.empty()
        projectilesgroup.empty()
        playerprojectilesgroup.empty()
        enemyprojectilesgroup.empty()
        obstruction_entity_list = []
        collectable_entity_list = []
        bg_image = pygame.transform.scale(background_level_2, (SCREEN_WIDTH, SCREEN_HEIGHT))
        startbackground = Background("Assets/background_entrance_level_2.png", -720, 0)
        obstaclesprites.add(startbackground)
        endbackground = Background("Assets/background_exit_level_2.png", 21000, 0)
        obstaclesprites.add(endbackground)
        endbackgroundgroup.add(endbackground)
        boss_level_start = False
        Levelcounter = 4
        pygame.time.set_timer(ADDENEMY, 3000)
    #More setup for sidescrolling, resetting backgrounds if they move offscreen
    if bg_x_1 <= -SCREEN_WIDTH + camera_x:
        bg_x_1 = bg_x_2 + SCREEN_WIDTH
    if bg_x_2 <= -SCREEN_WIDTH + camera_x:
        bg_x_2 = bg_x_1 + SCREEN_WIDTH
    if bg_x_1 >= SCREEN_WIDTH + camera_x:
        bg_x_1 = bg_x_2 - SCREEN_WIDTH
    if bg_x_2 >= SCREEN_WIDTH + camera_x:
        bg_x_2 = bg_x_1 - SCREEN_WIDTH
    #Initialise pressing keys
    pressed_keys = pygame.key.get_pressed()
    #Update Projectiles
    projectilesgroup.update(playerposition)
    #Damaging collision detection
    if not gamelose:
        if pygame.sprite.spritecollideany(player, enemies):
            player.losehp()
        for enemyprojectile in enemyprojectilesgroup:
            if pygame.sprite.spritecollideany(player, enemyprojectilesgroup):
                player.losehp()
                enemyprojectile.kill()
    for enemy in enemies:
        if pygame.sprite.spritecollideany(enemy, playerprojectilesgroup):
            enemy.losehp()
    for playerprojectile in playerprojectilesgroup:
        if pygame.sprite.spritecollideany(playerprojectile, obstaclesprites):
            playerprojectile.kill()

    #Collectables collision
    for collectable in collectablesprites:
        if pygame.sprite.spritecollideany(player, collectablesprites):
            pygame.mixer.Sound.play(collectablesound)
            scorecounter += 2
            collectable.kill()
            #Play collectable sound**

    #Update enemies with playerposition
    enemies.update(playerposition)
    #Updates player on key press
    player.update(pressed_keys)
    #Clear screen
    screen.fill((0,0,0))

    #Modify backgrounds
    screen.blit(bg_image, (bg_x_1 - camera_x, 0))
    screen.blit(bg_image, (bg_x_2 - camera_x, 0))

    #Blit projectiles
    for bullet in projectilesgroup:
        screen.blit(bullet.surf, (bullet.rect.x - camera_x, bullet.rect.y))

    #Blit enemies
    for entity in obstaclesprites:
        screen.blit(entity.surf, (entity.rect.x - camera_x, entity.rect.y))

    #Blit player
    screen.blit(player.surf, (player.rect.x - camera_x, player.rect.y))

    #Score text blit
    score_surface = render_collectable_score(scorevalue)
    screen.blit(score_surface, (10, 20))

    #Player hp bar
    playerhpbar()

    #Spawn controls text
    if level_1:
        screen.blit(textcontrols, (SCREEN_WIDTH//2 - textcontrols.get_width()//2, 20))

    if gamewin:
        #Put in game end screen. Blit player onto level 3, in the middle, disable controls, surf victory text? VICTORY.
        text = font.render("You Win! Victory!", True, (255, 0, 0))
        text2 = font.render(f"Your score: {scorevalue}", True, (255, 0, 0))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
        screen.blit(text2, (SCREEN_WIDTH//2 - text2.get_width()//2, SCREEN_HEIGHT//2 + 40 - text2.get_height()//2))
        pygame.mixer.music.stop()
    if gamelose:
        text = font.render("Game Over. You died! Press Escape to exit.", True, (255, 0, 0))
        screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
        pygame.mixer.music.stop()
        pygame.time.set_timer(ADDENEMY, 0)


    #Updating the display
    pygame.display.flip()