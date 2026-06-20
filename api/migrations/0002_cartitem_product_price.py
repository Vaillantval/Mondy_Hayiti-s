from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
        ("shop", "0019_setting_apk_url"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="product_price",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="cart_items",
                to="shop.productprice",
            ),
        ),
    ]
