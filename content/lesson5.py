import RPi.GPIO as GPIO
from raspigpio.lcd_display import lcd
from tkinter import *
import mfrc522 as MFRC522
import threading
import sys
from time import sleep, time
import datetime
from gpiozero import Buzzer
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class App():
    def __init__(self,window):
        
        #初始化lcd
        self.my_lcd = lcd()

        #初始化buzzer
        self.my_buzzer = Buzzer(16)

        #初始化RFID
        self.previousUid = []
        self.MIFAREReader= MFRC522.MFRC522()
        self.rfidStatusHandler()

        #初始化firestore
        cred = credentials.Certificate("/home/pi/raspberryfirebase-firebase-adminsdk-y4f0x-ce1ddd9e4b.json")
        firebase_admin.initialize_app(cred,{
            'databaseURL': 'https://raspberryfirebase.firebaseio.com/'
            })
        self.firestore = firestore.client()

        

        
    
    def rfidStatusHandler(self):
        (status, tagType)= self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        if status == self.MIFAREReader.MI_OK:
            print("Find Card")
            self.my_lcd.display_string("Find Card",1)
            self.my_lcd.display_string("......",2)
           
            self.cardRuning()  

        else:
            print("Put Car on It")
            self.my_lcd.display_string("Put Car on It",1)
            self.my_lcd.display_string("",2)
         
        threading.Timer(0.5, self.rfidStatusHandler).start()
    
    def cardRuning(self):
        (status, currentUid) = self.MIFAREReader.MFRC522_Anticoll()
        if status == self.MIFAREReader.MI_OK and currentUid != self.previousUid:
             #buzzer sound()
            self.my_buzzer.on()
            sleep(0.2)
            self.my_buzzer.off()

            self.previousUid = currentUid
            print(currentUid)
            cardCode=""
            for singleId in currentUid:
                cardCode += "{:x}.".format(singleId)
            self.my_lcd.display_string("Card ID",1)
            self.my_lcd.display_string(cardCode.upper(),2)
            print(cardCode)
            self.saveToFireStore(cardCode)
    
    def saveToFireStore(self,cardCode):
        doc_ref = self.firestore.collection('Doors').document()
        currentTime = time()
        timestamp = datetime.datetime.fromtimestamp(currentTime)
        date = timestamp.strftime("%Y-%m-%d-%H-%M-%S")
        doc_ref.set({
            'timesamp':timestamp,
            'cardID':cardCode,
            'date':date
        })


def on_closing():
    GPIO.cleanup()
    root.destroy()
    sys.exit()

if __name__ == "__main__":
    GPIO.setwarnings(False)
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app = App(root)
    root.mainloop()
