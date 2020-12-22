from django.urls import path,include
from . import views

urlpatterns=[
    path('control/',views.control),
    path('baoming/',views.baoming)
]