# fcporto-calendario

Unofficial FC Porto fixtures calendar (.ics) for iPhone, Mac and Google Calendar.

Calendário não oficial dos jogos do FC Porto, em ficheiro `.ics`, para importar no Calendário do iPhone, Mac ou Google.

> Não é oficial. Datas e horas podem mudar; confirma sempre no site do clube ou da Liga Portugal.

## Importar

1. Descarrega o ficheiro da época que queres, por exemplo `FCPorto-2026-27.ics`.
2. Abre-o no Calendário (Mac) ou importa-o no Google Calendar.
3. Escolhe um calendário iCloud para sincronizar com o iPhone.

Jogos sem hora marcada ficam como eventos de dia inteiro, com "Hora por confirmar" na descrição.

## Estrutura

```
mk.py                 # gerador
fixtures/2026-27.csv  # jogos da época
FCPorto-2026-27.ics   # resultado
```

## Gerar uma época

```
python3 mk.py 2026-27
```

O script lê `fixtures/<época>.csv` e cria `FCPorto-<época>.ics`.

### Formato do CSV

| Coluna     | Descrição                                                        |
|------------|------------------------------------------------------------------|
| `date`     | `AAAA-MM-DD`                                                     |
| `time`     | `HH:MM` em hora de Lisboa. Vazio = evento de dia inteiro         |
| `match`    | Ex.: `FC Porto vs Sporting`                                      |
| `location` | Estádio e cidade                                                 |

### Nova época

1. Cria `fixtures/2027-28.csv` com estas colunas.
2. Corre `python3 mk.py 2027-28`.

Quando a Liga marcar uma hora, edita a linha no CSV e volta a correr o script. Os IDs dos eventos vêm da data e do jogo, por isso os eventos não alterados mantêm o mesmo ID. Se o Calendário duplicar jogos ao reimportar, apaga os antigos primeiro.

## Estado dos dados 2026-27

Reunidos a partir de fontes públicas. Horas do Betis e do PSV, datas europeias e jogos sem hora estão por confirmar. Taças nacionais não incluídas.
