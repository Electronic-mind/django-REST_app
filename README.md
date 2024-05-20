# Restaurant reservation system using Django REST framework

This project is a restaurant table reservation system that allows staff users to reserve tables for customers for a given date and time period.


## Installation
This project was implemented using python version 3.10.11

To run the project locally:
- Create a virtual environment and install the packages in requirements.txt.
- run ```python manage.py makemigration``` to create the models.
- run ```python manage.py migrate``` to create the database.
- run ```python manage.py loaddata tables.json``` to load the table objects to the database.
- run ```python manage.py runserver``` to host the website on your localhost.

Note: the db server is listening on port:5050 as indicated in the ```settings.py``` file

The url routes are as follows:
- ```api/register/```: register new users.
- ```api/login/```: login using employee number and password.
- ```api/user/logout/```: log the user out.
- ```api/user/```: See the user details (employee id, name).
- ```api/user/reservations/```: see a list of all the current reservations.
- ```api/user/reservations/reserve/```: Create a new reservation.
- ```api/user/reservations/delete/```: Delete a reservation.


The project contains two apps:
- user_management
- reservations_app


## user_management

This app handles the registration and authentication of users. In ```views.py```, there are 4 API views:

- UserRegistrationAPIView
- UserLoginAPIView
- UserAPIView
- UserLogoutAPIView

### UserRegistrationAPIView

UserRegistrationAPIView handles two methods:  

```get(self, request)``` : Handles the GET request, and prompts the user to enter their info.  
```post(self, request)```: Handles the POST request, and creates a new user with the entered credentials along with a JWT token to log them in during the current session.


### UserLoginAPIView

UserLoginAPIView handles two methods:  

```get(self, request)``` : Handles the GET request, and prompts the user to enter their credentials.  
```post(self, request)```: Handles the POST request, and logs the user in, if the user exists, and generates a JWT token to log them in during the current session.


### UserAPIView

UserAPIView handles one method:  

```get(self, request)``` : Handles the GET request, and returns the user informations if the user is logged in, else it will raise AuthenticationFailed error.


### UserLogoutAPIView

UserLogoutAPIView handles one method:  

```get(self, request)``` : Handles the GET request, and gets the access token from the cookies in the browser and destroys it.


## reservation_app

This app handles the reservations after the user authenticates. In ```views.py```, there are 4 API views:

- ReservationAPIView
- NewReservationAPIView
- DeleteReservationAPIView
- CheckTimeSlotsAPIView


### ReservationAPIView

ReservationAPIView handles only one method:  

```get(self, request)``` : Handles the GET request, and lists all the reservations in the database (present, past, and future reservations).  


### NewReservationAPIView

NewReservationAPIView handles two methods:  

```get(self, request)``` : Handles the GET request, and prompts the user to enter the reservation details (start time, end time, date, number of seats).  
```post(self, request)```: Handles the POST request, creates a new reservation for the table with the given number of seats, or alert the user if the table is reserved for the given time.  


### DeleteReservationAPIView

DeleteReservationAPIView handles two methods:  

```get(self, request)``` : Handles the GET request, and prompts the user to enter reservation id, and list all the reservations of the current day that start after the current time.  
```post(self, request)```: Handles the POST request, delete the reservation of the given id unless the reservation has already started, finished, or is in another day.  


### CheckTimeSlotsAPIView (in progress)

CheckTimeSlotsAPIView handles two methods:  

```get(self, request)``` : Handles the GET request, and prompts the user to enter the desired number of seats.  
```post(self, request)```: Handles the POST request, and display the available time for the rest of the working day.

