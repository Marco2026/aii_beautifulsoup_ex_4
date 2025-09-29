from tkinter import *
import urllib.request, ssl, os, re, sqlite3
from bs4 import BeautifulSoup
from tkinter import messagebox
from datetime import datetime

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context=ssl._create_unverified_context

def get_matches():
    return None

def load_data():
    conn = sqlite3.connect('results.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXIST RESULTS")
    conn.execute('''CREATE TABLE RESULTS (
                 LOCAL              TEXT NOT NULL,
                 VISITANTE          TEXT NOT NULL,
                 GOLES_LOCAL        INT,
                 GOLES_VISITANTE    INT,
                 LISTA_GOLES_LOCAL              TEXT,
                 LISTA_GOLES_VISITANTE              TEXT,          
                 JORNADA            INT NOT NULL
                 );''')
    
    matches_list = get_matches()

    for m in matches_list():
        conn.execute('''INSERT INTO RESULTS VALUES (?,?,?,?,?,?,?)''',m)
    conn.commit()
    cursor = conn.execute("SELECT COUNT(*) FROM RESULTS")
    messagebox.showinfo("Database", "Database created successfully \nThere are" + str(cursor.fetchone()[0]) + " results")
    conn.close()

def list_journeys(mode='COMPLETE', journey=0, local_team='Barcelona'):
    conn = sqlite3.connect("results.db")
    if mode == 'COMPLETE':
        journeys = list(conn.execute("SELECT * FROM RESULTS ORDER BY journey DESC"))
    elif mode == 'SEARCH_JOURNEY':
        query = "SELECT * FROM RESULTS WHERE journey = ?"
        param = (journey,)
        journeys = list(conn.execute(query, param))
    elif mode == 'STATISTICS_JOURNEY':
        pass
    elif mode == 'SEARCH_GOALS':
        pass

    list_window = Toplevel()
    list_window.title("List window")
    list_window.geometry("800x600")
    list_window_scrollbar = Scrollbar(list_window)
    list_window_scrollbar.pack(side=RIGHT, fill=Y)
    journeys_listbox = Listbox(master=list_window, width=800, height=600, yscrollcommand=list_window_scrollbar.set)
    journeys_listbox.insert(END, *journeys)
    journeys_listbox.pack()
    list_window_scrollbar.config(command=journeys_listbox.yview)

def search_journey():
    journeys_spinbox_window = Toplevel()
    journeys_spinbox_window.title("Select journey")
    journeys_spinbox_window.geometry("200x100")
    
    conn = sqlite3.connect("results.db")
    journeys = conn.execute("SELECT COUNT(DISTINCT(JOURNEY)) FROM RESULTS").fetchone()[0]
    conn.close()
    
    selected = StringVar(value=0)
    journeys_spinbox = Spinbox(journeys_spinbox_window, from_=0, to=journeys, textvariable=selected)
    journeys_spinbox.pack()

    def confirm():
        list_journeys(mode="SEARCH_JOURNEY", journey=int(selected.get()))
        journeys_spinbox_window.destroy()

    Button(journeys_spinbox_window, text="Accept", command=confirm).pack(pady=5)

def statistics_journey():
    journeys_spinbox_window = Toplevel()
    journeys_spinbox_window.title("Select journey")
    journeys_spinbox_window.geometry("200x100")
    
    conn = sqlite3.connect("results.db")
    journeys = conn.execute("SELECT COUNT(DISTINCT(JOURNEY)) FROM RESULTS").fetchone()[0]
    conn.close()
    
    selected = StringVar(value=0)
    journeys_spinbox = Spinbox(journeys_spinbox_window, from_=0, to=journeys, textvariable=selected)
    journeys_spinbox.pack()

    def confirm():
        list_journeys(mode="STATISTICS_JOURNEY", journey=int(selected.get()))
        journeys_spinbox_window.destroy()

    Button(journeys_spinbox_window, text="Accept", command=confirm).pack(pady=5)

def search_goals():
    journeys_spinbox_window = Toplevel()
    journeys_spinbox_window.title("Select journey")
    journeys_spinbox_window.geometry("200x100")

    conn = sqlite3.connect("results.db")
    journeys = conn.execute("SELECT COUNT(DISTINCT(journey)) FROM results").fetchone()[0]
    teams = list(conn.execute("SELECT DISTINCT(local) FROM results"))
    conn.close()

    selected_journey = StringVar(value=0)
    journey_spinbox = Spinbox(journeys_spinbox_window, from_=0, to=journeys, textvariable=selected_journey)
    journey_spinbox.pack()

    selected_team = StringVar(value=0)
    team_spinbox = Spinbox(journeys_spinbox_window, values=teams, textvariable=selected_team)
    team_spinbox.pack()

    def confirm():
        list_journeys(mode="STATISTICS_JOURNEY", journey=int(selected_journey.get()), local_team=selected_team.get())
        journeys_spinbox_window.destroy()

    Button(journeys_spinbox_window, text="Accept", command=confirm).pack(pady=5)

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
