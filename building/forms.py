from django import forms
from django.apps import apps
from django.utils.translation import gettext_lazy as _

models = apps.get_app_config('building').models.keys()
MODEL_CHOICES = tuple(zip(models, models))

class UploadFileForm(forms.Form):   
    file = forms.FileField(label=_('File'))
    model = forms.ChoiceField(label=_('Model'),
                                initial='',
                                widget=forms.Select(),
                                required=True, choices=MODEL_CHOICES)
