from django import forms

class URLForm(forms.Form):
    siteUrl = forms.CharField(label='Website Address', max_length=100,required=True)
'''
    javascriptChoices = ((2,"Keep Javascript",),(1,"Remove Some Javascript"),(0,"Remove All Javascript"))
    keepJavascript = forms.ChoiceField(choices=javascriptChoices,label=" Website Javascript")

'''
