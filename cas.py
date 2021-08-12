from tkinter import *
from tkinter.messagebox import *
from sqlite3 import *
from tkinter.scrolledtext import *
import requests
import bs4
import matplotlib.pyplot as plt
import pandas as pd


try:
	webaddress = "https://www.brainyquote.com/quote_of_the_day"
	res = requests.get(webaddress)
	print(res)

	data = bs4.BeautifulSoup(res.text, 'html.parser')
	#print(data)

	info = data.find('img', {'class' : 'p-qotd'})
	#print(info)

	qotd = info['alt']
	#print(qotd)	
except Exception as e:
	print(e)
	

splash = Tk()
splash.after(3000, splash.destroy)
splash.geometry("1200x700+100+50")
filename = PhotoImage(file = "splash.png")
c = Canvas(splash,width = 1200,height = 700)
c.create_image(600 , 350, image = filename)
c.create_text(850, 500, text='Current Awareness System \n~By \nGayatri Nadar \nVaibhavi Kharkar \nHarshada Khairnar \nSnehal Dagade', font=('calisto mt', 40, 'bold'), fill ='black')
c.pack()
splash.mainloop()


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


def open_weather():
        weather_window.deiconify()
        main_window.withdraw()

def open_corona():
        corona_window.deiconify()
        main_window.withdraw()

def open_news():
        news_window.deiconify()
        main_window.withdraw()

def open_bitcoin():
        bitcoin_window.deiconify()
        main_window.withdraw()


def logout():
        status = askyesno("Quit" , "Do you really want to logout")
        if status:
                main_window.withdraw()
                welcome_page.deiconify()
                welcome_page_ent_username.focus()
                welcome_page_ent_username.delete(0, END)
                welcome_page_ent_password.delete(0, END)        

def search_weather():
        try:
                city_name = weather_window_ent_city.get()
                a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
                a2 = "&q=" + city_name
                a3 = "&appid=" + "c6e315d09197cec231495138183954bd"
	
                webaddress = a1 + a2 + a3
                res = requests.get(webaddress)
                print(res)

                data = res.json()

                temp = data['main']['temp']
                weather = data['weather']
                climate = (weather[0]['description'])
                wind_speed = data['wind']['speed']
                humidity = data['main']['humidity']
                temperature.set("Temperature: " + str(temp) + "\u00B0" + " C" + "\nClimate: " + climate +
                                "\nWind Speed :" + str(wind_speed) + "\nHumidity :" + str(humidity))
	
        except Exception as e:
                print("issue", e)
                
def back_weather():
        main_window.deiconify()
        weather_window.withdraw()

def refresh_weather():
        weather_window_ent_city.delete(0, END)
        temperature.set("")

def search_corona():
        try:
                country_name = corona_window_ent_country.get()
                wa = "https://www.worldometers.info/coronavirus/country/" + country_name + "/"
                res = requests.get(wa)
                #print(res)

                data = bs4.BeautifulSoup(res.text,"html.parser")
                #print(data)

                info = data.find_all("div" , {"class" ,"maincounter-number"})
                #print(info)
	
                tc = info[0].span.text
	
                td = info[1].span.text

                tr = info[2].span.text

                covid_msg = "Total count of " + country_name + " is " + tc + "\n\nTotal death are " + td + "\n\nTotal recovery is " + tr
                result.set(covid_msg)

        except Exception as e:
                print("Issue ",e)

def back_corona():
        main_window.deiconify()
        corona_window.withdraw()

def refresh_corona():
        corona_window_ent_country.delete(0, END)
        result.set("")

def search_bitcoin():
        try:
                wa = "https://api.coindesk.com/v1/bpi/currentprice.json"
                res = requests.get(wa)
                print(res)
	
                data = res.json()
	
                usd_rate = data['bpi']['USD']['rate']

                gbp_rate = data['bpi']['GBP']['rate']

                eur_rate = data['bpi']['EUR']['rate']

                if str(k.get()) == "1":
                        msg = ("Current USD rate is : "+usd_rate)
                        
                elif str(k.get()) == "2":
                        msg = ("Current GBP rate is : "+gbp_rate)
                        
                else:
                        msg = ("Current EURO rate is : "+eur_rate)
                        
                

                bitcoin_result.set(str(msg))


        except Exception as e:
                print("Issue  " , e)

