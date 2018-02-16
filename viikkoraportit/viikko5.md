# Viikko 5

Taas on projekti edennyt. Nyt ollaan sellaisessa tilanteessa, että ns. "bisnes logiikka" alkaa olla
kasassa. Pitäisi vielä tehdä ainakin demo UI. Ajattelin, että teen sen Reactilla selaimeen. Node tarjoaa
nyt "näppärän" HTTP API:n millä voi luoda lompakon ja siirrellä rahaa. Piti aloitella dokkaria tällä viikolla
mutta vähän hiljaiseksi jäi kun tässä oli vielä sen verran tekemistä. Teen nyt seuraavaksi sen simppelin
UI:n ja sitten voin tehdä nuo muut jutut pois. Testien kattavuus on nyt ihan hyvä perustoiminnallisuuden
kannalta. 

Dokumentoin tähän nyt hieman miten tuota käytetään toistaiseksi.

Node käyntiin
    python -m node.server

HTTP API

    POST /wallet/create
    
    Response:

    {
        "public_key": "MTc6MTc5MjkzNDk3MTczNzg1MDUyM....xOTA1MzA5NDE2NDg2MzI1ODk=",
        "private_key": "ODQzNzM0MTA0MzQ3MjIzNzc1MTcwMjM5NTE...TY0ODYzMjU4OQ=="
    }

    POST /wallet/info

    {
        "public_key":"MTc6MTQxNjM...DIyNjk="
    }

    RESPONSE:

    {
        "balance": 0
    }

    POST /wallet/send

    {
        "public_key": "MTc6MTc5MjkzNDk3MTczNzg1MDUyM....xOTA1MzA5NDE2NDg2MzI1ODk=",
        "private_key": "ODQzNzM0MTA0MzQ3MjIzNzc1MTcwMjM5NTE...TY0ODYzMjU4OQ=="
        "amount": 10,
        "recipient": "MTc6MTQxNjM...DIyNjk="
    }

    RESPONSE:

    {
        "successful": true
    }

    POST /mine

    {
        "reward_address":"MTc6MTQxNjM...DIyNjk="
    }

    RESPONSE:

    {
    }