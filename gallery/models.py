# Placeholder: vedi documento Starter Kit per il modello completo
from django.db import models

class Autore(models.Model):
    VIVO = "vivo"
    MORTO = "morto"
    TIPO_CHOICES = [(VIVO, "Vivo"), (MORTO, "Morto")]

    codice = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=60)
    cognome = models.CharField(max_length=60)
    nazione = models.CharField(max_length=40)
    data_nascita = models.DateField()
    tipo = models.CharField(max_length=5, choices=TIPO_CHOICES)
    data_morte = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(tipo="vivo", data_morte__isnull=True)
                    | models.Q(tipo="morto", data_morte__isnull=False)
                ),
                name="autore_vivo_morto_constraint",
            )
        ]

    def __str__(self):
        return f"{self.cognome} {self.nome}"


class Tema(models.Model):
    codice = models.AutoField(primary_key=True)
    descrizione = models.TextField()

    def __str__(self):
        return self.descrizione


class Sala(models.Model):
    numero = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=60)
    superficie = models.PositiveIntegerField(help_text="metri quadri")
    tema = models.ForeignKey(Tema, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nome


class Opera(models.Model):
    QUADRO = "Quadro"
    SCULTURA = "Scultura"
    TIPO_CHOICES = [(QUADRO, "Quadro"), (SCULTURA, "Scultura")]

    codice = models.AutoField(primary_key=True)
    autore = models.ForeignKey(
        Autore, on_delete=models.PROTECT, related_name="opere"
    )
    titolo = models.CharField(max_length=120)
    anno_acquisto = models.PositiveSmallIntegerField()
    anno_realizzazione = models.PositiveSmallIntegerField()
    tipo = models.CharField(max_length=8, choices=TIPO_CHOICES)
    esposta_in_sala = models.ForeignKey(
        Sala, null=True, blank=True, on_delete=models.SET_NULL
    )
    immagine = models.ImageField(upload_to="opere/", null=True, blank=True)

    def __str__(self):
        return self.titolo