def back_bitcoin():
        main_window.deiconify()
        bitcoin_window.withdraw()

def refresh_bitcoin():
        bitcoin_result.set("")

def search_news():
        res = clicked.get()
        print(res)
        try:
                option = clicked.get()
                a1 = "https://newsapi.org/v2/top-headlines"
                a2 = '?sources=' + option
                a3 = "&apiKey=" + 'ae9ed9a8389b41e096d315477b6d4d09'
                wa = a1 + a2 + a3

                res = requests.get(wa)
                data = res.json()
                articles = data['articles']
                # print(info)

                for article in articles:
                        content = []
                        title = article['title']

                for i in range(10):
                        news = data['articles'][i]['title']
                        n_result = ("News " + str(i+1)+" : "+news+"\n\n")
                        news_window_st_data.insert(INSERT,n_result)
        except Exception as e:
                print("Issue  " , e)

def back_news():
        main_window.deiconify()
        news_window.withdraw()

def refresh_news():
        news_window_st_data.delete("1.0", "end")

def petrol():
        data = pd.read_csv("petrol_prices.csv")
        #print(data)
        city = data['STATES'].tolist()
        prices = data['PRICES'].tolist()
        mng = plt.get_current_fig_manager()
        mng.window.state("zoomed")
        #plt.figure(figsize=(80,60))
        plt.bar(city, prices, color=['green', 'red', 'blue', 'yellow'])
        plt.xlabel("STATES")
        plt.ylabel("PRICES")
        plt.title("PETROL PRICES")
        plt.show()

#------------------------------------------------------WELCOME PAGE-------------------------------------------------------------------

welcome_page = Tk()
welcome_page.title("Current Awareness System")
welcome_page.geometry("1200x700+100+50")
welcome_page.resizable(True,True)

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

def wd():
	if askokcancel("Quit" , "Do you really want to quit"):
		welcome_page.destroy()

welcome_page.protocol("WM_DELETE_WINDOW",wd)


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

#------------------------------------------------------MAIN PAGE-------------------------------------------------------------------

main_window = Toplevel(welcome_page)
main_window.title("Main Page")
main_window.geometry("1000x748+400+0")

image3 = PhotoImage(file = r"D:\Python\TEC Python Project\m1.png")
Image_lbl = Label(main_window, image = image3)
Image_lbl.place(x=0, y=0)

welcome = StringVar()
main_window_lbl_welcome = Label(main_window, textvariable = welcome  , font = ("calisto mt", 29, "bold"), bg="#ccff99", borderwidth=5)
main_window_btn_weather = Button(main_window, text="WEATHER", width=13, font = f1, borderwidth=10,bg ="#66cc00" , fg="black", command=open_weather)
main_window_btn_corona = Button(main_window, text="CORONA", width=13, font = f1, borderwidth=10,bg ="#66cc00" , fg="black", command=open_corona)
main_window_btn_news = Button(main_window, text="NEWS", width=13, font = f1, borderwidth=10,bg ="#66cc00" , fg="black", command=open_news)
main_window_btn_bitcoin = Button(main_window, text="BITCOIN", width=13,font = f1, borderwidth=10,bg ="#66cc00" , fg="black", command=open_bitcoin)
main_window_btn_pp = Button(main_window, text="PETROL PRICES", width=13, font = f1, borderwidth=10,bg ="#66cc00" , fg="black", command=petrol)
main_window_btn_back = Button(main_window, text="LOGOUT", width=13, font = f1, borderwidth=10,bg ="#66cc00" , fg="black", command=logout)
main_window_lbl_qotd = Label(main_window, text="Quote: " + qotd  , font = ("lucida calligraphy", 17, "bold"), borderwidth=2,
                             relief="solid", wraplength=750, bg="lightblue")

main_window_lbl_qotd.place(x=150, y=650)

