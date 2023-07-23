from django.db import models

from user.models import NoteUser


# Create your models here.
class Note(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    author = models.ForeignKey(NoteUser, on_delete=models.CASCADE,
                               related_name='notes')
    completed_at = models.DateTimeField(help_text="None if the note isn't completed. Contain datetime when the note was completed", blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}: {self.title}'

    @property
    def is_completed(self):
        '''check if note completed'''
        if self.completed_at is not None:
            return True
        return False
