# Generates content/qene.html
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qene.html")
def T(am, en): return f'<span lang="am">{am}</span><span lang="en">{en}</span>'
def P(am, en, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<p lang="am"{c}>{am}</p>\n<p lang="en"{c}>{en}</p>\n'
def chips(word, n):
    return '<span class="w">' + "".join(f'<span class="ch">{c}<sub>{n}</sub></span>' for c in word) + "</span>"
def row(left, right, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<div{c}><span class="ws-l">{left}</span><span class="ws-r">{right}</span></div>'
def sheet(title_am, title_en, rows):
    return f'<div class="worksheet"><p class="ws-title">{T(title_am, title_en)}</p>{"".join(rows)}</div>\n'
SUM = T("ሲደመር", "Sum")

essay = f'''<article class="prose qene-essay">
<h2 class="page-title">{T("ንቃተ ሕሊና፡ ፍልስፍናና ቅኔ", "Consciousness: Philosophy and Qene")}</h2>
<div class="ornament" aria-hidden="true"><span></span></div>
<div lang="am">
<p><strong>ንቃተ ሕሊና</strong> ማለት ሌላ ሰው ያላየውን ጥበብና ደስታ በጨለማ ውስጥ ገበብቶ ለማየት የሚያስችል የመብራት መሣርያ ነው፡፡ ፍልስፍናም ንቃተ ሕሊናን ተከትሎ የሚመነጭ የዕውቀት ባሕር ነው፡፡ ንቀቃተ ሕሊናና ፍልስፍና ራስን አድኖ ኅብረተ ሰብን ለማዳን የሚያስችሉ ውሑድ መሣርያ ሲሆኑ ቀዳሚው ግን ንቃተ ሕሊና ነው፡፡ ንቃተ ሕሊና ከሌለ ፍልስፍና ሊኖር አይችልምና፡፡ ንቃተ ሕሊና የኅብረተ ሰቡ ማኅበራዊ ኑሮን መመዘንና አስተካክሎ ለማኖር የሚያስችል መሣርያ ነው፡፡ በንቃተ ሕሊና ያልተስተካከሉ ሰዎች ወደ ሥልጣን ሲወጡ በጨለማ የሚያበራው ፍልስፍና ገና አልተመሠረተባዉምና ኅብረተ ሰቡን አስተካክሎ የሚመለከት ዓይነ ብርሃን አይኖራቸዉም፡፡ ንቃተ ሕሊና ከሌለም የማያውቁትና የማይችሉት መሆናቸዉን ራሳቸዉን አያውቁምና የሚያውቁ እየመሰላቸዉ ኅብረተ ሰቡ ወደ ትርምስ ይገባል፡፡ እንዲያውም በዚሁ ጊዜም ችግሩም ጎልቶ አይታያቸዉም፡፡ የንቃተ ሕሊናው ብርሃን የላቸዉምና የፈሰሰውን ውሃ ለማፈስ ጊዜያቸውን የሚባክኑ ናቸዉ እንጂ ለሃገር የሚበጅ ከኔ የተሻለ ሰው ይኖራልና እስቲ ይሞክረው የሚል ዓይነ ሐሊና አይኖራቸዉም፡፡ እንደዚህ ያሉ ሰዎች ሲያጋጥሙ በተናጠል ሰውን ሳይሆን አገርን ገዳዮች ናቸዉ፡፡</p>
<p><strong>ፍልስፍና፡</strong> ፍልስፍና ባጭሩ የብዙ ዓይነት የተደበቀ ተፈጥሮዊ ጥበብ መግለጫ ነው፡፡ ጠቅለል ባለ መልኩ ስናስቀምጠው ፍልስፍና ያልታሠበውን ማሠብና ማሳሰብ፡ ያልታየውን ማየትና ማሳየት፡ ያልተነገረውን መናገር የሚያስችል መሣርያ ነው፡፡ ለምሳሌ፡ ፈጠራ፡ ግኝትና የመሳሰሉት ፍልስፍና ናቸዉ፡፡ በዓለማችን ፍላስፋ ተብሎ የሚነገርለት ሰው፡ ያልተነገረና ያልተሰማ ሐሣቡን በጽሑፍ ወይም በቃል አብራርቶ መግለጽ የቻለ ነው፡፡ እንደ ዚሁም የተደበቀ ያልተከሰተ ተፈጥሮን በአጭርም ሆነ በረጅም ኂደት ፈልጎና አመሥጥሮ ማግኘት ነው፡፡ የማይታየውን በዓይን አሳይቶ እንዲደሰት፡ እንዲነቃቃና እንዲያስብ ማድረግ ነው፡፡ ያልተሰማውን ምሥጢር በጆሮ አሰምቶ አስደስቶና አነቃቅቶ እንዲያስብ ማድረግ ነው፡፡ በሌላ ወገን ለዕለታዊ ኑሮ አገልግሎት የሚውሉ ፈጠራዎችንም ማስገኘትና ኅብረተ ሰቡ እንዲገለገልበት ለማድረግ መቻል ነው፡፡ ይሁን እንጂ አንዳንድ ጊዜ ፍልስፍና ከሚባሉ በከፊል ክስተቱ ውሱን ሆኖ እናገኘውአለን፡፡ አንድ ጊዜ ፍላስፋው አጉልቶ ካሳየውና ካሰማው በኋላ ብዙ ዕድገትን አያመለክትም፡፡ ጉልት ሆኖ ነው የሚኖረው፡፡ ለምሳሌ፡ ከታወቁት ግኝቶች በከፊል፡ መሬት ትዞራለች፡ ፕላኔቶች ባላቸው የተፈጥሮ ስበትና ግፊት እናዳይጋጩ እንዳይበታተኑ ባላቸዉ የተፈጥሮ ስበት ሥርዓታቸዉን ወይም ኦርቢታቸዉን ጠብቀዉ ሲጓዙ ይኖራሉ፡፡ ቀዝቃዛና ደረቅ አየር ሲጋጭ መብረቅ ይፈጥራል የሚሉና የመሳሰሉት የፍልስፍና ዓይነቶች አንድ ጊዜ ከተከሰቱ በሁዋላ በአንድ ሕግ ተወስነውና ተጎልተዉ የሚኖሩ ናቸዉ፡፡ ኢትዮጵያዊ ፍልስፍና ቅኔ ግን ዘለዓለም የማያልቅ በየቀኑ አዲስ ፈጠራ እየፈጠረ እየፈለሰፈ እየሰፋ እየተመጠጠ የሚኖር ነው፡፡ የቅኔን ስፋትና መጠን የለካና የወሰነ ኖሮ አያውቅም፡፡ ቅኔ የሚታሰብ እንጂ የማይታይ የማይዳሰስ ረቂቅ ፍልስፍና ነው፡፡ ግን አእምሮን ከጉድፍ እያጸዳ ጨለማውን አስወግዶ ብርሃንን የሚያላብስ ፍልስፍና ነው፡፡ ቅኔን የሚያውቅ ሰው የፈለገ ሀብታም፡ ምሁር፡ ባለ ሥልጣን አጠገቡ ቢኖር እንደ ምንም አይቆጥረውም፡፡ ሠርቶ መብላትን አምላካዊ ትዕዛዝና የማኅበራዊ ኑሮ መድኀኒት መሆኑን አመሥጥሮ አግኝቶ ባያረጋግጥም ከማንም በላይ እኔ ነኝ ብሎ ያምናል፡፡ ልበ ሙሉ ነው፡፡</p>
<p class="continued">ከኢትዮጵያ ፍልስፍና አንዱ ቅኔ ……ይቀጥላል</p>
</div>
<div lang="en">
<p><strong>Consciousness</strong> is a lamp that lets one see, even in darkness, a wisdom and a joy that others have not seen. Philosophy is the sea of knowledge that springs from consciousness. Together, consciousness and philosophy are a single instrument by which a person can save himself and so save society — but consciousness comes first, for without it there can be no philosophy. Consciousness is the instrument by which a society can weigh its common life and set it in order. When people not formed by consciousness rise to power, the philosophy that gives light in darkness has not yet been laid in them, and they lack the eye of light that would see society rightly. Without consciousness they do not even know what they do not know and cannot do; believing that they know, they lead society into chaos — and even then the problem does not stand out to them. Lacking the light of consciousness, they waste their time trying to gather up spilt water, and they lack the inner eye that would say, “There may be someone better than I for the good of the country — let him try.” When such people come to power, they kill not individuals but a whole country.</p>
<p><strong>Philosophy:</strong> In brief, philosophy is the expression of many kinds of hidden natural wisdom. Put broadly, it is the instrument that lets us think and provoke thought about what has not been thought, see and show what has not been seen, and say what has not been said. Invention and discovery, for example, are philosophy. The one the world calls a philosopher is the person able to explain, in writing or in speech, an idea never before spoken or heard — and to seek out and decipher, by short or long process, a nature that was hidden and unrevealed. It is to show the eye what it cannot see, so that a person rejoices, is stirred and thinks; to let the ear hear a mystery unheard, so that it delights, awakens and reflects. It is also the ability to bring forth inventions for daily life, and to put them at society’s service. Some of what is called philosophy, however, proves limited in what it reveals: once the philosopher has shown it and made it heard, it does not grow much further; it simply sits there, heaped up. Among well-known discoveries, for example — that the earth turns; that the planets travel on, keeping their order, their orbits, through their natural gravity and force so that they neither collide nor scatter; that cold and dry air colliding produces lightning — such kinds of philosophy, once revealed, are fixed by a single law and remain on display. Ethiopian philosophy — Qene — is different: it never runs out. Every day it creates and invents anew, expanding and deepening. No one has ever measured or set bounds to the breadth and depth of Qene. It is a subtle philosophy, to be thought rather than seen or touched; yet it cleanses the mind of its dross, drives out the darkness and clothes it in light. A person who knows Qene counts as nothing the richest, most learned or most powerful man beside him. Even if he has not deciphered and confirmed that to work for one’s bread is a divine command and the remedy for social life, he believes himself above anyone. He is wholehearted.</p>
<p class="continued">Qene, one of the philosophies of Ethiopia — to be continued…</p>
</div>
<p class="contribute-link"><a class="text-link" href="../contact/">{T("በዚህ ርእስ መሳተፍ ለሚፈልጉ ቅድመ ገጹ ክፍት ነው →", "This page is open to anyone who wishes to contribute on this subject →")}</a></p>
</article>
'''

# ---------- Qene 1: Zeamlakiye ----------
z_lines = "ኖላዌ አባግዕ ኪሩቤል አማላከ ነግደ ኢዮር ዜና፡፡\nፅዑን ዓየረ ነጋሢ ኤልያስ ደመና፡፡\nሐዊረ ምድረ ኢዮር ዓርብ ሃገረ ፀዓዱን ዘሲና፡፡"
q1 = f'''<article class="qene" id="zeamlakiye">
<p class="eyebrow">{T("የመንክር ግጨው", "By Menkir Gichew")}</p>
<h2>{T("ዘአምላኪየ — 2ኛ ቅኔ", "Ze-Amlakiye — Qene 2")}</h2>
<div class="verse geez">{z_lines}</div>
<h3>{T("በአማርኛ ሲፈታ", "Meaning")}</h3>
{P("ኪሩቤል በጎችን የሚጠብቅ የሰማይ ዜና መንገደኛ አምላክ ሲናይ የተባለች ወደ ነጮች አገር ወደ ሰማይ አገር ምድር ለመኄድ ዓርብ ዕለት በንጉሥ ኤልያስ አየር ደመና ተጫነ ነው፡፡",
   "The God who keeps the cherubim as His flock — the traveller of heavenly tidings — mounted the cloud of King Elijah’s air on a Friday, to go to the land called Sinai: the land of the white ones, the land of heaven.")}
<h3>{T("በባሕረ ቀመር ቍጥር ሒሣብ ሲሠራ", "Worked by Bahre Kemer Calculation")}</h3>
{P("አሁን ለቃላት ሦስት ቍጥር ለፊደላት ዐራት፡ አምስትና ስድስት ቍጥር መድበናል፡፡",
   "Here we have assigned the value 3 to each word, and 4, 5 and 6 to the letters of the first, second and third lines.")}
{sheet("ቃላት (× 3)", "Words (× 3)", [
  row("ኖላዌ + አባግዕ + ኪሩቤል + አማላከ + ነግደ + ኢዮረ + ዜና", "7 × 3 = 21"),
  row("ፅዑን + ዓየረ + ነጋሢ + ኤልያስ + ደመና", "5 × 3 = 15"),
  row("ሐዊረ ምድረ ኢዮር ዓርብ ሃገረ + ፀዓዱን + ዘሲና", "3 × 5 = 15 + 3 + 3 = 21"),
  row(SUM, "21 + 15 + 21 = <b>37</b>", "ws-sum")])}
{sheet("ፊደላት (× 4፡ × 5፡ × 6)", "Letters (× 4, × 5, × 6)", [
  row(chips("ኖላዌአባግዕኪሩቤልአማ", 4), "13 × 4 = 52"),
  row(chips("ላከነግደኢዮረዜና", 4), "10 × 4 = 40"),
  row("ፅዑን 3×5 + ዓየረ 3×5 + ነጋሢ 3×5 + ኤልያስ 4×5 + ደመና 3×5", "80"),
  row("ሐዊረ 3×6 + ምድረ 3×6 + ኢዮር 3×6 + ዓርብ 3×6 + ሃገረ 3×6 + ፀዓዱን 4×6 + ዘሲና 3×6", "132"),
  row(SUM, "52 + 40 + 80 + 132 = <b>304</b>", "ws-sum")])}
<p class="grand">{T("ጠቅላላ ድምር", "Grand total")}: 37 + 304 = <b>341</b></p>
</article>
'''

# ---------- Qene 2: Gubae Qana ----------
g1 = "ዮሐንስ ደክመ በመንግሥተ ሰማይ ፍና፡፡\nአኮኑ ኢጥዕመ መቃብረ አልዓዛር መና፡፡"
words1 = ["ዮሐንስ", "ደክመ", "በመንግሥተ", "ሰማይ", "ፍና"]
words2 = ["አኮኑ", "ኢጥዕመ", "መቃብረ", "አልዓዛር", "መና"]
def letter_rows(words):
    out = []
    for w in words:
        out.append(row(chips(w, 2), f"{len(w)} × 2 = {len(w)*2}"))
    return out
q2 = f'''<article class="qene" id="gubae-qana">
<p class="eyebrow">{T("የመምህር መንክር ግጨው", "By Memhir Menkir Gichew")}</p>
<h2>{T("ጉባዔ ቃና — 1ኛ ቅኔ", "Gubae Qana — Qene 1")}</h2>
<div class="verse geez">{g1}</div>
<h3>{T("ሲፈታ", "Meaning")}</h3>
{P("ዮሐንስ ወደ መንግሥተ ሰማያት በሚወስደው መንገድ ደከመ፡፡ የአልዓዛር መቃብር ምግብን አልቀመሰምና፡ ነው፡፡",
   "John grew weary on the road to the Kingdom of Heaven — for he had not tasted the food of Lazarus’s tomb.")}
<dl class="semwerq">
<dt>{T("ሰሙ", "Sem — the wax")}</dt>
<dd>{T("አንድ ሰው ወደ መንገድ ሲኄድ እህልን ካልቀመሰ ይደክመዋል፡፡ ደከመ የሚለው አንቀጽ ጉዳትን ያመለክት ነበር፡፡ ዮሐንስ ግን ጉዳት አልደረሰበትም፡፡ የቅኔ ኩሸት የሚባለውን ማጉላታቸዉ ነው እንጂ፡፡",
       "A person who sets out on a journey without having eaten grows weary. The verb ደከመ (“grew weary”) would suggest harm, but John came to no harm: it is simply the poet heightening what Qene calls <i>kushet</i> — the poetic feint.")}</dd>
<dt>{T("ወርቁ", "Werq — the gold")}</dt>
<dd>{T("ቅኔው ለዮሐንስ ወልደ ነጎድጓድ ሳይሆን አይቀርም፡፡ እና ዮሐንስ አልዓዛር ከተቀበረበት መቃብር አልተቀበረም ለማለት ነው፡፡ ታሪኩ፡ ሥጋው ከመቃብር ጠፋ ስለ ሚል ነው፡፡ ስለዚህ የአልዓዛር መቃብር ምግብን አልቀመሰም አለ ቅኔው፡፡",
       "The qene is most likely about John, Son of Thunder. It means that John was not buried in a tomb as Lazarus was — for the tradition says his body vanished from the tomb. So the qene says he “did not taste the food of Lazarus’s tomb.”")}</dd>
</dl>
<h3>{T("በባሕረ ቀመር ዘዴ ሒሣብ ሲሠራ", "Worked by the Bahre Kemer Method")}</h3>
{P("ለያንዳንዷ ቃልና ፊደል የፈለግነውን ቊጥር እንመድባለን፡፡ 1ም 2ም 3ም 4ም 5ም....12ም....19ም ሊሆን ይችላል፡፡ ከዚያ በላይም መመደብ ይቻላል፡፡ አሁን ለቃላት 4ት 4ት ቁጥር፡ ለፊደላት 2ት 2ት ቁጥር መድበናል፡፡",
   "We assign whatever number we choose to each word and each letter — it may be 1, 2, 3, 4, 5 … 12 … 19, or higher. Here we have assigned 4 to each word and 2 to each letter.")}
{sheet("ቃላት (× 4)", "Words (× 4)", [
  row("ዮሐንስ + ደክመ + በመንግሥተ + ሰማይ + ፍና", "5 × 4 = 20"),
  row("አኮኑ + ኢጥዕመ + መቃብረ + አልዓዛር + መና", "5 × 4 = 20"),
  row(SUM, "20 + 20 = <b>40</b>", "ws-sum")])}
{sheet("ፊደላት (× 2) — 1ኛ መስመር", "Letters (× 2) — line 1", letter_rows(words1) + [row(SUM, "8 + 6 + 12 + 6 + 4 = <b>36</b>", "ws-sum")])}
{sheet("ፊደላት (× 2) — 2ኛ መስመር", "Letters (× 2) — line 2", letter_rows(words2) + [row(SUM, "6 + 8 + 8 + 10 + 4 = <b>36</b>", "ws-sum")])}
<p class="grand">{T("ሲደመር", "Sum")}: 36 + 36 = <b>72</b> &nbsp;·&nbsp; {T("የመጨረሻ ድምር", "Final total")}: 40 + 72 = <b>112</b></p>
{P("ይህ በቀላል ሒሣብ የተሠራ የአንዲት ጉባዔ ቃና ሒሣብ ሥራ ነው፡፡", "This is the working of a single Gubae Qana, done with simple arithmetic.")}
<h3>{T("2ኛ. እንደ ዚህም", "A second way")}</h3>
{P("እንደ ሚከተለውም መሥራት ይቻላል፡፡ ልዩነቱ የቁጥሩ አቀማመጥ ቦታ ነው፡፡", "It can also be worked as follows; the only difference is where the numbers are placed.")}
{sheet("", "", [
  row("ዮሐንስ<sub>4</sub> + ደክመ<sub>4</sub> + በመንግሥተ<sub>4</sub> + ሰማይ<sub>4</sub> + ፍና<sub>4</sub>", "20"),
  row("አኮኑ<sub>4</sub> + ኢጥዕመ<sub>4</sub> + መቃብረ<sub>4</sub> + አልዓዛር<sub>4</sub> + መና<sub>4</sub>", "+ 20 = <b>40</b>"),
  row(chips("ዮሐንስደክመበመንግሥተሰማይፍና", 2), "36"),
  row(chips("አኮኑኢጥዕመመቃብረአልዓዛርመና", 2), "+ 36 = <b>72</b>"),
  row(T("የመጨረሻ ድምር", "Final total"), "40 + 72 = <b>112</b>", "ws-sum")])}
<aside class="note">{P("ማሳሰቢያ፡ ሒሣቡን በአኀዝ ቁጥር መሥራት ይቻል ነበር፡፡ ግን ዌብሳይቱ የኛን ቁጥር አልቀበልም አለኝ፡፡",
   "Note: the calculation could have been done in Ge’ez numerals, but the website would not accept our numerals.")}</aside>
</article>
'''
open(OUT, "w", encoding="utf-8").write("<!-- Generated by _gen_qene.py -->\n" + essay + '<div class="qene-list">\n' + q1 + q2 + "</div>\n")
print("ok")
