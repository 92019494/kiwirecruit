from django.db import models
import logging

from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver


log = logging.getLogger(__name__)

# log failed login and user name to identify brute force attacks

@receiver(user_login_failed)

def user_login_failed_callback(sender, credentials, **kwargs):

    log.warning('login failed for: {credentials}'.format(

        credentials=credentials['username'],

    ))
	
class User(models.Model):
	SEX_CHOICES = [('M', 'Male'),('F', 'Female')]
	name = models.CharField(max_length=100)
	username = models.CharField(max_length=100)
	sex=models.CharField(choices=SEX_CHOICES, max_length=1, blank=True)
	age = models.IntegerField(null=True)
	def __str__(self):
		return self.username

class Position(models.Model):
	job_title=models.CharField(max_length=50)
	description = models.TextField()
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.job_title
