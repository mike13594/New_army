from django.shortcuts import render, get_object_or_404
from seoul.models import Place
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.
def place_list(request):
    places = Place.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(places,8)

    page_obj = paginator.get_page(page)

    context = {
        "places": places,
        "page_obj":page_obj,
        "paginator":paginator,
    }
    return render(request, "places.html", context)

def place_detail(request, place_id):
    place = get_object_or_404(Place, id=place_id)
    context = {
        "place": place,
    }
    return render(request, "place_detail.html", context)