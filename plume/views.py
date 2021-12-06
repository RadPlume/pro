# Create your views here.
from bokeh.embed import server_document
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def plume(request: HttpRequest) -> HttpResponse:
    script = server_document(request.build_absolute_uri())
    return render(request, "base.html", {'script': script})
