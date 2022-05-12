#Designed by mehranredrose (Mehran Abbasi)
#github : mehranredrose

#importing libraries 
import os
import threading
import time
import tkinter
from pygame import mixer
from tkinter import *
import tkinter.font as font
from tkinter import filedialog
from tkinter import ttk
from mutagen.mp3 import MP3

#----------------------------------------------------
#creating the root window 
root=Tk()
root.title('MEHRUNIHA Music Player')
root.configure(background='black')
#initialize mixer 
mixer.init()


statusbar = ttk.Label(root, text="\t"*2+"\tWelcome to MEHRUNIHA", relief=SUNKEN, anchor=W, font='Dosis')
statusbar.pack(side=BOTTOM, fill=X)

#font is defined which is to be used for the button font 
defined_font = font.Font(family='Dosis')

playlist = []
#----------------------------------------------------
# Root Window : StatusBar, LeftFrame, RightFrame
# LeftFrame : The listbox (playlist)
# RightFrame : TopFrame,MiddleFrame and the BottomFrame

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)

rightframe = Frame(root)
#rightframe.configure(background='black')
rightframe.pack(pady=30)

middleframe = Frame(rightframe)
#middleframe.configure(background='black')
middleframe.pack(pady=30, padx=30)

topframe = Frame(rightframe)
#topframe.configure(background='black')
topframe.pack()

bottomframe = Frame(rightframe)
#bottomframe.configure(background='black')
bottomframe.pack()

#---------------------------------------------------
#Creating list box -- will use for musics
playlistbox = Listbox(leftframe)
playlistbox.pack()


#---------------------------------------------------
#main functions in music player

def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    index += 1

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

    mixer.music.queue(filename_path)

def deletesong():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

def show_details(Play):
    file_data = os.path.splitext(Play)

    if file_data[1] == '.mp3':
        audio = MP3(Play)
        total_length = audio.info.length
    else:
        a = mixer.Sound(Play)
        total_length = a.get_length()

    # div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = "Total Length" + ' - ' + timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            current_time += 1


def Play():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            Stop()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('File not found', 'MEHRUNIHA could not find the file. Please check again.')


def Stop():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"


paused = FALSE

def Pause():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"


def Previous():
    Stop()
    time.sleep(1)
    #to get the selected song index
    selected_song=playlistbox.curselection()
    #to get the previous song index
    previous_one = int(selected_song[0]-1)
    #to get the previous song
    play_it = playlist[previous_one]
    mixer.music.load(play_it)
    mixer.music.play()
    statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
    show_details(play_it)
    playlistbox.selection_clear(0,END)
    #activate new song
    playlistbox.activate(previous_one)
    #set the next song
    playlistbox.selection_set(previous_one)


def Next(): 
    Stop()
    time.sleep(1)   
    #to get the selected song index
    selected_song = playlistbox.curselection()
    #to get the next song index
    next_one = int(selected_song[0]+1)
    play_it = playlist[next_one]
    mixer.music.load(play_it)
    mixer.music.play()
    statusbar['text'] = "Playing music" + ' - ' + os.path.basename(play_it)
    show_details(play_it)
    playlistbox.selection_clear(0,END)
    #activate newsong
    playlistbox.activate(next_one)
     #set the next song
    playlistbox.selection_set(next_one)


def set_vol(val):
    volume = float(val) / 100
    mixer.music.set_volume(volume)
    # set_volume of mixer takes value only from 0 to 1. Example - 0, 0.1,0.55,0.54.0.99,1


def Mute():
    global muted
    if muted:  # Unmute the music
        mixer.music.set_volume(0.7)
        #volumeBtn.configure(image=volumePhoto)
        scale.set(70)
        muted = FALSE
    else:  # mute the music
        mixer.music.set_volume(0)
        #volumeBtn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE

muted = FALSE

#----------------------------------------------------------------------------------------------------
#Labels
lengthlabel = ttk.Label(topframe, text='Total Length : --:--')
#lengthlabel = ttk.Label(topframe, text='Total Length : --:--',background='black',foreground='white')
lengthlabel.pack(pady=5)

#currenttimelabel = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE ,background='black',foreground='white')
currenttimelabel = ttk.Label(topframe, text='Current Time : --:--', relief=GROOVE )
currenttimelabel.pack()

#----------------------------------------------------------
#Buttons

#play button
play_button = ttk.Button(middleframe,text="Play",width =7,command=Play)
play_button.grid(row=0, column=1, padx=10)

#pause button 
pause_button= ttk.Button(middleframe,text="Pause",width =7,command=Pause)
pause_button.grid(row=0, column=2, padx=10)

#stop button
stop_button= ttk.Button(middleframe,text="Stop",width =7,command=Stop)
stop_button.grid(row=0, column=0, padx=10)

previous_button = ttk.Button(rightframe, text="Pervious", command=Previous)
previous_button.pack(side=LEFT)

next_button = ttk.Button(rightframe, text="Next", command=Next)
next_button.pack(side=RIGHT)

# Bottom Frame for volume Scale, mute etc.
volume_button = ttk.Button(bottomframe, text="Mute",width =5, command=Mute)
volume_button.grid(row=1, column=2)

scale = ttk.Scale(bottomframe,from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)  # implement the default value of scale when music player starts
mixer.music.set_volume(0.7)
scale.grid(row=0, column=2, pady=15, padx=30)

#---------------------------------------------------------------------------
#menu 
my_menu=Menu(root)
root.config(menu=my_menu)
add_song_menu=Menu(my_menu)
my_menu.add_cascade(label="Menu",menu=add_song_menu)
add_song_menu.add_command(label="Add songs",command=browse_file)
add_song_menu.add_command(label="Delete song",command=deletesong)


mainloop()