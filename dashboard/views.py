from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import create_user_form
import time, json, requests
from google_trans_new import google_translator

# Create your views here.


@login_required
def dashboard(request):

    # Obtener Lista de países para seleccionar

    url_allcountries = "https://covid-19-data.p.rapidapi.com/help/countries"

    headers = {
        'x-rapidapi-key': "029a770d4dmsh68cc1833d5b39c4p1c6abbjsn4b81f652ec8f",
        'x-rapidapi-host': "covid-19-data.p.rapidapi.com"
        }

    response_allcountries = requests.request(
        "GET", url_allcountries, headers=headers).json()

    time.sleep(1)

    list_of_countries = []

    for ele in response_allcountries:
         list_of_countries.append(ele['name'])



    # Mostrar información del país seleccionado

    context_selected_country = {}

    if request.method == "POST":

        # Obtener id de 2 digitos de la elección del usuario

        selected_country = request.POST['selected_country']

        for ele in response_allcountries:
            if selected_country == ele["name"]:
                selected_country_id = ele["alpha2code"]


        # getLatesCountryDataByCode

        url_countrydata = "https://covid-19-data.p.rapidapi.com/country/code"

        querystring_countrydata = {"code":selected_country_id}

        response_countrydata = requests.request(
            "GET", url_countrydata, headers=headers, params=querystring_countrydata).json()

        time.sleep(1)


        # getDailyReportByCountryCode ( Desde la última fecha actualizada en el endpoint)

        url_countrydaily = "https://covid-19-data.p.rapidapi.com/report/country/code"

        querystring_countrydaily = {"date":"2020-06-16","code":selected_country_id}

        response_countrydaily = requests.request(
            "GET", url_countrydaily, headers=headers, params=querystring_countrydaily).json()

        time.sleep(1)


        # Obtención datos de response

        confirmados_total_pais = response_countrydata[0]["confirmed"]
        recuperados_total_pais = response_countrydata[0]["recovered"]
        criticos_total_pais = response_countrydata[0]["critical"]
        muertes_total_pais = response_countrydata[0]["deaths"]

        confirmados_dia_pais = response_countrydaily[0]["provinces"][0]["confirmed"]
        recuperados_dia_pais = response_countrydaily[0]["provinces"][0]["recovered"]
        muertes_dia_pais = response_countrydaily[0]["provinces"][0]["deaths"]
        activos_dia_pais = response_countrydaily[0]["provinces"][0]["active"]

        # Traducción del país al español

        translator = google_translator()
        nombre_pais = translator.translate(selected_country, lang_src="en", lang_tgt="es")



        context_selected_country = {
            'nombre_pais': nombre_pais,
            'confirmados_total_pais': confirmados_total_pais,
            'recuperados_total_pais': recuperados_total_pais,
            'criticos_total_pais': criticos_total_pais,
            'muertes_total_pais': muertes_total_pais,
            'confirmados_dia_pais': confirmados_dia_pais,
            'recuperados_dia_pais': recuperados_dia_pais,
            'muertes_dia_pais': muertes_dia_pais,
            'activos_dia_pais': activos_dia_pais,
        }



    # Obtener datos globales en los últimos siete días para mostrar

    url = "https://covid-19-data.p.rapidapi.com/report/totals"


    # Fechas ficticias de última semana que coincide con getDailyReportByCountryCode
    #   para dar la información a 16 de junio del 2020
    # La última fecha para este endpoint sería el 2 de agosto del 2020
    # En situación normal se hubiera usado la librería datetime para las fechas

    querystring_sevendaysago = {"date":"2020-06-09"}
    querystring_currentdate = {"date":"2020-06-16"}

    response_sevendaysago = requests.request(
        "GET", url, headers=headers, params=querystring_sevendaysago).json()

    time.sleep(1)

    response_currentdate = requests.request(
        "GET", url, headers=headers, params=querystring_currentdate).json()

    time.sleep(1)

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
        'response_allcountries': response_allcountries,
        'list_of_countries': list_of_countries,
    }


    context.update(context_selected_country)

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
