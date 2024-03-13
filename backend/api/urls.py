from django.urls import path
from . import views


urlpatterns = [
    path('emailscan/',views.emailscan),
    path('phishurl/',views.philurl),
    path('extension/',views.extension),


    path('moralis_auth/', views.moralis_auth, name='moralis_auth'),
    path('request_message/', views.request_message, name='request_message'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('verify_message/', views.verify_message, name='verify_message'),

    path('transact/<int:id>/',views.transact),
    path('gencode/',views.gencode),
    path('usersub/<int:id>/',views.usersub),

    path('subscribe/<int:id>',views.subscribe,name='subscribe')

]