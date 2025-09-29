from tkinter import *
import urllib.request, ssl, os, re, sqlite3
from bs4 import BeautifulSoup
from tkinter import messagebox
from datetime import datetime

def root_window():
    root = Tk()
    root.geometry("400x300")
    root.title("Beautifulsoup exercise 2")

    ## MENU BAR

    menubar = Menu(root)

    ### DATA

    datamenu = Menu(menubar, tearoff=0)
    datamenu.add_command(label="Load", command=load_data)
    datamenu.add_command(label="List", command=lambda: list_films(mode='COMPLETE'))
    datamenu.add_separator()
    datamenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="Data", menu=datamenu)

    ### SEARCH

    searchmenu = Menu(menubar, tearoff=0)
    searchmenu.add_command(label="Title", command=open_title_entry_window)
    searchmenu.add_command(label="Date", command=open_date_entry_window)
    searchmenu.add_command(label="Genres", command=open_genres_spinbox_window)
    menubar.add_cascade(label="Search", menu=searchmenu)

    root.config(menu=menubar)

    root.mainloop()

if __name__ == "__main__":
    root_window()