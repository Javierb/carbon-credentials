from django.db import models
from django.utils.translation import gettext_lazy as _


class Building(models.Model):
    name = models.CharField(max_length=70, verbose_name=_('name'))

    def __str__(self):
        return f"{self.id} - {self.name}"

    class Meta:
        db_table = 'buildings'
        verbose_name = _('building')
        verbose_name_plural = _('buildings')


class Meter(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, verbose_name=_('building'))
    fuel = models.CharField(max_length=50, verbose_name=_('fuel'))
    unit = models.CharField(max_length=5, verbose_name=_('unit'))

    def __str__(self):
        return f"{self.id} - {self.fuel} : {self.unit}"

    class Meta:
        db_table = 'meters'
        verbose_name = _('meter')
        verbose_name_plural = _('meters')


class Energy(models.Model):
    consumption = models.FloatField(verbose_name=_('consumption'))
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, verbose_name=_('meter'))
    reading_date_time = models.DateTimeField(verbose_name=_('reading date'))

    def __str__(self):
        return f"{self.id} - {self.consumption} : {self.reading_date_time}"

    class Meta:
        db_table = 'energy'
        verbose_name = _('energy')
        verbose_name_plural = _('energy')
        unique_together = ['meter', 'reading_date_time']

