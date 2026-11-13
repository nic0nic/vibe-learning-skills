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
            if not (isinstance(x, list) and x and isinstance(x[0], str) and x[0].strip()):
                f.append(f"{wo}: In der Lösung fehlt bei einer Zeile das Konto.")
            elif x[0] not in a["konten"]:
                f.append(f"{wo}: Das Konto „{x[0]}“ steht in der Lösung, aber nicht in „konten“ (Auswahl für die Schüler).")
            elif not (len(x) > 1 and zahl(x[1])):
                f.append(f"{wo}: In der Lösung fehlt beim Konto „{x[0]}“ der Betrag (als Zahl).")
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
                    elif x[0] is not None and not isinstance(x[0], str):
                        f.append(f"{wo}, Betrag zum Ziehen {i + 1}: Die Bezeichnung muss ein Text sein (oder leer \"\").")
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


# ---------- Formeln der Trainings-Szenarien (wie lib/formel.js in vibe learning) ----------
import math, random, re as _re
_FUNK = {"runden": lambda x, n=0: math.floor(x * 10 ** n + 0.5 + 1e-9) / 10 ** n if x >= 0 else -math.floor(-x * 10 ** n + 0.5 + 1e-9) / 10 ** n,
         "abs": abs, "min": min, "max": max, "wurzel": math.sqrt, "ganz": math.floor, "rest": lambda a, b: a % b}
_WORT = {"und": "&&", "oder": "||", "nicht": "!"}


def _lex(s):
    t, i = [], 0
    while i < len(s):
        r = s[i:]
        m = _re.match(r"\s+", r)
        if m: i += m.end(); continue
        m = _re.match(r"\d+(\.\d+)?", r)
        if m: t.append(("zahl", float(m.group()))); i += m.end(); continue
        m = _re.match(r"[A-Za-zÄÖÜäöüß_][A-Za-z0-9ÄÖÜäöüß_]*", r)
        if m:
            w = m.group().lower(); t.append(("op", _WORT[w]) if w in _WORT else ("name", m.group())); i += m.end(); continue
        m = _re.match(r"(<=|>=|==|!=|<>|&&|\|\||[-+*/^()<>=,!·:×])", r)
        if m:
            v = {"·": "*", "×": "*", ":": "/", "<>": "!=", "=": "=="}.get(m.group(), m.group()); t.append(("op", v)); i += m.end(); continue
        raise ValueError(f"Das Zeichen „{r[0]}“ kann ich nicht rechnen")
    return t


def _parse(s):
    t, i = _lex(str(s)), [0]
    ist = lambda v: i[0] < len(t) and t[i[0]] == ("op", v)
    def binaer(nach, ops):
        def f():
            a = nach()
            while any(ist(o) for o in ops):
                o = t[i[0]][1]; i[0] += 1; a = ("o", o, a, nach())
            return a
        return f
    def einst():
        if ist("-"): i[0] += 1; return ("u", "-", einst())
        if ist("!"): i[0] += 1; return ("u", "!", einst())
        if ist("+"): i[0] += 1; return einst()
        a = atom()
        if ist("^"): i[0] += 1; return ("o", "^", a, einst())
        return a
    def atom():
        if i[0] >= len(t): raise ValueError("Der Ausdruck endet zu früh")
        art, v = t[i[0]]
        if art == "zahl": i[0] += 1; return ("z", v)
        if art == "name":
            i[0] += 1
            if ist("("):
                if v.lower() not in _FUNK: raise ValueError(f"Die Funktion „{v}“ gibt es nicht")
                i[0] += 1; args = []
                if not ist(")"):
                    while True:
                        args.append(oder())
                        if ist(","): i[0] += 1; continue
                        break
                if not ist(")"): raise ValueError(f"Bei „{v}(…)“ fehlt die schließende Klammer")
                i[0] += 1; return ("f", v.lower(), args)
            return ("n", v)
        if ist("("):
            i[0] += 1; e = oder()
            if not ist(")"): raise ValueError("Es fehlt eine schließende Klammer )")
            i[0] += 1; return e
        raise ValueError(f"„{v}“ steht hier an der falschen Stelle")
    produkt = binaer(einst, ["*", "/"]); summe = binaer(produkt, ["+", "-"])
    vergleich = binaer(summe, ["<=", ">=", "==", "!=", "<", ">"]); und = binaer(vergleich, ["&&"]); oder = binaer(und, ["||"])
    if not t: raise ValueError("Der Ausdruck ist leer")
    e = oder()
    if i[0] < len(t): raise ValueError(f"„{t[i[0]][1]}“ steht hier an der falschen Stelle" + (" – Kommazahlen mit Punkt schreiben (2.5)" if t[i[0]][1] == "," else ""))
    return e


