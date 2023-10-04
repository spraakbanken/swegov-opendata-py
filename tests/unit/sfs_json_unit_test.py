from lxml import etree
import pytest

from swegov_opendata.core.component.preprocess.preprocess_sfs.sfs_json import (
    div_dok_extract_page,
    div_dok_extract_paragraph,
    div_dok_extract_text_and_br,
    div_dok_extract_text_br_and_tail,
    extract_paragraph_recursive,
)
from swegov_opendata.lxml_extension import print_tree, cleaning
from tests.etree_asserts import assert_elem_equal, assert_elem_equal_no_trim


# def test_div_dok_extract_paragraph():
#     elem = etree.fromstring(
#         """<p style="margin-left: 40px">
#           <span class="line" style="font-size: 0.65em">Från Riksgäldskontor utgående riksdags- och revisionskostnader,
#             aflöriingar, för<br /> </span><span class="line" style="font-size: 0.85em">valtningsutgifter m. m. §§
#             21—31.</span>
#         </p>"""
#     )
#     paragraphs = []
#     div_dok_extract_paragraph(elem, paragraphs)

#     expected = etree.fromstring(
#         """
#         <p>Från Riksgäldskontor utgående riksdags- och revisionskostnader,
#             aflöriingar, för<br />valtningsutgifter m. m. §§
#             21—31.
#         </p>"""
#     )
#     assert assert_elem_equal(paragraphs[0], expected)


# def test_div_dok_extract_text_br_and_tail():
#     elem = etree.fromstring(
#         """
#           <span class="line" style="font-size: 0.65em">Från Riksgäldskontor utgående riksdags- och revisionskostnader,
#             aflöriingar, för<br /> </span>"""
#     )

#     texts_or_elems = div_dok_extract_text_br_and_tail(elem)

#     assert (
#         texts_or_elems[0]
#         == """Från Riksgäldskontor utgående riksdags- och revisionskostnader,
#             aflöriingar, för"""
#     )
#     assert_elem_equal(texts_or_elems[1], etree.Element("br"))
#     assert texts_or_elems[2] is None


@pytest.mark.parametrize(
    "source, expected",
    [
        (
            """<p class="line" style="font-size: 0.65em">Från Riksgäldskontor</p>""",
            """<p>Från Riksgäldskontor</p>""",
        ),
        (
            """<span class="line" style="font-size: 0.65em">Från Riksgäldskontor</span>""",
            """<p>Från Riksgäldskontor</p>""",
        ),
        (
            """<span class="line" style="font-size: 0.65em">Från<br /> Riksgäldskontor</span>""",
            """<p>Från<br /> Riksgäldskontor</p>""",
        ),
        (
            """<p><span class="line" style="font-size: 0.65em">Från<br /> Riksgäldskontor</span></p>""",
            """<p>Från<br /> Riksgäldskontor</p>""",
        ),
        (
            """<p style="margin-left: 40px"><span class="line" style="font-size: 0.65em">Från Riksgäldskontor utgående riksdags- och revisionskostnader,
             aflöriingar, för<br /> </span><span class="line" style="font-size: 0.85em">valtningsutgifter m. m. §§
             21—31.</span></p>""",
            """<p>Från Riksgäldskontor utgående riksdags- och revisionskostnader,
             aflöriingar, för<br />  valtningsutgifter m. m. §§
             21—31.</p>""",
        ),
    ],
)
def test_extract_paragraph_recursive(source: str, expected: str):
    print("arrange")
    elem = etree.fromstring(source)
    print_tree(elem)

    print("act")
    actual = extract_paragraph_recursive(elem)

    print("assert")
    print_tree(actual)
    expected = etree.fromstring(expected)
    print("assert:expected")
    print_tree(expected)
    assert_elem_equal_no_trim(actual, expected)


