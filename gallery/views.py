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




