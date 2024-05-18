from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination

from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from .serializers import ReservationSerializer, DeleteReservationSerializer, CheckTimeSlotsSerializer
from .models import Reservation, Table
from .queries import *

from restaurant_site import settings
from rest_framework.exceptions import AuthenticationFailed
import jwt
from datetime import datetime, date

# This API is where all the reservations are listed
class ReservationAPIView(APIView):
    '''Here is a list of all the reservations'''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    pagination_class = LimitOffsetPagination

    def get(self, request):
        # Check if the access token exists
        user_token = request.COOKIES.get('access_token')
        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')
        
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

        user_model = get_user_model()
        user = user_model.objects.filter(emp_id=payload['emp_id']).first()
        if user:
            if user.is_authenticated:
                reservations = list(Reservation.objects.values())
                return Response(reservations)
        return redirect('login')

# This API is where the user can reserve a table -- in progress
class NewReservationAPIView(APIView):

    '''You can reserve a table here'''
    serializer_class = ReservationSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request):
        content = {'message': ''}
        user_token = request.COOKIES.get('access_token')

        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')
        
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

        user_model = get_user_model()
        user = user_model.objects.filter(emp_id=payload['emp_id']).first()
        if user.is_authenticated:
            # list all the reservations
            reservations = list(Reservation.objects.values())
            return Response(reservations)
        
    def post(self, request):

        # Retrieve user access token
        user_token = request.COOKIES.get('access_token')
        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')
        
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

        user_model = get_user_model()
        user = user_model.objects.filter(emp_id=payload['emp_id']).first()

        # check if the user is authenticated
        if user.is_authenticated:

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):

                # get the data from the serializer
                start_time = serializer.validated_data['start_time']
                end_time = serializer.validated_data['end_time']
                seats = int(serializer.validated_data['seats_needed'])
                current_date = serializer.validated_data['date']
                

                # -------------Input validation----------------

                # if the start time is between 00:00 and 12:00
                if int(str(start_time)[:2]) < 12:
                    return Response('Time should be within the restauran\'s working hours. (12:00 PM - 11:59 PM)', status=status.HTTP_400_BAD_REQUEST)
                
                # if the end time is between 00:00 and 12:00
                if int(str(end_time)[:2]) < 12:
                    return Response('End time should be within the restauran\'s working hours. (12:00 PM - 11:59 PM)', status=status.HTTP_400_BAD_REQUEST)
                
                if start_time < datetime.now().time() and current_date == date.today():
                    return Response('Reservations cannot be before the current time')

                # if end time is before start time 
                if start_time > end_time:
                    return Response('End time cannot be before start time.', status=status.HTTP_400_BAD_REQUEST)
                
                # if the date is before the current day
                if current_date < date.today():
                    return Response('Date cannot be before today.', status=status.HTTP_400_BAD_REQUEST)

                # -------------------reservation process-----------------
                # retrieve a table with the requested number of seats
                table = get_table(seats)

                if table:
                    # if more than one table are returned
                    if isinstance(table, list):
                        for t in table:
                            if not is_reserved(start_time, end_time, t):
                                # if the table is free for the given time slot
                                serializer.validated_data.update({'employee': user, 'table': t})
                                serializer.save()
                                return Response(f'The table is successfully reserved from {start_time} to {end_time} on {current_date}', status=status.HTTP_201_CREATED)
                            return Response('The rquested table is fully booked for the rquested time.', status=status.HTTP_400_BAD_REQUEST)
                        
                    # if only one table is returned
                    elif not is_reserved(start_time, end_time, table):
                        # if the table is free for the given time slot
                        serializer.validated_data.update({'employee': user, 'table': table})
                        serializer.save()
                        return Response(f'The table is successfully reserved from {start_time} to {end_time} on {current_date}', status=status.HTTP_201_CREATED)
                    
                    return Response('The rquested table is reserved for the rquested time.', status=status.HTTP_400_BAD_REQUEST)

                # if the table is None
                return Response('The table does not exist.', status=status.HTTP_400_BAD_REQUEST)
        return AuthenticationFailed('Unauthenticated user.')


class DeleteReservationAPIView(APIView):
    '''Delete a reservation for the current working day'''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = DeleteReservationSerializer

    def get(self, request):
        # Retrieve user access token
        user_token = request.COOKIES.get('access_token')
        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')
        
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

        user_model = get_user_model()
        user = user_model.objects.filter(emp_id=payload['emp_id']).first()

        # check if the user is authenticated
        if user.is_authenticated:
            return Response({'message': 'choose a reservation to delete.', 'reservations': Reservation.objects.filter(date__gte=date.today(), start_time__gt=datetime.now().time())})
        return AuthenticationFailed('Unauthenticated user.')
    
    def post(self, request):
        # Retrieve user access token
        user_token = request.COOKIES.get('access_token')
        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')
        
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

        user_model = get_user_model()
        user = user_model.objects.filter(emp_id=payload['emp_id']).first()

        # check if the user is authenticated
        if user.is_authenticated:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):

                # Query the reservations to find the specified reservation
                reservation_id = serializer.data['reservation_id']
                reservation = Reservation.objects.filter(id=reservation_id, date__gte=date.today(), start_time__gt=datetime.now().time())
                if reservation:
                    # delete the reservation if it exists
                    reservation.delete()
                    return Response('The reservation is successfully deleted.', status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response('The reservation does not exist.', status=status.HTTP_404_NOT_FOUND)
        return AuthenticationFailed('Unauthenticated user.')
    

class CheckTimeSlotsAPIView(APIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = CheckTimeSlotsSerializer

    def get(self, request):
        # Retrieve user access token
        user_token = request.COOKIES.get('access_token')
        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')
        
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

        user_model = get_user_model()
        user = user_model.objects.filter(emp_id=payload['emp_id']).first()

        # check if the user is authenticated
        if user.is_authenticated:
            return Response({'message': 'choose the number of seats to query available time slots.'})
        return AuthenticationFailed('Unauthenticated user.')
    
    def post(self, request):
        # Retrieve user access token
        user_token = request.COOKIES.get('access_token')
        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')
        
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

        user_model = get_user_model()
        user = user_model.objects.filter(emp_id=payload['emp_id']).first()

        # check if the user is authenticated
        if user.is_authenticated:

            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                seats = int(serializer.data['number_of_seats'])
                table = get_table(seats)

                available_time = get_available_time_slots(table)

                return Response(str(available_time))

                #TODO: query the available time slots

                
        return AuthenticationFailed('Unauthenticated user.')
    
