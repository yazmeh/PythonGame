import pygame as pg
import time
from pygame.locals import *
import random;
import numpy
def save_hs(high):
     f = open("data.csv", "w");
     f.write("#high");        # column names
     numpy.savetxt(f, numpy.array([high]).T,fmt='int64');
def load_hs():
    high=numpy.loadtxt("data.csv", unpack=True);
    return high;
pg.init();
d_height=600;
d_width=800;
sidewalk_width=150;
maxscore=0;

black=(0,0,0);
white=(255,255,255);
red=(255,0,0);
dark_red=(200,0,0);
grey=(125,125,125);
green=(0,255,0);
dark_green=(0,200,0);
blue=(0,0,255);
dark_blue=(0,0,200);
resornew=3;
gameDisplay=pg.display.set_mode((d_width,d_height));
pg.display.set_caption('PotHoles');
clock = pg.time.Clock();

carImg=pg.image.load('card.png');

def save_hs(high):
     f = open("data", "w");
     f.write("#high");        # column names
     numpy.savetxt(f, numpy.array([high]).T);
def load_hs():
    high=numpy.loadtxt("data", unpack=True);
    return high;
def dodged_block(count):
    font =pg.font.SysFont(None,25);
    text=font.render("Dodged : " + str(count),True,black);
    gameDisplay.blit(text,(0,0));
def high_score(high):
    font =pg.font.SysFont(None,25);
    text=font.render("High Score : " + str(high),True,black);
    gameDisplay.blit(text,(d_width-sidewalk_width+10,0));
def car(x,y):
    gameDisplay.blit(carImg,(x,y));

def crash():
    message_display('You Crashed');
    pg.display.update();
    time.sleep(2);
    game_loop();

def thing(thingx,thingy,thingw,thingh,color):
    pg.draw.rect(gameDisplay,color,[thingx,thingy,thingw,thingh]);
    
def message_display(text,color=red):
    largeText=pg.font.Font('Impact.TTF',100);
    textSurf,textRect = textObj(text,largeText,color);
    textRect.center=(d_width/2,d_height/2);
    gameDisplay.blit(textSurf,textRect);

def label(text,cpos,size):
    smallText=pg.font.Font('Comic.TTF',size);
    textSurf,textRect = textObj(text,smallText,black);
    textRect.center=(cpos[0],cpos[1]);
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
def resume():
    global resornew;
    resornew=1;
def newStart():
    global resornew;
    resornew=2;
def quit_game():
    save_hs(maxscore);
    pg.quit();
    quit();
def button_func(msg,pos,size,color1,color2=None,func=None):
    mouse=pg.mouse.get_pos();
    click=pg.mouse.get_pressed();
    global resornew;
    if pos[0]+size[0]>mouse[0]>pos[0] and pos[1]<mouse[1]<pos[1]+size[1]: 
        pg.draw.rect(gameDisplay,color1,pos+size);
        if click[0]==1 and func!=None:
            func();
    else:
        if color2==None:
            color=color1;
        else:
            color=color2;
        pg.draw.rect(gameDisplay,color,pos+size);
    label(msg,(pos[0]+size[0]/2,pos[1]+size[1]/2),25);

def game_menu(gameOn=False):
    global resornew;
    menu=True;
    mspace=75;
    mh=50;
    mw=150;
    mx=d_width/2-mw/2;
    my=d_height/2+mspace;
    c=0;
    while menu:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit();
                quit();
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_p:
                    menu=False;
        gameDisplay.fill(white);
        mouse=pg.mouse.get_pos();

        if gameOn:
            message_display('Paused',black);
            button_func('Resume',(mx,my+c*mh),(mw,mh),blue,dark_blue,resume);
            c+=1;
        else:
            message_display('PotHoles',black);
            
        button_func('New Game',(mx,my+c*mh),(mw,mh),green,dark_green,newStart);
        c+=1;
        button_func('Quit',(mx,my+c*mh),(mw,mh),red,dark_red,quit_game);
        c=0;
        if resornew==1:
            resornew=3;
            menu=False;
            return False;
        elif resornew==2:
            resornew=3;
            game_loop();
            menu=False;
            return True;
    
        pg.display.update();
        clock.tick(60);
        
def game_loop():
    global maxscore;
    space=0;
    #car
    c_speed=6;
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
    ts=4;
    tcount=1;
    dodged=0;
    #strip
    stpy=-600;

    gameExit=False;
    while not gameExit:
        for event in pg.event.get():
            if event.type==pg.QUIT:
                pg.quit();
                quit();
                print('here');
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_LEFT:
                    xc=0-c_speed;
                if event.key==pg.K_RIGHT:
                    xc=c_speed;
                if event.key==pg.K_UP:
                    ts+=3;
                if event.key==pg.K_p:
                    paused=True;
                if event.key==pg.K_q:
                    quit_game();
            if event.type==pg.KEYUP:
                if event.key==pg.K_LEFT or event.key==pg.K_RIGHT:
                    xc=0;
                if event.key==pg.K_UP:
                    ts-=3;
            

        x+=xc;
        gameDisplay.fill(grey);
        pg.draw.rect(gameDisplay,green,(0,0,sidewalk_width,d_height));
        pg.draw.rect(gameDisplay,green,(d_width-sidewalk_width,0,sidewalk_width,d_height));
        strip(stpy,white);
        car(x,y)
        dodged_block(dodged);
        high_score(maxscore);
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
                if maxscore<dodged:
                    maxscore=dodged;
            b[1]+=ts;
        if space==30 and len(block)<tcount  :
            tx=random.randrange(sidewalk_width,d_width-sidewalk_width);
            ty=-600;
            block+=[[tx,ty]];
            space=0;
        if x+cw>d_width-sidewalk_width or x<sidewalk_width:
            crash();
        if stpy>d_height:
            stpy%=d_height;
            #stpy-=100;
        if paused:
            nStart=game_menu(True);
            if nStart:
                gameExit=True;
            paused=False;
        pg.display.update();
        space+=1;
        clock.tick(60);
        
game_menu()
game_loop();

quit_game();
