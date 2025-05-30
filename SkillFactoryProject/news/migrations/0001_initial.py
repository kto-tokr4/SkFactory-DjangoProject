# Generated by Django 5.2 on 2025-05-10 12:30

import django.db.models.deletion
import django_summernote.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique_for_date='created')),
                ('slug', models.SlugField(max_length=150, unique_for_date='created')),
                ('content', django_summernote.fields.SummernoteTextField()),
                ('category', models.CharField(choices=[('TNK', 'Танк'), ('DMG', 'Разрушитель'), ('HLR', 'Целитель'), ('TRD', 'Торговец'), ('GLM', 'Гилдмастер'), ('QGR', 'Квестодатель'), ('SMT', 'Кузнец'), ('TNR', 'Кожевник'), ('ALC', 'Зельевар'), ('WZD', 'Мастер заклинаний')], max_length=3)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='account.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='account.profile')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.post')),
            ],
        ),
    ]
