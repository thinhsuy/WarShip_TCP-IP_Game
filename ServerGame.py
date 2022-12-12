import socket
import time
import threading
import MySQL
import player
import Caesar
import numpy as np
import random

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5500
FORMAT = "utf-8"
ADDR = (HOST, PORT)
HEADER = 1024
SIZE = HEADER
DISCONNECT_MESSAGE = "DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen(10)
print(f"[SERVER]: Listening on {HOST} at port {PORT}")
DataBase = []


"""NGUYỄN DUY THỊNH"""
#init Global variables
BLOCKNUMB = 10
SIZEROOM = 100
Map = np.zeros((BLOCKNUMB,BLOCKNUMB))
room = [["empty","empty"] for i in range(SIZEROOM)]
game = [["none","none"] for i in range(SIZEROOM)]
warmap = [[Map, Map] for i in range(SIZEROOM)]
check_ready = [[False, False] for i in range(SIZEROOM)]
check_loadmap = [[False, False] for i in range(SIZEROOM)]
isHit = ["none" for i in range(SIZEROOM)]
isEnd = ["none" for i in range(SIZEROOM)]

room[10][0]="Naruto"
room[10][1]="Sasuke"
room[30][0]="Luffy"
room[20][0] = "CardiB"
room[20][1] = "TaylorSwift"
room[40][0] = "Madara"
room[60][0] = "Pikachu"
room[60][1] = "Bubasour"
room[80][0] = "Rayquaza"
room[80][1] = "MewTwo"
room[95][0] = "KaitoKid"
room[95][1] = "Conan"

def send(sv, msg):
   message=msg.encode(FORMAT)
   sv.send(message)

def sendCoordinate(sv, idr, player):
   for i in range(BLOCKNUMB):
      for j in range(BLOCKNUMB):
        time.sleep(0.1)

def randomMap():
   a = random.randint(2,4)
   return f"map{a}.txt"

def sendMap(sv, idr):
   global warmap
   #send check whether player is first player or not
   send(sv, room[idr][0])
   time.sleep(0.25)
   reply = sv.recv(SIZE).decode(FORMAT)
   #if true, send the first map, else send second one
   time.sleep(0.25)
   if (reply=="Yes"):
      if (room[idr][0]=="thinh" or room[idr][0]=="vddung" or room[idr][0]=="quinxi"):
         send(sv, "map1.txt")
      else: 
         randmap = randomMap()
         send(sv, randmap)
      sendCoordinate(sv, idr, 0)
   elif (reply=="No"):
      if (room[idr][1]=="thinh" or room[idr][1]=="vddung" or room[idr][1]=="quinxi"):
         send(sv, "map2.txt")
      else: 
         randmap = randomMap() 
         send(sv, randmap)
      sendCoordinate(sv, idr, 1)

