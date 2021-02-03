from django.urls import path
from rest_framework.response import Response
from rest_framework.views import APIView


class PingView(APIView):

    def get(self, *args, **kwargs):
        return Response({'hello': 'world'})


urlpatterns = [
    path('ping/', PingView.as_view(), name='ping'),
]
