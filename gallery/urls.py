# ===========================
# gallery/urls.py
# ===========================
"""URL routing per l'app 'gallery'."""

from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = "gallery"

urlpatterns = [
    # HOME / dashboard
    path("", views.DashboardView.as_view(), name="opere_dashboard"),

    # ─── CRUD Opere gestite via view CBV
    path("opere/nuova/", views.OperaCreateView.as_view(), name="opera_create"),

    # Pagina di ricerca (front‑end con AJAX)
    path(
        "opere/cerca/",
        TemplateView.as_view(template_name="museo/opera_search.html"),
        name="opera_search",
    ),

    # Pagina di selezione modifica (front‑end con AJAX)
    path(
        "opere/modifica/",
        TemplateView.as_view(template_name="museo/opera_update_select.html"),
        name="opera_update_select",
    ),

    # Pagina di selezione eliminazione (front‑end con AJAX)
    path(
        "opere/elimina/",
        TemplateView.as_view(template_name="museo/opera_delete_select.html"),
        name="opera_delete_select",
    ),

    # Facoltativo – se vuoi un dettaglio CBV classico:
    # path("opere/<int:pk>/", views.OperaDetailView.as_view(), name="opera_detail"),

    # ─── Sezioni secondarie (template statici/AJAX)
    path(
        "autori/",
        TemplateView.as_view(template_name="museo/autori_list.html"),
        name="autori_list",
    ),
    path(
        "sale/",
        TemplateView.as_view(template_name="museo/sale_list.html"),
        name="sale_list",
    ),
    path(
        "temi/",
        TemplateView.as_view(template_name="museo/temi_list.html"),
        name="temi_list",
    ),
]

