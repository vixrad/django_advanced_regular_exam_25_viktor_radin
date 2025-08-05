from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import DatabaseError
from restaurants.models import Restaurant
from .models import MenuCategory, MenuItem
from .forms import MenuCategoryForm, MenuItemForm

# check if user is owner or superuser
def is_owner_or_superuser(user):
    return user.is_authenticated and (getattr(user, "is_owner", False) or user.is_superuser)

# display menu details
def menu_detail(request, restaurant_id):
    try:
        restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        categories = restaurant.menu_categories.prefetch_related('menu_items')
        return render(request, "menu/menu_detail.html", {
            "restaurant": restaurant,
            "categories": categories
        })
    except DatabaseError:
        messages.error(request, "could not load the menu for this restaurant.")
        return redirect("restaurant_list")

# add a new category
@login_required
@user_passes_test(is_owner_or_superuser)
def add_category(request, restaurant_id):
    try:
        if request.user.is_superuser:
            restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
        else:
            restaurant = get_object_or_404(Restaurant, pk=restaurant_id, owner=request.user)

        if request.method == "POST":
            form = MenuCategoryForm(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.restaurant = restaurant
                category.save()
                messages.success(request, "category added successfully.")
                return redirect("menu_detail", restaurant_id=restaurant.id)
            else:
                messages.error(request, "please correct the errors below and try again.")
        else:
            form = MenuCategoryForm()

        return render(request, "menu/add_category.html", {
            "form": form,
            "restaurant": restaurant
        })
    except DatabaseError:
        messages.error(request, "could not add category due to a database error.")
        return redirect("menu_detail", restaurant_id=restaurant_id)

# edit an existing category
@login_required
@user_passes_test(is_owner_or_superuser)
def edit_category(request, pk):
    try:
        category = get_object_or_404(MenuCategory, pk=pk, restaurant__owner=request.user)
        if request.method == "POST":
            form = MenuCategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, "category updated successfully.")
                return redirect("menu_detail", restaurant_id=category.restaurant.id)
            else:
                messages.error(request, "please correct the errors below and try again.")
        else:
            form = MenuCategoryForm(instance=category)
        return render(request, "menu/edit_category.html", {"form": form, "category": category})
    except DatabaseError:
        messages.error(request, "could not edit category due to a database error.")
        return redirect("menu_detail", restaurant_id=category.restaurant.id)

# delete a category
@login_required
@user_passes_test(is_owner_or_superuser)
def delete_category(request, pk):
    try:
        category = get_object_or_404(MenuCategory, pk=pk, restaurant__owner=request.user)
        if request.method == "POST":
            restaurant_id = category.restaurant.id
            category.delete()
            messages.success(request, "category deleted successfully.")
            return redirect("menu_detail", restaurant_id=restaurant_id)
        return render(request, "menu/delete_category.html", {"category": category})
    except DatabaseError:
        messages.error(request, "could not delete category due to a database error.")
        return redirect("menu_detail", restaurant_id=category.restaurant.id)

# add a new menu item
@login_required
@user_passes_test(is_owner_or_superuser)
def add_item(request, category_id):
    try:
        category = get_object_or_404(MenuCategory, pk=category_id, restaurant__owner=request.user)
        if request.method == "POST":
            form = MenuItemForm(request.POST, request.FILES)
            if form.is_valid():
                item = form.save(commit=False)
                item.category = category
                item.save()
                messages.success(request, "menu item added successfully.")
                return redirect("menu_detail", restaurant_id=category.restaurant.id)
            else:
                messages.error(request, "please correct the errors below and try again.")
        else:
            form = MenuItemForm()
        return render(request, "menu/add_item.html", {"form": form, "category": category})
    except DatabaseError:
        messages.error(request, "could not add menu item due to a database error.")
        return redirect("menu_detail", restaurant_id=category.restaurant.id)

# edit an existing menu item
@login_required
@user_passes_test(is_owner_or_superuser)
def edit_item(request, pk):
    try:
        item = get_object_or_404(MenuItem, pk=pk, category__restaurant__owner=request.user)
        if request.method == "POST":
            form = MenuItemForm(request.POST, request.FILES, instance=item)
            if form.is_valid():
                form.save()
                messages.success(request, "menu item updated successfully.")
                return redirect("menu_detail", restaurant_id=item.category.restaurant.id)
            else:
                messages.error(request, "please correct the errors below and try again.")
        else:
            form = MenuItemForm(instance=item)
        return render(request, "menu/edit_item.html", {"form": form, "item": item})
    except DatabaseError:
        messages.error(request, "could not edit menu item due to a database error.")
        return redirect("menu_detail", restaurant_id=item.category.restaurant.id)

# delete an existing menu item
@login_required
@user_passes_test(is_owner_or_superuser)
def delete_item(request, pk):
    try:
        item = get_object_or_404(MenuItem, pk=pk, category__restaurant__owner=request.user)
        if request.method == "POST":
            restaurant_id = item.category.restaurant.id
            item.delete()
            messages.success(request, "menu item deleted successfully.")
            return redirect("menu_detail", restaurant_id=restaurant_id)
        return render(request, "menu/delete_item.html", {"item": item})
    except DatabaseError:
        messages.error(request, "could not delete menu item due to a database error.")
        return redirect("menu_detail", restaurant_id=item.category.restaurant.id)