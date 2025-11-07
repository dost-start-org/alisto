# Generated migration for converting URLField to TextField for logo storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agencies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agency',
            name='logo_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
