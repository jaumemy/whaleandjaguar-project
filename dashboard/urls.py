from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('<str:pk>', views.dashboard, name='dashboard'),
    path('register/', views.register_page, name="register"),
]
