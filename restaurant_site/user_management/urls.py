from django.urls import path
from django.urls.conf import include
from . import views



# URL patterns for authentication
urlpatterns = [
    path('login/', views.UserLoginAPIView.as_view(), name='login'),
    path('user/logout/', views.UserLogoutViewAPI.as_view(), name='logout'),
    path('user/', views.UserViewAPI.as_view(), name='home'),
    path('register/', views.UserRegistrationAPIView.as_view(), name='registration'),
    path('user/reservations/', include('reservations_app.urls'), name='reservations')
]