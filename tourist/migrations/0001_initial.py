# Generated by Django 2.1.2 on 2018-10-02 09:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReView',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='후기')),
                ('star_score', models.FloatField(default=5.0, verbose_name='별점')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReViewLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_set', to='tourist.ReView')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ReViewPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='review/%Y/%m/%d', verbose_name='후기 사진')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tourist.ReView', verbose_name='후기')),
            ],
        ),
        migrations.CreateModel(
            name='SpotVisit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TouristSpot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_id', models.IntegerField(unique=True)),
                ('visit_user_set', models.ManyToManyField(blank=True, related_name='ts_visit_user_set', through='tourist.SpotVisit', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='spotvisit',
            name='ts',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visit_set', to='tourist.TouristSpot'),
        ),
        migrations.AddField(
            model_name='spotvisit',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='review',
            name='content_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tourist.TouristSpot', verbose_name='관광지'),
        ),
        migrations.AddField(
            model_name='review',
            name='like_user_set',
            field=models.ManyToManyField(blank=True, related_name='rv_like_user_set', through='tourist.ReViewLike', to=settings.AUTH_USER_MODEL),
        ),
    ]
