# Design System — Hayiti's

Référence complète des couleurs, typographies, composants et styles visuels de tous les templates du projet.

---

## 1. Palette de couleurs

### Couleurs principales

| Nom | Valeur | Usage |
|-----|--------|-------|
| Rouge principal | `#C62828` | CTA, prix, badges, accents partout |
| Rouge foncé | `#B71C1C` | Top bar, header app banner, hover |
| Rouge profond | `#8B0000` | Footer bg, gradients sombres |
| Rouge clair | `#EF5350` | Fin de gradient, highlights hover |

### Couleurs de fond et de surface

| Nom | Valeur | Usage |
|-----|--------|-------|
| Fond chaud global | `#FFF8F0` | `body` (via `base.html`) |
| Fond rose pâle | `#FFF5F5` | Image produit, sections alternées, en-têtes de tableau |
| Bordure rose | `#FFCDD2` | Borders de carte, inputs, séparateurs |

### Couleurs de texte

| Nom | Valeur | Usage |
|-----|--------|-------|
| Noir doux | `#1A1A1A` | Headings, texte principal |
| Gris moyen | `#616161` | Texte secondaire, labels |
| Gris clair | `#9E9E9E` | Descriptions, metas, placeholders |
| Gris très clair | `#BDBDBD` | Prix barrés, placeholders de champ |

### Couleurs sémantiques

| Nom | Valeur | Usage |
|-----|--------|-------|
| Vert succès / stock | `#2E7D32` | Badge "En stock", step "done", toast success |
| Rouge erreur / rupture | `#B71C1C` | Badge "Rupture", toast error, texte déconnexion |
| Jaune avertissement / rating | `#F9A825` | Étoiles produit, badge "Hot", toast warning |
| Bleu info | `#0277BD` | Toast info uniquement |

### Gradients récurrents

```css
/* Avatar utilisateur */
background: linear-gradient(135deg, #C62828, #EF5350);

/* Overlay carte collection */
background: linear-gradient(to top, rgba(0,0,0,0.70) 0%, rgba(0,0,0,0.10) 55%, transparent 100%);
```

> **Règle fondamentale :** `#C62828` n'est **jamais** utilisé comme fond de grande surface. Il reste couleur d'accent (texte, bordure, icône, bouton CTA, badge, prix).

---

## 2. Typographie

### Familles de polices

| Police | Type | Chargement |
|--------|------|-----------|
| **Playfair Display** (400, 600, 700, 800) | Serif — titres | Google Fonts |
| **Nunito** (400, 500, 600, 700, 800) | Sans-serif — corps, UI | Google Fonts |

### Règle d'attribution

```css
/* Titres et nom de marque */
h1, h2, h3, h4, h5, h6,
.display-title, .section-title,
.pc-name, .ft-brand-name, .ck-brand { font-family: 'Playfair Display', serif; }

/* Tout le reste : nav, boutons, badges, descriptions */
body, .pc-body, .hd-topbar, .ft-links { font-family: 'Nunito', sans-serif; }
```

### Tailles caractéristiques

| Élément | Taille | Poids |
|---------|--------|-------|
| Nom de la marque (navbar) | 22px | 800 |
| Titre de section (h2) | 22–28px | 800–900 |
| Prix produit | 20px | 800 |
| Nom produit (carte) | 15px | 700 |
| Navigation principale | 14px | 700 |
| Corps / descriptions | 12.5–13.5px | 400–600 |
| Badges / labels | 9–11px | 700–800 + uppercase |

---

## 3. Composants globaux (`base.html`)

### Body

```css
body { background: #FFF8F0; color: #1A1A1A; font-family: 'Nunito', sans-serif; }
```

### Carte produit (`.pc`)

Structure : image → badges → overlay au survol → body (catégorie, nom, description, étoiles, prix, actions).

