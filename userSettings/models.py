from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    user = models.OneToOneField(User,primary_key=True)
    email_Feeds_To = models.CharField(max_length=100)
    
 
    PDF = "p"
    EPUB = "e"
    TXT = "t"
    FEED_FORMAT_CHOICES = (
        (PDF,"PDF"),
        (EPUB,"Epub"),
        (TXT,'Plain Text'),
        )

    feed_Format = models.CharField(max_length=1, choices = FEED_FORMAT_CHOICES, default = PDF)
   
#User.profile = property(lambda u: UserSettings.objects.get_or_create(user=u)[0])
