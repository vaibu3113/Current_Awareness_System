from tkinter import *
from tkinter import ttk
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

                covid_msg = "Total count of " + country_name + " is " + tc + "\n Total death are " + td + "\nTotal recovery is " + tr
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


f = ("Calisto MT", 26, "bold")
f1 = ("Calisto MT", 20, "bold")

bitcoin_window = Tk()
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
bitcoin_window_rb_gbp.place(x=2,y=290)
bitcoin_window_rb_euro.place(x=2,y=340)
bitcoin_window_btn_search.place(x=550,y=400)
bitcoin_window_lbl_result.place(x=300,y=500)
bitcoin_window_btn_back.place(x=150,y=600)
bitcoin_window_btn_refresh.place(x=820,y=600)

C5.pack(expand = True)
bitcoin_window.mainloop()

