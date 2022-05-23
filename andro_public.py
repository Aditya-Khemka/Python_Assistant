#importing needed libraries
import subprocess 
import smtplib
import wolframalpha 
import pyttsx3 
import tkinter 
import json 
import random 
import operator 
import speech_recognition as sr 
import datetime 
import wikipedia 
import webbrowser 
import os 
import winshell 
import pyjokes 
import feedparser 
import ctypes 
import time 
import requests 
import json
import shutil 
from bs4 import BeautifulSoup 
import win32com.client as wincl 
from urllib.request import urlopen 
from nsetools import Nse 
from yahoo_fin import stock_info
import yfinance as yf
from googletrans import Translator

###########################################################################################################

#Setting up speaker defaults
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    engine.setProperty('rate',145)


#Greeting message
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("Hi. I am Andro, Aditya's personal assistant. How may I serve you?")       


#To take microphone input from the user and return string output
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

    except Exception as e:
        print("Please say that again.....")  
        return "None"

    return query


###########################################################################################################


#to send e-mail
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('Your_Email_ID', 'Email IDs password') #enable low security if using gmail
    server.sendmail('Your_Email_ID', to, content)
    server.close()

###########################################################################################################

#to extract headlines
def News(): 
		topic="general" #news related to general topics, can be changed 
		number="5" # read 5 headlines, max 100
		main_url = "http://newsapi.org/v2/top-headlines?country=in&category="+topic+"&pageSize="+number+"&apiKey=Your_Api_Key" #get one from newsapi.org 
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

#open chrome and search for url (default: Internet Explorer)
def web(url):
    webbrowser.register('chrome',
	    None,
	    webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))

    webbrowser.get('chrome').open(url)       

###########################################################################################################

#gathers stock information of any company registered in NSE (India) or NASDAQ (USA)
def stockInfo() :
  name=""
  price=""
  symbol=""

  exchange=input("Enter I for NSE and A for NASDAQ: ")
  symbol=input("Enter brand symbol: ")


  if "I" in exchange or "i" in exchange:
    nse = Nse() 
    quote = nse.get_quote(symbol) 
    price = (quote['basePrice'] )
    price = "INR " + str (price)
    name  = quote['companyName'] 
  
  elif "A" in exchange or "a" in exchange :
    name = yf.Ticker(symbol)
    name = (name.info['longName'])
    price= stock_info.get_live_price(symbol)
    price = "USD " + str (price)

  else :
    print("Error")  
 

  print ("Name   : " + name)
  print ("Symbol : " + symbol) 
  print ("Price  : " + price)
  print("-------------------------------------------------------------------------") 

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
    #get API key from https://www.fast2sms.com/dashboard/dev-api
    querystring = {"authorization":"Your_API_Key","sender_id":"FSTSMS","message":message,"language":"english","route":"p","numbers":numbers}
    headers = {
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)

###########################################################################################################

def Translate_Text(text,lang_code):
  trans = Translator()
  t = trans.translate(text, dest=lang_code)
  print(f'{t.text}')
  speak(f'{t.text}')


