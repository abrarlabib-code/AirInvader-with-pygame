def invade():
    import pygame
    import random
    from pygame import mask,Mask
    pygame.init()

    blt = pygame.image.load("bul.png")
    myplane = pygame.image.load("myplaneforgame.png")
    enemy1 = pygame.image.load("enemy1.png")
    enemy2 = pygame.image.load("enemy2.png")
    enemy3 = pygame.image.load("enemy3.png")
    pics = [myplane,enemy1,enemy2,enemy3] 
    gameon = True


    win = pygame.display.set_mode((900,750))
    pygame.display.set_caption("AirInvaders")
    clock = pygame.time.Clock()

    #elements
    shots = []
    enemies =[]
    enemyshots = []
    shotloop = 0
    enemyloop = 1

    class button:
        def __init__(self,x,y,width,height,textcolor,buttoncolor,text=""):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.textcolor = textcolor
            self.buttoncolor = buttoncolor
            self.text = text
        
        def draw(self,win):
            pygame.draw.rect(win,self.buttoncolor,(self.x,self.y,self.width,self.height))
            fnt = pygame.font.SysFont("comicsens",30)
            bttxt = fnt.render(self.text,1,self.textcolor)
            win.blit(bttxt,(self.x+(self.width/2 -bttxt.get_width()/2),self.y+(self.height/2 - bttxt.get_height()/2)))
        
        def overbutton(self,pos):
            if pos[0] < self.x + self.width and pos[0] > self.x :
                if pos[1] < self.y + self.height and pos[1] > self.y:
                    return True


    class plane:
        score = 0
        def __init__(self,x,y,width,height,pic):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.pic = pic
            self.visible = True
            self.health = 30
            self.vel = 5
            self.firevel = 10
            self.mask = pygame.mask.from_surface(self.pic)
            self.hitbox1 = (self.x+25,self.y,self.width-50,self.height)
            self.hitbox2 = (self.x,self.y+10,self.width,self.height-30)

        def shootenemy(self,objs):
            for shot in shots:
                shot.y -= self.firevel
                if shot.y <= 0:
                    shots.remove(shot)
                else:
                    for obj in objs:
                        if shot.hit(obj):
                            objs.remove(obj)
                            if shot in shots:
                                shots.remove(shot)

        def gothit(self):
            for reshot in enemyshots:
                if collied(self,reshot):
                    enemyshots.remove(reshot)
                    self.health -= 2
            

        def showhealth(self):
            pygame.draw.rect(win,(0,0,255),(self.hitbox1[0]-6 ,self.hitbox1[1]+50,30,5))
            if self.health > 0:
                pygame.draw.rect(win,(255,0,0),(self.hitbox1[0]-6 ,self.hitbox1[1]+50,self.health,5))

        def showscore(self):
            font = pygame.font.SysFont("comicsens",30,True)
            scrtxt = font.render("Score:"+str(self.score),1,(0,0,0))
            win.blit(scrtxt,(100,0))

        def checkhit(self):
            if self.height <= 0:
                return True

        def draw(self,win):
            self.hitbox1 = (self.x+25,self.y,self.width-50,self.height)
            self.hitbox2 = (self.x,self.y+10,self.width,self.height-30)
            if self.visible:
                win.blit(self.pic,(self.x,self.y))
            # pygame.draw.rect(win,(255,0,0),self.hitbox1,2) #body
            # pygame.draw.rect(win,(255,0,0),self.hitbox2,2) #wing
        

    class attacker:
        enemyshotloop = 0
        def __init__(self,x,y,width,height,pic):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.pic = pic
            self.mask = pygame.mask.from_surface(self.pic)
            self.visible = True
            if self.pic == pics[1]:
                self.vel = 1
                self.firevel = 10
                self.hitbox1 = (self.x+20,self.y,self.width-40,self.height)
                self.hitbox2 = (self.x,self.y+25,self.width,self.height-35)
            if self.pic == pics[2]:
                self.vel = 1
                self.firevel = 10
                self.hitbox1 = (self.x+25,self.y,self.width-40,self.height-5)
                self.hitbox2 = (self.x,self.y+21,self.width+12,self.height-30)
            if self.pic == pics[3]:
                self.vel = 1
                self.firevel = 10
                self.hitbox1 = (self.x+20,self.y,self.width-30,self.height)
                self.hitbox2 = (self.x,self.y+25,self.width,self.height-35)
        def draw(self,win):
            if self.pic == pics[1]:
                self.hitbox1 = (self.x+20,self.y,self.width-40,self.height)
                self.hitbox2 = (self.x,self.y+25,self.width,self.height-35)
            if self.pic == pics[2]:
                self.hitbox1 = (self.x+25,self.y,self.width-40,self.height-5)
                self.hitbox2 = (self.x,self.y+21,self.width+12,self.height-30)
            if self.pic == pics[3]:
                self.hitbox1 = (self.x+20,self.y,self.width-30,self.height)
                self.hitbox2 = (self.x,self.y+25,self.width,self.height-35)
            if self.visible:
                win.blit(self.pic,(self.x,self.y))
                # pygame.draw.rect(win,(255,0,0),self.hitbox1,2) #body
                # pygame.draw.rect(win,(255,0,0),self.hitbox2,2) #wing

        def gothit(self):  
            for shot in shots:
                if collied(self,shot):
                    enemies.remove(self)
                    shots.remove(shot)
                    defender.score += 1

            if collied(self,defender):
                enemies.remove(self)
                defender.health -= 10
        
        def shootloop(self):
            if self.enemyshotloop > 0:
                self.enemyshotloop +=1
            if self.enemyshotloop > 100:
                self.enemyshotloop = 0

        def shootdefender(self):
            self.shootloop()
            enemybul = fire(self.hitbox1[0]+10,self.hitbox1[1]+self.hitbox1[3])
            if self.enemyshotloop==0:
                enemyshots.append(enemybul)
                self.enemyshotloop = 1



    class fire:
        def __init__(self,x,y):
            self.x = x
            self.y = y
            self.img = blt
            self.mask = pygame.mask.from_surface(self.img)
        
        def hit(self,obj):
            return collied(self,obj)
        
        def draw(self,win):
            win.blit(self.img,(self.x,self.y-10))


    def collied(obj1,obj2):
        offsetx = obj1.x - obj2.x
        offsety = obj1.y - obj2.y
        return obj2.mask.overlap(obj1.mask,(offsetx,offsety)) != None
    

    class disp_txt:
        def __init__(self,text,time,destination):
            self.text = text
            self.time = time
            self.destination = destination            
            self.shfnt = pygame.font.SysFont("comicsens",30,False)
            self.shtxt = self.shfnt.render(self.text,0,(255,0,0))


        def draw(self,win):
            if self.time>0:
                win.blit(self.shtxt,self.destination)
            self.time -= 1


    #fonts
    overfnt = pygame.font.SysFont("comicsens",80,True)
    overtxt = overfnt.render("Game Over",1,(0,0,0))
    overscrfnt = pygame.font.SysFont("comicsens",50,True)

    #gamedrawwindowfunction
    def gamedraw():
        win.fill((0,255,255))
        if gameon:
            hint.draw(win)
            defender.draw(win)            
            defender.gothit()
            defender.showhealth()
            defender.showscore()
            for enemy in enemies:
                enemy.draw(win)
                enemy.y += enemy.vel
                enemy.gothit()
                k = random.choice([0,1,1])
                if k == 1:
                    enemy.shootdefender()

            for reshot in enemyshots:
                reshot.draw(win)
                reshot.y += 10

            for shot in shots:
                shot.draw(win)
                shot.y -= defender.firevel

        if gameon == False:
            win.fill((255,255,0))
            win.blit(overtxt,(250,200))
            overscrtxt = overscrfnt.render("Score:"+" "+str(defender.score),1,(255,0,0))
            win.blit(overscrtxt,(320,300))
            plybutton.draw(win)
        
        backbutton.draw(win)   

        pygame.display.update()

    #objs and fonts
    defender = plane(430,660,70,45,pics[0])
    backbutton = button(0,0,60,30,(255,255,255),(255,0,0),"quit")
    plybutton = button(300,650,200,60,(255,255,255),(0,0,0),"play again")
    hint = disp_txt("Tap SPACE-BAR/UP to fire, Tap LEFT/RIGHT to move respective direction",100,(100,400))

    fighting = True

    while fighting:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backbutton.overbutton(pos):
                    fighting = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if plybutton.overbutton(pos):
                    fighting = False
                    invade()

        if keys[pygame.K_ESCAPE]:
            fighting = False

        if gameon:

            atkr = attacker(random.randrange(0,840),-10,59,49,pics[random.randrange(1,4)])
            bullet = fire(defender.hitbox1[0] + 8, defender.hitbox1[1])

            for enemy in enemies:
                if enemy.y + enemy.hitbox1[2] > 750:
                    pygame.time.delay(1750)
                    gameon = False

            if defender.health <=0:
                defender.visible = False
                pygame.time.delay(1750)
                gameon = False

            if enemyloop > 0:
                enemyloop+=1
            if enemyloop > 95:
                enemyloop = 1

            if shotloop > 0:
                shotloop +=1
            if shotloop > 20:
                shotloop = 0
            
            if keys[pygame.K_LEFT] and defender.x > 0 :
                defender.x -= defender.vel

            if keys[pygame.K_RIGHT] and defender.x + defender.hitbox2[3] + 50 < 900:
                defender.x += defender.vel

            if enemyloop == 95:
                enemies.append(atkr)

            if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and shotloop == 0 and len(shots) < 10:
                defender.shootenemy(enemies)
                shots.append(bullet)
                shotloop = 1
            
        
                


        gamedraw()

if __name__ =='__main__':
    invade()
