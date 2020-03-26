"""
reader/writer- If sent is empty, the person cannot read it. Email can be modified.
sender/receiver- message passing
priority-
binary semaphore - only one person can login
"""
from tkinter import *
from tkinter import ttk
import os
from os import path
import re

if not path.exists('sentbox'):
    os.makedirs('sentbox')
if not path.exists('receivedbox'):
    os.makedirs('receivedbox')

window = Tk()
window.geometry("250x265")
account = "xyz@gmail.com"


class mail:
    def __init__(self):
        self.prior = IntVar()
        self.toget = StringVar()
        self.content = StringVar()
        self.user = StringVar()
        self.pwd = StringVar()
        self.choose = StringVar()
        self.d1 = {"aryann": "1234", "dc": "normie", "naman": "666", "": ""}

    def create(self):
        global ff
        ff = Frame(window)
        self.incorrectemail = ttk.Label(ff, text="Incorrect email!")
        self.enteremail = ttk.Label(ff, text="Enter an email!")
        self.emptybody = ttk.Label(ff, text="Cannot be empty!")
        self.invalid = Label(
            ff, text="Invalid Username/Password pair. Try again.", fg="red")
        self.alreadyexists = Label(ff, text="Username already exists!")
        self.registered = Label(ff, text="Registered! Try logging in!")
        self.lb1 = Listbox(ff)

    def die(self):
        ff.destroy()

    def clear(self):
        self.prior.set("")
        self.toget.set("")
        self.content.set("")

    def forgeterrors(self):
        enames = ['incorrectemail', 'enteremail', 'emptybody']
        for i in enames:
            exec("self.%s.grid_forget()" % i)

    def sendfunc(self):
        self.forgeterrors()
        dir = path.dirname(__file__)
        to = self.toget.get()
        if to:
            tmp = re.search("\w+@\w+.\w+", to)
            if tmp:
                ndir = path.join(dir, ("sentbox\\%s.txt" % to))
                content = contentbody.get('1.0', 'end')
                priority = self.prior.get()
                if content != "\n":
                    try:
                        f = open(ndir, 'r+')
                    except:
                        f = open(ndir, 'w+')
                    msg = ""
                    msg += "<from>" + account + "<priority>" + \
                        str(priority) + "<body>" + content
                    f.write(msg)
                    f.close()
                    contentbody.delete('1.0', 'end')
                else:
                    self.emptybody.grid()
            else:
                self.incorrectemail.grid()
        else:
            self.enteremail.grid()

    def send(self):
        self.die()
        self.create()
        ttk.Label(ff, text="To:").grid()
        ttk.Entry(ff, textvariable=self.toget).grid()

        global contentbody
        contentbody = Text(ff, height=10, width=30)
        contentbody.grid(padx=2)

        self.prior.set(1)
        ttk.Label(ff, text="Priority").grid()
        priorbox = ttk.Spinbox(
            ff, from_=0.0, to=4.0, textvariable=self.prior, wrap=True, width=5, state='readonly')
        priorbox.grid()
        ttk.Button(ff, text="Send", command=self.sendfunc).grid()

        ff.grid()

    def onselect(self, evt,):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.click = w.get(index)
        print('You selected item %d: "%s"' % (index, value))

    def edit1func(self):
        global s3
        s3 = p1 + "\\"+self.user.get()+"--" + self.choose.get() + ".txt"

        self.lb1.delete(0, END)
        l1.clear()

        with open(s3) as fc:
            for line in fc.readlines():
                s1 = line.split("\n")
                s2 = "".join(s1[0])
                s2 = s2.split("<body>")
                l1.append(s2[1])

        for f in l1:
            self.lb1.insert(END, f)

        self.lb1.bind('<<ListboxSelect>>', self.onselect)

    def edit1(self):
        self.die()
        self.create()
        self.user.set("abc@gmail.com")

        global p1
        p1 = os.getcwd()

        global l1
        files, l1 = [], []

        # r=root, d=directories, f = files
        for r, d, f in os.walk(p1+'\\sentbox'):
            for file in f:
                if '.txt' in file:
                    s1 = self.user.get() + "--"
                    if s1 in file:
                        s2 = file.split("--")
                        s3 = s2[1].split(".txt")
                        files.append(s3[0])

        ttk.Label(ff, text="Select Email ID").grid(row=0, column=0)
        self.lb1.grid(row=3, column=0)

        ttk.Label(ff, text="Select Mail").grid(row=2, column=0)
        OptionMenu(ff, self.choose, *files,
                   command=lambda _: self.edit1func()).grid(row=1, column=0)

        ttk.Button(ff, text="Edit", command=self.edit2).grid()

        ff.grid()

    def edit2func(self):
        l2 = []
        with open(s3) as fc:
            for line in fc.readlines():
                print(line)
                if self.click not in line:
                    l2.append(line)
                else:
                    l2.append("<priority>"+str(self.prior.get()) +
                              "<body>"+cb.get('1.0', 'end'))
        fc.close()

        print(l2)

        fc = open(s3, "w")
        for i in l2:
            fc.write(i)
        fc.close()

    def edit2(self):
        self.die()
        self.create()

        ttk.Label(ff, text="New Message").grid(row=0, column=0)
        ttk.Label(ff, text=f"To:  {self.choose.get()}").grid(row=1, column=0)

        global cb
        cb = Text(ff, height=10, width=30)
        cb.grid(padx=2)

        self.prior.set(1)
        ttk.Label(ff, text="Priority").grid()
        priorbox = ttk.Spinbox(
            ff, from_=0.0, to=4.0, textvariable=self.prior, wrap=True, width=5, state='readonly')
        priorbox.grid()

        ttk.Button(ff, text="Save", command=self.edit2func).grid()

        ff.grid()

    def home(self):
        self.die()
        self.create()

        Button(ff, text="Send", command=self.send).grid(row=0, column=0)
        Button(ff, text="Edit", command=self.edit1).grid(row=0, column=1)
        Button(ff, text="Read", command=self.read).grid(row=0, column=2)

        ff.grid()

    def validatelogin(self):
        u1 = self.user.get()
        pwd = self.pwd.get()

        if self.d1[u1] == pwd:
            self.home()
        else:
            self.invalid.grid()

    def validatesignup(self):
        self.forgeterrors()
        u = self.user.get()
        p = self.pwd.get()

        if u == "" or p == "":
            self.emptybody.grid()
        elif u in self.d1:
            self.alreadyexists.grid()
        else:
            self.registered.grid()
            self.login()

    def register(self):
        self.die()
        self.create()

        Label(ff, text="Enter New Username").grid(row=0, column=0)
        Label(ff, text="Last New Password").grid(row=1, column=0)
        Entry(ff, textvariable=self.user).grid(row=0, column=1)
        Entry(ff, textvariable=self.pwd).grid(row=1, column=1)
        Button(ff, text="Register", command=self.validatesignup).grid(
            row=4, column=0)

        ff.grid()

    def login(self):
        self.die()
        self.create()

        Label(ff, text="Username").grid(row=0, column=0)
        Label(ff, text="Password").grid(row=1, column=0)

        ttk.Entry(ff, textvariable=self.user).grid(row=0, column=1)
        ttk.Entry(ff, textvariable=self.pwd, show="*").grid(row=1, column=1)

        Button(ff, text="Login", command=self.validatelogin).grid(
            row=2, column=0)
        Button(ff, text="Register", command=self.register).grid(row=2, column=1)

        ff.grid()

    def read(self):
        self.die()
        self.create()
        self.user.set('enji@gmail.com')
        Label(ff, text="INBOX").grid()
        inbox = ttk.Combobox()
        p1 = os.getcwd()
        senders_emails = []
        file_names = []
        for r, d, f in os.walk(p1 + '\\sentbox'):
            for file in f:
                if '.txt' in file:
                    s1 = "--"+self.user.get()
                    if s1 in file:
                        s2 = file.split("--")
                        senders_emails.append(s2[0])
                        file_names.append(file)

        def readmessage():
            print(file_names)
            msg.config(text="THIS IS THE TEXT IN THE MESSAGE")
            sender = inbox.get()
            file_to_display = file_names[senders_emails.index(sender)]
            print(file_to_display)

        print(file_names)
        inbox['values'] = senders_emails
        inbox.grid()
        Button(ff, text="READ MESSAGE",
               command=readmessage).grid(row=2, column=0)
        msg = Label(ff, text="Username")
        msg.grid()
        ff.grid()


obj = mail()
obj.create()
obj.login()
window.mainloop()
