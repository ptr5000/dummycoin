
# Määrittelydokumentaatio

## 1. Johdanto

Dummycoin on yksinkertainen kryptovaluutan ns. proof-of-concept implementaatio. Se 
toteutetaan aikarajatusti priorisioitua tehtävälistaa käyttäen. Kaikkea ei siis välttämättä ehditä.

Implementaatio pohjautuu Bitcoinin alkuperäiseen paperiin Bitcoin: A Peer-to-Peer Electronic Cash System jonka on kirjoittanut Satoshi Nakamoto.

## 2. Käsitteet

Käytettyjä käsitteitä:

*Lohko*: Lohko sisältää viittauksen edelliseen lohkoon. 
*Ketju*: Lohkot muodostavat viittauksilla ketjun. Ketjun ensimmäinen lohko on ns. genesis lohko. Se ei viittaa mihinkään lohkoon.
*Lohkoketju*: Sisältää listan louhituista lohkoista eli transaktioista. 
*Transaktio*: Transaktio on käytännössä arvon siirtoa. Se pitää sisällään kuinka paljon arvoa siirretään. Transaktio sijoitetaan lohkoon. 
*Louhiminen*: Louhimisella varmistetaan transaktioiden oikeellisuus, tätä kautta lohkot päätyvät lohkoketjuun.

## 3. Toiminnalliset vaatimukset

Korkean tason toiminnalliset vaatimukset prioriteettijärjestyksessä

**D-1** Valuuttaa tulee pystyä siirtämään "lompakosta" x "lompakkoon" y (transaktiot) 
**D-2** Lohkoketjun (blockchain) tulee tarjota mahdollisuus transaktioiden tallentamiseen. 
**D-3** Lohkoketjun tulee tarjota mahdollisuus varmistaa transaktioiden oikeellisuus. 
**D-4** Sovelluksen tulee tarjota HTTP-rajapinta transaktioille käyttöliittymää varten. 

## 3. Implementoitavat algoritmit

D-1 vaatimuksen perusteella implementoidaan algoritmit RSA ja SHA-1. Nämä ovat ns. haastavimmat
näillä näkymin. RSA:ta ei varsinaisesti käytetä Bitcoinissa vaan algoritmi on muutamaa
kertaluokkaa haastavampi ECDSA. Projektin tunnit eivät todennäköisesti riitä
ECDSA:n implementoimiseen. Tirassa käytyjä perusrakenteita löytynee myös.

## 4. Käyttöliittymä

Käyttöliittymä on demotarkoitukseen. Sillä pitäisi olla mahdollista tehdä
jonkinlainen arvon siirto esimerkiksi lompakosta toiseen. Se tullaan
implementoimaan HTML5-pohjaisena.

## 5. Testit

Projektissa implementoidaan yksikkötestit oleellisille komponenteille. 
Muilta osin testaus tapahtuu integraatiotestien kautta.  


## X. Lähteet

[1] Bitcoin: A Peer-to-Peer Electronic Cash System, Satoshi Nakamoto, 2008
[2] Blockchain, Wikipedia, https://en.wikipedia.org/wiki/Blockchain [19.1.2018]
[3] Transaction, bitcoinwiki, https://en.bitcoin.it/wiki/Transaction [19.1.2018]
[4] Naivecoin - A cryptocurrency implementation in less than 1500 lines of code, GitHub, https://github.com/conradoqg/naivecoin

