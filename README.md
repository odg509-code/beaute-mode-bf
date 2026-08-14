# Beauté & Mode BF — Django

Marketplace burkinabè de mode, tissus, parfumerie et beauté, construite avec Django.

## Modules

- `accounts` : utilisateur personnalisé, rôles (client, vendeur, institut, styliste, admin) et profils professionnels.
- `catalog` : catégories, produits, images, favoris et avis.
- `commerce` : panier de session, commandes, lignes de commande et interface de paiement prête à connecter un prestataire réel.
- `beauty` : instituts, services et demandes de rendez-vous.

L’administration Django permet de gérer le catalogue, les utilisateurs, les commandes et les instituts dès le MVP.

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py makemigrations accounts catalog commerce beauty
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Par défaut, le projet utilise SQLite pour démarrer simplement. En définissant `DATABASE_URL`, il bascule sur PostgreSQL ; le format attendu est donné dans `.env.example`.

## Sécurité et paiements

Les mots de passe utilisent le système sécurisé de Django, les formulaires sont protégés par CSRF et les réservations exigent une session authentifiée. Aucun faux paiement n'est créé : les modèles `Payment` sont prêts à recevoir l'intégration Mobile Money, Orange Money, Moov Money, carte ou paiement à la livraison.
