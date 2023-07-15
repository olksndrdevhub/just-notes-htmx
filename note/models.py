from django.db import models

from user.models import NoteUser


# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(NoteUser, on_delete=models.CASCADE,
                               related_name='notes')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}: {self.title}'
