# Generated by Django 2.1.1 on 2018-10-09 18:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('container_id', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dockerfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('image_name', models.CharField(max_length=200)),
                ('dockerfile_content', models.TextField()),
                ('dockerfile', models.FileField(blank=True, upload_to='dockerfiles/')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='container',
            name='dockerfile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dockerapp.Dockerfile'),
        ),
    ]
