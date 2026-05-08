from django.db import models
from shop.models.Order import Order


class OrderDetail(models.Model):
    product = models.ForeignKey(
        'shop.Product', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='ordered_items',
    )
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    solde_price = models.FloatField()
    regular_price = models.FloatField()
    quantity = models.IntegerField()
    taxe = models.FloatField()
    sub_total_ht = models.FloatField()
    sub_total_ttc = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Relation avec le modèle Order
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')

    def __str__(self):
        return f"OrderDetail {self.id} - {self.product_name}"