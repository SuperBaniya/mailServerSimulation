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

window = Tk()
window.geometry("250x265")
account = "xyz@gmail.com"


class mail:
    def __init__(self):
        self.prior = IntVar()
        self.toget = StringVar()
        self.content = StringVar()

    def create(self):
        global ff
        ff = Frame(window)
        self.incorrectemail = ttk.Label(ff, text="Incorrect email!")
        self.enteremail = ttk.Label(ff, text="Enter an email!")
        self.emptybody = ttk.Label(ff, text="Body cannot be empty!")

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
        print(to)
        if to:
            tmp = re.search("@(\w+\.)+\w+$", to)
            print(tmp)
            if tmp:
                ndir = path.join(dir, ("sentbox\\%s.txt" % to))
                content = contentbody.get('1.0', 'end')
                priority = self.prior.get()
                print(priority)
                print(content)
                if content != "\n":
                    try:
                        f = open(ndir, 'r+')
                    except:
                        f = open(ndir, 'w+')
                    msg = ""
                    msg += "<from>" + account + "<priority>" + str(priority) + "<body>" + content
                    print(msg)
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
        priorbox = ttk.Spinbox(ff, from_=0.0, to=4.0, textvariable=self.prior, wrap=True, width=5, state='readonly')
        priorbox.grid()
        ttk.Button(ff, text="Send", command=self.sendfunc).grid()

        ff.grid()


obj = mail()
obj.create()
obj.send()
# obj.home()
window.mainloop()
