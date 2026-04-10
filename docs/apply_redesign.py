"""
Script de refonte MatStore → Hayiti's
Remplace toutes les couleurs, transparences et textes de marque dans les templates HTML.
"""
import os
import re

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")

# ── 1. Remplacement hex couleurs ────────────────────────────────────────────
HEX_REPLACEMENTS = [
    # Accent orange → rouge signature
    ("#ff5722", "#C62828"),
    ("#FF5722", "#C62828"),
    # Accent clair → rouge vif
    ("#ff8a65", "#EF5350"),
    ("#FF8A65", "#EF5350"),
    # Dark navy → espresso
    ("#1a1a2e", "#3E2723"),
    ("#1A1A2E", "#3E2723"),
    # Dark secondary → brun moyen
    ("#2d2d4e", "#4E342E"),
    ("#2D2D4E", "#4E342E"),
    # Dark deep → brun nuit
    ("#16213e", "#33190F"),
    ("#16213E", "#33190F"),
    # Noir footer
    ("#0f0f1a", "#1C0F0A"),
    ("#0F0F1A", "#1C0F0A"),
    # Fond général → crème chaud
    ("#f4f5f7", "#FFF8F0"),
    ("#F4F5F7", "#FFF8F0"),
    # Fond sections → crème clair
    ("#f8f9fa", "#FDF6EC"),
    ("#F8F9FA", "#FDF6EC"),
    # Bordures → beige doré
    ("#e9ecef", "#EDD9C0"),
    ("#E9ECEF", "#EDD9C0"),
    ("#eaecf0", "#EDD9C0"),
    ("#EAECF0", "#EDD9C0"),
    # Texte secondaire → brun texte
    ("#6c757d", "#6D4C41"),
    ("#6C757D", "#6D4C41"),
    # Texte muted → brun clair
    ("#8a94a6", "#A1887F"),
    ("#8A94A6", "#A1887F"),
    # Placeholder → brun pâle
    ("#b0b8c4", "#BCAAA4"),
    ("#B0B8C4", "#BCAAA4"),
    # Succès vert → vert forêt
    ("#22c55e", "#2E7D32"),
    ("#22C55E", "#2E7D32"),
    ("#28a745", "#388E3C"),
    ("#28A745", "#388E3C"),
    # Danger → rouge foncé
    ("#dc3545", "#B71C1C"),
    ("#DC3545", "#B71C1C"),
    # Warning → jaune miel
    ("#e67e22", "#F9A825"),
    ("#E67E22", "#F9A825"),
    # Info → bleu
    ("#17a2b8", "#0277BD"),
    ("#17A2B8", "#0277BD"),
    # Email accent (différent de l'accent boutique)
    ("#e63946", "#C62828"),
    ("#E63946", "#C62828"),
    # Gris très clair adb5bd → laisser (prix barrés) sauf s'il apparaît en bg
    # Noir pur #333 → garder
]

