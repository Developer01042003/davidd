import os
from pydoc import tempfilepager
import tempfile
from django.conf import settings
from django.shortcuts import redirect, render ,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
from openpyxl import Workbook
from requests import request
from django.http import FileResponse, HttpResponse , JsonResponse
import pandas as pd


import users



from .models import FormSubmission,BaseModel
from django.views.decorators.csrf import csrf_exempt



# Create your views here.
def login_page(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username ,password=password )

        if user is not None:
           login(request,user)
           return redirect('/')
    
        else :
            message = "something wrong with your account"

            return render(request,'login.html' ,{ 'message' : message ,})


    return render(request,"login.html")



def register(request):
    if request.method=="POST":
     
      username = request.POST['username']
      email = request.POST['email']
      password = request.POST['password']

      if User.objects.filter(username=username).exists():
        
        return render( request,'login.html')
      else:
        User_object = User.objects.create(
           username = username ,
           email = email )
        User_object.set_password(password)
        User_object.save()

        return render(request,"login.html")
      
    
    
    return render(request,"register.html")


    
        

    
    


@login_required(login_url='login/')
def home(request):
    return render(request,"home.html")



@login_required(login_url='login/')
def adddata(request):

    campname = BaseModel.objects.all()

    

    if request.method =="POST":
           camp = request.POST['campname']

           cbb = BaseModel.objects.get(campname=camp)

        
           
           cashback = cbb.cashback
        # Create a new FormSubmission instance and associate it with the logged-in user
           create_capm = FormSubmission.objects.create(
            user  =request.user,
            campname = request.POST['campname'],
            idname = request.POST['idname'],
            amount = request.POST['amount'],
            image = request.FILES['filename'],
            cashback = cashback,
            )
           create_capm.save()
        # Add code to handle and save other form data to the FormSubmission model
        # form_submission.field_name = request.POST['field_name']
        

    return render(request,"add.html", {"campname":campname})
    
    
@login_required(login_url='applogin')
def alldata(request):

   
        get_data = User.objects.all()



        return render(request,"alldata.html",{"data":get_data})

@login_required(login_url='applogin')
def details(request,id):
    if id:
        #userr = User.objects.filter(id=id)

        camp = FormSubmission.objects.filter(user_id=id)

        camps = camp.all()

  
        return render(request,"detail.html",{"camps":camps})

@csrf_exempt
@login_required(login_url='applogin')
def update(request):
    if request.method=="POST":
        id = request.POST['dataId']

        campu = FormSubmission.objects.get(pk=id)

        campu.approve = True

        campu.save()

        return JsonResponse({'status':1})
    
    else:
        return JsonResponse({'status':0})


def app_login(request):

    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request , username=username ,password=password )

        if user is not None :
           
           if user.is_staff: 
              login(request,user)
              return redirect(alldata)
           
           else:
               return HttpResponse("You are not an admin")
        

    return render(request,"alogin.html")    

def logout_page(request):
    logout(request)
    return redirect('/')

@login_required(login_url='login')
def history(request,id):

    user = User.objects.filter(pk=id)
    
    if user:
       campu = FormSubmission.objects.filter(
        user=id
       )

       camp = campu.all()

       return render(request,"history.html",{'camp':camp})
    else:
        return HttpResponse("Some error occured")
    
'''
def download_excel(request):

    objs = FormSubmission.objects.all()
    
    data = []

    for obj in objs:
        data.append({
            'Campaign Name' : obj.campname,
            'username':obj.idname,
            'deposit':obj.amount,
            'cashback':obj.cashback,
            'date':obj.date,

        })

    pd.DataFrame(data).to_excel("output.xlsx")   

    return JsonResponse({
        'status':200
    })  '''


from django.http import FileResponse
import pandas as pd
from io import BytesIO

