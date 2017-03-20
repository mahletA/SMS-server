from django.template import RequestContext, loader
from django.shortcuts import render,render_to_response
from django.template.loader import render_to_string

from django.template import Context
from django.template.loader import get_template

from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms  import *
from .models import *

import hashlib
import random
import base64
import csv
import os
import math
import datetime

from django.contrib.auth import get_user_model as user_model
#import pdfkit

def hashSSHA(password):
	salt = hashlib.sha1(str(random.getrandbits(32))).hexdigest()
	salt = salt[:10]
	encrypted  = base64.b64encode(hashlib.sha1(password+salt).hexdigest()+salt)
	my_hash = {"salt":salt,"encrypted":encrypted}
	return my_hash	

def checkhashSSHA(salt,password):
	my_hash =  base64.b64encode(hashlib.sha1(password+salt).hexdigest()+salt)		
	return my_hash

def authenticate_user(username,password):
	user  = Users.objects.get(email=username)
	print user.email
	print user.password
	if user == None:return None
	if(user.password in checkhashSSHA(user.salt,password)):return user
	else:return None


"""########################### ADMIN #######################"""

def admin_login(request):
	# Like before, obtain the context for the user's request.
	context = RequestContext(request)
	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
	# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		username = request.POST.get('username', "Null")
		password = request.POST.get('password',"Null")

		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)
	  	if user is not None:
			# Is the account active? It could have been disabled.
			if user.is_active:
				login(request, user)
			
				return HttpResponseRedirect('/admin_dashboard/dashboard/')
			else:
			
				return HttpResponse("Your Rango account is disabled.")
		else:

			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")

	else:
		return render(request,'admin_login.html',{})



def admin_dashboard(request):
	return render(request, "admn.html", {})



def admin_dashboard_add_user(request):
#TODO do the template properly
	context = RequestContext(request)
	registered = False
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		systemuser_form = SystemUserForm(data=request.POST)
		practitioner_form=PractitionerForm(data=request.POST)
		print (user_form)
		print (systemuser_form)
		print (practitioner_form)
		print user_form.is_valid()
		print systemuser_form.is_valid()
		print practitioner_form.is_valid()
		if user_form.is_valid() and systemuser_form.is_valid():
			
			user = user_form.save(commit=False)
			systemuser =systemuser_form.save(commit=False)

			#if 'photo' in request.FILES:

			#systemuser.photo = request.FILES['photo']

			systemuser.save()			
			user.systemuser = systemuser
			

			my_hash = hashSSHA(user.password)
			user.password = my_hash['encrypted']
			user.salt     = my_hash['salt']
			user.save()
			if practitioner_form.is_valid():
				prac=practitioner_form.save(commit=False)
				prac.user=user
				prac.save()

			django_user = User.objects.create_user(username=user.username,
                                 email=user.email,
                                 password=user.password)
			#my_user = Users.objects.create(hospitalID=user.hospitalID,username=user.username,email=user.email,password=user.password)
			django_user.save()
			registered = True
		else:
			
			print user_form.errors, systemuser_form.errors
	else:
		user_form = UserForm()
		systemuser_form = SystemUserForm()
# Render the template depending on the context.
	return render(request,'admin_new_new.html',{'registered':registered})

def admin_dashboard_add_patient(request):
#TODO do the template properly
	context = RequestContext(request)
	registered = False
	practitioners = Practitioner.objects.filter(status=Practitioner.PRAC_STATUS[1][0])
	for practitioner in practitioners:
		print practitioner.user.username

	gsms = GsmDevice.objects.filter(status=GsmDevice.GSM_STATUS[0][0])
	for gsm in gsms:
		print gsm.device_id

	if request.method == 'POST':
		print request.POST
		patient_form = PatientForm(data=request.POST)
		systemuser_form = SystemUserForm(data=request.POST)
		print (patient_form)
		print (systemuser_form)
		print patient_form.is_valid()
		print systemuser_form.is_valid()
		if patient_form.is_valid() and systemuser_form.is_valid():
	
			user = patient_form.save(commit=False)
			systemuser =systemuser_form.save(commit=False)

			#if 'photo' in request.FILES:

			#systemuser.photo = request.FILES['photo']

			systemuser.save()			
			user.systemuser = systemuser
			if 'assign' in request.POST and 'pair' in request.POST:
				if request.POST['assign']!='':
					print request.POST['assign']
					try:
						
						practitioner  = Practitioner.objects.get(id=request.POST['assign'])#if not assigned yet
						print practitioner.id
												
					except:
				
						print "can't get assign values!"
				if request.POST['pair']!='':
					print request.POST['pair']
					try:
						
						gsm = GsmDevice.objects.get(device_id=request.POST['pair'])#if not assigned yet
						print gsm.device_id
						
					except:
				
						print "can't get pair values!"
					#user.gsm_id=gsm.device_id
					#user.save()
					django_user = Patient.objects.create(gestation=user.gestation,
					                 status=user.status,practitioner_id=practitioner.id,gsm_id=gsm.device_id
					                 )
					#my_user = Users.objects.create(hospitalID=user.hospitalID,username=user.username,email=user.email,password=user.password)
					django_user.save()

					registered = True
		else:
			
			print patient_form.errors, systemuser_form.errors
	else:
		user_form = UserForm()
		systemuser_form = SystemUserForm()
