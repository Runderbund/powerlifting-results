from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    date = forms.DateField()
    file = forms.FileField()
