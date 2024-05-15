# Restaurant reservation system using Django REST framwork

This project is a restaurant table reservation system that allows staff users to reserve tables for customers for a given date and time period.


## Installation
This project was implemented using python version 3.10.11

To run the project locally:
- Create a virtual environment and install the packages in requirements.txt.
- run ```python manage.py migrate``` to create the database.
- run ```python manage.py loaddata tables.json``` to load the table objects to the database.
- run ```python manage.py runserver``` to host the website on your localhost.

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

UserRegistrationAPIView has two methods:
```get(self, request)``` : Handles the GET request, and prompts the user to enter their info.
```post(self, request)```: Handles the 


