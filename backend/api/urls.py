from django.urls import path
from . import views


urlpatterns = [
    path('emailscan/',views.emailscan),
    path('phishurl/',views.philurl)
]