def _namen(e, out):
    if e[0] == "n": out.add(e[1])
    elif e[0] == "o": _namen(e[2], out); _namen(e[3], out)
    elif e[0] == "u": _namen(e[2], out)
    elif e[0] == "f": [_namen(x, out) for x in e[2]]
    return out


def _rechne(e, w):
    k = e[0]
    if k == "z": return e[1]
    if k == "n": return w[e[1]]
    if k == "f": return _FUNK[e[1]](*[_rechne(x, w) for x in e[2]])
    if k == "u": a = _rechne(e[2], w); return -a if e[1] == "-" else (0 if a else 1)
    a, b = _rechne(e[2], w), _rechne(e[3], w)
    return {"+": lambda: a + b, "-": lambda: a - b, "*": lambda: a * b, "/": lambda: a / b, "^": lambda: a ** b,
            "<": lambda: a < b, "<=": lambda: a <= b, ">": lambda: a > b, ">=": lambda: a >= b, "==": lambda: abs(a - b) < 1e-9,
            "!=": lambda: abs(a - b) >= 1e-9, "&&": lambda: bool(a and b), "||": lambda: bool(a or b)}[e[1]]()


def formel_fehler(s, namen):
    try:
        fremd = sorted(_namen(_parse(s), set()) - set(namen))
        return f"„{fremd[0]}“ ist kein festgelegter Wert (festgelegt: {', '.join(namen)})" if fremd else None
    except ValueError as x:
        return str(x)


def szenario(sz, wo, f):
    if not isinstance(sz, dict):
        return f.append(f"{wo}: Szenario muss ein Objekt sein")
    vorher = len(f)
    if not text(sz.get("frage")): f.append(f"{wo}: Der Fragetext fehlt (z. B. „{{a}} + {{b}}“)")
    werte = sz.get("werte") if isinstance(sz.get("werte"), dict) else None
    if werte is None: f.append(f"{wo}: „werte“ fehlt (z. B. {{\"a\": [1, 10]}})")
    bekannt = []
    for k, v in (werte or {}).items():
        if isinstance(v, list):
            if not (2 <= len(v) <= 3 and all(zahl(x) for x in v)) or v[0] > v[1] or (len(v) == 3 and v[2] <= 0):
                f.append(f"{wo}, Wert {k}: [von, bis] oder [von, bis, Schritt] (von ≤ bis, Schritt > 0)")
        elif isinstance(v, dict):
            if not (isinstance(v.get("aus"), list) and v["aus"] and all(zahl(x) for x in v["aus"])): f.append(f"{wo}, Wert {k}: braucht {{\"aus\": [Zahlen]}}")
        elif isinstance(v, str):
            e = formel_fehler(v, bekannt)
            if e: f.append(f"{wo}, Wert {k} = {v}: {e}")
        else:
            f.append(f"{wo}, Wert {k}: [von, bis], {{\"aus\": […]}} oder Formel")
        bekannt.append(k)
    for feld, name in (("loesung", "Lösung"), ("bedingung", "Bedingung")):
        if sz.get(feld) is None:
            if feld == "loesung": f.append(f"{wo}: Die Lösung fehlt (Formel, z. B. „a + b“)")
            continue
        e = formel_fehler(str(sz[feld]), bekannt)
        if e: f.append(f"{wo}: {name} „{sz[feld]}“: {e}")
    for x in sz.get("falsch") or []:
        e = formel_fehler(str(x), bekannt)
        if e: f.append(f"{wo}: Falsche Antwort „{x}“: {e}")
    for m in _re.finditer(r"\{=([^}]+)\}|\{([^}]*)\}", str(sz.get("frage") or "")):
        if m.group(2) is not None and m.group(2) not in bekannt: f.append(f"{wo}: Im Fragetext steht {{{m.group(2)}}}, aber „{m.group(2)}“ ist kein festgelegter Wert")
    if len(f) == vorher and sz.get("bedingung"):   # Probewürfeln: ist die Bedingung erfüllbar?
        b, ok = _parse(sz["bedingung"]), False
        for _ in range(200):
            w = {}
            for k, v in werte.items():
                if isinstance(v, list): s = v[2] if len(v) == 3 else 1; w[k] = v[0] + random.randint(0, int((v[1] - v[0]) / s + 1e-9)) * s
                elif isinstance(v, dict): w[k] = random.choice(v["aus"])
                else: w[k] = _rechne(_parse(v), w)
            if _rechne(b, w): ok = True; break
        if not ok: f.append(f"{wo}: Die Bedingung ist auch nach 200 Versuchen nicht erfüllt – Wertebereiche oder Bedingung anpassen")


