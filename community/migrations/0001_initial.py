import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("shop", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Channel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=60)),
                ("slug", models.SlugField(blank=True, max_length=80, unique=True)),
                ("description", models.CharField(blank=True, default="", max_length=160)),
                ("emoji", models.CharField(default="💬", help_text="Émoji affiché à côté du nom du salon.", max_length=8)),
                ("color", models.CharField(default="#C62828", help_text="Couleur d'accent (hex).", max_length=7)),
                ("image", models.ImageField(blank=True, null=True, upload_to="community/channels/%Y/%m/%d/")),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("read_access", models.CharField(choices=[("public", "Public — tout le monde peut lire"), ("authenticated", "Connectés uniquement"), ("closed", "Fermé — admins uniquement")], default="public", max_length=20, verbose_name="Accès en lecture")),
                ("write_access", models.CharField(choices=[("open", "Ouvert — membres connectés"), ("locked", "Verrouillé — lecture seule"), ("admins", "Admins uniquement")], default="open", max_length=20, verbose_name="Accès en écriture")),
                ("notify_admins", models.BooleanField(default=True, help_text="Notifier les admins (push FCM) à chaque nouveau message de membre.")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Salon",
                "verbose_name_plural": "Salons",
                "ordering": ["order", "name"],
            },
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("content", models.TextField(blank=True, default="")),
                ("is_pinned", models.BooleanField(default=False)),
                ("is_deleted", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("author", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="community_messages", to=settings.AUTH_USER_MODEL)),
                ("channel", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="messages", to="community.channel")),
                ("deleted_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to=settings.AUTH_USER_MODEL)),
                ("product", models.ForeignKey(blank=True, help_text="Produit tagué dans le message.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="community_mentions", to="shop.product")),
                ("reply_to", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="replies", to="community.message")),
            ],
            options={
                "verbose_name": "Message",
                "verbose_name_plural": "Messages",
                "ordering": ["created_at"],
            },
        ),
        migrations.CreateModel(
            name="MessageAttachment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="community/attachments/%Y/%m/%d/")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("message", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attachments", to="community.message")),
            ],
        ),
        migrations.CreateModel(
            name="MessageReaction",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("emoji", models.CharField(default="❤️", max_length=8)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("message", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reactions", to="community.message")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="community_reactions", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Réaction",
                "verbose_name_plural": "Réactions",
            },
        ),
        migrations.CreateModel(
            name="CommunityBan",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reason", models.CharField(blank=True, default="", max_length=255)),
                ("can_read", models.BooleanField(default=True, help_text="Si décoché, l'utilisateur ne peut plus rien lire non plus.")),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to=settings.AUTH_USER_MODEL)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="community_ban", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Bannissement",
                "verbose_name_plural": "Bannissements",
            },
        ),
        migrations.CreateModel(
            name="ChannelMute",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reason", models.CharField(blank=True, default="", max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("channel", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="mutes", to="community.channel")),
                ("created_by", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="+", to=settings.AUTH_USER_MODEL)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="channel_mutes", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Mute (salon)",
                "verbose_name_plural": "Mutes (salon)",
            },
        ),
        migrations.AddIndex(
            model_name="message",
            index=models.Index(fields=["channel", "created_at"], name="community_m_channel_314b55_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="messagereaction",
            unique_together={("message", "user", "emoji")},
        ),
        migrations.AlterUniqueTogether(
            name="channelmute",
            unique_together={("channel", "user")},
        ),
    ]
