# ===========================
# gallery/views.py
# ===========================
"""Class-based views per l'app 'gallery'."""

from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, DeleteView
from .models import Opera

class DashboardView(TemplateView):
    template_name = "museo/opere_dashboard.html"

class OperaCreateView(CreateView):
    model = Opera
    template_name = "museo/opera_form.html"
    fields = ["autore", "titolo", "anno_realizzazione", "anno_acquisto", "tipo", "esposta_in_sala", "immagine"]
    success_url = reverse_lazy("gallery:opere_dashboard")

class OperaUpdateView(UpdateView):
    model = Opera
    template_name = "museo/opera_form.html"
    fields = ["autore", "titolo", "anno_realizzazione", "anno_acquisto", "tipo", "esposta_in_sala", "immagine"]
    success_url = reverse_lazy("gallery:opere_dashboard")

class OperaDetailView(DetailView):
    model = Opera
    template_name = "museo/opera_detail.html"

class OperaDeleteView(DeleteView):
    model = Opera
    template_name = "museo/opera_confirm_delete.html"
    success_url = reverse_lazy("gallery:opere_dashboard")









