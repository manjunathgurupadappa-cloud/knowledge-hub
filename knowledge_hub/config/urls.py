from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("logs/", include("logs.urls")),
    path("books/", include("books.urls")),
    path("", include("core.urls")),
]
