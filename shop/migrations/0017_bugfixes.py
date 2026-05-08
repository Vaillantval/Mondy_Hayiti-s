import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_productprice'),
    ]

    operations = [
        # Bug 9 : slug unique sur Product
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
        # Bug 8 : FK Product sur OrderDetail pour restitution de stock fiable
        migrations.AddField(
            model_name='orderdetail',
            name='product',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='ordered_items',
                to='shop.product',
            ),
        ),
    ]
