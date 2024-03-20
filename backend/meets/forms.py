from django import forms

class UploadFileForm(forms.Form):
    meetName = forms.CharField(max_length=255)
    meetDate = forms.DateField()
    resultsFile = forms.FileField()
