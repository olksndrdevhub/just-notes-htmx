from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home_view'),
    path('note/', views.note_view, name='note_view'),
    path('notes/', views.bulk_notes_view, name='bulk_notes_view'),
    path('note/<int:note_id>/', views.delete_note_view,
         name='delete_note_view'),
]
