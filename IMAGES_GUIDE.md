# 📸 Guide des Images - Beauté & Mode BF

## Structure des Dossiers

Les images doivent être placées dans `/static/images/` avec cette structure:

```
static/images/
├── hero/
│   └── mode-africaine.jpg          # Image héro (1200x600px)
├── sections/
│   ├── faso-dan-fani.jpg           # Cartes "Tissus & Pagnes" (400x300px)
│   ├── tenue-traditionelle-bleue.jpg  # Cartes "Mode Africaine" (400x300px)
│   └── tissu-closeup.jpg           # Section "Faso Dan Fani" (500x400px)
├── artisans/
│   ├── tissage.jpg                 # Artisanes tissage (240x240px)
│   ├── teinture.jpg                # Teinture naturelle (240x240px)
│   └── creation.jpg                # Création & Design (240x240px)
└── perfumes/
    ├── fragrances.jpg              # Cartes parfums (400x300px)
    ├── parfum-prestige.jpg         # Parfums prestige (400x300px)
    └── essences-naturelles.jpg     # Essences naturelles (400x300px)
```

## Images à Utiliser

Vous avez fourni ces images:

### 1. **Parfums de Luxe** 
   - Fichier: `perfumes/parfum-prestige.jpg`
   - Utilisé dans: Section "PARFUMERIE SÉLECTIONNÉE" (Parfums Prestige)
   - Dimensions recommandées: 400x300px

### 2. **Atelier de Tissage** ✂️
   - Fichier: `artisans/tissage.jpg`
   - Utilisé dans: Section "RENCONTREZ NOS ARTISANES" (Tissage à la main)
   - Dimensions recommandées: 240x240px

### 3. **Tenue Traditionnelle Bleue** 👗
   - Fichier: `sections/tenue-traditionelle-bleue.jpg` (carte NOS UNIVERS)
   - Fichier: `artisans/creation.jpg` (section artisanes)
   - Dimensions recommandées: 400x300px (carte), 240x240px (artisanes)

### 4. **Tenue Traditionnelle Verte** 💚
   - Fichier: `sections/faso-dan-fani.jpg`
   - Utilisé dans: Section "FASO DAN FANI" (côté texte)
   - Dimensions recommandées: 400x300px

### 5. **Gros Plan Tissu Faso Dan Fani** 🧵
   - Fichier: `sections/tissu-closeup.jpg`
   - Utilisé dans: Section "FASO DAN FANI" (highlight-image)
   - Dimensions recommandées: 500x400px

### 6. **Tissu Faso Dan Fani Bleu/Orange** 📦
   - Fichier: `perfumes/fragrances.jpg` (reuse pour cartes)
   - Utilisé dans: Section "NOS UNIVERS" (carte Beauté & Bien-être)
   - Dimensions recommandées: 400x300px

### 7. **Parfum Rouge de Luxe** 🌹
   - Fichier: `perfumes/essences-naturelles.jpg`
   - Utilisé dans: Section "PARFUMERIE SÉLECTIONNÉE" (Essences Naturelles)
   - Dimensions recommandées: 400x300px

## Instructions de Téléchargement

1. **Téléchargez** vos images de haute qualité
2. **Nommez-les** selon la structure ci-dessus
3. **Redimensionnez-les** aux dimensions recommandées
4. **Placez-les** dans les dossiers correspondants sous `/static/images/`
5. **Rafraîchissez** votre navigateur (Ctrl+F5)

## Fallback Temporaire

Pendant ce temps, le site utilise des images Unsplash comme placeholder. 
Une fois vos images locales placées, elles remplaceront automatiquement les placeholders.

## Notes

- Les images doivent être au format JPG ou PNG
- Pour de meilleures performances, optimisez vos images (compression)
- Les dimensions recommandées assurent un affichage optimal
- Les images sont utilisées avec `background-size: cover` pour remplir les zones
