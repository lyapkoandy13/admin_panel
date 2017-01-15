import os
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
import json
import urllib.request
from wienerberger.models import WienerbergerUser
from django.views.decorators.csrf import csrf_exempt
import datetime

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

	data = json.dumps(data).encode('utf-8')
	req = urllib.request.Request(FCM_URL)
	req.add_header('Content-Type', 'application/json; charset=utf-8')
	req.add_header('Authorization', 'key=' + SERVER_KEY)

	with urllib.request.urlopen(req, data=data) as response:
		new_response = response.read()

	return HttpResponseRedirect('/wienerberer')

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


def download_wienerberger(request):
	file_path = os.path.join("/usr/pushmessanger/app-release.apk")
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/vnd.android.package-archive")
			response['Content-Disposition'] = 'inline; filename=' + 'wienerberger.apk'
			return response
	return redirect("/wienerberger/")

def get_version(request):
	data = ""
	with open('/usr/pushmessanger/version.txt', 'r') as myfile:
		data = myfile.read().replace('\n', '')
	return HttpResponse(data)