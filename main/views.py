from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.shortcuts import redirect

# Create your views here.

def index(request):
	return render(request, 'main/index.html')

def ajax_send_mail(request):
	try:
		name = request.GET.get('name')
		email = request.GET.get('email')
		text = request.GET.get('text')
		message = ("Name: "+name+ "\nEmail: "+email+ "\n\n "+ text)
		emailMessage = EmailMessage('Mail from site', message, to=['director@aits.ua'])
		emailMessage.send()
		return HttpResponse("ok")
	except:
		return HttpResponse("")