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
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk

def _parse_date(value: str):
    if not value:
        return None
    if '/' in value:
        return datetime.strptime(value, "%d/%m/%Y").date()
    return datetime.strptime(value, "%Y-%m-%d").date()

class Command(BaseCommand):
    help = (
        "Popola il database Museo con dati di test o da CSV.\n\n"
        "Esempi:\n"
        "  python manage.py seed_museo --fake 1000\n"
        "  python manage.py seed_museo --csv ./dati\n"
    )

    def add_arguments(self, parser):
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--fake", type=int, metavar="N", help="Numero di opere da generare con Faker")
        group.add_argument("--csv", type=Path, help="Cartella con temas.csv, salas.csv, autores.csv, operas.csv")
        parser.add_argument("--flush", action="store_true", help="Svuota le tabelle prima di importare")

    def handle(self, *args, **opts):
        if opts["flush"]:
            self._flush_tables()

        if opts["csv"]:
            self._import_from_csv(opts["csv"])
        else:
            self._generate_fake(opts["fake"])

    def _flush_tables(self):
        self.stdout.write("\n» Pulizia tabelle…", ending=" ")
        Opera.objects.all().delete()
        Sala.objects.all().delete()
        Autore.objects.all().delete()
        Tema.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("ok"))

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

    def _generate_fake(self, n_opere: int):
        fake = Faker("it_IT")
        self.stdout.write(f"\n» Genero dati faker: {n_opere} opere…")
        n_autori = max(10, n_opere // 10)
        n_temi   = 8
        n_sale   = 10

        temi_objs = [Tema(descrizione=fake.word()) for _ in range(n_temi)]
        temi = self._bulk_save(Tema, temi_objs)

        sale_objs = [
            Sala(
                nome=f"Sala {i+1}",
                superficie=random.randint(50, 200),
                tema=random.choice(temi),
            )
            for i in range(n_sale)
        ]
        sale = self._bulk_save(Sala, sale_objs)

        autori_objs = []
        for _ in range(n_autori):
            nome = fake.first_name()
            cognome = fake.last_name()
            nazione = "IT" 
            data_nascita = fake.date_of_birth(minimum_age=30, maximum_age=90)
            tipo = random.choice([Autore.VIVO, Autore.MORTO])
            data_morte = None
            if tipo == Autore.MORTO:
                death_age = random.randint(50, 90)
                data_morte = data_nascita + timedelta(days=death_age * 365)
                if data_morte > datetime.today().date():
                    data_morte = datetime.today().date() - timedelta(days=random.randint(30, 365))
            autori_objs.append(
                Autore(
                    nome=nome,
                    cognome=cognome,
                    nazione=nazione,
                    data_nascita=data_nascita,
                    tipo=tipo,
                    data_morte=data_morte if tipo == Autore.MORTO else None,
                )
            )
        autori = self._bulk_save(Autore, autori_objs)

        opere = []
        oggi = datetime.today().year
        for _ in range(n_opere):
            autore = random.choice(autori)
            min_anno = autore.data_nascita.year + 20
            max_anno = autore.data_nascita.year + 90
            if autore.data_morte:
                max_anno = min(max_anno, autore.data_morte.year)
            max_anno = min(max_anno, oggi)
            if min_anno > max_anno:
                min_anno = max_anno - 1
            anno_realizzazione = random.randint(min_anno, max_anno)
            anno_acquisto = random.randint(anno_realizzazione, oggi)

            opere.append(
                Opera(
                    autore=autore,
                    titolo=fake.sentence(nb_words=3),
                    anno_realizzazione=anno_realizzazione,
                    anno_acquisto=anno_acquisto,
                    tipo=random.choice([Opera.QUADRO, Opera.SCULTURA]),
                    esposta_in_sala=random.choice(sale) if random.random() < 0.7 else None,
                )
            )
        self._bulk_save(Opera, opere)
        self.stdout.write(self.style.SUCCESS("✓ Popolamento completato"))

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

    def _bulk_save(self, model, objs):
        if not objs:
            return []
        with transaction.atomic():
            for chunk in _grouper(objs, CHUNK):
                model.objects.bulk_create(chunk)
        return list(model.objects.filter(pk__in=[o.pk for o in objs]))

