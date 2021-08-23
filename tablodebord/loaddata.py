import requests
import json
from tablodebord.FonctionsEtMethodes import SuprCar
from collections import Counter
import os
from django.conf import settings
from matplotlib.figure import Figure

# Requête sur Airtable
def getdata():
    r = requests.get('https://api.airtable.com/v0/appBvKk6a0YWsf0ay/'
                 'Biblioth%C3%A8que%20des%20Fulcos?api_key=keyAeXwxVMw0lLYtK&'
                 'fields%5B%5D=Titre&fields%5B%5D=Nomtxt&fields%5B%5D=Tagstxt&'
                 'fields%5B%5D=Formatcm&fields%5B%5D=Pages&fields%5B%5D=Lutxt')
    base = json.loads(r.text)
    return base


# calcul du nombre de livres #
def nbedelivre():
    base = getdata()
    temp = base["records"]
    nb = 0
    for element in temp:
        nb = nb + 1
    return nb

# calcul du nombre de livre par format #
def livreparformat():
    base = getdata()
    temp = base["records"]
    j = 0
    k = 0
    l = 0
    m = 0
    for element in temp:
        champa = temp[m]
        champb = champa["fields"]
        element_format = str(champb["Formatcm"])
        m = m + 1
        a = element_format.find('x') + 1
        element = float(element_format[a:])
        if element < 19:
            j = j + 1
        elif element >= 19 and element < 25:
            k = k +1
        else:
            l = l +1
    format = [str(j), str(k), str(l)]
    return format

### Calcule le nombre de livres par auteurs. ###
def nblivreauteur():
    base = getdata()
    temp = base["records"]
    tablo1 = []
    n = 0
    for element in temp:
        champa = temp[n]
        champb = champa["fields"]
        champc = str(champb["Nomtxt"])
        champc = champc[2:-2]
        tablo1.append(champc)
        n = n + 1
    tablo2 = {}
    for auteur in tablo1:
        tablo2.update({ auteur : tablo1.count(auteur) })
    tablo2 = sorted(tablo2.items(), key=lambda t: t[1])
    tablo2.reverse()
    return tablo2



### Calcule le nombre de fois
# que les tags sont cités. ###
def tagcites():
    base = getdata()
    temp = base["records"]
    tablo3 = []
    m = 0
    for element in temp:
        champa = temp[m]
        champb = champa["fields"]
        champc = str(champb["Tagstxt"])
        champc = SuprCar(champc)
        champc = champc.split(', ')
        tablo3.extend(champc)
        m = m + 1
    comptetags = Counter(tablo3)
    tablo4 = {}
    for item in comptetags:
        tablo4.update({item: comptetags[item]})
    tablo4 = sorted(tablo4.items(), key=lambda t: t[1])
    tablo4.reverse()
    return tablo4




### Creation du graphique des livres lu par qui
# livres lu et par qui ###

def LivresLus():
    nb = nbedelivre()
    base = getdata()
    temp = base["records"]
    tablo5 = []
    p = 0
    for element in temp:
        champa = temp[p]
        champb = champa["fields"]
        champc = champb["Lutxt"]
        tablo5.append(champc)
        p= p + 1
    comptelu = Counter(tablo5)
    tablo6 = {}
    camlist = []
    for lu in comptelu:
        tablo6.update({lu: comptelu[lu]})
        pourcentage = (100*comptelu[lu]/nb)
        pourcentage = round(pourcentage, 2)
        camlist.append(pourcentage)
    fig2 = Figure(figsize=(3, 2.3), dpi=100, facecolor='#ffffff')
    fig2.suptitle("Les livres lus par...")
    x = [tablo6['Lu par Marc'], tablo6['Lu par Annie'], tablo6['Utilise'], tablo6['Non lu']]
    plot1 = fig2.add_subplot(111)
    plot1.pie(x, labels=['Marc', 'Annie', 'Non lus', 'Feuilletés'], normalize=True)
    fig2.savefig(os.path.join(settings.BASE_DIR, 'static-res/images/mongraphe2.png'))
    return

