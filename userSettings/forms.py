from django.forms import ModelForm
from userSettings import models


class UserSettingsForm(ModelForm):
#    captcha = ReCaptchaField(use_ssl=True)

    class Meta:
        model = models.UserSettings
        exclude = ['user']
        


