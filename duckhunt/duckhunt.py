import sys, pygame, random
import sqlite3
import os

pygame.init()

size = width, height = 512, 450
screen = pygame.display.set_mode(size)

ground = pygame.Rect(0, 350, width, 100)

black = 0,0,0
white = 255,255,255
grass = 133, 233, 75

green = pygame.image.load("greenBird.png")
red = pygame.image.load("redBird.png")
blu = pygame.image.load("bluBird.png")
gDie = pygame.image.load("greenDie.png")
rDie = pygame.image.load("redDie.png")
bDie = pygame.image.load("bluDie.png")
gFall = pygame.image.load("greenFall.png")
rFall = pygame.image.load("redFall.png")
bFall = pygame.image.load("bluFall.png")
gFly = pygame.image.load("greenFly.png")
rFly = pygame.image.load("redFly.png")
bFly = pygame.image.load("bluFly.png")

g = [green, gDie, gFall, gFly]
r = [red, rDie, rFall, rFly]
b = [blu, bDie, bFall, bFly]
 
bullet = pygame.image.load("bullet.png")
bulletRect = bullet.get_rect()

bulletRect.y = height-bulletRect.height

dog = pygame.image.load("dogLaugh.png")
dogRect = dog.get_rect()
dogRect.x = width/2 - dogRect.width/2
dogRect.y = 350

dog2 = pygame.image.load("dogLaugh2.png")
dog2Rect = dog2.get_rect()
dog2Rect.x = width/2 - dog2Rect.width/2
dog2Rect.y = 350

class Bird:
    def __init__(self, img, speed):
        self.imgs = img
        self.img = img[0]
        self.imgRect = img[0].get_rect()
        self.imgRect.x = width/2
        self.imgRect.y = height/2
        self.speed = speed
        self.alive = True
        self.up = False

    def move(self):
        self.imgRect = self.imgRect.move(self.speed)

        if(self.alive==True and self.up==False):
            if self.imgRect.left < 0 or self.imgRect.right > width:
                self.speed[0] = -self.speed[0]
            if self.imgRect.top < 0 or self.imgRect.bottom>350:
                self.speed[1] = -self.speed[1]
            


    def hit(self, x, y):
        if(self.alive==True and x>=self.imgRect.x and x<=self.imgRect.x+self.imgRect.width and y>=self.imgRect.y and y<=self.imgRect.y+self.imgRect.width):
            self.img = self.imgs[1]
            self.alive = False
            

    def fall(self):
        self.img = self.imgs[2]
        self.speed = [0,6]
    
    def fly(self):
        self.img = self.imgs[3]
        self.speed = [0,-6]
    

#Starter Bird   
speedX = 2
speedY = 2
speed = [speedX, speedY]
duck = Bird(g, speed)
start_ticks=pygame.time.get_ticks()
shots = 3

score = 0

hits = 0
misses = 0

birds = 0
rounds = 1
total = 10*rounds

font = pygame.font.Font('freesansbold.ttf', 32) 
font2 = pygame.font.Font('freesansbold.ttf', 24) 

over=False

