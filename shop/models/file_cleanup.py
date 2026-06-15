"""Helper : supprimer les anciens fichiers quand un FileField/ImageField est remplacé.

Django ne supprime jamais l'ancien fichier lors d'un remplacement → ils s'accumulent
sur le volume. À appeler dans `save()` AVANT `super().save()`, puis supprimer le retour
APRÈS (une fois le nouveau fichier bien enregistré).
"""


def collect_replaced_files(instance, model, fields):
    """Retourne la liste des anciens fichiers à supprimer (ceux remplacés ou vidés)."""
    olds = []
    if not instance.pk:
        return olds
    previous = model.objects.filter(pk=instance.pk).first()
    if not previous:
        return olds
    for name in fields:
        old = getattr(previous, name)
        new = getattr(instance, name)
        if old and (not new or old.name != new.name):
            olds.append(old)
    return olds
