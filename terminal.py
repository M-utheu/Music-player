from tkinter import *
import customtkinter
import pygame
import os
from CTkListbox import *
from tkinter import filedialog

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

# initialising root
root = customtkinter.CTk()
root.title("BoomBa")
root.iconbitmap('logo.ico')
root.geometry("600x400")

# pygame for the music
pygame.mixer.init()

root.columnconfigure(0, weight=1, uniform='a')
root.columnconfigure(1, weight=1, uniform='a')
root.columnconfigure(2, weight=1, uniform='a')
root.rowconfigure(0, weight=1, uniform='a')
root.rowconfigure(1, weight=15, uniform='a')
root.rowconfigure(2, weight=1, uniform='a')


def aut_songs():
    for filename in os.listdir("songs/"):
        if filename.endswith(".mp3"):
            song = filename.replace(".mp3", "")
            songlist.insert("END", song)


songlist = CTkListbox(root, bg_color="black")
songlist.grid(row=1, column=0, sticky='nswe', padx=20)

aut_songs()

songs_folder = "songs/"
musicplayer_dir = os.path.dirname(os.path.realpath(__file__))
full_path_backslash = os.path.join(musicplayer_dir, songs_folder)
full_path = full_path_backslash.replace("\\", "/")


def add_songs():
    songs = filedialog.askopenfilenames(initialdir="songs/", title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))
    for song in songs:
        song = song.replace(full_path, "")
        song = song.replace(".mp3", "")
        songlist.insert("END", song)


def play_music(song):
    song = songlist.get(songlist.curselection())
    song = f"{full_path}{song}.mp3"
    play_pause_button.configure(image=pause_img)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    paused = True


def stop_music():
    pygame.mixer.music.stop()


paused = False


def pause_music():
    global paused
    if paused:
        pygame.mixer.music.unpause()
        play_pause_button.configure(image=play_img)
        paused = False


    else:
        pygame.mixer.music.pause()
        play_pause_button.configure(image=pause_img)
        paused = True


def next_song():
    nextsong = songlist.curselection()
    nextsong = nextsong[0] + 1
    song = songlist.get(nextsong)

    play_music(song)


def previous_song():
    prevsong = songlist.curselection()
    prevsong = prevsong[0] - 1
    song = songlist.get(prevsong)

    play_music(song)


back_img = PhotoImage(file=r"previous.png")
forward_img = PhotoImage(file=r"next.png")
pause_img = PhotoImage(file=r"pause.png")
play_img = PhotoImage(file=r"play.png")
stop_img = PhotoImage(file=r"stop.png")

controls = customtkinter.CTkFrame(master=root)
controls.grid(row=2, column=0, sticky='nw', columnspan=3, padx=20)

back_button = Button(controls, image=back_img, borderwidth=0, command=previous_song)
forward_button = Button(controls, image=forward_img, borderwidth=0, command=next_song)
play_pause_button = Button(controls, image=play_img, borderwidth=0, command=pause_music)
stop_button = Button(controls, image=stop_img, borderwidth=0, command=stop_music)
songlist.bind("<<ListboxSelect>>", "play_music")

back_button.grid(row=0, column=0, padx=10, pady=40)
forward_button.grid(row=0, column=1, padx=10, pady=40)
play_pause_button.grid(row=0, column=2, padx=10, pady=40)
stop_button.grid(row=0, column=4, padx=10, pady=40)

menuOptions = ["Add Songs"]

my_menu = customtkinter.CTkOptionMenu(master=root, values=menuOptions, command=add_songs)
my_menu.grid(row=0, column=0, rowspan=3, sticky="nw")
root.mainloop()
