# Viikko 3

Projekti etenee; peruslogiikka rahansiirtoon osoitteiden välillä toimii tosin sen testit ovat vielä puutteelliset ja siitä puuttuu
verifiointi (allekirjoitusten tarkastus). Tarkoitukseni on tällä viikolla viimeistellä tuo verifiointiosuus ja aloittaa RSA:n implementointi.
Sitten loppuviikoilla lompakko ja mining (blockchain valmiiksi). Jos ehdin niin jonkinlainen "blockchain explorer" voisi olla kiva demoon.
Sisennyksen tyyliä en edes huomannut katsoa kun otin tähän projektiin käyttöön Visual Studio Coden testimielessä. Tuntuu ihan pätevältä editorilta, vaikka näköjään tabeja defaulttina tarjoaakin. 

Coveragen voi ajaa Coverage.py:llä ainakin. 

    > coverage run tests.py
    > coverage report

    Name                  Stmts   Miss  Cover
    -----------------------------------------
    lib/__init__.py           0      0   100%
    lib/blockchain.py        42      3    93%
    lib/transaction.py       68      2    97%
    lib/utils.py             14      0   100%
    tests.py                  5      0   100%
    tests/__init__.py         0      0   100%
    tests/blockchain.py      47      0   100%
    tests/utils.py           10      0   100%
    -----------------------------------------
    TOTAL                   186      5    97%


Linkki vielä parhaaseen (lue: ainoaan) kirjaan aiheesta mikä on jokseenkin riittävän kattava ja selkeä https://github.com/bitcoinbook/bitcoinbook/. 
