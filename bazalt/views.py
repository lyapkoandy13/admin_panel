import os
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
import json
import urllib.request
from bazalt.models import BazaltUser
from django.views.decorators.csrf import csrf_exempt
import datetime

# Create your views here.

def index(request):
	if request.user.is_authenticated():
		bazaltusers = BazaltUser.objects.all()
		return render(request, 'bazalt/index.html', {'bazaltusers' : bazaltusers})
	else:
		return redirect('/')

@csrf_exempt
def create_user(request):
	token = request.POST.get('token','')
	firstname = request.POST.get('firstname','')
	secondname = request.POST.get('secondname','')
	email = request.POST.get('email','')
	date = datetime.datetime.now().strftime("%d-%m-%Y")
	a = BazlaltUser(token=token,firstname=firstname,secondname=secondname,email=email,auth=0,date=date,agentCode="None")
	a.save()
	
	return HttpResponse('success')

@csrf_exempt
def delete_user(request):
	id = request.POST.get('id','')
	id = int(id)
	BazaltUser.objects.filter(id=id).delete()

	return HttpResponse("success")

@csrf_exempt
def grant_access(request):
	id = request.POST.get('id', '')
	BazaltUser.objects.filter(id=id).update(auth=1)

	return HttpResponse("success")

@csrf_exempt
def deny_access(request):
	id = request.POST.get('id', '')
	BazaltUser.objects.filter(id=id).update(auth=0)

	return HttpResponse("success")


def download_bazalt(request):
	file_path = os.path.join("/usr/bazalt/app-release.apk")
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/vnd.android.package-archive")
			response['Content-Disposition'] = 'inline; filename=' + 'wienerberger.apk'
			return response
	return redirect("/wienerberger/")

def get_version(request):
	data = ""
	with open('/usr/bazalt/version.txt', 'r') as myfile:
		data = myfile.read().replace('\n', '')
	return HttpResponse(data)