def training(t, wo, f):
    if not isinstance(t, dict):
        return f.append(f"{wo}: „training“ muss ein Objekt sein")
    if t.get("antwort") not in (None, "eingabe", "mc"): f.append(f"{wo}: „antwort“ ist \"eingabe\" oder \"mc\"")
    if t.get("anzahl") is not None and not (isinstance(t["anzahl"], int) and 0 < t["anzahl"] <= 500): f.append(f"{wo}: „anzahl“ = Aufgaben pro Runde (1 bis 500) – oder weglassen für endlos")
    z = t.get("zeit")
    if z is not None and not (isinstance(z, dict) and zahl(z.get("start")) and z["start"] > 0): f.append(f"{wo}: Zeit: „start“ = Sekunden für die erste Aufgabe (größer als 0)")
    stufen = t.get("stufen")
    for k, s in enumerate(stufen if isinstance(stufen, list) and stufen else [t]):
        ws = f"{wo}, Stufe {k + 1}" if stufen else wo
        if not isinstance(s, dict): f.append(f"{ws}: Objekt erwartet"); continue
        sz, wb = s.get("szenarien"), s.get("woerterbuch")
        if not sz and not wb: f.append(f"{ws}: Es fehlen „szenarien“ (Zahlen) oder „woerterbuch“ (Vokabeln)"); continue
        for i, x in enumerate(sz or []): szenario(x, f"{ws}, Szenario {i + 1}", f)
        if wb is not None:
            E = wb.get("eintraege") if isinstance(wb, dict) else None
            if not isinstance(E, list) or not E: f.append(f"{ws}: Das Wörterbuch hat keine Einträge")
            else:
                for i, e in enumerate(E):
                    if not (isinstance(e, list) and len(e) >= 2 and text(e[0]) and text(e[1])): f.append(f"{ws}, Eintrag {i + 1}: braucht zwei Seiten, z. B. [\"house\", \"Haus\"]")
                if t.get("antwort") == "mc" and len(E) < 4: f.append(f"{ws}: Für Multiple Choice mindestens 4 Einträge")
            if isinstance(wb, dict) and wb.get("richtung") not in (None, "a-b", "b-a", "beide"): f.append(f"{ws}: „richtung“ ist \"a-b\", \"b-a\" oder \"beide\"")


DESIGNS = ("standard", "kommandozeile")   # wie lib/designs.js in vibe learning


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
    if j.get("design") is not None and j.get("design") not in DESIGNS:
        f.append(f"Das Design „{j['design']}“ gibt es nicht (möglich: {', '.join(DESIGNS)}).")
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
        if not s.get("html") and not s.get("aufgaben") and not s.get("training"):
            f.append(f"{wo}: weder Erklärung („html“) noch Aufgaben")
        if s.get("training") is not None:
            training(s["training"], f"{wo}, Training", f)
            if s.get("aufgaben"):
                f.append(f"{wo}: Ein Schritt mit Training hat keine weiteren Aufgaben – lege dafür einen eigenen Schritt an")
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
