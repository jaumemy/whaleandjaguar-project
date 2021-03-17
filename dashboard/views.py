from django.shortcuts import render

# Create your views here.



def dashboard(request):

    dashboard = 'This is the dashboard'

    context = {
        'dashboard': dashboard,
    }

    return render(request, 'dashboard.html', context=context)
