# ===========================
# gallery/api_views.py
# ===========================
"""API JSON reali per inserimento opera, lista autori e sale."""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Autore, Sala, Opera

# ---- Autori ----

def autori_lista(request):
    autori = Autore.objects.all().values("codice", "nome", "cognome")
    return JsonResponse(list(autori), safe=False)

def autori_search(request):
    return JsonResponse([], safe=False)

@require_POST
def autori_update(request):
    return JsonResponse({"msg": "Stub OK"})

# ---- Sale ----

def sale_lista(request):
    sale = Sala.objects.all().values("numero", "nome")
    return JsonResponse(list(sale), safe=False)

# ---- Opere comuni ----

@csrf_exempt
@require_POST
def opera_create(request):
    try:
        autore_id = request.POST.get("autore")
        titolo = request.POST.get("titolo")
        anno_realizzazione = request.POST.get("annoRealizzazione")
        anno_acquisto = request.POST.get("annoAcquisto")
        tipo = request.POST.get("tipo")
        sala_id = request.POST.get("sala") or None

        if not (autore_id and titolo and anno_realizzazione and anno_acquisto and tipo):
            return JsonResponse({"error": "Tutti i campi obbligatori devono essere compilati."}, status=400)

        autore = Autore.objects.get(pk=autore_id)
        sala = Sala.objects.get(pk=sala_id) if sala_id else None

        Opera.objects.create(
            autore=autore,
            titolo=titolo,
            anno_realizzazione=int(anno_realizzazione),
            anno_acquisto=int(anno_acquisto),
            tipo=tipo,
            esposta_in_sala=sala
        )

        return JsonResponse({"msg": "Opera inserita correttamente"}, status=201)

    except Autore.DoesNotExist:
        return JsonResponse({"error": "Autore non trovato."}, status=400)
    except Sala.DoesNotExist:
        return JsonResponse({"error": "Sala non trovata."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_POST
def opere_search(request):
    from django.db.models import Q

    titolo = request.POST.get("titolo", "").strip()
    autore_id = request.POST.get("autoreId", "")
    tipo = request.POST.get("tipo", "")
    sala_id = request.POST.get("salaId", "")

    pagina = int(request.POST.get("pagina", 1))
    limite = 10
    offset = (pagina - 1) * limite

    filtri = Q()
    if titolo:
        filtri &= Q(titolo__icontains=titolo)
    if autore_id:
        filtri &= Q(autore__codice=autore_id)
    if tipo:
        filtri &= Q(tipo=tipo)
    if sala_id:
        filtri &= Q(esposta_in_sala__numero=sala_id)

    queryset = Opera.objects.filter(filtri).select_related("autore", "esposta_in_sala")
    totale = queryset.count()
    opere = queryset.order_by("titolo")[offset:offset + limite]

    risultati = []
    for o in opere:
        risultati.append({
            "titolo": o.titolo,
            "autore": f"{o.autore.nome} {o.autore.cognome}",
            "tipo": o.tipo,
            "annoRealizzazione": o.anno_realizzazione,
            "annoAcquisto": o.anno_acquisto,
            "sala": o.esposta_in_sala.nome if o.esposta_in_sala else None
        })

    return JsonResponse({
        "opere": risultati,
        "totale": totale,
        "limite": limite
    })


def opera_get(request):
    from django.shortcuts import get_object_or_404

    codice = request.GET.get("codice")
    opera = get_object_or_404(Opera, pk=codice)

    return JsonResponse({
        "codice": opera.codice,
        "titolo": opera.titolo,
        "annoRealizzazione": opera.anno_realizzazione,
        "annoAcquisto": opera.anno_acquisto,
        "tipo": opera.tipo,
        "espostaInSala": opera.esposta_in_sala.numero if opera.esposta_in_sala else None
    })


@csrf_exempt
@require_POST
def opere_update_search(request):
    from django.db.models import Q

    titolo = request.POST.get("titolo", "").strip()
    autore_id = request.POST.get("autoreId", "")
    tipo = request.POST.get("tipo", "")
    sala_id = request.POST.get("salaId", "")

    pagina = int(request.POST.get("pagina", 1))
    limite = 10
    offset = (pagina - 1) * limite

    filtri = Q()
    if titolo:
        filtri &= Q(titolo__icontains=titolo)
    if autore_id:
        filtri &= Q(autore__codice=autore_id)
    if tipo:
        filtri &= Q(tipo=tipo)
    if sala_id:
        filtri &= Q(esposta_in_sala__numero=sala_id)

    queryset = Opera.objects.filter(filtri).select_related("autore", "esposta_in_sala")
    totale = queryset.count()
    opere = queryset.order_by("titolo")[offset:offset + limite]

    risultati = [{
        "codice": o.codice,
        "titolo": o.titolo,
        "autore": f"{o.autore.nome} {o.autore.cognome}",
        "tipo": o.tipo,
        "annoRealizzazione": o.anno_realizzazione,
        "annoAcquisto": o.anno_acquisto,
        "sala": o.esposta_in_sala.nome if o.esposta_in_sala else None
    } for o in opere]

    return JsonResponse({
        "opere": risultati,
        "totale": totale,
        "limite": limite
    })

@csrf_exempt
@require_POST
def opera_update(request):
    try:
        codice = request.POST.get("codice")
        titolo = request.POST.get("titolo")
        anno_realizzazione = request.POST.get("annoRealizzazione")
        anno_acquisto = request.POST.get("annoAcquisto")
        tipo = request.POST.get("tipo")
        sala_id = request.POST.get("espostaInSala") or None

        opera = Opera.objects.get(pk=codice)
        opera.titolo = titolo
        opera.anno_realizzazione = int(anno_realizzazione)
        opera.anno_acquisto = int(anno_acquisto)
        opera.tipo = tipo
        opera.esposta_in_sala = Sala.objects.get(pk=sala_id) if sala_id else None
        opera.save()

        return JsonResponse({"msg": "Modifica salvata con successo"})

    except Opera.DoesNotExist:
        return JsonResponse({"error": "Opera non trovata"}, status=404)
    except Sala.DoesNotExist:
        return JsonResponse({"error": "Sala non trovata"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_POST
def opere_delete_search(request):
    from django.db.models import Q

    titolo = request.POST.get("titolo", "").strip()
    autore_id = request.POST.get("autoreId", "")
    tipo = request.POST.get("tipo", "")
    sala_id = request.POST.get("salaId", "")

    pagina = int(request.POST.get("pagina", 1))
    limite = 10
    offset = (pagina - 1) * limite

    filtri = Q()
    if titolo:
        filtri &= Q(titolo__icontains=titolo)
    if autore_id:
        filtri &= Q(autore__codice=autore_id)
    if tipo:
        filtri &= Q(tipo=tipo)
    if sala_id:
        filtri &= Q(esposta_in_sala__numero=sala_id)

    queryset = Opera.objects.filter(filtri).select_related("autore", "esposta_in_sala")
    totale = queryset.count()
    opere = queryset.order_by("titolo")[offset:offset + limite]

    dati = [{
        "codice": o.codice,
        "titolo": o.titolo,
        "autore": f"{o.autore.nome} {o.autore.cognome}",
        "tipo": o.tipo,
        "annoRealizzazione": o.anno_realizzazione,
        "annoAcquisto": o.anno_acquisto,
        "sala": o.esposta_in_sala.nome if o.esposta_in_sala else None
    } for o in opere]

    return JsonResponse({
        "opere": dati,
        "totale": totale,
        "limite": limite
    })


@csrf_exempt
@require_POST
def opere_delete(request):
    from django.http import QueryDict

    codici_raw = request.POST.getlist("codici[]")
    if not codici_raw:
        return JsonResponse({"error": "Nessuna opera selezionata."}, status=400)

    try:
        codici = list(map(int, codici_raw))
        eliminate, _ = Opera.objects.filter(codice__in=codici).delete()
        return JsonResponse({"msg": f"{eliminate} opera/e eliminate correttamente."})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


