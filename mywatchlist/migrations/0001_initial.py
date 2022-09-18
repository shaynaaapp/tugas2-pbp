# Generated by Django 4.1 on 2022-09-18 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyWatchListItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('watched', models.CharField(max_length=255)),
                ('title', models.TextField()),
                ('rating', models.IntegerField()),
                ('release_date', models.TextField()),
                ('review', models.TextField()),
            ],
        ),
    ]