while over==False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN and (duck.alive==True and duck.up==False) :
            shots=shots-1
            x,y = pygame.mouse.get_pos()
            screen.fill(white)
            pygame.display.flip()
            pygame.time.delay(25)
            duck.hit(x,y)

            #Shot the duck
            if(duck.alive==False):
                hits+=1

                #Show background
                screen.fill(black)
                pygame.draw.rect(screen, grass, ground)

                #Show score
                text = font.render("Score: " + str(score), True, black, grass) 
                textRect = text.get_rect()  
                textRect.x = 0
                textRect.y = 400
                screen.blit(text, textRect) 

                #Show bird amount
                text = font2.render("Round " + str(rounds) + ": " + str(hits)+"/"+str(total), True, black, grass) 
                textRect = text.get_rect()  
                textRect.x = 0
                textRect.y = 375
                screen.blit(text, textRect) 

                #Show bullet
                bulletRect.x = 0
                for i in range(shots):
                    screen.blit(bullet, bulletRect)
                    bulletRect.x += bulletRect.width

                #Show duck
                screen.blit(duck.img, duck.imgRect)
                pygame.display.flip()
                pygame.time.delay(500)

                #Add score
                if(duck.img == gDie):
                    score+=500
                if(duck.img == bDie):
                    score+=1000
                if(duck.img == rDie):
                    score+=1500

                duck.fall()
            else:
                misses+=1

    

    #Timer
    seconds=(pygame.time.get_ticks()-start_ticks)/1000 
    if (seconds>8 and duck.alive==True) or (shots==0 and duck.alive==True):
        duck.up = True
        duck.fly()

    #Background
    screen.fill(black)
    pygame.draw.rect(screen, grass, ground)

    #Show Score
    text = font.render("Score: " + str(score), True, black, grass) 
    textRect = text.get_rect()  
    textRect.x = 0
    textRect.y = 400
    screen.blit(text, textRect) 


    #Show bird amount
    text = font2.render("Round " + str(rounds) + ": " + str(hits)+"/"+str(total), True, black, grass) 
    textRect = text.get_rect()  
    textRect.x = 0
    textRect.y = 375
    screen.blit(text, textRect)
    
    #Show bullets
    bulletRect.x = 0
    for i in range(shots):
        screen.blit(bullet, bulletRect)
        bulletRect.x += bulletRect.width

    duck.move()

    #Show duck
    screen.blit(duck.img, duck.imgRect)

    pygame.display.flip()
    pygame.time.delay(20)

    if(birds==total):
        if(hits-((rounds-1)*10)>=5):
            rounds+=1
            total=rounds*10
        else:
            over=True

    #Next Duck
    if((duck.alive==False or duck.up == True) and birds<total):

            
        if duck.imgRect.bottom>350 or duck.imgRect.bottom<0:
            
            if(duck.imgRect.bottom<0):
                for i in range(10):

                    #Background
                    screen.fill(black)

                    if(i%2==0):
                        screen.blit(dog2, dog2Rect)
                    else:
                        screen.blit(dog, dogRect)
                    dogRect.y-=dogRect.height/10
                    dog2Rect.y = dogRect.y

                    pygame.draw.rect(screen, grass, ground)

                    #Show Score
                    text = font.render("Score: " + str(score), True, black, grass) 
                    textRect = text.get_rect()  
                    textRect.x = 0
                    textRect.y = 400
                    screen.blit(text, textRect) 


                    #Show bird amount
                    text = font2.render("Round " + str(rounds) + ": " + str(hits)+"/"+str(total), True, black, grass) 
                    textRect = text.get_rect()  
                    textRect.x = 0
                    textRect.y = 375
                    screen.blit(text, textRect)
                    
                    #Show bullets
                    bulletRect.x = 0
                    for i in range(shots):
                        screen.blit(bullet, bulletRect)
                        bulletRect.x += bulletRect.width

                    pygame.display.flip()
                    pygame.time.delay(50)
                for i in range(5):

                    #Background
                    screen.fill(black)

                    if(i%2==0):
                        screen.blit(dog2, dog2Rect)
                    else:
                        screen.blit(dog, dogRect)

                    pygame.draw.rect(screen, grass, ground)

                    #Show Score
                    text = font.render("Score: " + str(score), True, black, grass) 
                    textRect = text.get_rect()  
                    textRect.x = 0
                    textRect.y = 400
                    screen.blit(text, textRect) 


                    #Show bird amount
                    text = font2.render("Round " + str(rounds) + ": " + str(hits)+"/"+str(total), True, black, grass) 
                    textRect = text.get_rect()  
                    textRect.x = 0
                    textRect.y = 375
                    screen.blit(text, textRect)
                    
                    #Show bullets
                    bulletRect.x = 0
                    for i in range(shots):
                        screen.blit(bullet, bulletRect)
                        bulletRect.x += bulletRect.width

                    pygame.display.flip()
                    pygame.time.delay(100)
                for i in range(10):

                    #Background
                    screen.fill(black)

                    if(i%2==0):
                        screen.blit(dog2, dog2Rect)
                    else:
                        screen.blit(dog, dogRect)
                    dogRect.y+=dogRect.height/10
                    dog2Rect.y=dogRect.y

                    pygame.draw.rect(screen, grass, ground)

                    #Show Score
                    text = font.render("Score: " + str(score), True, black, grass) 
                    textRect = text.get_rect()  
                    textRect.x = 0
                    textRect.y = 400
                    screen.blit(text, textRect) 


                    #Show bird amount
                    text = font2.render("Round " + str(rounds) + ": " + str(hits)+"/"+str(total), True, black, grass) 
                    textRect = text.get_rect()  
                    textRect.x = 0
                    textRect.y = 375
                    screen.blit(text, textRect)
                    
                    #Show bullets
                    bulletRect.x = 0
                    for i in range(shots):
                        screen.blit(bullet, bulletRect)
                        bulletRect.x += bulletRect.width

                    pygame.display.flip()
                    pygame.time.delay(50)





            birds += 1
            pygame.time.delay(20)
            chance = random.randint(0,1)
            if(chance==0):
                speedX = random.randint(abs(speedX),abs(speedX)+2)
                speedY = random.choice([-abs(speedY),abs(speedY)])
            if(chance==1):
                speedY = random.randint(abs(speedY), abs(speedY)+2)
                speedX = random.choice([-abs(speedX),abs(speedX)])
            speed = [speedX, speedY]

            print(speed)

            chance = random.randint(0,9)
            if(chance<=5):
                duck = Bird(g, speed)
            if(chance<=8 and chance>5):
                for i in range(len(speed)):
                    speed[i] = int(speed[i]*1.25)
                duck = Bird(b, speed)
            if(chance==9):
                for i in range(len(speed)):
                    speed[i] = int(speed[i]*1.5)
                duck = Bird(r, speed)
            start_ticks=pygame.time.get_ticks()
            shots = 3

