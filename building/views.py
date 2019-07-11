
from django.views.generic import TemplateView
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



class IndexView(TemplateView):
    template_name = "building/index.html"
    

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
                
            print(valid_data)
            if valid_data:
                # Async task to import the data.
                import_file_task.delay(file_path, model_name)

                # handle_uploaded_file(request.FILES['file'], request.POST['model'])
                messages.info(request, 'We are importing the data! It will be available shortly.')
            else:
                messages.warning(request, 'The data structure doesn\'t match with the selected model.')

            return render(request, 'building/upload.html', {'form': form})
    else:
        form = UploadFileForm()
    return render(request, 'building/upload.html', {'form': form})
