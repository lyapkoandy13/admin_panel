from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.shortcuts import redirect
import json
import urllib.request
from wienerberger.models import WienerbergerUser

# Create your views here.

def index(request):
	if request.user.is_authenticated():
		return render(request, 'wienerberger/index.html')
	else:
		return redirect('/')

def create_user(request):
	token = request.POST.get('token','')
	firstname = request.POST.get('firstname','')
	secondname = request.POST.get('secondname','')
	email = request.POST.get('email','')
	a = WienerbergerUser(token=token,firstname=firstname,secondname=secondname,email=email)
	a.save()
	
	return HttpResponse('success')

def send_message(request):
	message = request.POST.get('message','')
	users = WienerbergerUser.objects.filter(auth=1)
	tokens = users.token

	data = {
		"data": {
			"message" : message 
		},
		"registration_ids" : tokens,
		"priority" : "high"
	}

	FCM_URL = "https://fcm.googleapis.com/fcm/send"
	SERVER_KEY = "AIzaSyAkawp5NLDyMAXjzomidjTVG92q-8GIa64"

	req = urllib.request.Request(FCM_URL, json.dumps(data))
	req.add_header('Content-Type', 'application/json')
	req.add_header('Authorization', 'key=' + SERVER_KEY)

	with urllib.request.urlopen(req) as response:
		new_response = response.read()

	return HttpResponse('success')

def delete_user(request):
	id = request.POST.get('id','')
	WienerbergerUser.objects.filter(id=id).delete()

	return HttpResponse("success")

def grant_access(request):
	id = request.POST.get('id', '')
	WienerbergerUser.objects.filter(id=id).update(auth=1)

	return HttpResponse("success")

def deny_access(request):
	id = request.POST.get('id', '')
	WienerbergerUser.objects.filter(id=id).update(auth=0)

	return HttpResponse("success")