#main function in infinite loop
if __name__ == "__main__":
    wishMe()

    while True:
        query = takeCommand().lower() #accepts input

        # Logic for executing tasks based on query

        if 'wikipedia' in query: #search wikipedia
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            web("youtube.com")
  

        elif 'open google' in query:
            web("google.com")

        elif 'open stack overflow' in query:
            web("stackoverflow.com") 

        elif 'open github' in query:
            web("github.com")      

        elif 'open unacademy' in query:
            web("unacademy.com") 

        elif 'hello' in query:
            speak("Hi! I am andro. how may i help you ?")     

        elif '.com' in query:
            query = query.replace("open ", "")
            query=query.strip()
            web(query)

        elif '.in' in query:
            query = query.replace("open ", "")
            query=query.strip()
            web(query)    

        elif 'open my website' in query:
            web("aditya-khemka.github.io")     

        elif 'search youtube for' in query:
            speak('Opening YouTube...')
            query = query.replace("search youtube for", "")
            query=query.strip()
            link="https://www.youtube.com/results?search_query="+query+""
            web(link)

        elif 'google for' in query:
            speak('Opening Google...')
            query = query.replace("search ", "")
            query = query.replace("google for", "")
            query=query.strip()
            link="https://www.google.com/search?q="+query+"&oq="+query+"+&aqs=chrome.0.69i59j69i57.2093j0j1&sourceid=chrome&ie=UTF-8"
            web(link)    

        elif 'play music' in query:
            speak("Playing music")
            music_dir = "folder path"
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[Index_number_in_folder])) #ex. if your .mp3 file is present in the 5th position in folder, then replace with 4 (location-1)

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'headlines' in query:
            News()

        elif 'open text' in query:
            codePath = "C:\\Program Files\\Sublime Text\\subl.exe"
            os.startfile(codePath)


        elif 'email to aditya' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "www.khemkaaditya@gmail.com"    
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry Sir. I could not send this email") 


        elif 'send an email' in query or 'send a mail' in query: 
            try: 
                speak("What should I say?") 
                content = takeCommand() 
                speak("Sir, please type the receiver's address") 
                to = input()     
                sendEmail(to, content) 
                speak("Email has been sent !") 
            except Exception as e: 
                print(e) 
                speak("Sorry Sir. I could not send this email") 

        elif 'how are you' in query: 
            speak("I am fine, Thank you") 
            speak("How are you, Sir") 
  
        elif 'I am fine' in query or "good" in query: 
            speak("It's good to know that your fine") 


        elif 'exit' in query: 
            speak("Thanks for giving me your time") 
            exit() 


        elif 'joke' in query: 
            speak(pyjokes.get_joke()) 


        elif "algebra" in query or "calculator" in query:  
              
            app_id = "Your_Api_Key" #get one from https://www.wolframalpha.com/ 
            client = wolframalpha.Client(app_id) 
            question=input("Question please: ")  
            res = client.query(question) 
            answer = next(res.results).text 
            print("answer: "+answer)   
            speak("The answer is " )
            speak(answer)   
    

        elif "don't listen" in query or "stop listening" in query: 
            speak("Sir, for how much time shall I remain silence?") 
            a = int(takeCommand()) 
            print(a)
            time.sleep(a)  


        elif "where is" in query or "locate" in query: 
            query = query.replace("where is", "")
            query = query.replace("locate", "") 
            speak("Searching for ...") 
            speak(query) 
            web("https://www.google.com/maps/search/"+ query + "") 


        elif "write a note" in query: 
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
          
        elif "show" in query and "note" in query or "so note" in query: 
            speak("Showing Notes") 
            file = open("andro.txt", "r")  
            print(file.read()) 
            speak(file.read(6))
            time.sleep(2)


        elif "weather" in query or "temperature" in query:  
            api_key = "Your_Api_Key" #get one from https://openweathermap.org/
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


        elif "what is" in query or "who is" in query : 
              
            client = wolframalpha.Client("Wolfrem alpha API key, same as above")

            try:
                res = client.query(query) 
            except Exception as e:
                speak("Sorry Sir, the server encountered a problem")
                continue  
              
            try: 
                print (next(res.results).text) 
                speak (next(res.results).text) 
            except Exception as e:
                print ("No results")  
                speak ("Sorry sir, I could not fetch any results. Opening google for the query")   
                query = query.replace("what", "")
                query = query.replace("who", "")
                query = query.replace("is", "")
                query=query.strip()
                link="https://www.google.com/search?q="+query+"&oq="+query+"+&aqs=chrome.0.69i59j69i57.2093j0j1&sourceid=chrome&ie=UTF-8"
                web(link) 
                  
            except Exception as e:
                speak("Sorry Sir, the server encountered a problem")
                continue   
                

        elif 'who made you' in query:
            speak('I am a smart virtual assistant made by Aditya Khemka. Here is sirs portfolio website')  
            web("aditya-khemka.github.io")   

        elif 'open' in query or 'project' in query:
            speak('opening mathematics project')  
            webbrowser.open_new(r"File_Path")
        
        elif 'stock' in query or 'share' in query:
            speak("Sir, please enter stock exchange and brand symbol")
            stockInfo()


        elif 'alert' in query and 'message' in query:
            speak("Sir, a message has been sent to you from IFTTT")
            requests.get("https://maker.ifttt.com/trigger/trigger_keyword/with/key/IFTTT_Api_Key")

        elif  'ring' in query or 'call' in query:
            speak("Ringing device")
            requests.get("https://maker.ifttt.com/trigger/trigger_keyword/with/key/IFTTT_Api_Key")

        elif 'notification' in query or 'notify' in query:
            speak("Sir, a notification has been sent to you from IFTTT")
            requests.get("https://maker.ifttt.com/trigger/trigger_keyword/with/key/IFTTT_Api_Key")  

        elif 'message' in query or 'text' in query:
            speak("Sir, please enter the message to send")
            message = input ("Enter message: ")
            speak("Sir, please enter phone numbers to send sms to")
            numbers = input ("Enter numbers seperated by commas: ")
            send_message(message,numbers)
            speak("Message sent")

        elif 'translate' in query and 'english' in query :
            text=input("Enter text to translate: ")
            Translate_Text(text,"en")  

        elif 'translate' in query :
            text=input("Enter text to translate: ")
            lang_code=input("Enter Language Code: ")
            Translate_Text(text,lang_code)   



###################################################################################################################################
##            '''                                                                                                                ##
##           Made by Aditya Khemka (D.B.M.S. English School, Jamshedpur)                                                         ##
##                                                                                                                               ##
##           Slow response is due to poor connection                                                                             ##
##                                                                                                                               ##
##            Made with the help of:                                                                                             ##
##                CodeWithHarry  (YouTube channel)                                                                               ##
##                GeekForGeeks   (Coding/Learning platform)                                                                      ##
##                Stack Overflow (Paradise for software developers)                                                              ##
##                                                                                                                               ##
##            '''                                                                                                                ##
###################################################################################################################################         



'''
  Andro uses various external APIs, get your API keys from the following websites:
  News        from  newsapi.org                       # can also change number of messages to send and news topic 
  Message     from  fast2sms.com        
  Calculator  from  wolframalpha.com    
  Weather     from  openweathermap.org  
  Query       from  wolframalpha.com    
  IFTTT       from  ifttt.com                          # will also have to configure applets in IFTTT.com


  Change email ID and its password
  Change file path 
  Change file path 
  Change trigger words (The "Event Name" in webhooks)

'''
