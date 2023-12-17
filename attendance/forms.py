# forms.py
from django import forms
from .models import EmployeeRecord, FileUpload


class FilterForm(forms.Form):
    filter_name = forms.CharField(required=False, label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Filter by Name'}))
    filter_id = forms.CharField(required=False, label="", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Filter by Employee ID'}))
    from_date = forms.DateField(required=False, label="", widget=forms.widgets.DateInput(
        attrs={'class': 'form-control',
               'placeholder': 'From Date', 'type': 'date'}
    ))
    to_date = forms.DateField(required=False, label="", widget=forms.widgets.DateInput(
        attrs={'class': 'form-control',
               'placeholder': 'To Date', 'type': 'date'}
    ))


class RemarkForm(forms.ModelForm):
    class Meta:
        model = EmployeeRecord
        fields = ["em_id", "name", "role", "remark"]
        widgets = {"em_id": forms.TextInput(
            attrs={'class': 'form-control', 'label': "", 'placeholder': 'Employee ID'}),
            "name": forms.TextInput(
            attrs={'class': 'form-control', 'label': "", 'placeholder': 'Employee Name'}),
            "role": forms.TextInput(
            attrs={'class': 'form-control', 'label': "", 'placeholder': 'Designation'}),
            "remark": forms.TextInput(
            attrs={'class': 'form-control', 'label': "", 'placeholder': 'Remark for Clocking'})}


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ['file']
