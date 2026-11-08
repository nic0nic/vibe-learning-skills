# Syntax-Regeln für Buchungssätze

Ergänzt Kap. 2.1 der Handreichung um die konkreten Layout-Regeln, nach denen Buchungssätze in Angabe/Lösung geschrieben werden.

## Grundformen

**Einfacher Buchungssatz** (1 Soll-Konto zu 1 Haben-Konto):

```
7030 KFZST    320,00 €   an   2800 BK   320,00 €
```

**Zusammengesetzter Buchungssatz** – drei Varianten, je nachdem wo mehrere Konten stehen:

a) **Mehrere Soll-Konten, ein Haben-Konto** – alle Soll-Zeilen stehen übereinander; `an` + das einzige Haben-Konto stehen auf der **letzten** Soll-Zeile:

```
6000 AWR      11.500,00 €
6001 BZKR        380,00 €
2600 VORST     2.257,20 €   an   4400 VE   14.137,20 €
```

b) **Ein Soll-Konto, mehrere Haben-Konten** – `an` + das erste Haben-Konto stehen direkt neben dem einzigen Soll-Konto; die weiteren Haben-Konten folgen darunter, bündig unter dem ersten Haben-Konto (kein wiederholtes `an`):

```
4400 VE     14.137,20 €   an   2800 BK      13.854,46 €
                                6000 AWR        237,60 €
                                2600 VORST       45,14 €
```

c) **Mehrere Konten auf beiden Seiten** (Sammelbuchungssatz) – gleiche Logik: alle Soll-Zeilen zuerst, `an` + erstes Haben-Konto auf der letzten Soll-Zeile, die übrigen Haben-Konten darunter bündig unter dem ersten Haben-Konto:

```
6200 LG      42.000,00 €   an   2800 BK    26.040,00 €
6400 AGASV    8.400,00 €        4830 VFA    7.560,00 €
                                 4840 VSV   16.800,00 €
```

Merkregel: `an` markiert immer den Übergang von der letzten Soll-Zeile zur ersten Haben-Zeile – unabhängig davon, welche Seite mehr Konten hat.

## Reihenfolge der Konten innerhalb einer Seite

Die Reihenfolge folgt dem Geschäftsfall/Beleg, nicht dem Alphabet oder der Kontonummer: zuerst das inhaltlich tragende Hauptkonto (z. B. Waren-/Aufwands-/Erlöskonto), danach Nebenkosten (z. B. Bezugskosten), zuletzt Steuerkonten (Vorsteuer/Umsatzsteuer). Diese Reihenfolge entspricht der Reihenfolge, in der die Beträge auf einer echten Rechnung erscheinen.

## Spaltenausrichtung im Codeblock

- Kontobezeichnung linksbündig, Betrag rechtsbündig – innerhalb **eines** Buchungssatz-Blocks konsistente Spaltenbreite wählen, damit Kommas und Eurozeichen optisch untereinanderstehen.
- `an` durch mindestens drei Leerzeichen von Konto/Betrag abgesetzt, nie direkt angehängt.
- Jeder Buchungssatz in einem eigenen Codeblock (nicht mehrere Geschäftsfälle in einem Block vermischen).

## Kontodarstellung

- Ab der 8. Jahrgangsstufe **immer** Kontonummer **und** Kurzbezeichnung gemeinsam (z. B. „4400 VE"), nie nur die Nummer oder nur die Bezeichnung. In der 7. Jahrgangsstufe wird teils nur die Bezeichnung ohne Nummer verlangt – für diesen Skill (8./9. Jgst.) gilt durchgängig „Nummer + Kürzel".
- Kontonummer, Kontenbezeichnung/Abkürzung und Betrag sind eine untrennbare Einheit (Korrektur-„Block", siehe Korrekturprinzipien) – nie eines davon weglassen.

## Was zu vermeiden ist

- Schrägstrich (`/`) anstelle von `an`.
- Doppelpfeil zur nachträglichen „Korrektur" eines Drehfehlers – nicht zulässig, gilt weiterhin als Drehfehler (0 P).
- Buchungssatz ohne Beträge – in der Praxis unbrauchbar, wird nur mit dem Konten-Teilpunkt bewertet, nicht mit den Betragspunkten.
- Minuszeichen bei Stornobuchungen (Rücksendung, Storno von Sofortrabatten o. Ä.): Storno wird durch **Vertauschen von Soll und Haben mit denselben, weiterhin positiven Beträgen** dargestellt, nicht durch ein Minuszeichen.
  - Ursprungsbuchung (Verkauf): `2400 FO ... an 5000 UEFE ... / 4800 UST ...`
  - Stornobuchung (Rücksendung): `5000 UEFE ... / 4800 UST ... an 2400 FO ...`

## Betragsformat (Kurzfassung, Details in `korrekturprinzipien.md`)

- Cent-Beträge stets mit zwei Nachkommastellen, auch bei „,00".
- Tausenderpunkt, Komma als Dezimaltrennzeichen: `14.137,20 €`.
- Eurozeichen **hinter** dem Betrag.
- Kaufmännisch runden (DIN 1333).

## Aussprache (für mündliche Unterrichtssituationen)

Kontonummern werden stellenweise (Ziffer für Ziffer) ausgesprochen, nicht als große Zahl: „sechs-neun-fünf-null Abschreibungen auf Forderungen", nicht „sechstausendneunhundertfünfzig ABFO". Beim Erstellen von Aufgaben mit Sprechanteil (z. B. Vorlesen eines Buchungssatzes) diese Konvention berücksichtigen.
