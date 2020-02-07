from django import forms

from map_quest.models import Dataset


class DatasetForm(forms.ModelForm):

    class Meta:
        model = Dataset
        fields = '__all__'
