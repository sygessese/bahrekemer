# Generates content/numbers.html (bilingual) for the Bahrekemer site.
import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "numbers.html")

def T(am, en): return f'<span lang="am">{am}</span><span lang="en">{en}</span>'
def P(am, en, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<p lang="am"{c}>{am}</p>\n<p lang="en"{c}>{en}</p>'

H = {"n": ("#", "#"), "akh": ("አኀዝ", "Numeral"), "gz": ("ግዕዝ", "Ge’ez name"), "am": ("አማርኛ", "Amharic"),
     "ar": ("ዓረቢክ", "Arabic"), "bk": ("ባሕረ ቀመር", "Bahre Kemer")}
GLOSS = {"ዐሥር ሺሕ": "ten thousand", "መቶ ሺሕ": "one hundred thousand", "ሚሊየን": "million", "ዐሥር ሚሊየን": "ten million",
         "መቶ እልፍ ጊዜ ሺሕ": "a hundred elf times a thousand", "ሺ ሚሊየን": "a thousand million",
         "እልፍ ሚሊየን": "ten thousand million", "መቶ ሚሊየን": "one hundred million",
         "አንድ": "one", "ዐሥር": "ten", "አንድ መቶ": "one hundred", "አንድ ሺሕ": "one thousand"}
for unit, tr in [("እልፍ", "elf"), ("አእላፍ", "a’elaf"), ("አእላፋት", "a’elafat")]:
    for am, en in [("አንድ", "one"), ("ዐሥር", "ten"), ("አንድ መቶ", "one hundred"), ("አንድ ሺሕ", "one thousand")]:
        GLOSS[f"{am} {unit}"] = f"{en} {tr}"
GLOSS["አንድ እልፋት"] = "one elfat"

def cell(v, col):
    if col == "am" and v:
        return T(v, GLOSS.get(v, v))
    return v

def table(cols, rows, groups=None):
    head = "".join(f'<th class="c-{c}">{T(*H[c])}</th>' for c in cols)
    body = []
    for i, r in enumerate(rows):
        cls = ' class="group-start"' if groups and i in groups else ""
        body.append(f"<tr{cls}>" + "".join(f'<td class="c-{c}">{cell(v, c)}</td>' for c, v in zip(cols, r)) + "</tr>")
    return (f'<div class="table-wrap"><table class="numtable"><thead><tr>{head}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>')

def numbered(rows):  # prepend row numbers
    return [[str(i + 1)] + list(r) for i, r in enumerate(rows)]

def entry(n, src_am, src_en, body):
    return f'''<article class="num-entry" id="source-{n}">
  <h3><span class="num-n">{n}</span>{T(src_am, src_en)}</h3>
  {body}
</article>'''

parts = []

# ---------- Intro ----------
parts.append(f'''<article class="prose num-intro">
<h2>{T("ከአሁን ቀደም አኀዝ ቊጥርን ማሻሻልና ማሳደግ የሞከሩ ኢትዮጵያዊያን", "Ethiopians Who Have Tried to Improve and Extend the Ge’ez Numerals")}</h2>
{P("ሙከራቸዉ የሚደነቅ ሲሆን፡ በነበረበት ዘመን ታሪካዊና ሃገራዊ ቊጥር እንደ መሆኑ መጠን፡ አሁን ቊጥሩ ከ፩፻፼ (ከ1000000) ቤት በላይ ከፍ እያለ ሲኄድ የሁሉም ባለ ሙያዎች ውሳኔ ሊስማማ አልቻለም፡፡ የኸውም ስለ ሃገር ስለ ህዝብ በኅብረት መሥራትና መወሰን ይገባ ነበር፡፡ ስለ አገር ጉዳይ በጥናት ተደግፎ እየቀነሱ እየጨመሩ በኅብረት መሥራት እንደ ሚገባ ይታመናል፡፡ የሁሉም መነሻቸዉ የአለቃ ኪዳነ ወልድ ክፍሌ እንደ ሆነም በሥራቸዉ ይረጋገጣል፡፡",
   "Their efforts are admirable; in its own time this was a historic and national system of numbers. Yet as the numbers rise beyond the place of ፩፻፼ (1,000,000), the conclusions of the specialists have failed to agree. On a matter that concerns the nation and its people, they ought to have worked and decided together; it is right that national questions be worked on jointly, supported by research, taking away and adding as needed. Their own work confirms that all of them took Aleqa Kidane Wold Kifle as their starting point.")}
{P("ይሁን እንጂ አለቃ ኪዳነ ወልድ እንደ ሌላ ጥናታቸዉ በአኀዝ ቍጥር ላይ አላተኮሩበትም፡፡ ከእሳቸዉ በፊት ሦስቱን የቍጥር ሕግ ያሟላ ከመቶ እልፍ ቤት በላይ የያዘ ዋቢ መጻሕፍትን ስለ አላገኙ እንደ መሰላቸዉ ነው ነክተውት ያለፉት፡፡ ለምሳሌ መዝገበ ፊደል 1926 ዓ. ም. በሚል መጽሐፋቸዉና መጽሐፈ ሰዋስው ወግሥ ወመዝገበ ቃላት ሐዲስ 1948 ዓ. ም. በሚለው ተመሳሳይ ውሳኔ አያመለክትም፡፡ በ፼፼ (አእላፍ) ትእልፊትና ምእልፊት ላይ ውሳኔያቸዉ የተለያየ ሆኖ ይገኛል፡፡ ስለ ዚህ ስለ አኀዝ ቍጥር አላሰቡበትም ነበር ለማለት ይቻላል፡፡ ምክንያቱም ሌላ ጥናታቸዉ የተከበረ የሚደነቅ ስለ ሆነ ነው፡፡ ስለ ሌላዎች ከእሳቸዉ መጽሐፍ እየገለበጡ የጻፉት ስለ ሆኑ ብዙም የሚያነጋግር አይደለም፡፡ በባሕረ ቀመር ከ፩፻፼ ቤት በላይ የቀረበው ጥናት፡ የራሴ ግኝት እንደ ሆነ መታወቅ አለበት፡፡",
   "Aleqa Kidane Wold, however, did not give the numerals the attention he gave his other studies. Having found no earlier reference work that satisfied the three laws of number and went beyond the place of a hundred elf, he touched on the subject as it seemed to him and moved on. His <i>Mezgebe Fidel</i> (1926 E.C.) and his <i>Metshafe Sewasew Wegis Wemezgebe Qalat Haddis</i> (1948 E.C.), for example, do not reach the same conclusion: they differ on ፼፼ (a’elaf), ትእልፊት and ምእልፊት. One may say, then, that he had not thought the numerals through — for the rest of his scholarship is respected and admired. As for the others, since they wrote by copying from his book, there is little to discuss. It should be known that the study presented in <i>Bahre Kemer</i> beyond the place of ፩፻፼ is my own discovery.")}
</article>''')

# ---------- Ownership ----------
parts.append(f'''<aside class="notice">
<h2>{T("የባለ ቤትነት ማረጋገጫ", "Proof of Ownership")}</h2>
{P("ከየኢትዮጵያ አእምሮአዊ ንብረት መሥሪያ ቤት ጽ/ቤት በቊጥር 1/1/1/2/0041 የምዝገባ ቀን 03/09/2007 ዓ. ም. በተረጋገጠ የባለቤትነት ሰርቲፊኬት የተሰጠኝ መሆኑን በቅድሚያ ማረጋገጥ ይገባል፡፡ ከዚህ ቀን በሁዋላ ከ፩፻፼ (ከአንድ መቶ እልፍ) ቤት በላይ የያለውን የባሕረ ቀመር ቊጥር፡ ከባሕረ ቀመር ቊጥር ሕግ ውጪ አዛብቶ የጻፈ በሕግ የሚያስጠይቅ መሆኑን ማስታወስ ይገባል፡፡",
   "Let it first be established that I hold a certificate of ownership issued by the Ethiopian Intellectual Property Office, No. 1/1/1/2/0041, registered on 03/09/2007 E.C. Be advised that, from that date, anyone who writes the Bahre Kemer numbers beyond the place of ፩፻፼ (one hundred elf) in a distorted form, outside the rules of the Bahre Kemer number system, is liable under the law.")}
<p class="sig">{T('መ. ይትባረክ ገሠሠ — አድራሻና ፎን <a href="../contact/">ኮንታክት</a> ከሚለው ይመልከቱ፡፡', 'Memhir Yitbarek Gessese — for address and phone, see <a href="../contact/">Contact</a>.')}</p>
</aside>''')

# ---------- Sources ----------
parts.append(f'''<header class="section-head num-sources-head">
<h2>{T("ማሻሻል የሞከሩ ደራሲያን ኢትዮጵያዊያን", "Ethiopian Authors Who Have Attempted Improvements")}</h2>
<p>{T("ከ1950 (ሃምሣዎቹ) ወዲህ አኀዝ ቊጥርን ማሻሻልና ማሳደግ የሞከሩ ኢትዮጵያዊያን ደራሲያን የሙከራ ሥራቸዉ ከዚህ ቀጥሎ ተመልክቶአል፡፡",
       "The attempts of Ethiopian authors who, since the 1950s, have tried to improve and extend the Ge’ez numerals are set out below.")}</p>
<div class="ornament" aria-hidden="true"><span></span></div>
</header>''')

E = []
E.append(entry("1", "አለቃ ኪዳነ ወልድ ከፍሌ፡ መዝገበ ፊደል የገዕዝና አማርኛ ቋንቋ የአፍ መክፈቻ፡ 1926 ዓ. ም.",
  "Aleqa Kidane Wold Kifle, <i>Mezgebe Fidel: An Opening of the Mouth in Ge’ez and Amharic</i>, 1926 E.C.",
  table(["n", "akh", "gz", "am"], numbered([
    ["፼", "እልፍ", "ዐሥር ሺሕ"], ["፲፼", "አእላፍ", "መቶ ሺሕ"], ["፻፼", "አእላፋት", "ሚሊየን"], ["፲፻፼", "ትእልፊት", "ዐሥር ሚሊየን"],
    ["፼፼", "ትእልፊታት", "መቶ እልፍ ጊዜ ሺሕ"], ["፲፻፼፼", "ምእልፊት", "ሺ ሚሊየን"], ["፼፼፼", "ምእልፊታት", "እልፍ ሚሊየን"]]))
  + P("ስናየው በራሳቸዉ ስልት እንክዋን አልተሳካም፡፡ ዐሥርቱ ምእልፊት ሳይሉ ነው ዐሥርቱ ምእት ምእልፊት ያሉ፡፡",
      "As we see, it does not succeed even by its own method: it jumps to “ten hundred ምእልፊት” without first saying “ten ምእልፊት.”", "verdict")))

E.append(entry("2", "አለቃ ኪዳነ ወልድ ክፍሌ፡ መጽሐፈ ሰዋስው ወግሥ ወመዝገበ ቃላት ሐዲስ፡ 1948 ዓ. ም.",
  "Aleqa Kidane Wold Kifle, <i>Metshafe Sewasew Wegis Wemezgebe Qalat Haddis</i>, 1948 E.C.",
  table(["n", "akh", "gz", "am"], numbered([
    ["፼", "እልፍ", "ዐሥር ሺሕ"], ["፲፼", "ዐሥርቱ እልፍ", "መቶ ሺሕ"], ["፻፼", "አእላፋት", "ሚሊየን"], ["፲፻፼", "ትእልፊት", "ዐሥር ሚሊየን"],
    ["፼፼", "ምእልፊት", "መቶ ሚሊየን"]]))
  + P("ከላይኛውና ታችኛው ያለው ቁጥር 5ኛውንና 5ኛውን ተመልከቱ፡፡ ሁለቱም መጽሐፎቻቸዉ አልተስማሙም፡፡",
      "Compare row 5 of the table above with row 5 here: his two books do not agree.", "verdict")))

E.append(entry("3", "ሊቀ ጠበብት አክሊለ ብርሃን ወልደ ቂርቆስ፡ መጽሔተ ጠበብ፡ 1948 ዓ. ም.",
  "Liqe Tebebt Aklile Birhan Wolde Qirqos, <i>Metshete Tebeb</i>, 1948 E.C.",
  table(["n", "akh", "gz"], numbered([
    ["፼", "እልፍ"], ["፲፼", "አእላፍ"], ["፻፼", "አእላፋት"], ["፲፻፼", "ትእልፊት"], ["፻፼፼", "ትእልፊታት"], ["፲፻፼፼", "ምእልፊት"], ["፼፼፼", "ምእልፊታት"]]))
  + P("በአኀዝ ቁጥር እስከ 4 ተራ ቁጥር ሕጉን ጠብቆአል፡፡ ግዕዙ እስከ ሦስት ረድፍ ጠብቆአል፡ የዐሥር ዕድገትን ግን አላሙአላም፡፡",
      "The numerals keep the rule up to row 4, and the Ge’ez names up to row 3; but the growth by tens is not fulfilled.", "verdict")))

E.append(entry("4", "መሥፍን ልሳኑ፡ አማርኛ መጽሔተ ቃላት፡ 1952 ዓመተ ምሕረት",
  "Mesfin Lisanu, <i>Amharic Metshete Qalat</i>, 1952 E.C.",
  table(["n", "akh", "gz", "ar"], numbered([
    ["፼", "እልፍ", "10,000"], ["፲፼", "አእላፍ", "100,000"], ["፻፼", "አእላፋት", "1,000,000"], ["፲፻፼", "ትእልፊት", "10,000,000"],
    ["፼፼", "ምእልፊት", "100,000,000"], ["፲፻፼፼", "አእላፈ አእላፋት", "100,000,000,000"], ["፼፼፼", "አእላፈ ትእልፊት", "1,000,000,000,000"],
    ["፲፼፼፼", "ትእልፊተ አእላፋት", "10,000,000,000,000"], ["፼፼፼", "ምእልፊተ አእላፋት", "100,000,000,000,000"],
    ["፲፻፼፼፼", "ትእልፊተ ምእልፊት", "1,000,000,000,000,000"], ["፼፼፼፼", "ምእልፊተ ምእልፊት", "10,000,000,000,000,000"]]))
  + P("አኀዙ እስከ 5 ግዕዙ እስከ 3 ተሠርቶአል፡፡ ከዚህም በተመሳሳይ የዐሥር ዕድገትን አልጠበቀ፡፡ ከእሳቸዉ ስለ ተቀዳ ከአለቃ ውሳኔ ጋር ይመሳሰላል፡፡",
      "The numerals are correct up to row 5, the Ge’ez names up to row 3. Here too the growth by tens is not kept; having been copied from him, it resembles the Aleqa’s conclusion.", "verdict")))

E.append(entry("5", "መምህር ፍሥሐ ፅዮን ካሣ፡ መርኆ፡ 1991", "Memhir Fisseha Tsion Kassa, <i>Merkho</i>, 1991",
  table(["n", "akh", "gz"], numbered([
    ["፼", "እልፍ"], ["፲፼", "አእላፍ"], ["፻፼", "አእላፋት"], ["፲፻፼", "ትእላፍ"], ["፻፼፼", "ትእልፊት"], ["፲፻፼፼", "ትእላፋት"],
    ["፼፼፼", "አእላፍ"], ["፻፼፼፼", "ምእልፊት"], ["፲፻፼፼፼፼", "ምእላፋት"]]))
  + P("ከዚህም እስከ 4 አመልክቶአል፡፡ መፍቻው ደኅና ነበር ግን አልተስማማም፡፡",
      "This one, too, is correct up to row 4. The key was sound, but it does not hold together.", "verdict")))

E.append(entry("6", "አፈወርቅ ዘውዴ፡ ጸያሔ ፍኖት፡ 1948", "Afewerk Zewde, <i>Tseyahe Finot</i>, 1948",
  table(["n", "akh", "gz"], numbered([
    ["፼", "እልፍ"], ["፲፼", "ዐሥር አእላፍ"], ["፻፼", "መቶ አእላፋት"], ["፲፻፼", "ዐሥር መቶ እልፍ"], ["፼፼", "ምእልፊት"]]))
  + P("አኀዙ እስከ 4 ጠብቆአል፡ መፍቻው ግዕዙ ግን አልጠበቀም የተዘበራረቀ ነው፡፡",
      "The numerals hold up to row 4, but the key — the Ge’ez — does not; it is muddled.", "verdict")))

E.append(entry("7", "ሊቀ ኅሩያን በላይ መኮነን፡ ሕያው ልሳን፡ ግዕዝ - አማርኛ መዝገበ ቃላት፡ 1999 ዓ. ም.",
  "Liqe Hiruyan Belay Mekonnen, <i>Hiyaw Lisan: A Ge’ez–Amharic Dictionary</i>, 1999 E.C.",
  table(["n", "akh", "gz"], numbered([
    ["፼", "እልፍ"], ["፲፼", "አእላፍ"], ["፻፼", "አእላፋት"], ["፲፻፼", "አእላፈ አእላፋት"], ["፼፼", "ትእልፊት"], ["፲፼፼", "ትእላፋት"],
    ["፻፼፼", "ትእልፊታት"], ["፲፻፼፼", "ትእልፊተ አእላፋት"], ["፼፼፼", "ምእልፊት"], ["፲፼፼፼", "ምእላፋት"], ["፲፻፼፼፼", "ምእልፊታት"],
    ["፼፼፼፼", "ምእልፊተ አእላፋት"]]))
  + P("የአኀዝ ድርድሩ እስከ ቁጥር 10 የዐሥር ዕድገቱን ጠብቆአል፡ የግዕዝ ትርጉሙ እስከ 3 ጠብቆአል፡፡ ከዚያ የዐሥር ዕድገቱን አልጠበቀም፡፡",
      "The arrangement of numerals keeps the growth by tens up to row 10; the Ge’ez names hold up to row 3. Beyond that, the growth by tens is not kept.", "verdict")))

E.append(entry("8", "መሪጌታ ዘነበ ሐየሎም (ግን ((ኀ)) የኸ ነው — ኀየሎም)፡ ባሕረ ሐሣብ፡ 2008፡ አሳታሚና አከፋፋይ፡ በኢ/ኦ/ተ/ቤ/ክ/በሰ/ት/ቤቶች ማደራጃ መምርያ ማኅበረ ቅዱሳን",
  "Merigeta Zenebe Hayelom (properly spelled with ኀ — ኀየሎም), <i>Bahre Hassab</i>, 2008; published and distributed by Mahibere Kidusan, Sunday Schools Department of the Ethiopian Orthodox Tewahedo Church",
  table(["n", "akh", "gz", "ar"], numbered([
    ["፻", "መቶ", "100"], ["፲፻", "ሺሕ", "1,000"], ["፼", "ዕልፍ ዐሥር ሸሕ", "10,000"], ["፲፼", "አዕላፍ መቶ ሸሕ", "100,000"],
    ["፻፼*", "አዕላፋት", "1,000,000"], ["፲፻፼", "ትዕልፊት", "10,000,000"], ["፼፼", "ምዕልፊት", "100,000,000"],
    ["፲፻፼፼", "አዕላፈ አእላፋት", "100,000,000"], ["፼፼፼", "አዕላፈ ትዕልፊት", "1,000,000,000"], ["፲፼፼፼", "ትዕልፊተ አዕላፋት", "10,000,000,000"],
    ["፻፼፼፼", "ምዕልፊተ አዕላፋት", "100,000,000,000"], ["፲፻፼፼፼", "ትዕልፊተ ትዕልፊት", "1,000,000,000,000"], ["፼፼፼፼", "ምዕልፊተ ምዕልፊት", "10,000,000,000,000"]]))
  + P("አኀዙ እስከ ተራ ቁጥር 7 ጠብቆ ከዚያ ፈርሶአል፡፡ ግዕዙ ከ5ኛ ጀምሮ አልጠበቀም፡፡",
      "The numerals hold up to row 7 and then collapse; the Ge’ez fails from row 5 on.", "verdict")
  + P("ማኅበረ ቅዱሳን የሚባለው የወጣት ዘመናዊያን ድርጅት በቤተ ክርስቲያንዋ ደጀ ሰላምና ዐውደ ምሕረት ያደገ ባይሆንም ባለው መሠረትና ይዘት ቤተ ክርስቲያንዋን የምወክል እኔ ነኝ የሚልበት ጊዜ ሩቅ አይሆንም፡፡ መከላከል የማይችል ሰንበሊጥ የምንኩስና ሥርዓትን ጥሶ ABCD ሽጉጡን ታጥቆ ቤተ መቅደስ በመግባቱ፡ ቅርስን ጠባቂ ለባህል ተቆርቃሪ ይመስል ነበር፡፡ እውነትም የሚያስብል ነው፡፡ ለአብነት ለመምህራን ሞራልን በመስጠትና ትንሽ ቢሆንም ጊዜያዊ አዳጋን በመከላከል የሚያደርገው ያለ ሙከራም አሁንም የምንኩስና አስተዳደርን በሕሊና እየበለጠውና እየበከለው እንደ ሆነ እያመለከተ ነው፡፡ በሌላ ወገን አፍራሽነቱ በአደባባይ እየተረጋገጠ ነው፡፡ ትውልዱ በአንድ ሃገራዊ ጥናትና ጥበብ ተጉዞ የቊጥር ዕድገቱን እንዳያፋጥን ዕንቅፋት የሚፈጥር ነው፡፡ መጽሐፉ (ባሕረ ሐሣብ) ሃገራዊ ጥናቱ ሌላ ሆኖ ሳለ የአኀዝ ቊጥሩን ጨልፎና ከመጨረሻ ገጽ ለጥፎ ትውልድን ማወናበድ ማነንን ይጠቅማል? ሁሉንም ሊጎዳ ካልሆነ በቀር፡፡ በልማድ ከመጨረሻ ገጽ አኀዝ ቊጥርን መለጠፍ እንግዲህ አያስከድም፡ በባሕረ ቀመር ጥናታዊ መጽሐፍ አበቃ ተዘጋ፡፡ አሁንም አሥቡበት ሳያውቁ ከእንደ ዚህ ያለ አዳጋ ኄዶ መጨመሩ ሃገርንም ማንንም አይጠቅምም፡፡ በጥናት የተደገፈ የሚያነጋግር ቢሆን ኖሮ መነጋገሩ አይከፋም ነበር፡፡ ይህ ግን ዝም ብሎ ዎፍ ዘራሽ አረም ቢጤ ነውና ስለ ትውልድ ሲባል ከመጽሐፋችሁ መጨረሻ ለተለጠፈው የአኀዝ ቁጥር ዕድገት መግለጫ ቢደረግበት መልካም ሃገራዊ ትዝብት ሊሆን ይችላል፡፡ ልክ ነው የሚል ሰው ካለ ግን በኢትዮጵያዊነት ምሥጢር በታነፀ መድረክ አገናኙንና ተማምነን ቀናውን ሃገራዊ ምሥጢር እንመርጣለን፡፡",
      "The organisation of modern young people called Mahibere Kidusan did not grow up in the church’s courtyard and precincts; yet, given its foundation and its content, the day will not be far off when it says, “It is I who represent the Church.” Like a defenceless blade of grass that broke through the order of monasticism and entered the sanctuary armed with its ABCD pistol, it seemed a guardian of heritage and a defender of culture — and one might indeed think so. Its efforts, such as lifting the morale of the traditional teachers and, if only a little, warding off immediate dangers, show that even now it is outdoing the monastic administration in consciousness — and corrupting it. On the other hand, its destructiveness is being confirmed in public: it creates obstacles that keep the generation from advancing the growth of its numbers through a single national scholarship and wisdom. The book (<i>Bahre Hassab</i>) is otherwise a work of national scholarship; whom does it benefit to skim off a table of numerals, paste it on the last page and so mislead a generation? It can only harm everyone. Pasting numerals onto the last page out of habit will no longer pass: with the scholarly book <i>Bahre Kemer</i>, that is over and done. Think about it even now: wading unknowingly into such a hazard benefits neither the nation nor anyone. Had it been something supported by research and worth debating, a discussion would do no harm. But this is no more than a weed sown by birds; for the sake of the generation, it would be a worthy national gesture to issue a statement on the table of numerals pasted at the end of your book. And if anyone holds that it is correct, bring us together on a platform built in the spirit of Ethiopian identity, so that we may reach an understanding and choose what is true for the nation.")))

E.append(entry("9", "መሪጌታ አእምሮ በሪሁን፡ የኢትዮጵያ ፊደልና ክፍለ ዘመን፡ 2000 ዓ. ም.",
  "Merigeta Aemro Berihun, <i>The Ethiopian Alphabet and the Centuries</i>, 2000 E.C.",
  table(["n", "akh", "gz"], numbered([
    ["፼", "እልፍ"], ["፲፼", "አእላፍ"], ["፻፼", "አእላፍ"], ["፲፻፼", "ትእልፊት"], ["፼፼", "ትእልፊታት"], ["፲፼፼", "ምዕልፊት"],
    ["፻፼፼", "ምእልፊታት"], ["፲፻፼፼", "አእላፈ አእላፋት"], ["፼፼፼", "ትእልፊተ አእላፋት"], ["፲፼፼፼", "ምእልፊተ አእላፋት"], ["፼፼፼፼", "እልፊተ አእላፋት"]]))
  + P("አኀዙ እስከ ቁጥር 10 ሕጉን ጠብቆአል፡ ከዚያ አልጠበቀም፡፡", "The numerals keep the rule up to row 10, but not beyond.", "verdict")))

E.append(entry("10", "መሪ ራስ አማን በላይ፡ መጽሐፍ ብሩክ ዣን ቀዳማዊ፡ 2000 ዓ. ም.",
  "Meri Ras Aman Belay, <i>Metshaf Biruk Zhan Qedamawi</i>, 2000 E.C.",
  table(["akh", "gz"], [
    ["፼", "እልፍ"], ["፲፼", "እልፍ"], ["፻ ፼", "እልፈ አእላፍ"], ["፻፼", "አእላፍ"], ["፲ ፻፼", "አእላፈ አእላፋት"], ["፻ ፻፼", "አእላፋተ ትእልፍ"],
    ["፼፼", "ትእልፍ"], ["፻፼፼", "ትእልፊታት፡ ትእልፈ ትእልፊት፡ ትእልፊተ ትእልፊት"], ["፼፼፼", "ትእልፊት ትእልፊታት እልፊታት ትእልፊታተ እለፍት"],
    ["፼፼፼", "እለፍት እለፍተ እለፍታት እለፍታተ እለፍታት"],
    ["፻፼፼፼", "እለፍታት መእልፍ መእለፍት መእለፍታት ምእላፍ ምእላፋት ምእልፋታት ምልፍ ምእልፊት"]])
  + P("ከመጀመርያመም አልጠበቀም፡፡", "It fails from the very first row.", "verdict")))

names11 = ["እልፍ", "አእላፍ", "አእላፋት", "ትእልፊት", "ትእልፊታት", "ትእልፊታተ ትእልፊት", "ትእልፊታተ ትእልፊታት", "ምእልፊት", "ምእልፊታት",
           "ምእልፊታተ ምእልፊት", "ምእልፊታተ ምእልፊታት", "እልፈ አእላፋት ወትእልፊተ ትእልፊታት", "እልፈ አእላፋት ወምእልፊተ ምእልፊታት",
           "መናዝል", "መናዝላት", "መናዝለ መናዝል", "መናዝለ መናዝላት", "መናዝላተ መናዝላት"]
E.append(entry("11", "አባ ብርሃነ ሥላሴ", "Abba Birhane Selassie",
  P("የታዕካ ነገሥት በዓታ አዲስ አበባ አገልጋይ ሲሆኑ አባ ብርሃነ ሥላሴ ሲያስተምሩ ባላያቸዉም እንደ ነገሩኝ የአቡሻሕር መምህር ናቸዉ፡፡ በቀጠሮ ጥቅምት 28 ቀን 2001 ዓ. ም. በ10 ሰዓት ተገናኘን፡ የነገሩኝን የእልፍ ዕድገት የሚከተለው ነው፡፡",
    "Abba Birhane Selassie serves at Ta’eka Negest Be’ata in Addis Ababa. Though I have not seen him teach, he told me that he is a teacher of Abushakir. We met by appointment on Tiqimt 28, 2001 E.C., at ten o’clock (Ethiopian time). The progression of እልፍ that he gave me is as follows:")
  + '<ol class="namelist">' + "".join(f"<li>{n}</li>" for n in names11) + "</ol>"
  + P("ካሉ በኋላ ከዚህ በላይ ሰው የሚያው ቍጥር የለም ብለዋል፡፡ በመቀጠል በአኀዝ ያመለከቱት ቀጥሎ ተመልክቶአል፡፡",
      "Having said these, he stated that there is no number beyond this that a person can know. What he then showed in numerals is given below.")
  + table(["akh", "gz"], [["፼", "ዐሥር ሺሕ"], ["፻፼", "አእላፍ"], ["፻፼፼", "አእላፋት"], ["፻፼፼፼", "ትእልፊት"]])
  + P("ይህም ከመጀመርያዉ በሥርዓቱ አልጀመረም፡፡", "This, too, does not begin in proper order from the first.", "verdict")
  + P("የአባ ብርሃነ ሥላሴ ውሳኔ ተመልክተናል፡፡ የሁን እንጂ ይህ ሁሉ ድርድር ነው፡ ይዘትን አያመለክትም፡፡ ለጥናት ግን መሠረታዊ መነሻ ሊሆን ይችላል፡፡",
      "We have seen Abba Birhane Selassie’s conclusion. All of this, however, is a sequence of names; it does not show content. Still, it can serve as a basic starting point for study.")))

E.append(entry("12", "የሊቃውንት ጉባዔ", "The Council of Scholars (Liqawint Gubae)",
  P("የኢትዮጵያ ተዋሕዶ ጠቅላይ ቤተ ክህነት አዲስ አበባ፡ የሊቃውንት ጉባዔ፡ በ04 01 2001 ዓ. ም. በተደረገው ሁለተኛው ቀን ቀጣይ ስብሰባ፡ በዚህ ቀን ይህነንን የእልፍ አቀማመጥ ሥርዓትን አመልክቶአል፡፡",
    "At the second day of its continued meeting, on 04/01/2001 E.C., the Council of Scholars of the Ethiopian Tewahedo Patriarchate in Addis Ababa set out the following order for the placement of እልፍ:")
  + table(["akh", "gz"], [["፼", "እልፍ"], ["፼፼", "አእላፍ"], ["፼፼፼", "አእላፋት"], ["፼፼፼፼", "ትእልፊት"], ["፼፼፼፼፼", "ትእልፊታት"],
                          ["፼፼፼፼፼፼", "ምእልፊት"], ["፼፼፼፼፼፼፼", "ምእልፊታት"]])
  + P("ይህ ምእልፊታት ወደ ዘመናዊ የማባዛት ስሌት ሲለወጥ፡ 10000 × 10000 × 10000 × 10000 × 10000 × 10000 × 10000 ይሆናል፡፡ ተደጋገሚ ጥናት ቢከሃኄድበት በሁሉም መንገድ ሊያሠራ የሚችል የተሟላ ዕድገት ይኖረዋል ብሎአል የሊቃውንት ጉባዔ፡፡",
      "Converted to modern multiplication, this ምእልፊታት becomes 10000 × 10000 × 10000 × 10000 × 10000 × 10000 × 10000. The Council stated that, with repeated study, it would have a complete progression that works in every way.")
  + P("የአኀዝ ቁጥሩን ሥርዓት በማሳጠር ትክክለኛ ሕጉን ጠብቆአል፡፡ በዐሥር በዐሥር የሚያድገው ሥርዓትንም የጠበቀ ነው፡፡ ፍቹ ግን የአለቃ ኪዳነ ወልድ ሥርዓትን የተከተለ እንጂ መሠረታዊዉን አልተከተለም፡፡ ምክንያቱም ሦስቱን የቁጥር ሕጎችን አላሙዋላምና ነው፡፡",
      "By abbreviating the numeral system it keeps the correct rule, and it preserves growth by tens. Its reading, however, follows the system of Aleqa Kidane Wold rather than the fundamental one — for it does not fulfil the three laws of number.", "verdict")))

BK = [("፩", "፩", "አንድ", "1"), ("፲", "፩የ", "ዐሥር", "10"), ("፻", "፩የየ", "አንድ መቶ", "100"), ("፲፻", "፩የየየ", "አንድ ሺሕ", "1,000"),
      ("፩፼", "፩፡የየየየ", "አንድ እልፍ", "10,000"), ("፲፼", "፩የ፡የየየየ", "ዐሥር እልፍ", "100,000"), ("፻፼", "፩የየ፡የየየየ", "አንድ መቶ እልፍ", "1,000,000"),
      ("፲፻፼", "፩የየየ፡የየየየ", "አንድ ሺሕ እልፍ", "10,000,000"),
      ("፩፼፼", "፩፡የየየየ፡የየየየ", "አንድ አእላፍ", "100,000,000"), ("፲፼፼", "፩የ፡የየየየ፡የየየየ", "ዐሥር አእላፍ", "1,000,000,000"),
      ("፻፼፼", "፩የየ፡የየየየ፡የየየየ", "አንድ መቶ አእላፍ", "10,000,000,000"), ("፲፻፼፼", "፩የየየ፡የየየየ፡የየየየ", "አንድ ሺሕ አእላፍ", "100,000,000,000"),
      ("፩፼፼፼", "፩፡የየየየ፡የየየየ፡የየየየ", "አንድ አእላፋት", "1,000,000,000,000"), ("፲፼፼፼", "፩የ፡የየየየ፡የየየየ፡የየየየ", "ዐሥር አእላፋት", "10,000,000,000,000"),
      ("፻፼፼፼", "፩የየ፡የየየየ፡የየየየ፡የየየየ", "አንድ መቶ አእላፋት", "100,000,000,000,000"),
      ("፲፻፼፼፼", "፩የየየ፡የየየየ፡የየየየ፡የየየየ", "አንድ ሺሕ አእላፋት", "1,000,000,000,000,000"),
      ("፩፼፼፼፼", "፩፡የየየየ፡የየየየ፡የየየየ፡የየየየ", "አንድ እልፋት", "10,000,000,000,000,000")]
E.append(entry("13", "መ. ይትባረክ ገሠሠ", "Memhir Yitbarek Gessese",
  P("እኔ ራሴ ይትባረክ ገሠሠ፡ ሰዋስወ ቀመር 2001፡ ባሕረ ቀመር 2003ና ባሕረ ቀመር ሁለተኛ 2004 ዓ. ም.",
    "I myself, Yitbarek Gessese: <i>Sewasewe Kemer</i> (2001), <i>Bahre Kemer</i> (2003) and <i>Bahre Kemer, Volume Two</i> (2004 E.C.).")
  + table(["akh", "bk", "am", "ar"], [list(r) for r in BK], groups={4, 8, 12, 16})
  + P("አንድ እልፋት ወይም ቴን ክዋድሪሊየን (Ten quadrillion)፡ ከትሪሊየን ቀጥሎ ማለት ነው፡፡ ፩፼፼፼፼፡ ይህ ማለት አንድ እልፋት ነው፡፡ በተጨማሪ ባሕረ ቀመር ገጽ 8 በሕረ ቀመር ሁለተኛ ገጽ 61 ተመልከት፡፡",
      "One elfat — ten quadrillion — the order that follows the trillions. ፩፼፼፼፼ means one elfat. See also <i>Bahre Kemer</i>, p. 8, and <i>Bahre Kemer, Volume Two</i>, p. 61.")
  + P("የቁጥሩ መሠረት ከሆኑ ዐሠራ ሦስት ንዑሳን መራኁት ከሚባሉ የመጀመርያዎች 4ቱ እነዚህ ናቸዉ፡፡ በተጨማሪ ባሕረ ቀመር፡ 2003 ዓ. ም. ገጽ 8 እና 180፡ ባሕረ ቀመር ሁለተኛ 2004 ዓ. ም. ገጽ 61 ተመልከት፡፡ ከ16280000 ድርድር (ዲጂትስ) ውስጥ ዘርፍ ካልሆነ በቀር የቁጥርም ይሁን የፊች አንዲት ቃል የተደገመች አትገኝም፡፡ የቁጥሩ ሕግም በሁለት ዘዴ ማመሳከር እንደ ሚቻል ተገልጾአል፡፡",
      "These are the first four of the thirteen <i>ne’usan merakhut</i> (“minor keys”) on which the number system is founded. See also <i>Bahre Kemer</i> (2003 E.C.), pp. 8 and 180, and <i>Bahre Kemer, Volume Two</i> (2004 E.C.), p. 61. Across 16,280,000 digits, apart from the branch markers, not a single word — of numeral or of reading — is repeated. It has also been shown that the rules of the system can be verified by two methods.")
  + P("ከላይ ከዓራቱ አምዶች ሁለተኛው በግዕዝ የተነበበው ሁሉንም የኢትዮጵያ ቋንቋዎች ይወክላል፡፡ ይህ በዐሥር በዐሥር ያደገና በቅኔ ቤት ርባታ ሕግ የተመሠረተ ሦስቱን የቁጥር ሕጎችን አሙዋልቶ የተመሠረተ ነው፡፡",
      "Of the four columns above, the second — read in Ge’ez — represents all the languages of Ethiopia. This system grows by tens, rests on the rules of conjugation (<i>rubata</i>) of the Qene school, and fulfils the three laws of number.", "verdict")))

parts.append('<div class="num-entries">\n' + "\n".join(E) + "\n</div>")

parts.append(f'''<article class="prose num-close">
{P("የራሳችንን ቊጥር ሳናስተካክል የፈረንጁን ቊጥር ማስተካከል እንችላለን፡፡ ከዚህም በላይ እንደ ምናየው ከአንድ ቦታ በስተቀር የዓረቢክ ቊጥሩ ልክ ነው፡፡ የፈረንጁን ሥርዓት ይዞ ተደርድሮአል፡፡ ወደ እኛ የአኀዝ ቊጥርና ወደ ግዕዙ ስንገባ ግን ዕንግዶች መሆናችንን ሥራችን ያረጋግጥልናል ያጋልጠናል፡፡ ይህ ብቻም አይደለም የአብዛኛዎቹ በዚሁ መልክ የተሠራ ነው፡፡ በስሕተቱም ቢስማሙኮ መልካም ነበር፡፡ ያለው ችግር በስሕተቱም አይስማሙም፡፡ በጣም የሚያሳዝነው ግን ተተኪ ትውልድ በአንድ ሃገራዊ የቊትር አቅጣጫ ተመሥርቶ ምርምሩን እንዳያሳድግ በየጓዳው ድሪቶና አምቡላ የሚመስል ኮተት እየቆለሉ አቅጣጫን ማሳጣታቸዉን ነው፡፡ በጠላት ይሁን ባለ ማወቅ የነበረው ነባር የቁጥር ዕድገት ጠፍቶአል፡፡ አሁን በዚሁ መነሻነት ጥናታችንነን መቀጠለል ይገባል እንጂ ከፍተኛ የቁጥር ይዘት በኢትዮጵያ አልነበረም ብሎ መደምደም ግን በጣም የሚከብድ ነው፡፡",
   "We are able to set the foreigners’ numbers in order without having set our own in order. As we see above, the Arabic numerals are correct except in one place; they are arranged following the foreign system. But when we come to our own numerals and to the Ge’ez, our work confirms — and exposes — that we are strangers to them. Nor is this an isolated case: most of the works were made the same way. It would have been something had they at least agreed in their errors; the trouble is that they do not agree even in those. Saddest of all, by heaping up clutter like rags and dregs in every back room, they leave the next generation without direction — unable to ground itself in a single national approach to number and so advance its research. Whether through enemies or through ignorance, the old, established progression of numbers has been lost. We must now continue our study from this starting point; to conclude that Ethiopia never possessed a higher system of numbers would be a grave thing indeed.")}
<h2>{T("ለሚመለከተው", "To Whom It May Concern")}</h2>
{P("መጽሐፋቸዉን ያገኘሁት ደራሲያን ከዚህ በላይ ሰፍሮአል፡፡ ስለ አኀዝ ቊጥር የተጻፉት መጻሕፍት እነዚህ ብቻ ላይሆኑ ይችላሉ፡፡ ይሁን እንጂ ቢኖሩም ከእነዚህ ጸሐፊያን የተለየ ሐሣብና አቀራረብ ይሆናል ተብሎ ግን አይገመትም፡፡",
   "The authors whose books I was able to obtain are listed above. These may not be the only books written on the numerals; but if others exist, they are not expected to offer ideas or approaches different from these writers’.")}
{P("አኀዝ ቊጥር ሃገራዊ ቅርስ እንደ መሆኑ መጠን፡ መንግሥታዊም ይሁን ግለኛ ድርጅት ያገባኛል የሚል አካል ካለ፡ ስለአኀዝ ቊጥር የጻፉትንና ያገባኛል የሚሉት ኢትዮጵያዊያንን ሁሉ አሰባስቦና አገናኝቶ ለመጨመርም ሆነ ለማጥናት ወይም ለመወሰን የሆነ ኮንፈረንስ ሊያዘጋጅ እንዲገባ ጥሬን አቀርባለሁ፡፡",
   "As the Ge’ez numerals are a national heritage, I call on any body — governmental or private — that considers this its concern to gather all Ethiopians who have written on the numerals, or who hold the matter to be their concern, and to convene a conference to extend, study or decide upon them.")}
{P("ይህን መልእክት ያነበባችሁ፡ ኢትዮጵያዊነትን ለሚቀበል ሁሉ መልእክቱን ታስተላልፉ ዘንድ በክብርና በትሕትና ትጠየቃላችሁ፡፡",
   "You who have read this message are respectfully and humbly asked to pass it on to all who embrace their Ethiopian identity.")}
<p class="num-seal">( ፫-፼ ፩፼፼፼ ፲ወ፱፻፶ወ፭፼፳ወ፪)</p>
</article>''')

open(OUT, "w", encoding="utf-8").write("<!-- Generated: edit freely, or regenerate from gen_numbers.py -->\n" + "\n\n".join(parts) + "\n")
print("wrote", OUT)
