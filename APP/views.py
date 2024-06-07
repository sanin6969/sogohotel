from django.shortcuts import render,redirect
from .forms import ContactForm
from .models import Ticket,Room
from django.views import generic
from django.http import HttpResponse
# Create your views here.



class HomePageView(generic.TemplateView):
    template_name = "index.html"



def index(request):
    return render(request,'index.html')
def rooms(request):
    return render(request,'rooms.html')
def about(request):
    return render(request,'about.html')

def single_room(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            room_type = form.cleaned_data['Type_of_room']
            no_of_rooms = form.cleaned_data['Number_of_Rooms']
            check_in_date = form.cleaned_data['Check_in']
            check_out_date = form.cleaned_data['Check_out']
            
            available_rooms = Room.objects.filter(room_type=room_type, is_booked=False)
            available_rooms_count = available_rooms.count()
            
            if available_rooms_count >= no_of_rooms:
                selected_rooms = available_rooms[:no_of_rooms]
                for room in selected_rooms:
                    ticket = Ticket.objects.create(room=room, no_of_rooms=1, check_in_date=check_in_date, check_out_date=check_out_date)
                    room.is_booked = True
                    room.save()
                return redirect('payment')  # Redirect to payment page after successful booking
            else:
                return render(request, 'single_room.html', {'form': form, 'error_message': 'No available rooms matching your criteria'})
    else:
        form = ContactForm()
    return render(request, 'single_room.html', {'form': form})

def payment(request):
    return render(request,'payment.html')
def booking_complete(request):
    # Display booking complete message
    return HttpResponse("Booking complete! Thank you for your reservation.")
