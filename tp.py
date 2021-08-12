from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image

def signup():
	signup_window.deiconify()
	welcome_page.withdraw()

def login():
	con = None
	try:
		con = connect("cas.db")
		cursor = con.cursor()
		sql = "select username, password from user where username='%s' and password='%s'"
		username = welcome_page_ent_username.get()
		welcome.set("Welcome " + str(username) + "!!")
		password = welcome_page_ent_password.get()
		cursor.execute(sql % (username, password))
		data = cursor.fetchall()
		if len(data) > 0: 
			showinfo("Success", "Login Successful!")
			main_window.deiconify()
			welcome_page.withdraw()
		else:
			showerror("Failure", "Invalid Credentials")
			welcome_page_ent_username.delete(0, END)
			welcome_page_ent_password.delete(0, END)
		
	except Exception as e:
		showerror("Failure", e)

	finally:
		if con is not None:
			con.close()
    

welcome_page = Tk()
welcome_page.title("Current Awareness System")
welcome_page.geometry("800x538+400+100")
welcome_page.resizable(True,True)

pic1 = ImageTk.PhotoImage(file ="login.png")
pic2 = ImageTk.PhotoImage(file ="l_lbl.png")
pic3 = ImageTk.PhotoImage(file ="user_logo.png")
pic4 = ImageTk.PhotoImage(file ="pass_logo.png")

f = ("Calisto MT", 26, "bold")
f1 = ("calisto mt", 20, "bold")

C1 = Canvas(welcome_page,width = 800,height=538)
C1.create_image(400,280,image=pic1)
C1.create_image(300,150,image=pic2)
C1.create_image(115,250,image=pic3)
C1.create_image(115,350,image=pic4)
 

C1.create_text(410,60, text="CURRENT AWARENESS SYSTEM", font=("courier", 30, "bold"),fill="dark blue")
C1.create_text(400,80,text="________________________________________",font = f,fill="black")
C1.create_text(450,150, text="LOG-IN", font=("courier", 35, "bold"),fill = "black" )
C1.create_text(230,251, text="USERNAME", font = f1,fill = "black")
welcome_page_ent_username = Entry(welcome_page,bd = 5, font = f,width=22)
C1.create_text(230,350, text="PASSWORD", font = f1,fill = "black")
welcome_page_ent_password = Entry(welcome_page,bd=5, font = f,width=22)
welcome_page_ent_password.configure(show="*")
welcome_page_btn_signup = Button(welcome_page, text="SIGNUP", font=f1, borderwidth=10, command=signup,bg = "dark blue",fg="white")
welcome_page_btn_login = Button(welcome_page, text="LOGIN" , font=f1,borderwidth=10, command=login,bg = "dark blue",fg="white")

#welcome_page.columnconfigure(0,weight=1)
#welcome_page.rowconfigure(0,weight=1)

def resizer(e):
    global bg,resized_bg,new_bg
    #open image
    bg = Image.open("login.png")
    #resize it
    resized_bg = bg.resize((e.width,e.height),Image.ANTIALIAS)
    #define image again
    new_bg = ImageTk.PhotoImage(resized_bg)
    #place on canvas
    C1.create_image(400,280,image=new_bg)
    

my_sizegrip = ttk.Sizegrip(welcome_page)
my_sizegrip.pack(side="top",anchor=NE)
welcome_page_ent_username.place(x=350, y=220)
welcome_page_ent_password.place(x=350, y=330)
welcome_page_btn_signup.place(x=160, y=430)
welcome_page_btn_login.place(x=480, y=430)

welcome_page.bind('<Configure>',resizer)
C1.pack(expand=True)
