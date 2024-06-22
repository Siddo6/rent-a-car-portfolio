from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm
from .models import Car, reservation
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import now
from datetime import datetime
current_time = now()
current_month = current_time.month
current_year = current_time.year
# Create your views here.
def index(request):
    return render (request, 'core/index.html')

@user_passes_test(lambda u: u.is_superuser)
def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_reservations')  
        else:
            print(form.errors) 

    else:
        form = ReservationForm()
        
    context = {
        'form': form,
    }

    return render(request, 'core/add_reservation.html', context)

@user_passes_test(lambda u: u.is_superuser)
def reservation_list(request):
    reservations = reservation.objects.all()
    return render(request, 'core/all_reservations.html', {'reservations': reservations,'current_month': current_month,'current_year':current_year})

@user_passes_test(lambda u: u.is_superuser)
def reservation_list_current_month(request, current_month, current_year):
    
    # Filter reservations where from_date is within the current month and year
    reservations = reservation.objects.filter(from_date__month=current_month, from_date__year=current_year)
    
    return render(request, 'core/reservation_list_current_month.html', {'reservations': reservations,'current_month': current_month,'current_year':current_year})

@user_passes_test(lambda u: u.is_superuser)
def cars(request):
    cars = Car.objects.all()
    return render(request, 'core/cars.html', {'cars': cars})


def get_booked_dates(car_id):
    booked_dates = reservation.objects.filter(
        car_id=car_id
    ).values_list('from_date', 'to_date')
    return list(booked_dates)


#EDIT VIEW
@user_passes_test(lambda u: u.is_superuser)
def reservation_edit_view(request, pk):
    reservation_instance = get_object_or_404(reservation, pk=pk)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation_instance)
        if form.is_valid():
            form.save()
            return redirect('reservation_detail', pk=pk)  # Redirect to detail view or another appropriate URL
    else:
        form = ReservationForm(instance=reservation_instance)
    
    return render(request, 'core/reservation_edit.html', {'form': form, 'reservation': reservation_instance})

#DELETE RESERVATION
@user_passes_test(lambda u: u.is_superuser)
def reservation_delete_view(request, pk):
    reservation_instance = get_object_or_404(reservation, pk=pk)
    
    if request.method == 'POST':
        reservation_instance.delete()
        return redirect('all_reservations')  # Redirect to list view or another appropriate URL
    
    return render(request, 'core/reservation_delete.html', {'reservation': reservation_instance})

@user_passes_test(lambda u: u.is_superuser)
def reservation_detail_view(request, pk):
    reservation_instance = get_object_or_404(reservation, pk=pk)
    return render(request, 'core/reservation_detail.html', {'reservation': reservation_instance})



def available_cars(request):
    available_cars = Car.objects.none()  # Initialize with an empty queryset
    
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        
        # Convert to datetime objects
        from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        
        # Query available cars
        booked_cars = reservation.objects.filter(
            from_date__lte=to_date,
            to_date__gte=from_date
        ).values_list('car_id', flat=True)
        
        available_cars = Car.objects.exclude(id__in=booked_cars)
    
    return render(request, 'core/select_dates.html', {'available_cars': available_cars})