"""Inhalt der QR-Speisekarte (Deutsch / Türkisch / Englisch).

Preise = Ladenpreise der Bildschirmkarten im Laden (Stand 16.10.2026).
Preis ändern: hier ändern und `python3 assets-src/build.py` ausführen → index.html ist neu.

Helva-Preise: Liegt das Projekt der Helva-Bildschirmkarte daneben (../../helva-menuekarte), werden die Preise
von dort übernommen, damit Bildschirm und QR-Karte nie auseinanderlaufen. Sonst gilt HELVA_PREISE unten.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# Klein / Groß, jeweils mit Eis und ohne Eis (ohne Eis klein = mit Eis klein + 1,00 €)
HELVA_PREISE = {
    "original": dict(mit=("5,00", "7,50"), ohne=("6,00", "9,00")),
    "pistazie": dict(mit=("6,90", "9,50"), ohne=("7,90", "12,00")),
    "lotus": dict(mit=("5,50", "8,00"), ohne=("6,50", "9,50")),
    "weisse-schokolade": dict(mit=("5,50", "8,00"), ohne=("6,50", "9,50")),
    "schokolade": dict(mit=("5,50", "8,00"), ohne=("6,50", "9,50")),
    "mix": dict(mit=("6,00", "9,00"), ohne=("7,00", "10,50")),
}
_board = os.path.join(HERE, "..", "..", "helva-menuekarte", "assets-src")
if os.path.exists(os.path.join(_board, "build_menu.py")):
    sys.path.insert(0, _board)
    import build_menu as _helva  # noqa: E402
    _von_karte = {m["key"]: dict(mit=tuple(m["mit"]), ohne=tuple(m["ohne"])) for m in _helva.MENU}
    if _von_karte != HELVA_PREISE:
        print("Hinweis: Helva-Preise von der Bildschirmkarte übernommen (weichen von HELVA_PREISE ab):",
              {k: v for k, v in _von_karte.items() if HELVA_PREISE.get(k) != v})
    HELVA_PREISE = _von_karte


def L(de, tr, en):
    return {"de": de, "tr": tr, "en": en}


UI = {
    "title": L("Speisekarte", "Menü", "Menu"),
    "slogan_sub": L("Ein jahrhundertealter Geschmack", "", "A century-old taste"),
    "cue": L("Zur Karte", "Menüye git", "View menu"),
    "what": L("Was ist das?", "Bu nedir?", "What's this?"),
    "close": L("Schließen", "Kapat", "Close"),
    "good": L("Gut zu wissen", "Bilmekte fayda var", "Good to know"),
    "mit": L("mit Eis", "dondurmalı", "with ice cream"),
    "ohne": L("ohne Eis", "dondurmasız", "no ice cream"),
    "klein": L("Klein", "Küçük", "Small"),
    "gross": L("Groß", "Büyük", "Large"),
    "allergens": L("Allergene", "Alerjenler", "Allergens"),
    "tap_flavor": L("Sorte antippen", "Çeşide dokunun", "Tap a flavour"),
    "vat": L("Alle Preise in Euro inkl. MwSt.", "Tüm fiyatlar Euro cinsinden, KDV dahildir.",
             "All prices in euros incl. VAT."),
    "allergy_note": L("Fragen zu Allergenen? Wir helfen dir gern an der Theke.",
                      "Alerjenlerle ilgili sorularınız için ekibimize danışabilirsiniz.",
                      "Questions about allergens? Just ask us at the counter."),
    "follow": L("Folgt uns", "Bizi takip edin", "Follow us"),
    "place": L("Skyline Plaza · Frankfurt am Main", "Skyline Plaza · Frankfurt am Main",
               "Skyline Plaza · Frankfurt am Main"),
}

ALLERGENS = {
    "A": L("glutenhaltiges Getreide", "glütenli tahıl", "cereals containing gluten"),
    "C": L("Eier", "yumurta", "eggs"),
    "G": L("Milch / Laktose", "süt / laktoz", "milk / lactose"),
    "H": L("Schalenfrüchte (Nüsse)", "sert kabuklu yemişler", "tree nuts"),
}

FLAV = {
    "blaubeere": L("Blaubeere", "Yaban mersini", "Blueberry"),
    "mango": L("Mango", "Mango", "Mango"),
    "erdbeere": L("Erdbeere", "Çilek", "Strawberry"),
    "ananas": L("Ananas", "Ananas", "Pineapple"),
    "kokos": L("Kokosnuss", "Hindistan cevizi", "Coconut"),
    "vanille": L("Vanille", "Vanilya", "Vanilla"),
    "karamell": L("Karamell", "Karamel", "Caramel"),
    "haselnuss": L("Haselnuss", "Fındık", "Hazelnut"),
}

# ---------------------------------------------------------------- Helva (Preise aus build_menu.MENU)
H = HELVA_PREISE
HELVA_TXT = {
    "original": dict(
        name=L("Original", "Sade", "Original"),
        sub=L("der Klassiker", "klasik lezzet", "the classic"),
        info=L("Pur und klassisch: Grieß, in Butter goldbraun geröstet – so, wie Helva sein soll.",
               "Saf ve klasik: tereyağında altın rengine kadar kavrulmuş irmik – helva dediğin böyle olur.",
               "Pure and classic: semolina roasted golden in butter – helva the way it should be."),
        media={"video": "helva-original"}),
    "pistazie": dict(
        name=L("Pistazie", "Fıstıklı", "Pistachio"),
        sub=L("mit Pistazie", "fıstık ile", "with pistachio"),
        info=L("Mit fein gemahlener Pistazie: nussig im Geschmack und leuchtend grün.",
               "İnce çekilmiş fıstıkla: kuruyemiş aromalı ve yemyeşil.",
               "With finely ground pistachio: nutty in flavour and vividly green."),
        media={"video": "helva-pistazie"}),
    "lotus": dict(
        name=L("Lotus", "Lotus", "Lotus"),
        sub=L("mit Karamellkeks", "karamelize bisküvi ile", "with caramel biscuit"),
        info=L("Mit Bröseln vom Lotus-Karamellkeks – karamellig, mit einer feinen Zimtnote.",
               "Lotus bisküvi kırıntılarıyla – karamelli, hafif tarçın aromalı.",
               "Topped with Lotus caramel biscuit crumbs – caramelly with a hint of cinnamon."),
        media={"img": "helva-lotus"}),
    "weisse-schokolade": dict(
        name=L("Weiße Schokolade", "Beyaz Çikolatalı", "White chocolate"),
        sub=L("cremig und mild", "kremamsı ve hafif", "creamy and mild"),
        info=L("Mit weißer Schokolade verfeinert – besonders cremig und mild.",
               "Beyaz çikolatayla zenginleştirilmiş – yumuşacık ve kremamsı.",
               "Refined with white chocolate – especially creamy and mild."),
        media={"video": "helva-weisse-schokolade"}),
    "schokolade": dict(
        name=L("Schokolade", "Çikolatalı", "Chocolate"),
        sub=L("dunkel und intensiv", "koyu ve yoğun", "dark and rich"),
        info=L("Mit Schokolade – dunkel, intensiv und herrlich zum kalten Maraş-Eis.",
               "Çikolatayla – koyu, yoğun ve soğuk Maraş dondurmasıyla harika.",
               "With chocolate – dark, rich and wonderful with cold Maraş ice cream."),
        media={"video": "helva-schokolade"}),
    "mix": dict(
        name=L("Mix", "Karışık", "Mix"),
        sub=L("Original & Pistazie", "Sade & Fıstıklı", "Original & pistachio"),
        info=L("Halb Original, halb Pistazie – für alle, die sich nicht entscheiden wollen.",
               "Yarısı sade, yarısı fıstıklı – seçemeyenler için.",
               "Half original, half pistachio – for the undecided."),
        media={"img": "helva-mix"}),
}
HELVA_ITEMS = [dict(id=f"helva-{k}", img=f"helva-{k}", kind="helva",
                    helva={"mit": list(H[k]["mit"]), "ohne": list(H[k]["ohne"])}, **HELVA_TXT[k])
               for k in ["original", "pistazie", "lotus", "weisse-schokolade", "schokolade", "mix"]]

HELVA_GOOD = [
    dict(id="was-ist-helva",
         name=L("Was ist Helva?", "İrmik helvası nedir?", "What is helva?"),
         info=L("Grieß wird langsam in Butter goldbraun geröstet und dann mit Zuckersirup oder Milch gegart. "
                "Heraus kommt eine warme, lockere Süßspeise – in der Türkei ein Klassiker zu jedem Anlass.",
                "İrmik tereyağında ağır ağır kavrulur, ardından şerbet ya da sütle pişirilir. "
                "Ortaya sıcacık, tane tane bir tatlı çıkar – her güzel günün klasiği.",
                "Semolina is slowly roasted golden in butter, then simmered with syrup or milk. "
                "The result is a warm, fluffy dessert – a Turkish classic for every occasion."),
         media={"video": "helva-original"}),
    dict(id="was-ist-maras",
         name=L("Was ist Maraş-Eis?", "Maraş dondurması nedir?", "What is Maraş ice cream?"),
         info=L("Traditionelles Eis aus Kahramanmaraş. Salep (Orchideenmehl) und Mastix machen es dicht und "
                "elastisch, deshalb schmilzt es langsamer. Zur warmen Helva ein herrlicher Kontrast aus heiß und kalt.",
                "Kahramanmaraş'ın geleneksel dondurması. Salep ve damla sakızı ona yoğun, uzayan dokusunu verir; "
                "bu yüzden daha yavaş erir. Sıcak helvayla muhteşem bir sıcak-soğuk uyumu.",
                "Traditional ice cream from Kahramanmaraş. Salep (orchid flour) and mastic make it dense and "
                "stretchy, so it melts more slowly – a lovely hot-and-cold contrast with warm helva."),
         media={"video": "helva-schokolade"}),
]

# ---------------------------------------------------------------- Desserts
DESSERTS = [
    dict(id="katmer", img="katmer", kind="single", price="9,00",
         name=L("Katmer", "Katmer", "Katmer"),
         sub=L("hauchdünner Teig mit warmer Pistazienfüllung", "ince hamur, sıcak fıstık dolgulu",
               "paper-thin pastry with warm pistachio filling"),
         info=L("Eine Spezialität aus Gaziantep: Der Teig wird hauchdünn ausgezogen, mit Pistazie gefüllt, "
                "gefaltet und kurz gebacken. Warm serviert – außen knusprig, innen saftig.",
                "Gaziantep'in meşhur tatlısı: incecik açılan hamur fıstıkla doldurulur, katlanır ve kısa sürede "
                "pişirilir. Sıcak servis edilir – dışı çıtır, içi yumuşacık.",
                "A speciality from Gaziantep: dough stretched paper-thin, filled with pistachio, folded and "
                "briefly baked. Served warm – crisp outside, soft inside."),
         media={"img": "katmer"}),
    dict(id="kuenefe", img="kuenefe", kind="single", price="8,00",
         name=L("Künefe", "Künefe", "Künefe"),
         sub=L("Engelshaar-Teig mit warmem Käse", "tel kadayıf ve sıcak peynir", "shredded pastry with warm cheese"),
         info=L("Feine Teigfäden (Kadayıf) mit mildem Käse, goldbraun gebacken und mit Sirup getränkt. "
                "Beim ersten Bissen zieht der Käse lange Fäden.",
                "İnce tel kadayıf ve peynir, altın renginde pişirilip şerbetlenir. İlk lokmada peynir uzar.",
                "Fine pastry threads (kadayıf) with mild cheese, baked golden and soaked in syrup. "
                "The cheese stretches with the first bite."),
         media={"img": "kuenefe"}),
    dict(id="havuc", img="havuc", kind="single", price="7,00",
         name=L("Havuç Dilimi", "Havuç Dilimi", "Havuç Dilimi"),
         sub=L("Pistazien-Dreieck · 1 Stück", "fıstıklı dilim · 1 adet", "pistachio triangle · 1 piece"),
         info=L("„Karottenscheibe“ heißt dieses Baklava-Stück wegen seiner Form: viele hauchdünne Teigschichten, "
                "reichlich Pistazie und Sirup.",
                "Şekli havuç dilimine benzediği için bu adı alır: kat kat ince hamur, bol fıstık ve şerbet.",
                "Named “carrot slice” for its shape: many paper-thin pastry layers, plenty of pistachio and syrup."),
         media={"img": "havuc"}),
    dict(id="baklava", img="baklava-pistazie", kind="variants",
         name=L("Baklava", "Baklava", "Baklava"),
         sub=L("je 3 Stück", "3'er adet", "3 pieces each"),
         variants=[[L("Pistazien-Baklava", "Fıstıklı baklava", "Pistachio baklava"), "6,00"],
                   [L("Pistazienrolle", "Fıstık sarma", "Pistachio roll"), "6,50"],
                   [L("Walnuss-Baklava", "Cevizli baklava", "Walnut baklava"), "5,50"]],
         info=L("Dünne Yufka-Teigblätter, Schicht für Schicht mit Nüssen gefüllt und mit Sirup getränkt. "
                "Bei der Pistazienrolle wird der Teig um die Pistazien gewickelt.",
                "İncecik yufkalar kat kat dizilir, bol iç ile doldurulur ve şerbetlenir. "
                "Sarmada yufka fıstığın etrafına sarılır.",
                "Thin sheets of yufka pastry, layered with nuts and soaked in syrup. "
                "For the pistachio roll, the pastry is wrapped around the pistachios."),
         media={"img": "baklava-pistazie"}),
]
DESSERT_NOTES = [
    dict(kind="addon", label=L("Auf Wunsch", "İsteğe bağlı", "On request"),
         name=L("Extra Eis – eine Kugel Maraş-Eis zu jedem Dessert",
                "Ekstra dondurma – her tatlıya bir top Maraş dondurması",
                "Extra ice cream – a scoop of Maraş ice cream with any dessert"),
         price="+ 2,00"),
    dict(kind="takeaway", label=L("Baklava zum Mitnehmen · pro Kilo", "Paket baklava · kilogram",
                                  "Baklava to go · per kilo"),
         rows=[[L("Walnuss", "Cevizli", "Walnut"), "30,00"],
               [L("Pistazie klassisch", "Fıstıklı (klasik)", "Pistachio (classic)"), "35,00"],
               [L("Pistazienrolle", "Fıstık sarma", "Pistachio roll"), "40,00"]]),
]

# ---------------------------------------------------------------- Herzhaft
HERZHAFT = [
    dict(id="goezleme", img="goezleme", kind="variants",
         name=L("Gözleme", "Gözleme", "Gözleme"),
         sub=L("türkisches Fladenbrot, gefüllt", "sacda pişen dolgulu ince hamur", "Turkish filled flatbread"),
         variants=[[L("Spinat & Weißkäse", "Ispanaklı & beyaz peynirli", "Spinach & white cheese"), "6,00"],
                   [L("Weißkäse", "Beyaz peynirli", "White cheese"), "6,00"],
                   [L("Kartoffel", "Patatesli", "Potato"), "6,00"],
                   [L("Hackfleisch", "Kıymalı", "Minced meat"), "6,50"]],
         info=L("Hauchdünn ausgerollter Teig wird gefüllt, zusammengeklappt und auf der heißen Platte knusprig gebacken.",
                "İncecik açılan hamur, iç harçla doldurulup katlanır ve sacda çıtır çıtır pişirilir.",
                "Thinly rolled dough is filled, folded and baked crisp on a hot griddle."),
         media={"img": "goezleme"}),
    dict(id="goezleme-teller", kind="row", price="10,90", tag=L("Menü", "Menü", "Set"),
         name=L("Gözleme-Teller", "Gözleme Tabağı", "Gözleme platter"),
         sub=L("mit Oliven, Tomaten, Käse, Gurken und Tee", "zeytin, domates, peynir, salatalık ve çay ile",
               "with olives, tomatoes, cheese, cucumber and tea")),
    dict(id="boerek", img="boerek", kind="sizes", sizes=[[L("1 Stück", "1 adet", "1 piece"), "3,90"]],
         name=L("Börek", "Börek", "Börek"),
         sub=L("aus hauchdünnem Yufka-Teig", "incecik yufkadan", "made from paper-thin yufka pastry"),
         info=L("Viele Lagen hauchdünner Yufka-Teig, gefüllt und im Ofen goldbraun gebacken.",
                "Kat kat incecik yufka, iç harçla doldurulup fırında altın renginde pişirilir.",
                "Many layers of paper-thin yufka pastry, filled and baked golden in the oven."),
         media={"img": "boerek"}),
    dict(id="boerek-teller", kind="row", price="7,90",
         name=L("Börek-Teller", "Börek Tabağı", "Börek platter")),
]
SANDWICH_HEAD = dict(name=L("Sandwiches", "Sandviçler", "Sandwiches"),
                     cols=[L("einzeln", "tek", "single"), L("im Menü", "menü", "as a set")])
SANDWICHES = [
    dict(id="sandwich-sucuk", img="sandwich-sucuk", kind="duo", prices=["6,90", "8,90"],
         name=L("Sucuk & Käse", "Sucuklu & Kaşarlı", "Sucuk & cheese"),
         sub=L("würzige türkische Knoblauchwurst", "baharatlı, sarımsaklı Türk sucuğu", "spicy Turkish garlic sausage"),
         info=L("Sucuk ist eine kräftig gewürzte türkische Wurst mit Knoblauch und Paprika – warm im Brot, "
                "mit geschmolzenem Käse.",
                "Sarımsaklı, baharatlı Türk sucuğu – ekmek arasında, eriyen peynirle sıcacık.",
                "Sucuk is a boldly spiced Turkish sausage with garlic and paprika – served warm in bread "
                "with melted cheese."),
         media={"img": "sandwich-sucuk"}),
    dict(id="sandwich-haehnchen", img="sandwich-haehnchen", kind="duo", prices=["6,90", "8,90"],
         name=L("Hähnchen", "Tavuklu", "Chicken"),
         sub=L("mit Hähnchen und Salat", "tavuk ve yeşillik ile", "with chicken and salad")),
    dict(id="sandwich-veggie", img="sandwich-veggie", kind="duo", prices=["4,90", "6,90"],
         tag=L("vegetarisch", "vejetaryen", "vegetarian"),
         name=L("Vegetarisch", "Vejetaryen", "Veggie"),
         sub=L("mit frischem Gemüse", "taze sebzelerle", "with fresh vegetables")),
]


# ---------------------------------------------------------------- Warme Getränke (Gruppen)
def row(id, name, price=None, sizes=None, info=None, img=None, tag=None, sub=None):
    d = dict(id=id, kind="row", name=name)
    if price:
        d["price"] = price
    if sizes:
        d["sizes"] = sizes
    if info:
        d["info"] = info
        d["media"] = {"img": img} if img else None
    if tag:
        d["tag"] = tag
    if sub:
        d["sub"] = sub
    return d


M = L("M", "M", "M")
LL = L("L", "L", "L")
HEISS = [
    dict(name=L("Türkischer Kaffee", "Türk Kahvesi", "Turkish coffee"), img="mokka", rows=[
        row("tuerkischer-mokka", L("Türkischer Mokka", "Türk Kahvesi", "Turkish coffee"), "3,90",
            info=L("Sehr fein gemahlener Kaffee, im Kännchen (Cezve) aufgekocht und ungefiltert mit feinem Schaum "
                   "serviert. Den Satz am Boden lässt man einfach stehen.",
                   "İncecik çekilmiş kahve cezvede pişirilir, telvesiyle ve bol köpüklü servis edilir.",
                   "Very finely ground coffee, brewed in a small pot (cezve) and served unfiltered with a fine foam. "
                   "Simply leave the grounds at the bottom."), img="mokka"),
        row("osmanischer-mokka", L("Osmanischer Mokka", "Osmanlı Kahvesi", "Ottoman coffee"), "3,90",
            info=L("Türkischer Kaffee nach osmanischer Art – mild und aromatisch, mit einer feinen Gewürznote.",
                   "Osmanlı usulü kahve – yumuşak içimli, hafif baharat aromalı.",
                   "Ottoman-style Turkish coffee – mild and aromatic with a gentle hint of spice.")),
        row("dibek", L("Dibek Kaffee", "Dibek Kahvesi", "Dibek coffee"), "3,90",
            info=L("Traditionell im Steinmörser (Dibek) gemahlen – milder und cremiger als klassischer türkischer Kaffee.",
                   "Geleneksel olarak taş dibekte dövülür – klasik Türk kahvesinden daha yumuşak ve kremamsı.",
                   "Traditionally ground in a stone mortar (dibek) – milder and creamier than classic Turkish coffee.")),
        row("menengic", L("Menengiç Kaffee", "Menengiç Kahvesi", "Menengiç coffee"), "3,90",
            tag=L("koffeinfrei", "kafeinsiz", "caffeine-free"),
            info=L("Eigentlich kein Kaffee: geröstete Menengiç-Früchte (wilde Pistazie) – nussig, koffeinfrei "
                   "und meist mit Milch zubereitet.",
                   "Aslında kahve değil: kavrulmuş menengiç (yabani fıstık) – kuruyemiş aromalı, kafeinsiz, "
                   "genelde sütle hazırlanır.",
                   "Not really coffee: roasted menengiç (wild pistachio) – nutty, caffeine-free and usually "
                   "made with milk.")),
    ]),
    dict(name=L("Tee", "Çay", "Tea"), img="cay", rows=[
        row("cay", L("Çay", "Çay", "Turkish tea"), sizes=[[L("klein", "küçük", "small"), "2,00"],
                                                         [L("groß", "büyük", "large"), "2,50"]],
            info=L("Türkischer Schwarztee – kräftig, klar und ohne Milch getrunken.",
                   "Demli Türk çayı – sade ve tavşan kanı.",
                   "Turkish black tea – strong and clear, drunk without milk."), img="cay"),
        row("minztee", L("Frischer Minztee", "Taze Nane Çayı", "Fresh mint tea"), "4,90",
            info=L("Frische Minzblätter, heiß aufgegossen.", "Taze nane yaprakları sıcak suyla demlenir.",
                   "Fresh mint leaves steeped in hot water.")),
        row("kraeutertee", L("Kräutertee", "Bitki Çayı", "Herbal tea"), "3,50"),
    ]),
    dict(name=L("Spezialitäten", "Özel İçecekler", "Specialities"), img="salep", rows=[
        row("salep", L("Salep", "Salep", "Salep"), "3,90",
            info=L("Heißes, cremiges Milchgetränk mit Salep (Orchideenmehl), mit Zimt bestäubt – ein türkischer "
                   "Winterklassiker.",
                   "Salep tozuyla yapılan sıcak, kremamsı süt içeceği; üzeri tarçınlı – kışların vazgeçilmezi.",
                   "Hot, creamy milk drink thickened with salep (orchid flour), dusted with cinnamon – a Turkish "
                   "winter classic."), img="salep"),
        row("matcha-latte", L("Matcha Latte", "Matcha Latte", "Matcha latte"), "5,00",
            info=L("Fein gemahlener japanischer Grüntee, mit Milch aufgeschäumt – sanft und leicht herb.",
                   "İnce öğütülmüş Japon yeşil çayı, köpüklü sütle – yumuşak ve hafif buruk.",
                   "Finely ground Japanese green tea with frothed milk – smooth and slightly grassy."),
            img="matcha-latte"),
        row("heisse-schokolade", L("Heiße Schokolade", "Sıcak Çikolata", "Hot chocolate"), "4,50"),
    ]),
    dict(name=L("Kaffee", "Kahve", "Coffee"), img="cafe-creme", rows=[
        row("cafe-creme", L("Café Creme", "Café Crème", "Café crème"), sizes=[[M, "3,20"]],
            info=L("Langer, milder Kaffee mit feiner Crema.", "Uzun ve yumuşak içimli, ince kremalı kahve.",
                   "Long, mild coffee with a fine crema."), img="cafe-creme"),
        row("americano", L("Americano", "Americano", "Americano"), sizes=[[M, "3,20"]],
            info=L("Espresso, mit heißem Wasser verlängert.", "Sıcak suyla uzatılmış espresso.",
                   "Espresso topped up with hot water.")),
        row("milchkaffee", L("Milchkaffee", "Sütlü Kahve", "Café au lait"), sizes=[[LL, "3,90"]]),
    ]),
    dict(name=L("Mit Milchschaum", "Süt Köpüklü", "With milk foam"), img="cappuccino", rows=[
        row("cappuccino", L("Cappuccino", "Cappuccino", "Cappuccino"), sizes=[[M, "3,90"], [LL, "4,70"]]),
        row("latte-macchiato", L("Latte Macchiato", "Latte Macchiato", "Latte macchiato"), "4,70",
            info=L("Heiße Milch, Milchschaum und ein Espresso – im hohen Glas in drei Schichten.",
                   "Sıcak süt, süt köpüğü ve espresso – uzun bardakta üç katman.",
                   "Hot milk, milk foam and a shot of espresso – three layers in a tall glass."),
            img="latte-macchiato"),
        row("flat-white", L("Flat White", "Flat White", "Flat white"), "4,50",
            info=L("Doppelter Espresso mit samtigem, feinem Milchschaum – kräftiger als ein Cappuccino.",
                   "Duble espresso ve ipeksi süt köpüğü – kapuçinodan daha yoğun.",
                   "Double espresso with velvety micro-foam – stronger than a cappuccino.")),
    ]),
    dict(name=L("Espresso", "Espresso", "Espresso"), img="espresso", rows=[
        row("espresso", L("Espresso", "Espresso", "Espresso"), "2,50"),
        row("doppio", L("Doppio", "Doppio", "Doppio"), "3,50",
            info=L("Doppelter Espresso.", "Duble espresso.", "Double espresso.")),
        row("espresso-macchiato", L("Espresso Macchiato", "Espresso Macchiato", "Espresso macchiato"), "2,90",
            info=L("Espresso mit einem Häubchen Milchschaum.", "Üzerine biraz süt köpüğü eklenmiş espresso.",
                   "Espresso with a dollop of milk foam.")),
        row("cortado", L("Cortado", "Cortado", "Cortado"), "3,60",
            info=L("Espresso mit etwa gleich viel warmer Milch – kräftig, aber weich.",
                   "Espresso ve yaklaşık aynı miktarda sıcak süt – sert ama yumuşak.",
                   "Espresso cut with about the same amount of warm milk – strong yet smooth.")),
    ]),
]

# ---------------------------------------------------------------- Kalte Getränke
KALT = [
    dict(name=L("Erfrischungen", "Ferahlatıcılar", "Refreshments"), items=[
        dict(id="limonade", img="limonade", kind="single", price="4,50",
             name=L("Frische Limonade", "Taze Limonata", "Fresh lemonade"),
             sub=L("mit Zitrone und Minze", "limon ve nane ile", "with lemon and mint")),
        dict(id="frucht-limonade", img="limonade-blaubeere", kind="single", price="5,50",
             name=L("Frucht-Limonade", "Meyveli Limonata", "Fruit lemonade"),
             flavors=[["blaubeere", "limonade-blaubeere"], ["mango", "limonade-mango"],
                      ["erdbeere", "limonade-erdbeere"], ["ananas", "limonade-ananas"]]),
        dict(id="wasser", kind="row", price="2,50", name=L("Wasser", "Su", "Water")),
        dict(id="softdrinks", kind="row", price="3,00", name=L("Softdrinks", "Gazlı İçecekler", "Soft drinks")),
    ]),
    dict(name=L("Kalter Kaffee", "Soğuk Kahve", "Iced coffee"), items=[
        dict(id="ice-latte", img="ice-latte", kind="single", price="5,00",
             name=L("Ice Latte", "Ice Latte", "Iced latte"),
             sub=L("Espresso, kalte Milch, Eis", "espresso, soğuk süt, buz", "espresso, cold milk, ice")),
        dict(id="ice-latte-sirup", img="ice-latte-vanille", kind="single", price="5,50",
             name=L("Ice Latte mit Sirup", "Şuruplu Ice Latte", "Iced latte with syrup"),
             flavors=[["vanille", "ice-latte-vanille"], ["karamell", "ice-latte-karamell"],
                      ["haselnuss", "ice-latte-haselnuss"]]),
        dict(id="ice-americano", img="ice-americano", kind="single", price="4,00",
             name=L("Ice Americano", "Ice Americano", "Iced americano"),
             sub=L("Espresso und Wasser auf Eis", "buzlu espresso ve su", "espresso and water over ice")),
        dict(id="ice-spanish-latte", img="ice-latte-spanish", kind="single", price="6,50",
             name=L("Ice Spanish Latte", "Ice Spanish Latte", "Iced Spanish latte"),
             sub=L("mit gesüßter Kondensmilch", "şekerli yoğunlaştırılmış süt ile", "with sweetened condensed milk"),
             info=L("Espresso mit gesüßter Kondensmilch und kalter Milch auf Eis – süß und cremig.",
                    "Espresso, şekerli yoğunlaştırılmış süt ve soğuk süt, buzla – tatlı ve kremamsı.",
                    "Espresso with sweetened condensed milk and cold milk over ice – sweet and creamy."),
             media={"img": "ice-latte-spanish"}),
    ]),
    dict(name=L("Matcha", "Matcha", "Matcha"), items=[
        dict(id="ice-matcha", img="matcha", kind="single", price="5,50",
             name=L("Ice Matcha Latte", "Ice Matcha Latte", "Iced matcha latte"),
             sub=L("frisch aufgeschlagen", "taze çırpılmış", "freshly whisked"),
             info=L("Fein gemahlener japanischer Grüntee, frisch aufgeschlagen, mit kalter Milch auf Eis – "
                    "sanft, leicht herb und mit natürlichem Koffein.",
                    "İnce öğütülmüş Japon yeşil çayı taze çırpılır, soğuk süt ve buzla buluşur – yumuşak, "
                    "hafif buruk ve doğal kafeinli.",
                    "Finely ground Japanese green tea, freshly whisked, with cold milk over ice – smooth, "
                    "slightly grassy and naturally caffeinated."),
             media={"img": "matcha"}),
        dict(id="ice-matcha-frucht", img="matcha-erdbeere", kind="single", price="6,50",
             name=L("Ice Matcha mit Frucht", "Meyveli Ice Matcha", "Iced matcha with fruit"),
             flavors=[["erdbeere", "matcha-erdbeere"], ["mango", "matcha-mango"],
                      ["blaubeere", "matcha-blaubeere"], ["kokos", "matcha-kokos"]],
             info=L("Erst die Frucht, dann Milch und Eis, obendrauf frisch aufgeschlagener Matcha. "
                    "Vor dem Trinken umrühren!",
                    "Önce meyve, sonra süt ve buz, en üstte taze çırpılmış matcha. İçmeden önce karıştırın!",
                    "Fruit first, then milk and ice, topped with freshly whisked matcha. Stir before you sip!"),
             media={"video": "matcha-frucht"}),
        dict(id="ice-spanish-matcha", img="matcha-spanish", kind="single", price="6,90",
             name=L("Ice Spanish Matcha Latte", "Ice Spanish Matcha Latte", "Iced Spanish matcha latte"),
             sub=L("mit gesüßter Kondensmilch", "şekerli yoğunlaştırılmış süt ile", "with sweetened condensed milk"),
             info=L("Matcha mit gesüßter Kondensmilch und kalter Milch auf Eis – süß, cremig und grün.",
                    "Matcha, şekerli yoğunlaştırılmış süt ve soğuk süt, buzla – tatlı, kremamsı ve yeşil.",
                    "Matcha with sweetened condensed milk and cold milk over ice – sweet, creamy and green."),
             media={"img": "matcha-spanish"}),
    ]),
]
MILK = dict(label=L("Milch nach Wahl", "Süt seçimi", "Choice of milk"),
            sub=L("für Kaffee & Matcha", "kahve ve matcha için", "for coffee & matcha"),
            opts=[L("Kuhmilch", "İnek sütü", "Cow's milk"), L("Laktosefrei", "Laktozsuz", "Lactose-free"),
                  L("Hafermilch", "Yulaf sütü", "Oat milk"), L("Kokosmilch", "Hindistan cevizi sütü", "Coconut milk")])

CATS = [
    dict(id="helva", chip=L("Helva", "Helva", "Helva"),
         kicker=L("Unsere Spezialität", "Spesiyalitemiz", "Our signature"),
         title=L("Buttergrießhelva", "İrmik Helvası", "Semolina helva"),
         intro=L("Warm und buttrig – pur oder serviert auf türkischem Maraş-Eis.",
                 "Sıcacık ve tereyağlı – sade ya da Maraş dondurmasıyla.",
                 "Warm and buttery – on its own or served on Turkish Maraş ice cream."),
         good=HELVA_GOOD, items=HELVA_ITEMS),
    dict(id="desserts", chip=L("Desserts", "Tatlılar", "Desserts"),
         kicker=L("Süße Klassiker", "Klasik tatlılar", "Sweet classics"),
         title=L("Türkische Desserts", "Tatlılar", "Turkish desserts"),
         items=DESSERTS, notes=DESSERT_NOTES, allergens="A, G, H"),
    dict(id="herzhaft", chip=L("Herzhaft", "Tuzlular", "Savoury"),
         kicker=L("Herzhaft", "Tuzlu lezzetler", "Savoury"),
         title=L("Türkische Spezialitäten", "Hamur İşleri", "Turkish specialities"),
         items=HERZHAFT, sandwich_head=SANDWICH_HEAD, sandwiches=SANDWICHES, allergens="A, C, G, H"),
    dict(id="heiss", chip=L("Heiße Getränke", "Sıcak İçecekler", "Hot drinks"),
         kicker=L("Frisch aufgebrüht", "Taze demlenmiş", "Freshly brewed"),
         title=L("Warme Getränke", "Sıcak İçecekler", "Hot drinks"),
         groups=HEISS),
    dict(id="kalt", chip=L("Kalte Getränke", "Soğuk İçecekler", "Cold drinks"),
         kicker=L("Eiskalt", "Buz gibi", "Ice cold"),
         title=L("Kalte Getränke", "Soğuk İçecekler", "Cold drinks"),
         cgroups=KALT, milk=MILK),
]

DATA = dict(ui=UI, allergens=ALLERGENS, flavors=FLAV, cats=CATS)
