from django.urls import path

from . import views

urlpatterns = [
    path('analytics/', views.analytics_home, name='analytics_home_view'),
    path('analytics/get_data/', views.get_analytics_data, name='analytics_get_data'),
]
