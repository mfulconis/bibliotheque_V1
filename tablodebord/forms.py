from django import forms
from tablodebord.models import Livre, Auteur


class RechercheMot(forms.Form):
    terme1 = forms.CharField(label="", max_length=50, required=True)


class RechercheAuteur(forms.Form):
    variable = [(0, 'Sélectionner un auteur')]
    for liv in Auteur.objects.order_by('nom'):
        auteur = liv.nom
        id = liv.id
        variable.append((id, auteur))
    LISTE_AUTEURS = variable
    terme2 = forms.ChoiceField(label='', choices=LISTE_AUTEURS, required=False)
