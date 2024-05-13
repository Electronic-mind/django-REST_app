from django.urls import path
from django.urls.conf import include
from .views import ReservationAPIView, BookReservationAPIView



# URL patterns for authentication
urlpatterns = [
    path('', ReservationAPIView.as_view()),
    path('reserve/', BookReservationAPIView.as_view())
]