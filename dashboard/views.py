from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import create_user_form
import time, json, requests

# Create your views here.


@login_required
def dashboard(request, pk):

    url = "https://covid-19-data.p.rapidapi.com/report/totals"


    headers = {
        'x-rapidapi-key': "029a770d4dmsh68cc1833d5b39c4p1c6abbjsn4b81f652ec8f",
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }


    # Fechas ficticias de última semana debido al mal funcionamiento de la API
    # En situación normal se hubiera usado la librería datetime para las fechas

    querystring_sevendaysago = {"date":"2020-08-02"}
    querystring_currentdate = {"date":"2020-08-09"}

    response_sevendaysago = requests.request(
        "GET", url, headers=headers, params=querystring_sevendaysago).json()

    time.sleep(1)

    response_currentdate = requests.request(
        "GET", url, headers=headers, params=querystring_currentdate).json()

    response_week = {}

    for key in response_currentdate[0]:
        if key == "date":
            pass
        else:
            response_week[key] = int(response_currentdate[0][key]) - int(response_sevendaysago[0][key])

    confirmados = response_week["confirmed"]
    recuperados = response_week["recovered"]
    muertes = response_week["deaths"]
    activos = response_week["active"]
    criticos = response_week["critical"]


    context = {
        'confirmados': confirmados,
        'recuperados': recuperados,
        'muertes': muertes,
        'activos': activos,
        'criticos': criticos,
        'pk': pk,
    }

    return render(request, 'dashboard.html', context=context)



def register_page(request):

    form = create_user_form()

    if request.method == "POST":
        form = create_user_form(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request,'Cuenta creada para '+username)

            return redirect('login')

    context = {
        'form': form
    }

    return render(request, 'registration/register.html', context)