#GAME ENDS

#Check if database exists
if not os.path.exists("scores.db"):
	conn = sqlite3.connect("scores.db")
	c = conn.cursor()

	c.execute("CREATE TABLE scores(score INT, hits INT, misses INT, accuracy REAL)")
	c.close()
	conn.commit()
	conn.close()
	print("Setup Complete")

#Begin normal program
conn = sqlite3.connect("scores.db")
c = conn.cursor()

# c.execute(".headers on")
# c.execute(".mode column")

if(hits+misses==0):
    accuracy = 0
else:
    accuracy = (hits/(hits+misses))*100

c.execute("INSERT INTO scores(score, hits, misses, accuracy) VALUES(?,?,?,?)", (score, hits, misses, accuracy))
conn.commit()

ide = 0
for row in c.execute("SELECT Count(*) FROM scores"):
    ide = row[0]
print(ide)

print("Your Score")
print("=====================")
for row in c.execute("SELECT rowid, * FROM scores WHERE rowid="+str(ide)):
    print("ID: "+str(row[0]))
    print("Score: "+str(row[1]))
    print("Hits: "+str(row[2]))
    print("Misses: "+str(row[3]))
    print("Accuracy: "+str(row[4]))

print("=====================")
print()
print("High Scores")
print("=====================")

print("rank \trowid \tscore \thits \tmisses \taccuracy")
r = 0
for row in c.execute("SELECT rowid, * FROM scores ORDER BY score DESC"):
    r+=1
    print(str(r)+"\t", end =" ")
    for i in row:
	    print(str(i)+"\t", end =" ")
    print()
    

    

    
    
    

