from django.db import models

from shop.models.file_cleanup import collect_replaced_files


class Slider(models.Model):
    title = models.CharField(max_length=60, blank=False, null=False)
    description = models.CharField(max_length=120,blank=False, null=False)
    button_text=  models.CharField(max_length=60,blank=False, null=False)
    button_link = models.CharField(max_length=255,blank=False, null=False)
    image = models.ImageField(upload_to="sliders/%Y/%m/%d/",blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Supprime l'ancienne image quand on en met une nouvelle.
        old_files = collect_replaced_files(self, Slider, ("image",))
        super().save(*args, **kwargs)
        for f in old_files:
            f.delete(save=False)