```css
.pc { background: #fff; border: 1px solid #FFCDD2; border-radius: 20px; }
.pc:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(180,0,0,.13); border-color: #C62828; }

/* Badges */
.pc-new   { background: #2E7D32; color: #fff; }
.pc-promo { background: #B71C1C; color: #fff; }
.pc-hot   { background: #F9A825; color: #1A1A1A; }

/* Discount tag (coin haut-droit) */
.pc-discount-img { background: #C62828; color: #fff; border-radius: 20px; }

/* Overlay au survol */
.pc-overlay { background: rgba(139,0,0,.30); }
.pc-ov-btn:hover { background: #C62828; color: #fff; }

/* Prix */
.pc-price-main { color: #C62828; font-family: 'Playfair Display'; font-size: 20px; font-weight: 800; }
.pc-price-old  { color: #BDBDBD; text-decoration: line-through; }

/* Bouton panier */
.pc-btn-cart { background: linear-gradient(135deg, #C62828, #EF5350); color: #fff; border-radius: 10px; }

/* Bouton détail */
.pc-btn-detail { border: 1.5px solid #FFCDD2; color: #616161; }
.pc-btn-detail:hover { border-color: #C62828; color: #C62828; }

/* Stock */
.pc-in  { color: #2E7D32; }
.pc-out { color: #B71C1C; }
```

### Toast notification

Position : `fixed; top: 85px; right: 20px`. Fond blanc, bordure gauche colorée selon type.

| Type | Couleur bordure |
|------|----------------|
| `success` | `#388E3C` |
| `error` | `#B71C1C` |
| `info` | `#0277BD` |
| `warning` | `#F9A825` |

---

## 4. Header (`partials/header.html`)

Le header est fixe (`fixed-top`), composé de trois couches empilées de haut en bas.

### 4.1 Bandeau application mobile (`#app-banner`)

- Fond : `linear-gradient(90deg, #8B0000, #C62828)`
- Texte blanc, lien téléchargement en bouton rouge `#C62828` / border-radius 20px
- Bouton fermer : `rgba(255,255,255,0.45)`
- Masqué via `localStorage.app_banner_closed`

### 4.2 Top bar (`.hd-topbar`)

- Fond : `#B71C1C` ; texte : `rgba(255,255,255,.95)`
- Caché sur mobile (< 992px)
- **Gauche** : devise, téléphone, livraison (icônes `#ff7043`)
- **Droite** : Comparer, Favoris, Connexion/Inscription — pilules `.hd-tb-pill`
  - hover : `rgba(255,255,255,.18)` + texte `#EF5350`
  - active : `rgba(198,40,40,.20)` + texte `#EF5350`
- Badges compteurs : 15×15px, fond `#C62828`, bordure `#B71C1C`
- Séparateurs `.hd-tb-sep` : 1px, `rgba(255,255,255,.60)`

### 4.3 Navbar principale (`.hd-navbar-wrap`)

- Fond : `#FFFFFF` ; bordure basse : `1.5px solid #FFCDD2` ; shadow : `0 2px 20px rgba(180,0,0,.07)`
- Hauteur min : 70px

**Logo** : image jusqu'à 110px de hauteur, ou fallback texte `Playfair Display 22px 800 #1A1A1A`

**Liens nav** :
- `Nunito 14px 700 #1A1A1A` ; padding `22px 15px`
- Soulignement animé au survol : `2px solid #C62828`, `scaleX(0→1)`
- hover couleur : `#C62828`

**Dropdown standard** :
- Fond `#FFFFFF`, border `#FFCDD2`, radius 14px, shadow `0 8px 40px rgba(180,0,0,.12)`
- Item hover : `rgba(198,40,40,.06)` + texte `#C62828`

**Mega menu Produits** (860px max) :
- **Sidebar gauche** : 210px, gradient `#8B0000 → #B71C1C`
  - Liens : `rgba(255,255,255,.88)`, hover : fond `rgba(198,40,40,.20)` + `#EF5350` + bordure gauche `#C62828`
  - Bouton bas : fond `#C62828`, hover `#8E0000`
- **Corps** : fond blanc, titre Playfair Display, grille catégories 3 colonnes
  - Dot catégorie : 6×6px rond `#C62828`
  - Sous-items : hover → couleur `#C62828` + `padding-left` + bordure gauche `#C62828`
- **Pied** : fond `#FFF5F5`, bannières collections overlay gradient `rgba(139,0,0,.68)`

