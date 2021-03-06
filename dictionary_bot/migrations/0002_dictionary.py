# Generated by Django 4.0.3 on 2022-03-17 13:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dictionary_bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_word', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('original_word_lang_code', models.CharField(choices=[('EN', 'EN'), ('RU', 'RU')], max_length=5)),
                ('translated_word', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('translated_word_lang_code', models.CharField(choices=[('EN', 'EN'), ('RU', 'RU')], max_length=5)),
                ('context', models.CharField(blank=True, default=None, max_length=600, null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dictionary_bot.users', verbose_name='user')),
            ],
        ),
    ]
