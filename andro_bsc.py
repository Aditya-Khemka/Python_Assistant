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
import pyautogui as pg
import speech_recognition as sr
import yfinance as yf
from pyttsx3.drivers import sapi5
from nsetools import Nse
from yahoo_fin import stock_info
from googletrans import Translator
from ecapture import ecapture as ec

pg.FAILSAFE = False
os.system('CLS')
# Setting up speaker defaults
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    engine.setProperty('rate', 145)


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
# to play youtube video
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


# open chrome and search for url (default: Internet Explorer)
def web(url):
    webbrowser.register('chrome',None,webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))

    webbrowser.get('chrome').open(url)


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

# setting up a simple splash screen
def splash_screen():
    os.system('CLS')
    text = "A N D R O"
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
# function to send whatsapp messages
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


# translates using google trans (for some reason, does not support hindi)
def Translate_Text(text, lang_code):
    trans = Translator()
    t = trans.translate(text, dest=lang_code)
    print(f'{t.text}')


###########################################################################################################
#to update and clear history 

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
  #time.sleep(10)
  
def clear_history ():
  file = open("andro_his.txt", "w")
  print("********************")
  print("clearning history ...")
  print("********************")
  file.truncate(0)
  file.close()
  update_histroy("cleared history")

###########################################################################################################  

# main function in infinite loop
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

        elif 'image' in query or 'images' in query:
          keyword=keyword.replace("images","image")
          index = keyword.find('image')
          head=keyword[:index]
          keyword=keyword.replace(head,"")
          keyword=keyword.replace("image","")
          keyword=keyword.replace("of","")
          print("showing images of "+keyword+" in google")
          web("https://www.google.com/search?tbm=isch&sxsrf=ALeKk01IAim60Fo3Z5AQu8pK2VTCY5B8rg%3A1601865569267&source=hp&biw=1280&bih=648&ei=YYd6X8qnDsP59QPA55TIDA&q="+keyword+"&oq="+keyword+"&gs_lcp=CgNpbWcQAzIFCAAQsQMyBQgAELEDMgUIABCxAzIFCAAQsQMyBQgAELEDMgUIABCxAzIFCAAQsQMyBQgAELEDMgUIABCxAzIFCAAQsQM6CAgAELEDEIMBOgIIAFC_GFjBH2DmJmgAcAB4AIABwwGIAa8HkgEDMC41mAEAoAEBqgELZ3dzLXdpei1pbWc&sclient=img&ved=0ahUKEwiK3O2htpzsAhXDfH0KHcAzBckQ4dUDCAc&uact=5")


        elif 'play music' in query:
            speak("Playing music")
            music_dir = "F:\\aditya\\Python development"
            songs = os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir, songs[4]))
            update_histroy("played music")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
            update_histroy("asked for the time")


        elif 'open text' in query:
            codePath = "C:\\Program Files\\Sublime Text\\subl.exe"
            os.startfile(codePath)
            update_histroy("opened sublime text" + query)
            

        elif 'joke' in query:
            speak(pyjokes.get_joke())
            update_histroy("cracked a joke")


        elif "don't listen" in query or "stop listening" in query:
            speak("Sir, for how much time shall I remain silence?")
            a = int(takeCommand())
            print(a)
            speak("silent for"+((str)(a))+"seconds")
            update_histroy("played music")
            time.sleep(a)


        elif "where is" in query or "locate" in query:
            query = query.replace("where is", "")
            query = query.replace("locate", "")
            speak("Searching for ...")
            speak(query)
            web("https://www.google.com/maps/search/" + query + "")
            update_histroy(("located"+query+"on maps"))


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


        elif 'who made you' in query:
            speak('I am a smart virtual assistant made by Aditya Khemka. Here is sirs portfolio website')
            web("aditya-khemka.github.io")

        elif 'stock' in query or 'share' in query:
            speak("Sir, please enter stock exchange and brand symbol")
            stockInfo()

        elif 'translate' in query and 'english' in query:
            text = input("Enter text to translate: ")
            print (Translate_Text(text, "en"))
            update_histroy(("translated "+text+"to english"))

        elif 'translate' in query:
            text = input("Enter text to translate: ")
            lang_code = input("Enter Language Code: ")
            Translate_Text(text, lang_code)
            update_histroy(("translated "+text+"to "+lang_code))

        elif 'play' in query and 'youtube' in query:
            speak("Sir, please say the keywords to search for")
            keyword = takeCommand()
            YouTubePlay(keyword)
            update_histroy(("played YouTube video on "+keyword))


        elif 'whatsapp' in query:
            speak("sir, please type the receiver's phone number")
            no = input("Receiver's 10 digit number number: ")
            speak("sir, please type the message to be sent")
            msg = input("message: ")
            whatsapp_message(msg, no)
            update_histroy(("sent whatsapp message to "+no))


        elif 'help' in query or 'support' in query:
            print("****** Andro by Aditya Khemka ******")
            print("mail me at androbyaditya@gmail.com")
            print("visit https://wwwkhemkaaditya.wixsite.com/andro")
            time.sleep(5)
            speak("opening forum")
            web("wwwkhemkaaditya.wixsite.com/andro")

        elif 'so history' in query or 'show history' in query :
            show_history()

        elif 'delete history' in query and 'clear history' in query :
            clear_history()

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

        elif 'take image' in query or 'capture' in query or 'photo' in query:
            print("preparing to capture image")
            speak("sir, please smile for an image")
            ec.capture(0,"andro","img.jpg")
            update_histroy("took a selfie")

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


#bole toh boss function
andro()

###################################################################################################################################
##            '''                                                                                                                ##
##           Made by Aditya Khemka (D.B.M.S. English School, Jamshedpur)                                                         ##
##                                                                                                                               ##
##           Slow response is due to poor connection                                                                             ##
##                                                                                                                               ##
##            Made with the help of:                                                                                             ##
##                GeekForGeeks   (Coding/Learning platform)                                                                      ##
##                Stack Overflow (Paradise for software developers)                                                              ##
##                                                                                                                               ##
##            '''                                                                                                                ##
###################################################################################################################################
