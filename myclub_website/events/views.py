import calendar
from calendar import HTMLCalendar
from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404

from .models import Event, MyClubUser
from .forms import BuyTicketForm


def home(request, year=datetime.now().year , month=datetime.now().strftime('%B')):
    dict = {"name" : "Sergio" , "lname" : "Merdani"}
    name = dict["name"]
    lname = dict["lname"]

    month = month.capitalize()

    #convert month from name to number

    month_number =list(calendar.month_name).index(month)
    month_number = int(month_number)

    #create calendar

    cal = HTMLCalendar().formatmonth(year,month_number)

    #get current year
    now = datetime.now()
    current_year = now.year

    #Get current time

    time = now.strftime('%I:%M %p')
    return render(request,
        'events/home.html',{
        "name" : name,
        "lname" : lname,
        "year" : year,
        "month" : month,
        "month_number" : month_number,
        "cal" : cal,
        "current_year" : current_year,
        "time" : time
    })


def event_list(request):
    today = datetime.now()
    events = Event.objects.filter(event_date__gt=today).order_by('event_date').all()

    return render(request, 'events/event_list.html', context={
        'events': events
    })


def event_details(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = BuyTicketForm(request.POST, available_tickets=event.tickets)
        if form.is_valid():
            tickets = form.cleaned_data.pop('tickets')
            club_user = MyClubUser.objects.create(**form.cleaned_data)
            event.tickets = event.tickets - tickets
            event.attendees.add(club_user)
            event.save()
            return redirect('event_details', pk=event.pk)
    else:
        form = BuyTicketForm(available_tickets=event.tickets)

    return render(request, 'events/event_details.html', context={
        'event': event,
        'form': form,
    })
