/* Bildschirmkarten im Fernseher-Browser: Video ohne Ton in Dauerschleife.
   Das Video wird einmal ganz geladen und dann aus dem Arbeitsspeicher abgespielt – so ruckelt nichts, wenn das
   WLAN schwankt, auch nicht beim Neustart der Schleife. OK oder Klick schaltet auf Vollbild. Hinweise erscheinen
   nur kurz und verschwinden von selbst. Hängt das Bild, stößt die Seite es in Stufen wieder an, ohne den
   Vollbildmodus zu verlassen. Neue Videofassungen aus karten.json werden im Hintergrund geladen und am
   Schleifenanfang übernommen.
   Bewusst ES5: ältere Fernseher-Browser kennen keine neueren Sprachmittel. */
(function () {
  "use strict";

  var video = document.getElementById("karte");
  if (!video) {
    // Übersicht: erste Karte auswählen, damit die Fernbedienung sofort mit OK starten kann
    var erste = document.querySelector(".karte");
    if (erste) erste.focus();
    return;
  }

  var hinweis = document.getElementById("hinweis");
  var name = video.getAttribute("data-karte");
  var wurzel = document.documentElement;
  var URLS = window.URL || window.webkitURL;
  var vollbildAn = wurzel.requestFullscreen || wurzel.webkitRequestFullscreen ||
    wurzel.webkitRequestFullScreen || wurzel.mozRequestFullScreen || wurzel.msRequestFullscreen;

  function istVollbild() {
    return !!(document.fullscreenElement || document.webkitFullscreenElement ||
      document.webkitIsFullScreen || document.mozFullScreenElement || document.msFullscreenElement);
  }

  function absolut(adresse) {
    var a = document.createElement("a");
    a.href = adresse;
    return a.href;
  }

  // ---------- Hinweis: immer nur kurz, nie dauerhaft über der Karte ----------
  var hinweisUhr = null;
  var hinweisArt = "";
  function verstecke() {
    clearTimeout(hinweisUhr);
    hinweisArt = "";
    if (hinweis) hinweis.className = "hinweis";
  }
  function zeige(text, ms, art) {
    if (!hinweis) return;
    hinweis.textContent = text;
    hinweis.className = "hinweis an";
    hinweisArt = art || "";
    clearTimeout(hinweisUhr);
    hinweisUhr = setTimeout(verstecke, ms);
  }

  // ---------- Abspielen ----------
  function abspielen() {
    video.muted = true;
    var versprochen;
    try { versprochen = video.play(); } catch (e) { return; }
    if (versprochen && typeof versprochen.then === "function") {
      versprochen.then(function () {
        if (hinweisArt === "start") verstecke();
      }, function (fehler) {
        // Nur wenn der Browser das Abspielen ohne Tastendruck verbietet. Ein „unterbrochen“ (AbortError) beim
        // Neuladen ist harmlos – früher blieb dann „OK drücken: Start“ für immer stehen.
        if (fehler && fehler.name === "NotAllowedError") zeige("OK drücken: Start", 8000, "start");
      });
    }
  }
  video.addEventListener("playing", function () {
    if (hinweisArt === "start") verstecke();
  });

  function vollbild() {
    if (!vollbildAn || istVollbild()) return;
    try {
      var versprochen = vollbildAn.call(wurzel);
      if (versprochen && typeof versprochen.then === "function") versprochen.then(null, function () {});
    } catch (e) { /* Browser ohne Vollbild per Seite: dann über sein Menü */ }
  }

  function bedienen() {
    verstecke();
    abspielen();
    vollbild();
  }

  // Bedienung: OK/Enter oder Leertaste auf der Fernbedienung, Klick mit Zeiger oder Maus
  document.addEventListener("keydown", function (e) {
    var taste = e.keyCode || e.which;
    if (taste === 13 || taste === 32) bedienen();
  });
  document.addEventListener("click", bedienen);
  ["fullscreenchange", "webkitfullscreenchange", "mozfullscreenchange", "MSFullscreenChange"].forEach(function (ereignis) {
    document.addEventListener(ereignis, function () {
      if (istVollbild()) verstecke();
    });
  });

  // Mauszeiger (z. B. LG Magic Remote) nach drei Sekunden Ruhe ausblenden
  var mausUhr = null;
  function mausBewegt() {
    document.body.classList.remove("still");
    clearTimeout(mausUhr);
    mausUhr = setTimeout(function () { document.body.classList.add("still"); }, 3000);
  }
  document.addEventListener("mousemove", mausBewegt);
  mausBewegt();

  // ---------- Quelle: ganze Datei in den Arbeitsspeicher, sonst direkt aus dem Netz ----------
  var quelle = absolut(video.getAttribute("data-src") || video.getAttribute("src") || "");  // Fassung, die läuft
  var ziel = "";           // Fassung, die gerade im Hintergrund geladen wird
  var wartend = "";        // Adresse, die am nächsten Schleifenanfang übernommen wird
  var vorige = 0;

  function aktuelleQuelle() {
    return video.currentSrc || video.src || "";
  }

  function setzeQuelle(adresse) {
    var alt = aktuelleQuelle();
    video.src = adresse;
    try { video.load(); } catch (e) { /* manche alte Browser */ }
    abspielen();
    if (alt && alt !== adresse && alt.indexOf("blob:") === 0 && URLS && URLS.revokeObjectURL) {
      setTimeout(function () {
        try { URLS.revokeObjectURL(alt); } catch (e) { /* schon frei */ }
      }, 10000);
    }
  }

  function ladeInSpeicher(adresse, fertig) {
    if (!URLS || !URLS.createObjectURL || !window.XMLHttpRequest) { fertig(null); return; }
    var anfrage = new XMLHttpRequest();
    var gemeldet = false;
    function melde(ergebnis) {
      if (gemeldet) return;
      gemeldet = true;
      fertig(ergebnis);
    }
    try {
      anfrage.open("GET", adresse, true);
      anfrage.responseType = "blob";
      anfrage.timeout = 240000;
    } catch (e) { melde(null); return; }
    anfrage.onload = function () {
      var inhalt = anfrage.response;
      if (anfrage.status === 200 && inhalt && inhalt.size > 100000) {
        try { melde(URLS.createObjectURL(inhalt)); } catch (e) { melde(null); }
      } else {
        melde(null);
      }
    };
    anfrage.onerror = function () { melde(null); };
    anfrage.ontimeout = function () { melde(null); };
    anfrage.onabort = function () { melde(null); };
    try { anfrage.send(); } catch (e) { melde(null); }
  }

  // Läuft schon ein Video, wird die neue Adresse erst am Schleifenanfang übernommen (dort ist das Bild gleich)
  function uebernehmen(adresse) {
    if (!aktuelleQuelle() || video.paused || video.readyState < 2) {
      wartend = "";
      setzeQuelle(adresse);
    } else {
      wartend = adresse;
    }
  }
  video.addEventListener("timeupdate", function () {
    var t = video.currentTime;
    if (wartend && t + 0.5 < vorige) {
      var neu = wartend;
      wartend = "";
      setzeQuelle(neu);
    }
    vorige = t;
  });

  function holen(adresse) {
    ziel = adresse;
    // Dauert das Laden länger, schon einmal aus dem Netz zeigen; die Speicherfassung folgt am Schleifenanfang
    var notUhr = setTimeout(function () {
      if (!aktuelleQuelle()) { quelle = adresse; setzeQuelle(adresse); }
    }, 20000);
    ladeInSpeicher(adresse, function (speicher) {
      clearTimeout(notUhr);
      if (ziel !== adresse) {             // inzwischen wird eine neuere Fassung geladen
        if (speicher && URLS.revokeObjectURL) URLS.revokeObjectURL(speicher);
        return;
      }
      ziel = "";
      var jetzt = aktuelleQuelle();
      if (speicher) {
        quelle = adresse;
        uebernehmen(speicher);
      } else if (!jetzt || jetzt.indexOf("blob:") !== 0) {
        // Laden in den Speicher klappt nicht: direkt aus dem Netz (läuft schon diese Fassung, nichts tun)
        if (jetzt !== adresse) uebernehmen(adresse);
        quelle = adresse;
      }
      // sonst läuft die alte Fassung aus dem Speicher weiter; die nächste Prüfung versucht es erneut
    });
  }

  // Falls ein Browser das loop-Attribut nicht beachtet
  video.addEventListener("ended", function () {
    try { video.currentTime = 0; } catch (e) { /* noch nicht suchbar */ }
    abspielen();
  });
  // Datei kaputt oder Netz weg: aus dem Netz neu versuchen
  var fehlerUhr = null;
  video.addEventListener("error", function () {
    clearTimeout(fehlerUhr);
    fehlerUhr = setTimeout(function () { setzeQuelle(quelle); }, 8000);
  });

  // ---------- Wächter: hängt das Bild, in Stufen wieder anstoßen ----------
  // 6 s: kurz weiterspringen · 14 s: Quelle neu laden · 40 s: Datei neu holen · 120 s: Seite neu laden
  var letzteZeit = -1, steht = 0, stufe = 0;
  function anstossen() {
    try {
      var dauer = video.duration;
      if (dauer && isFinite(dauer)) video.currentTime = (video.currentTime + 0.1) % dauer;
    } catch (e) { /* noch nicht suchbar */ }
    abspielen();
  }
  setInterval(function () {
    if (document.hidden || !aktuelleQuelle()) return;
    var zeit = video.currentTime;
    if (video.paused && !video.ended) abspielen();
    if (!video.paused && zeit === letzteZeit) {
      steht += 2;
    } else {
      steht = 0;
      if (zeit !== letzteZeit) stufe = 0;
    }
    letzteZeit = zeit;
    if (wartend && steht >= 4) {          // steht das Bild, die wartende Fassung sofort übernehmen
      var neu = wartend;
      wartend = "";
      steht = 0;
      setzeQuelle(neu);
      return;
    }
    if (steht >= 6 && stufe === 0) { stufe = 1; anstossen(); }
    else if (steht >= 14 && stufe === 1) { stufe = 2; setzeQuelle(aktuelleQuelle()); }
    else if (steht >= 40 && stufe === 2) { stufe = 3; holen(quelle); }
    else if (steht >= 120 && stufe === 3) { location.reload(); }
  }, 2000);

  // Alle sechs Stunden am Schleifenanfang frisch starten (Fernseher-Browser laufen sonst tagelang am Stück)
  setInterval(function () {
    var jetzt = aktuelleQuelle();
    if (jetzt && !wartend) wartend = jetzt;
  }, 6 * 60 * 60 * 1000);

  // ---------- Bildschirm wach halten (Screen Wake Lock, wo vorhanden) ----------
  var sperre = null;
  function wachHalten() {
    if (sperre || !navigator.wakeLock || !navigator.wakeLock.request) return;
    navigator.wakeLock.request("screen").then(function (s) {
      sperre = s;
      s.addEventListener("release", function () { sperre = null; });
    }, function () {});
  }
  video.addEventListener("playing", wachHalten);
  document.addEventListener("visibilitychange", function () {
    if (!document.hidden) {
      wachHalten();
      abspielen();
    }
  });

  // ---------- Neue Fassung? karten.json alle 30 Minuten prüfen ----------
  function aufNeuePruefen() {
    if (!name) return;
    var anfrage = new XMLHttpRequest();
    anfrage.open("GET", "../karten.json?t=" + new Date().getTime(), true);
    anfrage.onreadystatechange = function () {
      if (anfrage.readyState !== 4 || anfrage.status !== 200) return;
      var liste;
      try { liste = JSON.parse(anfrage.responseText); } catch (e) { return; }
      var datei = liste && liste[name];
      if (!datei) return;
      var neu = absolut("../" + datei);
      if (neu !== quelle && neu !== ziel) holen(neu);
    };
    anfrage.send();
  }
  setInterval(aufNeuePruefen, 30 * 60 * 1000);

  // ---------- Start ----------
  if (vollbildAn && !istVollbild()) zeige("OK drücken: Vollbild", 6000, "vollbild");
  if (quelle) holen(quelle);
})();
