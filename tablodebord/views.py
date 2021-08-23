from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from tablodebord import loaddata
from tablodebord.models import Auteur
from tablodebord.models import Livre
import requests
import json
from tablodebord.FonctionsEtMethodes import SuprCar
from tablodebord.FonctionsEtMethodes import verifier
from tablodebord.FonctionsEtMethodes import SupprimerEnregistrement


# La page principale
def index(request):
    nb = loaddata.nbedelivre()
    format = loaddata.livreparformat()
    auteur = loaddata.nblivreauteur()
    tag = loaddata.tagcites()
    loaddata.LivresLus()
    template = loader.get_template('tablodebord/index.html')
    context = {'nbedelivre' : nb, 'poche' : format[0], 'moyen' : format[1], 'grand' : format[2], 'auteur' : auteur, 'tagcite' : tag}
    return HttpResponse(template.render(context, request))

def Save_base_Livre(request):
    # recupération des données airtable #
    r = requests.get('https://api.airtable.com/v0/appBvKk6a0YWsf0ay/'
                     'Biblioth%C3%A8que%20des%20Fulcos?api_key=keyAeXwxVMw0lLYtK&'
                     'fields%5B%5D=Titre&fields%5B%5D=Nomtxt&fields%5B%5D=Tagstxt&'
                     'fields%5B%5D=Formatcm&fields%5B%5D=Pages&fields%5B%5D=Lutxt')
    base = json.loads(r.text)
    # Suppression des données existantes
    SupprimerEnregistrement()
    # Traitement des données et enregistrement des données#
    temp = base["records"]
    i = 0
    for element in temp:
        champa = temp[i]
        champb = champa["fields"]
        i = i + 1
        element_titre = str(champb['Titre'])
        element_auteur = str(champb["Nomtxt"])
        element_auteur = element_auteur[2:-2]
        element_format = str(champb["Formatcm"])
        element_tags = str(champb["Tagstxt"])
        element_tags = SuprCar(element_tags)
        element_pages = int(champb["Pages"])
        element_livrelu = str(champb["Lutxt"])
        cur1 = verifier(element_auteur)
        if cur1 is None:
            nom_auteur = Auteur(nom=element_auteur)
            nom_auteur.save()
            cur2 = verifier(element_auteur)
            livre = Livre(titre=element_titre, auteur_id=cur2[0],
                          format=element_format, pages=element_pages,
                          tags=element_tags, livrelu=element_livrelu)
            livre.save()
        else:
            cur3 = verifier(element_auteur)
            livre = Livre(titre = element_titre, auteur_id = cur3[0],
                      format = element_format, pages = element_pages,
                      tags = element_tags, livrelu = element_livrelu)
            livre.save()
    return HttpResponse("La base de données a été sauvegardée !")
