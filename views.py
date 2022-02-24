from typing import List, Generator

import django
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render

import json

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control, cache_page
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny

from rest_framework.renderers import JSONRenderer
from rest_framework_csv.renderers import CSVStreamingRenderer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from . import api, serializers, forms

import logging, urllib.parse
import datetime

logger = logging.getLogger(__name__)

@api_view(['GET'])
@permission_classes([AllowAny])
@cache_page(60 * 60)
def get_user_chart(request):
    context = {'title': 'Chart'}
    template_name = 'main/index.html'

    return render(request, template_name, context)


class GetDataSourceInfoApiView(APIView):
    """API Class that parses data with DataReader using credential data specified in GET request...."""

    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer, )

    @cache_page(60 * 2)
    def get(self, request):

        credentials = {

         # SLOT: param user is looking for on DataSource....
         #  POINTS: start and end dates for Data Source Parsing
         # SOURCE_URL: Name of the source to parse from... 'quantl', 'stooq', etc...
         #API-KEY: Not Required.... But Necessary for Private Data Sources which requires api-keys

        'slot': urllib.parse.unquote(request.query_params['slot']),
        'data_source_url': request.query_params.get('data_source_url').lower(),

        'points': api.convert_to_datetime(request.query_params.get('points')),
        'api-key': request.get_signed_cookie('api-key')
        }

        if credentials['points'] and not all([isinstance(point, datetime.datetime) for point in credentials['points']]):
            logger.debug('start/end points need to be a datetime object, not anything else...')
            return HttpResponseBadRequest()

        try:
            serialized_data = api.get_source_data(source_credentials=credentials)
            request.session['source_data'] = serialized_data
            return JsonResponse({'session_key': request.session.session_key})

        except APIException:
            message = 'Invalid Credentials'
            return api.process_exception(message, code=status.HTTP_400_BAD_REQUEST)

class GetSessionSourceDataView(APIView):

    """
    Streaming data, rendered to accept request header format
    getting access to data by session key from request GET parameters)
    """

    permission_classes = (AllowAny,)
    renderer_classes = (CSVStreamingRenderer, JSONRenderer)

    @cache_control(private=True)
    @method_decorator(cache_page(60 * 2))
    def get(self, request):

        sess_id = request.query_params.get('session_key')
        try:
            # from django.contrib.sessions.backends.cache import SessionStore
            session = Session.objects.get(session_key=sess_id)
            data = session.get_decoded()['source_data']

            logger.debug('session data has been recovered.....')
            return self.stream_http_response(request, data=data, content_type='text/csv')

        except (KeyError, ObjectDoesNotExist):
            logger.debug('session not found with this session_key: %s' % sess_id)

    def stream_http_response(self, request, data: List[dict], content_type: str):

        response = django.http.StreamingHttpResponse(streaming_content=request.accepted_renderer.render(
        self.stream_source_data(data)), content_type=content_type)

        response['Content-Disposition'] = 'attachment; filename=data_source.%s' \
        % content_type.split('/')[1]

        logger.debug('returning csv chunks data.....')
        return response

    def stream_source_data(self, data: List[dict]) -> Generator:
        for elem in data:
            yield json.dumps(elem)

@csrf_exempt
def validate_stock_form(request):

    context = {'is_valid': False}
    serializer = serializers.StockSerializer(data=request.POST, many=False)
    if serializer.is_valid(raise_exception=True):
        context.update({'is_valid': True})

    response = JsonResponse(context)

    response.set_signed_cookie(key='api-key', value=request.POST.get('api_key'))\
    if serializer.is_valid(raise_exception=True) and request.POST['api_key'] else None

    return response

@csrf_exempt
def validate_file_form(request):
    context = {'is_valid': False}
    file = request.FILES.get('file')
    try:
        api.check_file_extension(file)
        context.update({"is_valid": True})

    except ValidationError as val_err:
        logger.debug('form is not valid %s' % val_err.message)

    return JsonResponse(context)

@cache_page(60 * 2)
def get_stock_form(request):

    context = {}
    context['form'] = forms.StockForm()
    template_name = 'main/stock.html'

    return render(request, template_name, context)

@cache_page(60 * 2)
def get_file_page(request):

    template_name = 'main/file_upload.html'
    form = forms.FileForm()
    return render(request, template_name, {'form': form})

class GetFileSourceDataView(APIView):

    """
    Used to read data from file with xls formats and save it to current session, (
    to get some access later)
    """

    permission_classes = (AllowAny, )
    renderer_classes = (JSONRenderer, )

    @cache_control(private=True)
    def post(self, request): # Currently can work only with files that have only 1 list.....

        if 'file' in request.FILES:
            file = request.FILES['file']

            serialized_data = api.get_prepared_dict('list(value.values())[0]',
            self.parse_xl_file_data(file))

            request.session['source_data'] = serialized_data
            return JsonResponse({'session_key': request.session.session_key})

    def parse_xl_file_data(self, file):
        import pandas
        datalist = {}

        ex_file = pandas.ExcelFile(file)
        for sheet in ex_file.sheet_names:
            datalist.update(**ex_file.parse(sheet_name=sheet).to_dict())

        return datalist






