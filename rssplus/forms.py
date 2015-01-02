from django import forms

class URLForm(forms.Form):
    siteUrl = forms.CharField(label='Website Address', max_length=100)
