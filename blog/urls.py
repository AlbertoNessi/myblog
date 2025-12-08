from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('now', views.now, name="now"),
    path('reading', views.reading, name="reading"),
    path('quotes', views.quotes, name="quotes")
]
