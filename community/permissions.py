"""Logique d'autorisation/modération partagée entre le web et l'API.

Un seul endroit décide qui peut lire/écrire dans un salon, afin que l'interface
web et l'API mobile appliquent exactement les mêmes règles.
"""
from .models import ChannelMute, CommunityBan


def get_active_ban(user):
    """Retourne le bannissement global actif de l'utilisateur, sinon None."""
    if not user or not user.is_authenticated:
        return None
    ban = getattr(user, "community_ban", None)
    if ban and ban.is_active:
        return ban
    return None


def can_read_channel(user, channel):
    """L'utilisateur peut-il lire le salon ?"""
    if not channel.is_active:
        return bool(user and user.is_authenticated and user.is_staff)

    ban = get_active_ban(user)
    if ban and not ban.can_read:
        return False

    if channel.read_access == channel.READ_PUBLIC:
        return True

    if not user or not user.is_authenticated:
        return False

    if channel.read_access == channel.READ_CLOSED:
        return user.is_staff

    # READ_AUTH
    return True


def can_write_channel(user, channel):
    """L'utilisateur peut-il publier dans le salon ?"""
    if not user or not user.is_authenticated:
        return False
    if not can_read_channel(user, channel):
        return False

    # Les admins passent outre le verrouillage et les mutes.
    if user.is_staff:
        return True

    if get_active_ban(user):
        return False

    if channel.write_access in (channel.WRITE_LOCKED, channel.WRITE_ADMINS):
        return False

    if ChannelMute.objects.filter(channel=channel, user=user).exists():
        return False

    return True


def write_block_reason(user, channel):
    """Message expliquant pourquoi l'écriture est bloquée (ou None si autorisée)."""
    if not user or not user.is_authenticated:
        return "Connectez-vous pour participer à la discussion."
    if not can_read_channel(user, channel):
        return "Ce salon ne vous est pas accessible."
    if user.is_staff:
        return None
    if get_active_ban(user):
        return "Vous avez été banni de la communauté."
    if channel.write_access == channel.WRITE_LOCKED:
        return "Ce salon est en lecture seule."
    if channel.write_access == channel.WRITE_ADMINS:
        return "Seuls les administrateurs peuvent écrire dans ce salon."
    if ChannelMute.objects.filter(channel=channel, user=user).exists():
        return "Vous ne pouvez pas écrire dans ce salon."
    return None


def readable_channels(user, queryset):
    """Filtre un queryset de salons sur ceux que l'utilisateur peut lire."""
    return [c for c in queryset if can_read_channel(user, c)]
