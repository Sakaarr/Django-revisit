# from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from .models import Menu
from django.core import serializers
from .models import Booking
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})

def book(request):
    hours_range = range(10,21)
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form , 
               'hours_range': hours_range}
    return render(request, 'book.html', context)

# Add your code here to create new views
def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 

@csrf_exempt
def bookings(request):
    # if request.method == 'POST':
    #     data = json.load(request)
    #     exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
    #         reservation_slot=data['reservation_slot']).exists()
    #     if exist==False:
    #         booking = Booking(
    #             first_name=data['first_name'],
    #             reservation_date=data['reservation_date'],
    #             reservation_slot=data['reservation_slot'],
    #         )
    #         booking.save()
    #     else:
    #         return HttpResponse("{'error':1}", content_type='application/json')
    
    # date = request.GET.get('date',datetime.today().date())

    # bookings = Booking.objects.all().filter(reservation_date=date)
    # booking_json = serializers.serialize('json', bookings)

    # return HttpResponse(booking_json, content_type='application/json')
    if request.method == 'POST':
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
        reservation_slot=data['reservation_slot']).exists()
        if not exist:
            booking = Booking(
            first_name=data['first_name'],
            reservation_date=data['reservation_date'],
            reservation_slot=data['reservation_slot'],
        )
            booking.save()
        else:
            return HttpResponse(json.dumps({'error': 1}), content_type='application/json')

    date = request.GET.get('date', datetime.today().date())
    bookings = Booking.objects.filter(reservation_date=date)

    booking_list = []
    for booking in bookings:
            booking_dict = {
        'first_name': booking.first_name,
        'reservation_date': str(booking.reservation_date),
        'reservation_slot': format_time(booking.reservation_slot),
    }
    booking_list.append(booking_dict)

    booking_json = json.dumps(booking_list)
    return HttpResponse(booking_json, content_type='application/json')

def format_time(slot):
    hour = slot % 24
    ampm = 'AM' if hour < 12 else 'PM'
    if hour == 0:
        hour = 12
    elif hour > 12:
        hour -= 12
    return f"{hour}:00 {ampm}"