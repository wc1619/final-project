# Generated by Django 2.0.8 on 2020-08-21 16:12

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('fasteat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='refCode',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
