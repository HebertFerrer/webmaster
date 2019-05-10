# Generated by Django 2.2 on 2019-05-09 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20190509_1526'),
    ]

    operations = [
        migrations.RenameField(
            model_name='application',
            old_name='employee',
            new_name='candidate',
        ),
        migrations.AlterField(
            model_name='application',
            name='status',
            field=models.IntegerField(choices=[(1, 'Accepted'), (2, 'Rejected'), (3, 'Waiting')]),
        ),
    ]
