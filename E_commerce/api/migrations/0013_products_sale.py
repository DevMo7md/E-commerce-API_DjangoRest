# Generated by Django 5.1.4 on 2025-02-04 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_customuser_reset_password_expires_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='sale',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]
