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
    carspe = "${[()]},_;:.?&«»"
    for c in carspe:
        locals()
        chaine = chaine.replace(c,'')
    return chaine

def SuprPonctuationTag(chaine):
    carspe = "${[()]},_;:.?&«»\'"
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
    stopwords = open('dictionnaire.txt', 'r')
    stopwords_list = []
    for line in stopwords.readlines():
         stopwords_list.append(str(line))
    # liste du corpus à étudier
    corpus = []
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
        dic = {"L\'" : "", "l\'" : "", "d\'" : "", "D\'" : "", "\'à" : "", "n\'" : "", "N\'" : "", "s\'" : "", "c\'" : "", "C\'" : ""}
        for i, j in dic.items():
            texteAetudier = texteAetudier.replace(i, j)

        #texteAetudier = texteAetudier.replace("l'", '')
        #texteAetudier = texteAetudier.replace("L'", '')
        #SuprPonctuation(texteAetudier)
        #texteAetudier = str(dico["Titre"]) + str(dico["Tagstxt"]) + str(dico["Resume"])
        #tokenizer = RegexpTokenizer(r'''\w'|\w+|[^\w\s]''')
        tokens = word_tokenize(texteAetudier, language='french')
        tokens = [value.lower() for value in tokens]
        tokens = [value for value in tokens if value + "\n" not in stopwords_list]
        corpus.append(tokens)
        #print(type(tokens))
        #print(type(corpus))
        modele = word2vec.Word2Vec(corpus, min_count=1,vector_size=2, window=3)
        words = modele.wv
        #print(words.most_similar(positive=['société'], topn=5))
        #grandDico.append([dico['reference'], words])
        grandDico.append([words])
        #vec1 = words.most_similar('société')
        corpus = []
    return grandDico

    #vec1 = words.most_similar('société')
    #print(vec1)
    #print(str(grandDico[0]) + "\n" + str(grandDico[3]))
        #print(type(corpus))
        #print(corpus[0])
        #texteAetudier = dico["Titre"], dico["Tagstxt"], dico["Resume"]
       #corpus =

#grandDico = creercorpus()

#print(grandDico)

def recherche(mot):
    grandDico = creercorpus()
    print(grandDico)
    for item in grandDico:
        try:
            #print(item[1].most_similar(positive=[mot], topn=5))
            print(item.most_similar(positive=[mot], topn=5))
        except:
            print("pas de mots similaire")#print(item[1].key_to_index)

mot = "société"
recherche(mot)

#var = creercorpus()
#print(var)