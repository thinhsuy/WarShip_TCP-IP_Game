import socket
import getpass #dùng để che mật khẩu lại *****
import MySQL
import player
import Caesar
import time
import pygame
import os
import threading
from tkinter import *
from tkinter import font
from PIL import ImageTk, Image
from tkcalendar import *
from tkinter import messagebox

clear = lambda: os.system('cls')
clear()

PORT = 5500
#HOST = "172.20.10.7"
host = input("Input server game: ")
if (host == "default"): HOST = socket.gethostbyname(socket.gethostname())
else: HOST = host
SIZE = 1024
FORMAT = "utf-8"
ADDR = (HOST,PORT)

client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(ADDR)

"""NGUYEN DUY THINH"""
user = "none"
cmd = "none"
turn = True
hallcmd = -1
glb_idr_create = 0
glb_idr_join = 0
invite_friend = "none"
player1 = "player 1"
player2 = "player 2"
ready_btn = "waiting"
hoster = False
loading_percent = 0
check_room = "None"
check_mess = "None"
done = False
game_on = False
exitt = False
valid = True

glb_username = "Finding..."
glb_fullname = "Finding..."
glb_phone = "Finding..."
glb_dob = "Finding..."
glb_gender = "Finding..."
glb_gameplayed = "Finding..."
glb_win = "Finding..."
glb_lost = "Finding..."
glb_online = "Finding..."
glb_input = "None"
glb_run = True
glb_exitRoom = False
BLOCKNUMB = 10
Map1 = [["0.0" for i in range(BLOCKNUMB)] for j in range(BLOCKNUMB)] 
Map2 = [["0.0" for i in range(BLOCKNUMB)] for j in range(BLOCKNUMB)]



def send(msg):
    client.send(msg.encode(FORMAT))

def receive():
    return client.recv(SIZE).decode(FORMAT)

def freeGlobalVar():
    global cmd ,turn ,hallcmd, glb_idr_create, glb_idr_join, invite_friend
    global player1, player2, ready_btn, hoster, loading_percent, check_room, check_mess
    global glb_username, glb_fullname, glb_phone, glb_dob, glb_gender, glb_gameplayed, glb_win
    global glb_lost, glb_online, glb_input, glb_run, glb_exitRoom
    cmd = "none"
    turn = True
    hallcmd = -1
    glb_idr_create = 0
    glb_idr_join = 0
    invite_friend = "none"
    player1 = "player 1"
    player2 = "player 2"
    ready_btn = "waiting"
    hoster = False
    loading_percent = 0
    check_room = "None"
    check_mess = "None"
    glb_username = "Finding..."
    glb_fullname = "Finding..."
    glb_phone = "Finding..."
    glb_dob = "Finding..."
    glb_gender = "Finding..."
    glb_gameplayed = "Finding..."
    glb_win = "Finding..."
    glb_lost = "Finding..."
    glb_online = "Finding..."
    glb_input = "None"
    glb_run = True
    glb_exitRoom = False

class ThreadReturn(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                                 **self._kwargs)
    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return

"""THINH INTERFACE"""
WHITE = (255,255,255)

def hideText(screen, x, y, color):
    rect = pygame.Rect(x, y, 300, 50)
    pygame.draw.rect(screen, color, rect)
def Text(screen, msg, x, y, color):
    font = pygame.font.Font(None, 32)
    screen.blit(font.render(msg, True, color), (x, y))
def drawImg(screen, string, x, y):
    rect = string.get_rect(center=(x, y))
    screen.blit(string, rect)
def drawRect(screen, x, y, width, height, color):
    box = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, color, box)

