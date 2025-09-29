from tkinter import *
import urllib.request, ssl, os, re, sqlite3
from bs4 import BeautifulSoup
from tkinter import messagebox
from datetime import datetime

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context=ssl._create_unverified_context

def get_all_matches_data(url):
    matchdays = get_matchdays(url)
    # print(f"Número de jornadas: {len(matchdays)}")
    all_matches = []
    for matchday in matchdays:
        matches, matchday_number = get_matches(matchday)
        # print(f"Jornada {matchday_number} - {len(matches)} partidos")
        for match in matches:
            match_info = get_match_info(match, matchday_number)
            all_matches.append(match_info)
            # print(match_info)
    print(f"Número total de partidos: {len(all_matches)}")
    print(f"Número de jornadas: {len(matchdays)}")
    return all_matches


def get_matchdays(url):
    f = urllib.request.urlopen(url)
    s = BeautifulSoup(f, "lxml")
    matchdays = s.find_all("div", class_="cont-modulo resultados")
    # print(f"Número de jornadas: {len(matchdays)}")
    return matchdays

def get_matches(matchday_div):
    matchday_number = matchday_div.get("id").replace("jornada-","")
    matches = matchday_div.find("table", class_="tabla-datos").find("tbody").find_all("tr")
    # print(f"Jornada {matchday_number} - {len(matches)} partidos")
    return matches, matchday_number

def get_match_info(match, matchday_number):
    local = match.find("td", class_="col-equipo-local").text.strip()
    visit = match.find("td", class_="col-equipo-visitante").text.strip()
    score = match.find("td", class_="col-resultado").text.strip().split("-")
    local_score = score[0].strip()
    visit_score = score[1].strip()
    match_link = match.find("td", class_="col-resultado").find("a")['href']
    local_goals, visit_goals = parse_goals_from_link(match_link)
    match_info = {
        'matchday': matchday_number,
        'local': local,
        'local_score': local_score,
        'local_goals': local_goals,
        'visit': visit,
        'visit_score': visit_score,
        'visit_goals': visit_goals,
    }
    # print(match_info)
    return match_info

def parse_goals_from_link(match_link):
    f = urllib.request.urlopen(match_link)
    s = BeautifulSoup(f, "lxml")    
    local_goals = s.find("div", class_="scr-hdr__team is-local").find("div", class_="scr-hdr__scorers").text
    visit_goals = s.find("div", class_="scr-hdr__team is-visitor").find("div", class_="scr-hdr__scorers").text
    return local_goals, visit_goals

def load_data():
    conn = sqlite3.connect('results.db')
    conn.text_factory = str
    conn.execute("DROP TABLE IF EXISTS RESULTS")
    conn.execute('''CREATE TABLE RESULTS (
                 LOCAL              TEXT NOT NULL,
                 VISITANTE          TEXT NOT NULL,
                 GOLES_LOCAL        INT,
                 GOLES_VISITANTE    INT,
                 LISTA_GOLES_LOCAL              TEXT,
                 LISTA_GOLES_VISITANTE              TEXT,          
                 JORNADA            INT NOT NULL
                 );''')
    
    matches_list = get_all_matches_data("https://as.com/resultados/futbol/primera/2023_2024/calendario/")

    for m in matches_list:
        conn.execute('''INSERT INTO RESULTS VALUES (?,?,?,?,?,?,?)''', (m['local'], m['visit'], int(m['local_score']), int(m['visit_score']), m['local_goals'], m['visit_goals'], int(m['matchday'])))
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
