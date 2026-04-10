from django.db import models
from shop.models.Product import Product


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    label = models.CharField(max_length=60, blank=True, default='')
    price = models.FloatField()
    regular_price = models.FloatField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        if self.label:
            return f"{self.label} — {self.price}"
        return str(self.price)
