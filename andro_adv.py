#importing needed libraries
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pyjokes
import requests
import time
import winsound
import wolframalpha
import smtplib
import json
from pyttsx3.drivers import sapi5
import pyautogui as pg
import speech_recognition as sr
from nsetools import Nse
from yahoo_fin import stock_info
import yfinance as yf
from googletrans import Translator
from ecapture import ecapture as ec

pg.FAILSAFE = False
os.system('CLS')


###########################################################################################################

#getting variables ready to rock:

#your email address line no. 
f = open("C:\\Users\\Administrator\\Desktop\\andro_variables\\email.txt", "r")
email=f.read()

#the password of above email  line no 
f = open("C:\\Users\\Administrator\\Desktop\\andro_variables\\password.txt", "r")
password=f.read()

#get an API key from https://newsapi.org,  line no 
#you can change news topic and number of headlines in line no
f = open("C:\\Users\\Administrator\\Desktop\\andro_variables\\newsapi.txt", "r")
newsapi=f.read()

f = open("C:\\Users\\Administrator\\Desktop\\andro_variables\\news_no.txt", "r")
news_no=f.read()

f = open("C:\\Users\\Administrator\\Desktop\\andro_variables\\news_topic.txt", "r")
news_topic=f.read()

#get an api key from https://fast2sms.com at line no 193
#read lines nos 
f = open("C:\\Users\\Administrator\\Desktop\\andro_variables\\smskey.txt", "r")
smskey=f.read()

#eg: andro
f = open("C:\\Users\\Administrator\\Desktop\\andro_variables\\appname.txt", "r")
appname=f.read()

#change your name in line nos
f = open("C:\\Users\\Administrator\\Desktop\\andro_variables\\yourname.txt", "r")
yourname=(str)(f.read())

#change your website address in line nos
f = open("C:\\Users\\Administrator\\Desktop\\andro_variables\\yourweb.txt", "r")
yourweb=f.read()

# the folder path where your music is stored
#line no: 356;  type in the position-1 (in number) of your mp3 file. Ex if music.mp3 is the fifth file in the folder, write 4
f = open("C:\\Users\\Administrator\\Desktop\\andro_variables\\music_dir.txt", "r")
music_dir=f.read()

#get your key from wolfram alpha in line no 417,493
f = open("C:\\Users\\Administrator\\Desktop\\andro_variables\\alpha.txt", "r")
alpha=f.read()

#get your key from https://openweather.org (verify your email atleast 3 hours in advance) in line no
f = open("C:\\Users\\Administrator\\Desktop\\andro_variables\\weather.txt", "r")
weather=f.read()

#get your key from https://ifttt.com/maker_webhooks --> documentation; in line no 531,535,539
f = open("C:\\Users\\Administrator\\Desktop\\andro_variables\\ifttt.txt", "r")
ifttt=f.read()

#get your key from https://ipstack.com/signup/free
f = open("C:\\Users\\Administrator\\Desktop\\andro_variables\\iplocation.txt", "r")
iplocation=f.read()

###########################################################################################################

# Setting up speaker defaults
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    engine.setProperty('rate', 145)

###########################################################################################################

# To take microphone input from the user and return string output
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")

    except:
        print("Please say that again.....")
        return "None"

    return query

###########################################################################################################

# Greeting message
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("Hi. I am Andro, Aditya's personal assistant. How may I serve you?")

###########################################################################################################

# setting up a simple splash screen
def splash_screen():
    os.system('CLS')
    text = appname
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    myfont = ImageFont.truetype("verdanab.ttf", 19)
    size = myfont.getsize(text)
    img = Image.new("1", size, "black")
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), text, "white", font=myfont)
    pixels = np.array(img, dtype=np.uint8)
    chars = np.array([' ', '#'], dtype="U1")[pixels]
    strings = chars.view('U' + str(chars.shape[1])).flatten()
    print("\n".join(strings))
    print("\n")
    print("\n")
    print("By Aditya Khemka")
    print("\n")
    print("\n")
    # https://stackoverflow.com/questions/9632995/how-to-easily-print-ascii-art-text
    time.sleep(3)
    print("* Contact me at androbyaditya@gmail.com")
    print("*  wwwkhemkaaditya.wixsite.com/andro")
    print("* The app is in its beta version")
    print("* I would like to hear about some bugs or possible improvments to the app")
    print("* Say help / support to get more info")
    print("* The app is protected by an MIT license")
    time.sleep(12)
    os.system('CLS')

