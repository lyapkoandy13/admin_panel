from django.db import models

# Create your models here.


class BazaltUser(models.Model):
	token = models.CharField(max_length=255)
	firstname = models.CharField(max_length=30)
	secondname = models.CharField(max_length=30)
	email =	models.CharField(max_length=50)
	auth = models.IntegerField()
	date = models.CharField(max_length=15)
	agentCode = models.CharField(max_length=15)

	def __str__(self):
		return self.token
