from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from coral_client import Client

# Create your views here.

a = Client('gokhan.karaboga', 'Yet123++')


@login_required
def homepage(request):
    return render(request, 'homepage.html')


@login_required()
def deneme(request):
    if request.method == "POST":
        destinations = request.POST.get("destinations")
        checkin = request.POST.get("checkin")
        checkout = request.POST.get("checkout")
        pax = request.POST.get('pax')

        search_params = {'checkin': checkin, 'checkout': checkout,
                         'pax': pax,
                         'destination_code': '11260',
                         'client_nationality': 'tr',
                         'currency': 'USD'}

        b = a.search(search_params)
        count = b[1]['count']

        # count = b['count']
        #
        bos_liste = []
        print count

        for i in xrange(count):
            bos_liste.append(b[1]['results'][i]['products'][0]['code'])

        deneme_dict = {'destinations': destinations, 'product_list': bos_liste}


    else:
        print 'Olmadi'

    return render(request, 'deneme.html', deneme_dict)
