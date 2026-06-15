"""Indicateur « en train d'écrire » — état éphémère stocké dans le cache (Redis en prod).

Pas de WebSocket : le client envoie un ping pendant la frappe, et l'état est lu dans
la réponse du feed (polling). Les entrées expirent automatiquement (TTL).
"""
import time

from django.core.cache import cache

TYPING_TTL = 6  # secondes : une frappe est « active » pendant 6 s après le dernier ping


def _key(kind, oid):
    return f"cmty_typing_{kind}_{oid}"


def set_typing(kind, oid, user_id, name, is_admin=False):
    """Marque l'utilisateur comme en train d'écrire dans (kind, oid)."""
    key = _key(kind, oid)
    now = time.time()
    d = cache.get(key) or {}
    d[str(user_id)] = {"name": name, "ts": now, "is_admin": is_admin}
    d = {k: v for k, v in d.items() if now - v["ts"] < TYPING_TTL}  # purge
    cache.set(key, d, TYPING_TTL + 4)


def get_typing(kind, oid, exclude_user_id=None):
    """Liste des personnes en train d'écrire (plus récente d'abord), hors `exclude_user_id`."""
    d = cache.get(_key(kind, oid)) or {}
    now = time.time()
    entries = [
        v for k, v in d.items()
        if (now - v["ts"] < TYPING_TTL) and str(k) != str(exclude_user_id)
    ]
    entries.sort(key=lambda v: v["ts"], reverse=True)
    return entries


def typing_names(kind, oid, exclude_user_id=None):
    return [e["name"] for e in get_typing(kind, oid, exclude_user_id)]
