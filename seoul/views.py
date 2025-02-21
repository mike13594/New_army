from django.shortcuts import render

# Create your views here.
def places(request):
    return render(request, "places.html")