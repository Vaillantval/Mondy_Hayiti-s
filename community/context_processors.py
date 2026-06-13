import json

from django.conf import settings


def web_push(request):
    """Expose la config Web Push (Firebase web) aux templates.

    `web_push_enabled` est False tant que toutes les variables Firebase web ne
    sont pas définies → le code de push ne s'initialise pas et ne casse rien.
    """
    enabled = getattr(settings, "FIREBASE_WEB_PUSH_ENABLED", False)
    return {
        "web_push_enabled": enabled,
        "firebase_web_config": json.dumps(getattr(settings, "FIREBASE_WEB_CONFIG", {})) if enabled else "{}",
        "firebase_vapid_key": getattr(settings, "FIREBASE_VAPID_KEY", "") if enabled else "",
    }
