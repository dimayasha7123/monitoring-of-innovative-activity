from parse import parse
from analyze import get_orgs_from_text, classify

urls = [
    "https://orenburg.media/?p=94827",
    "https://orennc.ru/?p=1146",
    "https://orenburg-cci.ru/znakomtes-uchebnyj-tsentr-podgotovki-buhgalterov-ogu/",
    "https://orenburg-gov.ru/news/4136/",
    "https://asi.ru/news/19083/",
    "https://sbp-invertor.ru/our-media/novosti/ao-zavod-invertor-vstupil-v-natsproekt-proizvoditelnost-truda.html"
    #"https://orenburzhie.ru/news/dve-studentki-predstavlyayut-orenburzhe-v-finale-konkursa-flagmany-obrazovaniya-studenty/",
    #"https://ria56.ru/posts/v-abdulinskom-gorodskom-okruge-sdelan-akcent-na-modernizacii-infrastruktury-zhkx.htm"
]

for s in urls:
    code, d = parse(s)
    if code:
        print(classify(d["text"]))
        orgs = get_orgs_from_text(d["text"])
        print(orgs)

    print(parse(s))





