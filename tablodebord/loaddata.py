import requests
import json
from tablodebord.FonctionsEtMethodes import SuprCar
from collections import Counter
import os
from django.conf import settings
from matplotlib.figure import Figure
import re
import spacy
from spacy.lang.fr.stop_words import STOP_WORDS as stopwords

stopwords2 =["L'", "La", "Le", "Une", "Un", "le", "la", "A", "Les", "les", "Des", "des", "Ce", "ce", "Ces", "ces", "Ses", "ses", "si", "Si", " ", "_", "jusqu'"]

# recuoère les données sur  Airtable
def getdata():
    r = requests.get('https://api.airtable.com/v0/appBvKk6a0YWsf0ay/'
                 'Biblioth%C3%A8que%20des%20Fulcos?api_key=keyAeXwxVMw0lLYtK&'
                 'fields%5B%5D=Titre&fields%5B%5D=Nomtxt&fields%5B%5D=Tagstxt&'
                 'fields%5B%5D=Formatcm&fields%5B%5D=Pages&fields%5B%5D=Lutxt&')
    base = json.loads(r.text)
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

def creerthesaurus():
    nlp = spacy.load("fr_core_news_md")
    creercorpus()
    r = open("corpus.json")
    dico = json.load(r)
    motsclefs = {}
    grilledef = {}
    mots = ""

    for element in dico:
        ligne = dico[element]
        tag = " ".join(ligne[1])
        grille = nlp(ligne[0] + " " + tag + " " + ligne[2])
        liste = []
        for item in grille:
            if item.pos_ == "NOUN" or "PROPN":
                if item.text not in stopwords:
                    if item.text not in stopwords2:
                        mots = re.sub(r'[^\w]+', "", item.text)
                        if mots and len(mots)>2:
                            liste.append(mots.lower())
        motsclefs = { str(element) : liste }
        grilledef = grilledef | motsclefs
    dictionnaire1 ={}
    for element in grilledef:
        laliste =  grilledef[element]
        dico1 = {}
        for item in laliste:
            nb = laliste.count(item)
            if nb > 1:
                dico1[item] = nb
        dictionnaire1[element] = dico1
    #for element in dictionnaire1:
       # print(element + " " + str(dictionnaire1[element]))
    file = open("thesaurus.json", "w")
    json.dump(dictionnaire1, file)
    file.close()


#creerthesaurus()

ref = "Cthulhu"
def choixdicoref(ref):
    creerthesaurus()
    with open("thesaurus.json") as json_data:
        dico = json.load(json_data)
        for y in dico.keys():
            w = dico[y]
            if ref.lower() in w:
                print(y + " : " + str(dico[y]))
        #for element in dico:
            #print(element)
    #file.close()
    #if ref in dico.keys:
        #print(dico.keys)

#choixdicoref(ref)

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

