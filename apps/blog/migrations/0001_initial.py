# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-27 11:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('head_img', models.CharField(max_length=150, verbose_name='hand image')),
                ('quote_title', models.CharField(blank=True, max_length=100, null=True, verbose_name='quote title')),
                ('quote', models.TextField(verbose_name='quote')),
                ('quote_cite', models.CharField(blank=True, max_length=40, null=True, verbose_name='quote_cite')),
                ('quote_footer', models.CharField(blank=True, max_length=100, null=True, verbose_name='quote_footer')),
                ('article_md', models.TextField(verbose_name='markdown article text')),
                ('article_html', models.TextField(default='', verbose_name='html article text')),
                ('is_valid', models.BooleanField(default=True, verbose_name='if is valid')),
                ('create_time', models.DateTimeField(verbose_name='create time')),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='modify time')),
                ('pinyin_title', models.CharField(default='', max_length=100, verbose_name='initial pinyin title')),
            ],
            options={
                'db_table': 'article',
            },
        ),
        migrations.CreateModel(
            name='Classify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='classification name')),
            ],
            options={
                'db_table': 'classify',
            },
        ),
        migrations.CreateModel(
            name='TagModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=20, verbose_name='article tag')),
            ],
            options={
                'db_table': 'tag',
            },
        ),
        migrations.AddField(
            model_name='articlemodel',
            name='classify',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to='blog.Classify'),
        ),
        migrations.AddField(
            model_name='articlemodel',
            name='tag',
            field=models.ManyToManyField(related_name='article', to='blog.TagModel'),
        ),
    ]
