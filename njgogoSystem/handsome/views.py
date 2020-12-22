from django.shortcuts import render
from .form import *

# Create your views here.
def control(request):
    user01='handsome'

    user01dic={'user01':user01}
    return render(request,'handsome/control.html',user01dic)

def baoming(request):

    # if request.method=='get':
    return render(request,'handsome/baoming.html')