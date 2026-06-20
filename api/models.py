from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from shop.models.Product import Product
from shop.models.ProductPrice import ProductPrice

User = settings.AUTH_USER_MODEL


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    product_price = models.ForeignKey(
        ProductPrice, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def unit_price(self):
        if self.product_price_id and self.product_price:
            return self.product_price.price
        return self.product.solde_price

    @property
    def price_label(self):
        if self.product_price_id and self.product_price:
            return self.product_price.label
        return ''

    class Meta:
        unique_together = ("user", "product")
        ordering = ["-created_at"]

    def __str__(self):
        return f"CartItem({self.user_id}, {self.product_id}, qty={self.quantity})"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product", "author")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Review({self.product_id}, {self.author_id}, {self.rating}★)"


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlist_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist_items")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Wishlist({self.user_id}, {self.product_id})"
