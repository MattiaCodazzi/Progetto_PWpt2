from django.urls import path
from . import views

urlpatterns = [
    # path('', views.ArtworkListView.as_view(), name='artwork-list'),
]

from .views import DashboardView
urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    # … altre rotte …
]
