'''
Required to change email Id and password in line no 69 and 70
Required to get an API key in line no 78
'''


#importing needed libraries
import pyttsx3  # also needed pyAudio
import speech_recognition as sr 
import datetime 
import wikipedia 
import webbrowser
import os
import smtplib
import requests
import re

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


#to send e-mail
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('YourEmail', 'EmailPassword')
    server.sendmail('YourEmail', to, content)
    server.close()


#to extract headlines provided by BBc news
def News(): 
		topic="general" #news related to general topics
		number="5" # max 5 headlines
		main_url = "http://newsapi.org/v2/top-headlines?country=in&category="+topic+"&pageSize="+number+"&apiKey=YourKey" #get one at newsapi.org
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


#open chrome and search for url
def web(url):
    webbrowser.register('chrome',
	    None,
	    webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome//Application//chrome.exe"))

    webbrowser.get('chrome').open(url)        



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
            music_dir = 'E:\\My Music\\jagjit singh'
            songs = os.listdir(music_dir)
            print(songs)    
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")

        elif 'read five headlines' in query:
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
                

        elif 'who made you' in query:
            speak('I am a smart virtual assistant made by Aditya Khemka. Here is sirs portfolio website')  
            web("aditya-khemka.github.io")            
