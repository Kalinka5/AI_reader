from django import forms
from .models import UploadedPDF


class UploadMultiplePDFForm(forms.ModelForm):
    pdf_files = forms.FileField(widget = forms.TextInput(attrs={
            "name": "images",
            "type": "File",
            "class": "form-control",
            "multiple": "True",
        }), label = "")
    class Meta:
        model = UploadedPDF
        fields = ['pdf_files']
    