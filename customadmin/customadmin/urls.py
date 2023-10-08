"""
URL configuration for crudajax project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import URLPattern, path , include
from users import views
from django.conf import settings
from django.conf.urls.static import static


 #if settings.DEBUG:
  #  URLPattern+=static(settings.MEDIA_URL,
  #                     document_root=settings.MEDIA_ROOT)



urlpatterns = [
    path('admin/', admin.site.urls),

    #profile
    path('',views.home , name ="home"),

    #login function
    path('login/',views.login_page,name="login"),

    #register function
    
    

    path('Register/',views.register,name="signup"),


    #logout function
    path('logout/',views.logout_page,name="logout_page"),
    path('add/',views.adddata,name="add"),

    path('davidadmin/',views.alldata,name="alldata"),
    path('details/<int:id>/',views.details,name="details"),

    #admin pannel ka kaam 

   # path('dj-admin/', include('customadmin.urls')),

   path('update/',views.update,name="update"),

   

   #excel download
  # path('download_excel/', views.download_excel, name='download_excel'),

  #approve data

  path('app/',views.app_login,name="applogin"),

  path('history/<int:id>',views.history,name="history"),

  #download excel file

 # path('excell/',views.download_excel,name="excel"),

]

if settings.DEBUG:
  urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

