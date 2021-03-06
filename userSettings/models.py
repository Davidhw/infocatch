from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    def getEmail(self):
        if self.email_Feeds_To =="":
            return self.user.email

    user = models.OneToOneField(User,primary_key=True)
    email_Feeds_To = models.CharField(max_length=100)
    PDF = "p"
    EPUB = "e"
    EMAIL_LINKS_BATCH = "b"
    EMAIL_LINKS_INDIVIDUALLY = "i"
    JUST_RSS = "r"
    FEED_FORMAT_CHOICES = (
        (EMAIL_LINKS_BATCH, "Email List of All The Links"),
        (EMAIL_LINKS_INDIVIDUALLY, "Email Individual Links"),
        (PDF,"Email PDF Compilation of the Links' Content"),
        (EPUB,"Email EPUB Compilation of the Links' Content"),
        (JUST_RSS,"Don't Email Links. (They'll still be available via RSS)"),
        )

    feed_Format = models.CharField(max_length=1, choices = FEED_FORMAT_CHOICES, default = EMAIL_LINKS_BATCH)
   
#User.profile = property(lambda u: UserSettings.objects.get_or_create(user=u)[0])
