from django.apps import apps
from .resources import BuildingsResource, MeterResource, EnergyResource
from tablib import Dataset
import logging
from itertools import islice
from .models import Energy
from django.apps import apps
import csv
from django.db import IntegrityError

logger = logging.getLogger(__name__)


class DataImporter:

    BATCH_SIZE = 100
    
    def __init__(self, model):
        self.model = model
        self.this_app = apps.get_app_config('building')

        if model.lower() in self.this_app.models.keys():
            if model == 'building':
                self.resource = BuildingsResource
            elif model == 'meter':
                self.resource = MeterResource
            else:
                self.resource = EnergyResource

    @classmethod
    def match_data_model(cls, file, app_name,  model_name):
        with open(file, 'r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='|')
            # Clean up BOM from the header
            headers = cls.clean_row([h.encode('utf-8').decode('utf-8-sig') for h in next(reader)])
            class_model = apps.get_model(app_label=app_name, model_name=model_name)
            row = cls.clean_row(next(reader))
       
        # object_dict = {key: value for key, value in zip(headers, filter(None, next(data_sample)))}
        object_dict = {key: value for key, value in zip(headers, row)}

        try:
            class_model(**object_dict)

        except TypeError:
            return False

        return True

    @classmethod
    def clean_row(cls, row):
        return list(filter(None, row))

    def skip_instance(self, instance):
        for field in instance._meta.fields:
            # Id fields can be blank in creation scenarios.
            if field.name != 'id':
                val = field.value_from_object(instance)
                if field.blank and val is None or val == '':
                    return True
        return False

    def import_file(self, file):
        logger.info(f'Importing data from the file: {file}')
        with open(file, 'r') as f:
            reader = csv.reader(f, delimiter=',', quotechar='|')
            
            # Clean up BOM from the header
            headers = self.clean_row([h.encode('utf-8').decode('utf-8-sig') for h in next(reader)])
            class_model = apps.get_model(app_label=self.this_app.name, model_name=self.model)
            
            objs = []
            try:
                for row in reader:
                    cleaned_row = self.clean_row(row)
                    object_dict = {key: value for key, value in zip(headers, cleaned_row)}
                    instance = class_model(**object_dict)
                    if not self.skip_instance(instance):
                        objs.append(instance)
                    if len(objs) == self.BATCH_SIZE:
                        class_model.objects.bulk_create(objs, self.BATCH_SIZE, ignore_conflicts=True)
                        objs = []
                    
                if len(objs) > 0:
                    class_model.objects.bulk_create(objs)
            except IntegrityError as e:
                logger.error(f'The file {file} has already been imported and can\'t be imported again.')
            except Exception as e:
                logger.error(e)
