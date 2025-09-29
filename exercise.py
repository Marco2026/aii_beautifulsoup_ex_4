from tkinter import *
import urllib.request, ssl, os, re, sqlite3
from bs4 import BeautifulSoup
from tkinter import messagebox
from datetime import datetime

def get_matches():
    return None

def load_data():
    conn = sqlite3.connect('results.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXIST RESULTS")
    conn.execute('''CREATE TABLE RESULTS (
                 LOCAL              TEXT NOT NULL,
                 VISITANTE          TEXT NOT NULL,
                 GOLES_LOCAL        INT
                 GOLES_VISITANTE    INT
                 GOLES              TEXT,          
                 JORNADA            INT NOT NULL
                 );''')
    
    matches_list = get_matches()

    for m in matches_list():
        conn.execute('''INSERT INTO RESULTS VALUES (?,?,?,?,?)''',m)
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM RESULTS")
    messagebox.showinfo("Database", "Database created successfully \nThere are" + str(cursor.fetchone()[0]) + " results")
    conn.close()

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
