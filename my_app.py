import sqlite3 

class Type:

    def __init__(self, type_name):
        self.type_name = type_name

class Person:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

class Account(Type):

    def __init__(self, type_name, person, username, password):
        super().__init__(type_name)
        self.person = person
        self.username = username
        self.password = password
  

class MyApp:

    accounts = []
    def __init__(self):
        pass
    
    def add_account(self):
        type = input("Enter type:")
        name = input("Enter name:")
        surname = input("Enter lastname:")
        username = input("Enter username:")
        password = input("Enter password:")
        MyApp.accounts.append(Account(type,Person(name,surname),username, password))

    def update_password(self):
        new_password = input("Enter new password:")
        type_name = input("Enter type:")
        name = input("Enter name:")
        for account in MyApp.accounts:
            if account.type_name == type_name:
                account.password = new_password
                return account

    def delete_account(self):
        password = input("enter password:")
        type_name = input("enter type")
        for account in MyApp.accounts:
            if account.type_name == type_name and account.password == password:
                MyApp.accounts.remove(account)
                return account

    def get_account(self):
        type_name = input("Enter type:")
        username = input("Enter username:")
        password = input("Enter password:")

        for account in MyApp.accounts:
            if type_name == account.type_name and username == account.username and password == account.password:
                print(account.username,account.password)          

    def connect_db(self,dbfile):
        try:
            with sqlite3.connect(dbfile) as condb:
                self.create_db(condb)
        except Exception as e :
                print(e)

    def create_db(self, connect):
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE 'ACCOUNTS'(
                        'TYPE' TEXT,
                        'NAME' TEXT,
                        'SURNAME' TEXT,
                        'USERNAME' TEXT,
                        'PASSWORD' TEXT,
                        PRIMARY KEY('TYPE','PASSWORD')
        ); """)

    def add_to_database(self,dbfile):
        try:
            with sqlite3.connect(dbfile) as condb:
                for account in MyApp.accounts:
                   type_name = account.type_name
                   name = account.person.name
                   surname = account.person.surname
                   username = account.username
                   password = account.password 
                cursor = condb.cursor()
                cursor.execute("""INSERT INTO ACCOUNTS VALUES((?),(?),(?),(?),(?));""",(type_name,name,surname,username,password,))
                condb.commit()
        except Exception as e:
            print(e)        

    def delete_from_db(self,dbfile):
        try:
            with sqlite3.connect(dbfile) as condb:
                account = self.delete_account()
                cursor = condb.cursor()
                cursor.execute(f"""DELETE FROM ACCOUNTS WHERE TYPE = (?) AND PASSWORD = (?)""",(account.type_name,account.password,))
                condb.commit()
        except Exception as e:
            print(e)        

    def get_data(self,dbfile):
        try:
            with sqlite3.connect(dbfile) as condb:
                cursor = condb.cursor()
                cursor.execute("""SELECT * FROM ACCOUNTS""")
                data_list = cursor.fetchall()
                for data in data_list:
                    MyApp.accounts.append(Account(data[0],Person(data[1],data[2]),data[3], data[4]))
        except Exception as e:
            print(e)   

    def update_password_db(self,dbfile):
        try:
            with sqlite3.connect(dbfile) as condb:
                account = self.update_password()
                cursor = condb.cursor()
                cursor.execute("""UPDATE ACCOUNTS SET PASSWORD = (?) WHERE TYPE = (?)""",(account.password,account.type_name))
                condb.commit()
        except Exception as e:
            print(e)





a = MyApp()

a.connect_db("data.db")
a.get_data("data.db")
while True:
    c = input("Enter:")
    if c =='':
        break
    elif c == '1':
        a.add_account()
        a.add_to_database("data.db")
    elif c == '2':
        a.update_password_db("data.db")
    elif c == '3':
        for account in MyApp.accounts:
            print(account.type_name,account.username,account.password)        
    elif c == '4':
        a.delete_from_db("data.db")
    elif c == '5':
        a.get_account()    