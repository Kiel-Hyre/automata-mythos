import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers

from django.shortcuts import render

from .generate.main import lex_execute

# Create your views here.
class LexxerExecuteView(APIView):
    class InputSerializer(serializers.Serializer):
        raw_data = serializers.CharField()

        def validate_raw_data(self, data):
            try:
                data = json.loads(data)
                if type(data) not in [list]:
                    raise serializers.ValidationError('Failed to load')
                return data
            except:
                raise serializers.ValidationError('Failed to load')

    class OutputSerializer(serializers.Serializer):
        value = serializers.CharField()
        title = serializers.CharField()
        description = serializers.CharField()
        line = serializers.IntegerField()


    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            data = lex_execute(data['raw_data'])
        except Exception as e:
            return Response(
                   { 'errors': str(e) }
                )

        return Response(
                {'lexxer': self.OutputSerializer(data, many=True).data}
            )