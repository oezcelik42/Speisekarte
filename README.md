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