###########################################################################################################

# open chrome and search for url (default: Internet Explorer)
def web(url):
    webbrowser.register('chrome',None,webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))

    webbrowser.get('chrome').open(url)

###########################################################################################################

# setting up alram using time function to ring at 6:30 am
def alram():
    a = 0
    x = datetime.datetime.now()
    print(x.strftime("%H") + x.strftime("%M"))
    hr = x.strftime("%H")
    if '06' in hr:
        mn = x.strftime("%M")
        print(mn)
        if '30' in mn and a == 0:
            print("Good Morining Sir")
            speak("Good morning sir")
            today = "Today is a " + x.strftime("%A") + ". Its " + x.strftime("%d") + " " + x.strftime(
                "%B") + " " + x.strftime("%Y") + "."
            print(today)
            speak(today)
            a = 1

###########################################################################################################

#to send e-mail
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(email, password)
    server.sendmail(email, to, content)
    server.close()

###########################################################################################################

#to play youtube video
def playonyt(topic):
    url = 'https://www.youtube.com/results?q=' + topic
    count = 0
    cont = requests.get(url)
    data = cont.content
    data = str(data)
    lst = data.split('"')
    for i in lst:
        count+=1
        if i == 'WEB_PAGE_TYPE_WATCH':
            break
    if lst[count-5] == "/results":
        raise Exception("No video found.")
    web("https://www.youtube.com"+lst[count-5])
    return "https://www.youtube.com"+lst[count-5]

###########################################################################################################

# to call above function
def YouTubePlay(keyword):
    try:
        playonyt(keyword)
        print("Playing...")
        speak("playing video ...")

    except:
        print("An unexpected error occured. Opening YouTube for query")
        speak("an unexpected error occured. Opening YouTube for query")
        link = "https://www.youtube.com/results?search_query=" + keyword + ""
        web(link)
        
###########################################################################################################

# function to send message via web.whatsapp.com
def preparemsg(phone_no, message, time_hour, time_min, wait_time=20, print_waitTime=True):
    import time 
    sleeptm = "time in seconds."

    # checking if the time received is in correct format
    if time_hour not in range(0, 25) or time_min not in range(0, 60):
        print("Invalid time format")

    if time_hour == 0:
        time_hour = 24
    callsec = (time_hour*3600)+(time_min*60)

    curr = time.localtime()
    currhr = curr.tm_hour
    currmin = curr.tm_min
    currsec = curr.tm_sec

    if currhr == 0:
        currhr = 24

    currtotsec = (currhr*3600)+(currmin*60) + \
        (currsec)
    lefttm = callsec-currtotsec

    if lefttm <= 0:  
        lefttm = 60+lefttm

    if lefttm < wait_time:  
        print("Call time must be greater than wait_time as web.whatsapp.com takes some time to load")

    sleeptm = lefttm-wait_time
    sleep = str(sleeptm)
    buff = str(wait_time)
    if print_waitTime:
        print("Your message will be delivered in "+sleep+" + "+buff +
              " seconds via whatsapp web . Please don't disturb the window")
    time.sleep(sleeptm)
    web('https://web.whatsapp.com/send?phone='+phone_no+'&text='+message)
    time.sleep(2)
    width, height = pg.size()
    pg.click(width/2, height/2)
    time.sleep(wait_time-2)
    pg.press('enter')

###########################################################################################################

# function to send whatsapp message by calling above function
def whatsapp_message(message, number):
    message = str(message)
    number = "+91" + str(number)
    print("sending message to: " + number)
    time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    hr = int(time.strftime("%H"))
    mn = int(time.strftime("%M"))
    try:
        speak("preparing to send message")
        preparemsg(number, message, hr, mn)
        print("Successfully Sent!")
        speak("Successfully Sent the message")
    except:
        print("An Unexpected error occured")
        speak("Sorry sir. The message could not be sent")


###########################################################################################################

def News(): 
		topic=news_topic #news related to general topics, can be changed 
		number=news_no # read 5 headlines, max 100
		main_url = "http://newsapi.org/v2/top-headlines?country=in&category="+topic+"&pageSize="+number+"&apiKey="+newsapi+"" 
		open_bbc_page = requests.get(main_url).json()  
		article = open_bbc_page["articles"] 
		results = [] 	
		for ar in article: 
			results.append(ar["title"]) 		
		for i in range(len(results)): 
			print(i + 1, results[i]) 
		from win32com.client import Dispatch 
		speak = Dispatch("SAPI.Spvoice") 
		speak.Speak(results)