# ── 2. Transparences rgba ───────────────────────────────────────────────────
RGBA_REPLACEMENTS = [
    # Orange accent avec espaces
    ("rgba(255, 87, 34, 0.10)", "rgba(198, 40, 40, 0.10)"),
    ("rgba(255, 87, 34, 0.15)", "rgba(198, 40, 40, 0.15)"),
    ("rgba(255, 87, 34, 0.35)", "rgba(198, 40, 40, 0.35)"),
    ("rgba(255, 87, 34, 0.55)", "rgba(198, 40, 40, 0.55)"),
    ("rgba(255, 87, 34, .12)",  "rgba(198, 40, 40, .12)"),
    ("rgba(255, 87, 34, .07)",  "rgba(198, 40, 40, .07)"),
    # Dark overlay
    ("rgba(10, 10, 20, 0.72)", "rgba(30, 10, 5, 0.72)"),
    # Blanc pur → blanc crème (sans espaces)
    ("rgba(255,255,255,0.08)", "rgba(255,252,245,0.08)"),
    ("rgba(255,255,255,0.07)", "rgba(255,252,245,0.07)"),
    ("rgba(255,255,255,0.06)", "rgba(255,252,245,0.06)"),
    ("rgba(255,255,255,0.05)", "rgba(255,252,245,0.05)"),
    ("rgba(255,255,255,0.04)", "rgba(255,252,245,0.04)"),
    ("rgba(255,255,255,0.10)", "rgba(255,252,245,0.10)"),
    ("rgba(255,255,255,0.12)", "rgba(255,252,245,0.12)"),
    ("rgba(255,255,255,0.15)", "rgba(255,252,245,0.15)"),
    ("rgba(255,255,255,0.09)", "rgba(255,252,245,0.09)"),
    # Blanc pur → blanc crème (avec espaces)
    ("rgba(255, 255, 255, 0.08)", "rgba(255, 252, 245, 0.08)"),
    ("rgba(255, 255, 255, 0.07)", "rgba(255, 252, 245, 0.07)"),
    ("rgba(255, 255, 255, 0.06)", "rgba(255, 252, 245, 0.06)"),
    ("rgba(255, 255, 255, 0.04)", "rgba(255, 252, 245, 0.04)"),
    ("rgba(255, 255, 255, 0.10)", "rgba(255, 252, 245, 0.10)"),
    ("rgba(255, 255, 255, 0.12)", "rgba(255, 252, 245, 0.12)"),
    ("rgba(255, 255, 255, 0.15)", "rgba(255, 252, 245, 0.15)"),
    # Raccourcis .XX
    ("rgba(255,255,255,.07)", "rgba(255,252,245,.07)"),
    ("rgba(255,255,255,.08)", "rgba(255,252,245,.08)"),
    ("rgba(255,255,255,.10)", "rgba(255,252,245,.10)"),
    ("rgba(255,255,255,.12)", "rgba(255,252,245,.12)"),
    ("rgba(255,255,255,.15)", "rgba(255,252,245,.15)"),
    ("rgba(255,255,255,.38)", "rgba(255,252,245,.38)"),
    ("rgba(255,255,255,.45)", "rgba(255,252,245,.45)"),
    ("rgba(255,255,255,.48)", "rgba(255,252,245,.48)"),
    ("rgba(255,255,255,.55)", "rgba(255,252,245,.55)"),
    ("rgba(255,255,255,.58)", "rgba(255,252,245,.58)"),
    ("rgba(255,255,255,.75)", "rgba(255,252,245,.75)"),
    ("rgba(255,255,255,.80)", "rgba(255,252,245,.80)"),
    ("rgba(255,255,255,.82)", "rgba(255,252,245,.82)"),
    ("rgba(255,255,255,.85)", "rgba(255,252,245,.85)"),
    ("rgba(255,255,255,.88)", "rgba(255,252,245,.88)"),
    ("rgba(255,255,255,.92)", "rgba(255,252,245,.92)"),
    # Orange sans espaces (catchall, après les listings explicites)
    ("rgba(255,87,34,0.10)", "rgba(198,40,40,0.10)"),
    ("rgba(255,87,34,0.15)", "rgba(198,40,40,0.15)"),
    ("rgba(255,87,34,0.35)", "rgba(198,40,40,0.35)"),
    ("rgba(255,87,34,0.55)", "rgba(198,40,40,0.55)"),
    ("rgba(255,87,34,.12)",  "rgba(198,40,40,.12)"),
    ("rgba(255,87,34,.07)",  "rgba(198,40,40,.07)"),
    ("rgba(255,87,34,.09)",  "rgba(198,40,40,.09)"),
    ("rgba(255,87,34,.25)",  "rgba(198,40,40,.25)"),
    ("rgba(255,87,34,0.09)", "rgba(198,40,40,0.09)"),
    ("rgba(255,87,34,0.25)", "rgba(198,40,40,0.25)"),
    ("rgba(255,87,34,0.45)", "rgba(198,40,40,0.45)"),
    ("rgba(255,87,34,.45)",  "rgba(198,40,40,.45)"),
    ("rgba(255,87,34,0.20)", "rgba(198,40,40,0.20)"),
    ("rgba(255,87,34,.20)",  "rgba(198,40,40,.20)"),
]

# ── 3. Textes de marque ─────────────────────────────────────────────────────
TEXT_REPLACEMENTS = [
    ("MatStore Haiti",  "Hayiti's"),
    ("MAT-STORE",       "Hayiti's"),
    ("Mat-Store",       "Hayiti's"),
    ("Matstore",        "Hayiti's"),
    ("matstore",        "hayitis"),
    # Slogan
    ("Votre partenaire de confiance pour les matériaux de construction", "Fait avec amour, livré chez vous."),
    ("Matériaux de construction", "Pâtisserie & Alimentation fine"),
    # Texte fallback titre
    ("Jstore",          "Hayiti's"),
    # Nom de domaine dans les urls affichés (pas les variables)
    ("matstorehaiti.online", "hayitis.online"),
    # Meta og
    ("MatStore",        "Hayiti's"),
    # Exclusive Products → Nos Meilleures Ventes
    ("Exclusive Products", "Nos Meilleures Ventes"),
]


def process_file(filepath: str) -> bool:
    """Applique tous les remplacements sur un fichier. Retourne True si modifié."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # Hex
    for old, new in HEX_REPLACEMENTS:
        content = content.replace(old, new)

    # Rgba exact
    for old, new in RGBA_REPLACEMENTS:
        content = content.replace(old, new)

    # Regex catchall pour rgba(255, 87, 34, ...) restants
    content = re.sub(
        r"rgba\(\s*255\s*,\s*87\s*,\s*34\s*,\s*([^)]+)\)",
        lambda m: f"rgba(198, 40, 40, {m.group(1).strip()})",
        content,
    )

    # Textes
    for old, new in TEXT_REPLACEMENTS:
        content = content.replace(old, new)

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    modified = []
    unchanged = []

    for root, _, files in os.walk(TEMPLATES_DIR):
        for fname in files:
            if fname.endswith(".html"):
                path = os.path.join(root, fname)
                if process_file(path):
                    modified.append(path.replace(TEMPLATES_DIR, "templates"))
                else:
                    unchanged.append(fname)

    print(f"\n✅ Modifiés ({len(modified)}) :")
    for p in sorted(modified):
        print(f"  {p}")

    print(f"\n── Non modifiés ({len(unchanged)}) : {', '.join(unchanged)}")


if __name__ == "__main__":
    main()
