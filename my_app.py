import pickle

class Person:

    def __init__(self, name, surname):
        self.name = name
        self.surname = surname

class Account:

    def __init__(self, person, username_or_email, password):
        self.person = person
        self.username_or_email = username_or_email
        self.password = password

    def __str__(self):
        return f"Person: {self.person.name} {self.person.surname}\nUsername or Email: {self.username_or_email}\nPassword: {self.password}"   

list_accounts = []

reply = input("Enter:")
if reply == "1":
    try:
        with open("data.pkl","wb") as f:
            person = Person("ete","test")
            pickle.dump(person,f)
    except:
        print("Error")
else:
    try:
        with open("data.pkl","rb") as f:
            ob = pickle.load(f)
            print(ob.name)
    except:
        print("ERROR")        
