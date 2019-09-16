from django.urls import path

from . import views

urlpatterns = [
    path('', views.client_main_page),
    path('profile', views.client_profile),
    path('edit', views.client_edit_main),
    path('save_edit_main', views.save_client_edit_main),  # TODO: есть ли лучший метод обработки POST ?
    path('edit/skills', views.client_edit_skills),
    path('save_edit_skills', views.save_client_edit_skills),
]