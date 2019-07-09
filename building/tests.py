from django.test import TestCase
from django.db.utils import IntegrityError
from .models import Building, Meter, Energy


class BaseBuildingTestCase(TestCase):
    def setUp(self):
        self.building = Building.objects.create(name="Empire State")
        self.meter = Meter.objects.create(building=self.building, fuel='Gas', unit='kWh')
        self.halfhour = Energy.objects.create(meter=self.meter, consumption=44.835, reading_date_time='2018-12-01 00:00')


class BuildingTestCase(BaseBuildingTestCase):
    def test_halfhourly_integrity(self):
        print(type(self.meter))
        other_halfhour = Energy(meter=self.meter, consumption=44.835, reading_date_time='2018-12-01 00:00')
        with self.assertRaises(IntegrityError):
            other_halfhour.save()

