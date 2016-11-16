from django.shortcuts import render
from django.template import RequestContext
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from coral_client import Client
from myapp1.models import Booking, Destination, Hotel
from operator import itemgetter
from django.conf import settings
from concurrent.futures import ThreadPoolExecutor
from django.core.mail import send_mail
import redis
import json
import random
import string

client_object = Client('gokhan.karaboga', 'Yet123++')

r = redis.Redis('localhost')


@login_required
def homepage(request):
    if request.method == "GET" or request.method == "POST":
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

        """Redis Caching"""
        r.set('checkin', checkin)
        r.set('checkout', checkout)
        """Redis Caching"""

        destination_code = str(Destination.objects.get(
            name=destinations).coral_code)

        search_params = {'checkin': checkin, 'checkout': checkout,
                         'pax': pax,
                         'destination_code': destination_code,
                         'client_nationality': 'tr',
                         'currency': 'USD'}

        request.session['search_params'] = search_params

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
                    'min_price': min([float(item['list_price']) for item in
                                      results[1]['results'][i][
                                          'products']]),

                    'hotel_code': results[1]['results'][i][
                        'hotel_code'],

                    'currency': results[1]['results'][i][
                        'products'][0]['currency'],

                    'hotel_name': Hotel.objects.get(
                        coral_code=results[1]['results'][i][
                            'hotel_code']).name}

                results_list.append(tmp_dict)

                debug_counter += 1

        assign_dict = {
            'total_list': sorted(results_list, key=itemgetter('min_price'))}

        print count, str(debug_counter)

    else:
        print 'Olmadi'

    return render(request, 'destination_search.html', assign_dict)


@login_required
def single_hotel_search(request):
    if request.method == "POST":
        hotel_code = request.POST.get("hotel_search")

        """Redis Caching"""
        r.set('hotel_code', hotel_code)
        """Redis Caching"""

        search_params = request.session["search_params"]
        search_params["hotel_code"] = str(hotel_code)

        hotel_results = client_object.search(search_params)

        count = len(hotel_results[1]["results"][0]["products"])

        print "Product Count:", count

        hotel_name = Hotel.objects.get(coral_code=hotel_code).name
        request.session["hotel_name"] = hotel_name

        product_list = []

        products = hotel_results[1]['results'][0]['products']

        for i in xrange(count):
            tmp_dict = {
                'product_code': products[i]['code'],
                'list_price': float(products[i]['list_price']),
                'currency': products[i]['currency'],
                'room_category': products[i]['rooms'][0]['room_category'],
                'room_type': products[i]['rooms'][0]['room_type'],
                'room_description': products[i]['rooms'][0][
                    'room_description'],
                'meal_type': products[i]['meal_type']
            }

            product_list.append(tmp_dict)

        request.session['product_list'] = product_list

    return render(request, 'single_hotel_search.html',
                  {'hotel_name': hotel_name,
                   'product_list': sorted(product_list,
                                          key=itemgetter('list_price'))})


@login_required
def availability(request):
    if request.method == "POST":
        product_code = request.POST.get("product_search")
        hotel_name = request.session["hotel_name"]
        product_list = request.session['product_list']

        response = client_object.availability(product_code)

        if response[0] != 200:
            return 'Something is wrong here'

        info_tmp = [product_list[i] for i in xrange(len(product_list)) if
                    product_list[i]['product_code'] == product_code]

        info_tmp[0]["pax"] = int(request.session["search_params"]["pax"])

        """Redis Caching"""
        r.set('product_code', product_code)
        json_package = json.dumps(info_tmp[0])
        r.set('product_info', json_package)
        """Redis Caching"""

    return render(request, 'booking_page.html',
                  {'info_tmp': info_tmp[0], 'hotel_name': hotel_name,
                   'checkin': r.get('checkin'), 'checkout': r.get('checkout')})


def random_key_generator():
    length = 8
    characters = string.digits + string.ascii_lowercase + string. \
        ascii_uppercase

    return ''.join(random.choice(characters) for _ in range(length))


def sending_mail(recipient, message):
    send_mail(
        'Booking Confirmation',
        'Your Booking has been successfully completed!',
        settings.EMAIL_HOST_USER,
        [recipient],
        fail_silently=False,
        html_message=message,
    )


@login_required
def booking(request):
    if request.method == "POST":
        provision_code = r.get('product_code')
        info_dict = json.loads(r.get('product_info'))

        pax_name = [str(request.POST.get('pax_name%s' % i)) for i in
                    xrange(int(info_dict['pax']))]

        book_param = {
            'name': ['1,{},{},adult'.format(pax_name[i].split(' ')[0],
                                            pax_name[i].split(' ')[1]) for i in
                     xrange(len(pax_name))]}

        book_code = client_object.provision(provision_code)[1].get('code')
        book_resp = client_object.book(book_code, book_param)

        if book_resp[0] != 200:
            return 'Something is wrong here'

        info_dict.update({
            'pax_names': pax_name,
            'pax_count': len(pax_name),
            'hotel_name': request.session['hotel_name'],
            'checkin': r.get('checkin'),
            'checkout': r.get('checkout'),
            'hotel_code': r.get('hotel_code'),
            'provision_code': provision_code,
            'user_id': request.user,
            'booking_code': random_key_generator(),
            'coral_booking_code': book_code,
            'status': book_resp[1]['status']
        })

        del info_dict['pax']
        del info_dict['product_code']

        if Booking.objects.filter(
                provision_code=info_dict['provision_code']).exists():
            return 'Duplicate Error!'

        Booking.objects.create(**info_dict)

        html_file = render(request, 'email.html',
                           {'info_dict': info_dict}).content

        with ThreadPoolExecutor(max_workers=1) as execute:
            execute.submit(
                sending_mail,
                request.POST.get("email"),
                html_file
            )
            # sending_mail(request.POST.get("email"), html_file)

    return render(request, 'book_success.html', {'info_dict': info_dict})


@login_required
def booking_list(request):
    if request.method == "POST":
        bookings = list()

        for item in Booking.objects.all():
            tmp = model_to_dict(item)
            bookings.append(tmp)

    return render(request, 'booking_list.html', {'bookings': bookings})