**Dropdown Compte** (`.hd-account-dropdown`) :
- 242px, radius 16px, shadow `rgba(180,0,0,.14)`
- En-tête : gradient `#8B0000 → #C62828`, avatar gradient `#C62828 → #EF5350`
- Items menu : hover `rgba(198,40,40,.06)` + `#C62828`
- Divider rouge : `#B71C1C`

**Aperçu panier** (`.hd-cart-preview`) :
- 302px, radius 16px, shadow `rgba(180,0,0,.14)`
- Tête : fond `#FFF5F5`, icône `#C62828`
- Badge : `rgba(198,40,40,.10)` + texte `#C62828`
- Bouton "Voir panier" : bordure `#FFCDD2`, hover `#C62828`
- Bouton "Commander" : gradient `#C62828 → #EF5350`

**Barre de recherche** (`.search_wrap`) :
- Fond blanc, bordure `#FFCDD2`
- Input : radius 30px, focus border `#C62828` + ring `rgba(198,40,40,.10)`

**Badge panier** (`.cart_count`) : 17×17px, fond `#C62828`, texte blanc

**Mobile (< 992px)** :
- Top bar cachée
- Navigation mobile via `.hd-mobile-nav-section` : items avec bordure `#FFCDD2`
- Lien déconnexion : `#B71C1C`

---

## 5. Footer (`partials/footer.html`)

Structure : newsletter bar → colonnes → bottom bar.

- **Fond global** : `#8B0000`
- **Police** : `Nunito`, texte `rgba(255,255,255,.88)`

### 5.1 Newsletter bar (`.ft-nl-bar`)

- Fond : `rgba(255,255,255,.09)` ; séparateur bas : `rgba(255,255,255,.15)`
- Input : fond `rgba(255,255,255,.15)`, bordure `rgba(255,255,255,.12)`, radius 8px
- Bouton : transparent avec bordure blanche, hover fond `rgba(255,255,255,.18)`

### 5.2 Corps (`.ft-main`)

4 colonnes (lg) : Brand + Contact | Liens utiles | Catégories | Mon compte

- **Logo** : icône `#C62828` radius 9px + `Playfair Display 20px 800 #fff`
- **Titres de colonne** (`.ft-col-title`) : `Playfair Display 14px 700 #fff`, bordure basse `rgba(255,255,255,.95) 2px`
- **Liens** : `rgba(255,255,255,.78)`, hover blanc + `padding-left: 4px`
- **Icônes contact** : 28×28px, fond `rgba(255,255,255,.12)`, radius 7px
- **Réseaux sociaux** : 36×36px, fond `rgba(255,255,255,.15)`, hover fond `rgba(255,255,255,.60)`
- **Trust badges** : texte `rgba(255,255,255,.95)`, icônes `rgba(255,255,255,.90)`

### 5.3 Bottom bar (`.ft-bottom`)

- Séparateur haut : `rgba(255,255,255,.15)`
- Copyright : `rgba(255,255,255,.90)` 12.5px
- Logos paiements : opacité 52%, grayscale → couleur au survol

---

## 6. Page d'accueil (`shop/index.html`)

Hérite de `base.html`.

### Section Collections (`.hs-collections-section`)

- Fond : `#FFF5F5` ; padding : 28px/24px
- Titre : `Playfair Display 22px 900 #1A1A1A`, mot-clé en `#C62828`
- Bouton "Voir boutique" : bordure `2px solid #1A1A1A`, hover : fond `#B71C1C` bordure `#B71C1C` texte blanc

**Carrousel** (`.hs-carousel-track`) :
- `overflow-x: auto`, `scroll-snap-type: x mandatory`, scrollbar masquée
- Cartes : `flex: 0 0 calc(33.333% - 10px)`, hauteur 200px, radius 14px
- Fond par défaut : `#B71C1C`
- Image : `object-fit: cover`, hover → `scale(1.06)` + `brightness(0.72)`
- Overlay : gradient noir bas vers transparent
- Tag : fond `rgba(198,40,40,0.90)`, blanc, uppercase 9px 700
- CTA : fond blanc, texte `#1A1A1A`, hover fond `#C62828` texte blanc
- Flèches nav : 34×34px blanc, shadow, hover fond `#C62828`

**Responsive** :
- < 992px : 2 cartes visibles (`calc(50% - 7px)`)
- < 576px : 78% largeur, hauteur 170px, flèches cachées

