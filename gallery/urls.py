# gallery/urls.py
from django.urls import path
from django.views.generic import TemplateView
from . import views        # contiene OperaCreateView, ecc.

app_name = "gallery"       # cambia se serve

urlpatterns = [
    # ─────────── DASHBOARD (HOME) ───────────
    path(
        "", 
        TemplateView.as_view(template_name="museo/opere_dashboard.html"),
        name="opere_dashboard"
    ),

    # ─────────── CRUD OPERE ───────────
    path("opere/nuova/",
         views.OperaCreateView.as_view(),
         name="opera_create"),

    path("opere/cerca/",
         TemplateView.as_view(template_name="museo/opera_search.html"),
         name="opera_search"),

    path("opere/modifica/",
         TemplateView.as_view(template_name="museo/opera_update_select.html"),
         name="opera_update_select"),

    path("opere/elimina/",
         TemplateView.as_view(template_name="museo/opera_delete_select.html"),
         name="opera_delete_select"),

    # ─────────── SEZIONI SECONDARIE ───────────
    path("autori/",
         TemplateView.as_view(template_name="museo/autori_list.html"),
         name="autori_list"),

    path("sale/",
         TemplateView.as_view(template_name="museo/sale_list.html"),
         name="sale_list"),

    path("temi/",
         TemplateView.as_view(template_name="museo/temi_list.html"),
         name="temi_list"),
]
