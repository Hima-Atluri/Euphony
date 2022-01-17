from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
import tkinter.font as font
import pygame
from pygame import mixer
import os
import voice_recog
import pyttsx3
import sqlite3

def player(u):
    
    def temp_text(e):           #to remove the text from search box
        Search.delete('1.0',END)
        
    def playsong():
        if(songstatus.get()=="Paused"):
            songstatus.set("Resuming")
            mixer.music.unpause()
        else:
            if len(playlist.curselection()):
                currentsong=playlist.get(ACTIVE)
            elif len(recentlist.curselection()):
                currentsong=recentlist.get(ACTIVE)
            cursor.execute("INSERT INTO {} (song) VALUES(?)".format(u),(str(currentsong),))
            conn.commit()
            mixer.music.load(currentsong)
            songstatus.set("Playing")
            mixer.music.play()
    def pausesong():
        songstatus.set("Paused")
        mixer.music.pause()
    def change_vol(_=None):
        mixer.music.set_volume(vol.get())
        
    def intro():
        engine=pyttsx3.init()
        voices=engine.getProperty('voices')
        engine.setProperty('voice','voices[1].id')
        engine.say("Hi Welcome to Euphony")
        engine.runAndWait()
    
    def search_song(s):
        s=s.lower()
        print(s)
        if(s=="Play recently played song".lower()):
            for row in cursor.execute("SELECT DISTINCT song FROM {} ".format(u)):
                mixer.music.load(row[0])
                songstatus.set("Playing")
                mixer.music.play()
        elif(s=="stop" or s=="top"):
            pausesong()
        elif(s=="play"):
             playsong()
        else:
            s+=".mp3"  
            l=[]
            l=s.split()
            os.chdir(r'C:\Users\Hima\Documents\Mini project\Songs')
            for root, dir, files in os.walk("C:"):
                for f in files:
                    f=f.lower()
                    for i in range(len(l)):
                        if l[i] in f:
                             cursor.execute("INSERT INTO {} (song) VALUES(?)".format(u),(str(f),))
                             conn.commit()
                             print(f)
                             mixer.music.load(f)
                             songstatus.set("Playing")
                             mixer.music.play()
                             break
                    
    
    def callback(g):
        if(g=="Melody"):
            o="\Melody"
        elif(g=="Sad"):
            o="\Sad"
        elif(g=="Party"):
            o="\Party"
        elif(g=="Devotional"):
            o="\Devotional"
        elif(g=="All"):
            o="\Songs"
        os.chdir(r'C:\Users\Hima\Documents\Mini project'+o)
        songs=os.listdir()
        playlist.delete(0,END)
        for s in songs:
           playlist.insert(END,s)
        os.chdir(r'C:\Users\Hima\Documents\Mini project\Songs')

    conn = sqlite3.connect("db_member.db")
    cursor = conn.cursor()    
    #to create window and give title
    root=Tk()
    root.title("Personalized music assistant")
    mixer.init()
    songstatus=StringVar()
    songstatus.set("choosing")
    #to get a full screen window
    width= root.winfo_screenwidth()               
    height= root.winfo_screenheight()               
    root.geometry("%dx%d" % (width, height))
    root.configure(bg="paleturquoise2")
    #insert image
    load= Image.open("Logo_edited.png")
    rload=load.resize((150,150))
    render = ImageTk.PhotoImage(rload)
    img = Label(root, image=render)
    img.place(x=0, y=0)
    #title bar
    title = Label(root, text = "EUPHONY",font =("Algerian", 100),bg="paleturquoise2")
    title.place(x=350,y=0)
    slogan1=Label(root,text="Personalized",font=("Times New Roman",30),bg="paleturquoise2")
    slogan1.place(x=1100,y=0)
    slogan2=Label(root,text="Music",font=("Times New Roman",30),bg="paleturquoise2")
    slogan2.place(x=1150,y=50)
    slogan3=Label(root,text="Assistant",font=("Times New Roman",30),bg="paleturquoise2")
    slogan3.place(x=1130,y=100)
    w = Canvas(root, width=1325, height=30,bg="paleturquoise2",highlightthickness=0)
    w.create_line(15, 25, 10000, 25,width=2)
    w.place(x=0,y=140)

    #buttons
    pl_photo = PhotoImage(file = r"Play button 1.png")
    pl_photoimage = pl_photo.subsample(1,1)
    play_btn=Button(root, text = 'Play', image = pl_photoimage,command=playsong)
    play_btn.place(x=650,y=600)
    pa_photo = PhotoImage(file = r"Pause button 1.png")
    pa_photoimage = pa_photo.subsample(1,1)
    pause_btn=Button(root, text = 'Pause', image = pa_photoimage,command=pausesong)
    pause_btn.place(x=500,y=600)
    vol = Scale(root,from_ = 1,to = 0,orient = HORIZONTAL ,bg="paleturquoise2",highlightthickness=0,length=150,width=20,resolution = .1,command=change_vol)
    vol.set(1)
    vol.place(x=850,y=610)

    #search
    vs=Label(root, text = "Voice Search:", font = ("Times New Roman", 15,'bold'),bg="paleturquoise2")
    vs.place(x=50,y=200)
    vs_photo = PhotoImage(file = r"Voice Search.png")
    vs_photoimage = vs_photo.subsample(3,3)
    vs_btn=Button(root, text = 'Voice Search', image = vs_photoimage,command=lambda:search_song(voice_recog.voice_recognizer()))
    vs_btn.place(x=180,y=180)

    Search = Text(root, height = 1, width = 40, bg = "light cyan",font=("Times New Roman",15))
    Search.insert(END,'Search')
    Search.place(x=475,y=200)
    Search.bind("<FocusIn>", temp_text)
    s_photo = PhotoImage(file = r"Search.png")
    s_photoimage = s_photo.subsample(3,3)
    s_btn=Button(root,text = 'Search',image = s_photoimage,command=lambda:search_song(Search.get('1.0',END)[:len(Search.get('1.0',END))-1]))
    s_btn.place(x=900,y=180)
    
    #genre
    genre=Label(root,text="Genre",font=("Times New Roman", 30,'bold'),bg="paleturquoise2")
    genre.place(x=1100,y=220)
    melody_photo = PhotoImage(file = r"Melody_pic.png")
    melody_btn=Button(root,text = 'Melody',image = melody_photo,command=lambda:callback("Melody"),width=125,height=125)
    melody_btn.place(x=1020,y=275)
    sad_photo = PhotoImage(file = r"Sad_pic.png")
    sad_btn=Button(root,text = 'Sad',image = sad_photo,command=lambda:callback("Sad"),width=125,height=125)
    sad_btn.place(x=1170,y=275)
    par_photo = PhotoImage(file = r"Party_pic.png")
    par_btn=Button(root,text = 'Party',image = par_photo,command=lambda:callback("Party"),width=125,height=125)
    par_btn.place(x=1020,y=425)
    dev_photo = PhotoImage(file = r"Dev_pic.png")
    dev_btn=Button(root,text = 'Devotional',image = dev_photo,command=lambda:callback("Devotional"),width=125,height=125)
    dev_btn.place(x=1170,y=425)
    all_btn=Button(root,text='ALL',command=lambda:callback("All"),font=("Source Sans Pro SemiBold", 15,'bold'))
    all_btn.place(x=1125,y=570)

    #playlist
    frame=Frame(root)
    playlist=Listbox(frame,selectmode=SINGLE,bg="paleturquoise2",font=("Times New Roman",15),width=40)
    scrollbar = Scrollbar(frame)
    scrollbar.pack(side = RIGHT, fill = Y)
    scrollbar.config(command = playlist.yview)
    os.chdir(r'C:\Users\Hima\Documents\Mini project\Songs')
    songs=os.listdir()
    playlist.delete(0,END)
    for s in songs:
         playlist.insert(END,s)
    playlist.pack()
    frame.place(x=475,y=300)

    #recently played list
    fr=Frame(root)
    r = Label(fr, text = "Recently Played",font = ("Times New Roman", 15,'bold'))
    recentlist=Listbox(fr,selectmode=SINGLE,bg="paleturquoise2",font=("Times New Roman",15),width=30,height=8)
    for row in cursor.execute("SELECT DISTINCT song FROM {} ".format(u)):
        recentlist.insert(END,row[0])
    scrollbar = Scrollbar(fr)
    scrollbar.pack(side = RIGHT, fill = Y)
    scrollbar.config(command = recentlist.yview)
    r.pack()
    recentlist.pack()
    fr.place(x=50,y=320)

    intro()
    root.mainloop() 
