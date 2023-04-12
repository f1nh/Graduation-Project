import random, json, datetime, webbrowser, os, time, subprocess, pickle, nltk, pyfirmata, telebot, threading, pandas as pd
import wikipedia
import pyttsx3
import speech_recognition as sr
import numpy as np
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from dateutil.relativedelta import relativedelta

class jarvis:
    lemmatizer = WordNetLemmatizer()
    intents = json.loads(open('intents.json').read())
    words = pickle.load(open('words.pkl', 'rb'))
    classes = pickle.load(open('classes.pkl', 'rb'))
    model = load_model('jarvis_model.h5')
        
    def speak(text):
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[4].id)
        engine.setProperty('rate', 155)
        engine.setProperty('volume', 0.5)
        engine.say(text=text)
        engine.runAndWait()
    
    def takecommand():
        r = sr.Recognizer()
        r.pause_threshold = 0.5
        
        with sr.Microphone() as source:
            query = ''
            print('Listening...')
            audio = r.listen(source)
            
            try:
                print('Recognizing...')
                query = str(r.recognize_google(audio, language='en-in'))
                print(query)
            except Exception as e:
                print(e)
        return query.lower()

    def wishMe():
        
        hour=datetime.datetime.now().hour
        if hour>=0 and hour<12:
            jarvis.speak("hello, good morning")
            print("hello, good morning")
        elif hour>=12 and hour<18:
            jarvis.speak("hello, good afternoon")
            print("hello, good afternoon")
        else:
            jarvis.speak("hello, good evening")
            print("hello, good evening")
        
    def clean_up_sentence(sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [jarvis.lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words
    
    def bag_of_words(sentence):
        sentence_words = jarvis.clean_up_sentence(sentence)
        bag = [0] * len(jarvis.words)
        for w in sentence_words:
            for i, word in enumerate(jarvis.words):
                if word == w:
                    bag[i] = 1
                    
        return np.array(bag)

    def predict_class(sentence):
        bow = jarvis.bag_of_words(sentence)
        res = jarvis.model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
        
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({'intents': jarvis.classes[r[0]], 'probability': str(r[1])})
        return return_list

    def get_response(intents_list, intents_json):
        tag = intents_list[0]['intents']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result

class skills:
    def wikipedia(query):
        statment = query.replace('tell me about', '')
        res = wikipedia.summary([statment], sentences=3)
        jarvis.speak(res)
        print(res)
    
    def work(res):
        jarvis.speak(res)
        with open('input.txt', 'w') as f:
            f.write(input('>'))
        with open('input.txt', 'r') as f:
            file_name = f.read()
        jarvis.speak('is the project for the college, friend, main project, quick project, or just for testing sir?')
        with open('input.txt', 'w') as f:
            f.write(input('>'))
        with open('input.txt', 'r') as f:
            project = f.read()
        if 'college' in project:
            os.mkdir(f'c:\\Users\\f2w\\Desktop\\Projects\\College Projects\\{file_name}')
            os.system(f'code "c:\\Users\\f2w\\Desktop\\Projects\\College Projects\\{file_name}\\{file_name}.py"')
        elif 'friend' in project:
            os.mkdir(f'c:\\Users\\f2w\\Desktop\\Projects\\Friends Projects\\{file_name}')
            os.system(f'code "c:\\Users\\f2w\\Desktop\\Projects\\Friends Projects\\{file_name}\\{file_name}.py"')
        elif 'main' in project:
            os.mkdir(f'c:\\Users\\f2w\\Desktop\\Projects\\Main Projects\\{file_name}')
            os.system(f'code "c:\\Users\\f2w\\Desktop\\Projects\\Main Projects\\{file_name}\\{file_name}.py"')
        elif 'quick' in project:
            os.mkdir(f'c:\\Users\\f2w\\Desktop\\Projects\\Quick Projects\\{file_name}')
            os.system(f'code "c:\\Users\\f2w\\Desktop\\Projects\\Quick Projects\\{file_name}\\{file_name}.py"')
        elif 'testing' in project:
            os.mkdir(f'c:\\Users\\f2w\\Desktop\\Projects\\Testing Projects\\{file_name}')
            os.system(f'code "c:\\Users\\f2w\\Desktop\\Projects\\Testing Projects\\{file_name}\\{file_name}.py"')
    
    def browser(query):
        if 'youtube' in query:
            webbrowser.open_new_tab('https://www.youtube.com')
            jarvis.speak('youtube is open')
            
        elif 'google' in query:
            webbrowser.open_new_tab('https://www.google.com')
            jarvis.speak('Google chrome is open')
            
        elif 'gmail' in query:
            webbrowser.open_new_tab('gmail.com')
            jarvis.speak('Google Mail open')
    
    def time():
        strTime=datetime.datetime.now().strftime('%H:%M:%S')
        jarvis.speak(f'the time is {strTime}')
    
    def news():
        webbrowser.open_new_tab('https://www.nytimes.com/section/world')
        jarvis.speak('Here are some News from the the new york times, Happy reading')
    
    def search(query):
        query = query.replace("search for", "")
        webbrowser.open_new_tab(query)
    
    def bye(res):
        jarvis.speak(res)
        subprocess.call(["shutdown", "/l"])
            
    def light(query):
        from telegram import Arduino
        if 'on the yellow' in query:
            YELLOW = board.digital[4]
            HIGH = 1
            YELLOW.write(HIGH)
            
        elif 'off the yellow' in query:
            YELLOW = board.digital[4]
            LOW = 0
            YELLOW.write(LOW)
            
        elif 'on the green' in query:
            GREEN = board.digital[3]
            HIGH = 1
            GREEN.write(HIGH)
            
        elif 'off the green' in query:
            GREEN = board.digital[3]
            LOW = 0
            GREEN.write(LOW)
            
    def age():
        rdelta = relativedelta(datetime.datetime.now().date(), pd.to_datetime('2021-03-23').date())
        jarvis.speak(f"i'm {str(rdelta.years)} year {str(rdelta.months)} months and {str(rdelta.days)} days old")
            
if __name__ == '__main__':
    
    print('Turning on the systems...')
    jarvis.wishMe()
    jarvis.speak('Arduino is Connected...')
    
    while True:
        query = jarvis.takecommand().lower()
        if query != "":
            ints = jarvis.predict_class(query)
            print(ints[0]['intents'])
            res = jarvis.get_response(ints, jarvis.intents)
            if 'wikipedia' in ints[0]['intents']:
                skills.wikipedia(query)
                
            elif 'work' in ints[0]['intents']:
                skills.work(res)
                
            elif 'browser' in ints[0]['intents']:
                skills.browser(query)
            
            elif 'arduino' in ints[0]['intents']:
                skills.light(query)
                
            elif 'time' in ints[0]['intents']:
                skills.time()
            
            elif 'age' in ints[0]['intents']:
                skills.age()
                
            elif 'news' in ints[0]['intents']:
                skills.news()
                
            elif 'search' in ints[0]['intents']:
                skills.search(query)
                
            elif "bye" in ints[0]['intents']:
                skills.bye(res)
                
            else:
                jarvis.speak(res)