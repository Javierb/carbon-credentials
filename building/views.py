
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .importer import DataImporter
from django.conf import settings
from .tasks import import_file_task
import os
from django.contrib import messages
from itertools import islice
from .models import Energy, Building, Meter


class BuildingListView(ListView):
    template_name = "building/index.html"
    model = Building
    paginate_by = 50


class MeterListView(ListView):
    template_name = "building/meter_list.html"
    model = Meter
    paginate_by = 50

    def get_queryset(self):
        queryset = self.model.objects.select_related('building')
        building_id = self.kwargs['building_id']
        if building_id:
            queryset = queryset.filter(building_id=building_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['building'] = Building.objects.get(pk=self.kwargs['building_id'])
        return context



class EnergyListView(ListView):
    template_name = "building/energy_list.html"
    model = Energy
    paginate_by = 500

    def get_queryset(self):
        queryset = self.model.objects.select_related('meter')
        meter_id = self.kwargs['meter_id']
        if meter_id:
            queryset = queryset.filter(meter_id=meter_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meter'] = Meter.objects.select_related('building').get(pk=self.kwargs['meter_id'])
        return context


def upload_file(request):

    def handle_uploaded_file(f):
        file_path = os.path.join(settings.MEDIA_ROOT, f.name)
        with open(file_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return file_path
        

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.cleaned_data
            model_name = form.cleaned_data['model']
            file_path = handle_uploaded_file(request.FILES['file'])
            sample = None

            valid_data = DataImporter.match_data_model(file_path, 'building', model_name)
            if valid_data:
                # Async task to import the data.
                import_file_task.delay(file_path, model_name)
                messages.info(request, 'We are importing the data! It will be available shortly.')
            else:
                messages.warning(request, 'The data structure doesn\'t match with the selected model.')

            return render(request, 'building/upload.html', {'form': form})
    else:
        form = UploadFileForm()
    return render(request, 'building/upload.html', {'form': form})
