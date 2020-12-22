from django.urls import path,include
from . import views

app_name='mainIndex'
urlpatterns=[
    path('login/',views.logined,name='logined'),
    path('createuser/',views.createuser,name='createuser'),
    path('baoming/(?P<user>\d+)/$',views.baoming,name='baoming'),
    path('^control/(?P<user>\d+)/$',views.control,name='control'),
    path('logout/',views.logout_view,name='logout_view'),
    path('success/(?P<id>\d+)/$',views.baomingsuccess,name='baomingsuccess'),
    path('export/(?P<user>\d+)/$',views.export,name='export'),
    path('savematch/',views.savematch,name='savematch'),
    path('lufen/(?P<BMid>\d+)/$',views.lufen,name='lufen'),
    path('upload/',views.uploadbifen,name='uploadbifen'),
    path('jifenbiao/(?P<BMid>\d+)/$',views.printjifenbiao,name='printjifenbiao'),
    path('savecaipan/',views.savecaipan,name='savecaipan'),

]