# Render the template depending on the context.
	return render(request,'admin_new_patient.html',{'practitioners':practitioners,'gsms':gsms,'registered':registered})
def admin_dashboard_add_gsm(request):
#TODO do the template properly
	context = RequestContext(request)
	registered = False
	
	if request.method == 'POST':
		gsmdevice_form = GsmDeviceForm(data=request.POST)
		
		print (gsmdevice_form)
		print gsmdevice_form.is_valid()

		if gsmdevice_form.is_valid() :
			gsmm  = GsmDevice.objects.create(device_id=request.POST['device_id'], status = GsmDevice.GSM_STATUS[0][0])#active and not being used
		
			gsmm.save()
			#gsmm = gsmdevice_form.save(commit=False)
			#gsmm.device_id = device_id 
			#gsmm.status = status
			#gsmm.save()
			
			registered = True
		else:
			
			print gsmdevice_form.errors
	else:
		gsmdevice_form = GsmDeviceForm()
		
# Render the template depending on the context.
	return render(request,'admin_new_gsm.html',{'registered':registered})
@login_required
def admin_logout(request):
	logout(request)
	return HttpResponseRedirect('/admin_dashboard/dashboard/')

"""########################### USER #######################"""

def myview(request):
    #Retrieve data or whatever you need
    results = {}
    return render_to_pdf(
            'test.html',
            {
                'pagesize':'A4',
                'mylist': results,
            }
        )



def user_login(request):
	# Like before, obtain the context for the user's request.

	context = RequestContext(request)
	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
	        # Gather the username and password provided by the user.
		# This information is obtained from the login form.
		username = request.POST.get('username')
		password = request.POST.get('password')
		print (username)
		print (password)
		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate_user(username=username, password=password)
		print user
	  	if user is not None:
			# Is the account active? It could have been disabled.
			django_user = User.objects.get(username=user.username)
			if django_user.is_active:
				login(request,django_user)
				
				return HttpResponseRedirect('/dashboard')
			else:
			
				return HttpResponse("Your account is disabled.")
		else:

			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")

	else:
		return render(request,'user_login.html',{})

@login_required
def dashboard(request):
	return render(request,'index.html',{})

@login_required
def dashboard_table(request):
	return render(request,'tables.html',{})

@login_required
def dashboard_report(request):
	return render(request,'forms.html',{})
@login_required
def dashboard_chosenreport(request):
	return render(request,'flot.html',{})



@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/home/')

def main_page(request):
	return render(request,'main_page.html',{})
def contact(request):
	return render(request,'contact.html',{})

# def dashboard(request,user):
# 	user = User.objects.get(id=user)
# 	patient_info = {}

# 	try:	
# 		patients = Patient.objects.filter(user=user,status = Patient.VEHICLE_STATUS[0][0])#get all the active patients	
		
# 		for patient in patients:
# 			try:
# 				sms_data = SmsData.objects.get(gsm=patient.gsm)
# 				patient_info[patient]=sms_data
# 			except:
# 				print "error"
# 	except:
# 		patients = None	

# 	MEDIA_URL = '/media/'
# 	alert = False
# 	#return render(request, "my_map_with_map.html", {'user':user,'MEDIA_URL' : MEDIA_URL,'vehicle_location_pair':vehicle_location_pair,'zoom_lat':8.98927635 ,'zoom_long':38.78795788,'alert':alert})
# 	return render(request,'main_page.html',{})


def forgot_password(request):
	return render(request,'forgot_password.html',{})

def forgot_password_another(request):
	return render(request,'forgot_password_another.html',{})





