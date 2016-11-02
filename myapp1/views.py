from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def homepage(request):
    return render(request, 'homepage.html')


@login_required()
def deneme(request):

    if request.method == "POST":
        variable = request.POST["destinations"]
        return HttpResponse(variable)
    else:
        print 'Olmadi'

    return render_to_response('deneme.html')
