from rest_framework import serializers
from .models import Notification, Question

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'content', 'arrive_date', 'isread', 'question']