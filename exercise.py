from tkinter import *
import urllib.request, ssl, os, re, sqlite3
from bs4 import BeautifulSoup
from tkinter import messagebox
from datetime import datetime

def load_data():
    pass

def list_journeys():
    pass

def search_journey():
    pass

def statistics_journey():
    pass

def search_goals():
    pass

def root_window():
    root = Tk()
    root.geometry("400x300")
    root.title("Beautifulsoup exercise 4")

    ### BUTTONS

    Button(root, text='Load Results', command=load_data).pack()
    Button(root, text='List journeys', command=list_journeys).pack()
    Button(root, text='Search journey', command=search_journey).pack()
    Button(root, text='Statistics journey', command=statistics_journey).pack()
    Button(root, text='Search goals', command=search_goals).pack()

    root.mainloop()

if __name__ == "__main__":
    root_window()