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
    from django.db.models import Q

    query = request.GET.get("query", "").strip()
    if not query:
        return JsonResponse([], safe=False)

    autori = Autore.objects.filter(
        Q(nome__icontains=query) | Q(cognome__icontains=query)
    ).order_by("cognome")[:10]

    risultati = [
        {"codice": a.codice, "nome": a.nome, "cognome": a.cognome}
        for a in autori
    ]
    return JsonResponse(risultati, safe=False)

@csrf_exempt
@require_POST
def autori_delete(request):
    codici = request.POST.getlist("codici[]")
    if not codici:
        return JsonResponse({"error": "Nessun autore selezionato"}, status=400)
    eliminate, _ = Autore.objects.filter(codice__in=codici).delete()
    return JsonResponse({"msg": f"{eliminate} autore/i eliminati"})




@csrf_exempt
@require_POST
def autore_check_or_create(request):
    nome_completo = request.POST.get("nome_completo", "").strip()
    parti = nome_completo.split()
    if len(parti) < 2:
        return JsonResponse({"esiste": False})

    nome = parti[0]
    cognome = " ".join(parti[1:])
    try:
        autore = Autore.objects.get(nome__iexact=nome, cognome__iexact=cognome)
        return JsonResponse({"esiste": True, "codice": autore.codice})
    except Autore.DoesNotExist:
        return JsonResponse({"esiste": False})

@csrf_exempt
@require_POST
def autore_create(request):
    nome = request.POST.get("nome")
    cognome = request.POST.get("cognome")
    nazione = request.POST.get("nazione")
    data_nascita = request.POST.get("dataNascita")  # <-- con N maiuscola
    data_morte = request.POST.get("dataMorte")
    tipo = request.POST.get("tipo")

    if not nome or not cognome or not nazione:
        return JsonResponse({"error": "Dati mancanti"}, status=400)
    if tipo == "vivo":
        data_morte = None
    elif tipo == "morto" and not data_morte:
        return JsonResponse({"error": "Data di morte richiesta per autore morto"}, status=400)
    autore = Autore.objects.create(
        nome=nome,
        cognome=cognome,
        nazione=nazione,
        data_nascita=data_nascita or None,
        data_morte=data_morte or None,
        tipo=tipo
    )

    return JsonResponse({"msg": "Autore inserito", "id": autore.codice})



