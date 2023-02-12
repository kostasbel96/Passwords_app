import sqlite3 
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo

class Type:
    def __init__(self, type_name):
        self.type_name = type_name

class Account(Type):
    def __init__(self, type_name, username, password):
        super().__init__(type_name)
        self.username = username
        self.password = password
  
class MyApp:
    accounts = []
    def __init__(self,root):
        self.root = root
        self.root.geometry("800x600+300+100")
        self.root.resizable(0,0)
        self.root.config(bg='gray20')
        self.connect_db("data.db")
        self.get_data("data.db")
        self.frame_main = tk.Frame(self.root)
        self.frame_main.pack(side='right')
        self.canvas_main = tk.Canvas(self.frame_main,width=600,height=600,bg='gray20')
        self.canvas_main.pack(side='right',fill='both')
        self.start = True
        self.del_count = 0
        self.oldLen = 0
        self.passwords()
        
    def passwords(self):
        self.frame_passwords = tk.Frame(self.root)
        self.frame_passwords.pack()
        self.canvas = tk.Canvas(self.frame_passwords,width=200,height=570,bg='gray20')
        self.update()
        
    #setup scroll bar
    def set_scroll_bar(self):
        try:
            if self.canvas.bbox('all')[3] >= int(self.canvas['height'])-100 and self.start:
                print("mpike scroll")
                self.sbar = ttk.Scrollbar(self.frame_passwords,orient="vertical",command=self.canvas.yview)
                self.sbar.pack(side="right",fill="y")
                self.canvas.configure(yscrollcommand=self.sbar.set)
                self.canvas.bind('<Configure>',lambda e: self.canvas.configure(scrollregion=(self.canvas.bbox("all")[0],self.canvas.bbox('all')[1],self.canvas.bbox('all')[2],self.canvas.bbox('all')[3]+20)))
                self.canvas.bind_all("<MouseWheel>",self.on_mousewheel)
                self.start = False
                self.canvas.update()
            elif self.canvas.bbox('all')[3] >= int(self.canvas['height'])-100 and not self.start:
                self.reset_scrollregion()    
        except Exception as e:
            print(e)
        finally:
            self.canvas.pack()

    #create labels
    def update(self):
        btn = tk.Button(self.frame_passwords,text="Δημιουργία νέας σύνδεσης",width=30,command=self.btnpressed)
        btn.pack(side='bottom')
        self.labels = []
        for i,account in enumerate(MyApp.accounts):
            label = tk.Label(self.canvas,text=f"{account.type_name}\n{account.username}",width=150,bg="gray20",fg="white",anchor='w')
            self.labels.append(label)
            label.pack()
            self.canvas.create_window(100,20+i*50,width=150,window=label)
        self.hover_click()
        self.set_scroll_bar()
        
    #hover
    def hover_click(self):    
        if MyApp.accounts:            
            a = lambda i: self.labels[i].bind("<Enter>", lambda e: self.labels[i].config(bg='gray'))
            b = lambda j: self.labels[j].bind("<Leave>", lambda e: self.labels[j].config(bg='gray20'))
            c = lambda i: self.labels[i].bind("<Button-1>",self.click)

            for i in range(len(self.labels)):
                a(i)
                c(i)
            for j in range(len(self.labels)):
                b(j)
                
    def reset_scrollregion(self):
        self.canvas.configure(scrollregion=(self.canvas.bbox("all")[0],self.canvas.bbox('all')[1],self.canvas.bbox('all')[2],self.canvas.bbox('all')[3]+20))
 
    #click on label
    def click(self,event):
        self.labels_no = self.canvas.find_all()
        print("labels",self.labels_no)
        self.canvas_main.delete('all')
        abs_coord_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        abs_coord_y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
        for l in self.labels_no:
            if self.canvas.bbox(l)[0]<=self.canvas.canvasx(abs_coord_x)<= self.canvas.bbox(l)[2] and self.canvas.bbox(l)[1]<=self.canvas.canvasy(abs_coord_y)<= self.canvas.bbox(l)[3]:                
                for i,label in enumerate(self.labels):
                    if i+1 == l-self.oldLen:
                        text = label['text'].split('\n')
                        self.label_no = i
                        if text[1].strip() == MyApp.accounts[i].username:
                            print(l)
                            print("done2")
                            username = text[1]
                            password = MyApp.accounts[i].password
                            type_name = text[0]

                            delete_btn = tk.Button(self.root,text="Αφαίρεση",width=10,command=lambda :self.pressed_delete(l))
                            self.canvas_main.create_window(400,120,window=delete_btn)

                            label_type_name = tk.Label(self.root,text=type_name,bg="gray20",fg='white')
                            self.canvas_main.create_window(200,120,window=label_type_name)

                            label_username = tk.Label(self.root,text=username,bg="gray20",fg='white')
                            self.canvas_main.create_window(200,160,window=label_username)

                            label_password = tk.Label(self.root,text=f"{'*'*len(password)}",bg="gray20",fg='white')
                            self.canvas_main.create_window(200,200,window=label_password)

                            show_password_btn = tk.Button(self.root,text="show",width=5,command = lambda : self.show_password(password,label_password,show_password_btn))
                            self.canvas_main.create_window(350,200,window=show_password_btn)
                            
                            edit_btn = tk.Button(self.root,text="Επεξεργασία",width=10,command=lambda : self.edit_account(show_password_btn,label_password,label_username,password,type_name,i))
                            self.canvas_main.create_window(300,120,window=edit_btn)
                            
                            break
                        
    def edit_account(self,show_btn,label_password,label_username,password,type_name,i):
        try:
            text_var_password = tk.StringVar(self.root)
            text_var_password.set(password)
            entry_password = tk.Entry(self.root,textvariable=text_var_password,bg='gray20',fg='white')
            self.canvas_main.create_window(200,200,window=entry_password)

            text_var_username = tk.StringVar(self.root)
            text_var_username.set(label_username['text'])
            entry_password = tk.Entry(self.root,textvariable=text_var_username,bg='gray20',fg='white')
            self.canvas_main.create_window(200,160,window=entry_password)

            btn_confirm = tk.Button(self.root,text="confirm",width=5,command=lambda : [self.update_password_db('data.db',text_var_password.get(),type_name),self.update_username_db('data.db',text_var_password.get(),type_name,text_var_username.get(),i)])
            self.canvas_main.create_window(350,200,window=btn_confirm)

            show_btn.destroy()
            label_username.destroy()
            label_password.destroy()
        except Exception as e:
            print(e)

    def show_password(self,password,label_password,btn):
        try:

            if label_password['text'] == '*'*len(password):
                label_password.config(text=password)
                btn.config(text="hide")
            else:
                label_password.config(text=f"{'*'*len(password)}")
                btn.config(text="show")
        except Exception as e:
            print(e)
            
    def pressed_delete(self,l):
        self.delete_from_db('data.db')
        print("l",l)
        self.oldLen += len(self.labels_no)
        print("old",self.oldLen)
        self.canvas.delete('all')
        self.update()
        self.canvas_main.delete('all')
        
    #new record
    def btnpressed(self):
        self.canvas_main.delete('all')
        
        label_type_name = tk.Label(self.root,text='type',fg='white',bg='gray20')
        self.canvas_main.create_window(200,120,window=label_type_name)
        type_name = tk.Entry(self.root,width=20)
        self.canvas_main.create_window(200,140,window=type_name)

        
        label_username = tk.Label(self.root,text='username',fg='white',bg='gray20')
        self.canvas_main.create_window(200,160,window=label_username)
        username = tk.Entry(self.root,width=20)
        self.canvas_main.create_window(200,180,window=username)

        
        label_password = tk.Label(self.root,text='password',fg='white',bg='gray20')
        self.canvas_main.create_window(200,200,window=label_password)
        password = tk.Entry(self.root,width=20)
        self.canvas_main.create_window(200,220,window=password)


        btn_confirm = tk.Button(self.root,text="confirm",width=10,command=lambda: self.add_account(type_name.get(),username.get(),password.get()))
        self.canvas_main.create_window(200,250,window=btn_confirm)
        
    #scrolling with mousewheel
    def on_mousewheel(self, event):
        abs_coord_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        if int(self.canvas['height'])-50 < self.canvas.bbox('all')[3]:
            if 0<=abs_coord_x<=self.canvas.bbox('all')[2]: 
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def add_label(self,type_name,username):
        print("mpike add label")
        frame = tk.Frame(self.canvas,relief="groove",borderwidth=0)
        label = tk.Label(frame,text=f"{type_name.strip()}\n{username.strip()}",width=150,bg="gray20",fg="white",anchor='w')
        self.labels.append(label)
        label.pack()
        self.canvas.create_window(100,20+(len(self.labels)-1)*50,width=150,window=frame)
        self.hover_click()
        self.set_scroll_bar()
        
    def add_account(self,type_name,username,password):
        for account in MyApp.accounts:
            if type_name == account.type_name and password == account.password and account.username == username:
                showinfo("Window","Το account υπάρχει ήδη στο σύστημα")
                return
        MyApp.accounts.append(Account(type_name,username,password))
        self.add_to_database('data.db')
        self.add_label(type_name,username)
          
    def update_password(self,new_password,type_name):
        for account in MyApp.accounts:
            if account.type_name == type_name:
                account.password = new_password
                return account

    def delete_account(self):
        password = MyApp.accounts[self.label_no].password
        type_name = MyApp.accounts[self.label_no].type_name
        for account in MyApp.accounts:
            if account.type_name == type_name and account.password == password:
                MyApp.accounts.remove(account)
                return account        

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
                        'USERNAME' TEXT,
                        'PASSWORD' TEXT,
                        PRIMARY KEY('TYPE','PASSWORD')
        ); """)

    def add_to_database(self,dbfile):
        try:
            with sqlite3.connect(dbfile) as condb:
                for account in MyApp.accounts:
                   type_name = account.type_name
                   username = account.username
                   password = account.password 
                cursor = condb.cursor()
                cursor.execute("""INSERT INTO ACCOUNTS VALUES((?),(?),(?));""",(type_name,username,password,))
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
                    MyApp.accounts.append(Account(data[0],data[1], data[2]))
        except Exception as e:
            print(e)   


    def update_username(self,password,type_name,new_username):
        for account in MyApp.accounts:
            if account.type_name == type_name and account.password == password:
                account.username = new_username
                return account

    def update_username_db(self,dbfile,password,type_name,new_username,i):
        try:
            with sqlite3.connect(dbfile) as condb:
                account = self.update_username(password,type_name,new_username)
                self.labels[i].config(text=f"{account.type_name}\n{account.username}")
                cursor = condb.cursor()
                cursor.execute("""UPDATE ACCOUNTS SET USERNAME = (?) WHERE TYPE = (?) AND PASSWORD = (?)""",(account.username,account.type_name,account.password,))
                print("added to db")
                condb.commit()
        except Exception as e:
            print(e) 

    def update_password_db(self,dbfile,new_password,type_name):
        try:
            with sqlite3.connect(dbfile) as condb:
                account = self.update_password(new_password,type_name)
                cursor = condb.cursor()
                cursor.execute("""UPDATE ACCOUNTS SET PASSWORD = (?) WHERE TYPE = (?)""",(account.password,account.type_name,))
                print("added to db")
                condb.commit()
        except Exception as e:
            print(e)



if __name__ == '__main__':
    root = tk.Tk()
    a = MyApp(root)
    root.mainloop()