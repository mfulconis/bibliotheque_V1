import math
import requests
import json
from nltk.tokenize import word_tokenize
from gensim.models import word2vec



def SuprPonctuation(chaine):
    carspe = "${[()]},_;:.?&«»!"
    for c in carspe:
        locals()
        chaine = chaine.replace(c,'')
    return chaine

def SuprPonctuationTag(chaine):
    carspe = "${[()]},_;:.?&«»\'`"
    for c in carspe:
        locals()
        chaine = chaine.replace(c,'')
    return chaine

def creercorpus():
    temp1 = recupererDonnees()
    # définition des stopswords dans un fichier dictionnaire.txt
    stopwords = open('tablodebord/dictionnaire.txt', 'r')
    stopwords_list = []
    for line in stopwords.readlines():
         stopwords_list.append(str(line))
    # liste du corpus à étudier
    corpus = []
    texte = ""
    # construction du corpus à étudier  pour chaque livre : TITRE+TAGS+RESUME
    # et premiers Nettoyages du texte
    for item in temp1:
        dico = item["fields"]
        a = SuprPonctuation(str(dico["Titre"]))
        b = SuprPonctuationTag(str(dico["Tagstxt"]))
        c = SuprPonctuation(str(dico["Resume"]))
        texteAetudier = a + " " + b + " " + c
        dic = {"L\'" : "", "l\'" : "", "d\'" : "", "D\'" : "", "\'à" : "", "n\'" : "", "N\'" : "", "s\'" : "", "c\'" : "", "C\'" : "", "’" : " ", "``" : " ", }
        for i, j in dic.items():
            texteAetudier = texteAetudier.replace(i, j)
        texte = texte + texteAetudier
    tokens = word_tokenize(texte, language='french')
    tokens = [value.lower() for value in tokens]
    tokens = [value for value in tokens if value + "\n" not in stopwords_list]
    corpus.append(tokens)
    # Vectorisation des termes du corpus
    modele = word2vec.Word2Vec(corpus, min_count=4,vector_size=500, window=10)
    words = modele.wv
    return words



def motAChercher(mot):
    listeMotAChercher = [mot]
    grandDico = creercorpus()
    var = grandDico.most_similar(positive=[mot], topn=4)
    for item in var:
        listeMotAChercher = listeMotAChercher + [item[0]]
    return listeMotAChercher



def SearchBook(mot):

        temp1 = recupererDonnees()
        # définition des stopswords dans un fichier dictionnaire.txt
        stopwords = open('tablodebord/dictionnaire.txt', 'r')
        stopwords_list = []
        for line in stopwords.readlines():
            stopwords_list.append(str(line))
        # liste du des mots finaux pour chaque référence de livre
        listeLivre = {}
        # construction du corpus à étudier  pour chaque livre : TITRE+TAGS+RESUME
        # et premiers Nettoyages du texte
        for item in temp1:
            dico = item["fields"]
            a = SuprPonctuation(str(dico["Titre"]))
            b = SuprPonctuationTag(str(dico["Tagstxt"]))
            c = SuprPonctuation(str(dico["Resume"]))
            texteAetudier = a + " " + b + " " + c
            dic = {"L\'": "", "l\'": "", "d\'": "", "D\'": "", "\'à": "", "n\'": "", "N\'": "", "s\'": "", "c\'": "",
                   "C\'": "", "’": " ", "``": " ", }
            for i, j in dic.items():
                texteAetudier = texteAetudier.replace(i, j)
                texteAetudier = texteAetudier.casefold()
                reference = str(dico["reference"])
            livre = {reference : texteAetudier}
            listeLivre.update(livre)
        listeMotAChercher = motAChercher(mot)
        listeref2 = []
        for elmt in listeMotAChercher:
            listeref = []
            i = 0
            for cle, valeur in listeLivre.items():
                if elmt in valeur:
                    i = i + 1
                    if cle not in listeref:
                        w = round(valeur.count(elmt) * math.log(len(temp1) / i), 1)
                        livretrouve = (elmt, cle, w)
                        listeref.append(livretrouve)
                        listeref.sort(key = lambda x: x[2])
                        listeref.reverse()
            listeref2.append(listeref)
        return listeref2


def recupererDonnees():
    params = ()
    airtable_records = []
    run = True
    while run is True:
        r = requests.get('https://api.airtable.com/v0/appBvKk6a0YWsf0ay/'
                         'Biblioth%C3%A8que%20des%20Fulcos?api_key=keyAeXwxVMw0lLYtK&'
                         'fields%5B%5D=Titre&fields%5B%5D=Tagstxt&fields%5B%5D=reference&fields%5B%5D=Resume', params=params)
        airtable_reponse = r.json()
        airtable_records += (airtable_reponse['records'])
        if 'offset' in airtable_reponse:
            run = True
            params = (('offset', airtable_reponse['offset']),)
        else:
            run = False
    temp1 = airtable_records
    return temp1
