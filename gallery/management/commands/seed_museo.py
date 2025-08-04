from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from pathlib import Path
import csv, random, itertools
from datetime import datetime, timedelta
from faker import Faker

from gallery.models import Tema, Sala, Autore, Opera

CHUNK = 500  # bulk_create chunk size

# ----------------------------------------------------------------------
#  HELPER UTILITIES
# ----------------------------------------------------------------------

def _grouper(iterable, n):
    """Yield fixed-length chunks from *iterable* (chunk size *n*)."""
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk


def _parse_date(value: str):
    """Accetta 'YYYY-MM-DD' oppure 'DD/MM/YYYY' e restituisce datetime.date."""
    if not value:
        return None
    if '/' in value:
        return datetime.strptime(value, "%d/%m/%Y").date()
    return datetime.strptime(value, "%Y-%m-%d").date()

# ----------------------------------------------------------------------
#  MANAGEMENT COMMAND
# ----------------------------------------------------------------------
class Command(BaseCommand):
    help = (
        "Popola il database Museo con dati di test o da CSV.\n\n"
        "Esempi:\n"
        "  python manage.py seed_museo --fake 1000              # dati faker\n"
        "  python manage.py seed_museo --csv ./dati             # 4 csv nella cartella\n"
    )

    # -------------------------
    #  ARGUMENTI
    # -------------------------
    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--fake", type=int, metavar="N",
                           help="Numero di opere da generare con Faker (auto-scala autori/sale/temi)")
        group.add_argument("--csv", type=Path,
                           help="Cartella con temas.csv, salas.csv, autores.csv, operas.csv — intestazioni snake_case")
        parser.add_argument("--flush", action="store_true", help="Svuota le tabelle prima di importare")

    # -------------------------
    #  MAIN
    # -------------------------
    def handle(self, *args, **opts):
        if opts["flush"]:
            self._flush_tables()

        if opts["csv"]:
            self._import_from_csv(opts["csv"])
        else:
            self._generate_fake(opts["fake"])

    # -------------------------
    #  HELPERS
    # -------------------------
    def _flush_tables(self):
        self.stdout.write("\n» Pulizia tabelle…", ending=" ")
        Opera.objects.all().delete()
        Sala.objects.all().delete()
        Autore.objects.all().delete()
        Tema.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("ok"))

    # --- CSV ----------------------------------------------------------
    def _import_from_csv(self, folder: Path):
        self.stdout.write(f"\n» Import CSV da {folder.resolve()}")
        expected = {
            'temas': (Tema, self._row_tema),
            'salas': (Sala, self._row_sala),
            'autores': (Autore, self._row_autore),
            'operas': (Opera, self._row_opera),
        }
        for name, (model, builder) in expected.items():
            file = folder / f"{name}.csv"
            if not file.exists():
                raise CommandError(f"Manca il file {file}")
            objs = [builder(row) for row in self._read_csv(file)]
            self._bulk_save(model, objs)
            self.stdout.write(f"  {name.capitalize():8}: {len(objs)} record")
        self.stdout.write(self.style.SUCCESS("✓ Import completato"))

    def _read_csv(self, file: Path):
        with file.open(newline='', encoding='utf-8') as fh:
            yield from csv.DictReader(fh)

    # --- Faker --------------------------------------------------------
    def _generate_fake(self, n_opere: int):
        fake = Faker("it_IT")
        self.stdout.write(f"\n» Genero dati faker: {n_opere} opere…")
        n_autori = max(10, n_opere // 10)
        n_temi   = 8
        n_sale   = 10

        # TEMI
        temi_objs = [Tema(descrizione=fake.word()) for _ in range(n_temi)]
        temi = self._bulk_save(Tema, temi_objs)

        # SALE
        sale_objs = [
            Sala(
                nome=f"Sala {i+1}",
                superficie=random.randint(50, 200),
                tema=random.choice(temi),
            )
            for i in range(n_sale)
        ]
        sale = self._bulk_save(Sala, sale_objs)

        # AUTORI
        autori_objs = []
        for _ in range(n_autori):
            data_nascita = fake.date_of_birth(minimum_age=20, maximum_age=90)
            tipo = random.choice([Autore.VIVO, Autore.MORTO])
            data_morte = None
            if tipo == Autore.MORTO:
                # tra 20 e 90 anni dopo la nascita, ma prima di oggi
                death_age = random.randint(20, 90)
                data_morte = min(datetime.today().date() - timedelta(days=1),
                                  data_nascita + timedelta(days=death_age * 365))
            autori_objs.append(
                Autore(
                    nome=fake.first_name(),
                    cognome=fake.last_name(),
                    nazione=fake.country_code(),
                    data_nascita=data_nascita,
                    tipo=tipo,
                    data_morte=data_morte,
                )
            )
        autori = self._bulk_save(Autore, autori_objs)

        # OPERE
        opere = []
        for _ in range(n_opere):
            opere.append(
                Opera(
                    autore=random.choice(autori),
                    titolo=fake.sentence(nb_words=3),
                    anno_acquisto=random.randint(1800, 2025),
                    anno_realizzazione=random.randint(1500, 2024),
                    tipo=random.choice([Opera.QUADRO, Opera.SCULTURA]),
                    esposta_in_sala=random.choice(sale) if random.random() < 0.7 else None,
                )
            )
        self._bulk_save(Opera, opere)
        self.stdout.write(self.style.SUCCESS("✓ Popolamento completato"))

    # ---------------- CSV row-to-model builders -----------------------
    def _row_tema(self, row):
        return Tema(pk=int(row.get('codice') or row.get('id') or 0) or None,
                    descrizione=row['descrizione'])

    def _row_sala(self, row):
        tema_id = row.get('tema') or row.get('temaSala')
        tema = Tema.objects.get(pk=int(tema_id)) if tema_id else None
        return Sala(pk=int(row.get('numero', 0)) or None,
                    nome=row['nome'],
                    superficie=int(row['superficie']),
                    tema=tema)

    def _row_autore(self, row):
        return Autore(
            pk=int(row.get('codice', 0)) or None,
            nome=row['nome'],
            cognome=row['cognome'],
            nazione=row['nazione'],
            data_nascita=_parse_date(row['data_nascita']),
            tipo=row['tipo'],
            data_morte=_parse_date(row.get('data_morte')),
        )

    def _row_opera(self, row):
        return Opera(
            pk=int(row.get('codice', 0)) or None,
            autore=Autore.objects.get(pk=int(row['autore'])),
            titolo=row['titolo'],
            anno_acquisto=int(row['anno_acquisto']),
            anno_realizzazione=int(row['anno_realizzazione']),
            tipo=row['tipo'],
            esposta_in_sala=Sala.objects.filter(pk=row.get('esposta_in_sala')).first(),
        )

    # ---------------- BULK SAVE --------------------------------------
    def _bulk_save(self, model, objs):
        """Bulk‑insert *objs* and return the saved queryset so that PKs are guaranteed."""
        if not objs:
            return []
        with transaction.atomic():
            for chunk in _grouper(objs, CHUNK):
                model.objects.bulk_create(chunk)  # PKs returned by Postgres
        return list(model.objects.filter(pk__in=[o.pk for o in objs]))
