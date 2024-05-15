from django.urls import path
from django.urls.conf import include
from .views import ReservationAPIView, NewReservationAPIView, DeleteReservationAPIView



# URL patterns for authentication
urlpatterns = [
    path('', ReservationAPIView.as_view()),
    path('reserve/', NewReservationAPIView.as_view()),
    path('delete/', DeleteReservationAPIView.as_view())
]