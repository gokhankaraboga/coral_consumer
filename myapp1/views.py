from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from coral_client import Client
from myapp1.models import Destination, Hotel
import itertools

# Create your views here.

client_object = Client('gokhan.karaboga', 'Yet123++')


@login_required
def homepage(request):
    if request.method == "GET":
        destination_name_list = Destination.objects.values_list('name',
                                                                flat=True)

    return render(request, 'homepage.html',
                  {'destination': destination_name_list})


@login_required
def deneme(request):
    if request.method == "POST":
        destinations = request.POST.get("destinations")
        checkin = request.POST.get("checkin")
        checkout = request.POST.get("checkout")
        pax = request.POST.get('pax')

        destination_code = str(Destination.objects.get(
            name=destinations).coral_code)

        search_params = {'checkin': checkin, 'checkout': checkout,
                         'pax': pax,
                         'destination_code': destination_code,
                         'client_nationality': 'tr',
                         'currency': 'USD'}

        results = client_object.search(search_params)
        count = results[1]['count']
        bos_liste, list_price, hotel_name_list, min_price_list = (
            [], [], [], [])
        hotelcode_database_list = Hotel.objects.values_list('coral_code',
                                                            flat=True)
        debug_counter = 0
        for i in xrange(count):
            if results[1]['results'][i]['hotel_code'] \
                    in hotelcode_database_list:

                hotel_name_list.append(Hotel.objects.get(
                    coral_code=results[1]['results'][i]['hotel_code']).name)

                for item in results[1]['results'][i]['products']:
                    list_price.append(float(item['list_price']))

                min_price_list.append(min(list_price))
                list_price = []

                debug_counter += 1

        zipped_list = itertools.izip(hotel_name_list, min_price_list)

        deneme_dict = {'zipped_list': zipped_list}

        print count, str(debug_counter)



    else:
        print 'Olmadi'

    return render(request, 'deneme.html', deneme_dict)
