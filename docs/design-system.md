# Design System — MatStore Haiti

Documentation complète du style visuel, des couleurs, de la typographie et des composants de tous les templates du projet.

---

## Table des matières

1. [Palette de couleurs](#1-palette-de-couleurs)
2. [Typographie](#2-typographie)
3. [Espacement & Border-radius](#3-espacement--border-radius)
4. [Ombres](#4-ombres)
5. [Animations & Transitions](#5-animations--transitions)
6. [Icônes](#6-icônes)
7. [Composants](#7-composants)
   - [Header & Navigation](#71-header--navigation)
   - [Footer](#72-footer)
   - [Cartes produit](#73-cartes-produit)
   - [Formulaires & Inputs](#74-formulaires--inputs)
   - [Boutons](#75-boutons)
   - [Badges & Labels](#76-badges--labels)
   - [Toast notifications](#77-toast-notifications)
8. [Layouts](#8-layouts)
   - [Base boutique](#81-base-boutique-basehtml)
   - [Dashboard client](#82-dashboard-client)
   - [Checkout](#83-checkout)
9. [Pages — détail visuel](#9-pages--détail-visuel)
   - [Accueil (index)](#91-accueil)
   - [Liste produits (shop_list)](#92-liste-produits)
   - [Détail produit](#93-détail-produit)
   - [Panier](#94-panier)
   - [Checkout](#95-checkout)
   - [Wishlist](#96-wishlist)
   - [Comparaison](#97-comparaison)
   - [Authentification](#98-authentification-signin--signup)
   - [Dashboard — pages internes](#99-dashboard--pages-internes)
   - [Emails transactionnels](#910-emails-transactionnels)
10. [Préfixes CSS & conventions](#10-préfixes-css--conventions)
11. [Responsive & Breakpoints](#11-responsive--breakpoints)

---

## 1. Palette de couleurs

### Couleurs primaires

| Rôle | Valeur | Usage |
|------|--------|-------|
| Accent / CTA | `#ff5722` | Boutons, liens actifs, badges, bordures focus, icônes |
| Accent clair | `#ff8a65` | Gradients, hover states, avatars |
| Dark Navy | `#1a1a2e` | Fond dark, texte principal fort, sidebar, header topbar |
| Navy secondaire | `#2d2d4e` | Gradients sur éléments dark (mega-menu, dropdowns) |
| Navy profond | `#16213e` | Arrière-plans gradient alternatifs |
| Noir footer | `#0f0f1a` | Fond footer |

### Couleurs neutres

| Rôle | Valeur | Usage |
|------|--------|-------|
| Blanc | `#ffffff` | Fond cartes, formulaires, navbar |
| Gris très clair | `#f4f5f7` | Fond pages dashboard et checkout |
| Gris clair | `#f8f9fa` | Fond sections shop, thead tables |
| Gris bordure | `#e9ecef` / `#eaecf0` | Séparateurs, bordures inputs |
| Gris texte | `#6c757d` | Texte secondaire, descriptions |
| Gris muted | `#8a94a6` | Labels, meta-informations |
| Gris placeholder | `#b0b8c4` | Placeholder inputs |

### Couleurs sémantiques

| Rôle | Valeur | Usage |
|------|--------|-------|
| Succès / En stock | `#22c55e` | Badge stock, confirmations, icône secure |
| Succès alt | `#28a745` | Toast success, badge in-stock |
| Danger / Rupture | `#dc3545` | Badge rupture, toast error, alertes |
| Danger fort | `#dc2626` | Texte erreur formulaire |
| Warning | `#e67e22` | Toast warning |
| Info | `#17a2b8` | Toast info |

### Transparences récurrentes

| Contexte | Valeur |
|----------|--------|
| Overlay slider (gradient dark) | `rgba(10, 10, 20, 0.72)` |
| Éléments sur dark background | `rgba(255,255,255,0.08)` |
| Séparateurs sur dark | `rgba(255,255,255,0.07)` |
| Focus ring inputs | `rgba(255, 87, 34, 0.10)` |
| Accent sur dark (15%) | `rgba(255, 87, 34, 0.15)` |
| Texte secondaire sur dark | `rgba(255,255,255,0.58)` |
| Texte inactif sur dark | `rgba(255,255,255,0.38)` |

### Variables CSS (dashboard)

```css
:root {
    --sidebar-w : 250px;
    --topbar-h  : 60px;
    --dark      : #1a1a2e;
    --accent    : #ff5722;
    --text      : #1a1a2e;
    --muted     : #8a94a6;
    --border    : #eaecf0;
    --bg        : #f4f5f7;
    --card      : #ffffff;
    --radius    : 10px;
}
```

> Ces variables sont définies dans `dashboard/base_dashboard.html`. Les autres zones (boutique, checkout) utilisent les valeurs hexadécimales directement — voir [section 10](#10-préfixes-css--conventions).

---

## 2. Typographie

### Font-families

| Zone | Font | Fallback |
|------|------|---------|
| Boutique (body) | `Poppins` | `sans-serif` |
| Boutique (headings) | `Roboto` | `sans-serif` |
| Dashboard | `Segoe UI` | `system-ui, sans-serif` |
| Emails | `Arial` | `sans-serif` (compatibilité email clients) |

### Échelle de tailles

#### Titres

| Élément | Taille | Weight | Notes |
|---------|--------|--------|-------|
| Hero slider | `52px` | `800` | `letter-spacing: -0.5px` |
| H1 page | `48px` | `700` | |
| H2 section | `28px` | `900` | `letter-spacing: -0.5px` |
| H3 sous-section | `24px` | `700` | |
| Titre page produit | `28px` | `700` | |
| Prix produit (détail) | `32px` | `800` | `color: #ff5722` |
| Titre form box auth | `23px` | `800` | |
| Titre topbar dashboard | `16px` | `700` | |

#### Corps de texte

| Élément | Taille | Weight | Color |
|---------|--------|--------|-------|
| Paragraphe standard | `16px` | `400` | `#6c757d`, `line-height: 1.8` |
| Texte secondaire | `14px` | `400` | `#8a94a6` |
| Texte petits détails | `13px` | `500` | Hérité |
| Label input | `12.5px` | `700` | `#1a1a2e`, `letter-spacing: 0.1px` |
| Caption / metadata | `11.5px–12px` | `400–600` | `rgba(255,255,255,0.38)` sur dark |
| Section nav sidebar | `9.5px` | `700` | `letter-spacing: 1.6px`, uppercase |

#### Boutons

| Type | Taille | Weight | Letter-spacing |
|------|--------|--------|----------------|
| CTA principal | `15px` | `700` | `1.5px` |
| Bouton standard | `14px` | `600` | — |
| Petit bouton | `13px` | `600` | — |

---

## 3. Espacement & Border-radius

### Padding / Margin courants

```
4px  · 5px  · 6px  · 7px  · 8px
10px · 11px · 12px · 13px · 14px
16px · 18px · 20px · 22px · 24px
26px · 28px · 36px · 40px · 48px · 52px · 60px
```

### Border-radius

| Valeur | Usage |
|--------|-------|
| `4px` | Badges simples |
| `8px` · `9px` · `10px` | Inputs, boutons, icônes box, cards dashboard |
| `12px` · `14px` | Option radios (carriers), cartes checkout |
| `16px` · `18px` · `20px` | Cartes larges, dropdowns, form boxes |
| `20px` · `50px` | Pills, badges arrondis complets |
| `50%` | Avatars, badges compteurs ronds |

---

## 4. Ombres

| Niveau | Valeur | Usage |
|--------|--------|-------|
| Subtile | `0 2px 8px rgba(0,0,0,0.06)` | Cards légères |
| Light | `0 2px 12px rgba(0,0,0,0.08)` | Topbar dashboard |
| Medium | `0 4px 24px rgba(0,0,0,0.10)` | Navbar, form boxes |
| Strong | `0 8px 40px rgba(0,0,0,0.12)` | Dropdowns, modals |
| Very strong | `0 20px 60px rgba(0,0,0,0.16)` | Overlay panels |
| CTA hover | `0 8px 25px rgba(255,87,34,0.35)` | Bouton primary au hover |

---

## 5. Animations & Transitions

### Durées standard

| Vitesse | Valeur | Usage |
|---------|--------|-------|
| Rapide | `.15s` · `.16s` | Hover couleur simple |
| Standard | `.18s` · `.2s` | Transitions boutons, links |
| Moyen | `.28s` · `.3s` | Sidebar toggle, images |
| Long | `.45s` | Zoom images produits |
| Très long | `.55s` | Collection cards, entrées animées |

### Easing

- Standard : `ease`, `ease-in-out`
- Zoom produit : `cubic-bezier(.25,.46,.45,.94)`
- Guide entrance : `cubic-bezier(.22,.68,0,1.2)` (légère overdamp)

### Animations nommées

#### `guideEntrance` (checkout banner)
```css
from { opacity: 0; transform: translateY(-14px); }
to   { opacity: 1; transform: translateY(0); }
/* duration: 0.55s, cubic-bezier(.22,.68,0,1.2) */
```

#### `gsSlideUp` (étapes guide checkout)
```css
from { opacity: 0; transform: translateY(10px) scale(.9); }
to   { opacity: 1; transform: translateY(0)    scale(1);  }
/* duration: 0.45s, ease — avec delays 0.10s / 0.22s / 0.34s / 0.46s */
```

#### Toast (base.html JS)
```
Apparition : opacity 0→1, translateX(30px)→0, durée 0.3s
Disparition : opacity 1→0, translateX(0)→30px, durée 0.3s
Auto-dismiss : après 3.5s
```

### Hover states communs

| Élément | Effet |
|---------|-------|
| Image produit (card) | `transform: scale(1.06)`, `0.45s` |
| Collection card image | `scale(1.06)`, `filter: brightness(0.75)`, `0.55s` |
| Card produit | `transform: translateY(-2px)`, shadow increase |
| Bouton CTA | `translateY(-2px)`, `box-shadow: 0 8px 25px rgba(255,87,34,0.35)` |
| Footer links | `color: #ff5722`, `padding-left: 4px` |
| Nav links boutique | Underline slide animation |

---

## 6. Icônes

Le projet utilise **4 librairies d'icônes** combinées :

| Librairie | Préfixe classes | Usage principal |
|-----------|----------------|-----------------|
| Themify Icons | `ti-` | Dashboard, actions, navigation |
| Ion Icons | `ion-ios-` · `ion-` | Étoiles reviews, navicon mobile |
| Linearicons | `linearicons-` | Panier, logo |
| Font Awesome (all.min) | `fa-` · `fas-` | Icônes générales |

**Tailles courantes** : `9px`, `11px`, `13px`, `14px`, `15px`, `16px`, `18px`, `20px`  
**Couleur accent** : `#ff5722` sur éléments actifs / hovered

---

## 7. Composants

### 7.1 Header & Navigation

Le header est composé de **3 couches** (fichier `partials/header.html`).

#### Top Bar (`hd-topbar`)
- Background : `#1a1a2e`
- Padding : `10px 0`
- Border-bottom : `1px solid rgba(255,255,255,0.07)`
- Contenu gauche : devise sélectionnable, téléphone
- Contenu droit : Comparer, Wishlist, Compte, Langue
- **Pills** (`hd-tb-pill`) : `border-radius: 20px`, `padding: 5px 13px`, `font-weight: 500`, `font-size: 13px`
- **Badge compteur** (`hd-tb-badge`) : `16×16px`, `background: #ff5722`, `border-radius: 50%`, `font-size: 9px`
- **Séparateur** (`hd-tb-sep`) : `1×14px`, `background: rgba(255,255,255,0.15)`

#### Navbar principale (`hd-navbar-wrap`)
- Background : `#ffffff`
- Box-shadow : `0 3px 24px rgba(0,0,0,0.10)`
- Height min : `72px`
- **Logo** : positionné en float absolu, `border-radius: 18px`
- **Nav links** : `padding: 24px 18px`, `font-size: 14.5px`, uppercase, underline-animation au hover
- **Search bar** : input inline avec icône

#### Mega Menu Produits
- Border-radius : `20px`
- **Sidebar** : `width: 220px`, `background: linear-gradient(160deg, #1a1a2e, #2d2d4e)`, liste de catégories
- **Body** : `background: #ffffff`, grille `repeat(3, 1fr)`, sous-catégories
- **Footer** : bannières collections, hauteur `58px`, overlay `linear-gradient(to top, rgba(0,0,0,0.62), transparent)`

#### Dropdown compte
- Background : `#ffffff`, `border-radius: 16px`
- **Header** : `linear-gradient(135deg, #1a1a2e, #2d2d4e)`, padding `16px 18px`
- **Avatar** : `40×40px`, `background: linear-gradient(135deg,#ff5722,#ff8a65)`, `border-radius: 50%`
- Transition : `opacity`, `transform`, `visibility`, `222ms ease`

#### Aperçu panier (dropdown)
- Max-height : `260px` (scroll interne)
- Scrollbar : `scrollbar-width: thin`, `scrollbar-color: #e9ecef`
- **Item** : `52×52px` image, `border-radius: 8px`, padding `10px 20px`
- **Bouton retirer** : `26×26px`, `border: 1.5px solid #e9ecef`, hover : `#dc3545`

---

### 7.2 Footer

Fichier `partials/footer.html`.

- Background global : `#0f0f1a`
- Couleur texte : `rgba(255,255,255,.58)`, `font-size: 13.5px`, `line-height: 1.6`

#### Newsletter bar (`ft-nl-bar`)
- Background : `rgba(255,255,255,.04)`, border-bottom subtle
- **Input** : `background: rgba(255,255,255,.07)`, `border: 1px solid rgba(255,255,255,.12)`, `border-radius: 8px`, `width: 220px`
- **Bouton** : `border: 1px solid rgba(255,87,34,.55)`, `color: #ff5722`, hover : `background: #ff5722`, `color: #fff`

#### Brand section (`ft-brand`)
- Logo icon : `38×38px`, `background: #ff5722`, `border-radius: 9px`
- Nom : `font-size: 18px`, `font-weight: 800`, `color: #fff`
- Description : `font-size: 13px`, `color: rgba(255,255,255,.45)`, `max-width: 320px`

#### Titres colonnes (`ft-col-title`)
- `font-size: 13px`, `font-weight: 800`, uppercase, `letter-spacing: 1.2px`
- `border-bottom: 2px solid #ff5722`

#### Liens (`ft-links`)
- `font-size: 13px`, `color: rgba(255,255,255,.48)`
- Icône chevron : `color: #ff5722`, `font-size: 9px`
- Hover : `color: #ff5722`, `padding-left: 4px` (glissement)

#### Réseaux sociaux
- Boutons : `36×36px`, `background: rgba(255,255,255,.07)`, `border-radius: 9px`
- Hover : `background: #ff5722`, `color: #fff`

#### Logos paiement
- Height : `22px`, `opacity: 0.55`
- Filter : `grayscale(1) brightness(1.5)` (monochrome par défaut)
- Hover : `opacity: 1`, `filter: none`

#### Bottom bar (`ft-bottom`)
- Border-top : `1px solid rgba(255,255,255,.07)`, padding `18px 0`
- Copyright : `font-size: 12.5px`, `color: rgba(255,255,255,.30)`

---

### 7.3 Cartes produit

#### Card grille standard (`pc-*`)
Fichier `partials/product_card.html`.

```
┌──────────────────────┐
│  [Image + badges]    │  ← pc-img (aspect-ratio 1/1, padding-top 72%)
│  [Overlay au hover]  │  ← pc-overlay (4 boutons icon)
├──────────────────────┤
│  Catégories          │  ← pc-cats (pills liens)
│  Nom produit         │  ← pc-name (2 lignes max, clamp)
│  Description         │  ← pc-desc
│  ★★★★½  4.5  Marque  │  ← pc-stars (hardcodé 4.5 actuellement)
│  Prix / Prix barré   │  ← pc-price-row
│  En stock / Rupture  │  ← pc-stock
│  [Ajouter] [Détails] │  ← pc-actions
└──────────────────────┘
```

**Badges image** :
- `pc-new` (Nouveau) : vert Bootstrap
- `pc-promo` (Promo) : rouge Bootstrap
- `pc-hot` (Top vente) : orange Bootstrap
- Réduction : `position: absolute`, `background: #ff5722`, coin supérieur

**Overlay hover** :
- 4 boutons icon `pc-ov-btn` : `44×44px`, `border-radius: 50%`, `background: rgba(0,0,0,0.3)`
- Actions : Panier, Voir, Wishlist, Comparer

**Prix** :
- Principal : `color: #ff5722`, `font-weight: 800`
- Barré : `text-decoration: line-through`, `color: #adb5bd`

#### Card liste (`plc-*`)
- Layout : `flex-direction: row`
- Image : `width: 220px`, `height: 210px`, `flex-shrink: 0`
- Corps : plus large, tous détails visibles sans hover

---

### 7.4 Formulaires & Inputs

#### Input standard (`auth-input`)
```css
padding       : 11px 14px
border        : 1.5px solid #e2e5ea
border-radius : 9px
font-size     : 14px
color         : #1a1a2e
background    : #ffffff
```
**Focus** : `border-color: #ff5722`, `box-shadow: 0 0 0 3px rgba(255,87,34,.10)`  
**Placeholder** : `color: #b0b8c4`

#### Champ mot de passe (`pw-wrap`)
- Wrapper `position: relative`
- Bouton œil : `position: absolute`, `right: 12px`, `top: 50%`, `transform: translateY(-50%)`
- Actif (visible) : `color: #ff5722`

#### Select trié (`sort_select`)
- `padding: 7px 30px 7px 12px`, `background: #f8f9fa`
- `border: 1.5px solid #e9ecef`, `appearance: none`, custom SVG

#### Option transporteur (checkout)
```css
border        : 2px solid #e9ecef
border-radius : 12px
padding       : 14px 16px
```
**Sélectionné** : `border-color: #ff5722`, `background: #fff8f6`, `box-shadow: 0 0 0 3px rgba(255,87,34,.10)`

#### Alertes formulaire
- Danger : `background: #fef2f2`, `color: #dc2626`, `border: 1px solid #fecaca`
- Succès : `background: #f0fdf4`, `color: #15803d`, `border: 1px solid #bbf7d0`
- Border-radius : `9px`, padding `11px 14px`

---

### 7.5 Boutons

#### Bouton CTA principal
```css
background    : linear-gradient(135deg, #ff5722, #ff8a65)
color         : #ffffff
padding       : 14px 20px
border-radius : 10px
font-weight   : 600
```
**Hover** : `transform: translateY(-2px)`, `box-shadow: 0 8px 25px rgba(255,87,34,0.35)`

#### Bouton secondaire (outline)
```css
background    : #ffffff
color         : #ff5722
border        : 2px solid #ff5722
border-radius : 10px
```
**Hover** : `background: #ff5722`, `color: #fff`

#### Bouton icône (wishlist, compare)
```css
width/height  : 48px
border        : 1.5px solid #e9ecef
border-radius : 10px
```
**Hover** : `border-color: #ff5722`, `color: #ff5722`

#### Bouton submit auth
```css
width         : 100%
padding       : 13px
background    : #ff5722
border-radius : 9px
font-size     : 15px
font-weight   : 700
```

#### États boutons
| État | Style |
|------|-------|
| Default | Style défini ci-dessus |
| Hover | Translate Y, ombre, couleur |
| Active | `transform: scale(.99)` |
| Disabled | `opacity: .5`, `pointer-events: none` |
| Loading | `opacity: .55`, `pointer-events: none` |

---

### 7.6 Badges & Labels

| Type | Style |
|------|-------|
| Pill standard | `border-radius: 20px`, `padding: 3px 10px`, `font-size: 11px`, `font-weight: 700` |
| Badge carré | `border-radius: 6px`, `padding: 5px 12px` |
| Réduction produit | `position: absolute`, `background: #ff5722`, `color: #fff`, format `-X%` |
| En stock | `background: rgba(40,167,69,0.1)`, `color: #28a745` |
| Rupture | `background: rgba(220,53,69,0.1)`, `color: #dc3545` |
| Nav badge | `background: #ff5722`, `color: #fff`, `border-radius: 20px`, `font-size: 10px` |

---

### 7.7 Toast notifications

Défini en JavaScript dans `base.html`, affiché dans `#toast-container` (position `fixed`, top `85px`, right `20px`, `z-index: 99999`).

```
┌─ ✓ / ✕ / ℹ / ⚠ ─────────────────── × ─┐
│  [icône]  Message texte              [×] │
└───────────────────────────────────────────┘
```

| Type | Couleur bordure gauche |
|------|------------------------|
| `success` | `#28a745` |
| `error` | `#dc3545` |
| `info` | `#17a2b8` |
| `warning` | `#e67e22` |

- Background : `#fff`, `border-radius: 10px`, `box-shadow: 0 4px 24px rgba(0,0,0,0.13)`
- Auto-dismiss : `3.5s`
- Animation : `opacity + translateX(30px→0)` en `0.3s`

> **Incohérence** : `base_checkout.html` utilise les messages Django natifs (`.alert.alert-success`) à la place de ce système de toasts. À uniformiser.

---

## 8. Layouts

### 8.1 Base boutique (`base.html`)

```
┌──────────────────────────────────────────┐
│           HEADER (fixed top)             │  ← partials/header.html
│  [top bar] [navbar + mega-menu]          │
├──────────────────────────────────────────┤
│                                          │
│           {% block content %}            │
│                                          │
├──────────────────────────────────────────┤
│           FOOTER                         │  ← partials/footer.html
└──────────────────────────────────────────┘
```

- Max-width contenu : `1140px` (container Bootstrap)
- Scripts JS chargés en fin de `<body>`, avant `</body>`
- Block `{% block styles %}` dans le `<head>`
- Block `{% block scripts %}` en fin de `<body>`

---

### 8.2 Dashboard client

Fichier `dashboard/base_dashboard.html`. Template **autonome** (ne s'étend pas sur `base.html`).

```
┌────────────┬───────────────────────────────┐
│            │  TOPBAR (sticky, h=60px)       │
│  SIDEBAR   ├───────────────────────────────┤
│  (fixed,   │                               │
│  w=250px,  │   {% block content %}         │
│  bg dark)  │                               │
│            │                               │
└────────────┴───────────────────────────────┘
```

**Sidebar** :
- `position: fixed`, `width: 250px`, `min-height: 100vh`, `background: #1a1a2e`, `z-index: 1000`
- Zones : Logo · User card · Nav (sections + liens) · Footer (déconnexion)
- Lien actif : `border-left: 3px solid #ff5722`, `background: rgba(255,255,255,0.07)`, `color: #fff`

**Main** :
- `margin-left: 250px`, `flex: 1`, `background: #f4f5f7`

**Topbar** :
- `height: 60px`, `background: #fff`, `border-bottom: 1px solid #eaecf0`, `position: sticky`, `top: 0`, `z-index: 500`
- Contenu : Titre page + breadcrumb à gauche, bouton "Boutique" à droite

**Mobile** (< 992px) :
- Sidebar masquée par `transform: translateX(-100%)`, toggle via bouton burger
- `ds-main` passe à `margin-left: 0`

---

### 8.3 Checkout

Fichier `base_checkout.html`. Template **autonome** (ne s'étend pas sur `base.html`).

- Pas de header/footer boutique
- Background body : `#f4f6f9`
- **Topbar checkout** : sticky, white, `box-shadow: 0 2px 12px rgba(0,0,0,0.06)` — contient logo, bouton retour, badge sécurisé
- Layout 2 colonnes : formulaire (gauche) + récapitulatif (droite, sticky `top: 90px`)

---

## 9. Pages — détail visuel

### 9.1 Accueil

Fichier `shop/index.html`, étend `base.html`.

- **Slider principal** : `min-height: 520px`, overlay gradient dark, titre `52px/800`, bouton CTA orange
  - Contrôles : flèches `50×50px` avec `backdrop-filter: blur(6px)`, points `8px` → active `#ff5722 + scale(1.3)`
- **Section Collections** : grille featured (grand) + 3 cards — `border-radius: 18px`, zoom image au hover
- **Section produits** : grille `repeat(4,1fr)` desktop → responsive, cartes `pc-*`

---

### 9.2 Liste produits

Fichier `shop/shop_list.html`, étend `base.html`.

- Layout : sidebar filtres (gauche) + zone produits (droite)
- **Toolbar** : résultats count + select tri + toggle vue (grille/liste)
- **Sidebar widget** : `padding: 25px`, `border: 1px solid #f0f0f0`
- **Filtres prix** : range slider
- Vue grille / vue liste basculable via JS (classes `grid-view` / `list-view`)

---

### 9.3 Détail produit

Fichier `shop/product_detail.html`, étend `base.html`.

**Colonne gauche (galerie sticky)** :
- `position: sticky`, `top: 90px`
- Image principale : `aspect-ratio: 1/1`, `cursor: zoom-in`, hover `scale(1.09)`, hint badge opacity au hover
- Thumbnails : `74×74px`, strip scrollable horizontalement, sélectionné : `border: 2px solid #ff5722`

**Colonne droite (infos)** :
- Titre : `28px`, `font-weight: 700`
- Prix : `32px`, `font-weight: 800`, `color: #ff5722`
- Prix barré : `text-decoration: line-through`, `color: #adb5bd`
- Sélecteur quantité : boutons `−` / `+` avec input centré
- Boutons : Ajouter au panier (gradient) + Acheter maintenant (outline)
- Actions secondaires : Wishlist + Comparer (boutons icon `48×48px`)

**Tabs** : Description · Spécifications · Avis  
**Produits associés** : grille ou carousel

---

### 9.4 Panier

Fichier `shop/cart.html`, étend `base.html`.

- **Cart table** :
  - Thead : `background: #f8f9fa`, uppercase, `letter-spacing: 0.6px`
  - Image produit : `64×64px`, `border-radius: 10px`
  - Sélecteur quantité : inline
  - Ligne total : bold, `color: #ff5722`
- **Summary card** (droite sticky) :
  - Header gradient : `linear-gradient(135deg, #1a1a2e, #2d2d4e)`, `color: #fff`
  - Lignes : Sous-total · Livraison · Taxes · **Total TTC**
  - Bouton checkout : pleine largeur, gradient orange

---

### 9.5 Checkout

Fichier `shop/checkout.html`, étend `base_checkout.html`.

**Steps indicator** (4 étapes) :
- Cercles numérotés reliés par lignes
- Inactif : `color: #adb5bd`
- Actif : `background: #ff5722`, `color: #fff`
- Complété : `background: #22c55e`, `color: #fff`

**Guide banner** :
- Gradient dark, `border-radius: 16px`, animation `guideEntrance`
- 4 steps icônes avec animation `gsSlideUp` décalée

**Formulaire** :
- Sections fieldset avec `border: 1px solid #f0f0f0`
- Options transporteur : radios stylisées (voir [7.4](#74-formulaires--inputs))
- Options paiement : grille avec icons Stripe/MonCash/Hors ligne

**Récapitulatif** (droite) :
- Sticky `top: 90px`
- Liste articles + totaux + bouton confirmer

---

### 9.6 Wishlist

Fichier `shop/wishlist.html`, étend `base.html`.

- Grille `wl-card` : 3-4 colonnes
- Hover card : `box-shadow: 0 10px 32px`, `transform: translateY(-3px)`
- Empty state : icône `38px`, texte centré, bouton CTA vers boutique

---

### 9.7 Comparaison

Fichier `shop/compare.html`, étend `base.html`.

- Table comparative horizontale
- Scroll horizontal sur mobile
- Alternance légère de couleur par ligne

---

### 9.8 Authentification (signin / signup)

Fichiers `accounts/signin.html` et `accounts/signup.html`, étendent `base.html`.

**Layout 2 colonnes** :
```
┌──────────────────┬──────────────────────────┐
│  Brand panel     │  Form panel              │
│  (42%, dark)     │  (58%, #f4f5f7)          │
│                  │  ┌─────────────────────┐ │
│  Logo            │  │  Form box           │ │
│  Titre           │  │  (max-w 420px,      │ │
│  Avantages       │  │   white, shadow)    │ │
│  (perks list)    │  │                     │ │
│                  │  └─────────────────────┘ │
└──────────────────┴──────────────────────────┘
```

- **Brand panel** : `background: #1a1a2e`, 2 cercles décoratifs pseudo-éléments (`rgba(255,87,34,.12)`, `.07`)
- **Form box** : `border-radius: 18px`, `box-shadow: 0 4px 32px rgba(0,0,0,.07)`, `padding: 40px 36px`
- Mobile (< 900px) : brand panel masqué, form pleine largeur

---

### 9.9 Dashboard — pages internes

Toutes étendent `dashboard/base_dashboard.html`.

#### Overview (`dashboard/overview.html`)
- Stat cards (`ds-stat-card`) : 3 couleurs — orange, bleu, vert
- Stat icon : `44×44px`, fond coloré pastel, border colorée
- Stat value : `24px`, `font-weight: 800`
- Mini wishlist cards (`ds-wl-card`) : `aspect-ratio: 1/1`, zoom image au hover

#### Commandes (`dashboard/orders.html`)
- Table Bootstrap avec header dark
- Badges statut commande (pills colorées)

#### Détail commande (`dashboard/order_detail.html`)
- Card récapitulatif + table articles + timeline statut

#### Adresses (`dashboard/addresses.html`)
- Grille de cards adresses, badge "Par défaut"

#### Profil (`dashboard/profile.html`)
- Profile rows (`ds-profile-row`) : icône box `32×32px` + label + valeur

---

### 9.10 Emails transactionnels

Fichiers `emails/` — templates HTML email (table-based pour compatibilité clients mail).

> **Attention** : La couleur accent des emails est `#e63946` (rouge-orangé) et non `#ff5722`. Incohérence à corriger.

| Zone | Style |
|------|-------|
| Wrapper | Table, max-width `600px`, centré, fond blanc |
| Header email | `background: #e63946`, `padding: 28px 40px`, titre `24px` blanc |
| Body | `padding: 36px 40px`, `font-size: 14px`, `line-height: 1.8` |
| Footer | `background: #f9f9f9`, `border-top: 1px solid #eee`, `padding: 20px 40px` |
| Liens | `color: #e63946`, `text-decoration: none` |

Templates disponibles : `welcome`, `order_confirmation`, `order_status_update`, `admin_new_order`, `offline_order`, `proof_submitted`.

---

## 10. Préfixes CSS & conventions

Le projet utilise une convention de **préfixes par zone** pour éviter les collisions CSS :

| Préfixe | Zone |
|---------|------|
| `hd-` | Header & navigation (topbar, navbar, mega-menu, dropdown) |
| `pc-` | Product card grille standard |
| `plc-` | Product card mode liste |
| `ft-` | Footer |
| `ck-` | Checkout |
| `auth-` | Pages authentification |
| `ds-` | Dashboard client |
| `wl-` | Wishlist |
| `sl-` | Slider/Carousel accueil |
| `hs-` | Home Shop sections |

### Classes utilitaires récurrentes

| Classe | Effet |
|--------|-------|
| `.active` | État actif (lien, tab, bouton) |
| `.disabled` | `opacity: .5`, `cursor: not-allowed` |
| `.loading` | `pointer-events: none`, `opacity: .55` |

---

## 11. Responsive & Breakpoints

Le projet repose sur **Bootstrap 5** avec des overrides CSS custom.

### Breakpoints

| Label | Breakpoint | Comportements clés |
|-------|-----------|-------------------|
| `lg` | `≤ 991px` | Sidebar dashboard masquée, burger visible, navbar collapse, logo static |
| `md` | `≤ 768px` | Layouts 1 colonne, grille produits `repeat(2,1fr)`, slider titre réduit `32px` |
| `sm` | `≤ 576px` | Auth brand masquée, form grid 1 colonne |
| Custom | `≤ 900px` | Spécifique auth : brand panel masqué |
| Custom | `≤ 520px` | Breakpoints internes de certains composants |

### Éléments sticky / fixed

| Élément | Propriété | z-index |
|---------|-----------|---------|
| Header boutique | `position: fixed` | `1000+` |
| Sidebar dashboard | `position: fixed` | `1000` |
| Topbar dashboard | `position: sticky, top: 0` | `500` |
| Topbar checkout | `position: sticky, top: 0` | `100` |
| Galerie produit (gauche) | `position: sticky, top: 90px` | — |
| Card récapitulatif (panier/checkout) | `position: sticky, top: 90px` | — |
| Toasts | `position: fixed, top: 85px, right: 20px` | `99999` |

---

*Dernière mise à jour : 2026-04-10 — MatStore Haiti*
