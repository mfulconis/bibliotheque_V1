from django.db import models

# CREATION DE LA TABLE AUTEUR #
class Auteur(models.Model):
    nom = models.CharField(max_length=255)
    naissance = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.nom)

# CREATION DE LA TABLE LIVRE #
class Livre(models.Model):
    titre = models.CharField(max_length=255)
    auteur = models.ForeignKey('Auteur', on_delete=models.DO_NOTHING)
    format = models.CharField(max_length=5)
    pages = models.IntegerField()
    tags = models.TextField(blank=True)
    livrelu = models.CharField(max_length=255, blank=True)
    resume = models.TextField(blank=True)
    reference = models.CharField(max_length=20, default='REFERENCE')
    prix = models.IntegerField(default=0)
    ISBN = models.CharField(max_length=20, default='ISBN')
    date_edition = models.IntegerField(default=0)
    secteur_biblio = models.CharField(max_length=2, blank=False, default='NC')
    editeur = models.CharField(max_length=255, blank=True)
    collection = models.CharField(max_length=255, blank=True)
    fichier_couv = models.URLField(blank=True)

    def __str__(self):
        return '{} {}'.format(self.titre, self.auteur)