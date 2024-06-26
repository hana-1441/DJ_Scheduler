# Generated by Django 4.2.11 on 2024-03-29 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pl', models.CharField(max_length=100)),
                ('topic', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=200, null=True)),
                ('html_doc', models.FileField(null=True, upload_to='html_files/')),
                ('examples', models.CharField(max_length=1000, null=True)),
                ('time_in', models.CharField(max_length=200, null=True)),
                ('time_out', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
