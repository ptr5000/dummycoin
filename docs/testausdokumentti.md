

# Testausdokumentti

Testauksessa on pääasiassa keskitytty integraatiotestien toteuttamiseen. Testit kattavat ns. onnellisen polun kattavasti ja jonkin verran
myös väärinkäytöksiin liittyviä testejä. 

Coverage raportti ja siihen liittyvä tarkempi raportti löytyvät hakemistosta htmlcov. Tässä yhteenveto testien kattavuudesta:


        Name                  Stmts   Miss  Cover
        -----------------------------------------
        lib/__init__.py           0      0   100%
        lib/base64.py            31      0   100%
        lib/blockchain.py        72     14    81%
        lib/rsa.py              120     16    87%
        lib/transaction.py       66     13    80%
        lib/utils.py             10      0   100%
        lib/wallet.py            25      0   100%
        node/__init__.py          0      0   100%
        node/handler.py          32      2    94%
        node/miner.py            43      2    95%
        tests.py                  7      0   100%
        tests/__init__.py         0      0   100%
        tests/base64.py          21      0   100%
        tests/blockchain.py     112      1    99%
        tests/server.py          38      0   100%
        tests/utils.py           21      0   100%
        -----------------------------------------
        TOTAL                   598     48    92%


Testien suorittaminen tapahtuu juurihakemistossa ajamalla komento

        $ python tests.py

## Väärinkäytösten testaaminen

Koska projekti keskittyi virtuaalivaluuttaan, testit keskittyvät myös itse valuutan turvallisuuden testaamiseen. Eli voidaanko sitä varastaa tai yrittää vaikka kuluttaa useampaan kertaan. Testit kattavat tällä hetkellä ainakin seuraavat tapaukset:

    - Toisen omistaman kolikon siirtämisen omaan osoitteseen väärentämällä transaction input arvoja. 
    - Jo käytetyn kolikon uudelleenkäyttö (tämä tosin vaatii vielä lisätestejä jos implementaatioon lisätään hajautus)
    - Olemattoman rahan kulutus    



