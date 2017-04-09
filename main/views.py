from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.shortcuts import redirect

# Create your views here.

def index(request):
	return render(request, 'main/index.html')

def ajax_send_mail(request):
	if request.method == "POST":
		# try:
		name = request.POST.get('name')
		email = request.POST.get('email')
		text = request.POST.get('text')
		message = ("Name: "+name
			+ "\nEmail: "+email
			+ "\n\n "+ text)
		emailMessage = EmailMessage('Mail from site', message, to=['lyapkoandy13@gmail.com','director@aits.ua'])
		emailMessage.send()
		return HttpResponse("ok")
		# except:
		# 	return HttpResponse("")
	else:
		return redirect('/')