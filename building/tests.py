from django.test import TestCase
from django.utils import timezone
from django.db.utils import IntegrityError
from django.utils import timezone, dateparse
from .models import Building, Meter, Energy
from import_export import resources
from tablib import Dataset
import os



class BaseBuildingTestCase(TestCase):
    def setUp(self):
        self.dt = timezone.make_aware(dateparse.parse_datetime('2018-12-01 00:00'))
        self.building = Building.objects.create(name="Empire State")
        self.meter = Meter.objects.create(building=self.building, fuel='Gas', unit='kWh')
        self.halfhour = Energy.objects.create(meter=self.meter, consumption=44.835, reading_date_time=self.dt)


class BuildingTestCase(BaseBuildingTestCase):

    # def test_halfhourly_integrity(self):
    #     other_halfhour = Energy(meter=self.meter, consumption=44.835, reading_date_time=self.dt)
    #     with self.assertRaises(IntegrityError):
    #         other_halfhour.save()

    def test_csv_import(self):
        csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv/building_data.csv')
        building_resource = resources.modelresource_factory(model=Building)()
        building_dataset = Dataset().load(open(csv_path).read())
        result = building_resource.import_data(building_dataset)
        self.assertEqual(result.has_errors(), False)

        csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv/meter_data.csv')
        meter_resource = resources.modelresource_factory(model=Meter)()
        meter_dataset = Dataset().load(open(csv_path).read())
        result = meter_resource.import_data(meter_dataset, dry_run=False)
        self.assertEqual(result.has_errors(), False)

        csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csv/halfhourly_data.csv')
        energy_resource = resources.modelresource_factory(model=Energy)()
        energy_dataset = Dataset().load(open(csv_path).read())
        result = energy_resource.import_data(energy_dataset, dry_run=False)
        self.assertEqual(result.has_errors(), False)
    

