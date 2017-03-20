from django.contrib.auth.models import User
from .models import *
from django import  forms

class SystemUserForm(forms.ModelForm):
	class Meta:
		model  = SystemUser
		fields = ('first_name','middle_name','last_name','sex','birthday','age','tel','address')

class UserForm(forms.ModelForm):
	class Meta:
		model  = Users
		fields = ('hospitalID','username','email','password','question','answer','employee_agreement_file')	

class PractitionerForm(forms.ModelForm):

	class Meta:
		model  = Practitioner
		fields = ('status','pos')

class PatientForm(forms.ModelForm):

	class Meta:
		model  = Patient
		fields = ('gestation',)

			
class GsmDeviceForm(forms.ModelForm):

	class Meta:
		model  = GsmDevice
		fields = ('device_id','status')	







	