def Game(sv, idr):
    global warmap
    time.sleep(0.25)
    sendMap(sv, idr)
   
    def sendTurn(player):
            time.sleep(0.5)
            #send name to check player is the one that server looking for
            send(sv, room[idr][player])
            time.sleep(0.25)
            reply = sv.recv(SIZE).decode(FORMAT)
            if reply=="Yes":
                # if true, waiting for attacker choose position
                while True:
                    time.sleep(1)
                    cmd = sv.recv(SIZE).decode(FORMAT)
                    if (cmd!="none"):
                        game[idr][player]=cmd
                        break
                    else: trash = cmd
            else:
                # if false, force defender to wait
                while True:
                    time.sleep(1)
                    if (game[idr][player]=="none"): send(sv, "waiting")
                    else:
                        send(sv, "stop waiting")
                        return
    
    def checkIsHit(sv, idr, attacker):
        global isHit
        time.sleep(0.25)
        send(sv, room[idr][attacker])
        time.sleep(0.25)
        send(sv, game[idr][attacker])
        time.sleep(0.25)
        result = sv.recv(SIZE).decode(FORMAT)
        if (result=="Not my job"): pass
        else: isHit[idr] = result
        time.sleep(0.5)
        while isHit[idr]=="none":
            pass
        send(sv, isHit[idr])
        if isHit[idr]=="Hit": return True
        else: return False

    attacker = 0
    defender = 1
    running=True
    global isHit
    global isEnd
    game[idr][attacker]="none" 
    game[idr][defender]="none"
    isHit[idr] = "none"
    isEnd[idr] = "none"
    while running: 
        time.sleep(1)
        swapped = False
        sendTurn(attacker)
        time.sleep(0.5)
        if (checkIsHit(sv, idr, attacker)): swapped = False
        else: swapped = True

        time.sleep(1)
        #check whether the player(s) still able to fight or not
        checkEnd = sv.recv(SIZE).decode(FORMAT)
        if (checkEnd=="Not my job"): pass
        else: isEnd[idr] = checkEnd

        time.sleep(0.5)
        while isEnd[idr]=="none": pass
        if (isEnd[idr]=="continue"): 
            send(sv, "continue")
        elif (isEnd[idr]!="continue" and isEnd!="none"):
            game[idr][attacker]="none" 
            game[idr][defender]="none"
            isHit[idr] = "none"
            if (isEnd[idr]==room[idr][attacker]):
                send(sv, room[idr][attacker])
                return room[idr][attacker]
            elif (isEnd[idr]==room[idr][defender]):
                send(sv, room[idr][defender])
                return room[idr][defender]
        
        time.sleep(1)
        #swap player for sure
        if (swapped==True):
            temp = attacker
            attacker = defender
            defender = temp
        else: pass
        
        # because of thread so it would have to do these at last for safe information
        # set back default value after a round and set value in map to 0 if hit it
        game[idr][attacker]="none" 
        game[idr][defender]="none"
        isHit[idr] = "none"
        isEnd[idr] = "none"

def Invite(myself, friend, idr):
   if (friend=="none"): return
   else:
      for i in range(len(DataBase)):
         if (DataBase[i].account.getUsername()==friend):
            for i in range(len(DataBase[i].messBox)):
               if (DataBase[i].messBox[i]=="None"):
                  DataBase[i].messBox[i] = f"Player {myself} has invited you to Room:{idr}"
                  DataBase[i].messBox.append("None")

def CreateRoom(sv):
   time.sleep(0.5)
   while True:
      time.sleep(0.5)
      client = sv.recv(SIZE).decode(FORMAT)
      if client=="Exit": return 0
      idr = int(client.split(':')[0])
      if (idr!=0):
         username = client.split(':')[1]
         friend = client.split(':')[2]
         if (room[idr][0]=="empty"):
            room[idr][0]=username
            send(sv, "valid")
            Invite(username, friend, idr)
            return idr
         else: 
            send(sv, "invalid")
            #return 0
            continue
      else: 
         continue

def JoinRoom(sv):
   while True:
      time.sleep(0.5)
      client = sv.recv(SIZE).decode(FORMAT)
      if client=="Exit": return 0
      idr = int(client.split(':')[0])
      if (idr!=0):
         username = client.split(':')[1]
         if (room[idr][1]=="empty" and room[idr][0]!="empty"):
            room[idr][1]=username
            send(sv, "valid")
            return idr
         elif (room[idr][1]!="empty" and room[idr][0]!="empty"):
            send(sv, "Room already full of players")
            continue
         elif (room[idr][1]=="empty" and room[idr][0]=="empty"):
            send(sv, "Room is empty, please create one")
            return 0
      else:
         pass

def Room(sv, idr):
   time.sleep(0.25)
   sv.send(room[idr][0].encode(FORMAT))
   while True:
      time.sleep(1)
      sv.send(room[idr][1].encode(FORMAT))
      time.sleep(0.25)
      isExit = sv.recv(SIZE).decode(FORMAT)
      if isExit == "Exit": return False
      if (room[idr][1]!="empty"): break

   while True:
      time.sleep(1)
      reply = sv.recv(SIZE).decode(FORMAT)
      if (reply.split(':')[0]=="ready"):
         for i in range(2):
            if room[idr][i]==reply.split(':')[1]: check_ready[idr][i]=True
      elif (reply.split(':')[0]=="ready"): 
         for i in range(2):
            if room[idr][i]==reply.split(':')[1]: check_ready[idr][i]=False
      if (check_ready[idr][0] and check_ready[idr][1]):
         sv.send("Go".encode(FORMAT))
         return True
      elif (reply.split(':')[0]=="exit"):
         sv.send("Out".encode(FORMAT))
         for i in range(2):
            if room[idr][i]==reply.split(':')[1]: check_ready[idr][i]=False
         return False
      else: 
         sv.send("Wait".encode(FORMAT))
     
