from tkinter import *

root = Tk()
root.title("Title")
root.geometry("879x746")
root.configure(background="black")

background_image = PhotoImage(file="login")

background = Label(root, image=background_image, bd=0)
background.pack()

root.mainloop()