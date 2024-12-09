# Generated by Django 5.1.3 on 2024-12-04 20:42

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('scientific_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('care_instructions', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='plants/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('stock', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='services/')),
                ('price', models.DecimalField(decimal_places=2, default=50, max_digits=10)),
                ('duration_in_months', models.IntegerField(default=1, help_text='Duration in months')),
                ('category', models.CharField(choices=[('planting', 'Planting'), ('maintenance', 'Maintenance'), ('designing', 'Designing'), ('other', 'Other')], default='Landscaping', max_length=50)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlantRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('request_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('delivery_address', models.TextField()),
                ('phone_number', models.CharField(max_length=15)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.plant')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuoteRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+254 xxxxxxxxx'.", regex='^\\+254\\d{9}$')])),
                ('property_image', models.ImageField(blank=True, null=True, upload_to='property_images/')),
                ('location', models.CharField(max_length=100)),
                ('additional_info', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.service')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('address', models.TextField(blank=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_images/')),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female')], max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
