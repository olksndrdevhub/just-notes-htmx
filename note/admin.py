from django.contrib import admin

from .models import Note

# Register your models here.
class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'author', 'completed', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

admin.site.register(Note, NoteAdmin)
