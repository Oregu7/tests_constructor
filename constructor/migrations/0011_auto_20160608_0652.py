# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-06-08 03:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('constructor', '0010_auto_20160522_2113'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'verbose_name': 'Ответ', 'verbose_name_plural': 'Ответы'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Категорию', 'verbose_name_plural': 'Категории'},
        ),
        migrations.AlterModelOptions(
            name='option',
            options={'verbose_name': 'Вариант', 'verbose_name_plural': 'Варианты'},
        ),
        migrations.AlterModelOptions(
            name='query',
            options={'verbose_name': 'Вопрос', 'verbose_name_plural': 'Вопросы'},
        ),
        migrations.AlterModelOptions(
            name='test',
            options={'verbose_name': 'Тест', 'verbose_name_plural': 'Тесты'},
        ),
        migrations.RemoveField(
            model_name='test',
            name='questions_count',
        ),
        migrations.AlterField(
            model_name='answer',
            name='analytics',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AlterField(
            model_name='answer',
            name='correct',
            field=models.BooleanField(default=False, verbose_name='Правильность ответа'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='constructor.Query', verbose_name='Вопрос'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='text',
            field=models.CharField(blank=True, max_length=200, verbose_name='Текст ответа'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=250, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='option',
            name='number',
            field=models.IntegerField(default=1, verbose_name='Номер'),
        ),
        migrations.AlterField(
            model_name='option',
            name='public_access',
            field=models.BooleanField(default=False, verbose_name='Публичный доступ'),
        ),
        migrations.AlterField(
            model_name='option',
            name='questions',
            field=models.ManyToManyField(blank=True, to='constructor.Query', verbose_name='Ответы'),
        ),
        migrations.AlterField(
            model_name='option',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='constructor.Test', verbose_name='Тест'),
        ),
        migrations.AlterField(
            model_name='option',
            name='time',
            field=models.IntegerField(default=0, verbose_name='Ограничения по времени'),
        ),
        migrations.AlterField(
            model_name='query',
            name='help',
            field=models.TextField(blank=True, verbose_name='Текст подсказки'),
        ),
        migrations.AlterField(
            model_name='query',
            name='point',
            field=models.IntegerField(default=1, verbose_name='Балл'),
        ),
        migrations.AlterField(
            model_name='query',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='constructor.Test', verbose_name='Тест'),
        ),
        migrations.AlterField(
            model_name='query',
            name='text',
            field=models.TextField(verbose_name='Текст вопроса'),
        ),
        migrations.AlterField(
            model_name='test',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='constructor.Category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='test',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Создатель'),
        ),
        migrations.AlterField(
            model_name='test',
            name='date',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='test',
            name='description',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='test',
            name='four_mark',
            field=models.IntegerField(verbose_name='Четверка (до %)'),
        ),
        migrations.AlterField(
            model_name='test',
            name='helps',
            field=models.BooleanField(default=False, verbose_name='Подсказки'),
        ),
        migrations.AlterField(
            model_name='test',
            name='three_mark',
            field=models.IntegerField(verbose_name='Тройка (до %)'),
        ),
        migrations.AlterField(
            model_name='test',
            name='time_completion',
            field=models.IntegerField(default=20, verbose_name='Ограничение по времени'),
        ),
        migrations.AlterField(
            model_name='test',
            name='title',
            field=models.CharField(max_length=200, verbose_name='Тема'),
        ),
        migrations.AlterField(
            model_name='test',
            name='two_mark',
            field=models.IntegerField(verbose_name='Двойка (до %)'),
        ),
    ]
