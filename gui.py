from tkinter import *

win=Tk() #creating the main window and storing the window object in 'win'
win.title('STAT: Snazzy Tabletop Assistant Tracker')
win.geometry('350x525')

mn = Menu(win) 
win.config(menu=mn) 

pw = PanedWindow()

file_menu = Menu(mn) 
mn.add_cascade(label='File', menu=file_menu, activebackground="blue") 
file_menu.add_command(label='Create Game') 
file_menu.add_command(label='Load Game') 
file_menu.add_separator() 
file_menu.add_command(label='New Save') 
file_menu.add_command(label='Load Save')  
file_menu.add_separator() 
file_menu.add_command(label='Exit', command=win.quit) 

help_menu = Menu(mn) 
mn.add_cascade(label='Help', menu=help_menu) 
help_menu.add_command(label='Tutorials')
help_menu.add_command(label='Feedback') 
help_menu.add_command(label='Contact') 

pw.pack(fill = 'both', expand = 1)
w1 = Scrollbar(win)
w1.pack(side = RIGHT, fill = 'y')
list_1 = Listbox(win, yscrollcommand = w1.set)
for i in range(20):
    list_1.insert(END, 'ListItem ' + str(i))
list_1.pack( side = LEFT, fill = BOTH)
w1.config( command = list_1.yview)

pw.add(w1)


tl= Toplevel() 
tl.title('Greetings') 
txt=Text(tl, heigh=5, width=45)
txt.pack()
txt.insert(INSERT,"Hello!\n")
txt.insert(END, 'We begin the program here. :)\n')

win.mainloop() #running the loop that works as a trigger