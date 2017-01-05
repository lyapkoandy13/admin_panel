from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.shortcuts import redirect

# Create your views here.

def index(request):
	if request.user.is_authenticated():
		return render(request, 'main_panel/main_panel.html')
	else:
		return render(request, 'main_panel/login.html')

def check_user(request):
	if request.method == "POST":
		username = request.POST.get('user_login','')
		password = request.POST.get('user_password','')
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				request.session.set_expiry(86400)
				login(request, user)
				return HttpResponse('yes', content_type='text/html')
		return HttpResponse('', content_type='text/html')
	else:
		return HttpResponse('', content_type='text/html')

def logout(request):
	auth.logout(request)

	return redirect('/')