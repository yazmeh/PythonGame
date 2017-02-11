import pygame as pg
import time
from pygame.locals import *
import random;
pg.init();
d_height=600;
d_width=800;
sidewalk_width=150;

black=(0,0,0);
white=(255,255,255);
red=(255,0,0);
grey=(125,125,125);
green=(0,255,0);


gameDisplay=pg.display.set_mode((d_width,d_height));
pg.display.set_caption('PotHoles');
clock = pg.time.Clock();

carImg=pg.image.load('card.png');

def dodged_block(count):
    font =pg.font.SysFont(None,25);
    text=font.render("Dodged : " + str(count),True,black);
    gameDisplay.blit(text,(0,0));
def car(x,y):
    gameDisplay.blit(carImg,(x,y));

def crash():
    message_display('You Crashed');
    pg.display.update();
    time.sleep(2);
    game_loop();

def thing(thingx,thingy,thingw,thingh,color):
    pg.draw.rect(gameDisplay,color,[thingx,thingy,thingw,thingh]);
    
def message_display(text):
    largeText=pg.font.Font('Impact.TTF',100);
    textSurf,textRect = textObj(text,largeText,red);
    textRect.center=(d_width/2,d_height/2);
    gameDisplay.blit(textSurf,textRect);
   
    
def textObj(text,font,color):
    textSurf=font.render(text,True,color);
    return textSurf,textSurf.get_rect();

def strip(ty,color):
    y=6;
    for x in range(y):
        sx=d_width*.5-15;
        sy=ty+x*300;
        if sy>d_height:
            sy-=900;
            
        thing(sx,sy,30,200,color)
def game_loop():
    space=0;
    #car
    paused=False;
    x=d_width*0.45;
    y=d_height*0.8;
    cw=carImg.get_width();
    ch=carImg.get_height();
    xc=0;
    #blocks
    tx=random.randrange(sidewalk_width,d_width-sidewalk_width);
    ty=-600;
    block=[[tx,ty]];
    tw=75;
    th=75;
    ts=3;
    tcount=1;
    dodged=0;
    #strip
    stpy=-600;

    gameExit=False;
    while not gameExit:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit();
                quit()
                print('here');
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_LEFT:
                    xc=-5
                if event.key==pg.K_RIGHT:
                    xc=5
                if event.key==pg.K_p:
                    paused=True;
                if event.key==pg.K_q:
                    gameExit=True;
            if event.type==pg.KEYUP:
                if event.key==pg.K_LEFT or event.key==pg.K_RIGHT:
                    xc=0;
            

        x+=xc;
        gameDisplay.fill(grey);
        pg.draw.rect(gameDisplay,green,(0,0,sidewalk_width,d_height));
        pg.draw.rect(gameDisplay,green,(d_width-sidewalk_width,0,sidewalk_width,d_height));
        strip(stpy,white);
        car(x,y)
        dodged_block(dodged);
        stpy+=ts;
        
        for b in block:
            thing(b[0],b[1],tw,th,black);
            if y<b[1]+th and y>b[1]:
                if (x>b[0] and x<b[0]+tw) or (x+cw>b[0] and x+cw<b[0]+tw):
                    crash();
            
            if b[1]>d_height:
                b[1]=0-d_height;
                b[0]=random.randrange(sidewalk_width,d_width-sidewalk_width);
                dodged+=1;
                if dodged%3==0:
                    ts+=1;
                if dodged%5==0:
                    tcount+=1;
                space=0;
            b[1]+=ts;
        if space==50 and len(block)<tcount  :
            tx=random.randrange(sidewalk_width,d_width-sidewalk_width);
            ty=-600;
            block+=[[tx,ty]];
            space=0;
        if x>d_width-sidewalk_width-cw or x<sidewalk_width:
            crash();
            
        if stpy>d_height:
            stpy%=d_height;
            #stpy-=100;
        if paused:
            while paused:
                for event in pg.event.get():
                    if event.type==pg.KEYDOWN:
                        if event.key==pg.K_p:
                            paused=False;
        else:
            pg.display.update();
        space+=1;
        clock.tick(60);
        
game_loop();
pg.quit();
quit()
