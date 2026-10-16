/* Baut das HTML der Speisekarte aus den Daten.
 * Läuft zweimal mit demselben Code:
 *   - beim Bauen in Node (build.py) → die Karte steht fest in der HTML-Datei und ist auch ohne Skripte sichtbar
 *     (z. B. in der WhatsApp-Vorschau),
 *   - im Browser beim Sprachwechsel.
 */
(function (root) {
  "use strict";
  function HYE_CORE(DATA, env) {
    const LANGS = ["de", "tr", "en"];
    const NAMES = { de: "Deutsch", tr: "Türkçe", en: "English" };
    const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
    let lang = "de";
    let helvaMode = "mit";
    let fd = 0;
    const t = (o) => (o == null ? "" : typeof o === "string" ? o : o[lang] != null ? o[lang] : o.de);
    const U = (k) => t(DATA.ui[k]);
    const eur = (p) => esc(p) + "&nbsp;€";
    const nextFd = () => ((fd = (fd + 0.77) % 6), (-fd).toFixed(2) + "s");
    const IMG = (k) => env.A("img/" + k + ".webp");
    const img = (k, cls, alt) =>
      `<img${cls ? ` class="${cls}"` : ""} src="${IMG(k)}" data-asset="img/${k}.webp" alt="${esc(alt || "")}" loading="lazy" decoding="async" />`;
    let sandwichCols = null;

    function whatBtn() {
      return `<button class="what" type="button" data-toggle aria-expanded="false"><span class="q">+</span><span class="wl">${esc(U("what"))}</span></button>`;
    }
    function mediaHtml(media, alt) {
      if (!media) return "";
      if (media.video) {
        // Standbild als echtes Bild (sichtbar auch ohne Skript), das Video liegt darüber und startet beim Öffnen
        const pk = "video/" + media.video + ".jpg";
        return `<div class="media"><img class="vposter" src="${env.A(pk)}" data-asset="${pk}" alt="${esc(alt || "")}" loading="lazy" decoding="async" /><video muted loop playsinline preload="none" data-v="${media.video}"></video></div>`;
      }
      return `<div class="media img">${img(media.img, "", alt)}</div>`;
    }
    function explainHtml(it) {
      if (!it.info) return "";
      const m = mediaHtml(it.media, t(it.name));
      const cls = !m ? " noimg wide" : it.media.video ? " vid" : "";
      return `<div class="more"><div class="more-in"><div class="explain${cls}">${m}<div><p class="e-h">${esc(t(it.name))}</p><p>${esc(t(it.info))}</p></div></div></div></div>`;
    }
    function flavorsHtml(it) {
      if (!it.flavors) return "";
      const DOT = { blaubeere: "#4b3a8c", mango: "#f2b632", erdbeere: "#e0414f", ananas: "#f3cf45", kokos: "#f4efe4", vanille: "#f1e2bd", karamell: "#c88a3c", haselnuss: "#8a5a35" };
      const CHIPIMG = { blaubeere: 1, mango: 1, erdbeere: 1, ananas: 1 };
      return `<div class="flavors" role="group" aria-label="${esc(U("tap_flavor"))}">` +
        it.flavors.map(([k, im], i) => {
          const icon = CHIPIMG[k] ? img("chip-" + k) : `<span class="dot" style="background:${DOT[k]}"></span>`;
          return `<button type="button" class="fl${i === 0 ? " on" : ""}" data-flavor="${im || ""}">${icon}${esc(t(DATA.flavors[k]))}</button>`;
        }).join("") + `</div>`;
    }
    function picHtml(k) {
      return `<div class="pic" style="--fd:${nextFd()}"><span class="plate"></span>${img(k, "a")}<img class="b" alt="" /></div>`;
    }
    function itemHtml(it, i) {
      const d = `style="--d:${(i % 4) * 70}ms"`;
      const hasPic = !!it.img;
      const tag = it.tag ? `<span class="tag">${esc(t(it.tag))}</span>` : "";
      let price = "", below = "";
      if (it.kind === "single" || (it.kind === "row" && it.price)) price = `<div class="price">${eur(it.price)}</div>`;
      if (it.kind === "helva") {
        const p = it.helva[helvaMode];
        const h = it.helva;
        below = `<p class="nojs hl-lab">${esc(U("mit"))}</p>` +
          `<div class="pills"><div class="pill"><small>${esc(U("klein"))}</small><b class="hp" data-mit="${h.mit[0]}" data-ohne="${h.ohne[0]}">${eur(p[0])}</b></div>` +
          `<div class="pill"><small>${esc(U("gross"))}</small><b class="hp" data-mit="${h.mit[1]}" data-ohne="${h.ohne[1]}">${eur(p[1])}</b></div></div>` +
          `<p class="nojs hl-alt">${esc(U("ohne"))}: ${esc(U("klein"))} ${eur(h.ohne[0])} · ${esc(U("gross"))} ${eur(h.ohne[1])}</p>`;
      } else if (it.kind === "duo") {
        const c = sandwichCols;
        below = `<div class="pills"><div class="pill"><small>${esc(t(c[0]))}</small><b>${eur(it.prices[0])}</b></div><div class="pill"><small>${esc(t(c[1]))}</small><b>${eur(it.prices[1])}</b></div></div>`;
      } else if (it.kind === "sizes") {
        below = `<div class="pills">` + it.sizes.map(([l, p]) => `<div class="pill"><small>${esc(t(l))}</small><b>${eur(p)}</b></div>`).join("") + `</div>`;
      }
      const vars = it.variants
        ? `<ul class="vars">` + it.variants.map(([l, p]) => `<li><span>${esc(t(l))}</span><b>${eur(p)}</b></li>`).join("") + `</ul>`
        : "";
      const sub = it.sub ? `<p class="sub">${esc(t(it.sub))}</p>` : "";
      return `<article class="item rv${hasPic ? "" : " nopic"}" ${d} data-item="${it.id}">` +
        `<div class="item-main">${hasPic ? picHtml(it.img) : ""}` +
        `<div class="txt"><h3>${esc(t(it.name))}${tag}</h3>${sub}${below}${it.info ? whatBtn() : ""}</div>${price}</div>` +
        `${flavorsHtml(it)}${vars}${explainHtml(it)}</article>`;
    }
    function rowHtml(r) {
      let price = "";
      if (r.price) price = `<span class="rp">${eur(r.price)}</span>`;
      if (r.sizes) price = `<span class="rp">` + r.sizes.map(([l, p]) => `<em>${esc(t(l))}</em>${eur(p)}`).join("") + `</span>`;
      const tag = r.tag ? `<span class="tag">${esc(t(r.tag))}</span>` : "";
      const sub = r.sub ? `<span class="rs">${esc(t(r.sub))}</span>` : "";
      const q = r.info ? `<button class="qbtn" type="button" data-toggle aria-expanded="false" aria-label="${esc(U("what"))}">+</button>` : "";
      return `<li class="rowi" data-item="${r.id}"><div class="row-main"><div class="rt"><span class="rn">${esc(t(r.name))}</span>${tag}${sub}</div>${price}${q}</div>${explainHtml(r)}</li>`;
    }
    function catHead(c) {
      return `<header class="cat-h rv"><p class="kicker">${esc(t(c.kicker))}</p><h2>${esc(t(c.title))}</h2><div class="orn" aria-hidden="true"><i></i><b></b><i></i></div>${c.intro ? `<p class="intro">${esc(t(c.intro))}</p>` : ""}</header>`;
    }
    function allergHtml(c) {
      return c.allergens ? `<p class="allerg rv"><b>${esc(U("allergens"))}</b>${esc(c.allergens)}</p>` : "";
    }
    function renderCat(c) {
      let h = `<section class="cat" id="${c.id}" data-cat>` + catHead(c);
      if (c.id === "helva") {
        h += `<div class="mode rv"><div class="seg" data-mode="${helvaMode}" role="group"><button type="button" data-mode="mit" aria-pressed="${helvaMode === "mit"}">${esc(U("mit"))}</button><button type="button" data-mode="ohne" aria-pressed="${helvaMode === "ohne"}">${esc(U("ohne"))}</button></div></div>`;
        h += `<div class="goods">` + c.good.map((g, i) =>
          `<div class="good rv" style="--d:${i * 80}ms" data-item="${g.id}"><button type="button" data-toggle aria-expanded="false"><span class="q">+</span><span class="gt">${esc(t(g.name))}</span><span class="chev"></span></button>${explainHtml(g)}</div>`).join("") + `</div>`;
      }
      if (c.items) h += `<div class="list">` + c.items.map(itemHtml).join("") + `</div>`;
      if (c.sandwiches) {
        h += `<div class="sgroup-h rv"><h3>${esc(t(c.sandwich_head.name))}</h3></div><div class="list">` + c.sandwiches.map(itemHtml).join("") + `</div>`;
      }
      if (c.groups) {
        h += `<div class="list">` + c.groups.map((g, i) =>
          `<div class="group rv" style="--d:${(i % 3) * 70}ms"><div class="group-h"><div class="gpic" style="--fd:${nextFd()}">${img(g.img)}</div><h3>${esc(t(g.name))}</h3></div><ul class="rows">${g.rows.map(rowHtml).join("")}</ul></div>`).join("") + `</div>`;
      }
      if (c.cgroups) {
        h += c.cgroups.map((g) => `<div class="sgroup-h rv"><h3>${esc(t(g.name))}</h3></div><div class="list">` + g.items.map(itemHtml).join("") + `</div>`).join("");
      }
      if (c.milk) {
        h += `<div class="note block rv"><p class="nl">${esc(t(c.milk.label))}</p><p class="nt">${esc(t(c.milk.sub))}</p><div class="milk">${c.milk.opts.map((o) => `<span>${esc(t(o))}</span>`).join("")}</div></div>`;
      }
      if (c.notes) {
        for (const n of c.notes) {
          if (n.kind === "addon") h += `<div class="note rv"><div style="flex:1"><p class="nl">${esc(t(n.label))}</p><p class="nt">${esc(t(n.name))}</p></div><b>${eur(n.price)}</b></div>`;
          else h += `<div class="note block rv"><p class="nl">${esc(t(n.label))}</p><ul>${n.rows.map(([l, p]) => `<li><span>${esc(t(l))}</span><b>${eur(p)}</b></li>`).join("")}</ul></div>`;
        }
      }
      return h + allergHtml(c) + `</section>`;
    }

    function renderAll(l, mode) {
      lang = l;
      helvaMode = mode || "mit";
      fd = 0;
      const hz = DATA.cats.find((c) => c.sandwich_head);
      sandwichCols = hz ? hz.sandwich_head.cols : null;
      const ui = {};
      for (const k of Object.keys(DATA.ui)) ui[k] = U(k);
      return {
        main: DATA.cats.map(renderCat).join(""),
        // echte Links: springen auch ohne Skript zur Kategorie
        chips: DATA.cats.map((c) => `<a class="chip" href="#${c.id}" data-go="${c.id}">${esc(t(c.chip))}</a>`).join(""),
        lm:
          `<button class="lm-btn" type="button" data-lm aria-haspopup="true" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.6 3.9 5.6 3.9 9s-1.3 6.4-3.9 9c-2.6-2.6-3.9-5.6-3.9-9S9.4 5.6 12 3z"/></svg>${lang.toUpperCase()}</button>` +
          `<div class="lm-menu" role="menu">${LANGS.map((x) => `<button type="button" role="menuitem" data-lang="${x}" aria-pressed="${x === lang}">${NAMES[x]}<small>${x.toUpperCase()}</small></button>`).join("")}</div>`,
        langSwitch: LANGS.map((x) => `<button type="button" data-lang="${x}" aria-pressed="${x === lang}">${x.toUpperCase()}</button>`).join(""),
        legend: Object.entries(DATA.allergens).map(([k, v]) => `<b>${k}</b><span>${esc(t(v))}</span>`).join(""),
        ui,
        title: "Helvacı Yakub Efendi – " + U("title"),
      };
    }
    return { renderAll, U: (k) => U(k), LANGS };
  }
  if (typeof module !== "undefined" && module.exports) module.exports = HYE_CORE;
  else root.HYE_CORE = HYE_CORE;
})(this);
