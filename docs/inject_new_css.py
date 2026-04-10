"""
Hayiti's — Injection du nouveau CSS dans les templates.
Remplace les blocs <style> du header, footer, product_card, base.html.
"""
import os

BASE = os.path.dirname(os.path.dirname(__file__))
TPL  = os.path.join(BASE, "templates")

# ─────────────────────────────────────────────────────────────
# 1. HEADER CSS  (remplace lignes 2-845 de partials/header.html)
# ─────────────────────────────────────────────────────────────
HEADER_CSS = """\
<style>
/* =============================================================
   HEADER — Hayiti's | Patisserie Premium
   ============================================================= */

/* Reset overflow */
.header_wrap, .bottom_header, .bottom_header .navbar,
.bottom_header .navbar > .container { overflow: visible !important; }

/* ─── TOP BAR ─────────────────────────────────────────────── */
.hd-topbar {
    background: #3E2723;
    color: rgba(255,252,245,.72);
    font-size: 12.5px;
    font-family: 'Nunito', sans-serif;
    padding: 7px 0;
    border-bottom: 1px solid rgba(255,252,245,.08);
}
.hd-topbar a { color: rgba(255,252,245,.68); text-decoration: none; transition: color .2s; }
.hd-topbar a:hover { color: #EF5350; }

.hd-topbar-left  { display: flex; align-items: center; gap: 20px; }
.hd-topbar-right { display: flex; align-items: center; justify-content: flex-end; gap: 4px; }

.hd-tb-pill {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 12px; border-radius: 20px;
    font-size: 12.5px; font-weight: 600; font-family: 'Nunito', sans-serif;
    color: rgba(255,252,245,.68);
    transition: background .18s, color .18s;
    position: relative; white-space: nowrap;
}
.hd-tb-pill i { font-size: 13px; }
.hd-tb-pill:hover        { background: rgba(255,252,245,.09); color: #EF5350 !important; }
.hd-tb-pill.active-pill  { background: rgba(198,40,40,.20);   color: #EF5350 !important; }

.hd-tb-badge {
    position: absolute; top: -3px; right: -3px;
    width: 15px; height: 15px;
    background: #C62828; color: #fff;
    border-radius: 50%; font-size: 8px; font-weight: 800;
    display: flex; align-items: center; justify-content: center;
    border: 1.5px solid #3E2723; line-height: 1;
}
.hd-tb-sep {
    width: 1px; height: 12px;
    background: rgba(255,252,245,.12);
    margin: 0 2px; flex-shrink: 0;
}

/* ─── APP BANNER ──────────────────────────────────────────── */
#app-banner {
    background: linear-gradient(90deg, #C62828 0%, #8E0000 100%);
    color: #fff; font-family: 'Nunito', sans-serif;
    font-size: 13px; font-weight: 600;
    padding: 8px 0; text-align: center; letter-spacing: .2px;
}
#app-banner a       { color: #FFD54F; text-decoration: underline; margin-left: 12px; font-weight: 700; }
#app-banner button  { background: none; border: none; color: rgba(255,255,255,.7); font-size: 16px; cursor: pointer; margin-left: 16px; line-height: 1; padding: 0; }

/* ─── NAVBAR PRINCIPALE ───────────────────────────────────── */
.hd-navbar-wrap {
    background: #FFFDF8;
    border-bottom: 1.5px solid #EDD9C0;
    box-shadow: 0 2px 20px rgba(62,39,35,.07);
    position: relative;
}
.hd-navbar-wrap .navbar {
    padding: 0; min-height: 70px; align-items: center;
}

/* Logo */
.navbar-brand {
    padding: 8px 0; margin-right: 28px; position: relative; z-index: 2;
    transition: opacity .2s;
}
.navbar-brand:hover             { opacity: .85; box-shadow: none !important; }
.navbar-brand img               { max-height: 58px !important; width: auto; display: block; }
.brand-text {
    font-family: 'Playfair Display', serif !important;
    font-size: 22px !important; font-weight: 800 !important;
    color: #3E2723 !important; letter-spacing: -.5px;
    display: flex; align-items: center; gap: 10px; line-height: 1;
}
.brand-text span { font-size: 28px !important; line-height: 1; }

/* Nav links */
.navbar-nav .nav-link,
.navbar-nav .nav-item > a {
    font-family: 'Nunito', sans-serif;
    font-size: 14px; font-weight: 700;
    color: #3E2723; padding: 22px 15px;
    text-transform: none !important; letter-spacing: .1px;
    position: relative; transition: color .2s;
}
.navbar-nav .nav-link::after {
    content: '';
    position: absolute; bottom: 14px; left: 15px; right: 15px;
    height: 2px; background: #C62828;
    transform: scaleX(0); transition: transform .25s ease; border-radius: 2px;
}
.navbar-nav .nav-link:hover,
.navbar-nav .nav-item > a:hover          { color: #C62828; }
.navbar-nav .nav-link:hover::after       { transform: scaleX(1); }
.navbar-nav .nav-item .dropdown-toggle::after { margin-left: 5px; }

/* Attr nav (search / account / cart icons) */
.attr-nav > ul > li > a {
    font-size: 19px; color: #3E2723;
    padding: 22px 12px; transition: color .2s;
}
.attr-nav > ul > li > a:hover { color: #C62828; }

.cart_count {
    position: absolute; top: 10px; right: 2px;
    width: 17px; height: 17px;
    background: #C62828; color: #fff; border-radius: 50%;
    font-size: 9px; font-weight: 800; font-family: 'Nunito', sans-serif;
    display: flex; align-items: center; justify-content: center;
}

/* ─── SEARCH ──────────────────────────────────────────────── */
.search_wrap {
    background: #FFFDF8; border-bottom: 1.5px solid #EDD9C0; padding: 14px 0;
}
.search_wrap .form-control {
    border: 1.5px solid #EDD9C0; border-radius: 30px;
    padding: 10px 48px 10px 22px;
    font-family: 'Nunito', sans-serif; font-size: 14px;
    background: #fff; color: #3E2723;
}
.search_wrap .form-control:focus {
    border-color: #C62828; box-shadow: 0 0 0 3px rgba(198,40,40,.10); outline: none;
}
.search_wrap .form-control::placeholder { color: #BCAAA4; }
.search_icon { color: #C62828; }

/* ─── DROPDOWN PRINCIPAL ──────────────────────────────────── */
.dropdown-menu {
    background: #FFFDF8; border: 1px solid #EDD9C0;
    border-radius: 14px; box-shadow: 0 8px 40px rgba(62,39,35,.12);
    padding: 10px 0; min-width: 210px;
}
.dropdown-item, .dropdown-menu .nav-link {
    font-family: 'Nunito', sans-serif;
    font-size: 13.5px; font-weight: 600; color: #3E2723;
    padding: 9px 20px; display: flex; align-items: center; gap: 10px;
    transition: background .15s, color .15s;
}
.dropdown-item:hover, .dropdown-menu .nav-link:hover {
    background: rgba(198,40,40,.06); color: #C62828;
}
.dropdown-item i, .dropdown-menu .nav-link i {
    font-size: 13px; width: 16px; text-align: center; color: #A1887F;
}

/* ─── MEGA MENU ───────────────────────────────────────────── */
.dropdown-mega-menu > .dropdown-menu {
    width: 860px; max-width: 95vw;
    padding: 0; border-radius: 18px; overflow: hidden;
}
.dropdown-mega-menu > .dropdown-menu > div { display: flex; flex-direction: column; }
.dropdown-mega-menu > .dropdown-menu > div > div:first-child { display: flex; }

/* Sidebar */
.mega-sidebar {
    width: 210px; flex-shrink: 0;
    background: linear-gradient(180deg, #3E2723 0%, #4E342E 100%);
    padding: 24px 0 18px; display: flex; flex-direction: column;
}
.mega-sidebar-title {
    font-family: 'Nunito', sans-serif; font-size: 9px; font-weight: 800;
    text-transform: uppercase; letter-spacing: 1.8px;
    color: rgba(255,252,245,.30); padding: 0 20px 10px;
}
.mega-sidebar-link {
    display: flex; align-items: center; gap: 10px;
    padding: 10px 20px; font-family: 'Nunito', sans-serif;
    font-size: 13px; font-weight: 600;
    color: rgba(255,252,245,.62); text-decoration: none;
    transition: background .15s, color .15s, border-left-color .15s;
    border-left: 3px solid transparent;
}
.mega-sidebar-link i { font-size: 13px; width: 16px; text-align: center; }
.mega-sidebar-link:hover {
    background: rgba(198,40,40,.20); color: #EF5350; border-left-color: #C62828;
}
.mega-sidebar-bottom {
    margin-top: auto; padding: 14px 16px 0;
    border-top: 1px solid rgba(255,252,245,.08);
}
.mega-sidebar-btn {
    display: flex; align-items: center; justify-content: center; gap: 8px;
    padding: 9px 14px; background: #C62828; color: #fff;
    border-radius: 8px; font-family: 'Nunito', sans-serif;
    font-size: 12.5px; font-weight: 700; text-decoration: none;
    transition: background .18s;
}
.mega-sidebar-btn:hover { background: #8E0000; color: #fff; }

/* Body mega */
.mega-body { flex: 1; padding: 22px 24px; background: #FFFDF8; }
.mega-body-header {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 18px; padding-bottom: 12px; border-bottom: 1px solid #EDD9C0;
}
.mega-body-title {
    font-family: 'Playfair Display', serif; font-size: 15px; font-weight: 700; color: #3E2723;
}
.mega-body-viewall {
    font-family: 'Nunito', sans-serif; font-size: 12px; font-weight: 700; color: #C62828;
    text-decoration: none; display: flex; align-items: center; gap: 4px; transition: gap .15s;
}
.mega-body-viewall:hover { gap: 7px; }

.mega-cats-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 16px 24px; }
.mega-cat-group { display: flex; flex-direction: column; gap: 4px; }
.mega-cat-header {
    display: flex; align-items: center; gap: 7px;
    font-family: 'Nunito', sans-serif; font-size: 12.5px; font-weight: 800;
    color: #3E2723; text-decoration: none; margin-bottom: 4px; transition: color .15s;
}
.mega-cat-header:hover { color: #C62828; }
.mega-cat-dot { width: 6px; height: 6px; border-radius: 50%; background: #C62828; flex-shrink: 0; }
.mega-cat-items { list-style: none; padding: 0; margin: 0; }
.mega-cat-items li a {
    font-family: 'Nunito', sans-serif; font-size: 12.5px; color: #6D4C41;
    text-decoration: none; display: block; padding: 2px 0 2px 13px;
    border-left: 2px solid transparent;
    transition: color .15s, padding-left .15s, border-left-color .15s;
}
.mega-cat-items li a:hover { color: #C62828; padding-left: 17px; border-left-color: #C62828; }

/* Fallback grille (sans catégories) */
.mega-fallback-grid { display: flex; flex-wrap: wrap; gap: 10px; }
.mega-fallback-item {
    display: inline-flex; align-items: center; gap: 7px;
    padding: 8px 14px; border: 1px solid #EDD9C0; border-radius: 8px;
    font-family: 'Nunito', sans-serif; font-size: 13px; font-weight: 600;
    color: #3E2723; text-decoration: none; transition: border-color .15s, color .15s;
}
.mega-fallback-item:hover { border-color: #C62828; color: #C62828; }

/* Footer mega */
.mega-footer {
    border-top: 1px solid #EDD9C0; padding: 16px 24px 20px; background: #FDF6EC;
}
.mega-footer-title {
    font-family: 'Nunito', sans-serif; font-size: 9px; font-weight: 800;
    text-transform: uppercase; letter-spacing: 1.8px; color: #A1887F; margin-bottom: 12px;
}
.mega-footer-banners { display: flex; gap: 12px; }
.mega-footer-banner {
    flex: 1; position: relative; border-radius: 10px; overflow: hidden;
    height: 62px; display: block; text-decoration: none;
}
.mega-footer-banner img {
    width: 100%; height: 100%; object-fit: cover;
    filter: brightness(.80); transition: filter .3s;
}
.mega-footer-banner:hover img { filter: brightness(.65); }
.mega-footer-banner-overlay {
    position: absolute; inset: 0;
    background: linear-gradient(to top, rgba(30,10,5,.68), transparent);
    padding: 8px 12px; display: flex; flex-direction: column; justify-content: flex-end;
}
.mega-footer-banner-overlay h4 {
    font-family: 'Playfair Display', serif;
    font-size: 13px; font-weight: 700; color: #fff; margin: 0;
}
.mega-footer-banner-overlay h6 {
    font-family: 'Nunito', sans-serif;
    font-size: 10px; color: rgba(255,252,245,.72); margin: 0 0 2px;
}

/* ─── ACCOUNT DROPDOWN ────────────────────────────────────── */
.hd-account-wrap { position: relative; }
.hd-account-trigger {
    display: flex; align-items: center; gap: 8px;
    cursor: pointer; padding: 22px 12px;
    font-family: 'Nunito', sans-serif; font-size: 13.5px; font-weight: 700;
    color: #3E2723; text-decoration: none; transition: color .2s;
}
.hd-account-trigger:hover { color: #C62828; }
.hd-account-trigger > i { font-size: 10px; }
.hd-account-avatar {
    width: 30px; height: 30px; border-radius: 50%;
    background: linear-gradient(135deg, #C62828, #EF5350);
    color: #fff; font-size: 13px; font-weight: 800; font-family: 'Nunito', sans-serif;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}

.hd-account-dropdown {
    position: absolute; top: calc(100% + 4px); right: 0;
    width: 242px; background: #FFFDF8;
    border: 1px solid #EDD9C0; border-radius: 16px;
    box-shadow: 0 8px 40px rgba(62,39,35,.14);
    opacity: 0; visibility: hidden; transform: translateY(8px);
    transition: opacity .22s, visibility .22s, transform .22s;
    z-index: 9999; overflow: hidden;
}
.hd-account-wrap:hover .hd-account-dropdown {
    opacity: 1; visibility: visible; transform: translateY(0);
}

.hd-account-head {
    background: linear-gradient(135deg, #3E2723, #4E342E);
    padding: 16px 18px; display: flex; align-items: center; gap: 12px;
}
.hd-account-head-avatar {
    width: 38px; height: 38px; border-radius: 50%;
    background: linear-gradient(135deg, #C62828, #EF5350);
    color: #fff; font-size: 16px; font-weight: 800; font-family: 'Nunito', sans-serif;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.hd-account-head-name  { font-family: 'Nunito', sans-serif; font-size: 13.5px; font-weight: 700; color: #fff; }
.hd-account-head-label { font-family: 'Nunito', sans-serif; font-size: 11px; color: rgba(255,252,245,.48); margin-top: 2px; }

.hd-account-menu { list-style: none; padding: 8px 0; margin: 0; }
.hd-account-menu li a {
    display: flex; align-items: center; gap: 10px;
    padding: 9px 18px; font-family: 'Nunito', sans-serif;
    font-size: 13px; font-weight: 600; color: #3E2723;
    text-decoration: none; transition: background .15s, color .15s;
}
.hd-account-menu li a i { font-size: 13px; width: 14px; text-align: center; color: #A1887F; }
.hd-account-menu li a:hover { background: rgba(198,40,40,.06); color: #C62828; }
.hd-account-menu li a:hover i { color: #C62828; }
.hd-menu-divider { height: 1px; background: #EDD9C0; margin: 6px 0; }
.hd-menu-logout a   { color: #B71C1C !important; }
.hd-menu-logout a i { color: #B71C1C !important; }

/* ─── CART PREVIEW ────────────────────────────────────────── */
.hd-cart-wrap { position: relative; }
.hd-cart-trigger {
    position: relative; display: flex; align-items: center;
    padding: 22px 12px; color: #3E2723; font-size: 19px;
    text-decoration: none; transition: color .2s;
}
.hd-cart-trigger:hover { color: #C62828; }

.hd-cart-preview {
    position: absolute; top: calc(100% + 4px); right: 0;
    width: 302px; background: #FFFDF8;
    border: 1px solid #EDD9C0; border-radius: 16px;
    box-shadow: 0 8px 40px rgba(62,39,35,.14);
    opacity: 0; visibility: hidden; transform: translateY(8px);
    transition: opacity .22s, visibility .22s, transform .22s;
    z-index: 9999; overflow: hidden;
}
.hd-cart-wrap:hover .hd-cart-preview { opacity: 1; visibility: visible; transform: translateY(0); }

.hd-cart-preview-inner { display: flex; flex-direction: column; }
.hd-cp-head {
    display: flex; align-items: center; justify-content: space-between;
    padding: 13px 18px; border-bottom: 1px solid #EDD9C0; background: #FDF6EC;
}
.hd-cp-title {
    font-family: 'Nunito', sans-serif; font-size: 13px; font-weight: 800; color: #3E2723;
    display: flex; align-items: center; gap: 7px;
}
.hd-cp-title i { color: #C62828; }
.hd-cp-badge {
    background: rgba(198,40,40,.10); color: #C62828;
    font-family: 'Nunito', sans-serif; font-size: 11px; font-weight: 700;
    padding: 2px 8px; border-radius: 20px;
}
.hd-cp-list {
    list-style: none; padding: 0; margin: 0;
    max-height: 240px; overflow-y: auto;
    scrollbar-width: thin; scrollbar-color: #EDD9C0 transparent;
}
.hd-cp-item {
    display: flex; align-items: center; gap: 12px;
    padding: 10px 18px; border-bottom: 1px solid rgba(237,217,192,.4);
    transition: background .15s;
}
.hd-cp-item:hover { background: #FDF6EC; }
.hd-cp-img-wrap {
    width: 50px; height: 50px; border-radius: 10px;
    overflow: hidden; flex-shrink: 0; border: 1px solid #EDD9C0; background: #FDF6EC;
}
.hd-cp-img-wrap img         { width: 100%; height: 100%; object-fit: cover; }
.hd-cp-img-placeholder      { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; color: #EDD9C0; font-size: 18px; }
.hd-cp-info                 { flex: 1; min-width: 0; }
.hd-cp-name {
    font-family: 'Nunito', sans-serif; font-size: 12.5px; font-weight: 700; color: #3E2723;
    text-decoration: none; display: block;
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.hd-cp-name:hover           { color: #C62828; }
.hd-cp-qty                  { font-family: 'Nunito', sans-serif; font-size: 11.5px; color: #A1887F; margin-top: 2px; display: block; }
.hd-cp-qty strong           { color: #C62828; }
.hd-cp-remove {
    width: 24px; height: 24px; border-radius: 6px;
    border: 1px solid #EDD9C0; background: transparent;
    display: flex; align-items: center; justify-content: center;
    color: #A1887F; font-size: 14px; cursor: pointer; flex-shrink: 0; padding: 0;
    transition: background .15s, color .15s, border-color .15s;
}
.hd-cp-remove:hover { background: rgba(183,28,28,.08); color: #B71C1C; border-color: #B71C1C; }

.hd-cp-foot {
    padding: 13px 18px; border-top: 1px solid #EDD9C0; background: #FDF6EC;
}
.hd-cp-subtotal {
    display: flex; align-items: center; justify-content: space-between;
    font-family: 'Nunito', sans-serif; font-size: 13px; margin-bottom: 12px;
}
.hd-cp-subtotal span    { color: #A1887F; font-weight: 600; }
.hd-cp-subtotal strong  { color: #3E2723; font-size: 15px; font-weight: 800; }
.hd-cp-btn-cart {
    display: flex; align-items: center; justify-content: center; gap: 7px;
    width: 100%; padding: 9px; border: 1.5px solid #EDD9C0; border-radius: 8px;
    background: transparent; color: #3E2723;
    font-family: 'Nunito', sans-serif; font-size: 13px; font-weight: 700;
    text-decoration: none; margin-bottom: 8px;
    transition: border-color .18s, color .18s;
}
.hd-cp-btn-cart:hover { border-color: #C62828; color: #C62828; }
.hd-cp-btn-checkout {
    display: flex; align-items: center; justify-content: center; gap: 7px;
    width: 100%; padding: 10px;
    background: linear-gradient(135deg, #C62828, #EF5350);
    border-radius: 8px; color: #fff;
    font-family: 'Nunito', sans-serif; font-size: 13px; font-weight: 700;
    text-decoration: none; transition: opacity .18s, box-shadow .18s;
}
.hd-cp-btn-checkout:hover { color: #fff; opacity: .92; box-shadow: 0 4px 16px rgba(198,40,40,.30); }

.hd-cp-empty { padding: 28px 18px; text-align: center; }
.hd-cp-empty-icon { font-size: 36px; color: #EDD9C0; display: block; margin-bottom: 10px; }
.hd-cp-empty p { font-family: 'Nunito', sans-serif; font-size: 13px; color: #A1887F; margin-bottom: 14px; }

/* ─── MOBILE NAV ──────────────────────────────────────────── */
.hd-mobile-icons { display: none; align-items: center; gap: 4px; }
.hd-mobile-icons .nav-link { position: relative; padding: 8px !important; font-size: 20px; color: #3E2723; }
.hd-mobile-nav-section { display: none; }

.hd-mobile-nav-link {
    display: flex; align-items: center; gap: 10px;
    padding: 11px 0; font-family: 'Nunito', sans-serif;
    font-size: 14px; font-weight: 600; color: #3E2723;
    text-decoration: none; border-bottom: 1px solid #EDD9C0; transition: color .15s;
}
.hd-mobile-nav-link i    { font-size: 14px; width: 16px; text-align: center; color: #A1887F; }
.hd-mobile-nav-link:hover { color: #C62828; }
.hd-mobile-nav-link span { margin-left: auto; background: #C62828; color: #fff; font-size: 10px; font-weight: 800; padding: 1px 6px; border-radius: 10px; }
.hd-mobile-nav-link.logout { color: #B71C1C; border-bottom: none; }
.hd-mobile-nav-link.logout i { color: #B71C1C; }

/* ─── RESPONSIVE ──────────────────────────────────────────── */
@media (max-width: 991px) {
    .hd-topbar { display: none; }
    .navbar-brand { position: static !important; margin-right: 0; }
    .hd-mobile-icons { display: flex; }
    .hd-mobile-nav-section {
        display: flex; flex-direction: column;
        padding: 12px 0; margin-top: 8px;
        border-top: 1px solid #EDD9C0;
    }
    .navbar-nav .nav-link { padding: 10px 0; border-bottom: 1px solid #EDD9C0; }
    .navbar-nav .nav-link::after { display: none; }
    .hd-account-wrap { display: none; }
    .hd-cart-wrap .hd-cart-preview { display: none; }
    .attr-nav { display: none; }
}
@media (max-width: 480px) {
    .brand-text       { font-size: 20px !important; }
    .brand-text span  { font-size: 24px !important; }
}
</style>
"""

