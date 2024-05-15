from .models import Reservation, Table
from datetime import datetime, date
from django.db.models import Q

def is_reserved(start_time, end_time, table) -> bool:
    '''Check if the table is booked for the given time interval.'''
    return Reservation.objects.filter(table_id=table.pk, start_time__lt=end_time, end_time__gt=start_time).exists()
     


def get_table(seats) -> Table:
    '''Get the table for the given number of seats.'''
    # if the number of seats requested is 2 or 1
    if seats <= 2  and seats > 0:
        tables = list(Table.objects.filter(no_of_seats='2'))
        return tables if tables else 'No tables are available with the specified number of seats.'
    
    # if the number of seats requested is 4 or less
    elif seats <= 4:
        table = Table.objects.get(no_of_seats='4')
        return table if table else 'No tables are available with the specified number of seats.'
    
    # if the number of seats requested is 6 or less
    elif seats <= 6:
        table = Table.objects.get(no_of_seats='6')
        if table :
            return table if table else 'No tables are available with the specified number of seats.'
    
    else:
        # if the number of seats requested is greater than 6/ less than 1
        return 'No tables are available with this number of seats.'
    
def get_available_time_slots(table):
    '''Retrieve the available time slots'''
    reservations = Reservation.objects.filter(start_time=datetime.now().time(), table=table, date=date.today())
    if reservations.exists():
        available_time = reservations.filter()
    else:
        return f"{datetime.now().strftime('%H:%M %p')} - 11:59 PM"