def checkAvailable(sv):
   for i in range(SIZEROOM):
      time.sleep(0.1)
      if (room[i][0]=="empty"): 
         send(sv, "Free")
      else:
         text = f"{i}:{room[i][0]}:{room[i][1]}"
         send(sv, text)
   while True:
      time.sleep(0.5)
      reply = sv.recv(SIZE).decode(FORMAT)
      if (reply=="Yes"): break
      else: trash=reply
   return

def freeVariable(idr):
   for i in range(2):
      room[idr][i]="empty"
      game[idr][i]="none"
      check_ready[idr][i]=False
   isHit[idr] = "none"
   isEnd[idr] = "none"
   warmap[idr] = [Map, Map]

def updateInfor(user, result):
   if(result == 'win'):
      MySQL.WIN(user, DataBase)
   elif(result == 'lose'):
      MySQL.LOSE(user, DataBase)

def checkMess(sv):
   time.sleep(0.5)
   username = sv.recv(SIZE).decode(FORMAT)
   time.sleep(0.2)
   send(sv, str(len(DataBase)))
   for i in range(len(DataBase)):
      time.sleep(0.25)
      if (DataBase[i].account.getUsername()==username):
         send(sv, str(len(DataBase[i].messBox)))
         for i in range(len(DataBase[i].messBox)):
            time.sleep(0.25)
            send(sv, DataBase[i].messBox[i])
         break
      else:
         send(sv, "nah")

   while True:
      time.sleep(0.5)
      reply = sv.recv(SIZE).decode(FORMAT)
      if (reply=="Yes"): return
      else: trash = reply

def WaitingHall(sv, user):
   global DataBase
   caesar = Caesar.Caesar()
   user = caesar.decrypt(25, user)
   for player in DataBase:
      if player.account.getUsername()==user:
         player.online = "ON"
         break

   while True:
      idr = 0
      time.sleep(1)
      client_cmd = int(sv.recv(SIZE).decode(FORMAT))
      if (client_cmd==-1): pass
      else:
         if (client_cmd==1):
            idr = CreateRoom(sv)
            if (idr!=0): 
               if(Room(sv, idr)): 
                  time.sleep(0.5)
                  if (Game(sv, idr)==room[idr][0]): updateInfor(room[idr][0], 'win')
                  else: updateInfor(room[idr][1], 'lose')
                  time.sleep(3)
               else: pass
            else: pass
         elif (client_cmd==2):
            idr = JoinRoom(sv)
            if (idr!=0):
               if (Room(sv, idr)): 
                  time.sleep(0.5)
                  if (Game(sv, idr)==room[idr][0]): updateInfor(room[idr][0], 'win')
                  else: updateInfor(room[idr][1], 'lose')
                  time.sleep(3)
               else: pass
            else: pass
         elif (client_cmd==3):
            checkAvailable(sv)
         elif (client_cmd==4):
            checkDataUser_server(sv)
         elif (client_cmd==5):
            checkMess(sv)
         elif (client_cmd==0):
            freeVariable(idr)
            MySQL.setOFF(user, DataBase)
            for player in DataBase:
               if player.account.getUsername()==user:
                  player.online = "OFF"
                  break
            return  
         freeVariable(idr)
         time.sleep(1)
"""ENDING OF NDTHINH"""


