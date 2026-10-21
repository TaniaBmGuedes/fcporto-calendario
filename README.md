# fcporto-calendario

Unofficial football fixtures calendars (.ics) for iPhone, Mac and Google Calendar: FC Porto, Real Madrid, Chelsea, Liverpool, Manchester City, Manchester United, Arsenal and PSG.

Calendários não oficiais dos jogos de várias equipas, em ficheiros `.ics`, para importar no Calendário do iPhone, Mac ou Google.

> Não é oficial. Datas e horas podem mudar; confirma sempre no site do clube ou da liga.

## Calendários 2026-27

| Equipa            | Ficheiro                  | Provas                        |
|-------------------|---------------------------|-------------------------------|
| FC Porto          | `FCPorto-2026-27.ics`     | Liga Portugal + Champions     |
| Real Madrid       | `RealMadrid-2026-27.ics`  | LaLiga + Champions            |
| Chelsea           | `Chelsea-2026-27.ics`     | Premier League                |
| Liverpool         | `Liverpool-2026-27.ics`   | Premier League + Champions    |
| Manchester City   | `ManCity-2026-27.ics`     | Premier League + Champions    |
| Manchester United | `ManUtd-2026-27.ics`      | Premier League + Champions    |
| Arsenal           | `Arsenal-2026-27.ics`     | Premier League + Champions    |
| PSG               | `PSG-2026-27.ics`         | Ligue 1 + Champions           |

## Importar

1. Descarrega o ficheiro da equipa e da época que queres, por exemplo `FCPorto-2026-27.ics`.
2. Abre-o no Calendário (Mac) ou importa-o no Google Calendar.
3. Escolhe um calendário iCloud para sincronizar com o iPhone.

Jogos sem hora marcada ficam como eventos de dia inteiro, com "Hora por confirmar" na descrição.

## Estrutura

```
mk.py                          # gerador
importar.py                    # descarrega jogos (todas as equipas menos o FC Porto)
fixtures/<equipa>/2026-27.csv  # jogos da época
<Equipa>-2026-27.ics           # resultado
```

Equipas: `fcporto`, `realmadrid`, `chelsea`, `liverpool`, `mancity`, `manutd`, `arsenal`, `psg`.

## Gerar uma época

```
python3 mk.py fcporto 2026-27   # uma equipa
python3 mk.py all 2026-27       # todas
```

O script lê `fixtures/<equipa>/<época>.csv` e cria `<Equipa>-<época>.ics`.

### Atualizar horas (equipas estrangeiras)

```
python3 importar.py 2026-27
python3 mk.py all 2026-27
```

`importar.py` vai buscar a Premier League, LaLiga, Ligue 1 e provas da UEFA a [fixturedownload.com](https://fixturedownload.com) e reescreve os CSV dessas 7 equipas. Edições à mão nesses CSV perdem-se quando voltas a correr o script. O FC Porto continua a ser editado à mão.

As rondas que a TV ainda não marcou vêm com horas provisórias (ex.: todas às 15:00 em Inglaterra). Quando uma ronda tem só uma ou duas horas diferentes, o script trata-a como "Hora por confirmar". A data é a do fim de semana previsto e ainda pode mudar.

### Formato do CSV

| Coluna     | Descrição                                                        |
|------------|------------------------------------------------------------------|
| `date`     | `AAAA-MM-DD`                                                     |
| `time`     | `HH:MM` em hora de Lisboa. Vazio = evento de dia inteiro         |
| `match`    | Ex.: `FC Porto vs Sporting`                                      |
| `location` | Estádio (e cidade, nos jogos do FC Porto)                        |

### Nova época

1. FC Porto: cria `fixtures/fcporto/2027-28.csv` com estas colunas.
2. Outras equipas: corre `python3 importar.py 2027-28` (confirma primeiro as ligas e provas europeias de cada equipa em `importar.py`).
3. Corre `python3 mk.py all 2027-28`.

Quando uma liga marcar uma hora, atualiza o CSV e volta a correr o script. Os IDs dos eventos vêm da equipa, da data e do jogo, por isso os eventos não alterados mantêm o mesmo ID. Se o Calendário duplicar jogos ao reimportar, apaga os antigos primeiro.

## Estado dos dados 2026-27

- **FC Porto:** reunidos a partir de fontes públicas. Horas do Betis e do PSV, datas europeias e jogos sem hora estão por confirmar.
- **Outras equipas:** época inteira (desde agosto, incluindo jogos já disputados), obtida de fixturedownload.com a 21/10/2026. Inclui a liga e a fase de liga da Champions. O Chelsea não está em provas europeias. A fase a eliminar da Champions ainda não está incluída.
- Taças nacionais não incluídas.