main_window_lbl_welcome.place(x=280, y=40)
main_window_btn_weather.place(x=380, y=130)
main_window_btn_corona.place(x=380, y=210)
main_window_btn_news.place(x=380, y=290)
main_window_btn_bitcoin.place(x=380, y=370)
main_window_btn_pp.place(x=380, y=450)
main_window_btn_back.place(x=380, y=530)
main_window.withdraw()

#------------------------------------------------------WEATHER UPDATE-------------------------------------------------------------------

temperature = StringVar()
weather_window = Toplevel(welcome_page)
weather_window.title("Weather Update")
weather_window.geometry("1200x700+100+50")
weather_window.resizable(0,0)

w_photo1 = PhotoImage(file ="w1.png")

C3 = Canvas(weather_window,width = 1200,height=700)
C3.create_image(600,350,image=w_photo1)

temperature = StringVar()
C3.create_text(600,40,text="WEATHER UPDATE", font = ("courier", 35, "bold","underline"),fill = "dark blue")
C3.create_text(600,140, text="Enter City", font=("Calisto MT", 30, "bold"),fill = "black")
weather_window_ent_city = Entry(weather_window, width = 28 ,font = f)
weather_window_btn_search = Button(weather_window, text="SEARCH",borderwidth=10, font=f1, bg="#77b300", command=search_weather)
weather_window_lbl_result = Label(weather_window, textvariable = temperature , font = f,bg = "light blue")
weather_window_btn_back = Button(weather_window, text="BACK",width = 8, borderwidth=10, font=f1, bg="light blue", command=back_weather)
weather_window_btn_refresh = Button(weather_window, text="REFRESH",width = 8,borderwidth=10, font=f1, bg="light blue", command=refresh_weather)

weather_window_ent_city.place(x=350, y=200)
weather_window_btn_search.place(x=550, y=300)
weather_window_lbl_result.place(x=400, y=400)
weather_window_btn_back.place(x=150, y=600)
weather_window_btn_refresh.place(x=820, y=600)
C3.pack(expand = True)

weather_window.withdraw()

#------------------------------------------------------CORONA COUNTER-------------------------------------------------------------------
corona_window = Toplevel(welcome_page)
corona_window.title("Corona Counter")
corona_window.geometry("1200x700+100+50")
corona_window.resizable(0,0)

c_photo1 = PhotoImage(file ="c1.png")

C4 = Canvas(corona_window,width = 1200,height=700)
C4.create_image(600,350,image=c_photo1)

result = StringVar()
C4.create_text(600,40, text="CORONA COUNTER", fill="#004d00", font = ("courier",35, "bold","underline") )
C4.create_text(600,140, text="Enter Country Name ",fill="black", font=f)
corona_window_ent_country = Entry(corona_window,width = 28 , font = f)
corona_window_btn_search = Button(corona_window, text="SEARCH",borderwidth=10, font=f1,bg="#66ffb3", command=search_corona)
corona_window_lbl_result = Label(corona_window, font = ("calisto mt", 23 , "bold"), textvariable = result, bg="#66ffb3")
corona_window_btn_back = Button(corona_window, text="BACK",width = 8, borderwidth=10, font=f1, bg="#66ffb3", command = back_corona)
corona_window_btn_refresh = Button(corona_window, text="REFRESH",width = 8, borderwidth=10, font=f1, bg="#66ffb3", command=refresh_corona)

corona_window_ent_country.place(x=350, y=200)
corona_window_btn_search.place(x=550, y=300)
corona_window_lbl_result.place(x=400, y=400)
corona_window_btn_back.place(x=150, y=600)
corona_window_btn_refresh.place(x=820, y=600)
C4.pack(expand = True)

corona_window.withdraw()

#------------------------------------------------------BITCOIN PAGE-------------------------------------------------------------------

bitcoin_window = Toplevel(welcome_page)
bitcoin_window.title("Bitcoin Update")
bitcoin_window.geometry("1200x700+100+50")

b_photo1 = PhotoImage(file ="b.png")

