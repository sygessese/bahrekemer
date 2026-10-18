import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "key.html")
def T(am, en): return f'<span lang="am">{am}</span><span lang="en">{en}</span>'
def P(am, en, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<p lang="am"{c}>{am}</p>\n<p lang="en"{c}>{en}</p>\n'
H = {"n": ("#", "#"), "akh": ("አኀዝ", "Numeral"), "gz": ("ስም", "Name"), "am": ("አማርኛ", "Amharic"), "ar": ("ዓረቢክ", "Arabic"),
     "bk": ("ባሕረ ቀመር", "Bahre Kemer"), "code": ("ኮድ", "Code"), "rd": ("ንባብ", "Reading")}
GLOSS = {"አንድ": "one", "ዐሥር": "ten", "አንድ መቶ": "one hundred", "አንድ ሺሕ": "one thousand", "አንድ እልፋት": "one elfat",
         "ዐሥርቱ እልፍ": "ten elf", "ዐሥር መቶ እልፍ": "ten hundred elf", "አእላፍ": "a’elaf"}
for unit, tr in [("እልፍ", "elf"), ("አእላፍ", "a’elaf"), ("አእላፋት", "a’elafat")]:
    for a, e in [("አንድ", "one"), ("ዐሥር", "ten"), ("አንድ መቶ", "one hundred"), ("አንድ ሺሕ", "one thousand")]:
        GLOSS[f"{a} {unit}"] = f"{e} {tr}"
def table(cols, rows, groups=None):
    head = "".join(f'<th class="c-{c}">{T(*H[c])}</th>' for c in cols)
    body = ""
    for i, r in enumerate(rows):
        cls = ' class="group-start"' if groups and i in groups else ""
        cells = "".join(f'<td class="c-{c}">{T(v, GLOSS.get(v, v)) if c in ("am", "rd") else v}</td>' for c, v in zip(cols, r))
        body += f"<tr{cls}>{cells}</tr>"
    return f'<div class="table-wrap"><table class="numtable"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>\n'
def OL(items, cls="labeled"):  # items: (label_am, label_en, am, en)
    lis = "".join(f'<li><span class="lbl">{T(la, le)}</span><span class="li-body">{T(a, e)}</span></li>' for la, le, a, e in items)
    return f'<ol class="{cls}">{lis}</ol>\n'
def H3(am, en): return f"<h3>{T(am, en)}</h3>\n"

BK = [("፩", "አንድ", "1"), ("፩የ", "ዐሥር", "10"), ("፩የየ", "አንድ መቶ", "100"), ("፩የየየ", "አንድ ሺሕ", "1,000"),
      ("፩፡የየየየ", "አንድ እልፍ", "10,000"), ("፩የ፡የየየየ", "ዐሥር እልፍ", "100,000"), ("፩የየ፡የየየየ", "አንድ መቶ እልፍ", "1,000,000"), ("፩የየየ፡የየየየ", "አንድ ሺሕ እልፍ", "10,000,000"),
      ("፩፡የየየየ፡የየየየ", "አንድ አእላፍ", "100,000,000"), ("፩የ፡የየየየ፡የየየየ", "ዐሥር አእላፍ", "1,000,000,000"), ("፩የየ፡የየየየ፡የየየየ", "አንድ መቶ አእላፍ", "10,000,000,000"), ("፩የየየ፡የየየየ፡የየየየ", "አንድ ሺሕ አእላፍ", "100,000,000,000"),
      ("፩፡የየየየ፡የየየየ፡የየየየ", "አንድ አእላፋት", "1,000,000,000,000"), ("፩የ፡የየየየ፡የየየየ፡የየየየ", "ዐሥር አእላፋት", "10,000,000,000,000"), ("፩የየ፡የየየየ፡የየየየ፡የየየየ", "አንድ መቶ አእላፋት", "100,000,000,000,000"), ("፩የየየ፡የየየየ፡የየየየ፡የየየየ", "አንድ ሺሕ አእላፋት", "1,000,000,000,000,000"),
      ("፩፡የየየየ፡የየየየ፡የየየየ፡የየየየ", "አንድ እልፋት", "10,000,000,000,000,000")]

S = []  # (id, am, en, html)
S.append(("explanation", "መግለጫ", "Explanation",
  P("የባሕረ ቀመር የሒሣብ ቊጥር መጽሐፍ በጠቅላላ ይዘቱን ከማቅረባችን በፊት ለመግቢያ ይጠቅማሉ የተባሉ ነጥቦችን ለማቅረብ ወደድን፡፡ እነሱም መጽሐፉን እንዴት መረዳት እንደሚችሉ በቀላሉ ሊያሳዩ የሚችሉ ናቸዉ፡፡ በተለይ ባሕረ ቀመርና ባሕረ ቀመር ሁለተኛ አብረዉ የሚኄዱ ናቸዉ፡፡ ባሕረ ቀመር፡ የባሕረ ቀመር ቁጥር መግለጫና ማብራርያ ነው፡፡ ባሕረ ቀመር ሁለተኛ አንድ ብሎ እስከ ከፍተኛ ቁጥር የቁጥሩ ዕድገትን ብቻ የሚያረጋግጥ ነው፡፡ ስለዚህ ሁለቱ በአንድ ላይ ቢኖሩ ይመከራል፡፡",
    "Before presenting the full contents of the Bahre Kemer books on number and calculation, we wished to set out some points that serve as an introduction; they show simply how the books can be understood. <i>Bahre Kemer</i> and <i>Bahre Kemer, Volume Two</i> in particular go together: <i>Bahre Kemer</i> describes and explains the Bahre Kemer numbers, while <i>Volume Two</i> sets out only their growth, from one up to the highest. It is therefore recommended to have the two together.")
  + P("ለምሳሌ፡ ከባሕረ ቀመር ሁለተኛ — ዓቢይ ክፍል ሦስተኛ፡ ገጽ 61", "For example, from <i>Bahre Kemer, Volume Two</i> — Part Three, p. 61:", "label")
  + table(["n", "akh", "gz", "code"], [["1", "፩-፼", "እልፍ", "1-4-0"], ["2", "፪-፼", "አእላፍ", "2-8-0"], ["፫", "፫-፼", "አእላፋት", "3-12-0"]])
  + P("እንደዚህ ተጽፎ ይገኛል፡፡ ሰፊ ማብራርያ ያለው ግን ከባሕረ ቀመር ውስጥ ነው፡፡", "It is written there in this form; the full explanation is in <i>Bahre Kemer</i>.")
  + P("ከዚህ ላይ ይህ ፫-፼፡ ሦስት እልፍ ነው ማለት አይደለም፡፡ ሦስት የ፼ ቅርፅ ማለት ነው እንጂ፡፡ ለምሳሌ፡ ፩፼፼፼ ይህ ማለት ነው፡፡ በባሕረ ቀመር ሲጻፍ ፩፡የየየየ፡የየየየ፡የየየየ (አንድ አእላፋት ነው)፡፡ ፫-፼ = ፩፼፼፼፡፡ ይሆናል አንድ አእላፋት፡፡ በባሕረ ቀመርና በዓረቢክ ቁጥር ሲወዳደር እንደ ሚከተለው ነው፡፡",
      "Here, ፫-፼ does not mean “three elf.” It means three of the form ፼ — that is, ፩፼፼፼. Written in Bahre Kemer it is ፩፡የየየየ፡የየየየ፡የየየየ (one a’elafat). So ፫-፼ = ፩፼፼፼: one a’elafat. Compared in Bahre Kemer and Arabic numerals, it is as follows:")
  + OL([("1", "1", "፩-፼ = ፩፡የየየየ — አንድ እልፍ ወይም 1-4-0፡ 1 × 4 = 4፡፡ 1ና 4 ዚሮ = ዓሥር ሺሕ (10,000) ነው፡፡",
         "፩-፼ = ፩፡የየየየ — one elf, or 1-4-0: 1 × 4 = 4; a 1 followed by 4 zeros = ten thousand (10,000)."),
        ("2", "2", "፪-፼ = ፩፡የየየየ የየየየ — አንድ አእላፍ ወይም 2-4-0፡ 2 × 4 = 8፡፡ 1ና 8 ዚሮ = መቶ ሚሊየን (100,000,000)",
         "፪-፼ = ፩፡የየየየ የየየየ — one a’elaf, or 2-4-0: 2 × 4 = 8; a 1 followed by 8 zeros = one hundred million (100,000,000)."),
        ("3", "3", "፫-፼ = ፩፡የየየየ የየየየ የየየየ — አንድ አእላፋት ወይም 3-4-0፡ 3 × 4 = 12፡፡ 1ና 12 ዚሮ = ትሪሊየን (1,000,000,000,000)",
         "፫-፼ = ፩፡የየየየ የየየየ የየየየ — one a’elafat, or 3-4-0: 3 × 4 = 12; a 1 followed by 12 zeros = one trillion (1,000,000,000,000).")], "labeled worked")))

S.append(("introduction", "መግቢያ", "Introduction",
  P("የመጽሐፉ ጥናት ረዘም ያለ ጊዜ ወስዶአል፡፡ የጥናቱም አጀማመር በአኀዝ ቊጥር ሒሣብ መሠራት አለበት ነበር፡፡ በፅንሰ ሐሣቡ መሠረት ለሒሣብ ተዘጋጅቶአል፡፡ በተጨማሪ ነባር የአኀዝ ቊጥርን አሳጥሮ ይተረጒማል፡፡ ከፍተኛ የቊጥር ዕድገትንም አመልክቶአል፡፡ በዓለማችን የነበሩና ያሉ ከ፩የየ (100) በላይ ቊጥሮችና የቊጥር ፊደላት ቀርበዋል፡፡ ስለ መጽሐፉ ከ40 በላይ የአብነት መምህራን አስተያየት ሰጥተዉበታል፡፡ በመጨረሻ አሁን 5 መጻሕፍት ታትመዉ ለንባብ ቀርበዋል፡፡",
    "The study behind the book took a long time. It began from the conviction that it must be possible to calculate with the Ge’ez numerals, and in keeping with that idea the system has been prepared for calculation. It also interprets the traditional numerals in abbreviated form, and sets out a far higher growth of numbers. More than ፩የየ (100) numeral systems and numeral alphabets from around the world, past and present, are presented. More than forty traditional (<i>abinet</i>) teachers have given their views on the book. Five books have now been published and are available to readers.")))

S.append(("five-books", "ሰዋስወ ቀመር", "Sewasewe Kemer",
  P("የተዘጋጁ የ5 መጻሕፍት ስም፡ ኪነ ጥበብና ሥነ ጥበብ፡ ሰዋስወ ቀመር፡ ባሕረ ቀመር፡ ባሕረ ቀመር ሁለተኛና ባሕረ ቀመር የሒሣብ መልመጃ ናቸዉ፡፡ ፅንሰ ሐሣቡ የተጠነሰሰው በ1963 ዓ. ም. ነው፡፡ በኢንፎርሜሽን እጥረት፡ በኤኮኖሚና በልዩ ልዩ ምክንያት ጥናቱን በአጭር ጊዜ አጠናቅቆ ለማቀረብ ባይቻልም በ1986 ዓ. ም. ኪነ ጥበብና ሥነ ጥበብ፡ የአኀዝ መዝገበ ቊጥር፡ ከነባር እስከ ምርምር በሚል ሥያሜ የመጀመርያ እትሙ ለንባብ ቀርቦአል፡፡",
    "The five books prepared are <i>Kine Tibeb and Sine Tibeb</i>, <i>Sewasewe Kemer</i>, <i>Bahre Kemer</i>, <i>Bahre Kemer, Volume Two</i> and <i>Bahre Kemer Arithmetic Exercises</i>. The idea was conceived in 1963 E.C. Though lack of information, economic constraints and various other reasons kept the study from being completed quickly, its first edition was published in 1986 E.C. under the title <i>Kine Tibeb and Sine Tibeb: A Register of Ge’ez Numerals, from Tradition to Research</i>.")))

S.append(("three-findings", "የቊጥሩ ጥናት 3 ነገሮችን አስገኝቶአል", "Three Findings of the Study",
  P("ከግዕዝ መጻሕፍት ውስጥ የሚገኙ ነባር የአኀዝ ቊጥር ዐቅም የፈቀደውን ያህል ለማጥናት ተሞክሮአል፡፡ የጥናቱ ውጤትም ሦስት ግኝቶችን አስገኝቶአል፡፡",
    "The traditional numerals found in Ge’ez books have been studied as far as means allowed, and the study has produced three findings:")
  + OL([("1", "1", "አኀዝ ቁጥራችን ሙሉ ቁጥር አይደለም ሲባል የነበረውን ሙሉ ቁጥር እንደ ነበር በጥናት ተረጋግጦአል፡፤ ፻ አልቦ ወይም ዚሮ እንደ ነበር አረጋግጦአል፡",
         "Our numerals, long said not to be a complete number system, have been shown by study to have been complete: it has established that ፻ served as <i>albo</i>, or zero."),
        ("2", "2", "ከፍተኛ የቊጥር ዕድገትን አመልክቶአል፡፡", "It has set out a far higher growth of numbers."),
        ("3", "3", "ከግዕዝ መጻሕፍት ውስጥ የሚገኙ ብዙ የአኀዝ ቊጥሮችን በቀላሉ ለመተርጐም የሚያስችል ዘዴ አስገኝቶአል፡፡",
         "It has produced a method for easily interpreting the many numerals found in Ge’ez books.")])
  + P("ለምሳሌ፡ ፲ወ፱፻፶ወ፭፼፳ወ፪ ይሆናል = ፩፱፭፭፡የየ፪፪ — አንድ ሺሕ ዘጠኝ መቶ ሃምሣ አምስት እልፍ፡ ሃያ ሁለት ነው፡፡ 19,550,022 ነው፡፡",
      "For example: ፲ወ፱፻፶ወ፭፼፳ወ፪ = ፩፱፭፭፡የየ፪፪ — one thousand nine hundred fifty-five elf and twenty-two; that is, 19,550,022.", "example")))

S.append(("one-to-nine", "ከ፩ እስከ ፱ ሒሣብ ያሠራል", "Calculating with ፩ to ፱",
  P("ከነባር ቊጥር ከ፩ እሰከ ፱ ባሉ ቊጥሮች በመቶ አልቦነት ያለ ምንም ችግር በቀላሉ ሒሣብ የሚሠራበትን ዘዴ አስገኝቶአል፡፡ ሰዋስወ ቀመር ገጽ 108 እና 148 ተመልከት፡፡ እንደዚሁም ከፍተኛ የቊጥር ዕድገትን አመልክቶአል፡፡ ከገጽ 226 ጀምሮ ተመልከት፡፡ ዐቅም የፈቀደውን ያህል በዓለማችን ውስጥ የነበሩና ያሉ ቊጥሮችን ለማቅረብ ተሞክሮአል፡፡ ከ100 በላይ የዓለም ፊደልና የቊጥር ዓይነቶችም ከመጽሐፉ ገጽ ሰፍረዋል፡፡",
    "Using the traditional digits ፩ to ፱, with ፻ serving as <i>albo</i> (zero), the study has produced a method for calculating easily and without difficulty — see <i>Sewasewe Kemer</i>, pp. 108 and 148. It likewise sets out a far higher growth of numbers — see from p. 226 on. As far as means allowed, it presents the number systems of the world, past and present: more than 100 of the world’s alphabets and numeral systems appear in the book’s pages.")))

S.append(("hindu-arabic", "የሂንዱ ዓረቢክና የኛ ቊጥር", "Hindu-Arabic Numerals and Ours",
  P("ከ778-850 ዓ. ም. የነበረ ሙሐመድ ጃፋር አል ክሕዋርዝሚ የተባለ የሴንትራል ኤሺያ ተወላጅ ያገኘውን ዚሮ (0) በመጀመርያ ዚሮዉ ዐሥረኛ ቊጥር የነበረ ሲሆን የኛ አልቦ ግን መቶኛ መሆኑን ጥናቱ አመልክቶአል፡፡ የተለያየ ባህላዊ የሒሣብ ቊጥር ከነበራቸዉና ካላቸዉ ነባር ሃገራት፡ ለምሳሌ፡ ሕንድ፡ ግብጽ ቻይና፡ ደቡብ አሜሪካና የመሳሰሉት ይገኙበታል፡፡ ሰዋስወ ቀመር ገጽ 67 እና ባሕረ ቀመር 94 ጀምሮ ተመልከት ፡፡",
    "The study shows that the zero (0) found by Muhammad Jafar al-Khwarizmi, a native of Central Asia who lived from 778 to 850, was at first the tenth digit, whereas our <i>albo</i> is the hundredth. Among the ancient nations that had, and have, their own traditional numerals for calculation are India, Egypt, China, South America and others. See <i>Sewasewe Kemer</i>, p. 67, and <i>Bahre Kemer</i> from p. 94.")))

S.append(("elf", "የእልፍ ቅጽልነት", "Elf as a Qualifier",
  P("በግዕዝ መጻሕፍት ውስጥ የእልፍን ቅጽልነት አቀራረብና አገላለጽ የሚያሳዩ ሲሆን ከ200 በላይ የሚሆኑ የእልፍ ጥቅሶች ከግዕዝ መጻሕፍት ተለቅመዉ ቀርበዋል፡፡ በተለይ ሰዋስወ ቀመር የተባለዉ መጽሐፍ፡ በሦስት ዓበይት ክፍል የተከፈለ ሲሆን፡ እንዲሁም በዓበይቱ ክፍላት ውስት 22 ምዕራፎችና 1027 ሠራዊት አካትቶአል፡፡",
    "More than 200 citations of እልፍ, gathered from Ge’ez books, are presented to show how <i>elf</i> is used and expressed as a qualifier there. <i>Sewasewe Kemer</i> in particular is divided into three main parts, which together contain 22 chapters and 1,027 sections.")))

S.append(("why-groups", "ለምን አነሰ ወይም በዛ ለሚሉ", "For Those Who Ask Why Fewer or More",
  P("የኛና የሂንዱ ዓረቢክ ቊጥር የደረጃ ዕድገት ለማረጋገጥ መመጠኛውን እንመልከት፡፡ የዕድገቱ ደረጃ ሲወዳደር ለምን በዐራት ደረጃ ተከፈለ? ወይም ለምን በሦስት ደረጃ ተከፈለ? ለሚሉ፡",
    "To confirm how our numerals and the Hindu-Arabic numerals grow by place, let us look at the measure — for those who ask, when the stages of growth are compared, why one is divided into groups of four, and the other into groups of three:")
  + H3("በባሕረ ቀመር ሕግ ሲወዳደር", "Compared by the Rule of Bahre Kemer")
  + table(["bk", "am", "ar"], [list(r) for r in BK], groups={4, 8, 12, 16})
  + P("አንድ እልፋት ወይም ቴን ክዋድሪሊየን (Ten quadrillion)፡ ከትሪሊየን ቀጥሎ ማለት ነው፡፡ ፩፼፼፼፼፡ ይህ ማለት አንድ እልፋት ነው፡፡ በተጨማሪ ባሕረ ቀመር ገጽ 8 ባሕረ ቀመር ሁለተኛ ገጽ 61 ተመልከት፡፡",
      "One elfat — ten quadrillion — the order that follows the trillions. ፩፼፼፼፼ means one elfat. See also <i>Bahre Kemer</i>, p. 8, and <i>Bahre Kemer, Volume Two</i>, p. 61.")))

S.append(("why-differ", "ለምን ተለየ", "Why They Differ",
  P("የዓረቢክ ቊጥር ሕግ በ3 ደረጃ በአንድ 1000 መድረሻ ይከፍላል፡፡ የኛ ቊጥር ግን በዐራት ደረጃ በእልፍ መድረሻ ይከፍላል፡፡ የኛ ቊጥር በዐራት ምድብ ስለ ሚከፈልና የዓረብ ቊጥር በ3ት ደረጃ ወይም ምድብ ስለ ሚከፍል የዓረብ ቊጥር በየክፍሉ አንድ ደረጃ እንዲያን እንዲቀንስ አድርጎታል፡፡",
    "The rule of Arabic numerals groups digits in threes, with 1,000 as the boundary; ours groups them in fours, with the <i>elf</i> as the boundary. Because ours is divided into groups of four and the Arabic into groups of three, the Arabic falls one place short in each group.")))

S.append(("grouping", "አከፋፈል", "Grouping",
  P("የኛ ቊጥር ወደታች በዐራት ደረጃ ስለ ተከፈለ ወደ ግድምም በዓራት ደረጃ እንዲከፍል የቊጥሩ ሥርዓት ያመለክታል፡፡ የዓረቢክ ቊጥር ሕግ 1,000 እንደዚህ በሦስት ቦታ (ዲጂትስ) የሚከፍል ሲሆን፡ የኛ ግን ፩፡የየየየ እንደዚህ በዐራት ቦታ እንዲከፍል የቊጥሩ ሥርዓት ያመለክታል፡፡ ከዚህ የቊጥሩ ሕግ ሌላ፡ ቅርፅን፡ ድምፅንና ይዘትን ሳይመጥኑ ዝምብሎ ቅርፅን ብቻ መቆለል በምንም መልኩ ቊጥር ሊባል አይችልም፡፡",
    "Because our numbers are grouped in fours down the column, the system indicates that they should be grouped in fours across the row as well. The rule of Arabic numerals separates digits in threes, like 1,000; ours, the system indicates, separates them in fours, like ፩፡የየየየ. Outside this rule, merely piling up forms — without matching form, sound and content — cannot in any way be called a number.")))

S.append(("what-is-a-number", "ቊጥር ለመሆን", "What Makes a Number",
  P("አንድ ቊጥር፡ ቊጥር ለመሆን ሦስት ነገሮችን ሟሟላት አለበት፡፡ እነሱም ቅርፅ፡ ድምፅና ይዘት ናቸዉ፡፡ የቊጥሩ ሕግ ሰፋ ባለ ሁኔታ ተብራርቶአል፡፡ ለምሳሌ፡ አንድ መቶውን ፻ (ዐሥር) ሲከተለው፡ ዐሥርን ዐሥር መቶ ሲከተለው፡ እልፍን ዐሥር መቶ ሲከተለውና… የመሰለውን የሚያመለክት ሰፋ ባለ ይዘት ቀርቦአል፡፡ ሰዋስወ ቀመር ገጽ 190 እስከ 203፡ ባሕረ ቀመር 130 እስከ 143 ተመልከት፡፡",
    "For a number to be a number, it must fulfil three things: form, sound and content. The rules of the system are explained at length — for instance, how ፻ (ten) follows one hundred, how ten hundred follows ten, how ten hundred follows <i>elf</i>, and so on. See <i>Sewasewe Kemer</i>, pp. 190–203, and <i>Bahre Kemer</i>, pp. 130–143.")))

S.append(("multipliers", "አብዢ እንጂ ቊጥር አይደሉም", "Multipliers, Not Numbers",
  P("፻ ፼ ፼፼ ፼፼፼……የእነዚህ ቅርፆች ወይም ዋየሎች በአልቦነት አብዢ ይሆናሉ እንጂ የቊጥር ይዘት እንደ ሌላቸዉም የሚያረጋግጥ ሰፊ ማብራርያ ቀርቦአል፡፡ መቶ አልቦ መሆኑ ከማስረጃዎች አንዱ ይህ ነው፡፡ ቁጥር ሲሆኑ እንደ ሚከተለው ይጻፋሉ፡ ፩፻ ፩፼ ፩፼፼ ፩፼፼፼ ነው፡፡ የብርቲሽ፡ የአሜሪካና የኛ ሥርዓተ ነጥብ ተወራራሽ እንደ መሆኑ መጠን በራሳችን ሥርዓተ ነጥብ መገልገል እንደ ምንችል ያመለክታል፡፡",
    "A full explanation is given showing that these forms — ፻ ፼ ፼፼ ፼፼፼ …, the <i>wayel</i> — act as multipliers through their role as <i>albo</i> (zero), and have no numerical content of their own. This is one of the proofs that ፻ is <i>albo</i>. To become numbers they are written thus: ፩፻ ፩፼ ፩፼፼ ፩፼፼፼. And since British, American and our own systems of punctuation are interrelated, it shows that we can use our own punctuation.")))

S.append(("one-form", "አንድ ቅርፅ ሁለት አካል", "One Form, Two Parts",
  P("ከዐሥር እስከ ዘጠና ያሉ ቊጥሮች አንድ ቅርፅ ሁለት አካል (ሁለት ቤት) መሆናቸዉን መገንዘብ ያስፈልጋል፡፡ ማለት በዓይን ቅርፃቸዉን ስንመለከት አንድ ወጥ አንድ ቅርፅ ነው፡፡ በውስጣዊ የአእምሮ ዓይናችን ስንመለከታቸዉ ወይም ስንመዝናቸዉ ግን ሁለት አካል ወይም ሁለት ቤት መሆናቸዉን እንረዳለን፡፡ ከዐሥር እስከ ዘጠና ያሉ ቊጥሮች ማለት ነው፡፡ እነሱም በሒሣብ ጊዜ ከዐሥር ወደ አንድ ከሃያ ወደ ሁለት....እያልን እስከ ዘጠና ይቀየራሉ፡፡",
    "It must be understood that the numerals from ten to ninety are one form with two parts (two places). To the eye, each is a single, unified form; but when we look at them, or weigh them, with the inner eye of the mind, we see that they are two parts — two places. This holds for every numeral from ten to ninety. In calculation they are converted: ten to one, twenty to two … and so on up to ninety.")))

S.append(("in-calculation", "የሒሣብ አገልግሎት", "In Use for Calculation",
  P("የሒሣብ ቊጥር ሆነዉ ለማገልገል ከሁለት አካል ይዘታቸዉ ወደ አንድ አካል እንቀይራቸዉ አለን፡፡ ከዐሥር ወደ አንድ…ከሃያ ወደ ሁለት…ከዘጠና ወደ ዘጠኝ እያለ ይቀየራል፡፡",
    "To serve as numbers for calculation, we convert them from their two-part content to a single part: ten becomes one … twenty becomes two … ninety becomes nine.")))

S.append(("origins", "የጥናቱ ፅንሰ ሐሣብ", "How the Study Began",
  P("ለብቻየ ሳወጣ ሳወርድ ስጠይቅ እንደ ነበርኩ እንዳለ ሆኖ ለኔ ጥሩ አጋጣሚ ስለ ነበር የአኀዝ ቊጥራችን በባዕድ ቊጥር እየተዋጠ ከመጥፋቱም በላይ በወጣት ኢትዮጵያን ዘንድ ከማይታወቅበት ደረጃ እንደ ደረሰ ይታወቃል፡፡ ለዚህም መድኀኒት ሊሆን የሚችል ቊጥራችን ሒሣብ ሲሠራበት ነው፡፡ ስለ ሆነም ሒሣብ ሊሠራበት የሚችልበትን ጥናት ስናደርግ ነው የሚል ሐሣብ በ1963 ዓ. ም. የግዕዝ ሊቃውንት ማኅበር ተብሎ በአዲስ አበባ ከተማ ተቋቁሞ ለነበረው ማኅበር በማስታወሻ ሐሣቤን አቅርቤ እንደ ነበር አብዛኛዎቹ በአሁኑ ጊዜ ባይኖሩም ትንሽ ከነሱ የቀሩት የማኅበሩ አባላት የነበሩ በአፅንዖት ያስታውሱታል፡፡ በወቅቱ ሙሉ ድጋፍ ባላገኝም ስለ አኀዝ ቊጥር የሚመለከቱ የግዕዝና የታሪክ መጻሕፍትን ማንበብ፡ ማስታወሻ መያዝና መከታተል የመጀመሪያ ምርጫየ ነበር፡፡",
    "I had long been turning the question over alone — weighing it, asking about it — when a good opportunity came my way. It is well known that our Ge’ez numerals, swallowed up by foreign numerals, have not only been disappearing but have reached the point where young Ethiopians no longer know them. The remedy, I believed, was for our numerals to be used in calculation, and so we had to carry out the study that would make that possible. In 1963 E.C. I presented this idea in a memorandum to the association then established in Addis Ababa as the Association of Ge’ez Scholars. Most of its members are no longer living, but the few who remain recall it emphatically. Though I did not receive full support at the time, reading, taking notes on and following the Ge’ez and historical books concerning the numerals became my first priority.")
  + P("በተለይ ከ1979 ዓ. ም. ወዲህ እንደ መደበኛ ሥራ አጥብቄ ጥናቴን ስከታተል በተፈጥሮም ይሁን በመማር ብስለትና የሃገር ፍቅር አላቸዉ ብየ የምገምታቸዉ ኢትዮጵያዊያንን ሳገኝ ጥናቴን ሳልገልጽላቸዉ አላልፍም ነበር፡፡ ወደ የመጀመሪያዉ እትም ማጠቃለያ ስቃረብ በ1986 ዓ. ም. በጎጃም፡ በጎንደር በትግራይ፡ በወሎ፡ በሐረርጌ ክፍላተ ሃገርና በአዲስ አበባ ውስጥ የሚገኙ የብሉይ ኪዳን፡ የሐዲስ ኪዳን፡ የሊቃውንት የአቡሸሕርና የቅኔ የአብነት መምህራንን አግኝቼ ስለ ኪነ ጥበብና ሥነ ጥበብ መጽሐፌ አነጋግሬያቸዉ የድጋፍ ሐሣባቸዉንና ምክራቸዉን ለግሰውኛል፡፡ ሃገራዊ ቊጥር የነበረ እንደ መሆኑ መጠን ከአዲስ አበባ ዩኒበርሲቲ ከጥናት ባለ ሙያዎች፡ እንዲሁም ከባህል ሚኒስቴር ጥናጣዊ ክፍል ምክርና ድጋፍ አግኝቼ አለሁ፡፡ በማጠቃለያው ላይ ወደ ጠቅላይ ቤተ ክህነት የሊቃውንት ጉባዔ ክፍል ኄጄ ስለ ቊጥሩ መሠረታዊ ይዘት ሰፋ ያለ ውይይት ካደረግን በኋላ ከፍ ያለ ድጋፍና መተባበር ተደርጎልኛል፡፡",
      "From 1979 E.C. especially, as I pursued the study intensively as my regular work, I never met an Ethiopian whom I judged — by nature or by learning — to have maturity and love of country without explaining my study to them. As I neared the completion of the first edition in 1986 E.C., I met traditional teachers of the Old Testament, the New Testament, the Liqawint, Abushakir and Qene in the provinces of Gojjam, Gondar, Tigray, Wollo and Hararghe and in Addis Ababa; I discussed my book <i>Kine Tibeb and Sine Tibeb</i> with them, and they gave me their support and counsel. Since this was a national system of numbers, I also received advice and support from research specialists at Addis Ababa University and from the research department of the Ministry of Culture. Finally, I went to the Council of Scholars at the Patriarchate, and after a long discussion of the fundamentals of the system I received strong support and cooperation.")
  + H3("1ኛ. መጽሐፍ፡ ኪነ ጥበብና ሥነ ጥበብ", "1. <i>Kine Tibeb and Sine Tibeb</i>")
  + P("ይህ የመጀመሪያው እትም 268 ገጽ ያለው ኪነ ጠበብና ሥነ ጥበብ የአኀዝ መዝገበ ቊጥር ከነባር እሰከ ምርምር የተባለ መጽሐፍ በቦሌ ማተሚያ ድጅት በ1986 ዓ. ም. ታተመ፡፡ ይህ መጽሐፍ የጥናቱ ሕትመት የመጀመርያ መሠረት ነው፡፡",
      "This first edition — the 268-page <i>Kine Tibeb and Sine Tibeb: A Register of Ge’ez Numerals, from Tradition to Research</i> — was printed by Bole Printing Enterprise in 1986 E.C. It is the first foundation of the study in print.")
  + H3("2ኛ. ሰዋስወ ቀመር", "2. <i>Sewasewe Kemer</i>")
  + P("አሁንም ጥናቱ ለረጅም ጊዜ ቀጥሎ ከ15 ዓመታት በኋላ 278 ገጽ ያለው ሰዋስወ ቀመር የተባለ መጽሐፍ ታተመ፡፡ ይህ መጽሐፍ የተሻለ ጥናትን ያመለክታል፡፡ በዚሁ ጊዜ በሁለተኛው ዙር በትግራይ፡ በወሎ፡ በጎንደር፡ በጎጃም፡ በሐረርጌ፡ በደቡብ ህዝብና አዲስ አበባ ውስጥ በተጠቀሱት ክልሎች በመዘዋወር በገጠርና በከተማ ያሉ ከዐርባ በላይ የሚሆኑ የአብነት ምሁራንን አነጋግሬ ሐሣባቸዉን ገልጸዋል ምክራቸዉንና ጥበባቸዉን ለግሰዋል፡፡ ከገጽ 21 እስከ 48 ከዚሁ መጽሐፍ ውስጥና ከባሕረ ቀመር ገጽ 13 መመልከት ይቻላል፡፡",
      "The study continued for a long time, and fifteen years later the 278-page <i>Sewasewe Kemer</i> was published; it reflects a more developed study. In this second round I travelled through Tigray, Wollo, Gondar, Gojjam, Hararghe, the Southern Peoples’ region and Addis Ababa, and spoke with more than forty traditional scholars in town and countryside, who shared their views and gave me their counsel and their learning. See pp. 21–48 of that book, and p. 13 of <i>Bahre Kemer</i>.")
  + P("ከዚያም ወደ አዲስ አበባ ጠቅላይ ቤተ ክህነት የሊቃውንት ጉባዔ ክፍል በመኄድ የጉባዔው መልካም ፈቃድ ሆኖ ለሁለት ቀናት ውይይት ተደርጎአል፡፡ በተመለከተው የቊጥሩ ዕድገት ከተግባባን በኋላ ጉባዔው ድጋፋዊ ሐሣቡን ለግሶኛል፡፡ በዓለማችን ውስጥ የነበሩና ያሉ ከመቶ በላይ የሚሆኑ የአኀዝ ቊጥሮችና የፊደላት ቊጥር በጥናቱ ተካትቶአል፡፡ ሦስቱን የአኀዝ መለኪያዎች ሥርዓትን ባያሟላም በመጠኑም ቢሆን የአኀዝ ቊጥርን ለማሻሻል ያመለከቱ ኢትዮጵያዊያን በገጹ ተመለክተዋል፡፡ ከ1 እስከ 1 ሺሕ ከዓረቢክ ቊጥር ጋር በማመሳሰል በሁለት ዐምድ ረብቶአል፡፡ አንድ ሃገር የዕድገት አቅጣጫን ካመለከተ አዲስ ምልክት፡ ቁጥርና ኮድ የመሰሉትን የግድ እንዲፈጠሩ ያስገድዳል፡፡ በዚሁ ምክንያት የንዑሳንና ዓቢያን መራኁት ኮድንም ያመለክታል፡፡",
      "I then went to the Council of Scholars at the Patriarchate in Addis Ababa, where, by the Council’s good will, discussions were held over two days; once we had reached agreement on the growth of the numbers set out, the Council gave me its supporting opinion. More than a hundred numeral systems and alphabetic numerals from around the world, past and present, are included in the study. The Ethiopians who tried, in some measure, to improve the numerals — even without fulfilling the three measures — are also recorded in its pages. The numbers from 1 to 1,000 are set out in two columns alongside the Arabic numerals. When a country sets a direction of growth, it necessarily calls for new symbols, numbers, codes and the like; for this reason the book also sets out the code of the minor and major keys (<i>ne’usan</i> and <i>abiyan merakhut</i>).")
  + H3("የዋየሎች ቅደም ተከተል", "The Order of the Wayel")
  + P("ዋየል ማለት አብዢ ማለት ነው፡፡ ፼ ፼፼ ፼፼፼ ……እነዚህ አብዢ ናቸዉ እንጂ ቊጥር አይደሉም፡፡ ቊጥር ሲሆኑ አንድ ወይም ከአንድ በላይ አኀዝ ቊጠር በፊታቸዉ መኖር አለበት ብለናል፡፡ ለምሳሌ፡ ፩፼ ፩፼፼ ፩፼፼፼……እንደዚህ መሆን አለበት፡፡ ሲነበብ አንድ መቶ፡ አንድ እልፍ፡ አንድ አእላፍ አንድ አእላፋት ነው፡፡",
      "<i>Wayel</i> means multiplier. ፼ ፼፼ ፼፼፼ … are multipliers, not numbers. As we have said, to become numbers they must have one or more numerals in front of them — for example ፩፼ ፩፼፼ ፩፼፼፼ …. Read aloud: one hundred, one elf, one a’elaf, one a’elafat.")
  + H3("3ኛ. ባሕረ ቀመር", "3. <i>Bahre Kemer</i>")
  + P("ባህረ ቀመር ከሰዋስወ ቀመር ቀጥሎ የታተመ 188 ገጽ የያዘ መጽሐፍ ነው፡፡ ሰዋስወ ቀመር የግል አስተያየት ይጨምራል፡፡ ባሕረ ቀመር ግን ጥናቱን ብቻ የሚያመለክት ነው፡፡ እንዲሁም የአኀዝ ቁጥር ዕድገት ኮድ ወይም ምሥጢር በከፍተኛ ደረጃ የተመሠረተበት ነው፡፡",
      "<i>Bahre Kemer</i>, published after <i>Sewasewe Kemer</i>, runs to 188 pages. <i>Sewasewe Kemer</i> includes personal commentary; <i>Bahre Kemer</i> presents the study alone. It is also the book in which the code — the inner key — of the numerals’ growth is established at the highest level.")
  + H3("4ኛ. ባሕረ ቀመር ሁለተኛ፡ 144 ገጽ", "4. <i>Bahre Kemer, Volume Two</i> (144 pages)")
  + P("ይዘቱ ቊጥር ቢሆንም ባሕረ ቀመር ሁለተኛ ከሰዋስወ ቀመርና ከባሕረ ቀመር የተለየ ጥናት ያመለክታል፡፡ ከአንድ ቊጥር እስከ ረበዋተ ምእልፊታተ ምእልፊታት ከአንድ እሰከ 6የ ገጽ በአኀዝ በባሕረ ቀመርና በዓረቢክ በሦስት ዓምድ፡ ከ61 እስከ 144 በአኀዝ በዓረቢክ በግዕዝና በእንግሊዘኛ በዐራት ዓምድ አንድ በአንድ ተተንትኖ የቀረበ ነው፡፡ የኸም ሦስቱን የቊጥር ሕገጋት አማልቶ የረባ ነው፡፡ ለጊዜው የቊጥሩ ገደብ 1638፡0000 ድርደር ወይም ዲጂትስ ነው፡፡ ሲነበብ አንድ ሺሕ ስድስ መቶ ሠላሳ ስምንት እልፍ ድርድር ነው፡፡",
      "Though its subject is number, <i>Bahre Kemer, Volume Two</i> presents a study distinct from <i>Sewasewe Kemer</i> and <i>Bahre Kemer</i>. From the number one up to ረበዋተ ምእልፊታተ ምእልፊታት, each number is analysed one by one: on pp. 1–6የ (60) in three columns — Ge’ez numeral, Bahre Kemer and Arabic — and on pp. 61–144 in four columns — Ge’ez numeral, Arabic, Ge’ez and English. It is built up in fulfilment of the three laws of number. For now, the limit of the numbers is 1638፡0000 digits — read as one thousand six hundred thirty-eight elf digits.")
  + H3("5ኛ. ባሕረ ቀመር የሒሣብ መልመጃ፡ ቊጥር አንድ፡ 96 ገጽ", "5. <i>Bahre Kemer Arithmetic Exercises, No. 1</i> (96 pages)")
  + P("ይህ መጽሐፍ የተለየ ጥበብን ያመለከታል፡፡ ልብ ወለድ ድርሰቱ በግዕዝ ቋንቋ ሆኖ በአማርኛ እየተፈታ ወይም እየተተረጎመ በአኀዝ ቊጥር ቀላል ሒሣብ የሚሠራበትና የሚያስተመር ነው፡፡ ሒሣብ ብቻ ሳይሆን እግረ መንገዱ የግዕዝ ቋንቋንም ሊያስተምር የሚችል ነው፡፡",
      "This book shows a different craft. Its story is written in Ge’ez and explained, or translated, in Amharic, and through it simple arithmetic is worked and taught in Ge’ez numerals. Along the way it can teach not only arithmetic but the Ge’ez language too.")))

S.append(("results", "ጥናቱ ያስገኘው ውጤትና የቊጥሩ ሥርዓት", "What the Study Achieved, and the Number System",
  P("በጥናቱ ላይ ባለኝ ልምድ መሠረት የቊጥሩ ሥርዓት ከነበረው ነባር የአኀዝ ቊጥር ሥርዓት በማዛመድ በማያሻማ ሁኔታ በትክክል ሥርዓቱን ይዞአል፡፡ በመጀመርያ አንድ ቊጥር፡ ቊጥር ሊያሰኘው የሚችል ሦስት ነገሮችን አማልቶ መገኘት አለበት፡፡ እነሱም፡",
    "From my experience with the study, the system — related to the traditional system of Ge’ez numerals — holds its order correctly and unambiguously. First of all, for a number to be called a number, it must be found to fulfil three things:")
  + OL([("1ኛ", "1", "ቅርፅ፡ በእጅ ተቀርፆ በዓይን ተመልክቶ ርዝመቱ ስፋቱ የሚረጋገጥበት ውስጣዊ ምሥጢር፡", "<b>Form</b> (ቅርፅ): the inner principle by which it is shaped by hand, seen by the eye, and its length and breadth confirmed;"),
        ("2ኛ", "2", "ድምፅ፡ በአፍ ተነግሮ በጆሮ ተሰምቶ በአእምሮ የሚረጋገጥበት ውስጣዊ ምሥጢር፡", "<b>Sound</b> (ድምፅ): the inner principle by which it is spoken by the mouth, heard by the ear and confirmed by the mind;"),
        ("3ኛ", "3", "ይዘት፡ የይዘቱ ሚዛን በአእምሮ ተለክቶ ተመዝኖ ተገምቶ የሚረጋገጥበት ውስጣዊ ምሥጢር ነው፡፡", "<b>Content</b> (ይዘት): the inner principle by which the weight of its content is measured, weighed and estimated by the mind, and confirmed.")])
  + P("የእነዚህ ሥርዓታትን ያላሟላ ቊጥር፡ ቊጥር ሊባል አይገባም፡ አይችልምም፡፡ ከአሁን ቀደም ከመጨረሻ ገበታ ሲጻፍ የነበረ ሁሉ እንደ ተለመደው ዝምብሎ ጉልት፡ ዝርው ሊባል ይችላል፡፡",
      "A number that does not fulfil these should not — and cannot — be called a number. Everything that, by custom, used to be written on the last page may simply be called a heap, a scattering.")))

S.append(("growth", "የቊጥሩ ዕድገት ሥርዓት", "The Order of the Numbers’ Growth",
  P("የቊጥሩ ዕድገት የአኀዝ ቊጥር ርባታ ሥርዓትን ጠብቆ እጅግ በጣም ከፍተኛ ደረጃ ደርሶአል፡፡ የዓለም ትልቁ ቊጥር እሰከ 2004 እ፡ አ፡ አ፡ 7235733 ድርድር (ዲጂትስ) ደርሶ እንደ ነበር ይታወቃል፡፡ ከዚያ ጊዜ እሰከ አሁን በ11 ዓመት ውስጥ ምን ያህል ከፍተኛ ደረጃ እንደ ደረሰ ለመረዳት ከ(googoleplex.com) ገብቶ ማየት ይቻላል፡፡ እኛ ግን የነበረን ቊጥር ተጠብቆ ባለመቆየቱና ባለማደጋችን ለብዙ ዓመታት በቃል ብቻ የሚነገር ወሬ ካልሆነ በቀር ከ1,000,000 ቤት በላይ መቊጠር ያልቻልን ህዝብ እንድንሆን ተገደናል፡፡ የኸውም ዓለም ተፈጠረ በተባለው በተዋሕዶ እምነት አቆጣጠር ብቻ ከ8,000 በላይ እንዳንቆጥር አድርጎታል፡፡ የኸውም ያለ መማራችንና የድኅነታችን ውጤት ነው፡፡ አሁን ዕድገት እያመለከተ ስለ ሆነ ወደን ሳይሆን የተፈጥሮ ኂደት ነውና በዘመኑ ግዳጅ ራሱ ቊጥሩ ያድጋል፡፡ ብዙ ኮድ፡ ምልክት፡ ምሥጢራዊ ዶክዩሜንት የዕድገት ውጤቶች ስለ ሆኑ በኂደት የግድ ራሳቸዉ ይፈጠራሉ፡፡ በዚሁ መሠረት ይህ ጥናታዊ የቊጥር ዕድገት ጊዜ ስለ ሚፈቅድለት ቦታ ሊያገኝ ይገባል፡፡ ትውልዱ ከቊጥሩና ከቋንቋው የሸፈተበት ምክንያት የቊጥሩ ሥርዓት አለመስተካከልና ጥበብንም አለመከተል ሳይሆን አይቀርም፡፡",
    "Keeping to the rules of conjugation (<i>rubata</i>) of the Ge’ez numerals, the growth of the numbers has reached a very high level. It is known that the world’s largest number had reached 7,235,733 digits by 2004 G.C.; to see how much higher it has gone in the eleven years since, one can visit googoleplex.com. We, however — because the numbers we had were not preserved, and we did not develop them — have for many years been forced to be a people unable to count beyond the place of 1,000,000, except in talk. In the Tewahedo reckoning of the age of the world alone, this has kept us from counting beyond 8,000. It is the result of our lack of learning and our poverty. Now that the numbers are showing growth, they will grow of themselves under the demands of the age — not because we wish it, but because it is a natural process. Codes, symbols and encrypted documents are products of growth, and in time they will necessarily come into being of themselves. On this basis, this researched growth of numbers should be given its place, as time allows. The reason the generation has deserted its numbers and its language is most likely that the number system was never set in order, and that wisdom was not followed.")
  + P("አሁን ግን በባሕረ ቀመር ሁለተኛ መጽሐፍ የቊጥሩ ሥርዓት በቅኔ ቤት ርባታ ሕግ መሠረት ተተንትኖ አስተማማኝ የሆነ ሕግ (ፍሬምዎርክ) ያለው ነው፡፡ ከመጀመርያ እሰከ መጨረሻ በዐሥር በዐሥር እያደገ የረባበት ሥርዓት በ13 በ13 የተመደበ ሲሆን የቀደመው ድምር ከሚከተለው ድምር ሲቀነስ 169 መምጣት አለበት፡፡ ይህ ቊጥር ካልመጣ ልክ ስለ አይደለ ማንም አንባቢ ሊያስተካክለው የሚችል ሥርዓት ነው፡፡ 2ኛ. የቀደመው ድምር ከሚከተለው ድምር ሲቀነስ 52 ካልመጣ አሁንም አንባቢ ሊያስተከክለው ይችላል፡፡ በተረፈ ከመጽሐፉ ገጾች ማረጋገጥ ይቻላል፡፡ ከጥናቱ የተገኙ ተጨማሪ ውጤቶች ሦስት ናቸዉ፡፡ እነ ሱም፡",
      "Now, however, in <i>Bahre Kemer, Volume Two</i>, the number system has been analysed according to the rules of conjugation of the Qene school, and it has a reliable framework. From beginning to end the system, growing by tens, is arranged in groups of 13; when each preceding sum is subtracted from the following sum, the result must be 169. If it is not, something is wrong, and any reader can correct it. Second, if subtracting the preceding sum from the following one does not give 52, the reader can again correct it. The rest can be verified from the pages of the book. The study has produced three further results:")
  + OL([("ሀ", "a", "ሒሣብ ለመሥራት የሚያስችል ሙሉ ቁጥርን ያስገኘ፡", "a complete number system with which calculation is possible;"),
        ("ለ", "b", "የቊጥር በጣም ከፍተኛ ዕድገትን ያስገኘ፡", "a very high growth of numbers;"),
        ("ሐ", "c", "ከግዕዝ መጻሕፍት ውስጥ ብዙ የቁጥር ድርድር ሲገኝ በአጭር ጊዜ ማወቅ የሚያስችል ናቸዉ፡፡", "and a means of quickly reading the long strings of numerals found in Ge’ez books.")])
  + P("ከግዕዝ መጻሕፍት ውስጥ ብዙ ድርድር ወይም ዲጂትስ ሲገኝ ቅርፁና ድምፁ በተወሰኑ ምሁራን ሊታወቅ ይችላል፡፡ ይዘቱ ግን በምንም ተአምር አይታወቅም ነበር፡፡ አሁን በተገኘው ጥናታዊ ሥርዓት ግን በአጭር ጊዜ ማግኘት ይቻላል፡፡ እንደዚህ እንደ ሚከተለዉ ሊገኝ ይችላል፡፡",
      "When a long string of numerals is found in a Ge’ez book, its form and sound may be known to a few scholars, but its content — its value — could by no means be known. With the system this study has produced, it can now be found quickly, as follows:")
  + P("(፲ወ፱፻፶ወ፭፼፶ወ፪፻፲ወ፪) — ይህ ትንሽ ቁጥር ነው በጣም ብዙ ወይም ትልቅ ቁጥር የሚባል አይደለም፡፡",
      "(፲ወ፱፻፶ወ፭፼፶ወ፪፻፲ወ፪) — this is a small number, not one that could be called very large.", "example")
  + P("ይህ በአኀዝ ሲነበብ፡ ዐሥርቱ ወተስዐዓቱ ምእት፡ ሃምሣ ወሐምስቱ እልፍ፡ ሃምሣ ወክልኤቱ ምእት ዐሥርቱ ወክልኤቱ ነው፡፡ ደኅና ጠለቅ ብሎ አቡሻሕር፡ መጽሐፍና ቅኔ የተማረ ሁሉ ይህነንን ንባቡን ሊያነበው ይችላል፡፡ ስንት ዋጋ ወይም ባልዩ እንዳለው ግን ሁሉም ያውቀዋል ተብሎ አይገመትም፡፡ አሁን በአጭር እንተርጉመው፡፡ በአማርኛ ሲነበብ፡ አንድ አእላፍ፡ ዘጠኝ መቶ ሃምሣ አምስት እልፍ፡ ሃምሳ ሺሕ ሁለት መቶ ዐሥራ ሁለት ነው፡፡ በባሕረ ቀመር ቁጥር ሥርዓት ባጭሩ ሲጻፍ፡ ፩፡የ፱፶፭፡፶፪፲፪ ነው፡፡ ወይም 109,555,212",
      "Read in Ge’ez, this is ዐሥርቱ ወተስዐዓቱ ምእት፡ ሃምሣ ወሐምስቱ እልፍ፡ ሃምሣ ወክልኤቱ ምእት ዐሥርቱ ወክልኤቱ. Anyone who has studied Abushakir, the Scriptures and Qene in some depth can read it aloud; but not everyone, it is supposed, knows what value it holds. Let us interpret it briefly. Read in Amharic: one a’elaf, nine hundred fifty-five elf, fifty thousand two hundred twelve. Written briefly in the Bahre Kemer system: ፩፡የ፱፶፭፡፶፪፲፪ — or 109,555,212.")
  + P("( ፫-፼ ፩፼፼፼ ፲ወ፱፻፶ወ፭፼፳ወ፪ ) — ይህ ንባብ አይደለም", "( ፫-፼ ፩፼፼፼ ፲ወ፱፻፶ወ፭፼፳ወ፪ ) — this is not a reading", "num-seal")))

S.append(("strength", "የሃገር ጉልበትና ዕውቀት", "The Nation’s Strength and Knowledge",
  P("የኢትዮጵያዊያንን ዕውቀትና ጉልበት አስተባብሮ ለዕድገት እንዳይውል እንዲህ ተበታትኖ የየራሱ ጓዳ እያበጀ ለዘመናት የኖርንበት አገር ሆኖ ይገኛል፡፡ የኢትዮጵያ ታሪክ ወይም ሌላ ይዘት ያለው መጻፍ ይጽፉና በመጨራሻው ገጽ ቊልል ቊጥርን ይጎልታሉ፡፡ ጥናት ቢያደርጉበት የሆነ ውጤት አያጡም ነበር፡፡ ግን ከሌላ መጽሐፍ ጫፍ አይተዉ ጎትተው ነው የሚጽፉትና የሚቆልሉት፡፡ እሱም ከእልፍ በላይ ያለው ውሳኔያቸዉ እጅ፡ እግር፡ አፍንጫ፡ አፍና …ሌላም ብለዉ ነው የሚተረጉሙት፡፡ የየአንዳንዱ የቁጥር ውሳኔ ተመሳስሎ አይገኝም፡፡ የየራሳቸዉ ነው የሚወስኑትና የሚያነቡት፡፡ ምሳሌውን ቀጥለን ልናመጣው ነው፡፡ ሌላው እነዚህ ከዚህ ቀጥለው ያሉ ራሳቸውን የቻሉ የቊጥር ምደብ ናቸዉ፡፡",
    "Ours has become a country where, for ages, the knowledge and strength of Ethiopians have been scattered like this — each building a back room of his own — instead of being brought together for growth. People write a book of Ethiopian history or on some other subject, then pile a heap of numbers onto the last page and lay it out like goods in a market. Had they studied the matter, they would not have failed to reach some result; but they glance at the edge of another book, drag the numbers across, and pile them up. Their conclusions beyond <i>elf</i> they interpret as hand, foot, nose, mouth … and so on. No two of their conclusions agree; each decides and reads in his own way. We give an example below. Moreover, the following are number classes in their own right:")
  + '<ul class="term-list"><li>እልፍ</li><li>አእላፍ</li><li>አእላፋት</li><li>ትእልፊት</li><li>' + T("ምእልፊትና……የመሳሰሉት ናቸዉ፡፡", "ምእልፊት, and the like.") + "</li></ul>\n"
  + P("እነዚህ ራሳቸውን የቻሉ የአኀዝ ቊጥር ምድብ ስለ ሆኑ የሌላ የአኀዝ ቊጥር መፍቻ ወይም መተርጐሚያ ሊሆኑ አይችሉም፡፡ በዝርዝር ፊደል ወይም በዓረቢክ ቊጥር ወይም በማንኛውም ቋንቋ በዝርዝር መፍታት ይቻላል፡፡ ለምሳሌ 100) አንድ መቶ ነው፡፡ በአኀዝ ለአንድ መቶ ቊጥር መፍቻ ወይም መተርጎሚያ የለውም፡፡",
      "Because these are numeral classes in their own right, they cannot serve as the key or translation of other numerals. They can be spelled out in words, in Arabic numerals or in any language — 100, for example, is “one hundred” — but within the Ge’ez numerals, one hundred has no other key or translation.")
  + table(["akh", "rd"], [["፩፼", "አንድ እልፍ"], ["፲፼", "ዐሥርቱ እልፍ"], ["፩፻፼", "አንድ መቶ እልፍ"], ["፲፻፼", "ዐሥር መቶ እልፍ"], ["፼፼", "አእላፍ"]])
  + P("፼ ተብሎ ከተመደበ እንዴት ትእልፊት ትእልፊታትና…ሌላ ተብሎ ሊፈታ ይገባል፡፡ እንደ ዚህ ያለ ሥራ ልምዳዊ እንጂ ጥናታዊ ወይም መሠረታዊ ጥበብ ነው ሊባል አይችልም፡፡ እና ከአሁን ጀምሮ ስለ ሃገር ስለ ተተኪ ወጣት በማሰብ ሊታረም ይገባል፡፡",
      "If ፼ has been assigned as the unit, how can it be rendered as ትእልፊት, ትእልፊታት and so on? Work of this kind is customary, not scholarly or grounded in principle. From now on, for the sake of the nation and of the young who will follow, it must be corrected.")))

S.append(("further", "ስለ ጥናቱ ተጨማሪ ማብራርያ", "Further Explanation of the Study",
  P("እንግዲህ አንድ ቊጥር፡ ቊጥር ሊሆን የሚችል ሦስት ነገሮችን ሲያሟላ ነው ብለናል፡፡ እነሱም ቅርፅ ድምፅና ይዘት ናቸዉ፡፡ (እልፍ አእላፍ አእላፋት) እንዚህ ሦስቱ በድምፅና በአኀዝ ሳይሆን በቅርፅ ብቻ ሊታወቁ ይችላሉ፡፡ እልፍ ቤት በአብዛኛው በተዋሕዶ የአብነት ምሁራን ዘንድ በቅርፅም በድምፅም በይዘትም ምሁራኑ ሊስማሙ ይችላሉ ተብሎ ይታመናል፡፡ (በአእላፍና በአእላፍት……) ግን በድምፅ በስተቀር በቅርፅና በይዘት ሊስማሙ ይችላሉ ተብሎ አይታመንም፡፡ እያናዳንዱ ጸሐፊ ይሁን አስተማሪ በየአለበት ውስን ቦታ እሱ ራሱ ወሳኝ ሆኖ ውሳኔ መስሎት ይናገራል ይወስናል እንጂ ለሃገር ለተተኪ ትውልድ የሚተርፍ የሚያስተባብር ሆኖ አይደለም፡፡ ለማስረጃ ከላይ የቀረቡት ቊጥሮችን ማረጋገጥ ይገባል፡፡",
    "We have said, then, that a number is a number when it fulfils three things: form, sound and content. These three — እልፍ, አእላፍ, አእላፋት — may be known by form alone, not by sound and numeral. It is believed that, for the place of <i>elf</i>, the traditional scholars of the Tewahedo Church can largely agree on form, sound and content alike. For አእላፍ and አእላፋት …, however, it is not believed that they can agree on anything but the sound. Each writer or teacher, in his own small corner, speaks and decides as though his were the deciding word — not in a way that would serve the nation and the generation to come, or bring people together. For evidence, the numbers presented above should be checked.")
  + P("‹‹መጽሐፈ ሰዋስው ወግሥ ወመዝገበ ቃላት ሐዲስ›› በተባለ መጽሐፍ አዘጋጁ ያደረጉት ጥናትና ጥረት መሳይ የሌለው መሆኑ እናዳለ ሆኖ በአኀዝ ቊጥር ግን ብዙም አላተኮሩበትም፡፡ እንደ አጋጣሚ ጨረፍ አድርገውት ነው ያለፉት፡፡ ከላይ የተጠቀሱት መጸሕፍቶቻቸዉ ሁለቱ አይስማሙ፡፡ ለምሳሌ፡ አንዱ መጽሐፍ ፼፼ ይህን ምእልፊት ይላል፡፡ ሁለተኛው ፼፼ ትእልፊታት) ይላል፡ ይዘታቸውም እንዲሁ ነው፡፡ ከሳቸዉ በፊት የነበረ ዋቢ ማስረጃ ስለ አላገኙ ዝምብለዉ እንዲህ ይሁን ብለዉ አሰፈሩት እንጂ እንደ ምናየው በጥናታቸዉ አልተካተተም፡፡ እንደ ዚሁም ሕጉን ጠብቆ በዓሥር በዐሥር ያደገ አይደለም፡፡ ማንኛውንም የአኀዝ ቊጥርን የጻፈ ሁሉ ማስረጃው ወይም መነሻው መጽሐፈ ሰዋስው ወግሥ ወመዝገበ ቃላት ሐዲስ እንደ ሆነ የሁሉም በይዘታቸዉ ይረጋገጣል፡፡ ምክንያቱም ከ1926ና ከ1948 ዓ. ም በፊት የተጻፈ አኀዝ ቁጥርን የሚያመለክት ጽሑፍ ሊኖር ይችል ይሆናል፤ ግን አላጋጠመነም፡፡",
      "The study and effort of the compiler of <i>Metshafe Sewasew Wegis Wemezgebe Qalat Haddis</i> are without equal; but he did not concentrate on the numerals — he touched on them in passing, as the occasion arose. His two books mentioned above do not agree: one calls ፼፼ ምእልፊት, the other ትእልፊታት, and their content differs likewise. Having found no earlier reference, he simply set it down as he thought it should be; as we see, it was not part of his study. Nor does it grow by tens according to the rule. The content of every other author’s numerals confirms that their source, their starting point, is <i>Metshafe Sewasew Wegis Wemezgebe Qalat Haddis</i>. There may be writings on the Ge’ez numerals from before 1926 and 1948 E.C., but we have not come across them.")
  + P("ኃያልና የጥበብ ሃገር የነበረች ኢትዮጵያ ብዛት ያለው ቊጥር አልነበራትም ለማለት አይቻልም፡፡ ግን በጠላት ይሁን በውስጠ አርበኛ የነበረው ከፍተኛ ቊጥር ወድሞአል ተደምስሶአል፡፡ ጨርሶ በጠላት ወደመ እንዳንል በጠቅላላ ቅርስን የሚያወድም ጠላት ተነሥቶባት አያውቅም፡፡ ያም ሆነ ያ፡ አሁን ከ፩፻፼ ከአንድ መቶ እልፍ በላይ ቅርፅ፡ ድምፅና ይዘት፡ በአኀዝ፡ በግዕዝና በአማርኛ ፊደል አሟልቶ ጽፎ ከእልፍ ቤት በላይ የሚያውቅ ሰው የለም፡፡ ስለዚህ በአሁኑ ጊዜ ወጣቱ ትውልድ በአኀዝ ቊጥር የተነሣ በጣም ተረብሾአል፡፡ ታሪኩንና ቅርሱን ሊከተልና ሊያከብር ሊያጠና አልቻለም፡፡ ስለ ሆነም ወደ ሌላ ወደ ባዕድ ቊጥር ያመራው በዚሁ ምክንያት እንደ ሆነ ጥናቱ ያመለክታል፡፡",
      "It cannot be said that Ethiopia — once a mighty land of wisdom — had no system of large numbers. But whether through enemies or through traitors within, the higher numbers that existed were destroyed and wiped out. Nor can we say it was destroyed entirely by an enemy, for no enemy ever rose against her that destroyed her heritage wholesale. Be that as it may, there is no one today who can write numbers beyond ፩፻፼ (one hundred elf) complete in form, sound and content — in Ge’ez numerals, in Ge’ez and in Amharic letters — or who knows anything beyond the place of <i>elf</i>. The young generation is therefore deeply troubled by the Ge’ez numerals; it has been unable to follow, honour and study its own history and heritage. The study indicates that this is why it has turned to other, foreign numerals.")))

S.append(("on-the-study", "የጥናቱ", "On the Study",
  P("ጥናቱ መቼ እንደ ተጀመረ፡ ለምን አስፈለገ፡ ጥናቱ ስንት ዓመት ወሰደ፡ ጥናቱን በሚመለከት ስንት መጻሕፍት ታትመዋል፡ ይዘታቸዉ በምን ይለያል በምንስ ይመሳሰላል፡ የቊጥሩ ሥርዓት እንዴት እንደ ነበርና እንዴት እንደ አለ ለይቶ ለመመልከት ተሞክሮአል፡፡",
    "I have tried to set out clearly when the study began and why it was needed; how many years it took; how many books on it have been published, and how their contents differ and agree; and how the number system was, and how it stands now.")
  + P("በማንም ኃይል ሳይሆን በተፈጥሮ የታሪክ ድርሻ ግዳጅ ሆኖብኝ በዚህ አኀዝ ቊጥር ጥናት ግማሽ ዕድሜዬን አቃጥየበት አለሁ፡፡ ያስገኘው ውጤትም ለሕሊናዬ ከፍተኛ ዋጋ ነው፡፡ በዓለማችን ሥልጣኔና ኪነ ትበብ እየተነሣና እየወደቀ የኖረበት ዓለም እንደ ሆነ እንረዳለን፡፡ አኀዝ ቊጥርም የኪነ ጥበብ አካል ስለ ሆነ የውድቀት አዳጋ አጋጥሞታል፡፡ ይሁን እንጂ የትንሣኤውን ቀን የሚጠብቅ መሆኑን ግን ማስታወስ ይገባል፡፡",
      "Compelled by no one’s power, but by the natural duty that history laid upon me, I have spent half my life on this study of the Ge’ez numerals, and what it has yielded is of the highest worth to my conscience. We understand that ours is a world in which civilisation and the arts have risen and fallen. The Ge’ez numerals, being part of the arts, suffered the calamity of a fall; yet it should be remembered that they await the day of their resurrection.")
  + P("ባደረክሁት ድካም ብልጫ ቢኖረኝም በኢትዮጵያዊነቱ የሚተማመንና ቊጥሩም የኢትዮጵያ ቅርስ ንብረቴ ነው ብሎ ለሚያምን ሁሉ የጋራ የታሪክ ሃብታችን እንደ ሆነ መታወቅ አለበት፡፡ የአእምሮ ንብረትነትን ለማረጋገጥ በረቀቀ ዓይነ ሕሊና መመልከት ያስፈልጋል፡፡ የአእምሮ ንብረትነቱ ከ1 ቊጥር እሰከ አንድ መቶ እልፍ ቤት ያለውን ቊጥር ሳየያካትት ከዚያ በላይ በጥናት ያስገኘሁትን ብቻ ይመለከታል፡፡ ጥናቴም ሦስት የጥናት ውጤትን ያስገኘ ነው፡፡",
      "Though the labour was mine and the credit is my due, it should be known that this is our shared historical wealth — for everyone confident in their Ethiopian identity who holds that the numerals are Ethiopian heritage and their own possession. Intellectual property must be viewed with a discerning eye: it concerns only what I established through study above the place of one hundred elf, not the numbers from 1 up to one hundred elf. My study has produced three results.")
  + P("በአሁኑ ጊዜ በኢትዮጵያዊያን ጸሐፊያን ዘንድ በጣም አስቸጋሪ ሆኖ የተገኘ የሚጽፉትን መጽሐፍ የተለየ ጥናት ይሆንና በመጨረሻው ሽፋን ጥግ ወይም በሆነ ቦታ በአንዲት ገጽ አኀዝ ቊጥርን ከአለቃ ኪዳነ ወልድ መጽሐፍ (መጽሐፈ ሰዋስው ወግሥ ወመዝገበ ቃላት ሐዲስ) ገልብጠው ያሰፍራሉ፡፡ ከአለቃ ኪዳነ ወልድ ሥርዓት ውጪ የጻፉ ካሉም ከቊጥሩ ሕግ ጋር የማይስማማ ጥናትን የማያመለክት ጉልት ሆኖ ይገኛል፡፡ ትውልዱ እንዲህ የተዝረከረከ ስለ ሆነበት ቊጥሩን ጥሎት ሸሽቶአል፡፡ አሁንም ሳይመሽ ትውልድን አንድን አቅጣጫ ለማሳየት ቊጥሩ አንድ ወጥ መሆን ይገባል፡፡ አሁን ሆኖዋልም፡፡",
      "What has proved most troublesome among Ethiopian writers today is this: the book they write is on some other subject, and then, in a corner of the back cover or somewhere else, they set down a single page of Ge’ez numerals copied from Aleqa Kidane Wold’s book (<i>Metshafe Sewasew Wegis Wemezgebe Qalat Haddis</i>). Those who write outside the Aleqa’s system produce a heap that does not agree with the rules of number and reflects no study. Because things have become such a muddle, the generation has abandoned its numerals and fled. Before it is too late, the numbers must be made uniform, to show the generation a single direction — and now they have been.")
  + P("ከኔ በላይ ጥናት ያደረገና ትክኒካዊ የሆነ የተሻለ የቊጥር ይዘት ያለው ሰው ካለ ወጥቶ በአደባባይ ማሳመን ይቻላል፡፡ አለዚያ እያንዳንዱ በየፊናው እየጻፈ ወጣቱን ከማደናገር እንዲቆጠብ ማሳሰቢያ ማቅረብ አስፈላጊ ሆኖ ተገንቶአል፡፡",
      "If there is anyone who has studied more than I have, with a better and more technical account of the numbers, let them come forward and make their case in public. Otherwise, it has been found necessary to issue a reminder that each should refrain from confusing the young by writing in his own direction.")))

toc = "".join(f'<li><a href="#{i}">{T(a, e)}</a></li>' for i, a, e, _ in S)
body = "".join(f'<section class="key-sec" id="{i}">\n<h2>{T(a, e)}</h2>\n{h}</section>\n' for i, a, e, h in S)
html = f'''<!-- Key (ቁልፍ). Generated by _gen_key.py — edit here directly or regenerate. -->
<nav class="key-toc" aria-label="Contents">
<p class="eyebrow">{T("ማውጫ", "Contents")}</p>
<ol>{toc}</ol>
</nav>
<article class="key-body">
{body}</article>
'''
open(OUT, "w", encoding="utf-8").write(html)
print("ok", len(S))
