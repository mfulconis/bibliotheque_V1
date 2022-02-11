import math
from operator import itemgetter, attrgetter
import requests
import json

from nltk.corpus.europarl_raw import french

from tablodebord.FonctionsEtMethodes import SuprCar
import nltk

import nltk.data
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import RegexpTokenizer
import string

import gensim
from gensim.models import word2vec
import re


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

    #tokenizer = nltk.data.load('tokenizers/punkt/french.pickle')
    # récupération des données sur Airtable
    r = requests.get('https://api.airtable.com/v0/appBvKk6a0YWsf0ay/'
                     'Biblioth%C3%A8que%20des%20Fulcos?api_key=keyAeXwxVMw0lLYtK&'
                     'fields%5B%5D=Titre&fields%5B%5D=Tagstxt&fields%5B%5D=reference&fields%5B%5D=Resume')
    json_base = json.loads(r.text)
    temp1 = json_base["records"]
    # définition des stopswords dans un fichier dictionnaire.txt
    stopwords = open('tablodebord/dictionnaire.txt', 'r')
    stopwords_list = []
    for line in stopwords.readlines():
         stopwords_list.append(str(line))
    # liste du corpus à étudier
    corpus = []
    texte = ""
    # liste du des mots finaux pour chaque référence de livre
    grandDico = []
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

        #texteAetudier = texteAetudier.replace("l'", '')
        #texteAetudier = texteAetudier.replace("L'", '')
        #SuprPonctuation(texteAetudier)
        #texteAetudier = str(dico["Titre"]) + str(dico["Tagstxt"]) + str(dico["Resume"])
        #tokenizer = RegexpTokenizer(r'''\w'|\w+|[^\w\s]''')
    tokens = word_tokenize(texte, language='french')
    tokens = [value.lower() for value in tokens]
    tokens = [value for value in tokens if value + "\n" not in stopwords_list]
    corpus.append(tokens)
        #print(type(tokens))
        #print(type(corpus))
    modele = word2vec.Word2Vec(corpus, min_count=4,vector_size=500, window=10)
    words = modele.wv
        #print(words.most_similar(positive=['société'], topn=5))
        #grandDico.append([dico['reference'], words])
        #grandDico.append([words])
        #vec1 = words.most_similar('société')
        #corpus = []
    return words

    #vec1 = words.most_similar('société')
    #print(vec1)
    #print(str(grandDico[0]) + "\n" + str(grandDico[3]))
        #print(type(corpus))
        #print(corpus[0])
        #texteAetudier = dico["Titre"], dico["Tagstxt"], dico["Resume"]
       #corpus =

#grandDico = creercorpus()

#print(grandDico)

def motAChercher(mot):
    listeMotAChercher = [mot]
    grandDico = creercorpus()
    #print(grandDico.key_to_index)
    var = grandDico.most_similar(positive=[mot], topn=4)
    #print(var)
    for item in var:
        #print(item[0])
        listeMotAChercher = listeMotAChercher + [item[0]]
    return listeMotAChercher


    #print(var)


    #try:
       # print(grandDico.most_similar(positive=[mot], topn=5))
    #except:
        #print("pas de mots similaire")#print(item[1].key_to_index)

#mot = "policier"
#var = recherche(mot)
#print(var)

#var = creercorpus()
#print(var)

def SearchBook(mot):

        temp1 = recupererDonnees()
        # définition des stopswords dans un fichier dictionnaire.txt
        stopwords = open('tablodebord/dictionnaire.txt', 'r')
        stopwords_list = []
        for line in stopwords.readlines():
            stopwords_list.append(str(line))
        # liste du corpus à étudier
        corpus = []
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
        #print(listeMotAChercher)

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
                        #print(listeref)
                        #listeref = sorted(listeref, key=attrgetter(w))
                        #listeref = sorted(listeref, key=lambda student: student[2])
                        listeref.reverse()
            listeref2.append(listeref)
        return listeref2


def recupererDonnees():
    r = requests.get('https://api.airtable.com/v0/appBvKk6a0YWsf0ay/'
                     'Biblioth%C3%A8que%20des%20Fulcos?api_key=keyAeXwxVMw0lLYtK&'
                     'fields%5B%5D=Titre&fields%5B%5D=Tagstxt&fields%5B%5D=reference&fields%5B%5D=Resume')
    json_base = json.loads(r.text)
    temp1 = json_base["records"]
    return temp1

#mot = "policier"
#SearchBook(mot)

#creercorpus()

#temp1 = recupererDonnees()
#print(len(temp1))