import pygame
import time
import random

pygame.init()

'''constants'''

display_width=800
display_height=600

gameDisplay=pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('A Bit Racey')
game_clock=pygame.time.Clock()

black=(0,0,0)
white=(255,255,255)
green=(0,200,0)
bright_green=(0,255,0)
red=(200,0,0)
bright_red=(255,0,0)
blue=(0,0,250)

my_img=pygame.image.load('images/racecar2.png')
my_img=pygame.transform.scale(my_img,(90,90))
car_width=70
car_height=70
car_initial_x=display_width*0.44
car_initial_y=display_height*0.8


my_icon=pygame.image.load('images/car_icon3.png')
my_icon=pygame.transform.scale(my_icon,(32,34)).convert_alpha()
pygame.display.set_icon(my_icon)

pause=False
crash=False


crash_sound=pygame.mixer.Sound('soundeffects/crash.wav')
driving_sound=pygame.mixer.Sound('soundeffects/driving.wav')
intro_sound=pygame.mixer.Sound('soundeffects/frontend.wav')
pygame.mixer.music.load('soundeffects/live wires.mp3')
music_channel=pygame.mixer.Channel(1)


font_list=pygame.font.match_font('arial',bold=True,italic=True)
print(font_list)

'''constants'''

def quit_game():
    pygame.quit()
    quit()

def try_again():
    global crash
    crash=False
    pygame.mixer.music.play(-1)
    music_channel.set_volume(0.4)
    music_channel.play(driving_sound,-1)

def game_unpause():
    global pause
    pause=False
    pygame.mixer.music.unpause()
    music_channel.unpause()

def track_blocks_dodged(blocks):
    track_font=pygame.font.SysFont('elephant',italic=True,size=20)
    track_img=track_font.render("Dogded: "+str(blocks),True,black)
    track_img_rect=track_img.get_rect()
    gameDisplay.blit(track_img,track_img_rect)

def things(thingx,thingy,thingw,thingh,color):
    pygame.draw.rect(gameDisplay,color,[thingx,thingy,thingw,thingh])

def car(x,y):
    gameDisplay.blit(my_img,(x,y))

def text_objects(text,font):
    txt_image=font.render(text,True,black)
    txt_img_rect=txt_image.get_rect()
    return txt_image,txt_img_rect

def crashed():

    global crash
    crash=True


    pygame.mixer.music.stop()
    music_channel.stop()
    music_channel.play(crash_sound)
    
    crash_font=pygame.font.SysFont('arial',115)
    crash_surf,crash_rect=text_objects('You Crashed',crash_font)
    crash_rect.center=(display_width/2,display_height/2)
    gameDisplay.blit(crash_surf,crash_rect)

    while crash:

        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                pygame.quit()
                quit()

        
        create_button('Try Again',150,450,80,30,green,bright_green,try_again)
        create_button('QUIT',550,450,80,30,red,bright_red,quit_game)
        pygame.display.update()
        game_clock.tick(20)

    

def create_button(msg,x,y,w,h,ic,ac,action=None):
    mouse_xy=pygame.mouse.get_pos()
    mouse_buttons=pygame.mouse.get_pressed()

    if x<mouse_xy[0]<x+w and y<mouse_xy[1]<y+h:
        general_button_rect=pygame.draw.rect(gameDisplay,ac,(x,y,w,h))
        if(mouse_buttons[0]==1 and action!=None):
            action()
    else:
        general_button_rect=pygame.draw.rect(gameDisplay,ic,(x,y,w,h))

    button_font=pygame.font.SysFont('arial',bold=True,size=20)
    button_surf,button_rect=text_objects(msg,button_font)

    button_rect.center=general_button_rect.center
    gameDisplay.blit(button_surf,button_rect)


def game_pause():

    global pause
    
    pause=True

    pygame.mixer.music.pause()
    music_channel.pause()

    pause_font=pygame.font.SysFont('arial',115)
    pause_surf,pause_rect=text_objects('Paused!',pause_font)
    pause_rect.center=(display_width/2,display_height/2)
    gameDisplay.blit(pause_surf,pause_rect)

    while pause:

        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                pygame.quit()
                quit()

        create_button('Continue',150,450,80,30,green,bright_green,game_unpause)
        create_button('QUIT',550,450,80,30,red,bright_red,quit_game)

        pygame.display.update()
        game_clock.tick(20)
        

def game_intro():

    intro=True

    music_channel.play(intro_sound)

    gameDisplay.fill(white)
        
    intro_font=pygame.font.SysFont('elephant',italic=True,size=115)
    TextSurf,TextRect=text_objects('A Bit Racey',intro_font)
    TextRect.center=((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf,TextRect)

    while intro:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

        create_button('GO!',150,450,80,30,green,bright_green,game_loop)
        create_button('QUIT',550,450,80,30,red,bright_red,quit_game)
        
        pygame.display.update()
        game_clock.tick(15)


def game_loop():
    x_change=0
    game_exit=False
    car_x=car_initial_x
    car_y=car_initial_y
    thing_width=100
    thing_height=100
    thing_startx=random.randrange(0,display_width-int(thing_width))
    thing_starty=-600
    thing_speed=5
    dodged_blocks=0
    block_number=1

    pygame.mixer.music.play(-1)
    music_channel.set_volume(0.4)
    music_channel.play(driving_sound,-1)

    while not game_exit:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()

            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    x_change=-10

                elif event.key==pygame.K_RIGHT:
                    x_change=10

                elif event.key==pygame.K_p:
                    game_pause()

            elif event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    x_change=0

        car_x+=x_change
        
        gameDisplay.fill(white)
        track_blocks_dodged(dodged_blocks)
        car(car_x,car_y)
        things(thing_startx,thing_starty,thing_width,thing_height,blue)
        
        thing_starty+=thing_speed
        
        
        '''boundaries'''
        
        if car_x<=0 or display_width-car_x<=car_width:
            crashed()
            
            '''game_restart'''
            x_change=0
            gameDisplay.fill(white)
            car_x=car_initial_x
            car_y=car_initial_y
            car(car_x,car_y)
            thing_starty=-600
            thing_width=100
            thing_startx=random.randrange(0,display_width-thing_width)
            dodged_blocks=0
            thing_speed=5
            '''game_restart'''
            
        '''boundaries'''
        

        '''collision'''

        if(thing_starty+thing_height>car_y):
            if(car_x<=thing_startx+thing_width and thing_startx<=car_x+car_width):
                crashed()
                
                '''game_restart'''
                x_change=0
                gameDisplay.fill(white)
                car_x=car_initial_x
                car_y=car_initial_y
                car(car_x,car_y)
                thing_starty=-600
                thing_width=100
                thing_startx=random.randrange(0,display_width-thing_width)
                dodged_blocks=0
                thing_speed=5
            '''game_restart'''

        '''collision'''

        if display_height-thing_starty<=0:
            thing_starty=-thing_height
            thing_startx=random.randrange(0,display_width-int(thing_width))
            dodged_blocks+=1
            if(dodged_blocks%3==0):
                thing_speed+=1
                thing_width*=1.1
                block_number+=1

        
        
        pygame.display.update()
        game_clock.tick(60)


game_intro()
