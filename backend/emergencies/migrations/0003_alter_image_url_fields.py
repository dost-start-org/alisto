# Generated migration for converting URLField to TextField for image storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emergencies', '0002_emergencyreport_responder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emergencyreport',
            name='image_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='emergencyverification',
            name='image_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
