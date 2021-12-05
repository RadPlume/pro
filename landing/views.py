from django.shortcuts import render

# Create your views here.
def landing(request):
    return render(request, "landing/landing.html")

def equations(request):
    return render(request, "landing/equations.html")

def about(request):
    return render(request, "landing/about.html")