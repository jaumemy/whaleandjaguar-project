from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import create_user_form

# Create your views here.


@login_required
def dashboard(request):

    dashboard = 'This is the dashboard'

    context = {
        'dashboard': dashboard,
    }

    return render(request, 'dashboard.html', context=context)



def register_page(request):

    form = create_user_form()

    if request.method == "POST":
        form = create_user_form(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request,'Account created for '+username)

            return redirect('login')

    context = {
        'form': form
    }

    return render(request, 'registration/register.html', context)
