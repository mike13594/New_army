from django.shortcuts import render, get_object_or_404
from seoul.models import Place
# Create your views here.
def place_list(request):
    places = Place.objects.all()
    context = {
        "place": places,
    }
    return render(request, "places.html", context)

def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    context = {
        "place": place,
    }
    return render(request, "place_detail.html", context)