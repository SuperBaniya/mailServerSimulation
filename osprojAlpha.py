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

window= Tk()
window.geometry("250x265")
mainframe=ttk.Frame()
account="xyz@gmail.com"


#------ErrorLabels----
incorrectemail=ttk.Label(mainframe, text="Incorrect email!")
enteremail=ttk.Label(mainframe, text="Enter an email!")
emptybody=ttk.Label(mainframe, text="Body cannot be empty!")
#--------

def forgetErrors():
    enames=['incorrectemail', 'enteremail', 'emptybody']
    for i in enames:
        exec("%s.grid_forget()"%i)
def send():
    forgetErrors()
    dir=path.dirname(__file__)
    to=toget.get()
    if to:
        tmp=re.search("\w+@\w+.\w+", to)
        if tmp:
            ndir=path.join(dir, ("sentbox\\%s.txt"%to))
            content=contentbody.get('1.0','end')
            priority=prior.get()
            if content!="\n":
                try:
                    f=open(ndir, 'r+')
                except:
                    f=open(ndir, 'w+')
                msg=""
                msg+="<from>" + account +"<priority>"+ str(priority) + "<body>" + content
                f.write(msg)
                f.close()
                contentbody.delete('1.0', 'end')
            else:
                emptybody.grid()
        else:
            incorrectemail.grid()
    else:
        enteremail.grid()
                
            
toget=StringVar()
tof=ttk.Frame(mainframe)
ttk.Label(tof, text="To:").grid()
t=ttk.Entry(tof, textvariable=toget)
t.grid(row=0, column=1)
tof.grid(pady=1)

contentbody=Text(mainframe, height=10, width=30)
contentbody.grid(padx=2)


prior=IntVar()
prior.set(1)
ttk.Label(mainframe, text="Priority").grid()
priorbox=ttk.Spinbox(mainframe, from_=0.0, to=4.0, textvariable= prior, wrap=True, width=5, state='readonly')
priorbox.grid()
ttk.Button(mainframe, text="Send", command=send).grid()

mainframe.grid()
