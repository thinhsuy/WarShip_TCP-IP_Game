import csv
import sys

import player
import threading
import os
import Caesar 

def HandleData(data):
   new_data = ""
   for ch in data:
      new_data = new_data + chr(ord(ch)+3)
   return new_data

def EncryptAccount():
   print("Do you want to encrypt message before sending? (1 or 0)")
   print("1. Yes")
   print("0. No")
   choose = input("Your selection: ")
   return choose

def loadData_ChangePass():
   with open('account.csv', 'r') as csv_file:
      csv_reader = csv.DictReader(csv_file)  
      for line in csv_reader:
         acc = player.Account()
         acc.setUsername(line['username'])
         acc.setPassword(line['password'])
         name = line['name']
         phone = line['phone']
         gender = line['gender']
         birth = line['birth']
         gamePlayed = line['gamePlayed']
         win = line['win']
         lost = line['lost']
         online = line['online']
         user = player.Player(acc, name, phone, gender, birth, gamePlayed, win, lost, online)
      csv_file.close()
      return

def loadCurrentData(DataBase):
   with open('account.csv', 'r') as csv_file:
      csv_reader = csv.DictReader(csv_file)  
      for line in csv_reader:
         isCheck = False
         for user in DataBase:
            if(line['username']==user.account.getUsername()):
               isCheck = True

         if(isCheck == False):
            acc = player.Account()
            acc.setUsername(line['username'])
            acc.setPassword(line['password'])
            name = line['name']
            phone = line['phone']
            gender = line['gender']
            birth = line['birth']
            gamePlayed = line['gamePlayed']
            win = line['win']
            lost = line['lost']
            online = line['online']
            user = player.Player(acc, name, phone, gender, birth, gamePlayed, win, lost, online)
            DataBase.append(user)

      csv_file.close()
      return


def checkData(filename, data, type):
   with open(filename, 'r') as csv_file:
      csv_reader = csv.DictReader(csv_file)
      for line in csv_reader:
         if(line[type] == data):
            csv_file.close()
            return True
      csv_file.close()
      return False

def checkUser(filename, user):
   with open(filename, 'r') as csv_file:
      csv_reader = csv.DictReader(csv_file)
      for line in csv_reader:
         if(line['username'] == user):
            csv_file.close()
            return True
      csv_file.close()
      return False   
   
def checkPass(filename, password, username):
   with open(filename, 'r') as csv_file:
      csv_reader = csv.DictReader(csv_file)
      for line in csv_reader:
         if(line['password'] == password and line['username'] == username):
            csv_file.close()
            return True
      csv_file.close()
      return False

def setOFF(username, DataBase):
   for user in DataBase:
      if(user.account.getUsername()==username):
         user.online = "OFF"

   with open('account.csv', mode = 'w') as csv_file:
      fieldnames = ['username', 'password', 'name', 'phone', 'gender', 'birth', 'gamePlayed', 'win', 'lost', 'online']
      writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
      writer.writeheader()
      for player in DataBase:
         writer.writerow({'username': player.account.getUsername(),
                       'password': player.account.getPassword(),
                       'name': player.name,
                       'phone': player.getPhone(),
                       'gender': player.gender,
                       'birth': player.birth,
                       'gamePlayed': player.gamePlayed, 
                       'win': player.win, 'lost': player.lost,
                       'online': player.online})
      csv_file.close()
      return

def setON(DataBase):
   return "ON"

def WriteData(filename, data, type):
   with open(filename, 'a') as csv_file:
      fieldnames = ['username', 'password', 'name', 'phone', 'gender', 'birth', 'gamePlayed', 'win', 'lost', 'online']
      writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

