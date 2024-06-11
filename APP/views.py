from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from .forms import ContactForm,RoomAvailabilityForm
from .models import Ticket,Room,Users
from django.views import generic
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
# Create your views here.



class HomePageView(generic.TemplateView):
    template_name = "index.html"



def index(request):
    return render(request,'index.html')
def rooms(request):
    return render(request,'rooms.html')
def about(request):
    return render(request,'about.html')

from django.http import JsonResponse

def single_room(request):
    if request.method == 'POST':
        form = RoomAvailabilityForm(request.POST)
        if form.is_valid():
            room_type = form.cleaned_data['room_type']
            no_of_rooms = form.cleaned_data['no_of_rooms']
            check_in_date = form.cleaned_data['check_in_date']
            check_out_date = form.cleaned_data['check_out_date']
            check_in_time = form.cleaned_data['check_in_time']
            available_rooms = Room.objects.filter(
                room_type=room_type,
                is_booked=False
            ).exclude(
                booked_checkin_date__lt=check_out_date,
                booked_checkout_date__gt=check_in_date
            )

            if available_rooms.count() >= no_of_rooms:
                rooms = list(available_rooms.values('id', 'room_type', 'room_number', 'price'))
                return JsonResponse({'available': True, 'rooms': rooms, 'check_in_date': check_in_date , 'check_out_date': check_out_date})
            else:
                return JsonResponse({'available': False})
        else:
            return JsonResponse({'available': False, 'errors': form.errors})
    else:
        form = RoomAvailabilityForm()
    return render(request, 'single_room.html', {'form': form})


def payment(request):
    return render(request,'payment.html')
def booking_complete(request):
    # Display booking complete message
    return HttpResponse("Booking complete! Thank you for your reservation.")


def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        # Handle booking logic here
        # For example, create a Ticket, update Room's booked_checkin_date and booked_checkout_date, etc.
        room.is_booked = True
        room.booked_checkin_date = request.POST['check_in_date']
        room.booked_checkout_date = request.POST['check_out_date']
        room.save()
        # Redirect to a confirmation page or similar
        return redirect('booking_confirmation')
    return render(request, 'book_room.html', {'room': room})

def payment_page(request):
    room_type = request.GET.get('room_type')
    no_of_rooms = request.GET.get('no_of_rooms')
    room_total_amount = calculate_room_total_amount(room_type, no_of_rooms)
    context = {
        'room_type': room_type,
        'no_of_rooms': no_of_rooms,
        'room_total_amount': room_total_amount
    }
    return render(request, 'payment.html', context)

@csrf_exempt
def process_payment(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        transaction_id = request.POST.get('transaction_id')
        status = request.POST.get('status')
        amount = request.POST.get('amount')
        check_in_date_str = request.POST.get('check_in_date')
        check_out_date_str = request.POST.get('check_out_date')

        # Convert string dates to datetime objects
        try:
            check_in_date = datetime.datetime.fromisoformat(check_in_date_str)
            check_out_date = datetime.datetime.fromisoformat(check_out_date_str)
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)

        # Process the payment and create booking records
        if status == 'COMPLETED':
            # Create User record
            user = Users.objects.create(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                age=request.POST.get('age'),
                phone_number=request.POST.get('phone_number'),
                Email=request.POST.get('email'),
                proof=request.FILES.get('proof_image')
            )
            # Create Ticket record
            ticket = Ticket.objects.create(
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                no_of_rooms=request.POST.get('no_of_rooms'),
                is_checked_out=False
            )
            # Link User and Ticket
            user.ticket = ticket
            user.save()
            # Update Room availability
            room_type = request.POST.get('room_type')
            no_of_rooms = int(request.POST.get('no_of_rooms'))
            rooms = Room.objects.filter(room_type=room_type, is_booked=False)[:no_of_rooms]
            for room in rooms:
                room.is_booked = True
                room.booked_checkin_date = check_in_date
                room.booked_checkout_date = check_out_date
                room.save()

            return JsonResponse({'redirect_url': reverse('booking_complete')})
        else:
            return JsonResponse({'redirect_url': reverse('payment_failed')})

    return JsonResponse({'error': 'Invalid request'}, status=400)


def booking_complete(request):
    return render(request, 'booking_complete.html')

def payment_failed(request):
    return render(request, 'payment_failed.html')

def calculate_room_total_amount(room_type, no_of_rooms):
    room = Room.objects.filter(room_type=room_type).first()
    if room:
        return room.price * int(no_of_rooms)
    return 0


@csrf_exempt
def dummy_payment_gateway(request):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')

        # You can store the booking details in the session or pass it along the URL
        request.session['room_id'] = room_id
        request.session['check_in_date'] = check_in_date
        request.session['check_out_date'] = check_out_date

        return render(request, 'dummy_payment_gateway.html')

    return redirect('single_room')



def payment_success(request):
    room_id = request.session.get('room_id')
    check_in_date = request.session.get('check_in_date')
    check_out_date = request.session.get('check_out_date')

    if room_id and check_in_date and check_out_date:
        room = get_object_or_404(Room, id=room_id)

        # Create a ticket or booking record for the user
        ticket = Ticket.objects.create(
            room=room,
            no_of_rooms=1,  # Adjust as needed
            check_in_date=check_in_date,
            check_out_date=check_out_date
        )

        # Mark the room as booked
        room.is_booked = True
        room.booked_checkin_date = check_in_date
        room.booked_checkout_date = check_out_date
        room.save()

        return render(request, 'payment_success.html')

    return redirect('single_room')


def tickets(request):
    return render(request, 'tickets.html')