from rest_framework import serializers
from . import models

class ReservationSerializer(serializers.ModelSerializer):

    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    date = serializers.DateField()
    seats_needed = serializers.IntegerField(max_value=6, min_value=1)
    table = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    employee = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = models.Reservation
        fields = ['start_time', 'end_time', 'date', 'seats_needed', 'table', 'employee']


class DeleteReservationSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()