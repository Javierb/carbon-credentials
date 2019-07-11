# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .importer import DataImporter

@shared_task
def import_file_task(file_path, model_type):
    importer = DataImporter(model_type)
    importer.import_file(file_path)