@require_POST
def autori_update(request):
    codice = request.POST.get("codice")
    nome = request.POST.get("nome", "").strip()
    cognome = request.POST.get("cognome", "").strip()
    nazione = request.POST.get("nazione", "").strip()
    data_nascita = request.POST.get("dataNascita") or None
    data_morte = request.POST.get("dataMorte") or None
    tipo = request.POST.get("tipo", "").strip()

    if not codice or not nome or not cognome or not nazione:
        return JsonResponse({"error": "Dati incompleti"}, status=400)

    # 🛑 Se è stato inserito un tipo "vivo" ma c'è una data di morte, blocca
    if tipo == "vivo" and data_morte:
        return JsonResponse({"error": "Un autore vivo non può avere una data di morte."}, status=400)

    # 🛑 Se è stato selezionato "morto" ma manca la data di morte
    if tipo == "morto" and not data_morte:
        return JsonResponse({"error": "Seleziona una data di morte per un autore morto."}, status=400)

    try:
        autore = Autore.objects.get(codice=codice)
        autore.nome = nome
        autore.cognome = cognome
        autore.nazione = nazione
        autore.data_nascita = data_nascita
        autore.data_morte = data_morte
        autore.tipo = tipo
        autore.save()
        return JsonResponse({"msg": "Autore aggiornato"})
    except Autore.DoesNotExist:
        return JsonResponse({"error": "Autore non trovato"}, status=404)



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
        sala = Sala.objects.get(pk=sala_id) if sala_id not in [None, ""] else None


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
    autore_nome = request.POST.get("autore_nome", "").strip()
    tipo = request.POST.get("tipo", "")
    sala_id = request.POST.get("salaId", "")
    anno_real_min = request.POST.get("annoRealizzazioneMin", "")
    anno_real_max = request.POST.get("annoRealizzazioneMax", "")
    anno_acq_min = request.POST.get("annoAcquistoMin", "")
    anno_acq_max = request.POST.get("annoAcquistoMax", "")

    pagina = int(request.POST.get("pagina", 1))
    limite = 10
    offset = (pagina - 1) * limite

    filtri = Q()
    if titolo:
        filtri &= Q(titolo__istartswith=titolo)
    if autore_nome:
        parti = autore_nome.split()
        if len(parti) >= 2:
            nome = parti[0]
            cognome = " ".join(parti[1:])
            filtri &= Q(autore__nome__iexact=nome, autore__cognome__iexact=cognome)

    if tipo:
        filtri &= Q(tipo=tipo)
    if sala_id:
        filtri &= Q(esposta_in_sala__numero=sala_id)
    if anno_real_min:
        filtri &= Q(anno_realizzazione__gte=int(anno_real_min))
    if anno_real_max:
        filtri &= Q(anno_realizzazione__lte=int(anno_real_max))
    if anno_acq_min:
        filtri &= Q(anno_acquisto__gte=int(anno_acq_min))
    if anno_acq_max:
        filtri &= Q(anno_acquisto__lte=int(anno_acq_max))

    queryset = Opera.objects.filter(filtri).select_related("autore", "esposta_in_sala")
    totale = queryset.count()
    opere = queryset.order_by("titolo")[offset:offset + limite]

    risultati = []
    for o in opere:
        risultati.append({
    "codice": o.codice,
    "titolo": o.titolo,
    "autore": f"{o.autore.nome} {o.autore.cognome}",
    "autore_id": o.autore.codice,
    "tipo": o.tipo,
    "annoRealizzazione": o.anno_realizzazione,
    "annoAcquisto": o.anno_acquisto,
    "sala": o.esposta_in_sala.nome if o.esposta_in_sala else None,
    "sala_id": o.esposta_in_sala.numero if o.esposta_in_sala else None
})


    return JsonResponse({
        "opere": risultati,
        "totale": totale,
        "limite": limite
    })


    titolo = request.POST.get("titolo", "").strip()
    autore_id = request.POST.get("autore", "")           # ✅ corretto
    tipo = request.POST.get("tipo", "")
    sala_id = request.POST.get("salaId", "")             # ← questo è giusto
    anno_real = request.POST.get("annoRealizzazione", "")
    anno_acq = request.POST.get("annoAcquisto", "")

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
    if anno_real:
        filtri &= Q(anno_realizzazione=anno_real)
    if anno_acq:
        filtri &= Q(anno_acquisto=anno_acq)

    queryset = Opera.objects.filter(filtri).select_related("autore", "esposta_in_sala")
    totale = queryset.count()
    opere = queryset.order_by("titolo")[offset:offset + limite]

    risultati = []
    for o in opere:
        risultati.append({
            "codice": o.codice,
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
        autore_id = request.POST.get("autore")
        sala_id = request.POST.get("sala")

        if not codice or not titolo or not anno_realizzazione or not anno_acquisto or not tipo or not autore_id:
            return JsonResponse({"error": "Campi obbligatori mancanti."}, status=400)

        if int(anno_acquisto) < int(anno_realizzazione):
            return JsonResponse({
                "error": "L'anno di acquisto non può essere precedente a quello di realizzazione."
            }, status=400)

        # Recupera tutte le entità necessarie PRIMA di usarle
        opera = Opera.objects.get(pk=codice)
        autore = Autore.objects.get(pk=autore_id)
        sala = Sala.objects.get(pk=sala_id) if sala_id else None

        # Aggiorna i campi
        opera.titolo = titolo
        opera.anno_realizzazione = int(anno_realizzazione)
        opera.anno_acquisto = int(anno_acquisto)
        opera.tipo = tipo
        opera.autore = autore
        opera.esposta_in_sala = sala
        opera.save()

        return JsonResponse({"msg": "Modifica salvata con successo"})

    except Opera.DoesNotExist:
        return JsonResponse({"error": "Opera non trovata"}, status=404)
    except Autore.DoesNotExist:
        return JsonResponse({"error": "Autore non trovato"}, status=400)
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

# ---- Autori ----

def autori_lista(request):
    autori = Autore.objects.all().values("codice", "nome", "cognome")
    return JsonResponse(list(autori), safe=False)

def autori_search(request):
    from django.db.models import Q

    query = request.GET.get("query", "").strip()
    if not query:
        return JsonResponse([], safe=False)

    autori = Autore.objects.filter(
        Q(nome__icontains=query) | Q(cognome__icontains=query)
    ).order_by("cognome")[:10]

    risultati = [
        {"codice": a.codice, "nome": a.nome, "cognome": a.cognome}
        for a in autori
    ]
    return JsonResponse(risultati, safe=False)



def autore_detail_api(request, pk):
    autore = get_object_or_404(Autore, pk=pk)
    numero_opere = Opera.objects.filter(autore=autore).count()
    return JsonResponse({
        "nome": autore.nome,
        "cognome": autore.cognome,
        "nazione": autore.nazione,
        "data_nascita": autore.data_nascita,
        "data_morte": autore.data_morte,
        "numero_opere": numero_opere,
    })

# ---- Sale ----

def sale_lista(request):
    sale = Sala.objects.all().values("numero", "nome")
    return JsonResponse(list(sale), safe=False)

def sala_detail_api(request, pk):
    sala = get_object_or_404(Sala, pk=pk)
    opere = list(Opera.objects.filter(esposta_in_sala=sala).values("titolo"))
    return JsonResponse({
        "nome": sala.nome,
        "superficie": sala.superficie,
        "tema": sala.tema.descrizione if sala.tema else "—",
        "opere": opere
    })


#--------------AUTORI--------------#

@csrf_exempt
@require_POST
def autori_search_form(request):
    from django.db.models import Q

    nome_completo = request.POST.get("nomeCompleto", "").strip()
    nazione = request.POST.get("nazione", "").strip()
    tipo = request.POST.get("tipo", "").strip()
    data_nascita = request.POST.get("dataNascita", "").strip()
    data_morte = request.POST.get("dataMorte", "").strip()
    pagina = int(request.POST.get("pagina", 1))
    limite = int(request.POST.get("limite", 10))

    filtri = Q()
    if nome_completo:
        parti = nome_completo.split()
        if len(parti) == 1:
            filtri &= Q(nome__icontains=parti[0]) | Q(cognome__icontains=parti[0])
        else:
            filtri &= Q(nome__icontains=parti[0]) & Q(cognome__icontains=" ".join(parti[1:]))
    if nazione:
        filtri &= Q(nazione__icontains=nazione)
    if tipo:
        filtri &= Q(tipo=tipo)
    if data_nascita:
        filtri &= Q(data_nascita=data_nascita)
    if data_morte:
        filtri &= Q(data_morte=data_morte)

    queryset = Autore.objects.filter(filtri).order_by("cognome")
    totale = queryset.count()
    offset = (pagina - 1) * limite
    risultati = queryset[offset:offset + limite]

    dati = [{
        "codice": a.codice,
        "nome": a.nome,
        "cognome": a.cognome,
        "nazione": a.nazione,
        "dataNascita": a.data_nascita.isoformat() if a.data_nascita else "",
        "dataMorte": a.data_morte.isoformat() if a.data_morte else "",
        "tipo": a.tipo
    } for a in risultati]

    return JsonResponse({
        "totale": totale,
        "limite": limite,
        "pagina": pagina,
        "risultati": dati
    })


