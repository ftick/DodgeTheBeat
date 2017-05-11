import pygame, random, sys, time, math

'''
TODO
- implement scrolling projectiles
- implement projectile detection
- implement obstacles
- implement obstacle detection
'''

# Classes

# X VALS FOR RAILS: [125, 275, 425, 575, 725]

r = [125,275,425,575,725]

class Player:
    def __init__(self, rail, img):
        self.rail = rail-1
        self.eks = r[self.rail]
        self.wai = HEIGHT - 125
        self.img = img

    def left(self):
        if(self.rail!=0):
            self.rail-=1
        self.eks = r[self.rail]

    def right(self):
        if(self.rail!=4):
            self.rail+=1
        self.eks = r[self.rail]

class Obstacle:
    def __init__(self, rail):
        self.eks = r[rail]+25

# Pygame boilerplate
pygame.init()
WIDTH = 900
HEIGHT = 600
FPS = 60
size = [WIDTH, HEIGHT]
screen = pygame.display.set_mode(size)
title = "Platformer"
pygame.display.set_caption(title)
clock = pygame.time.Clock()

# Music

pygame.mixer.init()
pygame.mixer.music.load('Audio/song.ogg')
pygame.mixer.music.play(0, 0.0)

# Song settings

bpm = 497.0

early = HEIGHT-160
late = HEIGHT-70

beatTime = 121

points = [43, 51, 53, 55, 63, 65, 67, 79, 83, 87, 91, 99, 101, 103, 111, 115, 121, 123, 125, 127, 131, 139, 147, 149, 151, 159, 161, 163, 175, 179, 183, 187, 195, 197, 199, 207, 209, 211, 217, 219, 221, 223, 231, 235, 241, 247, 267, 269, 271, 277, 280, 283, 289, 291, 293, 295, 299, 303, 305, 307, 313, 315, 319, 323, 327, 331, 333, 335, 343, 345, 347, 353, 355, 357, 359, 365, 367, 369, 371, 377, 379, 385, 387, 391, 395, 403, 409, 411, 415, 419, 427, 435, 437, 439, 447, 449, 451, 461, 463, 467, 471, 475, 483, 485, 487, 495, 499, 505, 507, 509, 511, 519, 523, 531, 533, 535, 543, 545, 547, 559, 563, 567, 571, 579, 581, 583, 591, 593, 595, 603, 605, 607, 611, 615, 619, 627, 629, 631, 637, 641, 643, 645, 647, 665, 667, 669, 671, 675, 679, 683, 687, 691, 695, 697, 703, 707, 711, 715, 721, 723, 727, 733, 735, 737, 739, 741, 743, 759, 761, 765, 775, 779, 783, 784, 785, 786, 787, 795, 797, 799, 803, 807, 809, 811, 815, 819, 821, 823, 827, 831, 835, 839, 843, 845, 847, 855, 857, 859, 865, 867, 869, 871, 879, 883, 891, 893, 895, 903, 905, 907, 911, 915, 919, 923, 927, 931, 935, 939, 941, 943, 947, 951, 953, 955, 963, 969, 971, 973, 975, 977, 979, 987, 989, 991, 995, 999, 1001, 1003, 1009, 1013, 1015, 1019, 1023, 1027, 1031, 1035, 1037, 1039, 1045, 1047, 1051, 1057, 1059, 1061, 1063, 1071, 1075, 1079, 1083, 1085, 1087, 1091, 1095, 1097, 1099, 1103, 1107, 1111, 1115, 1119, 1123, 1131, 1133, 1135, 1143, 1145, 1147, 1155, 1157, 1159, 1165, 1167, 1171, 1183, 1195, 1211, 1215, 1219]
    
pointNum = len(points)