### Section "Nos Spécialités"

- Fond : `#FFF5F5`
- Cartes catégorie : fond blanc, bordure `1.5px solid #FFCDD2`, radius 16px
- Transition : `transform .2s, box-shadow .2s, border-color .2s`

---

## 7. Boutique / Liste produits (`shop/shop_list.html`)

Hérite de `base.html`. Utilise la grille `.shop_container` avec les cartes `.pc` de `base.html`.

```css
.shop_container .product_img { padding-top: 72%; background: #FFF5F5; }
```

---

## 8. Panier (`shop/cart.html`)

Hérite de `base.html`. Fond de page : `#FFF8F0` (hérité).

```css
.cart-card { background: #fff; border-radius: 14px; border: 1px solid #f0f0f0; box-shadow: 0 2px 16px rgba(0,0,0,0.06); }
.cart-table thead th { background: #FFF5F5; color: #616161; }
.cart-table tbody tr:hover { background: #fafafa; }

/* Sélecteur quantité */
.qty-group { border: 1.5px solid #FFCDD2; border-radius: 8px; }
.qty-btn { background: #FFF5F5; }
.qty-btn:hover { background: #FFCDD2; }
```

---

## 9. Checkout (`shop/checkout.html`)

Hérite de `base_checkout.html` (sans header/footer classique).

- **Fond body** : `#f4f6f9`
- **Top bar checkout** : fond blanc, bordure `#FFCDD2`, sticky, shadow légère
  - Bouton retour : fond `#FFF5F5`, bordure `#FFCDD2`, hover fond `#B71C1C` texte blanc
  - Cadenas sécurisé : vert `#2E7D32`

**Étapes (`.ck-step`)** :

| État | Texte | Rond |
|------|-------|------|
| Inactif | `#adb5bd` | `#FFCDD2` |
| Actif | `#C62828` | `#C62828` + ring `rgba(198,40,40,.15)` |
| Terminé | `#2E7D32` | `#2E7D32` |

Séparateur : `#FFCDD2` → `#2E7D32` si step done.

**Bandeau guide (`.ck-guide-banner`)** :
- Gradient : `#6B0000 → #B71C1C → #8B0000`
- Étapes animées (`gsSlideUp`) avec délais 0.1s–0.46s
- Étape active : pulse `rgba(198,40,40,.25)`
- Étape done : vert `#2E7D32`

**Cartes (`.ck-card`)** :
- Fond blanc, radius 18px, bordure `#FFCDD2`, shadow légère

**Layout** : grille `1fr 400px` (> 900px), colonne unique en-dessous.

---

## 10. Dashboard client (`dashboard/base_dashboard.html`)

Layout deux colonnes : sidebar fixe 250px + contenu principal.

### Variables CSS

```css
:root {
    --sidebar-w : 250px;
    --topbar-h  : 60px;
    --sidebar   : #1E2328;   /* quasi-noir bleuté */
    --accent    : #C62828;
    --accent-lt : rgba(198,40,40,.10);
    --dark      : #1A1A1A;
    --text      : #374151;
    --muted     : #6B7280;
    --border    : #E5E7EB;
    --bg        : #F3F4F6;
    --card      : #ffffff;
    --radius    : 10px;
}
```

### Sidebar (`.ds-sidebar`)

- Fond : `#1E2328` ; shadow : `4px 0 24px rgba(0,0,0,.15)`
- Logo : icône `#C62828` radius 9px + shadow `rgba(198,40,40,.45)` + texte `Playfair Display 17px 800 #fff`
- Avatar : gradient `#C62828 → #EF5350`, shadow rouge

| État lien nav | Fond | Texte | Bordure gauche |
|---------------|------|-------|---------------|
| Normal | transparent | `rgba(255,255,255,.55)` | transparent |
| Hover | `rgba(255,255,255,.07)` | `rgba(255,255,255,.88)` | transparent |
| Actif | `rgba(198,40,40,.10)` | `#fff` | `#C62828` |

- Badges : fond `#C62828`, texte blanc 10px 700
- Bouton déconnexion hover : fond `rgba(198,40,40,.15)`, texte `#EF5350`

### Top bar dashboard (`.ds-topbar`)

