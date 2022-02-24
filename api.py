from __future__ import annotations

import xml.etree.ElementTree
from typing import List

import os

from django.http import HttpResponse
from rest_framework.exceptions import APIException

import logging
import django.core.exceptions

logger = logging.getLogger(__name__)
valid_extensions = ['.xls', '.xlsx', '.xl']

def get_prepared_dict(string, data) -> List[dict]:
    try:
        ready_data = {key: round(eval(string))
        for key, value in data.items()}

        return [ready_data]

    except TypeError:
        return get_prepared_dict('int(' + string + ')', data)

def check_file_extension(file):

    filename = file.name
    filename, extension = os.path.splitext(filename)

    if not extension in valid_extensions:
        raise django.core.exceptions.ValidationError(
        message='extension is not valid....')

def convert_to_datetime(dates) -> list:
    from dateutil import parser
    return [parser.parse(date) for date in dates.split(',')]

def get_source_data(source_credentials: dict) -> List[dict]:
    import pandas_datareader.data as web
    try:
        dataframe = web.DataReader(name=source_credentials['slot'], data_source=source_credentials['data_source_url'],
        start=source_credentials['points'][0], end=source_credentials['points'][1],

        api_key=source_credentials['api-key'])

        return get_prepared_dict(string='list(value.values())[0]',
        data=dataframe.to_dict())

    except xml.etree.ElementTree.ParseError as xml_err:
        logger.error('error has been occurred during parsing: %s' % xml_err.msg)
        raise APIException(xml_err)


import json
def process_exception(message: str, code) -> HttpResponse:
    response = HttpResponse(status=code)
    context = json.dumps({'error_message': message})
    response.content = context

    return response



