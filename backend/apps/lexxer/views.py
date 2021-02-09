from rest_framework.views import APIView
from rest_framework.response import Response

from django.shortcuts import render


# Create your views here.
class LexxerExecuteView(APIView):

    def post(self, request, *args, **kwargs):
        return Response(
                {'hello': 'world'}
            )