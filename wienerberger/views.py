from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.shortcuts import redirect
import json
import urllib.request
from wienerberger.models import WienerbergerUser
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.http import JsonResponse
from django.core import  serializers

# Create your views here.

def index(request):
	if request.user.is_authenticated():
		wienerbergerusers = WienerbergerUser.objects.all()
		return render(request, 'wienerberger/index.html', {'wienerbergerusers' : wienerbergerusers})
	else:
		return redirect('/')

@csrf_exempt
def create_user(request):
	token = request.POST.get('token','')
	firstname = request.POST.get('firstname','')
	secondname = request.POST.get('secondname','')
	email = request.POST.get('email','')
	date = datetime.datetime.now().strftime("%d-%m-%Y")
	a = WienerbergerUser(token=token,firstname=firstname,secondname=secondname,email=email,auth=0,date=date)
	a.save()
	
	return HttpResponse('success')

def send_message(request):
	message = request.POST.get('message','')
	tokens = WienerbergerUser.objects.filter(auth=1).values_list('token', flat=True)
	tokens = list(tokens)

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

@csrf_exempt
def delete_user(request):
	id = request.POST.get('id','')
	id = int(id)
	WienerbergerUser.objects.filter(id=id).delete()

	return HttpResponse("success")

@csrf_exempt
def grant_access(request):
	id = request.POST.get('id', '')
	WienerbergerUser.objects.filter(id=id).update(auth=1)

	return HttpResponse("success")

@csrf_exempt
def deny_access(request):
	id = request.POST.get('id', '')
	WienerbergerUser.objects.filter(id=id).update(auth=0)

	return HttpResponse("success")


# @csrf_exempt
# def get_users(request):
# 	a = WienerbergerUser.objects.all()
# 	json_data = serializers.serialize('json', list(a), fields=('id','firstname','secondname','token','auth','date'))
# 	return JsonResponse(json_data, safe=False)
