from django.shortcuts import render
from forms import UserSettingsForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


# Create your views here.

#http://pydanny.com/the-easy-form-views-pattern-controversy.html                
#@login_required
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


