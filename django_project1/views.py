from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response


def homepage(request):
    return HttpResponse('Homepage')
