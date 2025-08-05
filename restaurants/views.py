from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.forms import modelformset_factory
from django.views.generic import ListView
from django.http import JsonResponse
from datetime import datetime
from core.utils import generate_available_time_slots
from .models import Restaurant, OpeningHour
from .forms import RestaurantForm, OpeningHourForm


def is_owner_or_superuser(user):
    return user.is_authenticated and (getattr(user, "is_owner", False) or user.is_superuser)


class RestaurantListView(ListView):
    model = Restaurant
    template_name = 'restaurants/restaurant_list.html'
    context_object_name = 'restaurants'


@login_required
@user_passes_test(is_owner_or_superuser)
def add_restaurant(request):
    OpeningHourFormSet = modelformset_factory(
        OpeningHour,
        form=OpeningHourForm,
        extra=0,
        can_delete=False,
        min_num=7,
        validate_min=True
    )

    days = OpeningHour.DAYS_OF_WEEK
    initial_data = [{'day_of_week': d[0]} for d in days]

    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        formset_hours = OpeningHourFormSet(request.POST, queryset=OpeningHour.objects.none(), prefix="hours")

        if form.is_valid() and formset_hours.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()

            for i, fh in enumerate(formset_hours.save(commit=False)):
                fh.restaurant = restaurant
                if fh.day_of_week is None:
                    fh.day_of_week = days[i][0]
                fh.save()

            messages.success(request, "Restaurant added successfully!")
            return redirect('profile')
    else:
        form = RestaurantForm()
        formset_hours = OpeningHourFormSet(queryset=OpeningHour.objects.none(),
                                           initial=initial_data, prefix="hours")

    return render(request, 'restaurants/add_restaurant.html', {
        'form': form,
        'formset_hours': formset_hours,
    })


@login_required
@user_passes_test(is_owner_or_superuser)
def edit_restaurant(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk, owner=request.user)
    OpeningHourFormSet = modelformset_factory(
        OpeningHour,
        form=OpeningHourForm,
        extra=0,
        can_delete=False,
        min_num=7,
        validate_min=True
    )

    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        formset_hours = OpeningHourFormSet(
            request.POST, queryset=restaurant.opening_hours.all(), prefix="hours"
        )
        if form.is_valid() and formset_hours.is_valid():
            form.save()
            for fh in formset_hours.save(commit=False):
                fh.restaurant = restaurant
                fh.save()
            messages.success(request, "Restaurant updated successfully!")
            return redirect('profile')
    else:
        form = RestaurantForm(instance=restaurant)
        formset_hours = OpeningHourFormSet(
            queryset=restaurant.opening_hours.all(), prefix="hours"
        )

    return render(
        request,
        'restaurants/edit_restaurant.html',
        {'form': form, 'formset_hours': formset_hours, 'restaurant': restaurant},
    )


@login_required
@user_passes_test(is_owner_or_superuser)
def delete_restaurant(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk, owner=request.user)
    if request.method == 'POST':
        restaurant.delete()
        messages.success(request, "Restaurant deleted successfully!")
        return redirect('profile')
    return render(
        request,
        'restaurants/delete_restaurant.html',
        {'restaurant': restaurant},
    )

def get_timeslots(request, restaurant_id):
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse([], safe=False)

    try:
        selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse([], safe=False)

    restaurant = Restaurant.objects.filter(pk=restaurant_id).first()
    if not restaurant:
        return JsonResponse([], safe=False)

    weekday = selected_date.weekday()
    opening = OpeningHour.objects.filter(restaurant=restaurant, day_of_week=weekday).first()
    if not opening or opening.is_closed:
        return JsonResponse([], safe=False)

    slots = generate_available_time_slots(opening.open_time, opening.close_time)
    formatted = [{"value": t.strftime("%H:%M"), "label": t.strftime("%I:%M %p")} for t in slots]
    return JsonResponse(formatted, safe=False)