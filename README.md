# Speisekarte – Helvacı Yakub Efendi

Digitale Speisekarte für den QR-Code im Laden (Skyline Plaza Frankfurt). Fürs Handy gebaut,
auf Deutsch, Türkisch und Englisch, im Stil der Bildschirmkarten (Grün, Gold, Fraunces/Montserrat).

Online: https://oezcelik42.github.io/Speisekarte/

## Preise oder Texte ändern

1. `assets-src/menu_data.py` öffnen. Dort stehen alle Produkte, Preise und Erklärtexte (DE/TR/EN).
2. `python3 assets-src/build.py` ausführen (braucht Python 3 und Node.js). Das schreibt `index.html` neu.
3. Änderungen hochladen. GitHub Pages veröffentlicht sie nach etwa einer Minute; der QR-Code bleibt gleich.

`python3 assets-src/build.py --inline` erzeugt zusätzlich `Vorschau_Speisekarte.html`: eine einzelne Datei
mit allem drin, zum Verschicken (wird nicht hochgeladen).

## Aufbau

- `index.html` – die fertige Seite. Die deutsche Karte steht fest im HTML, deshalb ist sie auch ohne
  JavaScript lesbar (z. B. in Vorschauen von Messengern). Das Skript ergänzt Sprachwechsel,
  „Was ist das?“-Erklärungen, den Umschalter „mit Eis / ohne Eis“ und die Sorten-Fotos.
- `assets-src/render_core.js` – baut das HTML; läuft beim Bauen (Node) und im Browser (Sprachwechsel).
- `assets-src/template.html` – Gestaltung (CSS) und Bedienung (JS).
- `assets/` – Produktfotos (WebP), kurze Videos (MP4 + WebM, Standbilder), Schriften, Logo.

Allergene stehen nur dort, wo sie auch auf den Bildschirmkarten stehen (Desserts, Spezialitäten).

## Bildschirmkarten im Fernseher-Browser

Ohne Mini-PC: Der Fernseher öffnet in seinem eigenen Browser https://oezcelik42.github.io/Speisekarte/tv/
und spielt die Karte in Dauerschleife ab. OK auf der Fernbedienung schaltet auf Vollbild.

- Je Bildschirm ein Ordner: `tv/helva/` (30 s alle Sorten, 10 s Videokarte Original und Pistazie),
  `tv/desserts-spezial/` und `tv/getraenke/` (je zwei Karten im Wechsel, 10 s, mit Überblendung).
  Die Einzelkarten liegen in `tv/desserts/`, `tv/spezial/`, `tv/warm/`, `tv/kalt/`.
  Die Videos liegen in `tv/media/` (H.264, FullHD, ohne Ton, CRF 20 mit höchstens 8 Mbit/s – klein genug, dass der
  Fernseher die ganze Datei in den Speicher lädt).
- `tv/aussen/` – Außen-TV im Hochformat (1080 × 1920, ungedreht). `tv/aussen-andersrum/` war eine gedrehte
  Fassung und leitet jetzt nur noch auf `tv/aussen/` weiter.
- `tv/getraenke-neu/` – Testfassung (52 s): Übersicht warme und kalte Getränke zusammen (29 s), danach je 10 s die
  warme und die kalte Karte. Quelle: Projekt `getraenke-heiss-kalt` (HyperFrames).
- `tv/tv.js` – lädt das Video einmal ganz in den Arbeitsspeicher und spielt es von dort (kein Ruckeln, wenn das WLAN
  schwankt), stößt hängende Wiedergabe in Stufen wieder an, hält den Bildschirm wach, zeigt Hinweise nur kurz und holt
  neue Videofassungen. In den Seiten steht die Videoadresse deshalb in `data-src`, nicht in `src`.
- Neue Fassung einer Karte: Video in `tv/media/` ersetzen und die Zahl hinter `?v=` in `tv/karten.json`
  und in der Seite der Karte (`data-src`) erhöhen. Laufende Fernseher laden sie innerhalb von 30 Minuten im
  Hintergrund und übernehmen sie am Schleifenanfang. Nach einer Änderung an `tv.js` die Zahl hinter `tv.js?v=` in
  allen Seiten erhöhen und die Seiten auf den Fernsehern einmal neu öffnen.
