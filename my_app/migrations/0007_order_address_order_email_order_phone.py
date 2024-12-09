# Generated by Django 5.1.3 on 2024-12-08 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0006_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.TextField(default='Default Address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(default='default@example.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(default='+254700000000', max_length=15),
            preserve_default=False,
        ),
    ]