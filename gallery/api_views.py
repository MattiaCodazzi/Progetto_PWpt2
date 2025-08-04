# ===========================
# gallery/api_views.py
# ===========================
"""API JSON stub: restituisce dati minimi per evitare NoReverseMatch.
   Sostituisci con logica reale quando avrai i modelli."""

from django.http import JsonResponse
from django.views.decorators.http import require_POST

# ---- Autori ----

def autori_lista(request):
    return JsonResponse([], safe=False)

def autori_search(request):
    return JsonResponse([], safe=False)

@require_POST
def autori_update(request):
    return JsonResponse({"msg": "Stub OK"})

# ---- Sale ----

def sale_lista(request):
    return JsonResponse([], safe=False)

# ---- Opere comuni ----
@require_POST
def opera_create(request):
    return JsonResponse({"msg": "Opera creata (stub)"}, status=201)

@require_POST
def opere_search(request):
    return JsonResponse({"opere": [], "totale": 0, "limite": 10})

# ---- Opere pagina Modifica ----
@require_POST
def opere_update_search(request):
    return JsonResponse({"opere": [], "totale": 0, "limite": 10})

def opera_get(request):
    return JsonResponse({"codice": 1, "titolo": "Stub", "annoRealizzazione": 0, "annoAcquisto": 0, "tipo": "Quadro", "espostaInSala": None})

@require_POST
def opera_update(request):
    return JsonResponse({"msg": "Opera aggiornata (stub)"})

# ---- Opere pagina Elimina ----
@require_POST
def opere_delete_search(request):
    return JsonResponse({"opere": [], "totale": 0, "limite": 10})

@require_POST
def opere_delete(request):
    return JsonResponse({"msg": "Eliminazione completata (stub)"})

