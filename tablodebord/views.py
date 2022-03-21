from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from tablodebord import loaddata
from tablodebord.models import Auteur
from tablodebord.models import Livre
import requests
import json
from tablodebord.FonctionsEtMethodes import SuprCar
from tablodebord.FonctionsEtMethodes import verifier
from tablodebord.FonctionsEtMethodes import SupprimerEnregistrement
from tablodebord.forms import RechercheMot, RechercheAuteur
from tablodebord.Testbis_word2vec import SearchBook
from django.views import generic
from django.db import models



# La page principale
def index(request):
    nb = loaddata.nbedelivre()
    format = loaddata.livreparformat()
    auteur = loaddata.nblivreauteur()
    tag = loaddata.tagcites()
    loaddata.LivresLus()
    template = loader.get_template('tablodebord/index.html')
    legende = "La bibliothèque compte " + str(nb) + " livres dont " + str(format[0]) + " livres de poche, " + str(format[1]) + " livres moyen format et " + str(format[2]) + " livres grand format."
    context = {'legende' : legende, 'auteur' : auteur, 'tagcite' : tag}
    return HttpResponse(template.render(context, request))

def Save_base_Livre(request):
    params = ()
    airtable_records = []
    run = True
    while run is True:
        r = requests.get('https://api.airtable.com/v0/appBvKk6a0YWsf0ay/'
                         'Biblioth%C3%A8que%20des%20Fulcos?api_key=keyAeXwxVMw0lLYtK&'
                         'fields%5B%5D=Titre&fields%5B%5D=Nomtxt&fields%5B%5D=Tagstxt&'
                         'fields%5B%5D=Formatcm&fields%5B%5D=Pages&fields%5B%5D=Lutxt&'
                         '&fields%5B%5D=reference&fields%5B%5D=Resume', params=params)
        airtable_reponse = r.json()
        airtable_records += (airtable_reponse['records'])
        if 'offset' in airtable_reponse:
            run = True
            params = (('offset', airtable_reponse['offset']),)
        else:
            run = False
    base = {'records': airtable_records}
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
        element_reference = str(champb["reference"])
        element_resume = str(champb["Resume"])
        cur1 = verifier(element_auteur)
        if cur1 is None:
            nom_auteur = Auteur(nom=element_auteur)
            nom_auteur.save()
            cur2 = verifier(element_auteur)
            livre = Livre(titre=element_titre, auteur_id=cur2[0],
                          format=element_format, pages=element_pages,
                          tags=element_tags, livrelu=element_livrelu,
                          reference=element_reference, resume=element_resume)
            livre.save()
        else:
            cur3 = verifier(element_auteur)
            livre = Livre(titre = element_titre, auteur_id = cur3[0],
                      format = element_format, pages = element_pages,
                      tags = element_tags, livrelu = element_livrelu,
                      reference=element_reference, resume=element_resume)
            livre.save()
    auteur = loaddata.nblivreauteur()
    tag = loaddata.tagcites()
    loaddata.LivresLus()
    template = loader.get_template('tablodebord/index.html')
    legende = "Votre base de données a bien été sauvegardée !"
    context = {'legende' : legende, 'auteur' : auteur, 'tagcite' : tag}
    return HttpResponse(template.render(context, request))


def resultats(request):
    return HttpResponse('le mot chrecherché est ')

def recherche(request):
    form = RechercheMot()
    form2 = RechercheAuteur()
    if request.method == 'POST':
        # TRAITEMENT DU FORMULAIRE PAR AUTEUR
        form2 = RechercheAuteur(request.POST)
        if form2.is_valid():
            id = form2.cleaned_data['terme2']
            r2 = []
            try:
                for liv2 in Livre.objects.filter(auteur_id=id):
                    r2 = r2 + [liv2]
                template = loader.get_template('tablodebord/forms.html')
                context = {'Resultats2': r2, 'form': form, 'form2': form2}
                return HttpResponse(template.render(context, request))
            except:

                #TRAITEMENT DU FORMULAIRE PAR MOT CLEF
                form = RechercheMot(request.POST)
                if form.is_valid():
                    mot = form.cleaned_data['terme1']
                    mot = mot.lower()
                    try:
                        resultats = SearchBook(mot)
                        re_list = []
                        for item in resultats:
                            for it in item:
                                _, var, _ = it
                                r = Livre.objects.get(reference=var)
                                re_list = re_list + [r]
                        template = loader.get_template('tablodebord/forms.html')
                        context = {'Resultats' : re_list, 'form' : form, 'form2' : form2 }
                        return HttpResponse(template.render(context, request))
                    except Exception as err:
                        Resultat = err
                        template = loader.get_template('tablodebord/forms.html')
                        context = {'Resultat': Resultat, 'form': form, 'form2': form2}
                        return HttpResponse(template.render(context, request))

    else:
        form = RechercheMot()
        form2 = RechercheAuteur()
    return render(request, 'tablodebord/forms.html' , {'form' : form, 'form2' : form2})

