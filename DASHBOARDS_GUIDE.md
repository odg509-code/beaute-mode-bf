# 📊 Guide d'Utilisation des Tableaux de Bord

## Accès Rapide

### Page Principale
- **URL:** http://127.0.0.1:8000/

### Authentification
- **Connexion:** http://127.0.0.1:8000/compte/connexion/
- **Inscription:** http://127.0.0.1:8000/compte/inscription/

## Comptes de Test

### 1. Client 👤
```
Utilisateur: client_test
Mot de passe: TestPassword123
URL Dashboard: http://127.0.0.1:8000/compte/tableau-de-bord/client/
```

**Fonctionnalités:**
- Consulter ses commandes
- Voir le total dépensé
- Suivre le statut des commandes
- Accéder au profil
- Gérer les paramètres

### 2. Vendeur 🛍️
```
Utilisateur: vendeur_test
Mot de passe: TestPassword123
URL Dashboard: http://127.0.0.1:8000/compte/tableau-de-bord/vendeur/
```

**Fonctionnalités:**
- Gérer ses produits
- Visualiser le revenu total
- Consulter les ventes
- Ajouter/éditer des produits
- Voir les statistiques

### 3. Institut 💇‍♀️
```
Utilisateur: institut_test
Mot de passe: TestPassword123
URL Dashboard: http://127.0.0.1:8000/compte/tableau-de-bord/institut/
```

**Fonctionnalités:**
- Gérer les rendez-vous
- Voir les services offerts
- Consulter la liste des clients
- Éditer les informations
- Vérifier le statut

### 4. Styliste 👗
```
Utilisateur: styliste_test
Mot de passe: TestPassword123
URL Dashboard: http://127.0.0.1:8000/compte/tableau-de-bord/styliste/
```

**Fonctionnalités:**
- Gérer le portfolio
- Voir les réservations
- Consulter les avis
- Ajouter des réalisations
- Suivre les statistiques

## Flux de Connexion

### Option 1: Créer un nouveau compte
1. Allez à http://127.0.0.1:8000/compte/inscription/
2. Remplissez le formulaire:
   - Prénom & Nom
   - Email
   - Nom d'utilisateur
   - Pays (liste déroulante)
   - Ville
   - Téléphone
   - Mot de passe (min 8 caractères)
3. Cliquez "Créer mon compte"
4. Vous êtes automatiquement connecté
5. Redirigé vers votre dashboard

### Option 2: Se connecter
1. Allez à http://127.0.0.1:8000/compte/connexion/
2. Entrez vos identifiants (utilisateur de test)
3. Cliquez "Se connecter"
4. Redirigé automatiquement vers votre dashboard

## Navigation dans les Dashboards

### Menu Utilisateur (En-tête)
- **Clic sur le nom:** Affiche le menu dropdown
  - 📊 Tableau de bord
  - 👤 Mon profil
  - ⚙️ Paramètres
  - 🚪 Déconnexion

### Sidebar Navigation
Chaque dashboard possède une navigation latérale:
- Pages principales (avec indicateur actif)
- Liens vers les sections
- Bouton déconnexion (rouge)

### Éléments Interactifs
- **Stat Cards:** Affichent les chiffres clés
- **Buttons:** 
  - Or pour les actions principales
  - Small pour les actions secondaires
- **Tables:** Listes avec actions (Voir, Éditer, Supprimer)
- **Empty States:** Messages quand aucune donnée

## Points de Contrôle

### ✓ Pages à Tester

1. **Inscription**
   - [ ] Tous les champs se remplissent
   - [ ] Validation des champs (email, min password)
   - [ ] Sélecteur de pays fonctionne
   - [ ] Création du compte réussit
   - [ ] Redirection vers dashboard

2. **Connexion**
   - [ ] Peut se connecter avec les comptes test
   - [ ] Message d'erreur si mauvais identifiants
   - [ ] Redirection vers dashboard automatique
   - [ ] Lien vers inscription fonctionne

3. **Dashboard Client**
   - [ ] Affiche le nom de l'utilisateur
   - [ ] Affiche les stats (0 commandes)
   - [ ] Section commandes visible (vide)
   - [ ] Navigation sidebar fonctionne
   - [ ] Bouton déconnexion fonctionne

4. **Dashboard Vendeur**
   - [ ] Affiche les stats (0 produits, 0 ventes)
   - [ ] Section produits avec bouton "Ajouter"
   - [ ] Grid de produits responsive
   - [ ] Boutons Éditer/Supprimer visibles
   - [ ] Section "Ventes récentes"

5. **Dashboard Institut**
   - [ ] Affiche les stats (rendez-vous, évaluation)
   - [ ] Affiche les infos de l'institut
   - [ ] Statut de vérification visible
   - [ ] Bouton "Éditer informations"
   - [ ] Section rendez-vous du jour

6. **Dashboard Styliste**
   - [ ] Affiche les stats (réalisations, réservations)
   - [ ] Section portfolio avec "Ajouter"
   - [ ] Section réservations récentes
   - [ ] Design cohérent

### ✓ Responsive Design
- [ ] Desktop (1200px+): Sidebar fixe, contenu large
- [ ] Tablet (1024px): Sidebar horizontal
- [ ] Mobile (700px): Navigation compacte, adapté mobile

### ✓ Styles & UX
- [ ] Cohérence de la palette (marron, or)
- [ ] Fonts Playfair Display & DM Sans
- [ ] Hover effects sur les boutons
- [ ] Icônes appropriées
- [ ] Messages vides explicites

## Structure des Fichiers

```
templates/
├── base.html (modifié - menu utilisateur)
├── registration/
│   ├── login.html (amélioré)
│   └── signup.html (amélioré)
├── accounts/
│   ├── customer_dashboard.html (nouveau)
│   ├── seller_dashboard.html (nouveau)
│   ├── institute_dashboard.html (nouveau)
│   └── stylist_dashboard.html (nouveau)

accounts/
├── views.py (5 vues dashboard)
├── urls.py (5 URLs dashboard)
├── models.py (User.country ajouté)
└── forms.py (Country field ajouté)
```

## Dépannage

### Problème: Dashboard vide/blanc
→ Assurez-vous d'être connecté
→ Vérifiez l'URL du dashboard
→ Rafraîchissez la page (Ctrl+F5)

### Problème: Impossible de se connecter
→ Vérifiez le nom d'utilisateur/mot de passe
→ Assurez-vous que le serveur Django tourne
→ Vérifiez qu'aucun message d'erreur n'est affiché

### Problème: Redirection infinite
→ Vérifiez les paramètres de Django
→ Consultez les logs du serveur
→ Vérifiez les URL patterns

## Prochaines Étapes

- [ ] Intégration API pour charger les vraies données
- [ ] Fonctionnalités d'édition de produits
- [ ] Système de réservations (Institut)
- [ ] Gestion du portfolio (Styliste)
- [ ] Notifications utilisateur
- [ ] Intégration paiement
- [ ] Système d'avis et évaluations
- [ ] Chat utilisateur
