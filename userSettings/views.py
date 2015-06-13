from django.shortcuts import render
from forms import UserSettingsForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from userSettings.models import UserSettings

from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator


#@login_required
class changeSettings(UpdateView):
        
    model = UserSettings
    fields = ['email_Feeds_To','feed_Format']
    template_name_suffix = '_change'

#http://stackoverflow.com/questions/15215295/how-to-use-current-logged-in-user-as-pk-for-django-detailview
    def get_object(self):
        return UserSettings.objects.get_or_create(user=self.request.user)[0]

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(changeSettings, self).dispatch(*args, **kwargs)

def loginToChangeSettings():
    return render(request,'userSettings/loginToChangeSettings.html')       


    #http://stackoverflow.com/questions/14422651/grabbing-current-logged-in-user-with-django-class-views

#http://pydanny.com/the-easy-form-views-pattern-controversy.html                
'''
def changeSettings(request):
    if request.user == None or request.user.is_anonymous():
        return render(request,'userSettings/loginToChangeSettings.html')

    elif request.method == 'GET':
        form = UserSettingsForm()
    else:
        form = UserSettingsForm(request.POST)
        if form.is_valid():
            # temp is used to create object we can assign a user attr to
            temp = form.save(commit=False)
            temp.user = request.user
            temp.save()
            return HttpResponseRedirect(reverse('home'))

    return render(request, 'userSettings/changeSettings.html', {
        'form': form,
        })
'''

