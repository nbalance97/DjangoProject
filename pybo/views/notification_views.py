from django.http.response import Http404
from django.core.exceptions import PermissionDenied
from ..models import Notification
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..serializer import NotificationSerializer


def make_notifications(target_user, content, question):
    return Notification.objects.create(
        user = target_user,
        content = content,
        question = question
    )

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    MAX_NOTIFICATION_COUNT = 15
    
    @action(detail=False, methods=['get'])
    def get_notification_information(self, request):
        if request.user.is_authenticated:
            notification = Notification.objects.filter(user=request.user, isread=False)[:self.MAX_NOTIFICATION_COUNT]
            serializer = self.get_serializer(notification, many=True)
            return Response(serializer.data)
        else:
            return PermissionDenied()
    
    @action(detail=True, methods=['get'])
    def change_notification_status(self, request, pk=None):
        if request.user.is_authenticated:
            notification = self.get_object()
            if notification != None:
                notification.isread = True
                notification.save()
                return Response({'status':'save successfully'})
            else:
                return Response({'status':'save failed'})
        else:
            return PermissionDenied()




