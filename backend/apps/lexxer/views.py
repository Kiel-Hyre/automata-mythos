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
        raw_data = serializers.CharField(required=False, allow_blank=True)
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
            # print(data)

            lexical, syntax = [], False

            # try:
            #     lexical = lex_parse(
            #         data.get('raw_data',''), data.get('start_line', 1))
            # except Exception as e:
            #     if hasattr(e, 'error_list'):
            #         response['errors'].extend(self.ErrorSerializer(e.error_list,
            #         many=True).data)
            #     else: raise Exception(e)


            lexical_dict = lex_parse(
                    data.get('raw_data', ''), data.get('start_line', 1))

            if lexical_dict['errors']: response['errors'].extend(
                self.ErrorSerializer(lexical_dict['errors'], many=True).data)

            # try:
            #     syntax = syn_parse(data.get('raw_data',''), data.get('start_line', 1))
            # except Exception as e:
            #     if hasattr(e, 'error_list'):
            #         response['errors'].extend(self.ErrorSerializer(
            #             e.error_list, many=True).data)
            #     else: raise Exception(e)

            syn_lex_token, syn_bool, syn_errors = syn_parse(data.get('raw_data',''),
                    data.get('start_line', 1))

            if syn_errors: response['errors'].extend(
                self.ErrorSerializer(syn_errors, many=True).data)

            # if response['errors']:
            #     return Response(response, status=status.HTTP_200_OK)

            if not response['errors']: response['success'] = True
            response['data'] ={
                'lexical': self.LexOutputSerializer(lexical_dict['data'],
                    many=True).data,
                'syntax': syn_bool
            }
        else:
            response['errors'] = serializer.errors
        return Response(response, status=status.HTTP_200_OK)