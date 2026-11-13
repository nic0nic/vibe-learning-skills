#!/usr/bin/env python3
"""Prüft ein Aufgaben-JSON für vibe learning mit denselben Regeln wie pb_public/lib/seite.js (Seite.pruefe).

Aufruf:  python3 scripts/pruefe.py aufgaben.json      (oder JSON über stdin: … | python3 scripts/pruefe.py -)
Ausgabe: „OK: …“ bzw. eine Fehlerliste; Rückgabewert 0 = in Ordnung, 1 = Fehler.
Bei Änderungen an seite.js (TYPEN, Prüfregeln) dieses Skript angleichen.
"""
import json, re, sys

TYPEN = {
    "mc": ["options", "correct"], "zahlen": ["felder"], "luecken": ["text"], "zuordnen": ["felder", "karten"],
    "freitext": ["felder", "antworten"], "chat": ["nachrichten"], "buchungssatz": ["konten", "soll", "haben"], "kombi": ["teile"],
    "tabelle": ["spalten", "zeilen"], "wahrheit": ["spalten", "zeilen"],
}
MAX = 150000
VERBOTEN = re.compile(r"<\s*script|\bon[a-z]+\s*=|javascript:|<\s*iframe|<\s*object|<\s*embed", re.I)
# Erlaubtliste für HTML in Texten (wie ERLAUBT/TAG in seite.js)
ERLAUBT = {"p", "br", "b", "strong", "i", "em", "u", "s", "sub", "sup", "small", "mark", "span", "div", "hr",
           "ul", "ol", "li", "h2", "h3", "h4", "table", "thead", "tbody", "tr", "th", "td", "code", "pre", "blockquote"}
TAG = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)((?:\s+[a-z]+="[a-z0-9 _-]*")*)\s*(/?)>')


def html_fehler(s):
    f = []
    i = s.find("<")
    while i >= 0:
        n = s[i + 1:i + 2]
        if n and re.match(r"[a-zA-Z/!?]", n):
            m = TAG.match(s, i)
            name = m.group(2).lower() if m else None
            if not m or name not in ERLAUBT:
                f.append(f"nicht erlaubtes HTML: {s[i:i + 40]}")
            else:
                attrs = re.findall(r"[a-z]+(?==)", m.group(3))
                ok = all(a == "class" or (name in ("td", "th") and a in ("colspan", "rowspan")) for a in attrs)
                if not ok or (m.group(1) and attrs):
                    f.append(f"nicht erlaubtes Attribut: {m.group(0)[:60]}")
                if re.search(r'span="[^"]*[^0-9"]', m.group(3)):
                    f.append(f"colspan/rowspan nur als Zahl: {m.group(0)[:60]}")
        i = s.find("<", i + 1)
    return f


def alle_texte(x, wo, f):
    if isinstance(x, str):
        f.extend(f"{wo}: {e}" for e in html_fehler(x))
    elif isinstance(x, list):
        for y in x:
            alle_texte(y, wo, f)
    elif isinstance(x, dict):
        for y in x.values():
            alle_texte(y, wo, f)


def text(v):
    return isinstance(v, str) and v.strip() != ""


