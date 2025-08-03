from django.urls import path
from .views import MenuDetailView

urlpatterns = [
    path('<int:restaurant_id>/', MenuDetailView.as_view(), name='menu_detail'),
]