###########################################################################################################

#sending message using fast2sms
'''
please note:
In accordance to the new regulations issued by TRAI (Telecom Regulation Authority of India), all bulk messages and net-messages services 
(like this one) will have to register themselves with any of the DLT operators.
The law will take effect from 20th September, 2020.
Must read: https://www.fast2sms.com/notice/
'''
def send_message(message,numbers):
    url = "https://www.fast2sms.com/dev/bulk"
    querystring = {"authorization":"djLX6ElaDJAwcM8x4fUtW9kNpRSzOsiHu7ynVo5FK3hZYm0GqTxFlTC6YnjSBoveMk8XEtq4LIipGJmf","sender_id":"FSTSMS","message":message,"language":"english","route":"p","numbers":numbers}
    headers = {
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)

###########################################################################################################

# gathers stock information of any company registered in NSE (India) or NASDAQ (USA)
def stockInfo():
    name = ""
    price = ""
    symbol = ""

    exchange = input("Enter I for NSE and A for NASDAQ: ")
    symbol = input("Enter brand symbol: ")

    if "I" in exchange or "i" in exchange:
        nse = Nse()
        quote = nse.get_quote(symbol)
        price = (quote['basePrice'])
        price = "INR " + str(price)
        name = quote['companyName']

    elif "A" in exchange or "a" in exchange:
        name = yf.Ticker(symbol)
        name = (name.info['longName'])
        price = stock_info.get_live_price(symbol)
        price = "USD " + str(price)

    else:
        print("Error")

    print("Name   : " + name)
    print("Symbol : " + symbol)
    print("Price  : " + price)
    update_histroy(("checked stock info for"+name))

###########################################################################################################

# translates using google trans (for some reason, does not support hindi)
def Translate_Text(text, lang_code):
    trans = Translator()
    t = trans.translate(text, dest=lang_code)
    print(f'{t.text}')

###########################################################################################################

#to update,show and clear history 

def update_histroy(text) :
  file = open("andro_his.txt","a")
  strTime = datetime.datetime.now().strftime("%H:%M:%S")
  text=strTime+": "+text
  file.write(text)
  file.write("\n--------------------\n")
  file.close()

def show_history ():
  file = open("andro_his.txt", "r")
  print(file.read())
  
def clear_history ():
  file = open("andro_his.txt", "w")
  print("********************")
  print("clearning history ...")
  print("********************")
  file.truncate(0)
  file.close()
  update_histroy("cleared history")

###########################################################################################################  

