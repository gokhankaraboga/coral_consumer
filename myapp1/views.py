from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from coral_client import Client
from myapp1.models import Destination, Hotel

client_object = Client('gokhan.karaboga', 'Yet123++')


@login_required
def homepage(request):
    if request.method == "GET":
        destination_name_list = Destination.objects.values_list('name',
                                                                flat=True)

    return render(request, 'homepage.html',
                  {'destination': destination_name_list})


@login_required
def destination_search(request):
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

        hotelcode_database_list = Hotel.objects.values_list('coral_code',
                                                            flat=True)

        results_list = []
        debug_counter = 0
        for i in xrange(count):
            if results[1]['results'][i]['hotel_code'] \
                    in hotelcode_database_list:
                tmp_dict = {
                    'min_price': float(min([item['list_price'] for item in
                                            results[1]['results'][i][
                                                'products']])),

                    'hotel_code': results[1]['results'][i][
                        'hotel_code'],

                    'currency': results[1]['results'][i][
                        'products'][0]['currency'],

                    'hotel_name': Hotel.objects.get(
                        coral_code=results[1]['results'][i][
                            'hotel_code']).name}

                results_list.append(tmp_dict)

                debug_counter += 1

        deneme_dict = {'total_list': results_list}

        print count, str(debug_counter)

    else:
        print 'Olmadi'

    return render(request, 'destination_search.html', deneme_dict)


@login_required()
def single_hotel_search(request):
    pass
