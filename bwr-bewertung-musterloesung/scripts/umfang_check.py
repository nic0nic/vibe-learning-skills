#!/usr/bin/env python3
"""Prüft Punktesummen einer Musterlösung (Markdown) und den Umfang gegen Richtwerte.

Erwartetes Format (siehe references/musterloesung_format.md):
  **Gesamtpunktzahl: N P**
  ## Aufgabe 1 – Titel (X P)
  1.1 Titel (Y P)      bzw.   1.1 (Y P)

Aufruf:
  umfang_check.py loesung.md [--art stegreif|kurz|schul|schul10|ap]
                  [--kategorien "1:B,2:R,3:F"]   B=BWL-Fragen, R=Rechnen, F=Buchführung
"""
import re, sys, argparse

RICHT = {  # (min, max) Punkte, Minuten
    "stegreif": (20, 22, 20),
    "kurz": (30, 32, 30),
    "schul": (42, 46, 45),
    "schul10": (42, 110, 60),
    "ap": (80, 110, 0),
}
NUM = r"(\d+(?:[.,]\d)?)"

def zahl(s):
    return float(s.replace(",", "."))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("datei")
    ap.add_argument("--art", choices=RICHT)
    ap.add_argument("--kategorien", default="")
    a = ap.parse_args()
    text = open(a.datei, encoding="utf-8").read()

    gesamt = None
    m = re.search(r"Gesamtpunktzahl:\s*" + NUM + r"\s*P", text)
    if m:
        gesamt = zahl(m.group(1))

    aufgaben = []  # [nr, titel, soll, [teile]]
    cur = None
    for line in text.splitlines():
        h = re.match(r"##\s+Aufgabe\s+(\d+)\b(.*?)\(" + NUM + r"\s*P\)\s*$", line)
        if h:
            cur = [h.group(1), h.group(2).strip(" –-"), zahl(h.group(3)), []]
            aufgaben.append(cur)
            continue
        t = re.match(r"(\d+)\.(\d+)\s.*?\(" + NUM + r"\s*P\)\s*$", line)
        if t and cur and t.group(1) == cur[0]:
            cur[3].append((t.group(1) + "." + t.group(2), zahl(t.group(3))))

    warn = []
    summe = 0.0
    print(f"{'Aufgabe':<8}{'Soll':>7}{'Summe Teile':>13}")
    for nr, titel, soll, teile in aufgaben:
        s = sum(p for _, p in teile)
        summe += soll
        flag = ""
        if teile and abs(s - soll) > 1e-9:
            flag = "  <-- Abweichung"
            warn.append(f"Aufgabe {nr}: Überschrift {soll:g} P, Teilaufgaben {s:g} P")
        if not teile:
            flag = "  (keine Teilaufgaben erkannt)"
        print(f"{nr:<8}{soll:>7g}{(f'{s:g}' if teile else '-'):>13}{flag}")
    print(f"Summe der Aufgaben: {summe:g} P")

    if gesamt is None:
        warn.append("Keine Zeile '**Gesamtpunktzahl: N P**' gefunden")
    else:
        print(f"Gesamtpunktzahl laut Datei: {gesamt:g} P")
        if abs(gesamt - summe) > 1e-9:
            warn.append(f"Gesamtpunktzahl {gesamt:g} ≠ Summe der Aufgaben {summe:g}")

    if a.art:
        lo, hi, minuten = RICHT[a.art]
        if summe < lo or summe > hi:
            warn.append(f"Umfang {summe:g} P außerhalb Richtwert {lo}–{hi} P ({a.art})")
        else:
            print(f"Umfang im Richtwert {lo}–{hi} P ({a.art})")
        if minuten:
            print(f"Veranschlagte Zeit ≈ {summe:g} min bei Richtwert {minuten} min (1 P ≈ 1 min)")

    if a.kategorien:
        kat = dict(x.split(":") for x in a.kategorien.split(","))
        namen = {"B": "BWL-Fragen", "R": "Rechnen", "F": "Buchführung"}
        verteilung = {"B": 0.0, "R": 0.0, "F": 0.0}
        for nr, _, soll, _ in aufgaben:
            k = kat.get(nr)
            if k in verteilung:
                verteilung[k] += soll
            else:
                warn.append(f"Aufgabe {nr}: keine Kategorie angegeben")
        for k, v in verteilung.items():
            anteil = 100 * v / summe if summe else 0
            print(f"{namen[k]:<12}{v:>6g} P  {anteil:5.1f} %")
            if abs(anteil - 100 / 3) > 12:
                warn.append(f"{namen[k]}: {anteil:.0f} % – weit von einem Drittel entfernt")

    print()
    if warn:
        for w in warn:
            print("WARNUNG:", w)
        sys.exit(1)
    print("OK")

if __name__ == "__main__":
    main()