C5 = Canvas(bitcoin_window,width = 1200,height=700)
C5.create_image(600,350,image=b_photo1)

k = IntVar()
k.set(1)
bitcoin_result = StringVar()
C5.create_text(600,60, text="BITCOIN UPDATES",font = ("calisto mt", 35, "bold","underline"),fill="white")
C5.create_text(600,140, text="Select desired option to know the rate",font = ("calisto mt",30, "bold"),fill="white")
bitcoin_window_rb_us = Radiobutton(bitcoin_window, text = "United States Dollar" , font = ("calisto mt",25, "bold"), variable = k ,value = 1,bg="black",fg="white")
bitcoin_window_rb_gbp = Radiobutton(bitcoin_window, text = "British Pound Sterling" , font = ("calisto mt",25, "bold"),variable = k ,value = 2,bg="black",fg="white")                                   
bitcoin_window_rb_euro = Radiobutton(bitcoin_window, text = "European Union" , font = ("calisto mt",25, "bold"), variable = k ,value = 3,bg="black",fg="white")                                   
bitcoin_window_btn_search = Button(bitcoin_window , text = "SEARCH" ,borderwidth=10, font =f1,bg = "grey",fg = "black",command = search_bitcoin)
bitcoin_window_lbl_result = Label(bitcoin_window ,font = f , textvariable = bitcoin_result,bg = "black",fg="white")
bitcoin_window_btn_back = Button(bitcoin_window, text="BACK", borderwidth=10, font=f1, bg = "grey",fg = "black" , command = back_bitcoin)
bitcoin_window_btn_refresh = Button(bitcoin_window, text="REFRESH", borderwidth=10, font=f1,command = refresh_bitcoin,bg = "grey",fg = "black")

bitcoin_window_rb_us.place(x=2,y=250)
bitcoin_window_rb_gbp.place(x=2,y=300)
bitcoin_window_rb_euro.place(x=2,y=350)
bitcoin_window_btn_search.place(x=550,y=400)
bitcoin_window_lbl_result.place(x=300,y=500)
bitcoin_window_btn_back.place(x=150,y=600)
bitcoin_window_btn_refresh.place(x=820,y=600)

C5.pack(expand = True)
bitcoin_window.withdraw()

#------------------------------------------------------NEWS PAGE-------------------------------------------------------------------

news_window = Toplevel(welcome_page)
news_window.title("News Update")
news_window.geometry("1200x700+100+50")
news_window.resizable(0,0)

i1 = PhotoImage(file = r"n1.png")
Image_lbl = Label(news_window, image = i1)
Image_lbl.place(x=0, y=0)


news_window_lbl_title = Label(news_window, text="NEWS UPDATES",font = ("calisto mt", 35, "bold"), borderwidth=2,relief="solid")
news_result = StringVar()
clicked = StringVar()		#this is python variable
options = [
    "the-times-of-india",
    "google-news",
    "espn-cric-info",
    "the-hindu"
]
clicked.set(options[0])

global dropdown		
dropdown = OptionMenu(news_window, clicked,*options)
dropdown.config(width=16, font=('calisto mt', 25, 'bold'),bg="white")

news_window_btn_search = Button(news_window , text = "SEARCH" , font = f1,borderwidth = 10 ,bg = "grey",fg = "black", command = search_news)
news_window_st_data = ScrolledText(news_window,width =80,height = 15 , font = ('calisto mt', 20, 'bold'),wrap = WORD, bg = "black",fg="white")
news_window_btn_back = Button(news_window, text="BACK", borderwidth=10, font = f1, bg = "grey",fg = "black", command = back_news)
news_window_refresh_back = Button(news_window, text="REFRESH", borderwidth=10, font = f1, bg = "grey",fg = "black", command = refresh_news)


news_window_lbl_title.pack(pady=10)
dropdown.pack(pady=15)
news_window_btn_search.pack(pady = 10)
news_window_st_data.pack(pady=5)
news_window_btn_back.place(x=50,y=20)
news_window_refresh_back.place(x=960,y=20)

news_window.withdraw()

welcome_page.mainloop()