# check_user [-option] [username]
def checkDataUser_server(conn):
   global DataBase
   while True:
      time.sleep(0.5)
      username = conn.recv(SIZE).decode(FORMAT)
      time.sleep(0.5)
      if (username!="None"):
         if(MySQL.checkUser('account.csv', username)):
            conn.sendall("EXIST".encode(FORMAT))
            time.sleep(0.25)
            ans = MySQL.handle_data_user(5, username, DataBase)
            time.sleep(0.25)
            conn.send(str('Username     :' + username).encode(FORMAT))
            time.sleep(0.25)
            conn.send(str('Fullname     :' + ans.name).encode(FORMAT))
            time.sleep(0.25)
            conn.send(str('Phone        :' + ans.getPhone()).encode(FORMAT))
            time.sleep(0.25)
            conn.send(str('Date of birth:' + ans.birth).encode(FORMAT))
            time.sleep(0.25)
            conn.send(str('Gender       :' + ans.gender).encode(FORMAT))
            time.sleep(0.25)
            conn.send(str('Game played  :' + ans.gamePlayed).encode(FORMAT))
            time.sleep(0.25)
            conn.send(str('Win          :' + ans.win).encode(FORMAT))
            time.sleep(0.25)
            conn.send(str('Lost         :' + ans.lost).encode(FORMAT))
            time.sleep(0.25)
            conn.send(str(username + ' :' + ans.online).encode(FORMAT))
            break
         else:
            conn.send("NotFound".encode(FORMAT))
      else: pass

   while True:
      time.sleep(0.5)
      reply = conn.recv(SIZE).decode(FORMAT)
      if (reply=="Yes"): return
      else: trash = reply

# LOGIN -- OK
def login_Server(conn):
   caesar = Caesar.Caesar()
   isEncrypt = conn.recv(1024).decode(FORMAT)
   original_username = "none"
   if(isEncrypt == '1'):
      username = conn.recv(1024).decode(FORMAT)
      original_username = username
      if(MySQL.checkUser('account.csv', caesar.decrypt(25, username))):
         conn.sendall("VALID".encode(FORMAT))
         password = conn.recv(1024).decode(FORMAT)
         if(MySQL.checkPass('account.csv', caesar.decrypt(25, password), caesar.decrypt(25, username))):
            conn.sendall("VALID".encode(FORMAT))
            return original_username
         else: 
            conn.sendall("INVALID".encode(FORMAT))
            return "None"
      else:
         conn.sendall("INVALID".encode(FORMAT))
         return False
   elif(isEncrypt == '0'):
      username = conn.recv(1024).decode(FORMAT)
      original_username = username
      if(MySQL.checkUser('account.csv', username)):
         conn.sendall("VALID".encode(FORMAT))
         password = conn.recv(1024).decode(FORMAT)
         if(MySQL.checkPass('account.csv', password, username)):
            conn.sendall("VALID".encode(FORMAT))
            return original_username
         else: 
            conn.sendall("INVALID".encode(FORMAT))
            return "None"
      else:
         conn.sendall("INVALID".encode(FORMAT))
         return False
   elif(isEncrypt == "EXIT"):
      return False
         
# Register -- OK
def signUp_Server(conn):
   global DataBase
   caesar = Caesar.Caesar()
   isEncrypt = conn.recv(1024).decode(FORMAT)
   if(isEncrypt == '1'):
      username = conn.recv(1024).decode(FORMAT)
      if (MySQL.checkUser('account.csv', caesar.decrypt(25, username))):
         conn.sendall("INVALID".encode(FORMAT))
      else:
         conn.sendall("VALID".encode(FORMAT))
         password = conn.recv(1024).decode(FORMAT)
         time.sleep(0.25)
         new_Account = player.Account()
         new_Account.setPassword(caesar.decrypt(25, password))
         new_Account.setUsername(caesar.decrypt(25, username))
         name = conn.recv(1024).decode(FORMAT)
         time.sleep(0.25)
         phone = conn.recv(1024).decode(FORMAT)
         time.sleep(0.25)
         gender = conn.recv(1024).decode(FORMAT)
         time.sleep(0.25)
         birth = conn.recv(1024).decode(FORMAT)
         # time.sleep(0.25)
         MySQL.setDataPlayer(new_Account, 'account.csv', name, phone, gender, birth)
         MySQL.loadCurrentData(DataBase)
         print("Register Successful!")
         # conn.sendall("Register Successful!".encode(FORMAT))
         return
         # for user in DataBase:
         #    print(user.account.getUsername())
         # conn.sendall("Register successfully!".encode(FORMAT))
   elif(isEncrypt == '0'):
      username = conn.recv(1024).decode(FORMAT)
      if (MySQL.checkUser('account.csv', username)):
         conn.sendall("INVALID".encode(FORMAT))
      else:
         conn.sendall("VALID".encode(FORMAT))
         password = conn.recv(1024).decode(FORMAT)
         time.sleep(0.25)
         new_Account = player.Account()
         new_Account.setPassword(password)
         new_Account.setUsername(username)
         name = conn.recv(1024).decode(FORMAT)
         time.sleep(0.25)
         phone = conn.recv(1024).decode(FORMAT)
         time.sleep(0.25)
         gender = conn.recv(1024).decode(FORMAT)
         time.sleep(0.25)
         birth = conn.recv(1024).decode(FORMAT)
         MySQL.setDataPlayer(new_Account, 'account.csv', name, phone, gender, birth)
         MySQL.loadCurrentData(DataBase)
         print("Register Successful!")
         # conn.sendall("Register Successful!".encode(FORMAT))
         return
         # conn.sendall("Register successfully!".encode(FORMAT))
   elif(isEncrypt == "EXIT"):
      print("REGISTER FAILED!")
      return

