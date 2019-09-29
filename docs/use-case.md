[Sommaire](https://ursi-2020.github.io/e-commerce/)

# Use case E-commerce

## E-commerce -> Catalogue produits

### Récupérer l'ensemble des produits du Catalogue

![Diagramme de séquence](./usecase_produits.svg)

L'application E-commerce est en charge d'afficher les différents produits à l'utilisateur.
Pour cela, E-commerce récupère les informations auprès du Catalogue Produits.

Ce diagramme de séquence montre comment l'application E-commerce récupère l'ensemble des produits disponibles dans le Catalogue Produits.

![Diagramme de séquence](./sequence_prduits.svg)

L'application E-commerce commence par demander la liste des produits disponibles auprès du Catalogue Produits.
Ce dernier nous renvoie un objet JSON contenant un tableau des produits disponibles.

Appel vers le catalogue:

```python
products = api.send_request("catalogue-produit", "api/data")
data = json.loads(products)
```

Ex de JSON reçu:

```json
{
    produits: [
        {
            id : 1,
            codeProduit: "X1-0",
            descriptionProduit: "Frigos:P1-0",
            familleProduit : "Frigos",
            packaging : 2,
            prix : 424,
            quantiteMin : 15
        }
    ]
}
```

### Enregistrement des données

Une fois le JSON reçu, nous enregistrons dans notre BDD l'ensemble des produits, à l'aide de ce code:

```python
for produit in data['produits']:
    p = Produit(codeProduit=produit['codeProduit'], familleProduit=produit['familleProduit'],
                descriptionProduit=produit['descriptionProduit'], prix=produit['prix'],
                quantiteMin=1, packaging=0)
    p.save()
```

Nous affichons ensuite le contenu de notre base de données à l'utilisateur via la route:
```
/ecommerce/products
```

### Vider la BDD Produits

Il est possible de vider le contenu de la base de données Produits de l'application, via le bouton dédié. Nous affichons ensuite la page Produits, qui est alors vide.
Pour cela, au clic sur le bouton, nous déclenchons le code suivant:

```python
models.Produit.objects.all().delete()
product_list = {
    "data" : Produit.objects.all()
}
return render(request, "products.html", product_list)
```

La base de données Produits est alors réinitialisée.

## E-commerce -> CRM

### Récupérer les clients du CRM

L'application E-commerce doit pouvoir avoir l'ensemble des informations clients.
Pour cela, il se connecte alors à l'application CRM pour récupérer toutes les informations clientes.

Ce diagramme de séquence montre comment l'application E-commerce récupère l'ensemble les informations des clients à l'aide de l'application CRM.

![Diagramme de séquence](./sequence_crm.svg)

E-commerce demande les informations des clients auprès du CRM, à l'aide de la route que l'application met à disposition.

### Enregistrer les clients dans la BDD E-commerce

Une fois les clients récupérés, nous les enregistrons dans notre base de données en tant que Customer.

### Effacer la base de données clients

Il est possible de vider la base de données clients à l'aide d'un bouton.