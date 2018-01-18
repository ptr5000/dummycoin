# Viikko 1

Aihe valittu. Ajattelin implementoida oman simppelin kryptovaluutan. En ole täysin varma miten se toimii ja onko tämä lopulta
liian helppo/työläs aihe. Toisaalta aihetta voi kyllä laajentaa ja supistaa joten siinä mielessä uskoisin että tämä menee ihan hyvin.
En oikeastaan tiennyt ennen eilistä aiheesta juuri mitään, sen takia aiheen oikeastaan valitsinkin. Mielenkiintoista nähdä
mitä tästä tulee. Ajattelin rajata aluetta aluksi sen verran, että blockchainista tulee ns. "oikea", mutta rajapinnat oikeaan distribuutioon puuttuvat. Kuitenkin transaktiot (rahan siirto, signaus jne) ja louhiminen olisi mukava saada mukaan. Ns. "smart contract" konsepti pitäisi myös tutkia koska haluan selvittää senkin mahdollisuuksia. Demo voisi olla esim. joku sopimus. Tavoite on, että valuutta olisi perustoiminnallisuudeltaan oikean kryptovaluutan kaltainen.

Algoritmeista. Tässä tarvitaan joku hash-funktio. Niiden implementointi ei vain
ole kovin mielekästä. Ajattelin, että joku simppeli voisi riittää tässä tapauksessa esim SHA-1. SHA-256 on jo sen verran
sekava, että se olisi vain copy-pastea eikä välttämättä kovin hyödyllinen oppimismielessä. Kieleksi valitsen todennäköisesit Pythonin, täytyy vielä vähän funtsia. Blockchain on vähän kuin linkitetty lista ja oikeastaan todella simppeli. Mietin myös, että onko OK käyttää esim. valmista JSON-parseria jos transaktiot olisivat JSON-dokumentteja vai pitäiskö se kirjotella itse? Base64 tarvitaan, se on aika helppo. Koko signaus prosessi on vielä vähän auki. 

Bitcoin: A Peer-to-Peer Electronic Cash System https://bitcoin.org/bitcoin.pdf
