import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status

from django.shortcuts import render

from .generate.main import LexExecute


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

        def validate(self, data):
            data = super().validate(data)

            try:
                data['lex_data'] = LexExecute().execute(data.get('raw_data'))
            except serializers.ValidationError as v:
                raise serializers.ValidationError(v, code='root')
            return data

    class OutputSerializer(serializers.Serializer):
        value = serializers.CharField()
        title = serializers.CharField()
        description = serializers.CharField()
        line = serializers.IntegerField()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)

        response = {'success': False, 'errors':[], 'data': None}
        if serializer.is_valid():
            data = serializer.validated_data
            response['success'] = True
            response['data'] = self.OutputSerializer(
                data['lex_data'], many=True).data
        else:
            response['errors'] = serializer.errors
        return Response(response, status=status.HTTP_200_OK)
