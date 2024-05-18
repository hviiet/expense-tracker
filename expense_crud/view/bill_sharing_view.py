from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponseBadRequest

def bill_sharing(request):
    return render(request, 'bill_sharing.html', {})