# Main game
def game():

    # Sound objects

    beats = [False] * 1250
    for p in points:
        beats[p] = True
    
    # Make player
    player_img = pygame.image.load("Graphics/sprite.png")
    player_img = pygame.transform.scale(player_img,(50,50))
    player = Player(3, player_img)
    GROUND = HEIGHT - 150

    BEAT = 0
    UPDATE_BEAT = pygame.USEREVENT + 2
    UPDATE_FRAME = pygame.USEREVENT + 3
    pygame.time.set_timer(UPDATE_BEAT, beatTime)
    pygame.time.set_timer(UPDATE_FRAME, 10)
    currentTime = pygame.time.get_ticks()

    scr = []
    obs = []

    health = 400.0
    
    # Game loop
    while health > 0 and BEAT < 1250:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                # Alternative close
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                # Movement
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    move = False
                    for y in range(len(scr)):
                        if(scr[y][0] >= early and scr[y][0] <= late):
                            move = True
                            scr[y][1] = 1
                            continue
                    if(move):
                        player.left()
                    else:
                        health-=10
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    move = False
                    for y in range(len(scr)):
                        if(scr[y][0] >= early and scr[y][0] <= late):
                            move = True
                            scr[y][1] = 1
                            continue
                    if(move):
                        player.right()
                    else:
                        health-=10
            if event.type == UPDATE_BEAT:
                if(beats[BEAT]):
                    # Add new beat to screen
                    scr.append([100,0])
                    obs.append([100,Obstacle(random.randint(0,4))])
                BEAT += 1
            if event.type == UPDATE_FRAME:
                # Make Shit Fall
                for i in range(len(scr)):
                    scr[i][0] += 5
                for i in range(len(obs)):
                    obs[i][0] += 5
                
                rem = []
                rem2 = []
                
                for i in range(len(scr)):
                    if(scr[i][0]) > 600:
                        rem.append([i])
                for i in range(len(obs)):
                    if(obs[i][0]) > 600:
                        rem2.append([i])
                
                for i in range(len(rem)):
                    scr.remove(scr[i])
                for i in range(len(rem2)):
                    obs.remove(obs[i])

                for i in range(len(scr)):
                    if scr[i][0] >= HEIGHT-60 and scr[i][1] == 0:
                        scr[i][1] = -1
        
        # Update display
        
        pygame.draw.rect(screen, (0,0,0), pygame.Rect((0,0),(WIDTH,HEIGHT)))
        
        # Testing rects
        pygame.draw.rect(screen, (64,64,64), pygame.Rect((0,0),(125,HEIGHT)))
        pygame.draw.rect(screen, (64,64,64), pygame.Rect((775,0),(WIDTH,HEIGHT)))
        #pygame.draw.rect(screen, (64,64,64), pygame.Rect((0,HEIGHT - 100),(WIDTH,HEIGHT)))
        pygame.draw.rect(screen, (64,64,64), pygame.Rect((0,HEIGHT-105),(WIDTH, 10)))
        
        # Rail rects
        for i in range(0,5):
            pygame.draw.rect(screen, (0,25,25), pygame.Rect( ((145 + 150*i),0),((10),HEIGHT) ))

        pygame.draw.rect(screen, (64,64,64), pygame.Rect((0,HEIGHT-105),(WIDTH, 10)))
        screen.blit(player.img, (player.eks, player.wai))
        
        # Beat rects
        for y in range(len(scr)):
            if scr[y][0] < early:
                pygame.draw.rect(screen, (255,255,255), pygame.Rect( (125,scr[y][0]-5),(650,10) ))
            elif scr[y][1] == 0 and scr[y][0] < late:
                pygame.draw.rect(screen, (255,255,255), pygame.Rect( (125,scr[y][0]-5),(650,10) ))
            elif scr[y][1] == -1:
                health -= 7
                scr[y][1] = 0
                pygame.draw.rect(screen, (255,0,0), pygame.Rect( (125,scr[y][0]-5),(650,10) ))
            elif scr[y][1] == 0:
                pygame.draw.rect(screen, (255,0,0), pygame.Rect( (125,scr[y][0]-5),(650,10) ))
            elif scr[y][1] == 1:
                health += 0.3
                if(health>400): health=400
                pygame.draw.rect(screen, (120,195,130), pygame.Rect( (125,scr[y][0]-5),(650,10) ))

        if(health>200):
            pygame.draw.rect(screen, (0,255,0), pygame.Rect( (250, 25),(health,50) ))
        elif(health>100):
            pygame.draw.rect(screen, (255,255,0), pygame.Rect( (250, 25),(health,50) ))
        else:
            pygame.draw.rect(screen, (255,0,0), pygame.Rect( (250, 25),(health,50) ))
        
        # Obstacle rects
        #for y in range(len(obs)):
            #pygame.draw.rect(screen, (150,150,150), pygame.Rect( (obs[y][1].eks-25,obs[y][0])-25,(50,50) ) )
        
        pygame.display.flip()
        clock.tick(FPS)
        
game()

pygame.quit()
sys.exit(0)
