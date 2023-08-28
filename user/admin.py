from django.contrib import admin

from .models import NoteUser


class NoteUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'email_confirmed']


# Register your models here.
admin.site.register(NoteUser, NoteUserAdmin)