PAGE_SOURCES = [
    """<div class="pageWrap"><div class="sida">  <div class="block" style="top:197px;left:198px">  <p style="margin-left:3px;"><span class="line " style="font-size:1.2em">REGLEMENTE</span></p> </div>    <div class="block" style="top:342px;left:288px">  <p style="margin-left:3px;"><span class="line " style="font-size:1.0em">FÖR</span></p> </div>    <div class="block" style="top:467px;left:75px">  <p><span class="line " style="font-size:1.2em">RIKSGÄLDS-KONTORET,</span></p> </div>    <div class="block" style="top:606px;left:141px">  <p style="margin-left:3px;"><span class="line " style="font-size:1.0em">utfärda (It vid slutet af 1887 års riksdag.</span></p> </div>    <div class="block" style="top:773px;left:316px">  </div>    <div class="block" style="top:779px;left:271px">  </div>  </div></div>""",  # noqa: E501
    """<div class="pageWrap">
    <div class="sida">
      <div class="block" style="top: 131px; left: 99px">
        <p>
          <span class="line" style="font-size: 0.65em">Till låneunderstöd för enskilda jernvägar har 1881 års Rikslag
            beviljat och<br /> </span><span class="line" style="font-size: 0.65em">stält till Kongl. Maj:ts disposition
            ett extra anslag åt 5,000,000
            kronor, att utgå<br /> </span><span class="line" style="font-size: 0.65em">under fem år från och med år 1882
            med 1,000,000 kronor årligen,
            dock så<br /> </span><span class="line" style="font-size: 0.65em">att belopp, som ej blifvit till utgående
            under ett af dessa år
            anvisadt, må för ett<br /> </span><span class="line" style="font-size: 0.65em">efterföljande år af samma
            femårsperiod disponeras, egande Kongl.
            Maj:t att å<br /> </span><span class="line" style="font-size: 0.65em">detta anslag till understödjande af
            nya, ännu ej påbörjade enskilda
            jeruvägsanläggniugar <br /></span><span class="line" style="font-size: 0.65em">anvisa af .Kong], Maj:t
            beviljade uuderstödsbelopp, att utgå i
            enlighet <br /></span><span class="line" style="font-size: 0.85em">med följande vilkor och
            bestämmelser:</span>
        </p>
        <p>
          <span class="line" style="font-size: 0.65em">l:o) att kostnadsförslag och arbetsplan fastställas af Kongl.
            Maj:t, som ock<br /> </span><span class="line" style="font-size: 0.65em">närmare bestämmer de ställen,
            hvilka jernväg skall beröra, varande
            det sökande<br /> </span><span class="line" style="font-size: 0.65em">bolaget skyldigt att godtgöra de
            särskilda kostnader för möjligen
            erforderliga besigtningar,<br /></span><span class="line" style="font-size: 0.65em">
            extra biträdens användande med mera dylikt, hvilka kunna af
            kostnadsförslaget <br /></span><span class="line" style="font-size: 0.85em">och arbetsplanens granskning
            föranledas;</span>
        </p>
        <p>
          <span class="line" style="font-size: 0.65em">2:o) att låneunderstödet må utgöra högst hälften af
            anläggningskostnaden<br /> </span><span class="line" style="font-size: 0.65em">efter det faststälda
            kostnadsförslaget samt lyftas i mån af
            arbetets fortgång på sätt<br /> </span><span class="line" style="font-size: 0.65em">och å tider, som Kongl.
            Maj:t bestämmer, dock med iakttagande deraf
            att bolagsmännens <br /></span><span class="line" style="font-size: 0.65em">inbetalningar å af dem tecknade
            belopp skola ske i förhållande till
            de<br /> </span><span class="line" style="font-size: 0.65em">andelar af lånesumman, som lyftas, och före
            lyftningen al dessa
            låneandelar; skolande <br /></span><span class="line" style="font-size: 0.65em">härjemte en tiondedel af den
            beviljade låneförsträckningen innestå
            till dess<br /> </span><span class="line" style="font-size: 0.65em">besigtning af jernvägsanläggningen
            blifvit i öfverensstämmelse med
            § 2 mom. 2 al<br /> </span><span class="line" style="font-size: 0.65em">Kongl. kungörelsen den 11 December
            1874, angående ordningen för
            afsyning och<br /> </span><span class="line" style="font-size: 0.65em">besigtning af enskilda jernvägar och
            deras upplåtande för allmän
            trafik, förrättad,<br /> </span><span class="line" style="font-size: 0.65em">och Väg- och
            vattenbyggnadsstyrelsen meddelat tillstånd till banans
            öppnande för<br /> </span><span class="line" style="font-size: 0.85em">allmän trafik;</span>
        </p>
        <p>
          <span class="line" style="font-size: 0.65em">3:o) att det lånesökande bolaget, för att kunna erhålla
            statsunderstöd, skall<br /> </span><span class="line" style="font-size: 0.65em">vara skyldigt hos Kongl.
            Maj:t styrka, att det förfogar öfver ett
            kapital, som jemte<br /> </span><span class="line" style="font-size: 0.65em">statslånet är fullt
            tillräckligt till jernvägsanläggningens
            utförande på sätt arbetsplan <br /></span><span class="line" style="font-size: 0.65em">och kostnadsförslag
            innehålla och hvaraf minst så stor del, som
            motsvarar<br /> </span><span class="line" style="font-size: 0.65em">hälften af den beräknade
            anläggningskostnaden, bör utgöras af
            tecknadt eller inbetaldt <br /></span><span class="line" style="font-size: 0.65em">aktiebelopp eller eljest
            utan återbetalningsskyldighet lemnadt
            tillskott till<br /> </span><span class="line" style="font-size: 0.85em">jernvägsanläggningens
            utförande;</span>
        </p>
        <p>
          <span class="line" style="font-size: 0.65em">4:o) att i afseende å ifrågavarande försträckningar skall
            iakttagas:</span>
        </p>
        <p>
          <span class="line" style="font-size: 0.65em">a) att annuiteten beräknas till fem procent å ursprungliga
            försträckningsbeloppet,<br /></span><span class="line" style="font-size: 0.65em">
            af hvilken annuitet först godtgöres ränta efter lyra och en half för
            hundra<br /> </span><span class="line" style="font-size: 0.65em">å oguldet kapitalbelopp, och återstoden
            utgör afbetalning
            derå;</span>
        </p>
        <p>
          <span class="line" style="font-size: 0.65em">b) att räntefrihet ej må beviljas, men anstånd med räntans
            erläggande medgifvas <br /></span><span class="line" style="font-size: 0.65em">för högst tre år, dock icke
            utöfver ett år från den dag, då, enligt
            Kongl.<br /> </span><span class="line" style="font-size: 0.65em">Maj:ts bestämmande, jernväg senast skall
            vara färdig och för trafik
            öppnad; sko-</span>
        </p>
      </div>
    </div>
  </div>""",
    """<div class="pageWrap">
    <div class="sida">
    <div class="block" style="top:43px;left:547px"> <p><span class="line " style="font-size:0.85em">43</span></p></div>  <div class="block" style="top:348px;left:279px"> <p><span class="line " style="font-size:0.90em">Bil. A,</span></p></div>  <div class="block" style="top:416px;left:78px"> <p><span class="line " style="font-size:0.65em">Riksgäldskontorets vid 1886 års slut utbalanserade kapitalskulder.</span></p></div>
    <div class="block" style="top:463px;left:-7px">
    <table class="skannad">
      <tr>
        <td><p><span class="line " style="font-size:0.75em">Reglemen-</span></p> <p><span class="line " style="font-size:0.75em">tets</span></p> </td>
          <td><p /> </td>
          <td><p style="margin-left:8px;"><span class="line " style="font-size:0.75em">Tiden, då för-</span></p> </td>
          <td><p style="margin-left:10px;" /> </td>
          <td><p><span class="line " style="font-size:0.85em">Återstående kapitalskuld dén 31 December<br />  </span><span class="line " style="font-size:0.75em">1886.</span></p> </td> </tr><tr><td><p /> </td>
          <td><p><span class="line " style="font-size:0.75em">bindelserna biff-</span></p> </td>
          <td><p style="margin-left:10px;"><span class="line " style="font-size:0.75em">Räntefot.</span></p> </td>
          <td><p /> </td>
          <td><p style="margin-left:13px;" /> </td> </tr><tr><td><p /> </td>
          <td><p /> </td>
          <td><p /> </td>
          <td><p style="margin-left:8px;"><span class="line " style="font-size:0.75em">vit utfärdade.</span></p> </td>
          <td><p /> </td>
          <td><p style="margin-left:13px;" /> </td> </tr><tr><td><p><span class="line " style="font-size:0.80em">Årtal.</span></p> </td>
          <td><p><span class="line " style="font-size:0.80em">§■</span></p> </td>
          <td><p /> </td>
          <td><p style="margin-left:10px;" /> </td>
          <td><p><span class="line " style="font-size:0.75em">Fonderad skuld.</span></p> </td>
          <td><p><span class="line " style="font-size:0.75em">loke fonderad<br />  </span><span class="line " style="font-size:0.75em">skuld.</span></p> </td> </tr><tr><td><p><span class="line " style="font-size:0.80em">1866</span></p> </td>
          <td><p><span class="line " style="font-size:0.80em">5</span></p> </td>
          <td><p style="margin-left:9px;"><span class="line " style="font-size:0.85em">Skulden för 1860 års pre-</span><span class="line " style="font-size:0.80em">mielån mot obligationer å<br />  </span><span class="line " style="font-size:0.85em">2,400,000 Thlr Pr. C:t, bok-</span><span class="line " style="font-size:0.85em">förda till fem sjettedelar<br />  </span><span class="line " style="font-size:0.80em">deraf, eller 2,000,000 Thlr</span></p> </td>
          <td><p style="margin-left:8px;"><span class="line " style="font-size:0.85em">1860 d. i/5</span></p> </td>
          <td><p style="margin-left:10px;" /> </td>
          <td><p><span class="line " style="font-size:0.85em">Thlr 597,083 Va</span></p> </td>
          <td><p style="margin-left:13px;" /> </td> </tr><tr><td><p><span class="line " style="font-size:0.80em">1872</span></p> </td>
          <td><p><span class="line " style="font-size:0.80em">83</span></p> </td>
          <td><p style="margin-left:9px;"><span class="line " style="font-size:0.80em">Obligationer för 1872 års<br />  </span><span class="line " style="font-size:0.85em">jernvägslån å 24,000,000<br />  </span><span class="line " style="font-size:0.80em">R:dr</span></p> </td>
          <td><p style="margin-left:8px;"><span class="line " style="font-size:0.80em">1872 d. 3»/a</span></p> </td>
          <td><p style="margin-left:18px;"><span class="line " style="font-size:0.75em">4</span></p> </td>
          <td><p style="margin-left:13px;" /> </td> </tr><tr><td><p><span class="line " style="font-size:0.80em">Er. 19,380,200</span></p> </td> </tr><tr><td><p /> </td>
          <td><p /> </td>
          <td><p /> </td>
          <td><p style="margin-left:10px;" /> </td>
          <td><p style="margin-left:13px;" /> </td> </tr><tr><td><p><span class="line " style="font-size:0.80em">1875</span></p> </td>
          <td><p><span class="line " style="font-size:0.80em">35</span></p> </td>
          <td><p style="margin-left:9px;"><span class="line " style="font-size:0.80em">Obligationer för 1875 års</span></p> </td>
          <td><p /> </td>
          <td><p style="margin-left:10px;" /> </td>
          <td><p style="margin-left:13px;" /> </td> </tr><tr><td><p><span class="line " style="font-size:0.80em">1876</span></p> </td>
          <td><p><span class="line " style="font-size:0.80em">33</span></p> </td>
          <td><p style="margin-left:9px;"><span class="line " style="font-size:0.85em">jernvägslån å 56,250,000</span></p> </td>
          <td><p /> </td>
          <td><p style="margin-left:10px;" /> </td>
          <td><p /> </td>
          <td><p style="margin-left:13px;" /> </td> </tr><tr><td><p><span class="line " style="font-size:0.80em">1878</span></p> </td>
          <td><p><span class="line " style="font-size:0.80em">39</span></p> </td>
          <td><p style="margin-left:9px;"><span class="line " style="font-size:0.80em">Rmk, deraf till 1886 års</span></p> </td>
          <td><p /> </td>
          <td><p style="margin-left:10px;" /> </td>
          <td><p /> </td>
          <td><p style="margin-left:13px;" /> </td> </tr><tr><td><p><span class="line " style="font-size:0.80em">1879</span></p> </td>
          <td><p><span class="line " style="font-size:0.85em">15</span></p> </td>
          <td><p style="margin-left:9px;"><span class="line " style="font-size:0.85em">slut blifvit utlemnade en</span></p> </td>
          <td><p /> </td>
          <td><p style="margin-left:10px;" /> </td>
          <td><p /> </td>
          <td><p style="margin-left:13px;" /> </td> </tr><tr><td><p><span class="line " style="font-size:0.80em">1880</span></p> </td>
          <td><p><span class="line " style="font-size:0.80em">38</span></p> </td>
          <td><p style="margin-left:9px;"><span class="line " style="font-size:0.85em">första emission å 20,250,000</span></p> </td>
          <td><p /> </td>
          <td><p style="margin-left:10px;" /> </td>
          <td><p /> </td>
          <td><p style="margin-left:13px;" /> </td> </tr><tr><td><p><span class="line " style="font-size:0.80em">1881</span></p> </td>
          <td><p><span class="line " style="font-size:0.80em">41</span></p> </td>
          <td><p style="margin-left:9px;"><span class="line " style="font-size:0.85em">Rmk, en andra emission å<br />  </span><span class="line " style="font-size:0.80em">18,000,000 Rmk samt af en<br />  </span><span class="line " style="font-size:0.85em">tredje emission, å likaledes<br />  </span><span class="line " style="font-size:0.85em">18,000,000 Rmk, obligatio-</span><span class="line " style="font-size:0.85em">ner å 3,241,800 Rmk</span></p> </td>
          <td><p style="margin-left:8px;"><span class="line " style="font-size:0.85em">1875 d. 2/8</span></p> </td>
          <td><p style="margin-left:10px;"><span class="line " style="font-size:0.85em">4 ’/2 %</span></p> </td>
          <td><p><span class="line " style="font-size:0.85em">Rulle 39,692,700</span></p> </td>
          <td><p style="margin-left:13px;" /> </td> 
        </tr>
    </table></div>
    <div class="block" style="top:978px;left:62px">  
      <p><span class="line " style="font-size:0.65em">Bill. till RiJcsd. Prat. 18S7. B. 10 Sami. 1 Åfd. 2 Band.</span></p> <p style="margin-left:19px;"><span class="line " style="font-size:0.75em">(Riksg.-kontorets reglemente.)</span></p>
      </div>
      </div>
      </div>""",
]
EXPECTED_SOURCES = [
    """<page><p>REGLEMENTE</p> <p>FÖR</p> <p>RIKSGÄLDS-KONTORET,</p> <p>utfärda (It vid slutet af 1887 års riksdag.</p> </page>""",  # noqa: E501
    """<page>
        <p>
          Till låneunderstöd för enskilda jernvägar har 1881 års Rikslag
            beviljat och<br /> stält till Kongl. Maj:ts disposition
            ett extra anslag åt 5,000,000
            kronor, att utgå<br /> under fem år från och med år 1882
            med 1,000,000 kronor årligen,
            dock så<br /> att belopp, som ej blifvit till utgående
            under ett af dessa år
            anvisadt, må för ett<br /> efterföljande år af samma
            femårsperiod disponeras, egande Kongl.
            Maj:t att å<br /> detta anslag till understödjande af
            nya, ännu ej påbörjade enskilda
            jeruvägsanläggniugar <br />anvisa af .Kong], Maj:t
            beviljade uuderstödsbelopp, att utgå i
            enlighet <br />med följande vilkor och
            bestämmelser:
        </p>
        <p>
          l:o) att kostnadsförslag och arbetsplan fastställas af Kongl.
            Maj:t, som ock<br /> närmare bestämmer de ställen,
            hvilka jernväg skall beröra, varande
            det sökande<br /> bolaget skyldigt att godtgöra de
            särskilda kostnader för möjligen
            erforderliga besigtningar,<br />
            extra biträdens användande med mera dylikt, hvilka kunna af
            kostnadsförslaget <br />och arbetsplanens granskning
            föranledas;
        </p>
        <p>
          2:o) att låneunderstödet må utgöra högst hälften af
            anläggningskostnaden<br /> efter det faststälda
            kostnadsförslaget samt lyftas i mån af
            arbetets fortgång på sätt<br /> och å tider, som Kongl.
            Maj:t bestämmer, dock med iakttagande deraf
            att bolagsmännens <br />inbetalningar å af dem tecknade
            belopp skola ske i förhållande till
            de<br /> andelar af lånesumman, som lyftas, och före
            lyftningen al dessa
            låneandelar; skolande <br />härjemte en tiondedel af den
            beviljade låneförsträckningen innestå
            till dess<br /> besigtning af jernvägsanläggningen
            blifvit i öfverensstämmelse med
            § 2 mom. 2 al<br /> Kongl. kungörelsen den 11 December
            1874, angående ordningen för
            afsyning och<br /> besigtning af enskilda jernvägar och
            deras upplåtande för allmän
            trafik, förrättad,<br /> och Väg- och
            vattenbyggnadsstyrelsen meddelat tillstånd till banans
            öppnande för<br /> allmän trafik;
        </p>
        <p>
          3:o) att det lånesökande bolaget, för att kunna erhålla
            statsunderstöd, skall<br /> vara skyldigt hos Kongl.
            Maj:t styrka, att det förfogar öfver ett
            kapital, som jemte<br /> statslånet är fullt
            tillräckligt till jernvägsanläggningens
            utförande på sätt arbetsplan <br />och kostnadsförslag
            innehålla och hvaraf minst så stor del, som
            motsvarar<br /> hälften af den beräknade
            anläggningskostnaden, bör utgöras af
            tecknadt eller inbetaldt <br />aktiebelopp eller eljest
            utan återbetalningsskyldighet lemnadt
            tillskott till<br /> jernvägsanläggningens
            utförande;
        </p>
        <p>
          4:o) att i afseende å ifrågavarande försträckningar skall
            iakttagas:
        </p>
        <p>
          a) att annuiteten beräknas till fem procent å ursprungliga
            försträckningsbeloppet,<br />
            af hvilken annuitet först godtgöres ränta efter lyra och en half för
            hundra<br /> å oguldet kapitalbelopp, och återstoden
            utgör afbetalning
            derå;
        </p>
        <p>
          b) att räntefrihet ej må beviljas, men anstånd med räntans
            erläggande medgifvas <br />för högst tre år, dock icke
            utöfver ett år från den dag, då, enligt
            Kongl.<br /> Maj:ts bestämmande, jernväg senast skall
            vara färdig och för trafik
            öppnad; sko-
        </p>
  </page>""",
    """<page>
    <p>43</p>
    <p>Bil. A,</p>
    <p>Riksgäldskontorets vid 1886 års slut utbalanserade kapitalskulder.</p>
    <table class="removed"/>
    <p>Bill. till RiJcsd. Prat. 18S7. B. 10 Sami. 1 Åfd. 2 Band.</p> 
    <p>(Riksg.-kontorets reglemente.)</p>
    </page>""",
]


@pytest.mark.parametrize(
    "source, expected",
    [
        (PAGE_SOURCES[0], EXPECTED_SOURCES[0]),
        (PAGE_SOURCES[1], EXPECTED_SOURCES[1]),
        (PAGE_SOURCES[2], EXPECTED_SOURCES[2]),
    ],
)
def test_div_dok_extract_page(source: str, expected: str):
    print("arrange")
    elem = etree.fromstring(source)
    # print_tree(elem)

    print("act")
    actual = div_dok_extract_page(elem)
    cleaning.clean_element(actual)
    print("assert")
    print_tree(actual, verbose=True)
    expected = etree.fromstring(expected)
    print("assert:expected")
    print_tree(expected, verbose=True)
    assert_elem_equal(actual, expected)
