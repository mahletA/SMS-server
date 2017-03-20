from __future__ import unicode_literals

from django.db import models

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, UserManager ,PermissionsMixin


# Create your models here.
class SystemUser(models.Model):

	GENDER_CHOICES = (
	(u'M', u'Male'),
	(u'F', u'Female'),
	)
	first_name   = models.CharField(max_length=50)
	middle_name  = models.CharField(max_length=50)
	last_name    = models.CharField(max_length=50)
	sex	         = models.CharField(max_length=2,choices=GENDER_CHOICES)
	birthday     = models.DateField(blank=True)
	age 	     = models.CharField(max_length=3)
	tel	         = models.CharField(max_length=14)
	address	     = models.TextField()
	#photo        = models.ImageField(upload_to ='profile_images',blank = True)
	reg_date     = models.DateField(auto_now_add=True)


	def __unicode__(self):
		return u'%s' '%s' % (self.first_name, self.last_name)

class Users(models.Model):
	#objects = UserManager()

	#user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	#REQUIRED_FIELDS = ('',)
	SystemUser   = models.ForeignKey(SystemUser,null=True)
	hospitalID   = models.CharField(max_length=30,primary_key=True)
	username     = models.CharField(max_length=30,unique=True,null = True)
	email        = models.EmailField(blank=False,unique=True)
	password     = models.CharField(max_length=30)
	salt         = models.CharField(max_length=10)
	question     = models.TextField()
	answer	     = models.TextField()

	employee_agreement_file = models.FileField(upload_to = 'agreement_files',blank = True) 
	created_date = models.DateField(auto_now_add=True)
	update_date  = models.DateField(auto_now_add=True)
	# USERNAME_FIELD = 'username'
	# is_authenticated="True"
	# is_anonymous="True"


class Practitioner(models.Model):
	
	PRAC_POS = (('D','doctor'),('N','nurse'),)
	PRAC_STATUS      = (('A','assigned'),('D','not assigned'),)

	user   = models.ForeignKey(Users,null=True)
	status = models.CharField(max_length=2,choices=PRAC_STATUS)
	pos    =  models.CharField(max_length=2,choices=PRAC_POS)

	def deassign(self):
		self.status = self.PRAC_STATUS[1][0];
	def assign(self):
		self.status = self.PRAC_STATUS[0][0];

	def set_pos_doc(self):
		self.status = self.PRAC_POS[0][0];
	def set_pos_nurse(self):
		self.status = self.PRAC_POS[1][0];	


	
class GsmDevice(models.Model):
	GSM_STATUS      = (('A','active'),('D','not active'),)
	device_id	= models.CharField(max_length=20,primary_key=True,default="123456789")
	status          = models.CharField(max_length=2,choices=GSM_STATUS)
	activated_date  = models.DateField(auto_now_add=True)
        
	def deactivate(self):
		self.status = self.GSM_STATUS[1][0];
	def activate(self):
		self.status = self.GSM_STATUS[0][0];
	


class Patient(models.Model):

	PATIENT_STATUS  = (('A','active'),('D','not active'),)

	SystemUser   = models.ForeignKey(SystemUser,null=True)
	gestation    = models.IntegerField()
	practitioner = models.ForeignKey(Practitioner,null=True)
	status	     = models.CharField(max_length=2,choices=PATIENT_STATUS)
	gsm     	 = models.ForeignKey(GsmDevice,null=False,primary_key=True)

	def __unicode__(self):
		return u'%s' '%s' % (self.first_name, self.last_name)

	
class SmsData(models.Model):
	gsm 	        = models.ForeignKey(GsmDevice)
	heart_rate   = models.FloatField(default  = 0.0)#TODO change to appropriat field
	kick_count   = models.FloatField(default  = 0.0)
	date     = models.DateTimeField(auto_now_add=True,primary_key=True)

