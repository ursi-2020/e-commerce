[Sommaire](https://ursi-2020.github.io/e-commerce/)

# Use case E-commerce

## E-commerce -> Catalogue produits

Ce diagramme de séquence montre comment l'application E-commerce récupère l'ensemble des produits disponibles dans le Catalogue Produits.

![Diagramme de séquence](./sequence_prduits.svg)

L'application E-commerce commence par demander la liste des produits disponibles auprès du Catalogue Produits.
Ce dernier nous renvoie un objet JSON contenant un tableau des produits disponibles.

Appel vers le catalogue:

```python
    products = api.send_request("catalogue-produit", "catalogueproduit/api/data")
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

Nous enregistrons ensuite dans notre BDD l'ensemble des produits reçus, à l'aide de ce code:

```python
    for produit in data['produits']:
        p = Produit(codeProduit=produit['codeProduit'], familleProduit=produit['familleProduit'],
                        descriptionProduit=produit['descriptionProduit'], prix=produit['prix'], quantiteMin=1, packaging=0)
        p.save()
```

Nous affichons ensuite le contenu de notre base de données à l'utilisateur via la route:
```
    /ecommerce/products
```

![Diagramme de cas d'utilisation](./usecase_prduits.svg)

## E-commerce -> CRM

Ce diagramme de séquence montre comment l'application E-commerce récupère l'ensemble les informations des clients à l'aide de l'application CRM.