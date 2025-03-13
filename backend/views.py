from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	print('')
	print('==== index ====')

	context = {}
	return render(request, 'index.html', context)