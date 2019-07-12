from django.test import TestCase
from django.utils import timezone
from django.db.utils import IntegrityError
from django.utils import timezone, dateparse
from .models import Building, Meter, Energy
from import_export import resources
from tablib import Dataset
from .admin import MeterResource, BuildingsResource, EnergyResource
import os
from .tasks import import_file_task
from django.db import transaction


class BaseBuildingTestCase(TestCase):
    def setUp(self):
        self.dt = timezone.make_aware(dateparse.parse_datetime('2018-12-01 00:00'))
        self.building = Building.objects.create(name="Empire State")
        self.meter = Meter.objects.create(building=self.building, fuel='Gas', unit='kWh')
        self.halfhour = Energy.objects.create(meter=self.meter, consumption=44.835, reading_date_time=self.dt)


class BuildingTestCase(BaseBuildingTestCase):

    def test_halfhourly_integrity(self):
        other_halfhour = Energy(meter=self.meter, consumption=44.835, reading_date_time=self.dt)
        with self.assertRaises(IntegrityError):
            other_halfhour.save()

    def test_import_buildings(self):
        csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv/building_data.csv')
        meter_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv/meter_data.csv')
        energy_csv = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv/halfhourly_data.csv')

        with transaction.atomic():
            import_file_task(csv_path, 'building')
            import_file_task(meter_csv, 'meter')
            import_file_task(energy_csv, 'energy')

        self.assertEqual(31, Building.objects.count())
        self.assertEqual(118, Meter.objects.count())
        self.assertEqual(92295, Energy.objects.count())

    

