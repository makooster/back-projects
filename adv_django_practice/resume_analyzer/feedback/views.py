from rest_framework import viewsets, permissions
from .models import Feedback
from .serializers import FeedbackSerializer

class FeedbackViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(resume__user=self.request.user)
