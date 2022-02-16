from django import views
from django.urls import path
from user import views


urlpatterns = [
    path('', views.index, name="index"),
    path('sign_up', views.sign_up, name="sign_up"),
    path('sign_up', views.sign_up, name="sign_up"),
    path('logout', views.logout, name="logout"),
    path('delete/<int:id>', views.delete, name="delete"),
    path('edit/<int:id>', views.edit, name="edit"),
    path('user_details/<int:id>', views.user_details, name="user_details"),
]