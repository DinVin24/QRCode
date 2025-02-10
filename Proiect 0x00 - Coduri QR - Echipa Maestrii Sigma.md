## Cuprins
- [Despre coduri QR](#despre-coduri-qr)
  - [Tehnologii noi aduc oportunitati noi de frauda](#tehnologii-noi-aduc-oportunitati-noi-de-frauda)
- [Cum a inceput](#cum-a-inceput)
- [Abordare limbaje librarii utilizate](#abordare-limbaje-librarii-utilizate)
- [Surse de inspiratie](#surse-de-inspiratie)
- [Generarea codului QR](#generarea-codului-qr)
  - [Generarea sirului de biti](#generarea-sirului-de-biti)
    - [Analiza caracterelor Unicode](#analiza-caracterelor-unicode)
    - [Crearea segmentelor de date](#crearea-segmentelor-de-date)
    - [Alegerea versiunii QR si adaptarea la capacitate](#alegerea-versiunii-qr-si-adaptarea-la-capacitate)
    - [Combinarea segmentelor adaugarea de padding si codificarea finala](#combinarea-segmentelor-adaugarea-de-padding-si-codificarea-finala)
    - [Adaugarea codurilor de corectie de eroare ECC](#adaugarea-codurilor-de-corectie-de-eroare-ecc)
  - [Crearea matricii](#crearea-matricii)
- [Decodarea si citirea codului QR](#decodarea-si-citirea-codului-qr)
  - [Procesarea imaginii](#procesarea-imaginii)
  - [Interpretarea propriu-zisa](#interpretarea-propriu-zisa)
- [Interfetele pentru utilizare](#interfetele-pentru-utilizare)
  - [Implementarea serverului HTTP](#implementarea-serverului-http)
    - [Mediul de rulare](#mediul-de-rulare)
    - [Cereri GET POST](#cereri-get-post)
    - [Comunicarea cu serviciile externe](#comunicarea-cu-serviciile-externe)
  - [Website](#website) - [http://maestrusigma.lol](http://maestrusigma.lol)
    - [Servirea datelor in pagina](#servirea-datelor-in-pagina)
  - [Joc](#joc) - [https://www.roblox.com/games/75361227921023/QR-ASC](https://www.roblox.com/games/75361227921023/QR-ASC)
    - [Procesul de creatie](#procesul-de-creatie)
    - [Implementarea scripturilor](#implementarea-scripturilor)
    - [Interactiunea cu serverul](#interactiunea-cu-serverul)
    - [Afisarea datelor](#afisarea-datelor)


## Despre coduri QR

[Codurile QR (quick response)](https://en.wikipedia.org/wiki/QR_code) au fost inventate in 1994 de [Masahiro Hara](https://en.wikipedia.org/wiki/Masahiro_Hara). Deoarece codurile de bare nu puteau stoca prea multa informatie (ceea ce este esential in ziua de azi) , oamenilor le-a venit ideea de a crea un cod de bare bidimensional. In final, dupa mai multe idei, ne-am ales cu codurile QR pe care le iubim si indragim si de care nu ne mai despartim.
La inceput acestea erau menite pentru depozite care trebuiau sa tina evidenta a mai multor proprietati ale mai multor produse.
Deoarece puteau stoca multa informatie, au inceput sa fie adoptate si de restul populatiei (care nu lucreaza intr-un depozit) pentru a distribui link-uri catre site-uri, aplicatii, profile de retele de socializare etc.
In ziua de azi, toata lumea are un telefon, orice telefon are o camera, iar orice telefon vine deja echipat cu un software de decodare al codurilor QR. Astfel codurile au devenit din ce in ce mai accesibile. Totodată, datorită distanțării sociale și altor măsuri de precauție din timpul pandemiei, codurile QR nu mai erau doar o scurtatura la un link, ci o parte esențială a vieții noastre (de exemplu au înlocuit meniurile fizice in majoritatea restaurantelor)

#### Tehnologii noi aduc oportunități noi de fraudă

Unii oameni au luat ca avantaj faptul ca noi nu stim ce se afla in spatele unui cod QR pana nu il scanam. Astfel ei inlocuiesc codul QR dintr-un loc public cu un cod QR care duce spre un site asemanator dar malițios. Imaginați-vă că scanați codul QR al unei parcări pentru a o plăti, dar de fapt link-ul pe care ai fost trimis duce spre un site care seamana cu cel corespunzător, dar redirectioneaza plata spre contul unui infractor. Acesta este doar unul din multele exemple cum codurile QR pot fi folosite pentru a frauda. [Mai multe informatii](https://www.cnb.com/personal-banking/insights/qr-code-fraud.html)
Sfatul meu este sa scanati codurile QR cu prudenta si sa le tratati ca orice link suspicios (guilty until proven innocent).


## Cum a inceput?

Totul a inceput, fireste, in momentul in care a fost anuntata tema de proiect. Toti dintre noi ne-am fi dorit sa abordam acest proiect, insa o echipa nu se formase la momentul respectiv. Cu toate acestea, la nivel individual ni s-a parut o idee buna datorita nivelului de practicabilitate in viata de zi cu zi si chiar am devenit interesati sa aflam cum functioneaza codurile QR. 

Intr-o buna zi (din pacate in timpul sesiunii de examene) chiar dupa ce am dat un examen, ne-am strans impreuna ca sa stam de vorba si sa ne plimbam. Intre timp, ne-am hotarat sa abordam acest proiect, cu toate ca parea usor intimidant. Am inceput sa discutam ce implica acesta si care ar fi strategia din urmatoarele zile. Facusem o decizie, insa nivelul de motivatie nu era asa de ridicat, pana cand cineva vine cu ideea:

**-Cat de amuzant ar fi sa desenam codul QR intr-un joc?**

Pentru cateva momente, toti am fost putin bulversati de idee, dar in acelasi timp, am crezut ca e o idee foarte buna.

**-Pai cum adica?**

**-Pai cum ar fi sa desenam matricea cu blocuri in Minecraft sau ceva de genul?**

Si in acel moment ne-au lovit pe toti, de parca ne-au strafulgerat, o groaza de idei legate de afisare in diverse jocuri. Pana la urma, cea mai indragita varianta a fost sa cream o interfata pe platforma de creat experiente virtuale, [Roblox](https://en.wikipedia.org/wiki/Roblox). Nu aveam nici cea mai vaga idee cum am putea face ce tocmai ne-am gandit, totusi cativa dintre noi s-au familiarizat (cand eram mai mici) cu programul de creat jocuri, [Roblox Studio](https://create.roblox.com/), dar ni s-a parut o idee draguta.


## Abordare (limbaje, librarii utilizate)

Datorita lipsei de restrictii privind limbajele de programare folosite din specificatia proiectului, am ales cel mai indragit limbaj de noi, [Python](https://www.python.org/). Am considerat ca este o alegere excelenta, pentru ca toti ne-am familiarizat foarte mult cu el pe parcurs, este usor de citit si modulele (librariile) pe care le ofera ne-au usurat si ne-au scurtat implementarea o gramada (evident, aceasta tot a fost lunga, pentru ca tot procesul de generare si decodare nu a putut depinde de metode specifice manipularii codurilor QR din librarii). 

Module/librarii Python folosite:
- [Pillow](https://pypi.org/project/pillow/)
- [NumPy](https://numpy.org/)
- [SciPy](https://scipy.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Werkzeug](https://pypi.org/project/Werkzeug/)
- [urllib](https://docs.python.org/3/library/urllib.html)
- [Flask-Cors](https://pypi.org/project/Flask-Cors/)
- [requests](https://pypi.org/project/requests/)
- [copy](https://docs.python.org/3/library/copy.html)
- [re (expresii regulate)](https://docs.python.org/3/library/re.html)
- [sys](https://docs.python.org/3/library/sys.html)
- [os](https://docs.python.org/3/library/os.html)

Un alt limbaj de programare folosit este [Luau](https://create.roblox.com/docs/luau), limbajul de scriptare in crearea jocurilor pe Roblox. Acesta a fost esential pentru implementarea functionalitatii in joc.

Pentru website, au fost folosite [HTML](https://html.spec.whatwg.org/multipage/), [CSS](https://www.w3.org/Style/CSS/Overview.en.html) si [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript). Folosind metodele invatate la materia de semestrul acesta, [Tehnici Web](https://cs.unibuc.ro/~cechirita/tw/), am reusit sa punem la cale o interfata draguta pentru utilizatorii programelor de generare si decodare. *Si da, aspectul site-ului este intentionat* 😊


## Surse de inspiratie

Fara anumite ghiduri puse foarte bine la punct, nu am fi avut nici o sansa sa ducem pana la capat acest proiect. Asa ca, multumim foarte mult celor ce urmeaza ca ne-au ghidat spre calea cea buna:

[Ghidul lui Nayuki](https://www.nayuki.io/page/creating-a-qr-code-step-by-step)
[Ghidul lui Thonky](https://www.thonky.com/qr-code-tutorial/)

De asemenea, multumim fiecarui membru al echipei ca a respectat atributiile sale si a adus contributii grozave in zona sa de lucru a proiectului!


## Generarea codului QR

### Generarea sirului de biti

#### Analiza caracterelor Unicode

Se analizează fiecare caracter din text, stabilindu-se codul Unicode.
Se determină dacă șirul de caractere poate fi codificat în cel mai bun mod (Numeric, Alfanumeric, Byte, Kanji).

#### Crearea segmentului de date

Pentru modul Numeric și Alfanumeric, se grupează caracterele consecutive. Restul se păstrează așa.
Se transformă fiecare grup de caractere într-o secvență de biți.
Se returnează o listă de octeți.

##### Alegerea versiunii QR și adaptarea la capacitate

Se verifică într-un dicționar unde încape dimensiunea totală a șirului de biți generat anterior, în funcție și de Error Correction. Ca să încapă, lungimea trebuie să fie mai mică decât ce e în dicționar.

##### Combinarea segmentelor, adăugarea de padding și codificarea finală

Se adaugă metadate, cum ar fi:
	-Modul de codificare 
	-Numărul de caractere 
În continuare, se adaugă biți până când este atinsă capacitatea maximă calculată conform versiunii și ECL (Error Correction Level).
Se adaugă terminatorul (4 biți sau mai puțin).
Se adaugă bit padding pentru a avea octeți compleți.
Se adaugă și byte padding, care este format din 0xEC și 0x11, alternant.

##### Adăugarea codurilor de corecție de eroare (ECC)

Se creează tabele de exponent și logaritm pentru operații în câmpul finit GF(256) (Galois Field). Aceste tabele sunt esențiale pentru operațiile de multiplicare și împărțire utilizate în codificarea Reed-Solomon.
Se obține lista de numere generată anterior, grupată în bytes.
Se determină dintr-un dicționar în câte blocuri trebuie împărțit textul și ce lungime are fiecare, în funcție de ECL și versiunea textului.
Se împart datele în blocuri conform regulilor stabilite.

Se determină dintr-un dicționar numărul de cuvinte ECC (Error Correction Codewords).
Codificarea Reed-Solomon tratează mesajul ca un polinom peste un câmp finit.
Mesajul original este văzut ca un polinom P(x), unde coeficienții sunt numerele din lista de numere generată.

Se generează un polinom generator g(x) de grad n, care este folosit pentru a calcula codurile de corecție a erorilor.
Se extinde mesajul prin împărțirea polinomului la generator:
$$
P(x) \cdot x^n \mod g(x)
$$
Rezultatul este restul împărțirii, care reprezintă cuvintele ECC.

Se amestecă blocurile de date astfel încât să fie distribuite uniform în codul QR.
Se intercalează și blocurile ECC.

Se concatenează datele intercalate și cuvintele ECC intercalate.
Fiecare valoare este transformată într-o secvență de bytes, creând astfel codificarea finală a textului.

Returnează șirul binar final, care este format din:

Se returnează șirul binar final, care este format din:

-Datele inițiale transformate
-Cuvintele de corecție a erorilor (ECC)
-Toate aranjate în blocuri intercalate

Această secvență binară este exact ceea ce este necesar pentru a construi matricea.


### Crearea matricei

Deoarece un text plin de 0 si 1 este greu si obositor de citit, am implementat cu ajutorul librăriei Pillow o funcție care generează o imagine conform matricei, unde 1 - negru, 0 - alb, 8 - gri (marchează spațiile necompletate încă).

Înainte de a introduce biții calculați la pașii anteriori, programul definește o matrice pătratică de lungime  (Versiune - 1) x 4 + 21 , versiune pe care o primim ca parametru de la pașii anteriori.
Pe această matrice creăm un template specific versiunii. Astfel:
	- desenăm cele 3 pătrate specifice în colțuri (finders)
	-  desenăm, după caz, un număr specific de pătrățele de aliniere și la poziții specifice fiecărei versiuni. (alignment patterns)
	- lângă finders, rezervăm loc pentru format bits. Mai mult despre ei vom discuta in rândurile următoare
	- desenăm pe linia și coloana 6 un șir alternativ de 0 și 1 dar fără să suprapunem ce am desenat până acum.
	- lângă finders desenăm totodată un dreptunghi 6x3 care conține informații despre versiunea codului QR (de ce 18 biți pentru un număr care poate fi reprezentat pe 6? Restul sunt de error correction, în cazul in care vreunul din cei 6 nu au fost citiți corect) (prezent doar de la versiunile 7-40 ) 
	- până în acest punct, matricea noastră arată ca orice alt cod QR de această versiune. Avem nevoie de acest template așadar îl salvăm într-o variabilă numită destul de sugestiv.
	- pentru a salva biții propriu-ziși, calculăm mai întâi traseul zig-zag și care să nu dea overwrite la ”obstacole” apoi va fi memorat într-o listă. 
	- salvăm, conform listei, șirul de biți calculat la partea anterioara și transmis ca parametru.
	- următorul pas este să aplicăm masca cea mai ”eficientă” pentru codul nostru. Acest pas presupune să testăm fiecare mască, îi acordăm un scor pentru ”greșeli” (ex: prea multe linii continue) iar cea cu scorul cel mai bun rămâne aplicată.
	- Ca masca sa nu dea overwrite la părțile elementare desenate pe matricea noastră, folosim template-ul salvat cu câțiva pași înainte. (Codul poate fi citit indiferent de orice mască este aplicată. Măștile sunt pentru a evita erori care pot apărea la image processing)
	- După ce ne-am hotărât asupra unei măști, trebuie să memorăm informații despre aceasta și nivelul de corectare al erorilor ales la început (L, M, Q, H). Aceștia sunt acei format bits menționați la ânceput. Aceștia se calculează într-un mod asemănător cu biții care rețin versiunea codului QR.
	- în final, umplem cu 0 pătratele care încă n-au fost ocupate și adăugăm un mic padding ca să asigurăm o citire corectă a codului.
	- Rezultatul (o matrice care conține 0  și 1 conform codului QR) va fi returnat de funcția principală.

## Decodarea / citirea codului QR


### Procesarea imaginii

Programul primeste ca parametru path-ul catre imaginea de interpretat. Cu ajutorul librariei Pillow, imaginea este accesata, convertita intr-o imagine alb/negru.
Cu ajutorul librariei numpy, se creaza o matrice in care fiecarui element ii corespunde culoarea (0-255) de pe pixelul respectiv. Deoarece nu avem nevoie de valori asa de mari,  elementele <=128 primesc valoarea 1 (negru), restul 0 (alb). Asfel facem rost de o matrice la fel de mare ca imaginea noastra, plina de 1 si 0.
In continuare, vom sterge padding-ul din matrice, aceasta va ramane doar cu portiunea relevanta decodarii codului QR.

Partea cea mai enervanta este interpretarea matricei. Dintr-un oarecare motiv, numarul de pixeli ocupat de aceasta uneori nu este divizibil cu o marime corespunzatoare versiunii codului QR.
In continuare vom spune că un pătrățel 1x1 negru/alb reprezintă un modul, pentru a nu crea confuzie cu pixelii.
De pe primul rand al matricei, numărăm câți pixeli negri consecutivi avem, pana la aparitia unuia alb. Acelasi lucru il facem pentru prima coloana. Cele doua valori reprezinta coordonatele in care incep timing patterns (modulele care alterneaza intre 0 si 1). Numaram cati timing patterns avem si adunam 14 la acel numar. Acesta reprezinta size-ul codului QR

In final, compresam matricea noastra, impartind numarul de pixeli la valoarea calculata anterior. 
In matricea compresata, valoarea fiecarui element reprezinta valoarea fiecarui modul in imaginea noastra. Din nou, pot aparea erori, astfel luam un interval de valori din matricea noastra originala iar valoarea care apare de cele mai multe ori o salvam in matricea noastra compresata.

Returnam matricea obtinuta, care reprezinta codul QR si o interpretam.

### Interpretarea propriu-zisa

Dupa ce imaginea noastra a fost convertita intr-o matrice corespunzatoare, vrem sa aflam informatiile specifice acesteia
	- Aflam versiunea codului QR numarand pixelii si aplicand formula V = ( size - 21 ) // 4 + 1
	- Citim modulele care retin nivelul de corectare al erorilor si masca aplicata
	- ”demascam” matricea folosind template-ul si algoritmul scris la crearea unui cod QR
	- Calculam traseul in care au fost salvati biții folosind apeland functia scrisa la crearea codului QR, apoi salvam in ordine corespunzatoare biții intr-un string.
	- Inlaturam biții pentru Error Correction
	- Deoarece la encodarea codului QR, biții sunt puși in codewords, care la rândul lor sunt puși in block-uri care la randul lor sunt puși in grupe, iar apoi sunt toți intercalați, trebuie să cream o matrice care reprezinta aceasta configuratie.
	- Dupa ce am reusit sa salvam biții din string in matricea anterioara, ii citim in ordine ( ”dez-intercalam” )
	- In final, din sirul de biti rezultat stergem padding-urile si interpretam fiecare byte cu un caracter. 
Rezultatul final este apoi returnat de functia noastra principala.


## Interfetele pentru utilizare


### Implementarea serverului HTTP

Multi s-ar intreba, de ce? De ce a fost nevoie macar de un server?

Ei bine, serverul joaca un rol esential in **primirea si trimiterea datelor**. Respectiv, pentru a comunica cu [website-ul](http://maestrusigma.lol) si cu [jocul](https://www.roblox.com/games/75361227921023/QR-ASC).

Prima data ne-am gandit: hmmm, daca avem un program in Python, cum putem sa rulam sa zicem o functie din Python, sa-i trimitem un parametru **din** si sa primim rezultatul **in** alte limbaje de scriptare ([Luau](https://create.roblox.com/docs/luau), [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)), ca sa il folosim ulterior pentru afisare? 

Ei bine... am fost loviti de realizarea ca nu este chiar asa de banal. Ideea ne-a venit uitandu-ne la documentatia Roblox Studio si vazand un serviciu al jocului care poate rula pe fundal, [HttpService](https://create.roblox.com/docs/reference/engine/classes/HttpService). Cand am vazut asta, ne-au sunat cativa clopotei, deoarece am folosit (si am invatat si pentru examen) fix acelasi lucru [pentru trimiterea, procesarea si primirea datelor, folosind AJAX si promisiuni](https://cs.unibuc.ro/~cechirita/tw/c10/#/70), Roblox oferind o interfata familiara pentru acest schimb de date.

#### Mediul de rulare

Cu toate acestea, avand experienta in lucrul cu masini care au instalate sisteme de operare bazate pe Unix, am vrut sa legam cunostiintele dobandite, setand un [Virtual Private Server](https://cloud.google.com/learn/what-is-a-virtual-private-server?hl=en), folosind serviciul Google Cloud si o masina virtuala (care permit traficul la Internet) [E2 Compute Engine](https://cloud.google.com/compute/docs/general-purpose-machines), accesandu-le in mod convenabil cu [SSH](https://en.wikipedia.org/wiki/Secure_Shell). Acesta va rula o aplicatie WSGI (o interfata mai convenabila si abstractizata de a lucra cu cereri [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)) in permanenta pe server, care asteapta cereri de la clienti (functionalitatea este oferita de [Flask](https://flask.palletsprojects.com/en/stable/)).

#### Cereri GET, POST

Pe portul 80 (destinat serviciului [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP)), serverul va asculta atat cererea paginii web de catre browserele vizitatorilor site-ului, cat si diverse [rute](https://flask.palletsprojects.com/en/stable/api/#flask.Flask.route) pentru a gestiona cererile POST, serverul asteptand primirea datelor in format JSON, pentru a le prelucra si apela functiile implementate in Python (fie primeste plaintext si nivelul de corectare de erori, fie primeste un URL / fisier pentru a-l decoda, ambele avand rutele lor definite), ca apoi sa trimita datele (in cazul nostru, ori o matrice in format JSON, ori plaintext) **inapoi la client-ul care a trimis cererea**.

#### Comunicarea cu serviciile externe

Clientii mentionati anterior pot fi: [site-ul web](http://maestrusigma.lol), si jucatorii care [interactioneaza cu interfata grafica a jocului](https://www.roblox.com/games/75361227921023/QR-ASC).

Site-ul web apeleaza la server prin [API-ul fetch pentru lucrat cu AJAX bazat pe promisiuni valabil in versiunile moderne de JavaScript](https://cs.unibuc.ro/~cechirita/tw/c10/#/70), folosind forme pentru validarea datelor.

Jucatorii, atunci cand apasa pe butoane de trimitere, de fapt trimit cereri POST cu continut JSON pentru a fi procesat. 

### Website

#### Servirea datelor in pagina

Comunicarea cu serverul se realizeaza dupa cum a fost documentata anterior. Insa, pentru servirea paginii web, se trimit de catre browser cereri GET (in mod uzual). Insa, folosind un [domeniu inregistrat](https://en.wikipedia.org/wiki/Domain_name), lucrurine devin mai complicate daca portul implicit pentru servicii [HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) este folosit. Mai intai este trimisa o cerere [OPTIONS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/OPTIONS), care este trimisa de fapt de mecanismul [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) pentru a valida originea primirii datelor si validitatea sa. Din fericire, un modul [Flask](https://flask.palletsprojects.com/en/stable/) numit [Flask-Cors](https://pypi.org/project/Flask-Cors/) ne lasa sa validam aceste verificari pentru fiecare ruta setata, fara a ne chinui cu gestiunea [header-elor cererilor](https://developer.mozilla.org/en-US/docs/Glossary/Request_header) pentru a fi in concordanta cu originile CORS.

De asemenea, utilizatorii site-ului pot incarca fisierul de pe dispozitivul lor, fara a fi nevoiti sa incarce poza cu codul QR pe un [host de fisiere/imagini](https://en.wikipedia.org/wiki/File-hosting_service), spre deosebire de jucatori.

Codul generat este afisat sub forma unui tag [SVG](https://www.w3.org/TR/SVG2/) construit dinamic prin [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript). Codul QR generat este trimis sub forma unei matrice de 0 si 1, pentru care este alocat spatiu in elementul SVG, astfel incat sa fie patratele negre unde este 1 in matrice si patratele albe unde este 0 in matrice.


### Joc

Acum vine partea mult indragita de noi: crearea jocului si interactiunile acestuia cu server-ul si vice versa!
#### Procesul de creatie

Din punct de vedere stilistic, acest aspect nu prea a fost dezvoltat. Totusi, este convenabil de utilizat!

Au existat foarte multe iteratii ale jocului, dar in general, cea finala a aparut dupa ce ne-am chinuit cu [editorul de lume](https://create.roblox.com/docs/get-started) si am decis sa cream fiecare obiect programatic [(prin script-uri)](https://create.roblox.com/docs/scripting) si ulterior sa le modificam dupa caz.

Interfata este simpla: se prezinta cateva butoane in coltul de dreapta jos al ecranului:
- **Snap**: permite jucatorului sa vizualizeze convenabil codul QR (amplasat pe un perete creat dinamic)
- **Plaintext**: permite jucatorului sa genereze un cod QR bazat pe datele introduse (textul de codificat si nivelul de corectare de erori, mic, mediu, quartil sau mare)
- **Photo**: permite jucatorului sa introduca **un URL (link)** la o imagine cu un cod QR, pentru a putea fi decodat, din pacate Roblox nepermitand atasarea fisierelor in joc. Pozele pot fi incarcate folosind un  [host de fisiere/imagini](https://en.wikipedia.org/wiki/File-hosting_service). Pentru testare, noi am folosit [Catbox](https://catbox.moe/).

#### Implementarea script-urilor

Functionalitatea oferita de Roblox Studio pentru a comunica cu obiectele din joc este destul de abstracta, fiind des utilizata paradigma [programarii orientate pe obiecte](https://ro.wikipedia.org/wiki/Programare_orientat%C4%83_pe_obiecte). Ca cu orice limbaj de scripting de altfel, am incercat sa punem piesa cu piesa ceva ce functioneaza, insa paradigma programarii orientate pe obiecte si a dezvoltarii jocurilor (care ne-a pus la dispozitie [event-urile](https://create.roblox.com/docs/scripting/events), schimbarea dinamica a obiectelor si asa mai departe) sunt niste detalii cam plictisitoare, pe care le vom omite deoarece sunt inafara scopului acestui proiect.

Ceva foarte frumos si interesant totusi este functionalitatea butonului **Snap** descris anterior. Scopul acestuia este sa mute camera Player-ului astfel incat sa se incadreze corespunzator in ecran (pentru ca codul sa fie scanat), **indiferent de cat de mare este codul**. Aici am intampinat niste probleme, deoarece trebuia sa gasim un mod de a calcula distanta optima dintre camera si perete in functie de dimensiunea peretelui. Asta suna ca o problema de geometrie, nu?

**Si chiar asa a fost!**
Dupa ceva gandit si inlocuit necunoscute, am gasit o formula pentru calcularea distantei optime:

$$
d = \frac{h}{2} \times \cot\left(\frac{FOV}{2}\right) \times 1.5
$$

**unde d este distanta optima, h este inaltimea peretelui si FOV este unghiul de vizualizare (care este campul pe care il poate vedea camera) al Player-ului.**

Scalarul 1.5 este pentru a incadra cat de cat mai bine peretele (ca sa marginile sale sa nu fie lipite de marginile ferestrei).
#### Interactiunea cu server-ul

Roblox [HttpService](https://create.roblox.com/docs/reference/engine/classes/HttpService) ne ofera o interfata simpla de a trimite cereri si de a transmite date JSON (limbajul Lua foloseste des un mod de stocare asemanator cu cel al datelor in format JSON, sub forma de tabele).

Callback-urile (functiile apelate de butoane) trimit datele folosind [RemoteEvents](https://create.roblox.com/docs/reference/engine/classes/RemoteEvent), acestea dau trigger la functii pentru comunicarea asincrona cu server-ul, si primesc raspunsul folosind acelasi mecanism.

#### Afisarea datelor

Atunci cand jucatorii genereaza coduri QR, acestea sunt afisate local pentru fiecare player (un player nu genera un cod QR vizibil pentru alti playeri pe joc). Un perete este creat si dimensionat in mod dinamic (pentru a desena matricea primita de la server ca raspuns), de care este lipit un [SurfaceGui](https://create.roblox.com/docs/reference/engine/classes/SurfaceGui) in care este calculata intr-un script rezolutia de afisare a matricii si unde sa fie amplasati "pixeli" negri, de dimensiuni egale. 

Se mai ia in considerare si padding pentru cod, pentru a putea fi citit mai bine, si brightness static, care nu este afectat de mediul inconjurator din joc (lumina soarelui, etc.).
