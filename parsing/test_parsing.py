from parsing.parse import parse, parse_and_save
from parsing.analyze import get_orgs_from_text, classify

urls = [
    "https://orenburg.media/?p=94827",
    "https://orennc.ru/?p=1146",
    "https://orenburg-cci.ru/znakomtes-uchebnyj-tsentr-podgotovki-buhgalterov-ogu/",
    "https://orenburg-gov.ru/news/4136/",
    "https://asi.ru/news/19083/",
    "https://sbp-invertor.ru/our-media/novosti/ao-zavod-invertor-vstupil-v-natsproekt-proizvoditelnost-truda.html",
    "https://mineconomy.orb.ru/presscenter/news/42901/",
    "https://www.akkermann.ru/kompaniya-akkermann-otkryla-czentr-betonnyh-tehnologij-pro_beton/",
    "http://zbo.ru/info/news/nauchnyy-proekt-goda/",
    "https://mz-orsk.ru/news/perspektiva-razvitiya/",
    "https://www.ecobios.ru/ooo-innovaczionnaya-kompaniya-ekobios-poluchen-sertifikat-sootvetstviya/", #universal
    "http://fncbst.ru/?p=11578",
    "https://trends.rbc.ru/trends/innovation/cmrm/62a09f139a79470bf2fac6c0?page=trend&nick=innovation&from=infinityscroll"
    #"https://orenburzhie.ru/news/dve-studentki-predstavlyayut-orenburzhe-v-finale-konkursa-flagmany-obrazovaniya-studenty/",
    #"https://ria56.ru/posts/v-abdulinskom-gorodskom-okruge-sdelan-akcent-na-modernizacii-infrastruktury-zhkx.htm"
]

def test():
    for s in urls:
        code, d = parse(s)
        print(d)

def test_save():
    for s in urls:
        parse_and_save(s)




