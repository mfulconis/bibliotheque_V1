import re
import json
import spacy
import pandas as pd
import numpy as np
from spacy.lang.fr.stop_words import STOP_WORDS as stopwords
from collections import ChainMap
texte = "451degrés Fahrenheit représentent la température à laquelle une société s'enflamme et se consume. La température dans cette société future où la lecture est considérée comme une lecture antisocial, un corps spécial de pompiers est chargé de brûler tous les livres, dont la détention est interdite pour le bien collectif. Le pompier Montag se met pourtant à rêver d'un monde différent, qui ne bannirait pas la littérature et l'imaginaire au profit d'un bonheur immédiatement consommable. Il devient dès lors un dangereux criminel, impitoyablement poursuivi par une société qui désavoue son passé."

#print(' '.join([t for t in texte.split() if t not in stopwords]))

dico_livre = {}
dictionnaire = {}
objet = []
ref = "RESFT1"
nlp=spacy.load("fr_core_news_md")
#texte = re.sub(r'[^\w ]+', "", texte)
docs = nlp.tokenizer(texte)
for item in docs:
    if item.text not in stopwords:
        item2 = re.sub(r'[^\w ]+', "", item.text)
        if item2 != '':
            objet.append(item2)
            if objet.count(item2) > 1:
                dico_livre = dico_livre | { item2:objet.count(item2)}
                #dictionnaire = dictionnaire | dico_livre
                #print(dico_livre)
dictionnaire = {ref : dico_livre }
print(type(dictionnaire))
print(dictionnaire)
            #print(objet)


#'"' + item2 + '"' + ":" + '"' + str(objet.count(item2)) + '"'

#fichier = open('dictionnaire.json', "w")
#jsonString = '{ {"REF1": "{ "société": "2", "essai": "1", "Histoire": "1", "guerre": "3", "France": "2"}"} }'
#json.dump(jsonString, fichier)
#fichier.close()


#for key, value in data():
   # print(key, value)

#with open('dictionnaire.json', 'r') as openfile:
    # Reading from json file
   # json_object = json.load(openfile)
#for element in json_object:
  #  print(element)


#print(json_object)
#print(type(json_object))
 #   for j in i:
  #      if j.value() > 1:
   #         print(type(i))
    #        print(type(j))
#f.close()


#print(objet



#objet1 = []
#objet2 = {}
#for doc in docs:
 #   print(doc)

#print(stopwords)
    #mot = str(token)
   # if len(mot) >= 4:
        #objet1.append(mot)
#print(objet1)
# for item in objet1:
 #   if objet1.count(item) > 1:
  #      objet2[item] = objet1.count(item)
#print(objet2)

# variable de test

data1 = "science, policier, essai, l'horreur, la police, à même, science, policier, essai, policier, essai, théâtre"
data2 = "science, humour, essai, l'horreur, la police, à même, théâtre, policier, essai, théâtre, essai"
data3 = "politique, humour, essai, histoire, santé, hôpital, Toulouse, médicament, politique, santé"
data4 = "histoire, Toulouse, sport, santé, histoire, université, sport, étudiant, sport"
data = [data1, data2, data3, data4]
item = "essai"


def comptocc(data):
    totalObjet = len(data)
    total = 0
    nbeObjet = 0
    for element in data:
        if item in element:
            occurence = element.count(item)
            total = total + occurence
            nbeObjet = nbeObjet +1
    for element in data:
        if item in element:
            occurence = element.count(item)

            print("Le score de l'objet est : " + str(w))
    print("Le mot " + item + " a été trouvé " + str(total) + " fois dans le corpus")
    print("Le mot " + item + " a été trouvé dans " + str(nbeObjet) + " objets.")
    return w

comptocc(data)





