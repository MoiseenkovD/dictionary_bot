from django.contrib import admin

from dictionary_bot.models import Users, Dictionary


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'pending_state',
        'chat_id',       
    )


@admin.register(Dictionary)
class DictionaryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_name',
        'original_word',
        'original_word_lang_code',
        'translated_word',
        'translated_word_lang_code',
        'context',
        'created_at',
        'updated_at',
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super(DictionaryAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['user'].label_from_instance = lambda inst: f"{inst.first_name}"
        return form


