import datetime
from threading import Thread

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

from EventsReservation import settings
from app.forms import UserRegisterForm, ReserveForm, typeForm, EventForm
from app.models import Event, Reservation


# Create your views here.

def is_admin(user):
    return user.groups.filter(name='Admin').exists()


from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def send_async_email(email):
    email.send(fail_silently=False)

def register(request):
    if request.method == "POST":
        username = User.objects.filter(username=request.POST['username'])
        email_qs = User.objects.filter(email=request.POST['email'])
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            if email_qs.exists():
                messages.error(request, 'Email already registered')
                return redirect("register")
            if username.exists():
                messages.error(request, 'Username already registered')
                return redirect("register")

            user = form.save()
            login(request, user)
            from_email = settings.EMAIL_HOST_USER

            # HTML email to user
            subject = "Welcome to Bookenda!"
            html_message = render_to_string('emails/welcome_email.html', {'user': user})
            email_user = EmailMessage(subject, html_message, from_email, [user.email])
            email_user.content_subtype = "html"  # важен ред за HTML
            Thread(target=send_async_email, args=(email_user,)).start()

            # Notification to admin (plain text)
            subject2 = "New user registered"
            message2 = f"New user registered:\nName: {user.first_name} {user.last_name}\nEmail: {user.email}"
            recipient_list2 = ['nvlavceski542@gmail.com']
            email_admin = EmailMessage(subject2, message2, from_email, recipient_list2)
            Thread(target=send_async_email, args=(email_admin,)).start()

            return redirect("index")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{error}")
                    break
                break
    else:
        form = UserRegisterForm()

    return render(request, "registration/register.html", {'form': form})

def events(request):
    events = Event.objects.all()
    is_admin = request.user.groups.filter(name="Admin").exists()
    for event in events:
        if event.date_time.date() <= datetime.date.today():
            if event.date_time.date().day - datetime.date.today().day <= -2:
                event.delete()

    location = request.GET.get('location')
    title = request.GET.get('title')
    type = request.GET.get('type')
    if location:
        events = events.filter(location__contains=location)
    if title:
        events = events.filter(title__contains=title)
    if type:
        events = events.filter(type=type)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, "events/_events_list.html", {"events": events, 'is_admin': is_admin})

    return render(request, "events.html",
                  {"events": events, "types": Event.objects.values_list("type", flat=True).distinct(),
                   "is_admin": is_admin, "date": datetime.date.today()})


def event_detail(request, id):
    if request.user.is_anonymous:
        return redirect("login")
    event = Event.objects.get(id=id)
    reservations = Reservation.objects.filter(event=event, user=request.user)
    print(reservations)
    if request.method == "POST":
        form = ReserveForm(request.POST, request.FILES)
        if form.is_valid():
            reservations = form.save(commit=False)
            if reservations.seat_reservation <= event.free_seats:
                reservations.event = event
                reservations.user = request.user
                event.free_seats -= reservations.seat_reservation
                event.save()
                reservations.save()
                return redirect("event_detail", id=event.id)
            else:
                messages.error(request, "Not enough available spots")
                return redirect("event_detail", id=event.id)
    else:
        form = ReserveForm()
        messages.success(request, "print")
        return render(request, "event_detail.html", {"event": event, "form": form, "reservations": reservations})


def index(request):
    return render(request, "index.html")


def add_event(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                event = form.save(commit=False)
                event.free_seats = event.capacity
                event.created_by = request.user
                event.save()
                return redirect("events")
        else:
            return render(request, "CRUD/add_event.html")
    else:
        return redirect("login")


def delete_event(request, id):
    event = Event.objects.get(id=id)
    is_admin = request.user.groups.filter(name="Admin").exists()
    if request.user != event.created_by and not request.user.is_staff and not is_admin:
        raise PermissionDenied("Not have access to this page")
    event.delete()
    return redirect("events")


def edit_event(request, id):
    event = Event.objects.get(id=id)
    is_admin = request.user.groups.filter(name="Admin").exists()
    if request.user != event.created_by and not request.user.is_staff and not is_admin:
        raise PermissionDenied("Not have access to this page")

    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            if Reservation.objects.filter(event=event).exists():
                reservation = Reservation.objects.get(event=event)
                event.free_seats = event.capacity - reservation.seat_reservation
                if event.free_seats < 0:
                    messages.error(request, "You can't make it less than reserved")
                    return redirect("edit_event", id=event.id)
            else:
                event.free_seats = event.capacity
            event.save()
        return redirect("events")
    else:
        form = EventForm(instance=event)
        return render(request, "CRUD/edit_event.html", {"form": form, "event": event})


def profile(request):
    reservations = Reservation.objects.filter(user=request.user)
    events = Event.objects.filter(created_by=request.user)
    return render(request, "profile.html", {"reservations": reservations, "events": events})


def remove_reservation(request, id):
    reservation = Reservation.objects.get(id=id)
    event = reservation.event
    if request.method == "POST":
        event.free_seats += reservation.seat_reservation
        event.save()
        reservation.delete()
        return redirect("profile")
    return render(request, "profile.html")
