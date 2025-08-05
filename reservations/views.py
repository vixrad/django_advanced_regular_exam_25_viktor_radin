from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, DetailView
from datetime import datetime
from .models import Reservation, Review
from .forms import ReservationForm, ReviewForm
from restaurants.models import Restaurant, OpeningHour
from core.utils import generate_available_time_slots


def is_owner_or_superuser(user):
    return user.is_authenticated and (user.is_owner or user.is_superuser)


def is_customer(user):
    return user.is_authenticated and not user.is_owner and not user.is_superuser


@method_decorator(user_passes_test(is_customer), name='dispatch')
class MyReservationsView(ListView):
    model = Reservation
    template_name = 'reservations/my_reservations.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        return (
            Reservation.objects
            .filter(user=self.request.user)
            .select_related('restaurant')
            .order_by('-reservation_time')
        )


@method_decorator([login_required, user_passes_test(is_owner_or_superuser)], name='dispatch')
class OwnerReservationsView(ListView):
    model = Reservation
    template_name = 'reservations/owner_reservations.html'
    context_object_name = 'reservations'

    def get_queryset(self):
        owner_restaurants = Restaurant.objects.filter(owner=self.request.user)
        return (
            Reservation.objects
            .filter(restaurant__in=owner_restaurants)
            .select_related('user', 'restaurant')
            .order_by('-reservation_time')
        )


@method_decorator(login_required, name='dispatch')
class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'reservations/reservation_form.html'
    success_url = '/reservations/my/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        restaurant_id = self.kwargs.get('restaurant_id')
        if restaurant_id:
            restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
            kwargs['restaurant'] = restaurant
            kwargs['hide_restaurant'] = True
            self.initial['restaurant'] = restaurant
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Your reservation has been created.")
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'reservations/reservation_detail.html'
    context_object_name = 'reservation'

    def get_queryset(self):
        user = self.request.user
        if user.is_owner or user.is_superuser:
            return Reservation.objects.filter(restaurant__owner=user)
        return Reservation.objects.filter(user=user)


@login_required
def leave_review(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
    if reservation.status != Reservation.STATUS_COMPLETED:
        messages.error(request, "You can only review completed reservations.")
        return redirect('reservation_detail', pk=pk)

    if hasattr(reservation, 'review'):
        messages.info(request, "You have already reviewed this reservation.")
        return redirect('reservation_detail', pk=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reservation = reservation
            review.user = request.user
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect('reservation_detail', pk=pk)
    else:
        form = ReviewForm()

    return render(request, 'reservations/review_form.html', {
        'form': form,
        'reservation': reservation
    })


@login_required
def available_timeslots(request, restaurant_id):
    """
    AJAX endpoint to fetch all available 30-minute interval time slots for a given date and restaurant.
    """
    date_str = request.GET.get('date')
    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return JsonResponse([], safe=False)

    weekday = selected_date.weekday()
    opening = OpeningHour.objects.filter(restaurant_id=restaurant_id, day_of_week=weekday).first()

    if not opening or opening.is_closed:
        return JsonResponse([], safe=False)

    slots = generate_available_time_slots(opening.open_time, opening.close_time)
    result = [{"value": t.strftime("%H:%M"), "label": t.strftime("%I:%M %p")} for t in slots]
    return JsonResponse(result, safe=False)