# Generated by Django 4.2.4 on 2023-09-03 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvitationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True)),
                ('is_used', models.BooleanField(default=False)),
                ('expiration_date', models.DateTimeField()),
            ],
        ),
    ]
