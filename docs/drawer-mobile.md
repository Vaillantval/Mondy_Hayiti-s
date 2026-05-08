# Drawer Mobile — Documentation complète

## Vue d'ensemble

Le drawer mobile est le panneau latéral qui s'ouvre depuis la droite sur les écrans ≤ 991px. Il remplace le menu Bootstrap collapse classique (expansion verticale) par un panneau off-canvas horizontal.

---

## Fichier concerné

```
templates/partials/header.html
```

---

## Structure HTML

```
<header class="header_wrap fixed-top header_with_topbar active">
│
├── #app-banner (bandeau APK, optionnel)
├── .hd-topbar (top bar desktop, cachée sur mobile)
│
└── .hd-navbar-wrap
    └── <nav class="navbar navbar-expand-lg">
        │
        ├── .navbar-brand (logo)
        │
        ├── .hd-mobile-icons          ← loupe + panier, toujours visibles sur mobile
        │   ├── .search_trigger
        │   └── a[href=cart] + .cart_count
        │
        ├── <button class="navbar-toggler">   ← BURGER (ouvre/ferme le drawer)
        │   data-bs-toggle="collapse"
        │   data-bs-target="#navbarMain"
        │
        └── #navbarMain.navbar-collapse.collapse   ← LE DRAWER
            │
            ├── .hd-drawer-head.d-lg-none          ← barre "Menu" + bouton ✕
            │   ├── .hd-drawer-head-title "Menu"
            │   └── #hdDrawerClose (bouton ✕)
            │
            ├── .hd-drawer-user.d-lg-none          ← "Bonjour, username" si connecté
            │
            ├── <ul class="navbar-nav">            ← liens principaux
            │   ├── Accueil
            │   ├── Pages (dropdown)
            │   ├── Produits (mega menu → dropdown static sur mobile)
            │   ├── Boutique
            │   └── Contact
            │
            ├── <ul class="navbar-nav attr-nav">   ← icônes desktop (cachées sur mobile)
            │   ├── Recherche
            │   ├── Compte (dropdown)
            │   └── Panier (preview dropdown)
            │
            └── .hd-mobile-nav-section             ← liens compte (mobile uniquement)
                ├── Tableau de bord / Se connecter
                ├── Mes commandes / Créer un compte
                ├── Mes favoris
                ├── Comparer
                └── Déconnexion (si connecté)

    └── #hdDrawerOverlay   ← overlay sombre (actuellement dans .hd-navbar-wrap)
```

---

## CSS — Classes et règles

### Classes globales (tous écrans)

| Classe | Rôle |
|--------|------|
| `.hd-mobile-icons` | `display:none` par défaut, `display:flex` sur mobile |
| `.hd-mobile-nav-section` | `display:none` par défaut, `display:flex` sur mobile |
| `.hd-mobile-nav-link` | Style des liens dans la section compte |
| `.hd-drawer-overlay` | Overlay sombre, `display:none` par défaut |
| `.hd-drawer-overlay.show` | `display:block` quand le drawer est ouvert |

### Règles mobile `@media (max-width: 991px)`

```css
/* Panneau drawer */
#navbarMain {
    position: fixed !important;
    top: 0; right: 0;
    width: 78vw; max-width: 280px;
    height: 100dvh;
    background: #fff;
    z-index: 1055;
    transform: translateX(110%);      /* caché à droite par défaut */
    transition: transform .28s ease;
    display: flex !important;         /* ⚠️ override Bootstrap display:none */
    flex-direction: column;
    box-shadow: -4px 0 24px rgba(0,0,0,.15);
}

#navbarMain.show       { transform: translateX(0); }   /* ouvert */
#navbarMain.collapsing { height: 100dvh !important; }  /* pendant animation */
```

### Overlay

```css
.hd-drawer-overlay {
    display: none;
    position: fixed; inset: 0;
    background: rgba(0,0,0,.45);
    z-index: 1053;
}
.hd-drawer-overlay.show { display: block; }
```

---

## JavaScript

Le script est en bas de `header.html`, APRÈS `</header>` :

```javascript
(function () {
    var drawer   = document.getElementById('navbarMain');
    var overlay  = document.getElementById('hdDrawerOverlay');
    var closeBtn = document.getElementById('hdDrawerClose');
    var toggler  = document.querySelector('.navbar-toggler');

    function closeDrawer() {
        if (drawer && drawer.classList.contains('show') && toggler) {
            toggler.click();  // délègue la fermeture à Bootstrap
        }
    }

    // Ouverture → affiche overlay + bloque scroll
    drawer.addEventListener('show.bs.collapse', function () {
        overlay.classList.add('show');
        document.body.classList.add('hd-drawer-open');
    });

    // Fermeture → cache overlay + libère scroll
    drawer.addEventListener('hidden.bs.collapse', function () {
        overlay.classList.remove('show');
        document.body.classList.remove('hd-drawer-open');
    });

    overlay.addEventListener('click', closeDrawer);
    closeBtn.addEventListener('click', closeDrawer);
})();
```

---

## Mécanisme d'ouverture/fermeture

