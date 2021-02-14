import json

from django.core.exceptions import ValidationError
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status

from .generate.lex import Lexxer, LexicalValidationError
from .generate.syntax import Syntax


from .generate.myth.lex import parse as lex_parse
from .generate.myth.syn import parse as syn_parse

# Create your views here.
class LexxerExecuteView(APIView):
    class InputSerializer(serializers.Serializer):
        raw_data = serializers.CharField(required=False)
        start_line = serializers.IntegerField(required=False)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['raw_data'].strip = False

    class ErrorSerializer(serializers.Serializer):
        code = serializers.CharField()
        line = serializers.IntegerField()
        char_line = serializers.IntegerField()
        message = serializers.CharField()

    class LexOutputSerializer(serializers.Serializer):
        type = serializers.CharField()
        value = serializers.CharField()
        description = serializers.CharField()
        lineno = serializers.IntegerField()
        char_line = serializers.IntegerField()

    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)
        ERROR_LIST = []

        response = {'success': False, 'errors':[], 'data': None}
        if serializer.is_valid():
            data = serializer.validated_data
            print(data)
            try:
                lexical, syntax = syn_parse(
                data.get('raw_data',''), data.get('start_line', 1), True)
            except Exception as e:
                if hasattr(e, 'error_list'):
                    response['errors'].extend(self.ErrorSerializer(e.error_list,
                        many=True).data)
                else: raise Exception(e)

            if not response['errors']:
                response['success'] = True
                response['data'] ={
                    'lexical': self.LexOutputSerializer(lexical,
                        many=True).data,
                    'syntax': syntax
                }
        else:
            response['errors'] = serializer.errors
        return Response(response, status=status.HTTP_200_OK)