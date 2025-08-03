# ===========================
# gallery/views.py
# ===========================
"""Class‑based views per l'app 'gallery'.
   – Dashboard (home)
   – CRUD Opere
   (Le API JSON restano in un futuro api_views.py)
"""

from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)

from .models import Opera


class DashboardView(TemplateView):
    """Homepage: mostra la dashboard delle opere."""

    template_name = "museo/opere_dashboard.html"


# ────────────────────────────── CRUD OPERE ──────────────────────────────

class OperaCreateView(CreateView):
    """Crea una nuova opera."""

    model = Opera
    template_name = "museo/opera_form.html"

    # I campi del model definiti in models.py
    fields = [
        "autore",
        "titolo",
        "anno_realizzazione",
        "anno_acquisto",
        "tipo",
        "esposta_in_sala",
        "immagine",
    ]

    success_url = reverse_lazy("gallery:opere_dashboard")


class OperaUpdateView(UpdateView):
    """Aggiorna un'opera esistente (richiamata via codice pk)."""

    model = Opera
    template_name = "museo/opera_form.html"
    fields = [
        "autore",
        "titolo",
        "anno_realizzazione",
        "anno_acquisto",
        "tipo",
        "esposta_in_sala",
        "immagine",
    ]

    success_url = reverse_lazy("gallery:opere_dashboard")


class OperaDetailView(DetailView):
    """Mostra i dettagli di un'opera (facoltativo, template da creare)."""

    model = Opera
    template_name = "museo/opera_detail.html"  # crea questo template se/quando serve


class OperaDeleteView(DeleteView):
    """Conferma ed elimina un'opera (template da creare)."""

    model = Opera
    template_name = "museo/opera_confirm_delete.html"  # crea questo template se/quando serve
    success_url = reverse_lazy("gallery:opere_dashboard")


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

