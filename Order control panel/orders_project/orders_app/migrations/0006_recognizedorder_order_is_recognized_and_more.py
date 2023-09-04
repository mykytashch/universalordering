# Generated by Django 4.2.4 on 2023-09-04 03:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders_app', '0005_comment_unrecognized_order_alter_comment_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecognizedOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('customer_name', models.CharField(max_length=255)),
                ('product', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='order',
            name='is_recognized',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='order',
            name='unrecognized_data',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='unrecognizedorder',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='customer_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='product',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
