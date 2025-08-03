# ===========================
# gallery/urls.py
# ===========================
"""Routing HTML + tutte le API stub."""

from django.urls import path
from django.views.generic import TemplateView
from . import views, api_views

app_name = "gallery"

urlpatterns = [
    # Pagine HTML
    path("", views.DashboardView.as_view(), name="opere_dashboard"),
    path("opere/nuova/",    views.OperaCreateView.as_view(), name="opera_create"),
    path("opere/cerca/",    TemplateView.as_view(template_name="museo/opera_search.html"),        name="opera_search"),
    path("opere/modifica/", TemplateView.as_view(template_name="museo/opera_update_select.html"), name="opera_update_select"),
    path("opere/elimina/",  TemplateView.as_view(template_name="museo/opera_delete_select.html"), name="opera_delete_select"),

    path("autori/", TemplateView.as_view(template_name="museo/autori_list.html"), name="autori_list"),
    path("sale/",   TemplateView.as_view(template_name="museo/sale_list.html"),   name="sale_list"),
    path("temi/",   TemplateView.as_view(template_name="museo/temi_list.html"),   name="temi_list"),

    # API Autori
    path("api/autori/",            api_views.autori_lista,          name="api_autori_lista"),
    path("api/autori/search/",     api_views.autori_search,         name="api_autori_search"),
    path("api/autori/update/",     api_views.autori_update,         name="api_autori_update"),

    # API Sale
    path("api/sale/",              api_views.sale_lista,            name="api_sale_lista"),

    # API Opere – inserimento/ricerca
    path("api/opere/",             api_views.opera_create,          name="api_opera_create"),
    path("api/opere/search/",      api_views.opere_search,          name="api_opere_search"),

    # API Opere – Modifica
    path("api/opere/update/search/", api_views.opere_update_search, name="api_opere_update_search"),
    path("api/opera/get/",           api_views.opera_get,           name="api_opera_get"),
    path("api/opera/update/",        api_views.opera_update,        name="api_opera_update"),

    # API Opere – Elimina
    path("api/opere/delete/search/", api_views.opere_delete_search, name="api_opere_delete_search"),
    path("api/opere/delete/",        api_views.opere_delete,        name="api_opere_delete"),
]




