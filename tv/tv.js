/* Bildschirmkarten im Fernseher-Browser: Video ohne Ton in Dauerschleife.
   OK oder Klick schaltet auf Vollbild. Die Seite startet hängende Wiedergabe neu, hält den Bildschirm
   wach (wo der Browser das kann) und holt neue Videofassungen aus karten.json, ohne neu zu laden –
   so bleibt der Vollbildmodus erhalten.
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
  var vollbildAn = wurzel.requestFullscreen || wurzel.webkitRequestFullscreen ||
    wurzel.webkitRequestFullScreen || wurzel.mozRequestFullScreen || wurzel.msRequestFullscreen;

  function istVollbild() {
    return !!(document.fullscreenElement || document.webkitFullscreenElement ||
      document.webkitIsFullScreen || document.mozFullScreenElement || document.msFullscreenElement);
  }

  var hinweisUhr = null;
  function zeige(text, ms) {
    if (!hinweis) return;
    hinweis.textContent = text;
    hinweis.className = "hinweis an";
    clearTimeout(hinweisUhr);
    if (ms) hinweisUhr = setTimeout(verstecke, ms);
  }
  function verstecke() {
    if (hinweis) hinweis.className = "hinweis";
  }

  function abspielen() {
    video.muted = true;
    var versprochen;
    try { versprochen = video.play(); } catch (e) { /* alte Browser werfen statt abzulehnen */ }
    if (versprochen && typeof versprochen.then === "function") {
      versprochen.then(null, function () { zeige("OK drücken: Start"); });
    }
  }

  function vollbild() {
    if (!vollbildAn || istVollbild()) return;
    try {
      var versprochen = vollbildAn.call(wurzel);
      if (versprochen && typeof versprochen.then === "function") versprochen.then(null, function () {});
    } catch (e) { /* Browser ohne Vollbild per Seite: dann über sein Menü */ }
  }

  function bedienen() {
    abspielen();
    vollbild();
  }

  function neuLaden(quelle) {
    if (quelle) video.src = quelle;
    video.load();
    abspielen();
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
  zeige(vollbildAn ? "OK drücken: Vollbild" : "Vollbild im Menü des Browsers einschalten", 10000);

  // Mauszeiger (z. B. LG Magic Remote) nach drei Sekunden Ruhe ausblenden
  var mausUhr = null;
  function mausBewegt() {
    document.body.classList.remove("still");
    clearTimeout(mausUhr);
    mausUhr = setTimeout(function () { document.body.classList.add("still"); }, 3000);
  }
  document.addEventListener("mousemove", mausBewegt);
  mausBewegt();

  // Falls ein Browser das loop-Attribut nicht beachtet
  video.addEventListener("ended", function () {
    try { video.currentTime = 0; } catch (e) { /* noch nicht suchbar */ }
    abspielen();
  });
  // Netz weg oder Datei kaputt: nach zehn Sekunden neu versuchen
  video.addEventListener("error", function () {
    setTimeout(function () { neuLaden(); }, 10000);
  });

  // Wächter: steht das Bild 20 Sekunden lang, Video neu laden; nach drei Versuchen die ganze Seite
  var letzteZeit = -1, stillstand = 0, versuche = 0;
  setInterval(function () {
    if (document.hidden) return;
    var zeit = video.currentTime;
    if (!video.paused && zeit === letzteZeit) {
      stillstand += 5;
    } else {
      if (zeit !== letzteZeit) versuche = 0;
      stillstand = 0;
    }
    letzteZeit = zeit;
    if (video.paused && !video.ended) abspielen();
    if (stillstand >= 20) {
      stillstand = 0;
      versuche += 1;
      if (versuche >= 3) { location.reload(); return; }
      neuLaden();
    }
  }, 5000);

  // Bildschirm wach halten (Screen Wake Lock, wo vorhanden)
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

  // Neue Fassung? karten.json alle 30 Minuten prüfen und das Video austauschen, ohne die Seite neu zu laden
  function absolut(adresse) {
    var a = document.createElement("a");
    a.href = adresse;
    return a.href;
  }
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
      if (neu !== video.src) neuLaden(neu);
    };
    anfrage.send();
  }
  setInterval(aufNeuePruefen, 30 * 60 * 1000);

  abspielen();
})();
