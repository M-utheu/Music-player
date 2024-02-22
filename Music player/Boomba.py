
from tkinter import *
import pygame
from tkinter import filedialog
import os
import random
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk


root = Tk()
pygame.mixer.init()

root.rowconfigure(0,weight = 1)
root.columnconfigure(0,weight = 1)
root.title('MP3 Player')
root.iconbitmap('apple_music_android_logo_icon_134021.ico')
root.geometry('750x550')

page1 = Frame(root)
page2 = Frame(root)

songlist = Listbox(root, bg="black", fg="white", width=80, height = 20, selectbackground="grey", selectforeground="black")


songs_folder = "songs/"
musicplayer_dir = os.path.dirname(os.path.realpath(__file__))
full_path_backslash = os.path.join(musicplayer_dir, songs_folder)
full_path = full_path_backslash.replace("\\", "/")

back_img = PhotoImage(file=r"previous.png")
forward_img = PhotoImage(file=r"next.png")
pause_img = PhotoImage(file=r"pause.png")
play_img = PhotoImage(file=r"play.png")
stop_img = PhotoImage(file=r"stop.png")
shuffle_img = PhotoImage(file=r"shuffle.png")
deactivated_shuffle_img = PhotoImage(file=r"shuffle_deactivated.png")
loop_img = PhotoImage(file = r"loop.png")
activated_loop_img = PhotoImage(file = r"loop_activated.png")

controls = Frame(root)

