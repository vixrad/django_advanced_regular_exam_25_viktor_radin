from django.urls import path
from . import views

urlpatterns = [
    path('<int:restaurant_id>/', views.menu_detail, name='menu_detail'),
    path('category/add/<int:restaurant_id>/', views.add_category, name='add_category'),
    path('category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('category/delete/<int:pk>/', views.delete_category, name='delete_category'),
    path('item/add/<int:category_id>/', views.add_item, name='add_item'),
    path('item/edit/<int:pk>/', views.edit_item, name='edit_item'),
    path('item/delete/<int:pk>/', views.delete_item, name='delete_item'),
]