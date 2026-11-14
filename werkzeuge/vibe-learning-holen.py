#!/usr/bin/env python3
"""Kopiert die Bausteine von vibe learning in den Skill vibe-learning-seite-erstellen (assets/vl/).

Aufruf im Ordner vibe-learning-skills:  python3 werkzeuge/vibe-learning-holen.py [Pfad zu vibe-learning]
(Standard: ../vibe-learning). Nach Änderungen an lib/, katalog.js, nav.js, sync.js oder scorm.js in vibe learning
laufen lassen und committen, sonst baut der Skill mit dem alten Stand.

assets/vl/ hat dieselben Ordner wie pb_public/: Eine Seite für pb_public/<Fach>/<Bereich>/ findet ihre Bausteine
über dieselben relativen Pfade (../../lib/aufgaben.js), scripts/baue.js bettet sie daraus ein.
Prüft außerdem, ob DESIGNS in scripts/pruefe.py zu lib/designs.js passt.
"""
import json, pathlib, re, shutil, subprocess, sys

SKILL = pathlib.Path(__file__).resolve().parent.parent / "vibe-learning-seite-erstellen"
ZIEL = SKILL / "assets" / "vl"
DATEIEN = ["katalog.js", "nav.js", "sync.js", "scorm.js", "seite.css", "BWR/bwr.css",
           "lib/aufgaben.js", "lib/aufgaben.css", "lib/basis.css", "lib/designs.js", "lib/formel.js",
           "lib/seite.js", "lib/scorm-manifest.xml"]


def main():
    vl = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else SKILL.parent.parent / "vibe-learning").resolve()
    pub = vl / "pb_public"
    if not (pub / "lib" / "seite.js").is_file():
        sys.exit(f"{pub}: lib/seite.js nicht gefunden")
    if ZIEL.exists():
        shutil.rmtree(ZIEL)
    for d in DATEIEN:
        (ZIEL / d).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pub / d, ZIEL / d)
    try:
        stand = subprocess.run(["git", "-C", str(vl), "log", "-1", "--format=%h %cs"], capture_output=True, text=True).stdout.strip()
    except OSError:
        stand = "?"
    (ZIEL / "STAND.txt").write_text(f"vibe learning {stand}\n", encoding="utf-8")
    print(f"{len(DATEIEN)} Dateien nach {ZIEL.relative_to(SKILL.parent)} (Stand {stand})")

    ids = subprocess.run(["node", "-e", "console.log(JSON.stringify(require(process.argv[1]).liste().map(d => d.id)))",
                          str(ZIEL / "lib" / "designs.js")], capture_output=True, text=True)
    if ids.returncode == 0:
        neu = set(json.loads(ids.stdout)) | {"standard"}
        m = re.search(r"DESIGNS = \(([^)]*)\)", (SKILL / "scripts" / "pruefe.py").read_text(encoding="utf-8"))
        alt = set(re.findall(r'"([a-z-]+)"', m.group(1))) if m else set()
        if neu != alt:
            print(f"Achtung: DESIGNS in scripts/pruefe.py anpassen (fehlt: {sorted(neu - alt)}, zu viel: {sorted(alt - neu)})")


if __name__ == "__main__":
    main()