# Change PASS 
def changePassword(conn, DataBase):
   check = conn.recv(1024).decode(FORMAT)
   time.sleep(0.25)
   if(check == "EXIT"): return False

   caesar = Caesar.Caesar()
   username = ""
   cur_pass = ""
   new_pass = ""
   
   checkEncrypt = conn.recv(1024).decode(FORMAT)
   time.sleep(0.25)
   if(checkEncrypt == '1'):
      username = caesar.decrypt(25, conn.recv(1024).decode(FORMAT))
      time.sleep(0.25)
      cur_pass = caesar.decrypt(25, conn.recv(1024).decode(FORMAT))
   else:
      username = conn.recv(1024).decode(FORMAT)
      time.sleep(0.25)
      cur_pass = conn.recv(1024).decode(FORMAT)
   
   for user in DataBase:
      if(user.account.getUsername()==username and user.account.getPassword()==cur_pass):
         conn.sendall("VALID".encode(FORMAT))
         if(checkEncrypt == '1'):
            new_pass = caesar.decrypt(25, conn.recv(1024).decode(FORMAT))
         else:
            new_pass = conn.recv(1024).decode(FORMAT)
         user.account.setPassword(new_pass)
         return True #if change password successful
   conn.sendall("INVALID".encode(FORMAT))
   return False #if failed to change password

def handle_client(conn, addr, DataBase):
   print(f"[NEW CONNECTION] {addr} is connected!")
   user = "None"
   connected = True
   while connected:
         msg = conn.recv(1024).decode(FORMAT)

         if msg == '1':
               print(f"[{addr}]: LOGIN")
               user = login_Server(conn)
               if (user!="None"): WaitingHall(conn, user)
               else: pass
         elif (msg == '2'):
               print(f"[{addr}]: REGISTER")
               signUp_Server(conn)
         elif(msg == '3'):
            print(f"[{addr}]: CHANGE PASSWORD")
            if(changePassword(conn, DataBase) == True):
               MySQL.UpdateDataBase(DataBase)
            else:
               pass
         elif (msg=='0'):
               connected = False
               print(f"[{addr}]: DISCONNECTED")
               # MySQL.setOFF(username, DataBase)
               break
   conn.close()

def printIt():
  threading.Timer(5.0, printIt).start()
  print("Hello")
#   MySQL.saveDataBase(DataBase)

def start():
   # Load data user
   # DataBase = []
   MySQL.loadCurrentData(DataBase)
   server.listen()
   while True:
      conn, addr = server.accept()
      thread = threading.Thread(target=handle_client, args=(conn, addr, DataBase))
      thread.start()
      MySQL.saveDataBase(DataBase)
      # thread_time = threading.Timer(5.0, MySQL.saveDataBase(DataBase))
      # thread_time.start()
      # printIt()
      print(f"[ACTIVE CONNECTION]: {threading.active_count()-1}")

if __name__ == '__main__':
   print("[SERVER] Server is starting...")
   start()
