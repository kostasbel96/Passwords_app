
class Type:

    def __init__(self, type_name):
        self.type_name = type_name

class Person:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

class Account(Type):

    def __init__(self, account_type, person, username_or_email, password):
        super().__init__(account_type)
        self.person = person
        self.username_or_email = username_or_email
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
        type = input("Enter type:")
        name = input("Enter name:")
        for account in MyApp.accounts:
            if account.type_name == type and account.person.name == name:
                account.password = new_password

    def delete_account(self):
        username = input("enter username:")
        password = input("enter password:")
        type = input("enter type")
        for account in MyApp.accounts:
            if account.type_name == type and account.username_or_email == username and account.password == password:
                MyApp.accounts.remove(account)




a = MyApp()

while True:
    c = input("Enter:")
    if c =='':
        break
    elif c == '1':
        a.add_account()
    elif c == '2':
        a.update_password()
    elif c == '3':
        for account in MyApp.accounts:
            print(account.username_or_email,account.password)        
    elif c == '4':
        a.delete_account()