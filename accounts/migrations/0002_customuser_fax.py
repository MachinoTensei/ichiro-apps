# Generated by Django 3.2.7 on 2021-09-10 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='fax',
            field=models.CharField(blank=True, max_length=150, verbose_name='FAX'),
        ),
    ]
