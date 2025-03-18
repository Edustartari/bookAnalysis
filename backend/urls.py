from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search/<slug:book_id>", views.search, name="search"),
]