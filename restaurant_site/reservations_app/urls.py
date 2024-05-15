from django.urls import path
from django.urls.conf import include
from .views import ReservationAPIView, NewReservationAPIView



# URL patterns for authentication
urlpatterns = [
    path('', ReservationAPIView.as_view()),
    path('reserve/', NewReservationAPIView.as_view())
]