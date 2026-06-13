# init_site.py
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from shop.management.commands.fetch_rates import fetch_rates_for_base
from shop.models.Setting import Setting


def setup_site():
    site, created = Site.objects.update_or_create(
        id=1, defaults={"domain": "hayitis.com", "name": "hayitis"}
    )
    status = "créé" if created else "mis à jour"
    print(f"✓ Site {status}: {site.domain}")


def create_superuser():
    User = get_user_model()
    username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
    if username and password and not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, password=password, email=email)


def seed_community_channels():
    from community.models import Channel

    defaults = [
        {"name": "Général", "emoji": "💬", "description": "Discussions ouvertes de la communauté.", "order": 1},
        {"name": "Nos pâtisseries", "emoji": "🍰", "description": "Partagez vos gâteaux et envies du jour.", "order": 2},
        {"name": "Recettes & astuces", "emoji": "👩‍🍳", "description": "Échangez vos recettes et conseils.", "order": 3},
        {"name": "Promos & nouveautés", "emoji": "🔥", "description": "Annonces de l'équipe Hayiti's.", "order": 4, "write_access": "admins"},
    ]
    created = 0
    for d in defaults:
        _, was_created = Channel.objects.get_or_create(name=d["name"], defaults=d)
        created += int(was_created)
    if created:
        print(f"✓ Communauté : {created} salon(s) par défaut créé(s).")


def fetch_exchange_rates():
    setting = Setting.objects.first()
    base = setting.base_currency if setting else "HTG"
    try:
        count = fetch_rates_for_base(base)
        print(f"✓ Taux de change : {count} taux sauvegardés pour {base}.")
    except Exception as e:
        print(f"✗ Taux de change : erreur — {e}")


if __name__ == "__main__":
    setup_site()
    create_superuser()
    seed_community_channels()
    fetch_exchange_rates()
