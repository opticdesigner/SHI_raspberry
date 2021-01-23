from tkinter import *

class Linebox():
    def __init__(self,w):
        #設定視窗基本功能
        w.title('溫度和光線的感應')
        w.option_add("*font",("verdana",18,"bold"))
        w.option_add("*background", "#068587")
        w.option_add("*foreground", "#ffffff")

        #設定介面
        mainFrame = Frame(w,borderwidth=2,relief=GROOVE,padx=100,pady=10)
        Label(mainFrame, text="室內溫度:").grid(row=0, column=0, sticky=E, padx=5, pady=20)
        Label(mainFrame, text="室內光線:").grid(row=1, column=0, sticky=E, padx=5, pady=20)
        Label(mainFrame, text="可變電阻:").grid(row=2, column=0, sticky=E, padx=5, pady=20)
        Label(mainFrame, text="10").grid(row=0, column=1, sticky=E, padx=5, pady=20)
        Label(mainFrame, text="89").grid(row=1, column=1, sticky=E, padx=5, pady=20)
        Label(mainFrame, text="75").grid(row=2, column=1, sticky=E, padx=5, pady=20)
        mainFrame.pack(padx=10, pady=10)
        
