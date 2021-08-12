from tkinter import *
from tkinter.messagebox import *
from sqlite3 import *
import requests
import bs4



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

def back_signup():
	welcome_page.deiconify()
	signup_window.withdraw()

def done_signup():
	con = None
	try:
		con = connect("cas.db")
		cursor = con.cursor()
		sql = "insert into user values('%s', '%s', '%s', '%s')"

		if len(signup_window_ent_name.get()) == 0:
			showerror("Failure","Please enter name")
			signup_window_ent_name.delete(0, END)
			signup_window_ent_name.focus()

		elif len(signup_window_ent_name.get()) < 2 or ((((signup_window_ent_name.get()).replace(" ","")).isalpha())==False): 
			showerror("Failure","Please enter name containing only alphabets with minimum two letters")
			add_window_ent_name.delete(0, END)
			add_window_ent_name.focus()
		else:
			name = signup_window_ent_name.get()
			email = signup_window_ent_email.get()
			username = signup_window_ent_username.get()
			password = signup_window_ent_password.get()
			cursor.execute(sql % (name, email, username, password))
			con.commit()
			showinfo("Success", "Record added")
			signup_window_ent_name.delete(0, END)
			signup_window_ent_email.delete(0, END)
			signup_window_ent_username.delete(0, END)
			signup_window_ent_password.delete(0, END)
			signup_window_ent_name.focus()
			welcome_page.deiconify()
			signup_window.withdraw()		
		
	except Exception as e:
		showerror("Failure", e)

	finally:
		if con is not None:
			con.close()


#------------------------------------------------------WELCOME PAGE-------------------------------------------------------------------

welcome_page = Tk()
welcome_page.title("Current Awareness System")
welcome_page.geometry("1200x700+100+50")

pic1 = PhotoImage(file ="n2.png")
pic2 = PhotoImage(file ="l_lbl.png")
pic3 = PhotoImage(file ="user_logo.png")
pic4 = PhotoImage(file ="pass_logo.png")

f = ("Calisto MT", 26, "bold")
f1 = ("Calisto MT", 20, "bold")

C1 = Canvas(welcome_page,width = 1200,height=700)
C1.create_image(600,350,image=pic1)
C1.create_image(600,150,image=pic2)
C1.create_image(370,280,image=pic3)
C1.create_image(370,380,image=pic4)
 

C1.create_text(750,150, text="LOG-IN", font=("courier", 35, "bold"),fill = "black" )
C1.create_text(700,190,text="________________________________________",font = f,fill="black")
C1.create_text(500,280, text="USERNAME", font = ("Calisto MT", 20, "bold"),fill = "black")
welcome_page_ent_username = Entry(welcome_page,bd = 5, font = f,width=22)
C1.create_text(500,380, text="PASSWORD", font = ("Calisto MT", 20, "bold"),fill = "black")
welcome_page_ent_password = Entry(welcome_page,bd=5, font = f,width=22)
welcome_page_ent_password.configure(show="*")
welcome_page_btn_signup = Button(welcome_page, text="SIGNUP", font=("Calisto MT", 20, "bold"), command=signup, borderwidth=10,bg = "dark blue",fg="white")
welcome_page_btn_login = Button(welcome_page, text="LOGIN" , font=("Calisto MT", 20, "bold"), command=login,borderwidth=10,bg = "dark blue",fg="white")

welcome_page_ent_username.place(x=650, y=250)
welcome_page_ent_password.place(x=650, y=350)
welcome_page_btn_signup.place(x=450, y=480)
welcome_page_btn_login.place(x=820, y=480)
C1.pack(expand=True)


#------------------------------------------------------SIGNUP PAGE-------------------------------------------------------------------

signup_window = Toplevel(welcome_page)
signup_window.title("Sign Up Page")
signup_window.geometry("1200x700+100+50")

photo1 = PhotoImage(file ="dn3.png")
photo2 = PhotoImage(file ="s_lbl.png")
photo3 = PhotoImage(file ="name.png")
photo4 = PhotoImage(file ="email.png")
photo5 = PhotoImage(file ="user_logo.png")
photo6 = PhotoImage(file ="pass_logo.png")

C2 = Canvas(signup_window,width = 1200,height=700)
C2.create_image(600,350,image=photo1)
C2.create_image(580,160,image=photo2)
C2.create_image(380,250,image=photo3)
C2.create_image(380,330,image=photo4)
C2.create_image(380,410,image=photo5)
C2.create_image(380,490,image=photo6)


C2.create_text(750,160,text="SIGN-UP PAGE", font=("courier", 25, "bold"),fill="dark blue")
C2.create_text(730,180,text="_________________________________________",font = f,fill="black")
C2.create_text(500,250,text="Name", font=f,fill="black")
signup_window_ent_name = Entry(signup_window,bd=5, font = f,width = 22)
C2.create_text(500,330, text="Email", font=f,fill="black")
signup_window_ent_email = Entry(signup_window,bd=5, font = f,width = 22)
C2.create_text(500,410, text="Username", font=f,fill="black")
signup_window_ent_username = Entry(signup_window,bd=5, font = f,width = 22)
C2.create_text(500,490, text="Password", font=f,fill="black")
signup_window_ent_password = Entry(signup_window,bd=5, font = f,width = 22)
signup_window_ent_password.configure(show="*")
signup_window_btn_back = Button(signup_window, text="BACK", borderwidth=10,font=f1, command=back_signup,bg = "dark blue",fg="white")
signup_window_btn_signup = Button(signup_window, text="DONE", borderwidth=10,font=f1, command=done_signup,bg = "dark blue",fg ="white")


signup_window_ent_name.place(x=650, y=230)
signup_window_ent_email.place(x=650, y=310)
signup_window_ent_username.place(x=650, y=390) 
signup_window_ent_password.place(x=650, y=470)
signup_window_btn_back.place(x=590, y=550)
signup_window_btn_signup.place(x=960, y=550)
C2.pack(expand = True)

signup_window.withdraw()


welcome_page.mainloop()
