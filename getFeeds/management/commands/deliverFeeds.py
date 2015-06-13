from django.core.management.base import NoArgsCommand
from getFeeds.downloadFeeds import getEveryUsersFeeds

class Command(NoArgsCommand):
    help = "Delivers each of the users' feeds to them."
    
    def handle_noargs(self,**options):
        getEveryUsersFeeds()
