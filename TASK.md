# Aufgabe: Pin-Content für alle Bilder generieren

Für jedes Bild in `images/` (`.jpeg`/`.jpg`/`.png`, außer `.gitkeep`/`.DS_Store`):

1. Bild ansehen (Read-Tool) und den Inhalt analysieren.
2. Eintrag in `content.json` schreiben (Format siehe `content.example.json`),
   Schlüssel = exakter Dateiname:
   - `title`: kurz und prägnant, **3–4 Wörter**, Englisch (z.B. "Men of the North")
   - `description`: 2–4 atmosphärische englische Sätze, ohne Hashtags
   - `hashtags`: **mindestens 10** relevante Hashtags
   - `board`: `synthetic stills`
   - `link`: `https://www.instagram.com/tele__prompt_er/`
3. Leere Vorlagen-Seiten (nur dunkler Hintergrund mit Logo-Text, ohne Foto)
   überspringen.
4. Wenn ein Bild beim Lesen einen Fehler wirft: einmal erneut versuchen,
   sonst überspringen und am Ende auflisten.
5. Danach `python3 generate_bulk_csv.py` ausführen und die erzeugte
   `pinterest_bulk_upload.csv` dem Nutzer schicken (SendUserFile).

Hinweise:
- Die Bilder sind Schwarzweiß-Fotografien im Stil von ca. 1972 ("nordic soul
  1972", Marke "synthetic stills"): Island/Grönland-Motive — Fischerboote im
  Packeis, Jäger, Dorfszenen, Schafe, Berglandschaften, Hundeschlitten etc.
- Dateinamen können ein geschütztes Leerzeichen (U+00A0) enthalten; ggf. erst
  auf normale Leerzeichen umbenennen, committen und pushen (Media-URLs in der
  CSV müssen zu den Dateinamen im Repo passen!).
- `content.json` ist in `.gitignore` — nicht committen, nur lokal nutzen.
- Die CSV nutzt automatisch eindeutige `utm_content`-Parameter pro Pin
  (Pinterest lehnt identische Links als Duplikat ab).
