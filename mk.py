"""Gera um .ics a partir de fixtures/<época>.csv.

Uso: python3 mk.py 2026-27
CSV: date (AAAA-MM-DD), time (HH:MM hora de Lisboa; vazio = dia inteiro), match, location
"""
import csv, re, sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

LISBON, UTC = ZoneInfo("Europe/Lisbon"), ZoneInfo("UTC")
season = sys.argv[1]
L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//FCPorto//PT", "CALSCALE:GREGORIAN"]
stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")

with open(f"fixtures/{season}.csv", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        slug = re.sub(r"[^a-z0-9]+", "-", r["match"].lower()).strip("-")
        L += ["BEGIN:VEVENT", f"UID:fcporto-{r['date']}-{slug}@local", f"DTSTAMP:{stamp}",
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

out = f"FCPorto-{season}.ics"
open(out, "w", encoding="utf-8").write("\r\n".join(L) + "\r\n")
print(f"{out} gerado")
