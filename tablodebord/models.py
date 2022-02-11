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

    def __str__(self):
        return '{} {}'.format(self.titre, self.auteur)