# ─────────────────────────────────────────────────────────────
# 2. FOOTER CSS  (remplace lignes 171+ de partials/footer.html)
# ─────────────────────────────────────────────────────────────
FOOTER_CSS = """\

<style>
/* =============================================================
   FOOTER — Hayiti's | Patisserie Premium
   ============================================================= */

/* ─── Wrapper ─────────────────────────────────────────────── */
.site-footer {
    background: #1C0F0A;
    color: rgba(255,248,240,.58);
    font-family: 'Nunito', sans-serif;
    font-size: 13.5px; line-height: 1.65;
}

/* ─── Newsletter bar ──────────────────────────────────────── */
.ft-nl-bar {
    background: rgba(255,248,240,.04);
    border-bottom: 1px solid rgba(255,248,240,.07);
    padding: 16px 0;
}
.ft-nl-bar-inner {
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 14px;
}
.ft-nl-bar-text {
    display: flex; align-items: center; gap: 10px;
    font-size: 13.5px; font-weight: 700; color: rgba(255,248,240,.82);
}
.ft-nl-bar-ico  { font-size: 15px; color: #C62828; }
.ft-nl-bar-muted { font-weight: 400; color: rgba(255,248,240,.45); font-size: 13px; }
.ft-nl-bar-form  { display: flex; align-items: center; gap: 8px; }
.ft-nl-bar-field { position: relative; }
.ft-nl-bar-field-ico {
    position: absolute; left: 11px; top: 50%; transform: translateY(-50%);
    color: rgba(255,248,240,.35); font-size: 13px;
}
.ft-nl-bar-input {
    padding: 9px 14px 9px 32px;
    background: rgba(255,248,240,.07);
    border: 1px solid rgba(255,248,240,.12);
    border-radius: 8px; width: 220px;
    color: rgba(255,248,240,.85); font-family: 'Nunito', sans-serif; font-size: 13px;
    outline: none; transition: border-color .18s, background .18s;
}
.ft-nl-bar-input:focus {
    border-color: rgba(198,40,40,.50); background: rgba(255,248,240,.10);
}
.ft-nl-bar-input::placeholder { color: rgba(255,248,240,.30); }
.ft-nl-bar-btn {
    padding: 9px 18px;
    border: 1px solid rgba(198,40,40,.55);
    background: transparent; color: #EF5350;
    border-radius: 8px; font-family: 'Nunito', sans-serif;
    font-size: 13px; font-weight: 700; cursor: pointer;
    transition: background .18s, color .18s, border-color .18s;
}
.ft-nl-bar-btn:hover { background: #C62828; color: #fff; border-color: #C62828; }

/* ─── Main section ────────────────────────────────────────── */
.ft-main { padding: 52px 0 36px; }

/* Brand */
.ft-brand-link { text-decoration: none; display: inline-flex; align-items: center; gap: 11px; margin-bottom: 14px; }
.ft-brand-logo { display: flex; align-items: center; gap: 11px; }
.ft-brand-icon {
    width: 38px; height: 38px; background: #C62828; border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; color: #fff; flex-shrink: 0;
}
.ft-brand-name {
    font-family: 'Playfair Display', serif;
    font-size: 20px; font-weight: 800; color: #fff;
    letter-spacing: -.3px;
}
.ft-brand-desc { font-size: 13px; color: rgba(255,248,240,.42); max-width: 300px; line-height: 1.7; margin: 12px 0 20px; }

/* Contact list */
.ft-contact-list { list-style: none; padding: 0; margin: 0 0 20px; display: flex; flex-direction: column; gap: 10px; }
.ft-contact-list li {
    display: flex; align-items: flex-start; gap: 10px;
    font-size: 13px; color: rgba(255,248,240,.55);
}
.ft-contact-list li a { color: rgba(255,248,240,.55); text-decoration: none; transition: color .18s; }
.ft-contact-list li a:hover { color: #EF5350; }
.ft-contact-icon {
    width: 28px; height: 28px; flex-shrink: 0;
    background: rgba(255,248,240,.07); border-radius: 7px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; color: #C62828; margin-top: 1px;
}

/* Socials */
.ft-socials { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.ft-social {
    width: 36px; height: 36px; border-radius: 9px;
    background: rgba(255,248,240,.07);
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; color: rgba(255,248,240,.52);
    text-decoration: none; transition: background .18s, color .18s;
}
.ft-social:hover { background: #C62828; color: #fff; }

/* Column titles */
.ft-col-title {
    font-family: 'Playfair Display', serif;
    font-size: 14px; font-weight: 700; color: #fff;
    margin-bottom: 16px; padding-bottom: 8px;
    border-bottom: 2px solid #C62828; display: inline-block;
}

/* Links */
.ft-links { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 6px; }
.ft-links li a {
    font-family: 'Nunito', sans-serif; font-size: 13px;
    color: rgba(255,248,240,.48); text-decoration: none;
    display: flex; align-items: center; gap: 7px;
    transition: color .18s, padding-left .18s;
}
.ft-links li a i { font-size: 9px; color: #C62828; flex-shrink: 0; }
.ft-links li a:hover { color: #EF5350; padding-left: 4px; }

/* Trust badges */
.ft-trust { margin-top: 20px; display: flex; flex-direction: column; gap: 8px; }
.ft-trust-item {
    display: flex; align-items: center; gap: 9px;
    font-family: 'Nunito', sans-serif; font-size: 12.5px;
    color: rgba(255,248,240,.40);
}
.ft-trust-item i { font-size: 14px; color: #C62828; flex-shrink: 0; }

/* ─── Bottom bar ──────────────────────────────────────────── */
.ft-bottom {
    border-top: 1px solid rgba(255,248,240,.07); padding: 18px 0;
}
.ft-bottom-inner {
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 14px;
}
.ft-copyright { font-size: 12.5px; color: rgba(255,248,240,.28); margin: 0; }

.ft-payments { list-style: none; padding: 0; margin: 0; display: flex; align-items: center; gap: 10px; }
.ft-payments li img {
    height: 22px; opacity: .52;
    filter: grayscale(1) brightness(1.8);
    transition: opacity .2s, filter .2s;
}
.ft-payments li img:hover { opacity: 1; filter: none; }

/* ─── Responsive ──────────────────────────────────────────── */
@media (max-width: 768px) {
    .ft-nl-bar-inner { flex-direction: column; text-align: center; }
    .ft-nl-bar-form  { width: 100%; justify-content: center; }
    .ft-nl-bar-input { width: 180px; }
    .ft-bottom-inner { flex-direction: column; text-align: center; }
    .ft-payments { justify-content: center; }
}
</style>
"""

