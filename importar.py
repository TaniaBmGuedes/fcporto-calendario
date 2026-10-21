"""Cria fixtures/<equipa>/<época>.csv a partir de fixturedownload.com (liga + Champions).

Uso: python3 importar.py 2026-27
Volta a correr quando as ligas marcarem horas novas e depois corre mk.py.

Rondas da liga em que todos os jogos têm a mesma hora (ou só duas horas diferentes)
ainda não foram marcadas pela TV: ficam sem hora ("Hora por confirmar").
"""
import csv, io, os, subprocess, sys
from collections import defaultdict
from datetime import datetime
from zoneinfo import ZoneInfo

LISBON, UTC = ZoneInfo("Europe/Lisbon"), ZoneInfo("UTC")
season = sys.argv[1]
year = season[:4]

LEAGUES = {  # código fixturedownload, fuso da liga
    "epl": ("epl", "Europe/London"),
    "laliga": ("la-liga", "Europe/Madrid"),
    "ligue1": ("ligue-1", "Europe/Paris"),
}
EUROPE = ["champions-league", "europa-league", "conference-league"]

# equipa -> (liga, nome na liga, nome na UEFA)
TEAMS = {
    "realmadrid": ("laliga", "Real Madrid", "Real Madrid"),
    "chelsea": ("epl", "Chelsea", "Chelsea"),
    "liverpool": ("epl", "Liverpool", "Liverpool"),
    "mancity": ("epl", "Man City", "Man City"),
    "manutd": ("epl", "Man Utd", "Man Utd"),
    "arsenal": ("epl", "Arsenal", "Arsenal"),
    "psg": ("ligue1", "Paris Saint-Germain", "Paris"),
}

NAMES = {
    # Premier League
    "Man Utd": "Manchester United", "Man City": "Manchester City", "Spurs": "Tottenham",
    "Nott'm Forest": "Nottingham Forest", "Hull": "Hull City", "Ipswich": "Ipswich Town",
    "Coventry": "Coventry City", "Leeds": "Leeds United", "Newcastle": "Newcastle United",
    # LaLiga
    "Atlético de Madrid": "Atlético de Madrid", "CA Osasuna": "Osasuna", "Celta": "Celta de Vigo",
    "Deportivo Alavés": "Alavés", "Elche CF": "Elche", "FC Barcelona": "Barcelona",
    "Getafe CF": "Getafe", "Levante UD": "Levante", "Málaga CF": "Málaga",
    "R. Racing Club": "Racing de Santander", "RC Deportivo": "Deportivo da Corunha",
    "RCD Espanyol de Barcelona": "Espanyol", "Real Betis": "Betis", "Sevilla FC": "Sevilha",
    "Valencia CF": "Valência", "Villarreal CF": "Villarreal",
    # Ligue 1
    "AJ Auxerre": "Auxerre", "AS Monaco": "Mónaco", "Angers SCO": "Angers", "Estac Troyes": "Troyes",
    "FC Lorient": "Lorient", "Havre Athletic Club": "Le Havre", "LOSC Lille": "Lille",
    "Le Mans FC": "Le Mans", "OGC Nice": "Nice", "Olympique Lyonnais": "Lyon",
    "Olympique de Marseille": "Marselha", "Paris Saint-Germain": "PSG", "RC Lens": "Lens",
    "RC Strasbourg Alsace": "Estrasburgo", "Stade Brestois 29": "Brest", "Stade Rennais FC": "Rennes",
    "Toulouse FC": "Toulouse",
    # UEFA
    "Atleti": "Atlético de Madrid", "B. Dortmund": "Borussia Dortmund", "Bayern München": "Bayern Munique",
    "Porto": "FC Porto", "Paris": "PSG", "Slavia Praha": "Slavia Praga", "LASK": "LASK Linz",
    "S. Bratislava": "Slovan Bratislava", "Sporting CP": "Sporting", "Leipzig": "RB Leipzig",
    "Shakhtar": "Shakhtar Donetsk", "AEK Athens": "AEK Atenas", "Villarreal": "Villarreal",
}


def fetch(code):
    url = f"https://fixturedownload.com/download/{code}-{year}-UTC.csv"
    # curl em vez de urllib: o Python do python.org no Mac não traz certificados SSL
    data = subprocess.run(["curl", "-sfL", url], capture_output=True, check=True).stdout
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))


def kickoff(row):
    return datetime.strptime(row["Date"], "%d/%m/%Y %H:%M").replace(tzinfo=UTC)


def row_out(row, tbc, tz):
    ko = kickoff(row)
    if tbc:  # data do fim de semana previsto, na hora local da liga
        date, time = ko.astimezone(ZoneInfo(tz)).strftime("%Y-%m-%d"), ""
    else:
        local = ko.astimezone(LISBON)
        date, time = local.strftime("%Y-%m-%d"), local.strftime("%H:%M")
    home, away = (NAMES.get(t, t) for t in (row["Home Team"], row["Away Team"]))
    return {"date": date, "time": time, "match": f"{home} vs {away}", "location": row["Location"].strip()}


leagues = {k: fetch(code) for k, (code, _) in LEAGUES.items()}
europe = [r for code in EUROPE for r in fetch(code)]

# rondas por marcar: todos os jogos da ronda com uma ou duas horas locais
tbc_rounds = {}
for k, rows in leagues.items():
    tz = ZoneInfo(LEAGUES[k][1])
    times = defaultdict(set)
    for r in rows:
        times[r["Round Number"]].add(kickoff(r).astimezone(tz).strftime("%H:%M"))
    tbc_rounds[k] = {rnd for rnd, t in times.items() if len(t) <= 2}

for team, (lg, league_name, uefa_name) in TEAMS.items():
    tz = LEAGUES[lg][1]
    out = [row_out(r, r["Round Number"] in tbc_rounds[lg], tz)
           for r in leagues[lg] if league_name in (r["Home Team"], r["Away Team"])]
    out += [row_out(r, False, tz)
            for r in europe if uefa_name in (r["Home Team"], r["Away Team"])]
    out.sort(key=lambda r: (r["date"], r["time"]))
    path = f"fixtures/{team}/{season}.csv"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, ["date", "time", "match", "location"], quoting=csv.QUOTE_MINIMAL)
        w.writeheader(); w.writerows(out)
    print(f"{path}: {len(out)} jogos, {sum(not r['time'] for r in out)} sem hora")
