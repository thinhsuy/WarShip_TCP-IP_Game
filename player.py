"""
1) Player:
- username
- password
- Name
- Phone
- Gender
- Date of birth
- Online or not
- Number of games played
- Win / Lost
- 
"""

class Account:
    def __init__(self):
        self.__username = ""
        self.__password = ""

    def getUsername(self):
        return self.__username
    def getPassword(self):
        return self.__password
    def setUsername(self, name):
        self.__username = name
    def setPassword(self, psw):
        self.__password = psw

class Player:
    # def __init__(self):
    #     self.account = ""
    #     self.name = ""
    #     self.__phone = ""
    #     self.gender = ""
    #     self.birth = ""
    #     self.gamePlayed = ''
    #     self.win = ""
    #     self.lost = ""
    #     self.online = ""

    def __init__(self, account, name, phone, gender, birth, gamePlayed, win, lost, online):
        self.account = account
        self.name = name
        self.__phone = phone
        self.gender = gender
        self.birth = birth
        self.gamePlayed = gamePlayed
        self.win = win
        self.lost = lost
        self.online = online
        self.messBox = ["None"]

    # Setter and Getter for private variable
    def getPhone(self):
        return self.__phone
    def setPhone(self, phone):
        self.__phone = phone