# ─────────────────────────────────────────────────────────────
# 3. PRODUCT CARD CSS OVERRIDES  (injecte dans base.html avant </head>)
# ─────────────────────────────────────────────────────────────
PC_CSS = """\
    <!-- Hayiti's — Product Card Overrides -->
    <style>
    /* =============================================================
       PRODUCT CARD — Hayiti's
       ============================================================= */
    .pc {
        background: #fff;
        border: 1px solid #EDD9C0;
        border-radius: 20px;
        overflow: hidden;
        display: flex; flex-direction: column;
        cursor: pointer;
        transition: transform .22s ease, box-shadow .22s ease, border-color .22s ease;
        width: 100%;
    }
    .pc:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(62,39,35,.13);
        border-color: #C62828;
    }

    /* Image */
    .pc-img {
        position: relative; width: 100%; padding-top: 90%;
        background: #FDF6EC; overflow: hidden; flex-shrink: 0;
    }
    .pc-img > a {
        position: absolute; inset: 0; display: block;
    }
    .pc-img img {
        position: absolute; inset: 0; width: 100%; height: 100%;
        object-fit: cover; transition: transform .5s cubic-bezier(.25,.46,.45,.94);
    }
    .pc:hover .pc-img img { transform: scale(1.07); }

    /* Badges */
    .pc-badges {
        position: absolute; top: 12px; left: 12px;
        display: flex; flex-direction: column; gap: 4px; z-index: 2;
    }
    .pc-badge {
        font-family: 'Nunito', sans-serif;
        font-size: 10px; font-weight: 800; letter-spacing: .4px;
        padding: 4px 10px; border-radius: 20px;
        text-transform: uppercase;
    }
    .pc-new  { background: #2E7D32; color: #fff; }
    .pc-promo{ background: #B71C1C; color: #fff; }
    .pc-hot  { background: #F9A825; color: #3E2723; }

    /* Discount tag */
    .pc-discount-img {
        position: absolute; top: 12px; right: 12px; z-index: 2;
        background: #C62828; color: #fff;
        font-family: 'Nunito', sans-serif; font-size: 11px; font-weight: 800;
        padding: 4px 9px; border-radius: 20px;
    }

    /* Hover overlay */
    .pc-overlay {
        position: absolute; inset: 0; z-index: 3;
        background: rgba(30,10,5,.30);
        display: flex; align-items: center; justify-content: center; gap: 8px;
        opacity: 0; transition: opacity .25s;
    }
    .pc:hover .pc-overlay { opacity: 1; }
    .pc-ov-btn {
        width: 40px; height: 40px; border-radius: 50%;
        background: rgba(255,252,245,.92); color: #3E2723;
        display: flex; align-items: center; justify-content: center;
        font-size: 15px; text-decoration: none;
        transition: background .18s, color .18s;
    }
    .pc-ov-btn:hover { background: #C62828; color: #fff; }

    /* Body */
    .pc-body {
        padding: 16px 18px 18px;
        display: flex; flex-direction: column; flex: 1;
    }

    /* Categories */
    .pc-cats {
        display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 8px;
    }
    .pc-cat {
        font-family: 'Nunito', sans-serif;
        font-size: 10.5px; font-weight: 700; text-transform: uppercase;
        letter-spacing: .5px; color: #A1887F; text-decoration: none;
        padding: 2px 8px; border: 1px solid #EDD9C0; border-radius: 20px;
        transition: color .15s, border-color .15s;
    }
    .pc-cat:hover { color: #C62828; border-color: #C62828; }

    /* Name */
    .pc-name {
        margin: 0 0 5px; font-family: 'Playfair Display', serif;
        font-size: 15px; font-weight: 700; line-height: 1.35;
    }
    .pc-name a { color: #3E2723; text-decoration: none; transition: color .18s; }
    .pc-name a:hover { color: #C62828; }

    /* Description */
    .pc-desc {
        font-family: 'Nunito', sans-serif;
        font-size: 12.5px; color: #A1887F; line-height: 1.5;
        margin: 0 0 10px;
        display: -webkit-box; -webkit-line-clamp: 2;
        -webkit-box-orient: vertical; overflow: hidden;
    }

    /* Stars */
    .pc-stars {
        display: flex; align-items: center; gap: 3px; margin-bottom: 10px;
        font-size: 12px; color: #F9A825;
    }
    .pc-rating { font-family: 'Nunito', sans-serif; font-size: 11.5px; font-weight: 700; color: #3E2723; margin-left: 3px; }
    .pc-brand  { font-family: 'Nunito', sans-serif; font-size: 11.5px; color: #A1887F; }

    /* Price */
    .pc-price-row { display: flex; align-items: baseline; gap: 8px; margin-bottom: 8px; }
    .pc-price-main {
        font-family: 'Playfair Display', serif;
        font-size: 20px; font-weight: 800; color: #C62828;
    }
    .pc-price-old {
        font-family: 'Nunito', sans-serif;
        font-size: 13px; color: #BCAAA4; text-decoration: line-through;
    }

    /* Stock */
    .pc-stock {
        font-family: 'Nunito', sans-serif;
        font-size: 11.5px; font-weight: 700; margin-bottom: 14px;
        display: flex; align-items: center; gap: 5px;
    }
    .pc-in  { color: #2E7D32; }
    .pc-out { color: #B71C1C; }

    /* Actions */
    .pc-actions {
        display: flex; gap: 8px; margin-top: auto;
    }
    .pc-btn-cart {
        flex: 1; display: flex; align-items: center; justify-content: center; gap: 7px;
        padding: 10px 14px;
        background: linear-gradient(135deg, #C62828, #EF5350);
        color: #fff; border-radius: 10px;
        font-family: 'Nunito', sans-serif; font-size: 13px; font-weight: 700;
        text-decoration: none; border: none; cursor: pointer;
        transition: box-shadow .2s, transform .15s, opacity .18s;
    }
    .pc-btn-cart:hover {
        color: #fff;
        box-shadow: 0 6px 20px rgba(198,40,40,.35);
        transform: translateY(-1px);
    }
    .pc-btn-detail {
        display: flex; align-items: center; gap: 5px;
        padding: 10px 14px;
        border: 1.5px solid #EDD9C0; border-radius: 10px;
        color: #6D4C41; background: transparent;
        font-family: 'Nunito', sans-serif; font-size: 13px; font-weight: 700;
        text-decoration: none; white-space: nowrap;
        transition: border-color .18s, color .18s;
    }
    .pc-btn-detail:hover { border-color: #C62828; color: #C62828; }

    /* Grid equal height */
    .shop_container > [class*="col-"] { display: flex; }
    .shop_container .product { display: flex; flex-direction: column; width: 100%; }
    </style>
"""

