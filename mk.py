"""Gera um .ics a partir de fixtures/<equipa>/<época>.csv.

Uso: python3 mk.py <equipa> <época>    ex.: python3 mk.py fcporto 2026-27
     python3 mk.py all <época>         gera todas as equipas
CSV: date (AAAA-MM-DD), time (HH:MM hora de Lisboa; vazio = dia inteiro), match, location
"""
import csv, re, sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

LISBON, UTC = ZoneInfo("Europe/Lisbon"), ZoneInfo("UTC")
# equipa -> prefixo do ficheiro .ics
TEAMS = {
    "fcporto": "FCPorto", "realmadrid": "RealMadrid", "chelsea": "Chelsea", "liverpool": "Liverpool",
    "mancity": "ManCity", "manutd": "ManUtd", "arsenal": "Arsenal", "psg": "PSG",
}


def build(team, season):
    L = ["BEGIN:VCALENDAR", "VERSION:2.0", f"PRODID:-//{TEAMS[team]}//PT", "CALSCALE:GREGORIAN"]
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    with open(f"fixtures/{team}/{season}.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            slug = re.sub(r"[^a-z0-9]+", "-", r["match"].lower()).strip("-")
            L += ["BEGIN:VEVENT", f"UID:{team}-{r['date']}-{slug}@local", f"DTSTAMP:{stamp}",
                  f"SUMMARY:⚽ {r['match']}", f"LOCATION:{r['location']}"]
            if r["time"]:
                st = datetime.strptime(f"{r['date']} {r['time']}", "%Y-%m-%d %H:%M").replace(tzinfo=LISBON).astimezone(UTC)
                L += [f"DTSTART:{st:%Y%m%dT%H%M%SZ}", f"DTEND:{st + timedelta(hours=2):%Y%m%dT%H%M%SZ}"]
            else:
                d = datetime.strptime(r["date"], "%Y-%m-%d")
                L += [f"DTSTART;VALUE=DATE:{d:%Y%m%d}", f"DTEND;VALUE=DATE:{d + timedelta(days=1):%Y%m%d}",
                      "DESCRIPTION:Hora por confirmar"]
            L.append("END:VEVENT")
    L.append("END:VCALENDAR")

    out = f"{TEAMS[team]}-{season}.ics"
    open(out, "w", encoding="utf-8").write("\r\n".join(L) + "\r\n")
    print(f"{out} gerado")


team, season = sys.argv[1], sys.argv[2]
for t in (TEAMS if team == "all" else [team]):
    build(t, season)
