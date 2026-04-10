# PROMPT CLAUDE CODE — Refonte visuelle complète : MatStore → Hayiti's

## Contexte du projet

Tu travailles sur un dépôt Django cloné depuis **MatStore Haiti**, une marketplace e-commerce
(matériaux de construction). Ce dépôt va être transformé en boutique en ligne pour
**Hayiti's** — une pâtisserie haïtienne haut de gamme vendant gâteaux, pizzas, bacon,
fromages et autres produits alimentaires.

Le backend Django (modèles, vues, API) reste **intact**. Seul le front-end visuel est à refaire :
tous les templates HTML, le CSS inline/dans les `<style>`, les variables CSS et les noms de marque.

---

## Identité de la marque Hayiti's

| Élément | Valeur |
|---------|--------|
| Nom | **Hayiti's** |
| Secteur | Pâtisserie & Alimentation fine |
| Produits | Gâteaux · Pizzas · Bacon · Fromages · Douceurs |
| Ton | Chaleureux · Artisanal · Gourmand · Premium haïtien |
| Baseline (slogan) | *"Fait avec amour, livré chez vous."* |

---

## Nouvelle palette de couleurs — REMPLACER INTÉGRALEMENT

### Correspondance directe (remplacement token par token)

| Rôle | Ancienne valeur (MatStore) | Nouvelle valeur (Hayiti's) |
|------|---------------------------|---------------------------|
| Accent / CTA principal | `#ff5722` | `#C62828` (rouge profond) |
| Accent clair / hover | `#ff8a65` | `#EF5350` (rouge vif) |
| Dark principal (fond nav/sidebar) | `#1a1a2e` | `#3E2723` (brun espresso) |
| Dark secondaire (gradient) | `#2d2d4e` | `#4E342E` (brun moyen) |
| Dark profond (alt gradient) | `#16213e` | `#33190F` (brun nuit) |
| Noir footer | `#0f0f1a` | `#1C0F0A` (brun quasi-noir) |
| Fond général pages | `#f4f5f7` | `#FFF8F0` (crème chaud) |
| Fond sections shop | `#f8f9fa` | `#FDF6EC` (crème clair) |
| Bordures | `#e9ecef` / `#eaecf0` | `#EDD9C0` (beige doré) |
| Texte secondaire | `#6c757d` | `#6D4C41` (brun texte) |
| Texte muted | `#8a94a6` | `#A1887F` (brun clair) |
| Placeholder | `#b0b8c4` | `#BCAAA4` (brun pâle) |
| Succès (stock) | `#22c55e` | `#2E7D32` (vert forêt) |
| Succès alt | `#28a745` | `#388E3C` |
| Danger | `#dc3545` | `#B71C1C` (rouge foncé) |
| Warning | `#e67e22` | `#F9A825` (jaune miel) |
| Info | `#17a2b8` | `#0277BD` |

### Couleurs exclusives à Hayiti's (nouvelles, à ajouter)

```css
:root {
  /* ─── Brand ─────────────────────── */
  --hy-red        : #C62828;   /* rouge signature */
  --hy-red-light  : #EF5350;   /* hover rouge */
  --hy-red-dark   : #8E0000;   /* rouge ombre/deep */
  --hy-brown      : #3E2723;   /* espresso dark */
  --hy-brown-mid  : #6D4C41;   /* brun medium */
  --hy-brown-light: #A1887F;   /* brun clair */
  --hy-cream      : #FFF8F0;   /* fond crème */
  --hy-cream-dark : #F5E6D3;   /* crème foncé / sections */
  --hy-gold       : #F9A825;   /* jaune doré / badges */
  --hy-gold-light : #FFD54F;   /* jaune pâle */
  --hy-beige      : #EDD9C0;   /* bordures chaudes */

  /* ─── Dashboard ─────────────────── */
  --sidebar-w : 250px;
  --topbar-h  : 60px;
  --dark      : #3E2723;
  --accent    : #C62828;
  --text      : #3E2723;
  --muted     : #A1887F;
  --border    : #EDD9C0;
  --bg        : #FFF8F0;
  --card      : #ffffff;
  --radius    : 10px;
}
```

### Transparences — remplacer toutes les occurrences

| Ancienne transparence | Nouvelle transparence |
|-----------------------|-----------------------|
| `rgba(255, 87, 34, 0.10)` | `rgba(198, 40, 40, 0.10)` |
| `rgba(255, 87, 34, 0.15)` | `rgba(198, 40, 40, 0.15)` |
| `rgba(255, 87, 34, 0.35)` | `rgba(198, 40, 40, 0.35)` |
| `rgba(255, 87, 34, 0.55)` | `rgba(198, 40, 40, 0.55)` |
| `rgba(255, 87, 34, .12)` | `rgba(198, 40, 40, .12)` |
| `rgba(255, 87, 34, .07)` | `rgba(198, 40, 40, .07)` |
| `rgba(10, 10, 20, 0.72)` | `rgba(30, 10, 5, 0.72)` |
| `rgba(255,255,255,0.08)` | `rgba(255,252,245,0.08)` |
| `rgba(255,255,255,0.07)` | `rgba(255,252,245,0.07)` |

---

## Typographie — REMPLACER

| Zone | Ancienne font | Nouvelle font | Import |
|------|--------------|---------------|--------|
| Headings boutique | `Roboto` | `Playfair Display` | Google Fonts |
| Body boutique | `Poppins` | `Nunito` | Google Fonts |
| Dashboard | `Segoe UI` | `Nunito` | Google Fonts |
| Emails | `Arial` | `Arial` (inchangé) | — |

**Nouveau tag `<link>` Google Fonts** (remplacer dans `base.html` et `base_dashboard.html`) :

```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;800&family=Nunito:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

**Règles CSS globales à appliquer dans `base.html`** :

```css
body {
  font-family: 'Nunito', sans-serif;
  background-color: #FFF8F0;
  color: #3E2723;
}
h1, h2, h3, h4, h5, h6, .display-title, .section-title {
  font-family: 'Playfair Display', serif;
}
```

---

## Composants — Refonte détaillée

### Header (`partials/header.html`)

#### Top Bar (`hd-topbar`) — RESTYLE COMPLET

**AVANT** : fond dark navy `#1a1a2e` avec texte blanc.  
**APRÈS** : fond brun espresso `#3E2723` avec fine ligne crème en bas.

```css
.hd-topbar {
  background: #3E2723;
  border-bottom: 1px solid rgba(255, 252, 245, 0.10);
}
.hd-tb-pill {
  background: rgba(255,252,245,0.08);
  color: rgba(255,252,245,0.80);
  border-radius: 20px;
  transition: background .18s ease;
}
.hd-tb-pill:hover {
  background: rgba(198,40,40,0.25);
  color: #fff;
}
.hd-tb-badge {
  background: #C62828;
  color: #fff;
  border-radius: 50%;
  font-size: 9px;
}
```

#### Navbar principale (`hd-navbar-wrap`) — FOND CRÈME

**AVANT** : fond blanc `#ffffff`.  
**APRÈS** : fond crème chaud `#FFFDF8` avec bordure beige.

```css
.hd-navbar-wrap {
  background: #FFFDF8;
  border-bottom: 1.5px solid #EDD9C0;
  box-shadow: 0 3px 24px rgba(62,39,35,0.08);
}
.hd-nav-link {
  color: #3E2723;
  font-family: 'Nunito', sans-serif;
  font-weight: 600;
}
.hd-nav-link:hover,
.hd-nav-link.active {
  color: #C62828;
}
/* Underline animation : remplacer la couleur de la barre */
.hd-nav-link::after {
  background: #C62828;
}
```

#### Mega Menu

```css
/* Sidebar catégories */
.hd-mega-sidebar {
  background: linear-gradient(160deg, #3E2723, #4E342E);
}
/* Item actif sidebar */
.hd-mega-sidebar-item.active,
.hd-mega-sidebar-item:hover {
  background: rgba(198,40,40,0.20);
  color: #EF5350;
}
/* Footer bannières mega-menu */
.hd-mega-footer-overlay {
  background: linear-gradient(to top, rgba(30,10,5,0.65), transparent);
}
```

#### Dropdown compte

```css
.hd-account-dropdown-header {
  background: linear-gradient(135deg, #3E2723, #4E342E);
}
.hd-avatar {
  background: linear-gradient(135deg, #C62828, #EF5350);
}
```

---

### Footer (`partials/footer.html`) — REFONTE TOTALE

**AVANT** : fond noir quasi-bleu `#0f0f1a`.  
**APRÈS** : fond brun espresso nuit `#1C0F0A`, texture chaude.

```css
.ft-wrapper {
  background: #1C0F0A;
  color: rgba(255, 248, 240, 0.58);
}

/* Newsletter bar */
.ft-nl-bar {
  background: rgba(255,248,240,0.04);
  border-bottom: 1px solid rgba(255,248,240,0.07);
}
.ft-nl-input {
  background: rgba(255,248,240,0.07);
  border: 1px solid rgba(255,248,240,0.12);
  color: rgba(255,248,240,0.85);
  border-radius: 8px;
}
.ft-nl-btn {
  border: 1px solid rgba(198,40,40,0.55);
  color: #EF5350;
  border-radius: 8px;
}
.ft-nl-btn:hover {
  background: #C62828;
  color: #fff;
}

/* Brand section */
.ft-brand-icon {
  background: #C62828;
  border-radius: 9px;
  width: 38px; height: 38px;
}
.ft-brand-name {
  font-family: 'Playfair Display', serif;
  font-size: 18px;
  font-weight: 800;
  color: #fff;
}
.ft-brand-desc {
  font-size: 13px;
  color: rgba(255,248,240,0.45);
  max-width: 320px;
}

/* Titres colonnes */
.ft-col-title {
  font-size: 12px;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: #fff;
  border-bottom: 2px solid #C62828;
  padding-bottom: 6px;
}

/* Liens */
.ft-links li a {
  font-size: 13px;
  color: rgba(255,248,240,0.48);
  transition: color .18s ease, padding-left .18s ease;
}
.ft-links li a:hover {
  color: #EF5350;
  padding-left: 4px;
}
.ft-links li a i { color: #C62828; font-size: 9px; }

/* Réseaux sociaux */
.ft-social-btn {
  width: 36px; height: 36px;
  background: rgba(255,248,240,0.07);
  border-radius: 9px;
  transition: background .18s ease;
}
.ft-social-btn:hover {
  background: #C62828;
  color: #fff;
}

/* Logos paiement */
.ft-payment-logo {
  height: 22px;
  opacity: 0.55;
  filter: grayscale(1) brightness(1.8);
  transition: opacity .2s, filter .2s;
}
.ft-payment-logo:hover {
  opacity: 1;
  filter: none;
}

/* Barre de copyright */
.ft-bottom {
  border-top: 1px solid rgba(255,248,240,0.07);
  padding: 18px 0;
}
.ft-bottom p {
  font-size: 12.5px;
  color: rgba(255,248,240,0.28);
}
```

---

### Cartes Produit (`pc-*`)

```css
/* Card container */
.pc-card {
  background: #ffffff;
  border: 1px solid #EDD9C0;
  border-radius: 16px;
  transition: transform .2s ease, box-shadow .2s ease;
}
.pc-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 36px rgba(62,39,35,0.12);
}
/* Prix */
.pc-price {
  color: #C62828;
  font-weight: 800;
}
/* Prix barré */
.pc-price-old {
  text-decoration: line-through;
  color: #A1887F;
}
/* Badge réduction */
.pc-discount-badge {
  background: #C62828;
  color: #fff;
}
/* Badges statut */
.pc-new   { background: #2E7D32; color: #fff; }
.pc-promo { background: #B71C1C; color: #fff; }
.pc-hot   { background: #F9A825; color: #3E2723; }

/* Overlay hover (4 boutons action) */
.pc-overlay { background: rgba(30,10,5,0.35); }
.pc-ov-btn {
  background: rgba(255,252,245,0.92);
  color: #3E2723;
  border-radius: 50%;
}
.pc-ov-btn:hover {
  background: #C62828;
  color: #fff;
}
/* Boutons action */
.pc-btn-add {
  background: linear-gradient(135deg, #C62828, #EF5350);
  color: #fff;
  border: none;
}
.pc-btn-add:hover {
  box-shadow: 0 8px 25px rgba(198,40,40,0.35);
  transform: translateY(-2px);
}
.pc-btn-detail {
  border: 2px solid #EDD9C0;
  color: #6D4C41;
  background: transparent;
}
.pc-btn-detail:hover {
  border-color: #C62828;
  color: #C62828;
}
```

---

### Boutons globaux

```css
/* Bouton primaire */
.btn-primary,
.btn-accent {
  background: linear-gradient(135deg, #C62828, #EF5350);
  border: none;
  color: #fff;
  font-weight: 700;
  letter-spacing: 0.8px;
  border-radius: 10px;
}
.btn-primary:hover,
.btn-accent:hover {
  background: linear-gradient(135deg, #8E0000, #C62828);
  box-shadow: 0 8px 25px rgba(198,40,40,0.35);
  transform: translateY(-2px);
}
/* Bouton outline */
.btn-outline-primary {
  border: 2px solid #C62828;
  color: #C62828;
  background: transparent;
}
.btn-outline-primary:hover {
  background: #C62828;
  color: #fff;
}
/* Bouton secondaire (brun) */
.btn-secondary {
  background: #3E2723;
  color: #fff;
  border: none;
}
.btn-secondary:hover {
  background: #4E342E;
}
```

---

### Formulaires & Inputs

```css
.form-control,
.form-select {
  border: 1.5px solid #EDD9C0;
  border-radius: 10px;
  background: #FFFDF8;
  color: #3E2723;
  font-family: 'Nunito', sans-serif;
}
.form-control:focus,
.form-select:focus {
  border-color: #C62828;
  box-shadow: 0 0 0 3px rgba(198,40,40,0.10);
  outline: none;
}
.form-label {
  font-weight: 700;
  font-size: 12.5px;
  color: #3E2723;
  letter-spacing: 0.1px;
}
.form-control::placeholder {
  color: #BCAAA4;
}
```

---

### Page Authentification (`auth-*`)

```css
/* Panel gauche brand */
.auth-brand-panel {
  background: linear-gradient(160deg, #3E2723, #4E342E);
  position: relative;
  overflow: hidden;
}
/* Cercles décoratifs pseudo */
.auth-brand-panel::before {
  background: rgba(198,40,40,0.12);
}
.auth-brand-panel::after {
  background: rgba(198,40,40,0.07);
}
/* Titres + texte avantages */
.auth-brand-title {
  font-family: 'Playfair Display', serif;
  color: #fff;
}
.auth-brand-perk {
  color: rgba(255,248,240,0.75);
}
/* Icône perk */
.auth-perk-icon {
  background: rgba(198,40,40,0.20);
  color: #EF5350;
  border-radius: 8px;
}
/* Form box panel droit */
.auth-form-box {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 32px rgba(62,39,35,0.08);
}
/* Fond du panel droit */
.auth-form-panel {
  background: #FFF8F0;
}
```

---

### Dashboard client (`ds-*`)

```css
/* Sidebar */
.ds-sidebar {
  background: linear-gradient(180deg, #3E2723, #4E342E);
  width: var(--sidebar-w);
}
.ds-sidebar-link {
  color: rgba(255,248,240,0.65);
}
.ds-sidebar-link:hover,
.ds-sidebar-link.active {
  background: rgba(198,40,40,0.20);
  color: #EF5350;
  border-left: 3px solid #C62828;
}
.ds-sidebar-section-label {
  color: rgba(255,248,240,0.35);
  font-size: 9.5px;
  text-transform: uppercase;
  letter-spacing: 1.6px;
}
/* Topbar */
.ds-topbar {
  background: #fff;
  border-bottom: 1px solid #EDD9C0;
  box-shadow: 0 2px 12px rgba(62,39,35,0.06);
}
/* Stat cards */
.ds-stat-card {
  background: #fff;
  border: 1px solid #EDD9C0;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(62,39,35,0.06);
}
/* Valeur stat */
.ds-stat-value {
  font-size: 24px;
  font-weight: 800;
  color: #3E2723;
  font-family: 'Playfair Display', serif;
}
/* Icônes stat */
.ds-stat-icon-red    { background: rgba(198,40,40,0.10); color: #C62828; border: 1px solid rgba(198,40,40,0.20); }
.ds-stat-icon-yellow { background: rgba(249,168,37,0.10); color: #F9A825; border: 1px solid rgba(249,168,37,0.20); }
.ds-stat-icon-green  { background: rgba(46,125,50,0.10);  color: #2E7D32; border: 1px solid rgba(46,125,50,0.20); }
```

---

### Checkout — Steps indicator

```css
/* Cercle numéroté inactif */
.ck-step-circle {
  background: #EDD9C0;
  color: #A1887F;
  border: 2px solid #EDD9C0;
}
/* Actif */
.ck-step-circle.active {
  background: #C62828;
  color: #fff;
  border-color: #C62828;
}
/* Complété */
.ck-step-circle.done {
  background: #2E7D32;
  color: #fff;
  border-color: #2E7D32;
}
/* Ligne de connexion */
.ck-step-line { background: #EDD9C0; }
.ck-step-line.done { background: #2E7D32; }

/* Guide banner */
.ck-guide-banner {
  background: linear-gradient(135deg, #3E2723, #4E342E);
  border-radius: 16px;
}
/* Topbar checkout */
.ck-topbar {
  background: #FFFDF8;
  border-bottom: 1.5px solid #EDD9C0;
  box-shadow: 0 2px 12px rgba(62,39,35,0.06);
}
/* Récapitulatif sticky */
.ck-summary-header {
  background: linear-gradient(135deg, #3E2723, #4E342E);
  color: #fff;
}
/* Option transporteur sélectionnée */
.ck-carrier-option.selected {
  border-color: #C62828;
  background: rgba(198,40,40,0.04);
}
/* Option paiement sélectionnée */
.ck-payment-option.selected {
  border-color: #C62828;
  box-shadow: 0 0 0 3px rgba(198,40,40,0.10);
}
```

---

### Panier — Summary card

```css
.cart-summary-header {
  background: linear-gradient(135deg, #3E2723, #4E342E);
  color: #fff;
  border-radius: 12px 12px 0 0;
}
.cart-total-line {
  color: #C62828;
  font-weight: 800;
}
```

---

### Slider principal (Accueil)

```css
.sl-overlay {
  background: linear-gradient(
    to right,
    rgba(30, 10, 5, 0.80),
    rgba(30, 10, 5, 0.30)
  );
}
/* Titre hero */
.sl-title {
  font-family: 'Playfair Display', serif;
  font-size: 52px;
  font-weight: 800;
  letter-spacing: -0.5px;
  color: #fff;
}
.sl-subtitle {
  color: rgba(255,248,240,0.80);
}
/* CTA hero */
.sl-btn-cta {
  background: linear-gradient(135deg, #C62828, #EF5350);
  color: #fff;
  border-radius: 10px;
  font-weight: 700;
  letter-spacing: 1.2px;
}
.sl-btn-cta:hover {
  box-shadow: 0 8px 25px rgba(198,40,40,0.45);
  transform: translateY(-2px);
}
/* Contrôles slider */
.sl-arrow {
  background: rgba(255,248,240,0.15);
  backdrop-filter: blur(6px);
  color: #fff;
}
.sl-arrow:hover { background: #C62828; }
.sl-dot { background: rgba(255,248,240,0.40); }
.sl-dot.active { background: #C62828; transform: scale(1.3); }
```

---

### Section Collections (Accueil)

```css
.hs-collection-card {
  border-radius: 18px;
  overflow: hidden;
}
.hs-collection-label {
  font-family: 'Playfair Display', serif;
  font-weight: 700;
  color: #fff;
  text-shadow: 0 2px 8px rgba(30,10,5,0.5);
}
.hs-collection-overlay {
  background: linear-gradient(to top, rgba(30,10,5,0.65), transparent);
}
```

---

### Emails transactionnels (`emails/`)

Remplacer `#e63946` par `#C62828` dans tous les fichiers `emails/`.

```
Header email  → background: #C62828
Liens email   → color: #C62828
CTA button    → background: #C62828, border-radius: 8px
Footer email  → background: #FFF8F0, border-top: 1px solid #EDD9C0
```

---

### Toasts & Notifications JS

```css
.toast-success { background: #2E7D32; }
.toast-error   { background: #B71C1C; }
.toast-warning { background: #F9A825; color: #3E2723; }
.toast-info    { background: #0277BD; }
```

---

## Textes de marque — REMPLACER partout

| Ancienne valeur | Nouvelle valeur |
|----------------|-----------------|
| `MatStore Haiti` | `Hayiti's` |
| `matstore` | `hayitis` |
| `Votre partenaire de confiance pour les matériaux de construction` | `Fait avec amour, livré chez vous.` |
| `Matériaux de construction` | `Pâtisserie & Alimentation fine` |
| `info@matstorehaiti.online` | *(laisser comme variable à configurer)* |
| `matstorehaiti.online` | *(laisser comme variable à configurer)* |
| Favicon / meta `og:site_name` | `Hayiti's` |

---

## Préfixes CSS — NE PAS CHANGER

Conserver tous les préfixes existants (`hd-`, `pc-`, `ft-`, `ck-`, `auth-`, `ds-`, `wl-`, `sl-`, `hs-`, `plc-`).  
Ce sont des conventions internes qui n'affectent pas le front-end utilisateur.

---

## Sections spécifiques à ajouter / modifier

### 1. Accueil — Ajouter une section "Nos spécialités"

Après la section Collections, ajouter une **section de mise en avant des catégories alimentaires** :

```html
<!-- Section spécialités — style Hayiti's -->
<section class="hs-specialties py-5" style="background: #FDF6EC;">
  <div class="container">
    <h2 class="text-center mb-4" style="font-family:'Playfair Display',serif; color:#3E2723;">
      Nos Spécialités
    </h2>
    <div class="row g-3 justify-content-center">
      <!-- Répéter pour chaque catégorie : Gâteaux, Pizza, Fromage, Bacon, etc. -->
      <div class="col-6 col-md-3">
        <a href="{% url 'shop:shop_list' %}?category=gateaux" class="hs-spec-card d-block text-center text-decoration-none">
          <div class="hs-spec-icon mb-2">🎂</div>
          <span class="hs-spec-label">Gâteaux</span>
        </a>
      </div>
      <!-- ... autres catégories ... -->
    </div>
  </div>
</section>
```

```css
.hs-spec-card {
  background: #fff;
  border: 1.5px solid #EDD9C0;
  border-radius: 16px;
  padding: 20px 12px;
  transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
}
.hs-spec-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(198,40,40,0.12);
  border-color: #C62828;
}
.hs-spec-icon { font-size: 36px; }
.hs-spec-label {
  font-family: 'Playfair Display', serif;
  font-size: 14px;
  font-weight: 600;
  color: #3E2723;
}
```

### 2. Page produit — Champ "Ingrédients / Composition"

Sur `shop/product_detail.html`, dans les **Tabs**, renommer :
- `Spécifications` → `Ingrédients`
- `Description` → `À propos`

### 3. Logo text dans la navbar

Remplacer le logo texte par :

```html
<a href="{% url 'shop:index' %}" class="hd-logo">
  <span class="hd-logo-icon">🍰</span>
  <span class="hd-logo-name">Hayiti's</span>
</a>
```

```css
.hd-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
}
.hd-logo-icon {
  font-size: 28px;
  line-height: 1;
}
.hd-logo-name {
  font-family: 'Playfair Display', serif;
  font-size: 22px;
  font-weight: 800;
  color: #3E2723;
  letter-spacing: -0.3px;
}
```

---

## Fichiers à modifier — liste exhaustive

```
templates/
├── base.html                          ✅ couleurs, fonts, logo, meta
├── base_checkout.html                 ✅ couleurs, topbar
├── partials/
│   ├── header.html                    ✅ topbar, navbar, mega-menu, account dropdown
│   └── footer.html                    ✅ fond, couleurs, brand name
├── shop/
│   ├── index.html                     ✅ slider, sections, spécialités
│   ├── shop_list.html                 ✅ sidebar, toolbar
│   ├── product_detail.html            ✅ tabs renommés, couleurs
│   ├── cart.html                      ✅ summary card
│   ├── checkout.html                  ✅ steps, guide banner, form
│   ├── wishlist.html                  ✅ couleurs cards
│   └── compare.html                   ✅ tableau
├── accounts/
│   ├── signin.html                    ✅ brand panel, form box
│   └── signup.html                    ✅ brand panel, form box
├── dashboard/
│   ├── base_dashboard.html            ✅ variables CSS, sidebar, topbar
│   ├── overview.html                  ✅ stat cards
│   ├── orders.html                    ✅ badges statut
│   ├── order_detail.html              ✅ couleurs
│   ├── addresses.html                 ✅ couleurs cards
│   └── profile.html                   ✅ couleurs rows
└── emails/
    ├── welcome.html                   ✅ accent rouge
    ├── order_confirmation.html        ✅ accent rouge
    ├── order_status_update.html       ✅ accent rouge
    ├── admin_new_order.html           ✅ accent rouge
    ├── offline_order.html             ✅ accent rouge
    └── proof_submitted.html           ✅ accent rouge
```

---

## README à mettre à jour

Modifier `README.md` :
- Titre : **Hayiti's — Boutique en ligne**
- Description : *Plateforme e-commerce pour la vente de pâtisseries et produits alimentaires fins en Haïti.*
- Supprimer toutes références aux matériaux de construction
- Conserver toute la documentation technique (stack, API, déploiement)

---

## Contraintes importantes

1. **Ne pas modifier** les fichiers Python (modèles, vues, serializers, services).
2. **Ne pas modifier** les URLs, les noms de templates ni la structure des blocs Django (`{% block %}`, `{% extends %}`).
3. **Ne pas supprimer** Bootstrap 5 — il reste la grille de base ; seuls les overrides CSS changent.
4. **Conserver** toutes les librairies d'icônes (`ti-`, `ion-`, `linearicons-`, `fa-`).
5. **Ne pas toucher** aux fichiers `static/js/` sauf pour remplacer les couleurs hardcodées dans les fonctions JS qui génèrent du CSS inline (vérifier les toasts dans `base.html`).
6. Pour chaque fichier modifié, **faire une passe globale** de recherche/remplacement sur toutes les valeurs hex listées dans la table de correspondance.

---

*Prompt préparé le 2026-04-10 — Projet Hayiti's (fork de MatStore Haiti)*
