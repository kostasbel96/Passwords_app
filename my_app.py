import pickle

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

    # def __str__(self):
        # return f"Person: {self.person.name} {self.person.surname}\nUsername or Email: {self.username_or_email}\nPassword: {self.password}"   

list_accounts = []

# list_accounts.append(Account("facebook", Person("Kostas", "Veloutsos"), "kwstasvel96@gmail.com", "password"))

 
# try:
#     with open("test.pkl","wb") as f:
#         pickle.dump(list_accounts,f)
# except:
#     print("Error")

try:
    with open("test.pkl","rb") as f:
        list_accounts = pickle.load(f)
except:
    print("Error")

print(list_accounts[0].type_name)            
