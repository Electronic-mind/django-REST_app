from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework.permissions import AllowAny

from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from .serializers import ReservationSerializer
from .models import Reservation, Table
from restaurant_site import settings
from rest_framework.exceptions import AuthenticationFailed
import jwt
from datetime import datetime, date

# This API is where all the reservations are listed
class ReservationAPIView(APIView):
    '''Here is a list of all the reservations'''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        # Check if the access token exists
        user_token = request.COOKIES.get('access_token')
        if not user_token:
            raise AuthenticationFailed('Unauthenticated user.')
        
        emp_id = pk
        payload = jwt.decode(user_token, settings.SECRET_KEY, algorithms=['HS256'])

        # check if the id in the access token matches the current id
        if emp_id != payload['emp_id']:
            raise AuthenticationFailed('Unauthenticated user.')

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


                start_t = serializer.validated_data['start_time']
                end_t = serializer.validated_data['end_time']
                seats = int(serializer.validated_data['seats_needed'])
                current_date = serializer.validated_data['date']

                # if the start time is between 00:00 and 12:00
                if int(str(start_t)[:2] ) < 12:
                    return Response('Start time should be within the restauran\'s working hours. (12:00 PM - 11:59 PM)', status=status.HTTP_400_BAD_REQUEST)
                
                # if the end time is between 00:00 and 12:00
                if int(str(end_t)[:2]) < 12:
                    return Response('End time should be within the restauran\'s working hours. (12:00 PM - 11:59 PM)', status=status.HTTP_400_BAD_REQUEST)
                
                # if end time is before start time 
                if start_t > end_t:
                    return Response('End time cannot be before start time.', status=status.HTTP_400_BAD_REQUEST)
                
                # if the date is before the current day
                if current_date < date.today():
                    return Response('Date cannot be before today.', status=status.HTTP_400_BAD_REQUEST)

                # if the number of seats requested is 2 or 1
                if seats <= 2  and seats > 0:
                    table = Table.objects.filter(no_of_seats='2').first()
                    if table :
                        serializer.validated_data.update({'table':int(table.pk), 'employee': str(user.pk)})
                        return Response(serializer.validated_data)
                    return Response('no tables are available', status=status.HTTP_400_BAD_REQUEST)
                
                # if the number of seats requested is 4 or less
                elif seats <= 4:
                    table = Table.objects.get(no_of_seats='4')
                    if table :
                        serializer.validated_data.update({'table':int(table.pk), 'employee': str(user.pk)})
                        return Response(serializer.validated_data)
                    return Response('no tables are available', status=status.HTTP_400_BAD_REQUEST)
                
                # if the number of seats requested is 6 or less
                elif seats <= 6:
                    table = Table.objects.get(no_of_seats='6')
                    if table :
                        serializer.validated_data.update({'table':int(table.pk), 'employee': str(user.pk)})
                        return Response(serializer.validated_data)
                    return Response('no tables are available', status=status.HTTP_400_BAD_REQUEST)
                
                else:
                    # if the number of seats requested is greater than 6/ less than 1
                    return Response('No tables are available with this number of seats.', status=status.HTTP_400_BAD_REQUEST)
                
                
                
                #serializer.update()
                return Response(serializer.validated_data)