# ─────────────────────────────────────────────────────────────
# Fonctions d'injection
# ─────────────────────────────────────────────────────────────

def inject_header_css():
    path = os.path.join(TPL, "partials", "header.html")
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Trouve les bornes du bloc <style>
    start = None
    end   = None
    for i, ln in enumerate(lines):
        if ln.strip() == "<style>" and start is None:
            start = i
        if ln.strip() == "</style>" and start is not None:
            end = i
            break

    if start is None or end is None:
        print("header.html: style block not found")
        return

    new_lines = lines[:start] + [HEADER_CSS] + lines[end+1:]
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print("header.html: CSS replaced")


def inject_footer_css():
    path = os.path.join(TPL, "partials", "footer.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Le CSS du footer est APRES </footer> — on coupe la
    cut = content.find("\n<style>", content.find("</footer>"))
    if cut == -1:
        print("footer.html: trailing style block not found")
        return

    new_content = content[:cut] + FOOTER_CSS
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("footer.html: CSS replaced")


def inject_pc_css():
    path = os.path.join(TPL, "base.html")
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    marker = "    {% block styles %}{% endblock %}"
    if marker not in content:
        print("base.html: marker not found")
        return

    new_content = content.replace(marker, PC_CSS + marker)
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("base.html: product card CSS injected")


if __name__ == "__main__":
    inject_header_css()
    inject_footer_css()
    inject_pc_css()
    print("Done.")
