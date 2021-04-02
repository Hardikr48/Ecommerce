# Generated by Django 2.1.5 on 2020-02-27 09:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_items', djongo.models.fields.ArrayField(model_container=models.CharField(max_length=255))),
                ('total_quantity', models.IntegerField()),
                ('total_amount', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('mobile_no', models.IntegerField()),
                ('address', models.TextField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zipcode', models.IntegerField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('order_status', models.CharField(choices=[('deliverd', 'deliverd'), ('pending', 'pending'), ('reject', 'reject'), ('cancel', 'cancel'), ('shipped', 'shipped')], max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