def setDataPlayer(acc, filename, name, phone, gender, birth):
   # isCheck = os.path.isfile(filename)
   with open(filename, mode = 'a') as csv_file:
      fieldnames = ['username', 'password', 'name', 'phone', 'gender', 'birth', 'gamePlayed', 'win', 'lost', 'online']
      writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
      # if(isCheck == False):
      #    writer.writeheader()
      writer.writerow({'username': acc.getUsername(),
                       'password': acc.getPassword(),
                       'name': name,
                       'phone': phone,
                       'gender': gender,
                       'birth': birth,
                       'gamePlayed': '0', 'win': '0', 'lost': '0',
                       'online': 'OFF'})
      csv_file.close()
      return

def UpdateDataBase(DataBase):
   with open('account.csv', mode = 'w') as csv_file:
      fieldnames = ['username', 'password', 'name', 'phone', 'gender', 'birth', 'gamePlayed', 'win', 'lost', 'online']
      writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
      writer.writeheader()
      for player in DataBase:
         writer.writerow({'username': player.account.getUsername(),
                       'password': player.account.getPassword(),
                       'name': player.name,
                       'phone': player.getPhone(),
                       'gender': player.gender,
                       'birth': player.birth,
                       'gamePlayed': player.gamePlayed, 
                       'win': player.win, 'lost': player.lost,
                       'online': player.online})
      csv_file.close()
      return

def saveDataBase(DataBase):
   with open('account1.csv', mode = 'w') as csv_file:
      fieldnames = ['username', 'password', 'name', 'phone', 'gender', 'birth', 'gamePlayed', 'win', 'lost', 'online']
      writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
      writer.writeheader()
   with open('account1.csv', mode = 'a') as csv_file:
      fieldnames = ['username', 'password', 'name', 'phone', 'gender', 'birth', 'gamePlayed', 'win', 'lost', 'online']
      writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
      for player in DataBase:
         writer.writerow({'username': player.account.getUsername(),
                       'password': player.account.getPassword(),
                       'name': player.name,
                       'phone': player.getPhone(),
                       'gender': player.gender,
                       'birth': player.birth,
                       'gamePlayed': player.gamePlayed, 
                       'win': player.win, 'lost': player.lost,
                       'online': player.online})

def check_user(username):
   print("Which option do you want to check?")
   print("1. Online")
   print("2. Show_date")
   print("3. Show_fullname")
   print("4. Show_note")
   print('5. Show_all')
   print('6. Show_point')
   clientOption = 5
   print("Auto client: 5")
   return clientOption

def handle_data_user(option, username, DataBase):
   if(option == 5):
      for _player in DataBase:
         if(_player.account.getUsername()==username):
            temp_acc = player.Account()
            temp_acc.setPassword(_player.account.getPassword())
            temp_acc.setUsername(username)
            account = temp_acc
            name = _player.name
            phone = _player.getPhone()
            gender = _player.gender
            birth = _player.birth
            gamePlayed = _player.gamePlayed
            win = _player.win
            lost = _player.lost
            online = _player.online
            temp_Player = player.Player(temp_acc, name, phone, gender, birth, gamePlayed, win, lost, online)
            return temp_Player


def WIN(username, DataBase):
   for player in DataBase:
      if(player.account.getUsername()==username):
         temp = player.win
         temp1 = int(temp)
         temp1 += 1
         player.win = str(temp1)
         temp2 = player.gamePlayed
         temp3 = int(temp2)
         temp3 += 1
         player.gamePlayed = temp3

def LOSE(username, DataBase):
   for player in DataBase:
      if(player.account.getUsername()==username):
         temp = player.lost
         temp1 = int(temp)
         temp1 += 1
         player.win = str(temp1)
         temp2 = player.gamePlayed
         temp3 = int(temp2)
         temp3 += 1
         player.gamePlayed = temp3


def main():
    checkData('None','None','None')
    WriteData('None', 'None', 'None')
    checkUser('None', 'None')
    checkPass('None', 'None', 'None')
    saveDataBase('None')
    handle_data_user('None','None','None')
    checkUser('None')

if __name__ == "__main__":
    main()
