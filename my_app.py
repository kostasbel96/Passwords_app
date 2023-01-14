
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

    def __str__(self):
        return f"Person: {self.person.name} {self.person.surname}\nUsername or Email: {self.username_or_email}\nPassword: {self.password}"   


