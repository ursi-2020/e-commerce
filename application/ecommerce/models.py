from django.db import models
from django.contrib.postgres.fields import ArrayField



class Produit(models.Model):
    id_catalogue = models.PositiveIntegerField()
    codeProduit = models.CharField(max_length=200)
    familleProduit = models.CharField(max_length=200)
    descriptionProduit = models.CharField(max_length=200)
    quantiteMin = models.PositiveIntegerField()
    packaging = models.PositiveIntegerField()
    prix = models.PositiveIntegerField()
    exclusivite = models.CharField(max_length=200)

    # def __str__(self):
    #     return "{\"codeProduit\":{}, \"familleProduit\":{}, \"descriptionProduit\":{},\"quantiteMin\":{}, \"packaging\":{}, \"prix\":{}}".format(self.codeProduit, self.familleProduit, self.descriptionProduit, self.quantiteMin, self.packaging, self.prix)

class Article(models.Model):
    nom = models.CharField(max_length=200)
    stock = models.PositiveIntegerField()

    def __str__(self):
        return 'Article: {}'.format(self.nom)


class Vente(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return 'Vente: {} - {}'.format(self.article.nom, self.date)

class Customer(models.Model):
    IdClient = models.CharField(max_length=200, default="")
    Prenom = models.CharField(max_length=200, default="")
    Nom = models.CharField(max_length=200, default="")
    Credit = models.CharField(max_length=200, default="")
    Paiement = models.IntegerField(default=0)
    Compte = models.CharField(max_length=200, default="")
    carteFid = models.IntegerField(default=0)

class Promotion(models.Model):
    codeProduit = models.CharField(max_length=200)
    familleProduit = models.CharField(max_length=200)
    descriptionProduit = models.CharField(max_length=200)
    quantiteMin = models.PositiveIntegerField()
    packaging = models.PositiveIntegerField()
    prix = models.PositiveIntegerField()
    prixOriginel = models.PositiveIntegerField()
    reduction = models.PositiveIntegerField()


class ClientPromotion(models.Model):
    IdClient = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    reduction = models.PositiveIntegerField()

class PromotionsCustomersProducts(models.Model):
    date = models.DateField()
    IdClient = models.TextField(blank=False)
    codeProduit = models.CharField(max_length=20)
    quantity = models.IntegerField(default = 0)
    reduction = models.IntegerField(default = 0)

class VenteTicket(models.Model):
    codeProduit = models.TextField(blank=False)
    prix = models.PositiveIntegerField()
    prixApres = models.PositiveIntegerField()
    promo = models.IntegerField()
    promo_client = models.IntegerField()
    promo_client_produit = models.IntegerField()
    quantity = models.PositiveIntegerField()

class Tickets(models.Model):
    date = models.DateField()
    prix = models.PositiveIntegerField()
    client = models.TextField(blank=False)
    pointsFidelite = models.PositiveIntegerField()
    modePaiement = models.TextField()
    articles = models.ManyToManyField(VenteTicket,
                                     related_name='articles')