def zahl(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def aufgabe(a, wo, f):
    if not isinstance(a, dict):
        return f.append(f"{wo}: keine Aufgabe (Objekt erwartet)")
    typ = a.get("typ")
    if typ not in TYPEN:
        return f.append(f"{wo}: unbekannter Aufgabentyp „{typ}“ (möglich: {', '.join(TYPEN)})")
    for k in TYPEN[typ]:
        if a.get(k) is None:
            f.append(f"{wo} ({typ}): Feld „{k}“ fehlt")
    if typ == "mc" and isinstance(a.get("options"), list) and isinstance(a.get("correct"), list):
        n = len(a["options"])
        if n < 2:
            f.append(f"{wo}: mindestens zwei Antworten nötig")
        if not a["correct"]:
            f.append(f"{wo}: „correct“ ist leer")
        for i in a["correct"]:
            if not (isinstance(i, int) and 0 <= i < n):
                f.append(f"{wo}: „correct“ enthält {i}, es gibt aber nur die Antworten 0 bis {n - 1}")
    if typ == "zahlen" and isinstance(a.get("felder"), list):
        for i, x in enumerate(a["felder"]):
            if not (isinstance(x, dict) and text(x.get("t")) and zahl(x.get("l"))):
                f.append(f"{wo}, Feld {i + 1}: braucht „t“ (Text) und „l“ (Lösung als Zahl)")
    if typ == "luecken" and isinstance(a.get("text"), str):
        l = re.findall(r"\[\[(.*?)\]\]", a["text"])
        if not l:
            f.append(f"{wo}: keine Lücke [[richtig|falsch]] im Text")
        for x in l:
            if not a.get("ziehen") and len(x.split("|")) < 2:
                f.append(f"{wo}: Lücke [[{x}]] braucht mindestens zwei Antworten, die richtige zuerst")
            if not x.split("|")[0].strip():
                f.append(f"{wo}: Lücke [[{x}]] ohne richtiges Wort")
        if a.get("extra") is not None and not (isinstance(a["extra"], list) and all(text(w) for w in a["extra"])):
            f.append(f"{wo}: „extra“ muss eine Liste von Wörtern sein")
    if typ == "zuordnen" and isinstance(a.get("felder"), list) and isinstance(a.get("karten"), list):
        ids = [x[0] if isinstance(x, list) and x else None for x in a["felder"]]
        if len(ids) < 2:
            f.append(f"{wo}: mindestens zwei Felder nötig")
        for i, k in enumerate(a["karten"]):
            if not (isinstance(k, dict) and text(k.get("t"))):
                f.append(f"{wo}, Karte {i + 1}: Die Karte hat noch keinen Text („t“).")
            elif k.get("z") not in ids:
                f.append(f"{wo}, Karte „{k['t']}“: Die Karte gehört zu keinem Feld („z“ muss eine der Feld-Kennungen sein: {', '.join(map(str, ids))}).")
    if typ == "freitext" and isinstance(a.get("felder"), list) and isinstance(a.get("antworten"), list):
        if len(a["antworten"]) < len(a["felder"]):
            f.append(f"{wo}: weniger mögliche Antworten ({len(a['antworten'])}) als Felder ({len(a['felder'])})")
    if typ == "chat" and isinstance(a.get("nachrichten"), list):
        for i, m in enumerate(a["nachrichten"]):
            if isinstance(m, str):
                continue
            if not (isinstance(m, dict) and text(m.get("bot"))):
                f.append(f"{wo}, Nachricht {i + 1}: Text oder {{\"bot\": …}} erwartet")
                continue
            if m.get("antworten") is not None and not any(isinstance(x, dict) and x.get("ok") for x in m["antworten"]):
                f.append(f"{wo}, Nachricht {i + 1}: keine Antwort mit \"ok\": true")
            if m.get("zahl") is not None and not zahl((m["zahl"] or {}).get("l")):
                f.append(f"{wo}, Nachricht {i + 1}: „zahl“ braucht „l“ (Lösung als Zahl)")
    if typ == "buchungssatz" and all(isinstance(a.get(k), list) for k in ("soll", "haben", "konten")):
        summe = lambda l: round(sum(x[1] for x in l if isinstance(x, list) and len(x) > 1 and zahl(x[1])), 2)
        for x in a["soll"] + a["haben"]:
            if not (isinstance(x, list) and len(x) > 1 and x[0] in a["konten"] and zahl(x[1])):
                f.append(f"{wo}: Buchungszeile {json.dumps(x, ensure_ascii=False)} – Konto muss in „konten“ stehen, Betrag als Zahl")
        if summe(a["soll"]) != summe(a["haben"]):
            f.append(f"{wo}: Soll ({summe(a['soll'])}) und Haben ({summe(a['haben'])}) sind nicht gleich groß")
        if a.get("jgst") is not None and a.get("jgst") != 7:
            f.append(f"{wo}: „jgst“ nur als 7 (7. Jahrgangsstufe), sonst weglassen")
        if a.get("jgst") == 7:
            for k in a["konten"]:
                if any(ch.isdigit() for ch in str(k)):
                    f.append(f"{wo}: In Jgst. 7 Konten nur mit Kürzel, ohne Nummer: „{k}“")
        if "betraege" in a:
            if not isinstance(a["betraege"], list):
                f.append(f"{wo}: Die Beträge zum Ziehen müssen eine Liste sein ([[\"Rechnungsbetrag\", 11900], …]).")
            else:
                for i, x in enumerate(a["betraege"]):
                    if not (isinstance(x, list) and len(x) > 1 and zahl(x[1])):
                        f.append(f"{wo}, Betrag zum Ziehen {i + 1}: Der Betrag fehlt oder ist keine Zahl.")
                    elif not (isinstance(x[0], str) and x[0].strip()):
                        f.append(f"{wo}, Betrag zum Ziehen {i + 1} ({str(x[1]).replace('.', ',')} €): Die Bezeichnung fehlt, z. B. „Rechnungsbetrag“.")
    if typ == "tabelle" and isinstance(a.get("spalten"), list) and isinstance(a.get("zeilen"), list):
        felder = 0
        for i, r in enumerate(a["zeilen"]):
            if not isinstance(r, list) or len(r) != len(a["spalten"]):
                f.append(f"{wo}, Zeile {i + 1}: braucht genau {len(a['spalten'])} Zellen (wie „spalten“)")
                continue
            for j, c in enumerate(r):
                if isinstance(c, dict):
                    if not zahl(c.get("l")):
                        f.append(f"{wo}, Zeile {i + 1}, Spalte {j + 1}: Eingabefeld braucht „l“ (Lösung als Zahl)")
                    else:
                        felder += 1
        if not felder:
            f.append(f"{wo}: keine Eingabefelder ({{\"l\": Lösung}}) in der Tabelle")
    if typ == "wahrheit" and isinstance(a.get("spalten"), list) and isinstance(a.get("zeilen"), list):
        felder = 0
        for i, r in enumerate(a["zeilen"]):
            if not isinstance(r, list) or len(r) != len(a["spalten"]):
                f.append(f"{wo}, Zeile {i + 1}: braucht genau {len(a['spalten'])} Zellen (wie „spalten“)")
                continue
            for j, c in enumerate(r):
                if isinstance(c, dict):
                    if not isinstance(c.get("l"), bool):
                        f.append(f"{wo}, Zeile {i + 1}, Spalte {j + 1}: Feld braucht „l“ (true oder false)")
                    else:
                        felder += 1
        if not felder:
            f.append(f"{wo}: keine Felder zum Anklicken ({{\"l\": true/false}}) in der Tabelle")
        w = a.get("werte")
        if w is not None and not (isinstance(w, list) and len(w) == 2 and all(isinstance(x, str) and x.strip() for x in w)):
            f.append(f"{wo}: „werte“ braucht genau zwei Wörter, z. B. [\"ja\", \"nein\"]")
    if typ == "kombi" and isinstance(a.get("teile"), list):
        if len(a["teile"]) < 2:
            f.append(f"{wo}: Eine kombinierte Aufgabe braucht mindestens zwei Teile")
        for i, t in enumerate(a["teile"]):
            if isinstance(t, dict) and t.get("typ") == "kombi":
                f.append(f"{wo}, Teil {i + 1}: keine kombinierte Aufgabe in einer kombinierten Aufgabe")
            else:
                aufgabe(t, f"{wo}, Teil {i + 1}", f)
    if a.get("danach"):
        f.append(f"{wo}: „danach“ ist veraltet – stattdessen {{\"typ\": \"kombi\", \"teile\": [Aufgabe, Folgeaufgabe]}}")


def pruefe(j):
    if not isinstance(j, dict):
        return ["Das ist kein Aufgaben-JSON (Objekt mit „titel“ und „schritte“ erwartet)."]
    f = []
    roh = json.dumps(j, ensure_ascii=False)
    if len(roh) > MAX:
        f.append(f"Zu groß ({len(roh) // 1000} kB, höchstens {MAX // 1000} kB).")
    if VERBOTEN.search(roh):
        f.append("Eigenes JavaScript (script, onclick=, javascript:, iframe …) ist nicht erlaubt.")
    if not text(j.get("titel")):
        f.append("„titel“ fehlt.")
    for k, wo in (("titel", "Titel"), ("kurztext", "Kurztext")):
        if j.get(k) is not None:
            alle_texte(j[k], wo, f)
    schritte = j.get("schritte") if isinstance(j.get("schritte"), list) else ([{"aufgaben": j["aufgaben"]}] if isinstance(j.get("aufgaben"), list) else [])
    if not schritte:
        f.append("Keine Schritte bzw. Aufgaben gefunden („schritte“ oder „aufgaben“).")
    if len(schritte) > 40:
        f.append("Höchstens 40 Schritte.")
    for i, s in enumerate(schritte):
        wo = f"Schritt {i + 1}"
        if not isinstance(s, dict):
            f.append(f"{wo}: Objekt erwartet")
            continue
        if not s.get("html") and not s.get("aufgaben"):
            f.append(f"{wo}: weder Erklärung („html“) noch Aufgaben")
        if s.get("aufgaben") is not None and not isinstance(s["aufgaben"], list):
            f.append(f"{wo}: „aufgaben“ muss eine Liste sein")
            continue
        for k, a in enumerate(s.get("aufgaben") or []):
            aufgabe(a, f"{wo}, Aufgabe {k + 1}", f)
        alle_texte(s, wo, f)
    return f


def main():
    quelle = sys.argv[1] if len(sys.argv) > 1 else "-"
    roh = sys.stdin.read() if quelle == "-" else open(quelle, encoding="utf-8").read()
    try:
        j = json.loads(roh)
    except json.JSONDecodeError as e:
        print(f"Kein gültiges JSON: {e.msg} (Zeile {e.lineno}, Spalte {e.colno})")
        return 1
    f = pruefe(j)
    if f:
        print("Bitte korrigieren:\n- " + "\n- ".join(f))
        return 1
    schritte = j.get("schritte") or [{"aufgaben": j.get("aufgaben", [])}]
    print(f"OK: {len(schritte)} Schritte, {sum(len(s.get('aufgaben') or []) for s in schritte)} Aufgaben.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
