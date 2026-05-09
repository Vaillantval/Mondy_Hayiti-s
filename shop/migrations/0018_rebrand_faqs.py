from django.db import migrations

REPLACEMENTS = [
    ("MatStore Haiti ne stocke", "Hayiti's ne stocke"),
    ("sur le compte MatStore Haiti", "sur le compte Hayiti's"),
    ("info@matstorehaiti.online", "info@hayitis.com"),
]


def rebrand_faqs(apps, schema_editor):
    FAQ = apps.get_model('shop', 'FAQ')
    for faq in FAQ.objects.all():
        updated = False
        for old, new in REPLACEMENTS:
            if old in faq.answer:
                faq.answer = faq.answer.replace(old, new)
                updated = True
        if updated:
            faq.save(update_fields=['answer'])


def reverse_rebrand_faqs(apps, schema_editor):
    FAQ = apps.get_model('shop', 'FAQ')
    for faq in FAQ.objects.all():
        updated = False
        for old, new in REPLACEMENTS:
            if new in faq.answer:
                faq.answer = faq.answer.replace(new, old)
                updated = True
        if updated:
            faq.save(update_fields=['answer'])


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_bugfixes'),
    ]

    operations = [
        migrations.RunPython(rebrand_faqs, reverse_rebrand_faqs),
    ]