status_bar = Label(root, text='', bd=2, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

def add_songs():
    songs = filedialog.askopenfilenames(initialdir="songs/", title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    for song in songs:
        song = song.replace(full_path, "")
        song = song.replace(".mp3", "")
        songlist.insert(END, song)

def music_play_time():
    current_play_time = pygame.mixer.music.get_pos() / 1000
    formatted_play_time = time.strftime('%M:%S', time.gmtime(current_play_time))

    current_selection = songlist.curselection()
    if current_selection:  # Check if there's a selection
        selected_index = current_selection[0]
        song = songlist.get(selected_index)
        song = f"{full_path}{song}.mp3"

        mut_song = MP3(song)

        global song_duration
        song_duration = mut_song.info.length
        formatted_song_duration = time.strftime('%M:%S', time.gmtime(song_duration))

        status_bar.config(text=f'Time passed: {formatted_play_time} of {formatted_song_duration}')
    else:
        status_bar.config(text=f'Time passed: {formatted_play_time}')  # Default text if no selection

    status_bar.after(1000, music_play_time)




def play_music(play):
    play_pause_button.configure(image = pause_img)
    song = songlist.get(songlist.curselection())
    song = f"{full_path}{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)


paused = False

def pause_music():
    global paused
    song = songlist.get(songlist.curselection())

    if paused:
        pygame.mixer.music.unpause()
        paused = False
        play_pause_button.configure(image=pause_img)


    else:
        pygame.mixer.music.pause()
        paused = True
        play_pause_button.configure(image=play_img)


def next_song():
    nextsong = songlist.curselection()
    nextsong = nextsong[0]+1
    song = songlist.get(nextsong)
    song = f"{full_path}{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    songlist.selection_clear(0, END)
    songlist.activate(nextsong)
    songlist.selection_set(nextsong, last=None)


def previous_song():
    no_of_songs = songlist.size()
    prevsong = songlist.curselection()
    prevsong = prevsong[0] - 1
    song = songlist.get(prevsong)

    song = f"{full_path}{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    songlist.selection_clear(0, END)
    songlist.activate(prevsong)
    songlist.selection_set(prevsong, last=None)

def next_songloop():
    no_of_songs = songlist.size()  - 1
    nextsong = songlist.curselection()
    nextsong = nextsong[0]+1

    if nextsong > no_of_songs:
        nextsong = 0

    song = songlist.get(nextsong)
    song = f"{full_path}{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    songlist.selection_clear(0, END)
    songlist.activate(nextsong)
    songlist.selection_set(nextsong, last=None)

def previous_songloop():
    no_of_songs = songlist.size() - 1
    prevsong = songlist.curselection()
    prevsong = prevsong[0] - 1
    print(no_of_songs, prevsong)
    if prevsong < 0:
        prevsong = no_of_songs

    song = songlist.get(prevsong)
    song = f"{full_path}{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    songlist.selection_clear(0, END)
    songlist.activate(prevsong)
    songlist.selection_set(prevsong, last=None)
def fwd_with_shuffle():
    no_of_songs = songlist.size()
    nextsong = songlist.curselection()
    n= random.randint(1,no_of_songs)
    nextsong = nextsong[0] + n
    no_of_songs = songlist.size()

    if nextsong>= no_of_songs:
        nextsong = nextsong % no_of_songs

    song = songlist.get(nextsong)

    song = f"{full_path}{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    songlist.selection_clear(0, END)
    songlist.activate(nextsong)
    songlist.selection_set(nextsong, last=None)

def bk_with_shuffle():
    no_of_songs= songlist.size()
    prevsong = songlist.curselection()
    n = random.randint(1, no_of_songs)
    prevsong = prevsong[0] - n
    song = songlist.get(prevsong)

    if prevsong<= no_of_songs:
        prevsong = -(prevsong % no_of_songs)

    song = f"{full_path}{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)

    songlist.selection_clear(0, END)
    songlist.activate(prevsong)
    songlist.selection_set(prevsong, last=None)



def shuffle():
    forward_button.configure(command = fwd_with_shuffle)
    back_button.configure(command = bk_with_shuffle)
    shuffle_button.configure(image = shuffle_img, command = no_shuffle)



def no_shuffle():
    forward_button.configure(command = next_song)
    back_button.configure(command = previous_song)
    shuffle_button.configure(image = deactivated_shuffle_img, command = shuffle)

def loop():
    forward_button.configure(command=next_songloop)
    back_button.configure(command=previous_songloop)
    loop_button.configure(image=activated_loop_img, command=noloop)

def noloop():
    forward_button.configure(command=next_song)
    back_button.configure(command=previous_song)
    loop_button.configure(image=loop_img, command=loop)


def show_frame(frame):
    frame.tkraise()

def slide(z):
    song_slider_label.config(text=f'{int(song_slider.get())} of {int(song_duration)}')


def load_music_player():
    show_frame(page2)

    songlist.pack(side = LEFT,anchor = NW)

    controls.pack()
    back_button.grid(row=0, column=1, padx=5, pady=40)
    forward_button.grid(row=0, column=3, padx=5, pady=40)
    play_pause_button.grid(row=0, column=2, padx=5, pady=40)
    shuffle_button.grid(row=0, column=4, padx=5, pady=40)
    loop_button.grid(row = 0, column = 0, padx = 5, pady = 40)


    my_menu = Menu(root)
    root.config(menu=my_menu)

    addsongmenu = Menu(my_menu)
    my_menu.add_cascade(label="Add songs", menu=addsongmenu)
    addsongmenu.add_command(label="Add Songs to Playlist", command=add_songs)
    music_play_time()

    song_slider_label.pack(pady=10)
    song_slider.pack(pady=30)



def destroybutton(button):
    load_music_player()
    button.destroy()
    label.destroy()

show_frame(page1)
background_img = PhotoImage(file = r"bckgrnd.png")
label = Label(root, image = background_img)
label.pack()
start_img = PhotoImage(file = r"start.png")
start_button = Button(root, image=start_img, borderwidth=0, command=lambda: destroybutton(start_button))
start_button.place(x=320, y=340)


controls = Frame(root)
back_button = Button(controls, image=back_img, borderwidth=0, command=previous_song)
forward_button = Button(controls, image=forward_img, borderwidth=0, command=next_song)
play_pause_button = Button(controls, image=play_img, borderwidth=0, command=pause_music)
shuffle_button = Button(controls, image=deactivated_shuffle_img, borderwidth=0, command=shuffle)
loop_button = Button(controls, image = loop_img, borderwidth = 0, command = loop)
songlist.bind("<<ListboxSelect>>", play_music)

song_slider = ttk.Scale(root, from_=0, to=100, orient=HORIZONTAL, value = 0, command=slide, length=400)
song_slider_label = Label(root, text='0')

root.mainloop()