- Fond blanc, bordure `#E5E7EB`, height 60px
- Bouton "Retour boutique" : fond `#C62828` plein, blanc

### Cartes (`.ds-card`)

- Fond blanc, radius 10px, bordure `#E5E7EB`, shadow très légère

---

## 11. Authentification (`accounts/signin.html`, `signup.html`)

Hérite de `base.html`. Layout deux colonnes (≥ 992px).

### Panneau gauche (`.auth-brand`) — 42% de largeur

- Fond : `#B71C1C`
- Décors ronds en `rgba(198,40,40,.12)` et `rgba(198,40,40,.07)`
- Icône marque : fond `#C62828`, radius 10px
- Titre : blanc 30px 800 ; sous-titre rose `#FFCDD2`
- Texte secondaire : `rgba(255,255,255,.5)`
- Masqué en mobile

### Panneau droit (formulaire)

- Fond blanc
- Inputs : bordure `#FFCDD2`, focus border `#C62828` + ring `rgba(198,40,40,.12)`
- Bouton submit : gradient `#C62828 → #EF5350`
- Lien secondaire : `#C62828`

---

## 12. Emails transactionnels (`emails/`)

HTML inline (compatibilité webmail). Pas de polices Google.

### Structure `base_email.html`

| Zone | Style |
|------|-------|
| Fond extérieur | `#f4f4f4` |
| Carte email | max 600px, fond blanc, radius 8px, shadow `rgba(0,0,0,0.08)` |
| En-tête | Fond `#C62828`, texte blanc 24px bold, sous-titre `#ffd6d8` |
| Corps | Padding 36px 40px, fond blanc |
| Pied | Fond `#f9f9f9`, bordure haut `#eeeeee`, texte `#aaaaaa`, lien `#C62828` |

---

## 13. Icônes utilisées

| Bibliothèque | Préfixe | Usage principal |
|-------------|---------|-----------------|
| Themify Icons | `ti-` | Navigation, UI, actions (panier, cœur, utilisateur…) |
| Linearicons | `linearicons-` | Icônes majeures (panier, loupe) |
| Ionicons | `ion-` | Réseaux sociaux, fermeture |
| Font Awesome | `fa-` | Complémentaire |
| Flaticon | `flaticon-` | Décoratif |

---

## 14. Bibliothèques JS

| Lib | Usage |
|-----|-------|
| jQuery 3.6.0 | Base AJAX (panier, wishlist, compare) |
| Bootstrap 5 | Grille, dropdowns, collapse mobile |
| Owl Carousel | Carrousels produits (accueil featured) |
| Slick | Slider images produit |
| Magnific Popup | Zoom image |
| Isotope | Filtrage grille boutique |
| ElevateZoom | Loupe sur fiche produit |
| Stripe.js (CDN) | Paiement carte |

---

## 15. Récapitulatif couleurs — aide-mémoire

```
ROUGE ACCENT     #C62828  → CTA, prix, accents (jamais fond de grande surface)
ROUGE HOVER      #B71C1C  → Hover boutons, erreur, badge rupture
ROUGE CLAIR      #EF5350  → Avatar gradient fin
FOND CHAUD       #FFFAF6  → Body global, top bar
FOND ROSE        #FDF6F0  → Images produit, sections alternées
BORDURE DOUCE    #EDE0D8  → Cartes, inputs — remplace #FFCDD2
ROSE PILULE      #FFF0EC  → Fond des pills top bar, badge promo
ROSE BORDER      #FFCDD2  → Bordures pilules, inputs (conservé sur composants)
CHOCOLAT PROFOND #1C1410  → Footer, mega sidebar, auth panel, banners
TEXTE NAV        #4A3728  → Liens navbar
TEXTE PRINCIPAL  #1A1A1A  → Headings
GRIS MOYEN       #616161  → Texte secondaire, top bar
GRIS CLAIR       #9E9E9E  → Descriptions / meta
GRIS BARRÉ       #BDBDBD  → Prix anciens, placeholders
VERT SUCCÈS      #2E7D32  → Stock, steps done, toast
JAUNE RATING     #F9A825  → Étoiles, badge hot
SIDEBAR SOMBRE   #1E2328  → Dashboard sidebar (inchangé)
```
