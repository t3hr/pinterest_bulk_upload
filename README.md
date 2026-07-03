# Pinterest Bulk-Upload (CSV)

Nutzt Pinterests offizielles Bulk-Upload-Tool (bis zu 200 Pins pro Durchlauf,
siehe [Pinterest-Hilfe](https://help.pinterest.com/de/business/article/bulk-upload-video-pins))
statt Browser-Automatisierung. Kein Selenium, keine Selektoren, keine
Login-Blockaden — nur eine CSV-Datei, die du manuell im Pinterest-Interface
hochlädst.

## Wie es funktioniert

Pinterest lädt die Bilder über öffentliche URLs, die in der CSV stehen —
Pinterest selbst hostet beim Bulk-Upload nichts. Dieses Repo dient als
Bild-Hosting: Bilder werden in `images/` committet und gepusht, wodurch sie
unter einer öffentlichen `raw.githubusercontent.com`-URL erreichbar sind.
Sobald Pinterest den Pin daraus erstellt hat, kopiert Pinterest das Bild auf
eigene Server — die Quelle (dieses Repo) muss danach nicht mehr erreichbar
bleiben.

## Ablauf

1. **Bilder ablegen:** Originaldateien in `images/` kopieren.

2. **Bilder pushen** (macht die URLs öffentlich erreichbar):

   ```bash
   git add images/
   git commit -m "Add images for Pinterest bulk upload"
   git push
   ```

3. **`content.json` anlegen** (Format siehe `content.example.json`): pro
   Bilddateiname `title`, `description`, `hashtags`, optional `board` und
   `link` (falls abweichend von den Standardwerten in
   `generate_bulk_csv.py`).

4. **CSV generieren** (keine Python-Abhängigkeiten nötig):

   ```bash
   python3 generate_bulk_csv.py
   ```

   Erzeugt `pinterest_bulk_upload.csv`.

5. **Bei Pinterest hochladen:**
   - Anmelden → Pfeil oben rechts → **Einstellungen** → **Inhalte
     importieren**
   - Bei der CSV/TXT-Option auf **Hochladen** klicken
   - `pinterest_bulk_upload.csv` auswählen/reinziehen

6. **Nach ein paar Tagen prüfen**, ob alle Pins erfolgreich erstellt wurden
   (Board-Ansicht in Pinterest), bevor du die Bilder aus `images/` wieder
   entfernst.

## Voraussetzungen (Pinterest-seitig)

- Pinterest-**Unternehmenskonto**
- Desktop-Browser (Bulk-Upload ist nicht mobil verfügbar)

## CSV-Format

| Spalte | Inhalt |
|---|---|
| Title | Max. 100 Zeichen |
| Media URL | Öffentliche raw-GitHub-URL zum Bild |
| Pinterest board | Board-Name (Standard aus `DEFAULT_BOARD` in `generate_bulk_csv.py`) |
| Description | Beschreibung + angehängte Hashtags, max. 500 Zeichen |
| Link | Zielwebsite (Standard aus `DEFAULT_LINK`) |
| Keywords | Hashtags ohne "#", komma-separiert |

## Dateien

- `images/` – hier liegen die zu veröffentlichenden Bilder (git-getrackt,
  nicht ignoriert).
- `content.json` – Titel/Beschreibung/Hashtags pro Bilddateiname (lokal,
  nicht committet).
- `content.example.json` – Beispielformat.
- `generate_bulk_csv.py` – erzeugt die Bulk-Upload-CSV.
