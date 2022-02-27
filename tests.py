from django.core.files.uploadedfile import InMemoryUploadedFile, SimpleUploadedFile, UploadedFile
from django.test import TestCase
from django.urls import reverse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework.test import APIRequestFactory, APIClient, RequestsClient
import pandas, os, io, json
# Create your tests here.

import datetime
from rest_framework import status

class PagesAPITestCase(TestCase):

    def setUp(self):
        self.client = RequestsClient()

    def test_main_chart_page(self):
        response = self.client.get('http://testserver/')
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_file_form_page(self):
        response = self.client.get('http://testserver/get/file/form/')
        self.assertEquals(status.HTTP_200_OK, response.status_code)

    def test_stock_page(self):
        response = self.client.get('http://testserver/get/stock/form/')
        self.assertEquals(status.HTTP_200_OK, response.status_code)


class DataSourcesAPITestCase(TestCase):

    def setUp(self):

        self.data = {
            'points': [datetime.datetime(2021, 12, 1), datetime.datetime(2021, 12, 2)],
            'data_source_url': 'test-source-url',
            'slot': 'test-slot'
        }
        self.urls = {
            'file-source-url': "http://testserver/get/file/datasource/data/",
            'stock-source-url': "http://testserver/get/datasource/data/"
        }

    def test_data_source_request(self):

        client = RequestsClient()
        url = self.urls['stock-source-url']
        response = client.get(url, data=self.data)

        self.assertEquals(response.status_code, 200)

    def test_excel_data_source_request(self):
        """Sending File XLS Request...."""

        link = 'C:\\Users\dell\Desktop\some_list.xlsx' # This suppose to be a file address...
        post_url = self.urls['file-source-url']
        file = open(link, 'rb')

        response = self.client.post(post_url, data={'file': file}, format='multipart')
        self.assertEqual(response.status_code, 200)

# C:\Users\dell\Desktop\ChartProject\ChartProject\manage.py test main.tests.TestAPIValidatorsTestCase

class TestAPIValidatorsTestCase(TestCase):

    def setUp(self):
        self.urls = {
            'form-file-url': 'http://testserver/validate/file/form/',
            'form-source-url': 'http://testserver/validate/stock/form/',
        }

    def test_form_file_validator(self):
        link = 'C:\\Users\dell\Desktop\some_list.xlsx' # need to specify file url...

        post_url_address = self.urls['form-file-url']
        file = open(link, 'rb')
        response = self.client.post(post_url_address, data={'file': file}, format='multipart')
        self.assertEquals(response.status_code, 200, msg='ERROR has been occurred, status:' \
        ' %s' % response.status_code)


    def test_stock_form_validator(self):
        client = RequestsClient()
        data = {
            'source_url': 'some-source-url',
            'slot': 'some-slot',
            'api_key': 'some-api-key'
        }
        request_url = self.urls['form-source-url']
        response = client.post(request_url, data=data)
        data = json.loads(response.text)

        self.assertIn(container=data, member='is_valid', msg='Data does not contains validation status')
        self.assertEquals(response.status_code, 200, msg='Response Should be with status 200')