def CreateRoom_interface(screen):
    base_font = pygame.font.Font(None, 32)
    user_text = ''
    idr_text = 'none'

    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')

    user_color = color_passive
    idr_color = color_passive
    user_active = False
    idr_active = False
    running = True

    idr_rect = pygame.Rect(600, 260, 100, 35)
    user_rect = pygame.Rect(200, 150, 100, 35)

    bg = pygame.image.load('asset/semiRoom.png').convert()
    drawImg(screen, bg, 500, 250)

    running = True
    global invite_friend
    global glb_idr_create
    global valid
    global glb_exitRoom
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (user_active): user_color=color_active
        else: user_color=color_passive
        if (idr_active): idr_color=color_active
        else: idr_color=color_passive
        Text(screen, "PLEASE INSERT ID ROOM", 200, 100, WHITE)
        Text(screen, "Inivite friend or not?", 550, 200, WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                return False
            if ((mouse_x>200 and mouse_x<300 and mouse_y>150 and mouse_y<185) 
                or 
                (mouse_x>600 and mouse_x<700 and mouse_y>260 and mouse_y<295)
                or
                (mouse_x>865 and mouse_x<930 and mouse_y>125 and mouse_y<470)
                ):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                try:
                    glb_idr_create = int(user_text)
                    invite_friend = idr_text
                    time.sleep(0.5)
                    if (valid==False): 
                        Text(screen, "Invalid value!", 850, 100, (0,0,0))
                    else:
                        running = False
                        return True
                except:   
                    Text(screen, "Invalid value!", 850, 100, (0,0,0))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1 and mouse_x>200 and mouse_x<300 and mouse_y>150 and mouse_y<185:
                    if (user_active): user_active=False
                    else: 
                        idr_active = False
                        user_active=True
                elif event.button==1 and mouse_x>600 and mouse_x<700 and mouse_y>260 and mouse_y<295:
                    if (idr_active): idr_active=False
                    else: 
                        user_active = False
                        idr_active=True
                elif (event.button==1 and mouse_x>865 and mouse_x<930 and mouse_y>125 and mouse_y<470):
                    glb_exitRoom = True   
                    running = False
                    return False
            elif (event.type == pygame.KEYDOWN and user_active==True):
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
            elif (event.type == pygame.KEYDOWN and idr_active==True):
                if event.key == pygame.K_BACKSPACE:
                    idr_text = idr_text[:-1]
                else:
                    idr_text += event.unicode
        pygame.draw.rect(screen, user_color, user_rect)
        user_surface = base_font.render(user_text, True, WHITE)
        screen.blit(user_surface, (user_rect.x+5, user_rect.y+5))
        user_rect.w = max(100, user_surface.get_width()+10)

        pygame.draw.rect(screen, idr_color, idr_rect)
        idr_surface = base_font.render(idr_text, True, WHITE)
        screen.blit(idr_surface, (idr_rect.x+5, idr_rect.y+5))
        idr_rect.w = max(100, idr_surface.get_width()+10)

        pygame.display.flip()

def JoinRoom_interface(screen):
    base_font = pygame.font.Font(None, 32)
    user_text = ''

    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')

    user_color = color_passive
    user_active = False
    running = True

    user_rect = pygame.Rect(200, 150, 100, 35)

    bg = pygame.image.load('asset/semiRoom.png').convert()
    drawImg(screen, bg, 500, 250)

    running = True
    global glb_idr_join
    global valid
    global glb_exitRoom
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (user_active): user_color=color_active
        else: user_color=color_passive
        Text(screen, "PLEASE INSERT ID ROOM", 200, 100, WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                return False
            if ((mouse_x>200 and mouse_x<300 and mouse_y>150 and mouse_y<185) 
                or
                (mouse_x>865 and mouse_x<930 and mouse_y>125 and mouse_y<470)
                ):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                try:
                    glb_idr_join = int(user_text)
                    time.sleep(0.5)
                    if (valid==False): 
                        Text(screen, "Invalid value!", 850, 100, (0,0,0))
                    else:
                        running = False
                        return True
                except:
                    Text(screen, "Invalid value!", 850, 100, (0,0,0))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==1 and mouse_x>200 and mouse_x<300 and mouse_y>150 and mouse_y<185:
                    if (user_active): user_active=False
                    else: 
                        user_active = True
                elif (event.button==1 and mouse_x>865 and mouse_x<930 and mouse_y>125 and mouse_y<470):
                    glb_exitRoom = True   
                    running = False
                    return False
            elif (event.type == pygame.KEYDOWN and user_active==True):
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
        pygame.draw.rect(screen, user_color, user_rect)
        user_surface = base_font.render(user_text, True, WHITE)
        screen.blit(user_surface, (user_rect.x+5, user_rect.y+5))
        user_rect.w = max(100, user_surface.get_width()+10)

        pygame.display.flip()

def Room_interface(screen):
    pygame.display.set_caption("WAITING ROOM")
    BLUE1 = (142, 202, 230)
    BLUE2 = (33, 158, 188)
    BLUE3 = (2, 48, 71)
    YELLOW = (255, 183, 3)
    ORANGE = (251, 133, 0)
    WHITE = (255, 255, 255)
    GRAY = (125,125,125)
    screen.fill(BLUE3)

    player1_rect=pygame.Rect(50,20,350,400)
    pygame.draw.rect(screen, YELLOW, player1_rect,0,20)
    player2_rect=pygame.Rect(600,20,350,400)
    pygame.draw.rect(screen,YELLOW,player2_rect,0,20)
    loading=pygame.Rect(400,45,200,350)
    pygame.draw.rect(screen,BLUE2,loading,0)
    Exit = pygame.Rect(420, 420, 160, 60)
    pygame.draw.rect(screen,GRAY,Exit,0,25)

    nameplayer1=pygame.Rect(50,440,350,45)
    pygame.draw.rect(screen,ORANGE,nameplayer1,0,20)
    nameplayer2=pygame.Rect(600,440,350,45)
    pygame.draw.rect(screen,ORANGE,nameplayer2,0,20)

    imgplayer1 = pygame.image.load('asset/1.png').convert()
    img_rectplayer1 = imgplayer1.get_rect(center=(220,220))
    imgplayer2 = pygame.image.load('asset/2.png').convert()
    img_rectplayer2 = imgplayer2.get_rect(center=(775,220))
    

    nameofplayer1="Player 1"
    nameofplayer2="Player 2"
    textloading="Loading"
    textExit = "Exit"
    font=pygame.font.SysFont('serif',28,5)
    fontload=pygame.font.SysFont('serif',32,1)
    fontper=pygame.font.SysFont('serif',40,1)
    fontrea=pygame.font.SysFont('serif',25,1)
    textloading=fontload.render(textloading, True, WHITE)
    
    textExit=fontrea.render(textExit, True, BLUE1)
    screen.blit(textloading,(445,140))
    screen.blit(textExit, (475, 435))
    
    global ready_btn
    global player1
    global player2
    global loading_percent

    ready_active = False
    ready=pygame.Rect(420,310,160,60)
    
    running = True
    while running:
        if ready_active == False:
            pygame.draw.rect(screen,ORANGE,ready,0,25)
        else:
            pygame.draw.rect(screen,WHITE,ready,0,25)
        textready="Ready"
        textready=fontrea.render(textready, True, BLUE1)
        screen.blit(textready,(466,325))

        textpercent = f"{loading_percent}%"
        pygame.draw.rect(screen, BLUE2, (470,190, 100, 50))
        textpercent=fontper.render(textpercent, True, WHITE)
        screen.blit(textpercent,(470,190))
        if (loading_percent==98): 
            running=False
            return

        nameofplayer1 = player1
        nameofplayer2 = player2
        textplayer1=font.render(nameofplayer1, True, WHITE)
        textplayer2=font.render(nameofplayer2, True, WHITE)
        if(nameofplayer2!="player 2"):
            pygame.draw.rect(screen,ORANGE,nameplayer1,0,20)
            pygame.draw.rect(screen,ORANGE,nameplayer2,0,20)
            screen.blit(textplayer1,(170,445))
            screen.blit(textplayer2,(725,445))
            screen.blit(imgplayer1,img_rectplayer1)
            screen.blit(imgplayer2,img_rectplayer2)
        else:
            pygame.draw.rect(screen,ORANGE,nameplayer1,0,20)
            screen.blit(textplayer1,(170,445))
            screen.blit(imgplayer1,img_rectplayer1)
            pygame.draw.rect(screen,YELLOW,player2_rect,0,20)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        if ((mouse_x>420 and mouse_x<580 and mouse_y>310 and mouse_y<370)
            or (mouse_x>420 and mouse_x<580 and mouse_y>420 and mouse_y<480)):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (event.button==1 and mouse_x>420 and mouse_x<580 and mouse_y>310 and mouse_y<370):
                    if (ready_btn!="ready"):
                        ready_btn = "ready"
                        print(f"You press {ready_btn}")
                    else:
                        ready_btn = "unready"
                        print(f"You press {ready_btn}")
                    if (ready_active): ready_active=False
                    else: ready_active=True
                if (event.button==1 and mouse_x>420 and mouse_x<580 and mouse_y>420 and mouse_y<480):
                    ready_btn = "exit"
                    global glb_exitRoom
                    glb_exitRoom = True
                    running=False
                    return
        pygame.display.flip()

def CheckRoom_interface(screen):
    pygame.display.set_caption("CHECK ROOM")
    ORANGE = (251, 133, 0)
    WHITE = (255, 255, 255)
    BLACK = (0,0,0)
    screen.fill(BLACK)
    pos_y = 50
    running = True
    font=pygame.font.SysFont('serif',15,5)
    screen.blit(font.render("ROOM", True, WHITE),(100,30))
    screen.blit(font.render("NAME", True, WHITE),(300,30))
    screen.blit(font.render("HOST", True, WHITE),(500,30))
    screen.blit(font.render("RIVAL", True, WHITE),(700,30))
    global check_room
    global done

    bg = pygame.image.load('asset/empty.png').convert()
    drawImg(screen, bg, 500, 300)
    
    while running:
        if pos_y == 70: drawRect(screen, 375, 150, 250, 300, BLACK)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if done==True:
            font2=pygame.font.SysFont('serif',20,5)
            pygame.draw.rect(screen, ORANGE, (800, 400, 150, 50))
            surface = font2.render("Quit", True, WHITE)
            screen.blit(surface, (800+50, 400+12))
        else:
            font2=pygame.font.SysFont('serif',20,5)
            pygame.draw.rect(screen, ORANGE, (800, 400, 150, 50))
            surface = font2.render("Checking...", True, WHITE)
            screen.blit(surface, (800+10, 400+12))

        if check_room!="None":
            print(check_room)
            name = f"Room of {check_room.split(':')[1]}"
            screen.blit(font.render(check_room.split(':')[0], True, WHITE),(100,pos_y))
            screen.blit(font.render(name, True, WHITE),(300,pos_y))
            screen.blit(font.render(check_room.split(':')[1], True, WHITE),(500,pos_y))
            screen.blit(font.render(check_room.split(':')[2], True, WHITE),(700,pos_y))
            pos_y+=20
            check_room = "None"

        if ((done==True and mouse_x>800 and mouse_x<950 and mouse_y>400 and mouse_y<450)):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if done==True and event.button==1 and mouse_x>800 and mouse_x<950 and mouse_y>400 and mouse_y<450:
                    print("Quit")
                    done=False
                    running = False
                    return
        pygame.display.flip()

def CheckUser_interface(screen):
    pygame.display.set_caption("INFORMATION")
    BLUE1 = (142, 202, 230)
    BLUE2 = (33, 158, 188)
    BLUE3 = (2, 48, 71)
    YELLOW = (255, 183, 3)
    ORANGE = (251, 133, 0)
    WHITE = (255, 255, 255)
    screen.fill(BLUE3)
    AvaPlayer=pygame.Rect(50,20,350,400)
    pygame.draw.rect(screen, YELLOW, AvaPlayer,0,20)

    RectNamePlayer=pygame.Rect(50,440,350,45)
    pygame.draw.rect(screen,ORANGE,RectNamePlayer,0,20)

    NameofPlayer=""
    font=pygame.font.SysFont('serif',28,5)
    TextPlayer=font.render(NameofPlayer, True, WHITE)
    screen.blit(TextPlayer,(170,445))

    InfoPlayer=pygame.Rect(500,20,450,465)
    pygame.draw.rect(screen,BLUE2,InfoPlayer,0,20)
    temp=pygame.Rect(500,20,450,46.5)
    pygame.draw.rect(screen,ORANGE,temp,0,-1,20,20)
    pygame.draw.line(screen,BLUE3,(500,66.5),(950,66.5),1)
    pygame.draw.line(screen,BLUE3,(500,113),(950,113),1)
    pygame.draw.line(screen,BLUE3,(500,159.5),(950,159.5),1)
    pygame.draw.line(screen,BLUE3,(500,206),(950,206),1)
    pygame.draw.line(screen,BLUE3,(500,252.5),(950,252.5),1)
    pygame.draw.line(screen,BLUE3,(500,299),(950,299),1)
    pygame.draw.line(screen,BLUE3,(500,345.5),(950,345.5),1)
    pygame.draw.line(screen,BLUE3,(500,392),(950,392),1)
    pygame.draw.line(screen,BLUE3,(500,438.5),(950,438.5),1)
    pygame.draw.line(screen,BLUE3,(500,485),(950,485),1)
    pygame.draw.line(screen,BLUE3,(655,66.5),(655,485),1)


    Info="INFORMATION"
    fontInfo=pygame.font.SysFont('serif',25,5)
    TextInfo=fontInfo.render(Info,True,WHITE)
    screen.blit(TextInfo,(640,31))

    Username="Username"
    Font=pygame.font.SysFont('serif',20,3)
    TextUsername=Font.render(Username, True, BLUE3)
    screen.blit(TextUsername,(510,80))

    Fullname="Full Name"
    TextFullname=Font.render(Fullname, True, BLUE3)
    screen.blit(TextFullname,(510,126.5))
    
    Phone="Phone"
    TextPhone=Font.render(Phone, True, BLUE3)
    screen.blit(TextPhone,(510,173))

    DOB="Date of Birth"
    TextDOB=Font.render(DOB, True, BLUE3)
    screen.blit(TextDOB,(510,219.5))

    Gender="Gender"
    TextGender=Font.render(Gender, True, BLUE3)
    screen.blit(TextGender,(510,266))

    GamePlayed="GamePlayed"
    TextGamePlayed=Font.render(GamePlayed, True, BLUE3)
    screen.blit(TextGamePlayed,(510,312.5))

    Win="Win"
    TextWin=Font.render(Win, True, BLUE3)
    screen.blit(TextWin,(510,359))

    Lost="Lost"
    TextLost=Font.render(Lost, True, BLUE3)
    screen.blit(TextLost,(510,405.5))

    CheckOnline="Status"
    TextCheckOnline=Font.render(CheckOnline, True,BLUE3)
    screen.blit(TextCheckOnline,(510,452))
    color_active = BLUE1
    color_passive = ORANGE
    color = color_passive

    global done
    global glb_username 
    global glb_fullname 
    global glb_phone 
    global glb_dob 
    global glb_gender 
    global glb_gameplayed 
    global glb_win
    global glb_lost
    global glb_online
    global glb_input

    active=False
    running=True
    global user
    while running:
        ImgPlayer = pygame.image.load('asset/searching.png').convert()
        if (glb_fullname=="Vu Duc Dung" and glb_dob=="19/04/2002") or (glb_fullname=="Nguyen Duy Thinh" and glb_dob=="2/1/2001"):
            ImgPlayer = pygame.image.load('asset/admale.png').convert()
        elif glb_fullname=="Nguyen Nhat Quynh" and glb_dob=="11/9/2002":
            ImgPlayer = pygame.image.load('asset/adfemale.png').convert()
        else:
            if glb_gender=="Male":
                ImgPlayer = pygame.image.load('asset/playermale.png').convert()
            elif glb_gender=="Female":
                ImgPlayer = pygame.image.load('asset/playerfemale.png').convert()
        img_rect = ImgPlayer.get_rect(center=(220,220))
        screen.blit(ImgPlayer,img_rect)
#hide text
        pygame.draw.rect(screen, BLUE2, (670,80, 270, 25))
        pygame.draw.rect(screen, BLUE2, (670,126.5, 270, 25))
        pygame.draw.rect(screen, BLUE2, (670,173, 270, 25))
        pygame.draw.rect(screen, BLUE2, (670,219.5, 270, 25))
        pygame.draw.rect(screen, BLUE2, (670,266, 270, 25))
        pygame.draw.rect(screen, BLUE2, (670,312.5, 270, 25))
        pygame.draw.rect(screen, BLUE2, (670,359, 270, 25))
        pygame.draw.rect(screen, BLUE2, (670,405.5, 270, 25))
        pygame.draw.rect(screen, BLUE2, (670,452, 270, 25))
#text
        screen.blit(Font.render(glb_username, True, BLUE3),(670,80))
        screen.blit(Font.render(glb_fullname, True, BLUE3),(670,126.5))
        screen.blit(Font.render(glb_phone , True, BLUE3),(670,173))
        screen.blit(Font.render(glb_dob, True, BLUE3),(670,219.5))
        screen.blit(Font.render(glb_gender , True, BLUE3),(670,266))
        screen.blit(Font.render(glb_gameplayed , True, BLUE3),(670,312.5))
        screen.blit(Font.render(glb_win, True, BLUE3),(670,359))
        screen.blit(Font.render(glb_lost, True, BLUE3),(670,405.5))
        screen.blit(Font.render(glb_online, True,BLUE3),(670,452))
        mouse_x, mouse_y =pygame.mouse.get_pos()
        if (active): color = color_active
        else: color = color_passive
        pygame.draw.rect(screen, color, (50,440,350,45),0,20)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                return
            if ((mouse_x>50 and mouse_x<400 and mouse_y>440 and mouse_y<485) or
                (done==True and mouse_x>50 and mouse_x<400 and mouse_y>20 and mouse_y<420)):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    if(mouse_x>50 and mouse_x<400 and mouse_y>440 and mouse_y<485):
                        if active==True:
                            active = False
                        else: active=True
                    if ((done==True and mouse_x>50 and mouse_x<400 and mouse_y>20 and mouse_y<420)):
                        print("You quit check user")
                        running=False
                        done=False
                        return
            if event.type==pygame.KEYDOWN and active:
                if event.key==pygame.K_BACKSPACE:
                    NameofPlayer=NameofPlayer[:-1]
                elif event.key==pygame.K_RETURN:
                    glb_input = NameofPlayer
                    print(f"Accessing to {glb_input}")
                    active=False
                else:
                    NameofPlayer+=event.unicode
        TextNameofPlayer=Font.render(NameofPlayer,True,WHITE)                     
        screen.blit(TextNameofPlayer,(175,450))    
        pygame.display.flip()

def CheckMess_interface(screen):
    pygame.display.set_caption("CHECK MESS")
    BLACK = (0,0,0)
    running = True

    bg = pygame.image.load('asset/mess.png').convert()
    drawImg(screen, bg , 500, 250)

    pos_y = 100
    global done
    global check_mess

    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (check_mess!="None"):
            font=pygame.font.SysFont('serif',15,5)
            screen.blit(font.render(check_mess, True, BLACK),(200,pos_y))
            check_mess="None"
            pos_y+=20
        if done==True:
            font=pygame.font.SysFont('serif',15,5)
            screen.blit(font.render("DONE", True, BLACK),(200,pos_y))
            
        if ((done==True and mouse_x>755 and mouse_x<960 and mouse_y>325 and mouse_y<500)):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if done==True and event.button==1 and mouse_x>755 and mouse_x<960 and mouse_y>325 and mouse_y<500:
                    print("Quit")
                    done=False
                    running = False
                    return
        pygame.display.flip()

def WaitingHall_interface(screen):
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    screen.fill((0,0,0))
    bg = pygame.image.load('asset/HallBG.png').convert()
    
    drawImg(screen, bg, 500, 250)
    box1 = pygame.Rect(385, 70, 230, 50)
    box2 = pygame.Rect(385, 130, 230, 50)
    box3 = pygame.Rect(385, 190, 230, 50)
    box4 = pygame.Rect(385, 250, 230, 50)
    box5 = pygame.Rect(385, 310, 230, 50)
    box6 = pygame.Rect(385, 370, 230, 50)
    boxlist =  [[box1, color_passive], 
                [box2, color_passive],
                [box3, color_passive], 
                [box4, color_passive], 
                [box5, color_passive], 
                [box6, color_passive]]
    running = True
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if ((mouse_x>385 and mouse_x<615 and mouse_y>70 and mouse_y<430)):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for i in range(len(boxlist)):
            pygame.draw.rect(screen, boxlist[i][1], boxlist[i][0])
        Text(screen, "Exit Server", 435, 85, WHITE)
        Text(screen, "Create Room", 430, 145, WHITE)
        Text(screen, "Join Room", 435, 205, WHITE)
        Text(screen, "Check Room", 435, 265, WHITE)
        Text(screen, "Check User", 435, 325, WHITE)
        Text(screen, "Check Mess", 430, 385, WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                index = (mouse_y-70)//60
                if (boxlist[index][1]==color_active): boxlist[index][1]=color_passive
                else: 
                    for i in range(len(boxlist)): 
                        if(i!=index): boxlist[i][1]=color_passive
                    boxlist[index][1]=color_active
                    global hallcmd
                    hallcmd = index
                    if (index==0): return
                    running=False
        pygame.display.flip()

def main_interface():
    global hallcmd
    pygame.init()
    screen = pygame.display.set_mode((1000,500))
    sound = pygame.mixer.Sound('asset/hall.mp3')
    sound.play(10,0,0)
    while True:
        time.sleep(0.5)
        WaitingHall_interface(screen)
        if (hallcmd==1): 
            if (CreateRoom_interface(screen)):
                Room_interface(screen)
            print("Early Thread stopped!")
            pygame.mixer.pause()
            pygame.quit()
            return
        elif (hallcmd==2): 
            if (JoinRoom_interface(screen)):
                Room_interface(screen)
            print("Early Thread stopped!")
            pygame.mixer.pause()
            pygame.quit()
            return
        elif (hallcmd==3):
            CheckRoom_interface(screen)
        elif (hallcmd==4):
            CheckUser_interface(screen)  
        elif (hallcmd==5):
            CheckMess_interface(screen)    
        elif (hallcmd==0):
            pygame.quit()
            return
        hallcmd=-1
        time.sleep(1)
"""ENDING THINH INTERFACE"""


def Game():
    BLACK = (0,0,0)
    GRAY = (150,150,150)
    WHITE = (250,250,250)
    YELLOW = (233, 196, 106)
    BLUE = (72, 202, 228)
    RED = (155, 34, 38)

    global BLOCKNUMB
    global Map1
    global Map2
    BLOCKSIZE = 40
    LMAP_LX = 30
    LMAP_RX = 430
    RMAP_LX = 550
    RMAP_RX = 950
    LMAP_TY = 30
    LMAP_BY = 430
    RMAP_TY = 30
    RMAP_BY = 430 

    def loadMap():
        Map = [["0.0" for i in range(BLOCKNUMB)] for j in range(BLOCKNUMB)] 
        #receive check mess from server and reply
        check = receive()
        time.sleep(0.25)
        print(f"Checking {check} with user {user}")
        if (check==user): 
            send("Yes")
            print("Reply Yes")
        else: 
            send("No")
            print("Reply No")

        time.sleep(0.25)
        mapname = receive()
        
        alist = [line.rstrip() for line in open(mapname)]
        for i in range(len(alist)):
            x = int(alist[i].split(' ')[0])
            y = int(alist[i].split(' ')[1])
            Map[x-1][y-1] = "1.0"
            
        global loading_percent
        for i in range(BLOCKNUMB):
            for j in range(BLOCKNUMB):
                time.sleep(0.1)
                print(f"Loading {loading_percent}%")
                loading_percent+=1

        # print(f"Recvecing map for {user}: ")
        # for i in range(BLOCKNUMB):
        #     for j in range(BLOCKNUMB):
        #         time.sleep(0.25)
        #         Map[i][j]=receive()
        #         print(Map[i][j], end="  ")
        #         # print(f"Loading {loading_percent}%")
        #         loading_percent+=1
        #     print()
        return Map

    def fillMap(minX, maxX, minY, maxY, Map):
        for x,i in zip(range(minX, maxX, BLOCKSIZE), range(BLOCKNUMB)):
            for y,j in zip(range(minY, maxY, BLOCKSIZE), range(BLOCKNUMB)):
                if (Map[i][j]=="1.0"):
                    pygame.draw.rect(screen, YELLOW, (x, y, BLOCKSIZE-2, BLOCKSIZE-2))

    def fillFullMap(minX, maxX, minY, maxY):
        for x in range(minX, maxX, BLOCKSIZE):
            for y in range(minY, maxY, BLOCKSIZE):
                pygame.draw.rect(screen, GRAY, (x, y, BLOCKSIZE-2, BLOCKSIZE-2))

    def drawMap(minX, maxX, minY, maxY):
        for x in range(minX, maxX, BLOCKSIZE):
            for y in range(minY, maxY, BLOCKSIZE):
                rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
                pygame.draw.rect(screen, BLACK, rect, 1)

    time.sleep(0.25)
    global Map1
    global Map2
    Map1 = loadMap()
    
    pygame.init()
    screen = pygame.display.set_mode((1000,500))
    screen.fill(BLUE)
    pygame.draw.line(screen, BLACK, (500,0),(500,500), 4)
    
    #draw grid for map
    drawMap(LMAP_LX, LMAP_RX, LMAP_TY, LMAP_BY)
    drawMap(RMAP_LX, RMAP_RX, RMAP_TY, RMAP_BY)
    #accept coordinate from server
    
    #fill color
    fillMap(LMAP_LX, LMAP_RX, LMAP_TY, LMAP_BY, Map1)
    fillFullMap(RMAP_LX, RMAP_RX, RMAP_TY, RMAP_BY)

    def hideText():
        rect = pygame.Rect(530, 450, 300, 50)
        pygame.draw.rect(screen, BLUE, rect)

    def Text(msg):
        screen.blit(font.render(msg, True, BLACK), (530, 450))

    def drawImg(string):
        rect = string.get_rect(center=(965, 465))
        screen.blit(string, rect)

    # threading run main course of game
    def main():
        def recieveTurn(ready_sound, textTurn, textDef, img_attacker, img_defender):
            time.sleep(0.5)
            global turn
            global cmd
            myturn = True
            # recieve checking from server and reply
            respon = receive()
            if (respon==user):
                print(f"{user} receive turn") 
                turn = True
                myturn = True
                time.sleep(0.25)
                send("Yes")
            else: 
                print(f"{user} refused turn")
                myturn = False
                turn = False
                time.sleep(0.25)
                send("No")
            if myturn==True:
                hideText()
                drawImg(img_attacker)
                ready_sound.play()
                Text(textTurn)
                # this thread would run paralell as same as "running system"
                while True:
                    time.sleep(1)
                    send(cmd)
                    if (cmd!="none"): 
                        cmd="none"
                        break
            else:
                hideText()
                drawImg(img_defender)
                Text(textDef)
                while True:
                    time.sleep(1)
                    respon = receive()
                    if (respon=="stop waiting"): 
                        return
                    else: pass

        def recieveCheck(miss_sound, hit_sound, textHit, textMiss, textRecHit, textRecMiss, img_hit, img_missed, img_hurt, img_haha):
            global Map1
            time.sleep(0.25)
            attacker = receive() #checker who is attacking
            time.sleep(0.25)
            coord = receive().split(':') #rec coordinate from attacker
            time.sleep(0.25)
            if (attacker!=user):
                print("Im receiving damage", end=" ")
                if (Map1[int(coord[0])][int(coord[1])]=="1.0"): 
                    send("Hit")
                    print("and it hit")
                else: 
                    send("Missed")
                    print("and it missed")
            else:
                send("Not my job")
                print("Im attacking")
            time.sleep(0.5)
            result = receive() #rec result after checking from server
            print(f"server Result = {result}")
            if (attacker==user and result=="Hit"):
                #recolor if attacker hit it
                pygame.draw.rect(screen, RED, (RMAP_LX+(BLOCKSIZE*int(coord[0])),RMAP_TY+(BLOCKSIZE*int(coord[1])),BLOCKSIZE-2,BLOCKSIZE-2))
                hideText()
                hit_sound.play()
                drawImg(img_hit)
                Text(textHit)
            elif (attacker==user and result=="Missed"):
                hideText()
                miss_sound.play()
                drawImg(img_missed)
                Text(textMiss)
            elif (attacker!=user and result=="Hit"):
                Map1[int(coord[0])][int(coord[1])]="0.0"
                #rec damage if defender is hit
                pygame.draw.rect(screen, RED, (LMAP_LX+(BLOCKSIZE*int(coord[0])),LMAP_TY+(BLOCKSIZE*int(coord[1])),BLOCKSIZE-2,BLOCKSIZE-2))
                hideText()
                hit_sound.play()
                drawImg(img_hurt)
                Text(textRecHit)
            elif (attacker!=user and result=="Missed"):
                hideText()
                miss_sound.play()
                drawImg(img_haha)
                Text(textRecMiss)

            global BLOCKNUMB
            #check is end
            if (attacker!=user):
                for i in range(BLOCKNUMB):
                    for j in range(BLOCKNUMB):
                        if (Map1[i][j]=="1.0"): 
                            return "continue"
                return attacker
            else: 
                return "Not my job"

        #RESOURSES
        textTurn = "Let's fight"
        textDef = "Repairing take damage"
        textRound = "Ending round"
        textHit = "Hit it yeahhh"
        textMiss = "Oh no! You missed"
        textRecHit = "Ough! It's hurt"
        textRecMiss = "HeHe! Miss me"
        textWin = "Game ended! You Win!"
        textLose = "Game ended! You Lose"
        img_attacker = pygame.image.load("asset/attacker.png").convert()
        img_defender = pygame.image.load("asset/defender.png").convert()
        img_hit = pygame.image.load("asset/hit.png").convert()
        img_missed = pygame.image.load("asset/missed.png").convert()
        img_hurt = pygame.image.load("asset/hurt.png").convert()
        img_haha = pygame.image.load("asset/haha.png").convert()
        hit_sound = pygame.mixer.Sound('asset/hit.mp3')
        miss_sound = pygame.mixer.Sound('asset/miss.wav')
        ready_sound = pygame.mixer.Sound('asset/readyGo.mp3')

        global glb_run
        glb_run = True
        sound = pygame.mixer.Sound('asset/backgroundMS.wav')
        sound.play()

        print(f"Map of {user}")
        for i in range(BLOCKNUMB):
            for j in range(BLOCKNUMB):
                print(Map1[i][j], end="  ")
            print()
        print()

        #main running thread game
        while glb_run:
            time.sleep(1)
            recieveTurn(ready_sound, textTurn, textDef, img_attacker, img_defender)
            isEnd = recieveCheck(miss_sound, hit_sound, textHit, textMiss, textRecHit, textRecMiss, img_hit, img_missed, img_hurt, img_haha)

            time.sleep(1)
            hideText()
            Text(textRound)

            send(isEnd)
            print(f"Is end = {isEnd}")
            time.sleep(0.5)
            final = receive()
            print(f"server Final check = {final}")
            if (final!="continue"):
                if (user==final):
                    pygame.draw.rect(screen, BLUE, (30, 450, 400, 50))
                    hideText()
                    Text(textWin)
                    time.sleep(3)
                elif (final!="none" and user!=final):
                    pygame.draw.rect(screen, BLUE, (30, 450, 400, 50))
                    hideText()
                    Text(textLose)
                    time.sleep(3)
                glb_run = False
                print("Ending Thread interface game")
                return
            else: print("Game is still go on")
            time.sleep(1)

    mainRun = threading.Thread(target=main, args=())
    mainRun.start()

    font=pygame.font.SysFont('arial', 30)
    global cmd  
    global turn
    textUser = f"Captain {user}"
    img_user = pygame.image.load("asset/boat.png").convert()

    #running system
    global glb_run
    while glb_run:
        rect = img_user.get_rect(center=(30, 465))
        screen.blit(img_user, rect)
        screen.blit(font.render(textUser, True, BLACK), (80, 450))
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                glb_run=False
                break
            elif (event.type == pygame.MOUSEBUTTONDOWN and event.button==1 and mouse_x>=RMAP_LX and mouse_x<=RMAP_RX and mouse_y>=RMAP_TY and mouse_y<=RMAP_BY):
                xbox = (mouse_x-RMAP_LX)//BLOCKSIZE
                ybox = (mouse_y-RMAP_TY)//BLOCKSIZE
                #check whether turn come, send it coordinate if your turn
                if (Map2[xbox][ybox]=="0.0" and turn):
                    pygame.draw.rect(screen, WHITE, (RMAP_LX+(BLOCKSIZE*xbox),RMAP_TY+(BLOCKSIZE*ybox),BLOCKSIZE-2,BLOCKSIZE-2))
                    cmd = f"{xbox}:{ybox}"
                    fired_sound = pygame.mixer.Sound('asset/firing.wav')
                    fired_sound.play()
                    turn = False
            if (mouse_x>=RMAP_LX and mouse_x<=RMAP_RX and mouse_y>=RMAP_TY and mouse_y<=RMAP_BY):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        pygame.display.flip()
    time.sleep(3)
    pygame.quit()

def CreateRoom():
    global glb_idr_create
    global invite_friend
    global valid
    global glb_exitRoom
    time.sleep(0.5)
    while True:
        time.sleep(0.5)
        idr = glb_idr_create
        if glb_exitRoom:
            send("Exit")
            return False
        send(f"{idr}:{user}:{invite_friend}")
        print(f"Sent specific mess as {idr}:{user}:{invite_friend}")
        if (idr!=0):
            if (receive()=="valid"):
                valid = True
                print("Create room successfully!")
                return True
            else:
                print("Room already hosted by another player")
                glb_idr_create = 0
                valid = False
                continue
        else:
            continue
        
def JoinRoom():
    global glb_idr_join
    global valid
    global glb_exitRoom
    while True:
        time.sleep(0.5)
        if glb_exitRoom:
            send("Exit")
            return False
        idr = glb_idr_join
        send(f"{idr}:{user}")
        print(f"Sent specific message as {idr}:{user}")
        if (idr!=0):
            respon = receive()
            if (respon=="valid"):
                valid = True
                print("Joined room successfully!")
                return True
            else:
                valid = False
                glb_idr_join = 0
                print(respon)
                continue
        else:
            pass

def Room():
    global player1
    global player2
    global ready_btn
    global hoster
    global glb_exitRoom
    time.sleep(0.25)
    respon_player1 = receive()
    #print(f"Waiting for player")
    if (respon_player1==user): hoster = True
    player1 = respon_player1
    while True:
        time.sleep(1)
        respon_player2 = receive()
        time.sleep(0.25)
        if glb_exitRoom: 
            send("Exit")
            return False
        else: send("wait")
        print(f"Waiting for player")
        if (respon_player2!="empty" and respon_player2!="none"): 
            player2=respon_player2
            break
    
    while True:
        time.sleep(1)
        send(f"{ready_btn}:{user}")
        respon = receive()
        if (respon=="Go"): return True
        elif (respon=="Out"):
            player1="player 1"
            player2="player 2"
            return False
        else:
            pass

def checkAvailable():
    SIZEROOM = 100
    global check_room
    global done
    done = False
    for i in range(SIZEROOM):
        time.sleep(0.1)
        respon = receive()
        print(f"Checking room status: {respon}")
        if respon!="Free": 
            check_room = respon
        else: pass
    done = True
    while True:
        time.sleep(0.5)
        if (done): send("No")
        else: 
            send("Yes")
            break
    return

def checkMess():
    global check_mess
    global done
    done = False
    time.sleep(0.5)
    send(user)
    time.sleep(0.2)
    length = int(receive())
    print(f"Length of users {length}")
    for i in range(length):
        time.sleep(0.25)
        data = receive()
        print(f"Finding data: {data}")
        if (data=="nah"): pass
        else:
            for i in range(int(data)):
                time.sleep(0.25)
                check_mess = receive()
                print(check_mess)
            break
    done = True
    while True:
        time.sleep(0.5)
        if (done): send("No")
        else: 
            send("Yes")
            return

def WaitingHall():
    thread_Hall = threading.Thread(target=main_interface, args=())
    thread_Hall.start()
    global hallcmd
    killthread = False
    while True:
        time.sleep(1)
        if (hallcmd==-1):
            send(str(hallcmd))
        elif (hallcmd>=0 and hallcmd<=5):
            send(str(hallcmd))
            print(f"You just pressed {hallcmd}")
            if (hallcmd==1):
                print("Creating Room")
                if (CreateRoom()): 
                    if(Room()):
                        time.sleep(0.5) 
                        Game()
                        killthread = True
                    else: killthread=True
                else: killthread = True
            elif (hallcmd==2):
                print("Joinning Room")
                if (JoinRoom()): 
                    if(Room()):
                        time.sleep(0.5) 
                        Game()
                        killthread=True
                    else: killthread=True
                else: killthread=True
            elif (hallcmd==3):
                print("Checking available Rooms")
                checkAvailable()
            elif (hallcmd==4):
                checkDataUser_client()
            elif (hallcmd==5):
                print("Cheking Message")
                checkMess()
            elif (hallcmd==0): 
                freeGlobalVar()
                print("Waiting for free varibale")
                return
            freeGlobalVar()
            print("Waiting for free varibale")
            time.sleep(1)
            if (killthread):
                thread_Hall = threading.Thread(target=main_interface, args=())
                print("Next Thread starting!")
                thread_Hall.start()
                killthread = False
            else: pass
                
"""ENDING NDTHINH"""


# check_user [-option] [username]
def checkDataUser_client():
    global glb_username 
    global glb_fullname 
    global glb_phone 
    global glb_dob 
    global glb_gender 
    global glb_gameplayed 
    global glb_win
    global glb_lost
    global glb_online
    global glb_input
    global done
    
    done = False
    while True:
        time.sleep(0.5)
        send(glb_input)
        print(f"Sent input {glb_input}")
        time.sleep(0.5)
        if (glb_input!="None"):
            client.send(glb_input.encode(FORMAT))
            time.sleep(0.25)
            rep = client.recv(SIZE).decode(FORMAT)
            time.sleep(0.25)
            if(rep == "EXIST"):
                time.sleep(0.25)
                respon = client.recv(SIZE).decode(FORMAT)
                print(respon)
                glb_username = respon.split(':')[1]
                time.sleep(0.25)
                respon = client.recv(SIZE).decode(FORMAT)
                print(respon)
                glb_fullname = respon.split(':')[1]
                time.sleep(0.25)
                respon = client.recv(SIZE).decode(FORMAT)
                print(respon)
                glb_phone = respon.split(':')[1]
                time.sleep(0.25)
                respon = client.recv(SIZE).decode(FORMAT)
                print(respon)
                glb_dob = respon.split(':')[1]
                time.sleep(0.25)
                respon = client.recv(SIZE).decode(FORMAT)
                print(respon)
                glb_gender = respon.split(':')[1]
                time.sleep(0.25)
                respon = client.recv(SIZE).decode(FORMAT)
                print(respon)
                glb_gameplayed = respon.split(':')[1]
                time.sleep(0.25)
                respon = client.recv(SIZE).decode(FORMAT)
                print(respon)
                glb_win = respon.split(':')[1]
                time.sleep(0.25)
                respon = client.recv(SIZE).decode(FORMAT)
                print(respon)
                glb_lost = respon.split(':')[1]
                time.sleep(0.25)
                respon = client.recv(SIZE).decode(FORMAT)
                print(respon)
                glb_online = respon.split(':')[1]
                break
            elif (rep=="NotFound"):
                glb_username = rep
                glb_fullname = rep
                glb_phone = rep
                glb_dob = rep
                glb_gender = rep
                glb_gameplayed = rep
                glb_win = rep
                glb_lost = rep
                glb_online = rep
                break
        else:
            pass
    done = True
    while True:
        time.sleep(0.5)
        if (done): send("No")
        else: 
            send("Yes")
            break
    return
        
# LOGIN -- OK
def login_Client(client):
    caesar = Caesar.Caesar()
    #Sau khi gửi lên server thì server sẽ check
    rep_From_server = ""
    username = input("Username: ")
    password = getpass.win_getpass(prompt="Password: ", show="*")
    isEncrypt = MySQL.EncryptAccount()
    client.sendall(isEncrypt.encode(FORMAT))
    if(isEncrypt == '1'):
        client.sendall(caesar.encrypt(25, username).encode(FORMAT))
        #Sau khi gửi lên server thì server sẽ check
        rep_From_server = client.recv(SIZE).decode(FORMAT)
        if(rep_From_server == "VALID"):
            client.sendall(caesar.encrypt(25, password).encode(FORMAT))
            rep_From_server = client.recv(SIZE).decode(FORMAT)
        elif(rep_From_server == "INVALID"):
            print("This username is not exist, pls enter again!")
            return False
    elif(isEncrypt == '0'):
        client.sendall(username.encode(FORMAT))
        #Sau khi gửi lên server thì server sẽ check
        rep_From_server = client.recv(SIZE).decode(FORMAT)
        if(rep_From_server == "VALID"):
            client.sendall(password.encode(FORMAT))
            rep_From_server = client.recv(SIZE).decode(FORMAT)
        elif(rep_From_server == "INVALID"):
            print("This username is not exist, pls enter again!")
            return False
    global user
    #After username is exist
    if(rep_From_server == "VALID"):
        user = username
        if(isEncrypt == '0'):
            print(f"Login successfully or Wellcome {username} login to server and Message wasnt encrypted!")
            return True
        elif(isEncrypt == '1'):
            print(f"Login successfully or Wellcome {username} login to server and Message was encrypted!")
            return True
    else:
        print("Failed to login, pls check your password again!")
        return False

# Register -- OK
def signUp_Client(client):
    caesar = Caesar.Caesar()
    username = input("Username: ")
    password = input("Password: ")
    isEncrypt = MySQL.EncryptAccount()
    client.sendall(isEncrypt.encode(FORMAT))
    new_Account = player.Account()
    if(isEncrypt == '1'):
        client.sendall(caesar.encrypt(25, username).encode(FORMAT))
        rep_user = client.recv(SIZE).decode(FORMAT)
        if(rep_user == 'INVALID'):
            print("This username is exist!")
        else:
            client.sendall(caesar.encrypt(25, password).encode(FORMAT))
            name = input("Name: ")
            client.sendall(name.encode(FORMAT))
            phone = input("Phone: ")
            client.sendall(phone.encode(FORMAT))
            gender = input("Gender (Male/Female): ")
            client.sendall(gender.encode(FORMAT))
            birth = input("Birth (dd/mm/yyyy): ")
            client.sendall(birth.encode(FORMAT))
            print(client.recv(SIZE).decode(FORMAT))
    elif(isEncrypt == "0"):
        client.sendall(username.encode(FORMAT))
        rep_user = client.recv(SIZE).decode(FORMAT)
        if(rep_user == 'INVALID'):
            print("This username is exist!")
        else:
            client.sendall(password.encode(FORMAT))
            name = input("Name: ")
            client.sendall(name.encode(FORMAT))
            phone = input("Phone: ")
            client.sendall(phone.encode(FORMAT))
            gender = input("Gender (Male/Female): ")
            client.sendall(gender.encode(FORMAT))
            birth = input("Birth (dd/mm/yyyy): ")
            client.sendall(birth.encode(FORMAT))
            print(client.recv(SIZE))

# Change PASS
def changePassword(client, username):
    caesar = Caesar.Caesar()
    client.sendall(caesar.encrypt(25, username).encode(FORMAT))
    cur_pass = getpass.win_getpass(prompt="Input your curent password: ", show="*")
    client.sendall(caesar.encrypt(25, cur_pass).encode(FORMAT))
    isCheck = client.recv(SIZE).decode(FORMAT)
    if(isCheck == 'VALID'):
        new_pass = getpass.win_getpass(prompt="Input your new password: ", show="*")
        new_pass_again = ""
        while(new_pass != new_pass_again):
            new_pass_again = getpass.win_getpass(prompt="Input your new password again: ", show="*")
        client.sendall(caesar.encrypt(25, new_pass_again).encode(FORMAT))
    elif(isCheck == 'INVALID'):
        print("Your username or password is wrong!")
    print(client.recv(SIZE).decode(FORMAT))


if __name__ == '__main__':
    pygame.mixer.init()
    sound = pygame.mixer.Sound("asset/BackgroundMS.mp3")
    sound.play(20,0,0)
    exit1 = False
    allCheck = True
    while allCheck:
        # Declare Tkinter
        window = Tk()
        window.title("Battle Ship")
        window.geometry("1250x650")
        buttonFont = font.Font(family='Helvetica', size=10, weight='bold')

        isCheck = ""

        # SET ICON
        my_pic = Image.open("asset/shipIcon.png")
        ship_resized = my_pic.resize((30, 30), Image.ANTIALIAS)
        new_pic_ship = ImageTk.PhotoImage(ship_resized)
        window.iconphoto(True, new_pic_ship)

        # SET BACKGROUND
        background = Image.open("asset/BackgroundShip.png")
        background_resized = background.resize((1250, 650), Image.ANTIALIAS)
        new_pic_background = ImageTk.PhotoImage(background_resized)
        my_label = Label(window, image=new_pic_background)
        my_label.place(x = 0, y = 0, relwidth=1, relheight=1)

        #LABEL NAME GAME
        nameGame = Image.open("asset/GameName.png")
        nameGame_resized = background.resize((1250, 650), Image.ANTIALIAS)
        new_pic_nameGame = ImageTk.PhotoImage(nameGame_resized)

        # CALENDAR ICON
        calendar = Image.open("asset/calendaricon.png")
        calendar_resized = background.resize((15, 15), Image.ANTIALIAS)
        new_pic_calendar = ImageTk.PhotoImage(calendar_resized)

        # GET DATE
        def calendar():
            calen = Tk()
            calen.title('Date')
            calen.geometry('300x300')
            cal = Calendar(calen, selectmode = "day", year = 2020, month = 5, day = 22)
            cal.pack(pady = 20)

            def grab_date():
                global date
                date = str((cal.get_date()))

            my_button = Button(calen, text= "Get Date", command=grab_date)
            my_button.pack(pady=20)

            my_label = Label(calen, text="")
            my_label.pack(pady=20)
            return date

        # LOGIN
        def NEW_LOGIN():
            msg = '1'
            client.sendall(msg.encode(FORMAT))

            global new_pic_ship1
            new_window =  Toplevel()
            new_window.title("Login")
            new_window.geometry("350x350")
            my_pic1 = Image.open("asset/shipcaro.png")
            ship_resized1 = my_pic1.resize((350, 350), Image.ANTIALIAS)
            new_pic_ship1 = ImageTk.PhotoImage(ship_resized1)
            label = Label(new_window, image=new_pic_ship1)
            label.place(x = 0, y = 0, relwidth=1, relheight=1)

            def on_closing1():
                client.sendall("EXIT".encode(FORMAT))
                new_window.destroy()

            new_window.protocol("WM_DELETE_WINDOW", on_closing1)

            def submit():
                caesar = Caesar.Caesar()
                username = entry_user.get()
                password = entry_pass.get()
                isEncrypt = ""
                rep_From_server = ""
                if messagebox.askyesno(title="EncryptAccount", 
                                    message="Do you want to encrypt message before sending?"):
                    isEncrypt = '1'
                else:
                    isEncrypt = '0'

                if (isEncrypt == '1'):
                    client.sendall(isEncrypt.encode(FORMAT))
                    client.sendall(caesar.encrypt(25, username).encode(FORMAT))
                    #Sau khi gửi lên server thì server sẽ check
                    rep_From_server = client.recv(SIZE).decode(FORMAT)
                    if(rep_From_server == "VALID"):
                        client.sendall(caesar.encrypt(25, password).encode(FORMAT))
                        rep_From_server = client.recv(SIZE).decode(FORMAT)
                    elif(rep_From_server == "INVALID"):
                        messagebox.showwarning(title="WARNING",
                                            message="This username is not exist, pls enter again!")
                        new_window.destroy()
                        return
                elif (isEncrypt == '0'):
                    client.sendall(isEncrypt.encode(FORMAT))
                    client.sendall(username.encode(FORMAT))
                    #Sau khi gửi lên server thì server sẽ check
                    rep_From_server = client.recv(SIZE).decode(FORMAT)
                    if(rep_From_server == "VALID"):
                        client.sendall(password.encode(FORMAT))
                        rep_From_server = client.recv(SIZE).decode(FORMAT)
                    elif(rep_From_server == "INVALID"):
                        messagebox.showwarning(title="WARNING",
                                            message="This username is not exist, pls enter again!")
                        new_window.destroy()
                        return

                global user
                #After username is exist
                if(rep_From_server == "VALID"):
                    user = username
                    if(isEncrypt == '0'):
                        messagebox.showinfo(title="INFO",
                                message=f"Login successfully or Wellcome {username} login to server and Message wasnt encrypted!")
                        new_window.destroy()
                        window.destroy()
                        pygame.mixer.pause()
                        WaitingHall()

                    elif(isEncrypt == '1'):
                        messagebox.showinfo(title="INFO",
                                message=f"Login successfully or Wellcome {username} login to server and Message was encrypted!")
                        new_window.destroy()
                        window.destroy()    
                        pygame.mixer.pause()                    
                        WaitingHall()
                else:
                    messagebox.showwarning(title="WARNING",
                                        message="Failed to login, pls check your password again!")
                    new_window.destroy()

            login = Label(new_window,
                    text="LOGIN",
                    font=('Arial', 20, 'bold'), 
                    fg='green', bg='black', 
                    relief=RIDGE,
                    bd=5, padx=20, pady=5, 
                    image=new_pic_ship,
                    compound='top').place(x = 110, y = 50)

            user = Label(new_window, text="Username", font = buttonFont,
                        fg='#00FF00', 
                        bg='black',
                        padx=10).place(x = 50, y = 180)
            password = Label(new_window, text="Password", font = buttonFont,
                    fg='#00FF00', 
                    bg='black',
                    padx=12).place(x = 50, y = 220)            
            entry_user = Entry(new_window,font=("Arial", 10))
            entry_user.place(x = 150, y = 180)
            entry_pass = Entry(new_window,font=("Arial", 10), show='*')
            entry_pass.place(x = 150, y = 220)

            submit_button = Button(new_window, text='Submit', command= submit)
            submit_button.place(x = 150, y = 280)
            # return submit()

        # REGISTER
        def NEW_REGISTER():
            msg = '2'
            client.sendall(msg.encode(FORMAT))
            global new_pic_ship2
            new_window =  Toplevel()
            new_window.title("Register")
            new_window.geometry("350x450")
            my_pic2 = Image.open("asset/shipcaro.png")
            ship_resized2 = my_pic2.resize((350, 450), Image.ANTIALIAS)
            new_pic_ship2 = ImageTk.PhotoImage(ship_resized2)
            label = Label(new_window, image=new_pic_ship2)
            label.place(x = 0, y = 0, relwidth=1, relheight=1)

            def on_closing1():
                client.sendall("EXIT".encode(FORMAT))
                new_window.destroy()

            new_window.protocol("WM_DELETE_WINDOW", on_closing1)


            def submit_Register():
                username = entry_user.get()
                password = entry_pass.get()
                fullname = entry_fullname.get()
                phone = entry_phone.get()
                gender = chooseGender()
                birth = entry_birth.get()

                isEncrypt = ""
                rep_From_server = ""
                caesar = Caesar.Caesar()
                if messagebox.askyesno(title="EncryptAccount", 
                                    message="Do you want to encrypt message before sending?"):
                    isEncrypt = '1'
                else:
                    isEncrypt = '0'

                if(isEncrypt == '1'):
                    client.sendall(isEncrypt.encode(FORMAT))
                    client.sendall(caesar.encrypt(25, username).encode(FORMAT))
                    rep_user = client.recv(SIZE).decode(FORMAT)
                    if(rep_user == 'INVALID'):
                        messagebox.showwarning(title="WARNING",
                                            message="This username is exist!")
                        new_window.destroy()
                        return
                    else:
                        client.sendall(caesar.encrypt(25, password).encode(FORMAT))
                        time.sleep(0.25)
                        client.sendall(fullname.encode(FORMAT))
                        time.sleep(0.25)
                        client.sendall(phone.encode(FORMAT))
                        time.sleep(0.25)
                        client.sendall(gender.encode(FORMAT))
                        time.sleep(0.25)
                        client.sendall(birth.encode(FORMAT))
                        # time.sleep(0.25)
                        # done = client.recv(SIZE).decode(FORMAT)
                        # repDone = client.recv(SIZE).decode(FORMAT)
                        messagebox.showinfo(title="INFO",
                                            message="Register Successful!")
                        new_window.destroy()
                        return
                elif(isEncrypt == "0"):
                    client.sendall(isEncrypt.encode(FORMAT))
                    client.sendall(username.encode(FORMAT))
                    rep_user = client.recv(SIZE).decode(FORMAT)
                    if(rep_user == 'INVALID'):
                        messagebox.showwarning(title="WARNING",
                                            message="This username is exist!")
                        new_window.destroy()
                        return
                    else:
                        client.sendall(password.encode(FORMAT))
                        time.sleep(0.25)
                        client.sendall(fullname.encode(FORMAT))
                        time.sleep(0.25)
                        client.sendall(phone.encode(FORMAT))
                        time.sleep(0.25)
                        client.sendall(gender.encode(FORMAT))
                        time.sleep(0.25)
                        client.sendall(birth.encode(FORMAT))
                        # time.sleep(0.25)
                        # done = client.recv(SIZE).decode(FORMAT)
                        # repDone = client.recv(SIZE).decode(FORMAT)
                        messagebox.showinfo(title="INFO",
                                            message="Register Successful!")
                        
                        new_window.destroy()        
                        return 
                

            login = Label(new_window,
                    text="REGISTER",
                    font=('Arial', 20, 'bold'), 
                    fg='green', bg='black', 
                    relief=RIDGE,
                    bd=5, padx=20, pady=5, 
                    image=new_pic_ship,
                    compound='top').place(x = 80, y = 40)

            user = Label(new_window, text="Username", font = buttonFont,
                        fg='#00FF00', 
                        bg='black',
                        padx=10).place(x = 50, y = 150)
            entry_user = Entry(new_window,font=("Arial", 10))
            entry_user.place(x = 150, y = 150)

            password = Label(new_window, text="Password", font = buttonFont,
                    fg='#00FF00', 
                    bg='black',
                    padx=12).place(x = 50, y = 180)         
            entry_pass = Entry(new_window,font=("Arial", 10))
            entry_pass.place(x = 150, y = 180)

            fullname = Label(new_window, text="Fullname", font = buttonFont,
                    fg='#00FF00', 
                    bg='black',
                    padx=12).place(x = 50, y = 210)         
            entry_fullname = Entry(new_window,font=("Arial", 10))
            entry_fullname.place(x = 150, y = 210)

            phone = Label(new_window, text="Phone", font = buttonFont,
                    fg='#00FF00', 
                    bg='black',
                    padx=22).place(x = 50, y = 240)         
            entry_phone = Entry(new_window,font=("Arial", 10))
            entry_phone.place(x = 150, y = 240)

            gender_list = ["Male", "Female"]
            x = IntVar()
            gender = Label(new_window, text="Gender", font = buttonFont,
                    fg='#00FF00', 
                    bg='black',
                    padx=19).place(x = 50, y = 270)  
            def chooseGender():
                ans = ''
                if x.get()==0:
                    ans = 'Male'
                else:
                    ans = 'Female'
                return ans
                
            for index in range(len(gender_list)):
                radio_gender = Radiobutton(new_window,
                                        variable=x,
                                        value= index,
                                        text = gender_list[index],
                                        font = buttonFont, padx=5, command=chooseGender)
                radio_gender.place(x = 150 + index*60, y = 270)
            # radio_gender = Entry(new_window,font=("Arial", 10)).place(x = 150, y = 270)

            birth = Label(new_window, text="Birth", font = buttonFont,
                    fg='#00FF00', 
                    bg='black',
                    padx=28).place(x = 50, y = 300)
            entry_birth = Entry(new_window,font=("Arial", 10), text = 'ONE')
            entry_birth.place(x = 150, y = 301)
            date = Button(new_window, command=calendar,
                        image=new_pic_calendar).place(x = 280, y = 301)
            
            submit_button = Button(new_window, text='Submit', command=submit_Register)
            submit_button.place(x = 150, y = 360)
      

        def NEW_CHANGEPASS():
            msg = '3'
            client.sendall(msg.encode(FORMAT))
            global new_pic_ship2
            new_window =  Toplevel()
            new_window.title("Change Password")
            new_window.geometry("350x450")
            my_pic2 = Image.open("asset/shipcaro.png")
            ship_resized2 = my_pic2.resize((350, 450), Image.ANTIALIAS)
            new_pic_ship2 = ImageTk.PhotoImage(ship_resized2)
            label = Label(new_window, image=new_pic_ship2)
            label.place(x = 0, y = 0, relwidth=1, relheight=1)

            def on_closing():
                client.sendall("EXIT".encode(FORMAT))
                # client.sendall("".encode(FORMAT))
                # client.sendall("".encode(FORMAT))
                # client.sendall("".encode(FORMAT))
                # client.sendall("".encode(FORMAT))
                # client.sendall("".encode(FORMAT))
                # client.sendall("".encode(FORMAT))
                new_window.destroy()

            new_window.protocol("WM_DELETE_WINDOW", on_closing)

            def submit_Change():
                client.sendall("OK".encode(FORMAT))
                time.sleep(0.25)
                caesar = Caesar.Caesar()
                checkEncrypt = ""
                
                if messagebox.askyesno(title="EncryptAccount", 
                                    message="Do you want to encrypt message before sending?"):
                    checkEncrypt = '1'
                else:
                    checkEncrypt = '0'

                if(checkEncrypt == '1'):
                    client.sendall(checkEncrypt.encode(FORMAT))
                    time.sleep(0.25)
                    username = entry_user.get()
                    cur_pass = entry_pass.get()
                    
                    client.sendall(caesar.encrypt(25, username).encode(FORMAT))
                    time.sleep(0.25)
                    client.sendall(caesar.encrypt(25, cur_pass).encode(FORMAT))
                else:
                    client.sendall(checkEncrypt.encode(FORMAT))
                    time.sleep(0.25)
                    username = entry_user.get()
                    cur_pass = entry_pass.get()
                    
                    client.sendall(username.encode(FORMAT))
                    time.sleep(0.25)
                    client.sendall(cur_pass.encode(FORMAT))

                isCheck = client.recv(SIZE).decode(FORMAT)
                if(isCheck == 'VALID'):
                    new_pass = entry_newpass.get()
                    if(checkEncrypt == '1'):
                        client.sendall(caesar.encrypt(25, new_pass).encode(FORMAT))
                    else:
                        client.sendall((new_pass).encode(FORMAT))
                    messagebox.showinfo(title="INFO",
                                            message="Successful to change your password!")
                elif(isCheck == 'INVALID'):
                    messagebox.showwarning(title="WARNING",
                                            message="Your username or password is wrong!")
                new_window.destroy()

            login = Label(new_window,
                    text="Change Password",
                    font=('Arial', 20, 'bold'), 
                    fg='green', bg='black', 
                    relief=RIDGE,
                    bd=5, padx=20, pady=5, 
                    image=new_pic_ship,
                    compound='top').place(x = 32, y = 50)

            user = Label(new_window, text="Username", font = buttonFont,
                        fg='#00FF00', 
                        bg='black',
                        padx=25).place(x = 40, y = 180)
            old_password = Label(new_window, text="Password", font = buttonFont,
                    fg='#00FF00', 
                    bg='black',
                    padx=27).place(x = 40, y = 220)
            
            new_password = Label(new_window, text="New password", font = buttonFont,
                    fg='#00FF00', 
                    bg='black',
                    padx=12).place(x = 40, y = 260)
                
            entry_user = Entry(new_window,font=("Arial", 10))
            entry_user.place(x = 170, y = 180)
            entry_pass = Entry(new_window,font=("Arial", 10), show='*')
            entry_pass.place(x = 170, y = 220)
            entry_newpass = Entry(new_window,font=("Arial", 10), show='*')
            entry_newpass.place(x = 170, y = 260)

            submit_button = Button(new_window, text='Submit', command=submit_Change).place(x = 150, y = 350) 

        #LABEL LOGIN
        label = Label(window,
                    text="BATTLE SHIP",
                    font=('Arial', 40, 'bold'), 
                    fg='green', bg='black', 
                    relief=RIDGE,
                    bd=10, pady=8, padx=30,
                    image=new_pic_ship,
                    compound='top')
        label.pack(pady = 120)

        login_button = Button(window, text="Login", font = buttonFont,
                            padx=50,
                            command=NEW_LOGIN,
                            fg='#00FF00', 
                            bg='black', 
                            activeforeground='#00FF00',
                            activebackground='white')
        login_button.place(x = 550, y = 400)

        register_button = Button(window, text="Register", font = buttonFont,
                                padx=42,
                                command=NEW_REGISTER, 
                                fg='#00FF00', 
                                bg='black', 
                                activeforeground='#00FF00',
                                activebackground='white')
        register_button.place(x = 550, y =450)

        forget_button = Button(window, text="Change Password", font = buttonFont,
                                padx=11,
                                command=NEW_CHANGEPASS, 
                                fg='#00FF00', 
                                bg='black', 
                                activeforeground='#00FF00',
                                activebackground='white')
        forget_button.place(x = 550, y = 500)


        def ExitExit():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                window.destroy()
                global allCheck
                allCheck = False
                msg = '0'
                client.sendall(msg.encode(FORMAT))

            
            
        exit_button = Button(window, text="Exit", font = buttonFont,
                            padx=55,
                            command=ExitExit,
                            fg='#00FF00', 
                            bg='black', 
                            activeforeground='#00FF00',
                            activebackground='white')
        exit_button.place(x = 550, y =550)

        

        # def on_closing3():
        #     msg = '0'
        #     client.sendall(msg.encode(FORMAT))
        #     window.destroy()
        #     exit1 = True

        # window.protocol("WM_DELETE_WINDOW", on_closing3)

        def on_closing():
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                window.destroy()
                global allCheck
                allCheck = False
                msg = '0'
                client.sendall(msg.encode(FORMAT))

        window.protocol("WM_DELETE_WINDOW", on_closing)

        window.mainloop()

        # if(exitt == True): 
        #     break
        # else: window.mainloop()

        # if(exit1 == True):
        #     break
        # # End Tkinter
        # else: window.mainloop()
        