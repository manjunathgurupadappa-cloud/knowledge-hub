from django.urls import path

from . import views

app_name = "logs"

urlpatterns = [
    path("", views.log_list, name="list"),
    path("new/", views.log_create, name="create"),
    path("<int:pk>/", views.log_detail, name="detail"),
    path("<int:pk>/edit/", views.log_edit, name="edit"),
    path("<int:pk>/delete/", views.log_delete, name="delete"),
    path("topics/", views.topic_list, name="topic_list"),
    path("topics/<int:pk>/edit/", views.topic_edit, name="topic_edit"),
    path("topics/<int:pk>/delete/", views.topic_delete, name="topic_delete"),
]
