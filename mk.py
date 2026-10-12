from datetime import datetime, timedelta
# (date, UTC "HH:MM" or None, title, location)
D="Estádio do Dragão, Porto"
g=[
("2026-10-14","19:00","Betis vs FC Porto","Estadio La Cartuja, Sevilha"),
("2026-10-20","19:00","FC Porto vs PSV",D),
("2026-10-24","19:30","Gil Vicente vs FC Porto","Estádio Cidade de Barcelos"),
("2026-10-31","20:30","FC Porto vs Estoril",D),
("2026-11-04",None,"FC Porto vs Napoli",D),
("2026-11-08","18:00","V. Guimarães vs FC Porto","Estádio D. Afonso Henriques, Guimarães"),
("2026-11-24",None,"Feyenoord vs FC Porto","De Kuip, Roterdão"),
("2026-11-29","20:30","FC Porto vs Sporting",D),
("2026-12-06",None,"Santa Clara vs FC Porto","Estádio de São Miguel, Ponta Delgada"),
("2026-12-09",None,"Liverpool vs FC Porto","Anfield, Liverpool"),
("2026-12-13",None,"FC Porto vs Estrela da Amadora",D),
("2026-12-20",None,"Famalicão vs FC Porto","Estádio 22 de Junho, Famalicão"),
("2026-12-27",None,"FC Porto vs Nacional",D),
("2027-01-10",None,"Braga vs FC Porto","Estádio Municipal de Braga"),
("2027-01-17",None,"Alverca vs FC Porto","Complexo Desportivo FC Alverca"),
("2027-01-19",None,"FC Porto vs Slavia Praga",D),
("2027-01-24",None,"FC Porto vs Rio Ave",D),
("2027-01-27",None,"LASK Linz vs FC Porto","Raiffeisen Arena, Linz"),
("2027-01-31",None,"Arouca vs FC Porto","Estádio Municipal de Arouca"),
("2027-02-07",None,"FC Porto vs Académico de Viseu",D),
("2027-02-14",None,"Moreirense vs FC Porto","Estádio Comendador Joaquim de Almeida Freitas"),
("2027-02-21",None,"FC Porto vs Casa Pia",D),
("2027-02-28",None,"Benfica vs FC Porto","Estádio da Luz, Lisboa"),
("2027-03-07",None,"FC Porto vs Marítimo",D),
("2027-03-14",None,"FC Porto vs Gil Vicente",D),
("2027-03-21",None,"Estoril vs FC Porto","Estádio António Coimbra da Mota, Estoril"),
("2027-04-04",None,"FC Porto vs V. Guimarães",D),
("2027-04-11",None,"Sporting vs FC Porto","Estádio José Alvalade, Lisboa"),
("2027-04-18",None,"FC Porto vs Santa Clara",D),
("2027-04-25",None,"Estrela da Amadora vs FC Porto","Estádio José Gomes, Amadora"),
("2027-05-02",None,"FC Porto vs Famalicão",D),
("2027-05-09",None,"Nacional vs FC Porto","Estádio da Madeira, Funchal"),
("2027-05-16",None,"FC Porto vs Braga",D),
]
L=["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//FCPorto//PT","CALSCALE:GREGORIAN"]
for i,(d,t,s,loc) in enumerate(g):
    L+=["BEGIN:VEVENT",f"UID:fcporto-2627-{i}@local","DTSTAMP:20261012T120000Z",f"SUMMARY:⚽ {s}",f"LOCATION:{loc}"]
    dd=datetime.strptime(d,"%Y-%m-%d")
    if t:
        st=datetime.strptime(d+" "+t,"%Y-%m-%d %H:%M")
        L+=[f"DTSTART:{st:%Y%m%dT%H%M%SZ}",f"DTEND:{st+timedelta(hours=2):%Y%m%dT%H%M%SZ}"]
    else:
        L+=[f"DTSTART;VALUE=DATE:{dd:%Y%m%d}",f"DTEND;VALUE=DATE:{dd+timedelta(days=1):%Y%m%d}","DESCRIPTION:Hora por confirmar"]
    L.append("END:VEVENT")
L.append("END:VCALENDAR")
open("FCPorto-2026-27.ics","w",encoding="utf-8").write("\r\n".join(L)+"\r\n")
print(len(g))
