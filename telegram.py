import telebot, pyfirmata, time, os, sys, webbrowser
from main import jarvis
from config import *

bot = telebot.TeleBot(Token, parse_mode=None)
board = pyfirmata.Arduino('COM5')        

if __name__ == '__main__':
    @bot.message_handler(commands=['yellow_on'])
    def yellow_on_telegram(message):
        YELLOW = board.digital[4]
        HIGH = 1
        YELLOW.write(HIGH)
        os.system('telegram-send "Yellow LED is on"')
        
    @bot.message_handler(commands=['yellow_off'])
    def yellow_off_telegram(message):
        YELLOW = board.digital[4]
        LOW = 0
        YELLOW.write(LOW)
        os.system('telegram-send "Yellow LED is off"')
        
    @bot.message_handler(commands=['green_on'])
    def green_on_telegram(message):
        GREEN = board.digital[3]
        HIGH = 1
        GREEN.write(HIGH)
        os.system('telegram-send "Green LED is on"')
        
    @bot.message_handler(commands=['green_off'])
    def green_off_telegram(message):
        GREEN = board.digital[3]
        LOW = 0
        GREEN.write(LOW)
        os.system('telegram-send "Green LED is off"')

    @bot.message_handler(commands=['lights'])
    def green_off_telegram(message):
        GREEN = board.digital[3]
        YELLOW = board.digital[4]
        HIGH = 1
        LOW = 0
        GREEN.write(HIGH)
        time.sleep(0.1)
        YELLOW.write(HIGH)
        time.sleep(0.1)
        GREEN.write(LOW)
        time.sleep(0.1)
        YELLOW.write(LOW)
        time.sleep(0.1)
        GREEN.write(HIGH)
        time.sleep(0.1)
        YELLOW.write(HIGH)
        time.sleep(0.1)
        GREEN.write(LOW)
        time.sleep(0.1)
        YELLOW.write(LOW)
        GREEN.write(HIGH)
        time.sleep(0.1)
        YELLOW.write(HIGH)
        time.sleep(0.1)
        GREEN.write(LOW)
        time.sleep(0.1)
        YELLOW.write(LOW)
        GREEN.write(HIGH)
        time.sleep(0.1)
        YELLOW.write(HIGH)
        time.sleep(0.1)
        GREEN.write(LOW)
        time.sleep(0.1)
        YELLOW.write(LOW)
                
    @bot.message_handler(commands=['open_google'])
    def green_off_telegram(message):
        webbrowser.open_new_tab('https://www.google.com')
        jarvis.speak('Google chrome is open')
    
    bot.polling()