### Ouverture (burger)
1. Clic sur `.navbar-toggler`
2. Bootstrap ajoute `.collapsing` puis `.collapse.show` sur `#navbarMain`
3. CSS : `transform: translateX(0)` → le drawer glisse depuis la droite
4. L'événement `show.bs.collapse` ajoute `.show` sur l'overlay + bloque le scroll body

### Fermeture théorique (✕ ou overlay)
1. Clic sur `#hdDrawerClose` ou `#hdDrawerOverlay`
2. `closeDrawer()` vérifie `drawer.classList.contains('show')` → true
3. `toggler.click()` → Bootstrap traite le clic
4. Bootstrap retire `.show`, ajoute `.collapsing`, puis retire `.collapsing`
5. CSS : `transform: translateX(110%)` → le drawer glisse hors écran
6. `hidden.bs.collapse` retire `.show` sur l'overlay + libère le scroll

---

## Bugs connus et causes racines

### Bug 1 — Le drawer ne se ferme pas (actuel)

**Symptôme** : cliquer ✕ ou l'overlay n'a aucun effet.

**Causes possibles** :

#### A) `display: flex !important` empêche Bootstrap de fermer
Bootstrap ferme un collapse via `.collapse:not(.show) { display: none }`. La règle `display: flex !important` dans notre CSS override ce `display: none`. Bootstrap pense avoir fermé le drawer (retire `.show`) mais le `display: flex` le maintient visible. La transition `transform` peut aussi ne pas se déclencher si Bootstrap manipule `height` et déclenche un reflow inattendu.

#### B) Conflit entre le mécanisme Bootstrap collapse et le CSS transform
Bootstrap gère le collapse via des animations de `height` (0 → auto, auto → 0). Notre CSS override `height: 100dvh !important` et `transition: transform`. Bootstrap peut ne pas détecter correctement la fin d'animation (`transitionend`), ce qui bloque la complétion de la séquence de fermeture.

#### C) z-index stacking context
Le `<header>` a `position: fixed; z-index: 1030` (Bootstrap `.fixed-top`) → crée un stacking context. `#navbarMain` à `z-index: 1055` est dans ce contexte (effectivement sous le z-index global 1030). L'overlay à `z-index: 1053` (en dehors du header, ou dedans selon position) peut peindre par-dessus le drawer et intercepter les clics sur ✕.

---

## Solution recommandée : drawer entièrement custom, sans Bootstrap collapse

Supprimer la dépendance à `data-bs-toggle="collapse"` et gérer le drawer 100% en JS custom.

### Changements HTML

```html
<!-- Burger : retirer data-bs-toggle / data-bs-target -->
<button type="button" id="hdBurger" class="navbar-toggler" aria-label="Ouvrir le menu">
    <span class="ion-android-menu"></span>
</button>

<!-- #navbarMain : retirer la classe "collapse" -->
<div id="navbarMain" class="navbar-collapse justify-content-between">
    ...
</div>
```

### Changements CSS

```css
/* Retirer les règles Bootstrap collapse override */
/* Garder uniquement : */
#navbarMain {
    position: fixed;
    top: 0; right: 0;
    width: 78vw; max-width: 280px;
    height: 100dvh;
    background: #fff;
    z-index: 1055;
    transform: translateX(110%);
    transition: transform .28s ease;
    display: flex;
    flex-direction: column;
    overflow-y: auto;
    box-shadow: -4px 0 24px rgba(0,0,0,.15);
}

#navbarMain.hd-open { transform: translateX(0); }
```

### Changements JS

```javascript
(function () {
    var drawer   = document.getElementById('navbarMain');
    var overlay  = document.getElementById('hdDrawerOverlay');
    var burger   = document.getElementById('hdBurger');
    var closeBtn = document.getElementById('hdDrawerClose');

    function openDrawer() {
        drawer.classList.add('hd-open');
        overlay.classList.add('show');
        document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
        drawer.classList.remove('hd-open');
        overlay.classList.remove('show');
        document.body.style.overflow = '';
    }

    burger.addEventListener('click', function () {
        drawer.classList.contains('hd-open') ? closeDrawer() : openDrawer();
    });

    overlay.addEventListener('click', closeDrawer);
    closeBtn.addEventListener('click', closeDrawer);
})();
```

### Avantages
- Zéro conflit avec Bootstrap collapse
- Contrôle total sur l'animation
- Pas de `!important` nécessaire
- `transitionend` non impliqué
- Fermeture fiable à 100%

---

## Dépendances

| Élément | Fichier |
|---------|---------|
| Bootstrap 5 JS | `static/assets/bootstrap/js/bootstrap.min.js` (chargé en bas de `base.html`) |
| jQuery | `static/assets/js/jquery-3.6.0.min.js` (chargé en bas de `base.html`) |
| Themify icons (`ti-*`) | `static/assets/css/themify-icons.css` |
| Linearicons | `static/assets/css/linearicons.css` |
| Ionicons (`ion-*`) | `static/assets/css/ionicons.min.css` |

---

## z-index utilisés dans le header

| Élément | z-index | Contexte |
|---------|---------|----------|
| `.header_wrap.fixed-top` | 1030 | Bootstrap, global |
| `#app-banner` | 1050 (inline style) | Dans le header |
| `#hdDrawerOverlay` | 1053 | Dans le header (même stacking context) |
| `#navbarMain` | 1055 | Dans le header (même stacking context) |
