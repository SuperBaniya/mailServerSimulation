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
if not path.isfile("accounts.txt"):
    with open(path.join(os.getcwd(), "accounts.txt"), 'w') as _:
        pass

l1 = []
with open("accounts.txt") as fc:
    for line in fc.readlines():
        l1.append(line)

window = Tk()
window.geometry("250x400")
window.resizable(width=False, height=False)
ff = Frame(window)


class mail:
    def __init__(self):
        global ff
        self.prior = IntVar()
        self.toget = StringVar()
        self.content = StringVar()
        self.sub = StringVar()
        self.user = StringVar()
        self.pwd = StringVar()
        self.choose = StringVar()
        self.backbutton = ttk.Button(window)

    def backButton(self, cmd):
        self.backbutton.destroy()
        self.backbutton = ttk.Button(window, text="Back", command=cmd)
        self.backbutton.grid(sticky=W)

    def die(self):
        ff.destroy()
        self.backbutton.destroy()

    def create(self):
        self.die()
        global ff
        ff = Frame(window)
        self.incorrectemail = ttk.Label(ff, text="Incorrect email!", font=("Calibri", 12))
        self.enteremail = ttk.Label(ff, text="Enter an email!", font=("Calibri", 12))
        self.emptybody = ttk.Label(ff, text="Cannot be empty!", font=("Calibri", 12))
        self.invalidreg = ttk.Label(ff, text="Invalid Email ID", font=("Calibri", 12))
        self.invalid = Label(
            ff, text="Invalid Email/Password", fg="red")
        self.alreadyexists = Label(ff, text="Username already exists!", font=("Calibri", 12))
        self.registered = Label(ff, text="Registered! Try logging in!", font=("Calibri", 12))
        self.lb1 = Listbox(ff, width=25)

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
        x = self.user.get()
        if to:
            tmp = re.search("(\w+\.?)+@\w +.\w +", to)
            if tmp:
                ndir = path.join(dir, f"sentbox\\{x}--{to}.txt")
                content = contentbody.get('1.0', 'end')
                priority = self.prior.get()
                if content != "\n":
                    try:
                        f = open(ndir, 'r+')
                    except:
                        f = open(ndir, 'w+')
                    msg = ""
                    msg += "<priority>" + \
                           str(priority) + "<subject>" + self.sub.get() + "<body>" + content
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
        self.backButton(self.home)

        ttk.Label(ff, text="To:", font=("Calibri", 12)).grid()
        ttk.Entry(ff, textvariable=self.toget).grid()

        ttk.Label(ff, text="Subject:", font=("Calibri", 12)).grid()
        ttk.Entry(ff, textvariable=self.sub).grid()

        ttk.Label(ff, text="Content:", font=("Calibri", 12)).grid()
        global contentbody
        contentbody = Text(ff, height=10, width=29)
        contentbody.grid(padx=6)

        self.prior.set(1)
        ttk.Label(ff, text="Priority", font=("Calibri", 12)).grid()
        priorbox = ttk.Spinbox(
            ff, from_=0.0, to=4.0, textvariable=self.prior, wrap=True, width=5, state='readonly')
        priorbox.grid()
        ttk.Button(ff, text="Send", command=self.sendfunc).grid(pady=2)

        ff.grid()

    def onselect(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.click = w.get(index)
        self.editbody = value

    def edit1func(self):
        global s3
        s3 = p1 + "\\sentbox\\" + self.user.get() + "--" + self.choose.get() + ".txt"

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
        self.backButton(self.home)

        global p1
        p1 = os.getcwd()

        global l1
        files, l1 = [], []

        # r=root, d=directories, f = files
        for r, d, f in os.walk(p1 + '\\sentbox'):
            for file in f:
                if '.txt' in file:
                    s1 = self.user.get() + "--"
                    if s1 in file:
                        s2 = file.split("--")
                        s3 = s2[1].split(".txt")
                        files.append(s3[0])

        ttk.Label(ff, text="Select Email ID", font=("Calibri", 12)).grid(row=0, column=0)
        self.lb1.grid(row=3, column=0)

        ttk.Label(ff, text="Select Mail", font=("Calibri", 12)).grid(row=2, column=0)
        ttk.OptionMenu(ff, self.choose, "Select one", *files,
                       command=lambda _: self.edit1func()).grid(row=1, column=0)

        ttk.Button(ff, text="Edit", command=self.edit2).grid(pady=5)

        ff.grid(padx=36, pady=30)

    def edit2func(self):
        l2 = []
        with open(s3) as fc:
            for line in fc.readlines():
                if self.click not in line:
                    l2.append(line)
                else:
                    l2.append("<priority>" + str(self.prior.get()) +
                              "<body>" + cb.get('1.0', 'end'))
        fc.close()

        fc = open(s3, "w")
        for i in l2:
            fc.write(i)
        fc.close()

    def edit2(self):
        self.die()
        self.create()
        self.backButton(self.edit1)

        ttk.Label(ff, text="Edit Message", font=("Calibri", 12)).grid(row=0, column=0)
        ttk.Label(ff, text=f"To:  {self.choose.get()}", font=("Calibri", 12)).grid(row=1, column=0)

        global cb
        cb = Text(ff, height=10, width=29)
        cb.insert(END, self.editbody)
        cb.grid(padx=6)

        self.prior.set(1)
        ttk.Label(ff, text="Priority", font=("Calibri", 12)).grid()
        priorbox = ttk.Spinbox(
            ff, from_=0.0, to=4.0, textvariable=self.prior, wrap=True, width=5, state='readonly')
        priorbox.grid()

        ttk.Button(ff, text="Save", command=self.edit2func).grid(pady=5)

        ff.grid(pady=2)

    def home(self):
        self.die()
        self.create()
        self.backButton(self.login)

        Button(ff, text="Send", command=self.send, height=2, width=8).grid(pady=5)
        Button(ff, text="Edit", command=self.edit1, height=2, width=8).grid(pady=5)
        Button(ff, text="Read", command=self.read, height=2, width=8).grid(pady=5)
        ff.grid(padx=90, pady=75)

    def validatelogin(self):
        u1 = self.user.get()
        pwd = self.pwd.get()
        ctr = 0

        for i in l1:
            if u1 in i and pwd in i:
                ctr = 1
                break

        if ctr == 0:
            self.invalid.grid()
        else:
            self.home()

    def validatesignup(self):
        self.forgeterrors()
        u = self.user.get()
        p = self.pwd.get()

        if u == "" or p == "":
            self.emptybody.grid()
        elif u in l1:
            self.alreadyexists.grid()
        elif not re.search("(\w+\.?)+@\w+.\w+", u):
            self.invalidreg.grid()
        else:
            l1.append("\n" + u + " " + p)
            f = open("accounts.txt", "w")
            for i in l1:
                f.write(i)
            f.close()
            self.login()

    def register(self):
        self.die()
        self.create()
        self.backButton(self.login)

        Label(ff, text="Enter New Email ID", font=("Calibri", 12)).grid()
        ttk.Entry(ff, textvariable=self.user).grid()
        Label(ff, text="Enter New Password", font=("Calibri", 12)).grid()

        ttk.Entry(ff, textvariable=self.pwd).grid()
        Button(ff, text="Register", command=self.validatesignup, height=2, width=8).grid(pady=5)

        ff.grid(padx=50, pady=60)

    def login(self):
        self.die()
        self.create()

        Label(ff, text="Email ID", font=("Calibri", 12)).grid(pady=5)
        ttk.Entry(ff, textvariable=self.user).grid()
        Label(ff, text="Password", font=("Calibri", 12)).grid(pady=5)
        ttk.Entry(ff, textvariable=self.pwd, show="*").grid()

        bframe = Frame(ff)
        Button(bframe, text="Login", command=self.validatelogin, height=2, width=8).grid()
        Button(bframe, text="Register", command=self.register, height=2, width=8).grid(pady=6)
        bframe.grid(pady=6)
        ff.grid(padx=52, pady=40)

    def read(self):
        self.die()
        self.create()
        self.backButton(self.home)

        Label(ff, text="INBOX", font=("Calibri", 12)).grid()
        inbox = ttk.Combobox(ff)
        p1 = os.getcwd()
        senders_emails = []
        file_names = []
        for r, d, f in os.walk(p1 + '\\sentbox'):
            for file in f:
                if '.txt' in file:
                    s1 = "--" + self.user.get()
                    if s1 in file:
                        s2 = file.split("--")
                        senders_emails.append(s2[0])
                        # print(s1)
                        file_names.append(file)

        def readmessage():
            # print(file_names)
            sender = inbox.get()
            file_to_display = file_names[senders_emails.index(sender)]
            # print(file_to_display)
            lines = []
            with open('sentbox\\' + file_to_display) as fc:
                for line in fc.readlines():
                    l = line.split("<priority>")[1].split("<body>")
                    lines.append(l[1])
                # print("".join(lines))

            msg.config(text="".join(lines))
            os.replace(os.getcwd() + "\\sentbox\\" + file_to_display,
                       os.getcwd() + "\\receivedbox\\" + file_to_display)

        # print(file_names)
        inbox['values'] = senders_emails
        inbox.grid()
        Button(ff, text="Read Message",
               command=readmessage).grid(row=2, column=0, pady=3)
        msg = Label(ff, text="Username", font=("Calibri", 12))
        msg.grid()
        ff.grid(padx=40)


obj = mail()
obj.create()
obj.login()
window.mainloop()
