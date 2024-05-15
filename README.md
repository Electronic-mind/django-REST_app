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