#main function that runs in an infinite loop
def andro():
    speak("initializing andro")
    splash_screen()
    wishMe()
    alram()
    os.system('CLS')

    while True:
        print("========================================================================================")
        query = takeCommand().lower()  # accepts input

        # Logic for executing tasks based on query

        if 'wikipedia' in query:  # search wikipedia
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
            update_histroy(("wikipedia search for" + query))

        elif 'who made you' in query:
            speak('I am a smart virtual assistant made by Aditya Khemka. Here is sirs portfolio website')
            web("aditya-khemka.github.io")


        #opening websites and apps

        elif 'open youtube' in query:
            web("youtube.com")
            update_histroy("opened youtube.com")

        elif 'open google' in query:
            web("google.com")
            update_histroy("opened google.com")

        elif 'open stack overflow' in query:
            web("stackoverflow.com")
            update_histroy("opened stackoverflow.com")

        elif 'open github' in query:
            web("github.com")
            update_histroy("opened github.com")

        elif 'open unacademy' in query:
            web("unacademy.com")
            update_histroy("opened unacademy.com")
            
        elif 'geeks' in query and 'for' in query:
            web("geeksforgeeks.org")
            update_histroy("opened geeksforgeeks.org")

        elif '.com' in query:
            query = query.replace("open ", "")
            query = query.strip()
            web(query)
            update_histroy(("opened" + query))

        elif '.in' in query:
            query = query.replace("open ", "")
            query = query.strip()
            web(query)
            update_histroy(("opened" + query))

        elif '.org' in query:
            query = query.replace("open ", "")
            query = query.strip()
            web(query)
            update_histroy(("opened" + query))

        elif 'open my website' in query:
            web("aditya-khemka.github.io")
            update_histroy(("opened aditya-khemka.github.io"))

        elif 'open text' in query:
            codePath = "C:\\Program Files\\Sublime Text\\subl.exe"
            os.startfile(codePath)
            update_histroy("opened sublime text" + query)


        #searching websites

        elif 'search youtube for' in query:
            speak('Opening YouTube...')
            query = query.replace("search youtube for", "")
            query = query.strip()
            link = "https://www.youtube.com/results?search_query=" + query + ""
            web(link)
            update_histroy(("searched YouTube for " + query))

        elif 'google for' in query:
            speak('Opening Google...')
            query = query.replace("search ", "")
            query = query.replace("google for", "")
            query = query.strip()
            link = "https://www.google.com/search?q=" + query + "&oq=" + query + "+&aqs=chrome.0.69i59j69i57.2093j0j1&sourceid=chrome&ie=UTF-8"
            web(link)
            update_histroy(("searched Google for " + query))

        elif "where is" in query or "locate" in query:
            query = query.replace("where is", "")
            query = query.replace("locate", "")
            speak("Searching for ...")
            speak(query)
            web("https://www.google.com/maps/search/" + query + "")
            update_histroy(("located"+query+"on maps"))

        elif 'image' in query or 'images' in query:
          keyword=keyword.replace("images","image")
          index = keyword.find('image')
          head=keyword[:index]
          keyword=keyword.replace(head,"")
          keyword=keyword.replace("image","")
          keyword=keyword.replace("of","")
          print("showing images of "+keyword+" in google")
          web("https://www.google.com/search?tbm=isch&sxsrf=ALeKk01IAim60Fo3Z5AQu8pK2VTCY5B8rg%3A1601865569267&source=hp&biw=1280&bih=648&ei=YYd6X8qnDsP59QPA55TIDA&q="+keyword+"&oq="+keyword+"&gs_lcp=CgNpbWcQAzIFCAAQsQMyBQgAELEDMgUIABCxAzIFCAAQsQMyBQgAELEDMgUIABCxAzIFCAAQsQMyBQgAELEDMgUIABCxAzIFCAAQsQM6CAgAELEDEIMBOgIIAFC_GFjBH2DmJmgAcAB4AIABwwGIAa8HkgEDMC41mAEAoAEBqgELZ3dzLXdpei1pbWc&sclient=img&ved=0ahUKEwiK3O2htpzsAhXDfH0KHcAzBckQ4dUDCAc&uact=5")
          update_histroy(("searched for images of "+keyword+"on google"))

        elif 'play' in query and 'youtube' in query:
            speak("Sir, please say the keywords to search for")
            keyword = takeCommand()
            YouTubePlay(keyword)
            update_histroy(("played YouTube video on "+keyword))


        #cracks jokes
        elif 'joke' in query:
            speak(pyjokes.get_joke())
            update_histroy("cracked a joke")

        #playing music
        elif 'play music' in query:
            speak("Playing music")
            music_dir = "F:\\aditya\\Python development"
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[4]))
            update_histroy("played music")


        #checking time and day
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
            update_histroy("asked for the time")

        elif 'timer' in query or 'countdown' in query:
            #https://www.geeksforgeeks.org/how-to-create-a-countdown-timer-using-python/
            speak("sir, please enter the time in seconds") 
            t = input("Enter the time in seconds: ") 
            update_histroy("set a timer for"+t+"seconds")
            while t: 
                mins, secs = divmod(t, 60) 
                timer = '{:02d}:{:02d}'.format(mins, secs) 
                print(timer, end="\r") 
                time.sleep(1) 
                t -= 1
            print("time over")
            winsound.Beep(1000, 2000) 
            time.sleep(0.25) 
            speak("time over")

        elif 'the day' in query:
            x = datetime.datetime.now()
            day=x.strftime("%A")
            speak("sir, today is a"+day)
            update_histroy("checked today's day")

        elif 'the date' in query:
            x = datetime.datetime.now()
            today = "Sir, today is "+ x.strftime("%d") + " " + x.strftime("%B") + " " + x.strftime("%Y") + "."
            speak(today)
            print(today)
            update_histroy("checked today's date")


        #mute functions
        elif "don't listen" in query or "stop listening" in query:
            speak("Sir, for how much time shall I remain silence?")
            a = int(takeCommand())
            print(a)
            speak("silent for"+((str)(a))+"seconds")
            update_histroy("played music")
            time.sleep(a)


        # actual usage of virtual assistant
        elif "algebra" in query or "calculator" in query:  
            app_id = alpha 
            client = wolframalpha.Client(app_id) 
            question=input("Question please: ")  
            res = client.query(question) 
            answer = next(res.results).text 
            print("answer: "+answer)   
            speak("The answer is " )
            speak(answer) 
            update_histroy("calculated "+question)


        elif "what is" in query or "who is" in query or "why is" in query or "when is" in query:  
            client = wolframalpha.Client(alpha)
            #connecting to wolfram alpha
            try:
                res = client.query(query) 
            except Exception as e:
                speak("Sorry Sir, the server encountered a problem")
                continue 
            #gathering information 
            try: 
                print (next(res.results).text) 
                speak (next(res.results).text) 
            except Exception as e:
                print ("No results")  
                speak ("Sorry sir, I could not fetch any results. Opening google for the query")   
                query = query.replace("what", "")
                query = query.replace("who", "")
                query = query.replace("when", "")
                query = query.replace("why", "")
                query = query.replace("is", "")
                query = query.replace("are", "")
                query=query.strip()
                link="https://www.google.com/search?q="+query+"&oq="+query+"+&aqs=chrome.0.69i59j69i57.2093j0j1&sourceid=chrome&ie=UTF-8"
                web(link)  
            #phir bhi koi galti hua toh    
            except Exception as e:
                speak("Sorry Sir, the server encountered a problem")
                continue
            update_histroy("learnt about '"+query+"'")

        #about the weather
        elif "weather" in query or "temperature" in query:  
            api_key = weather
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            speak("Sir, please tell the city name")
            city_name = takeCommand() 
            print("City name : ")
            print(city_name)  
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
            response = requests.get(complete_url) 
            x = response.json()   
            if x["cod"] != "404":  
                y = x["main"]  
                current_temperature = y["temp"]  
                current_pressure = y["pressure"]  
                current_humidiy = y["humidity"]  
                z = x["weather"]  
                weather_description = z[0]["description"]  
                print(" Temperature (in kelvin unit) = " +str(current_temperature)+"\n atmospheric pressure (in hPa unit) ="+str(current_pressure) +"\n humidity (in percentage) = " +str(current_humidiy) +"\n description = " +str(weather_description))  
                speak(" Temperature (in kelvin unit) = " +str(current_temperature)+"\n atmospheric pressure (in hPa unit) ="+str(current_pressure) +"\n humidity (in percentage) = " +str(current_humidiy) +"\n description " +str(weather_description))    
            else:  
                speak(" City Not Found ")  
            update_histroy("checked weather in "+city_name)


        #taking notes

        elif "write a note" in query or "take a note" in query:
            speak("Sir, what must I write")
            note = takeCommand()
            file = open('andro.txt', 'w')
            speak("Sir, Should i include date and time")
            snfm = takeCommand()
            if 'yes' in snfm or 'sure' in snfm or 'yup' in snfm:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)

            speak("Note added")
            update_histroy("added a note")

        elif "show" in query and "note" in query or "so note" in query:
            speak("Showing Notes")
            file = open("andro.txt", "r")
            print(file.read())
            speak(file.read(6))
            time.sleep(2)
            update_histroy("read notes")


        #IFTTT usage

        elif 'alert' in query and 'message' in query:
            speak("Sir, a message has been sent to you from IFTTT")
            requests.get("https://maker.ifttt.com/trigger/msg/with/key/"+ifttt)
            update_histroy("sent alert message")

        elif  'ring' in query or 'call' in query:
            speak("Ringing device")
            requests.get("https://maker.ifttt.com/trigger/call/with/key/"+ifttt)
            update_histroy("rang device")

        elif 'notification' in query or 'notify' in query:
            speak("Sir, a notification has been sent to you from IFTTT")
            requests.get("https://maker.ifttt.com/trigger/notify/with/key/"+ifttt)  
            update_histroy("sent notification")


        #stock price

        elif 'stock' in query or 'share' in query:
            speak("Sir, please enter stock exchange and brand symbol")
            stockInfo()

        #translating functions
        elif 'translate' in query and 'english' in query:
            text = input("Enter text to translate: ")
            print (Translate_Text(text, "en"))
            update_histroy(("translated "+text+"to english"))

        elif 'translate' in query:
            text = input("Enter text to translate: ")
            lang_code = input("Enter Language Code: ")
            Translate_Text(text, lang_code)
            update_histroy(("translated "+text+"to "+lang_code))


        #sending messages

        elif 'whatsapp' in query:
            speak("sir, please type the receiver's phone number")
            no = input("Receiver's 10 digit number number: ")
            speak("sir, please type the message to be sent")
            msg = input("message: ")
            whatsapp_message(msg, no)
            update_histroy(("sent whatsapp message to "+no))
        
        elif 'email to aditya' in query:
            try:
                speak("Sir, please type the content")
                content = input("Content of the email please: ")
                to = "www.khemkaaditya@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry Sir. I could not send this email") 
            update_histroy("sent email to aditya")

        elif 'send an email' in query or 'send a mail' in query: 
            try: 
                speak("Sir, please type the content") 
                content = input("Content of the email please: ")
                speak("Sir, please type the receiver's address ") 
                print("Sir, please type the receiver's address: ") 
                to = input()     
                sendEmail(to, content) 
                speak("Email has been sent !") 
            except Exception as e: 
                print(e) 
                speak("Sorry Sir. I could not send this email") 
            update_histroy("sent email to "+to)


        elif 'message' in query and 'text' in query:
            speak("Sir, please enter the message to send")
            message = input ("Enter message: ")
            speak("Sir, please enter phone numbers to send sms to")
            numbers = input ("Enter numbers seperated by commas: ")
            send_message(message,numbers)
            speak("Message sent")
            update_histroy("sent messages to "+numbers)

        #reading headlines
        elif 'headlines' in query:
            News()
            update_histroy("read headlines")

        #history ...
        elif 'so history' in query or 'show history' in query :
            show_history()

        elif 'delete history' in query and 'clear history' in query :
            clear_history()

        #selfie
        elif 'take image' in query or 'capture' in query or 'photo' in query:
            print("preparing to capture image")
            speak("sir, please smile for an image")
            ec.capture(0,"andro","img.jpg")
            update_histroy("took a selfie")

        #PC related functions

        elif ('sleep' in query or 'hibernate' in query) and ('pc' in query or 'computer' in query or 'system' in query) :
            print("your PC will go to hibernate in 15 secomds ...")
            speak("your PC will go to hibernate in 15 secomds")
            update_histroy("intialized computer hybernation")
            os.system("shutdown /h /t 15")

        elif ('shutdown' in query) and ('pc' in query or 'computer' in query or 'system' in query) :
            print("your PC will shutdown in 30 seconds. To cancel shutdown, call 'cancelShutdown'")
            speak("sir, your PC will shutdown in 30 seconds")
            update_histroy("initialised computer shutdown")
            os.system("shutdown /s /t 30")

        elif ('restart' in query) and ('pc' in query or 'computer' in query or 'system' in query) :
            print("your PC will restart in 30 seconds.  To cancel restart, call 'cancelShutdown'")
            speak("sir, your PC will restart in 30 seconds")
            update_histroy("initialised computer restart")
            os.system("shutdown /r /t 30")


        elif 'cancel' in query and  ('restart' in query or 'shutdown' in query) :
            cont = "shutdown/a"
            print("shutdown cancelled...")
            speak("shutdown cancelled")
            update_histroy("cancelled computer shutdown")
            os.system(cont)

        #location
        elif 'my location' in query or  'where am I' in query :
            send_url = "http://api.ipstack.com/check?access_key="+iplocation
            geo_req = requests.get(send_url)
            geo_json = json.loads(geo_req.text)
            city = geo_json['city']
            print("your IP location: "+city)
            speak("sir, your IP location is: "+city)
            update_histroy("checked your location")

        #communications ...

        elif 'help' in query or 'support' in query:
            print("****** Andro by Aditya Khemka ******")
            print("mail me at androbyaditya@gmail.com")
            print("visit https://wwwkhemkaaditya.wixsite.com/andro")
            time.sleep(5)
            speak("opening forum")
            web("wwwkhemkaaditya.wixsite.com/andro")

        elif 'hello' in query:
            speak("Hi! I am andro. how may i help you ?")

        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you, Sir")

        elif 'I am fine' in query or "good" in query:
            speak("It's good to know that your fine")

        elif "will you be my gf" in query or "will you be my bf" in query:    
            speak("I'm not sure about, may be you should give me some time") 
  
        elif "how are you" in query: 
            speak("I'm fine, glad you me that") 
  
        elif "i love you" in query: 
            speak("It's hard to understand") 


        elif 'exit' in query:
            speak("Thanks for giving me your time")
            update_histroy("closed andro")
            exit()       

        elif 'none' not in query:
            speak("Sorry Sir, I could not fetch any results for the query")
            print("Error")


#calls the boss function :)
andro()

#######################################
