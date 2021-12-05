# Create your views here.
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def mapi(request):
    return render(request, "mapi.html", {})

'''
def mapi(request):
    headers = {
        uri = "https://arcgis.com/apps/Embed/index.html?"
        'webmap' = "4001d7656b0949cfa8a30a9a38b3bf91"
        extent = "-113.5532,33.0206,-112.7519,33.7179"
        uri = "src="https://arcgis.com/apps/Embed/index.html?
        webmap=webmap 
        extent=extent
        zoom=true
        previewImage=true
        scale=true
        search=true
        searchextent=true
        basemap_toggle=true
        alt_basemap=topo
        disable_scroll=true
        theme=dark
    }
#return render(request, "mapi.html", {'sourced': editlink, 'webmap': webmap, 'extent': extent})
return render(request, "mapi.html", {'webmap':webmap, 'extent':extent})'''