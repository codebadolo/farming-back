from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Categorie, Produit, AttributProduit
from django.contrib.auth import get_user_model
import random

User = get_user_model()

# Définition des catégories et sous-catégories
CATEGORIES = {
    "Élevage Poulet": [
        "Poulet de chair",
        "Poulet pondeur",
        "Poulet double usage",
        "Couveuse et incubateurs",
        "Aliments pour poulet",
        "Équipements d’élevage poulet"
    ],
    "Élevage Oeufs": [
        "Œufs frais",
        "Œufs incubables",
        "Accessoires œufs"
    ],
    "Élevage Viande": [
        "Viande de poulet",
        "Viande de poisson",
        "Viande autres volailles"
    ],
    "Élevage Poisson": [
        "Poissons d’élevage",
        "Aliments pour poissons",
        "Matériels pisciculture"
    ],
    "Matériel d’élevage général": [
        "Outils et équipements",
        "Produits vétérinaires",
        "Systèmes de ventilation",
        "Equipement nettoyage"
    ]
}

# Exemple d'attributs types qu'on associera aux produits par catégorie
ATTRIBUTS_TEMPLATES = {
    "Poulet de chair": {
        "Race": ["Cobb 500", "Ross 308", "Hubbard"],
        "Usage": ["Chair"],
        "Poids à l’abattage (kg)": ["2.5", "3.0", "3.5"],
        "Age de maturité (semaines)": ["6", "7", "8"],
        "Mode d’élevage": ["Intensif", "Extensif"],
        "Statut sanitaire": ["Vacciné", "Non vacciné"],
    },
    "Poulet pondeur": {
        "Race": ["Lohmann Brown", "ISA Brown"],
        "Usage": ["Pondeuse"],
        "Production d’oeufs (nombre/semaine)": ["4", "5"],
        "Age de maturité (semaines)": ["18", "20"],
        "Mode d’élevage": ["Extensif", "Bio"],
        "Statut sanitaire": ["Vacciné"],
    },
    "Couveuse et incubateurs": {
        "Capacité (nombre d’oeufs)": ["48", "96", "192"],
        "Type d’alimentation": ["Électrique", "Solaire"],
        "Portabilité": ["Fixe", "Mobile"],
        "Dimensions (cm)": ["60x40x40", "80x60x60"],
        "Poids (kg)": ["5", "10", "15"],
    },
    "Aliments pour poulet": {
        "Composition nutritionnelle": ["18% protéines", "16% protéines"],
        "Type": ["Granulé", "Farine"],
        "Usage recommandé": ["Poussins", "Adultes"],
        "Conditionnement": ["25 kg sac", "50 kg sac"],
    },
    "Poissons d’élevage": {
        "Espèce": ["Tilapia", "Carpe", "Poisson-chat"],
        "Taille adulte (cm)": ["30", "40", "50"],
        "Température d’élevage (°C)": ["25", "28"],
        "Type d’eau": ["Douce", "Saumâtre"],
    },
    "Matériels pisciculture": {
        "Type": ["Réservoir", "Pompe", "Aération"],
        "Capacité (litres)": ["500", "1000", "2000"],
        "Dimensions (cm)": ["100x100x50", "150x150x60"],
    },
    # Ajoute autres catégories et attributs si besoin
}

class Command(BaseCommand):
    help = 'Génère des produits exemples pour un vendeur donné avec catégories et attributs d’élevage'

    def add_arguments(self, parser):
        parser.add_argument('vendeur_id', type=int, help='ID du vendeur')
        parser.add_argument('--nombre', type=int, default=40, help='Nombre total de produits à créer')

    def handle(self, *args, **options):
        vendeur_id = options['vendeur_id']
        nombre = options['nombre']

        try:
            vendeur = User.objects.get(id=vendeur_id)
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Vendeur avec ID {vendeur_id} introuvable."))
            return

        # Création des catégories et sous-catégories
        categorie_objets = {}
        for parent_name, children_names in CATEGORIES.items():
            parent_cat, created = Categorie.objects.get_or_create(
                nom=parent_name,
                defaults={'active': True}
            )
            categorie_objets[parent_name] = parent_cat
            for child_name in children_names:
                child_cat, created = Categorie.objects.get_or_create(
                    nom=child_name,
                    parent=parent_cat,
                    defaults={'active': True}
                )
                categorie_objets[child_name] = child_cat

        produits_crees = 0

        noms_de_produits = [
            "Poulet bouché", "Poulet blanc", "Incubateur Solar 200",
            "Aliment Granulé Premium", "Tilapia Jumbo", "Pompe à eau haute pression",
            "Œufs frais calibre XL", "Produits vétérinaires Basique",
            "Viande poulet fermier", "Couveuse Pro 100", "Nid poulet pondeur",
        ]

        while produits_crees < nombre:
            # Choisissez aléatoirement une catégorie fille parmi celles que tu as créées
            cat_name = random.choice(list(categorie_objets.keys()))
            cat_obj = categorie_objets[cat_name]

            nom_produit = random.choice(noms_de_produits) + f" #{produits_crees + 1}"
            slug = slugify(f"{nom_produit}-{vendeur_id}-{random.randint(1000,9999)}")
            prix = round(random.uniform(1000, 50000), 2)

            produit = Produit.objects.create(
                nom=nom_produit,
                description=f"Produit {nom_produit} catégorie {cat_name}",
                slug=slug,
                categorie=cat_obj,
                vendeur=vendeur,
                prix=prix,
                status=Produit.Status.PUBLIE,
                featured=(produits_crees % 10 == 0)
            )

            # Ajouter attributs pertinents si disponibles
            attribs_template = ATTRIBUTS_TEMPLATES.get(cat_name, None)
            if attribs_template:
                for attr_name, valeurs_possibles in attribs_template.items():
                    valeur = random.choice(valeurs_possibles)
                    AttributProduit.objects.create(
                        produit=produit,
                        nom_attribut=attr_name,
                        valeur=valeur
                    )

            produits_crees += 1
            self.stdout.write(self.style.SUCCESS(f"Créé : {nom_produit} (Catégorie: {cat_name})"))

        self.stdout.write(self.style.SUCCESS(f"\nTotal {produits_crees} produits créés pour le vendeur {vendeur.username} (ID {vendeur_id})."))
