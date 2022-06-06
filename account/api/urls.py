from django.urls import path

from . import views


urlpatterns = [
    path('<str:org>/login/',views.login_view,name='servicelogin')
]
