from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserInfo(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='info')
	# date_of_birth=models.DateField()
	points= models.IntegerField(default=0)
	phone= models.CharField(max_length=11, default=0)
	showPhone=models.BooleanField(default=False)
	level = models.IntegerField(default=1)
	def __str__(self):
		return self.user.last_name
