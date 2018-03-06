
# Käyttöohje

Ohjeet testattu: Python 2.7.11 ja Node v8.9.4

1. Käynnistä node seuraavasti dummycoin juurihakemistosta

        $ python -m node.server
        serving at port 3001

2. Käynnistä demoui seuraavasti

        $ cd demoui
        $ npm install
        $ npm start

    UI käynnistyy nyt Chromeen. Jos ei, navigoi http://localhost:3000/

3. Kirjaudu sisään jollain tunnuksella. Demo luo tunnuksen jos sellaista ei ole. 

4. Käynnistä toinen tabi ja kirjaudu sisään toisella tunnuksella

5. Klikkaa 'Mine' ensimmäisessä tabissa niin saat sille tunnukselle rewardin

6. Voit nyt siirtää toiseen tabiin rahaa kopioimalla toisen tabin public keyn ja pasteamalla sen "To address" kenttään ensimmäisessä tabissä. Voilà, olet siirtänyt ensimmäisen DummyCoinin.



