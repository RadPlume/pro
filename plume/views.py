# Create your views here.
from bokeh.embed import server_document
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def plume(request):
    return render(request, "plume.html", {'script': script})
