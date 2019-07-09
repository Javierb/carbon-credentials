from django.test import TestCase
from django.utils import timezone
from django.db.utils import IntegrityError
from django.utils import timezone, dateparse
from .models import Building, Meter, Energy


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

