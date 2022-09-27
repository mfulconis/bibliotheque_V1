import requests
import json
from tablodebord.FonctionsEtMethodes import SuprCar
from collections import Counter
import os
from django.conf import settings
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import re
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS as stopwords
import pandas as pd

stopwords2 =["L'", "La", "Le", "Une", "Un", "le", "la", "A", "Les", "les", "Des", "des", "Ce", "ce", "Ces", "ces", "Ses", "ses", "si", "Si", " ", "_", "jusqu'"]

# recuoère les données sur  Airtable
def getdata():
    params = ()
    airtable_records = []
    run = True
    while run is True:
        r = requests.get('https://api.airtable.com/v0/appBvKk6a0YWsf0ay/'
                         'Biblioth%C3%A8que%20des%20Fulcos?api_key=keyAeXwxVMw0lLYtK&'
                         'fields%5B%5D=Titre&fields%5B%5D=Nomtxt&fields%5B%5D=Tagstxt&'
                         'fields%5B%5D=Formatcm&fields%5B%5D=Pages&fields%5B%5D=Lutxt&', params=params)
        airtable_reponse = r.json()
        airtable_records += (airtable_reponse['records'])
        if 'offset' in airtable_reponse:
            run = True
            params = (('offset', airtable_reponse['offset']),)
        else:
            run = False
    base = {'records': airtable_records}
    return base

# recuoére les données sur Airtabkle qui vont être analyser sus forme de grille pour une recherche

def creercorpus():
    r = requests.get('https://api.airtable.com/v0/appBvKk6a0YWsf0ay/'
                     'Biblioth%C3%A8que%20des%20Fulcos?api_key=keyAeXwxVMw0lLYtK&'
                     'fields%5B%5D=Titre&fields%5B%5D=Tagstxt&fields%5B%5D=reference&fields%5B%5D=Resume')
    json_base = json.loads(r.text)
    temp1 = json_base["records"]
    dictionnaire = {}
    for item in temp1:
        dico = item["fields"]
        texteAetudier = dico["Titre"], dico["Tagstxt"], dico["Resume"]
        refe = str(dico["reference"])
        refe = refe.replace(" ", '')
        dictionnaire = dictionnaire | {refe : texteAetudier}
        file = open("corpus.json", "w")
        json.dump(dictionnaire, file)
        file.close()


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
    base = getdata()
    nb = nbedelivre()
    listedonnee = []
    i = 0
    while i < nb:
        listedonnee.append(base["records"][i]["fields"]["Lutxt"])
        i= i+1
    data_dict = dict(Counter(listedonnee))
    livreslus = pd.DataFrame(list(data_dict.items()), columns=['Lu', 'Quantité'])
    plt.style.use('ggplot')
    fig = plt.Figure(figsize=(4, 3))
    ax = fig.add_subplot(111)
    ax.set_title("Par qui sont lus les livres ?", color="#555555", fontname="Futura", fontsize="20", fontweight="bold")
    ax.pie(livreslus.Quantité, labels = ['Annie', 'Marc', 'Non lus', ' ', 'Les deux'],
           textprops={'fontsize': 16, 'fontname': 'Times'},
               colors = ['red', 'green', 'yellow', 'grey', 'orange'],
               explode = [0, 0, 0, 0, 0],
               #autopct = lambda x: str(round(x, 2)) + '%',
               pctdistance = 0.7, labeldistance = 1.15,
               shadow = True)
    fig.savefig(os.path.join(settings.BASE_DIR, 'static-res/images/mongraphe2.png'))
    return

###  FIN DE SCRIPT OU JE TESTE DU CODE ##