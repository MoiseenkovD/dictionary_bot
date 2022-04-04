from django.db import models

from dictionary_bot import model_choices as mch


class Users(models.Model):
    first_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=100, default=None, blank=True, null=True)
    username = models.CharField(max_length=100, default=None, blank=True, null=True)
    pending_state = models.CharField(max_length=30, default=None, blank=True, null=True)
    native_language = models.CharField(max_length=10, default=None, blank=True, null=True)
    target_language = models.CharField(max_length=10, default=None, blank=True, null=True)
    chat_id = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'Users'
        db_table = "users"


class Dictionary(models.Model):
    user = models.ForeignKey('dictionary_bot.Users', on_delete=models.CASCADE, verbose_name='user')
    original_word = models.CharField(max_length=100, default=None, blank=True, null=True)
    original_word_lang_code = models.CharField(max_length=5)
    translated_word = models.CharField(max_length=100, default=None, blank=True, null=True)
    translated_word_lang_code = models.CharField(max_length=5)
    context = models.CharField(max_length=600, default=None, blank=True, null=True)
    created_at = models.DateTimeField(default=None, blank=True, null=True)
    updated_at = models.DateTimeField(default=None, blank=True, null=True)

    def user_name(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'dictionary'
        verbose_name_plural = 'Dictionaries'
