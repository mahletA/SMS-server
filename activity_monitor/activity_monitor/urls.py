"""activity_monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from Activity_Monitor.views import *



	

urlpatterns = [
   
    url(r'^admin/', admin.site.urls),
    url(r'^admin_login/$', admin_login),
    url(r'^admin_home/$', admin_dashboard),
    url(r'^admin_dashboard/add_user/$', admin_dashboard_add_user ),
    url(r'^admin_dashboard/add_patient/$', admin_dashboard_add_patient ),
    url(r'^admin_dashboard/add_gsm/', admin_dashboard_add_gsm ),


    url(r'^admin_logout/$' , admin_logout),


    url(r'^home/$', main_page),
    url(r'^contact/$', contact),
   
    url(r'^dashboard/$', dashboard),
    url(r'^list/$', dashboard_table),
    url(r'^report/$', dashboard_report),
    url(r'^chosenreport/$', dashboard_chosenreport),
  
  
    
    url(r'^user_login/$', user_login),
    url(r'^user_login/forgot_password.html/$', forgot_password),
    url(r'^user_login/forgot_password.html/forgot_password_another.html$', forgot_password_another),
    url(r'^user_logout/$' , user_logout),
    
    

    #url(r'^dashboard/dashboard/(?P<user>[0-9]+)/', dashboard, name='dashboard'),  

]

