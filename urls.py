from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [

    path('get/file/datasource/data/', views.GetFileSourceDataView.as_view(), name='file-datasource-data'),
    path('get/session/data/', views.GetSessionSourceDataView.as_view(), name='session-data'),

    path('validate/stock/form/', views.validate_stock_form, name='validate-stock-form'),
    path('validate/file/form/', views.validate_file_form, name='validate-file-form'),

    path('', views.get_user_chart, name='get_chart'),
    path('get/stock/form/', views.get_stock_form, name='get-stock-form'),

    path('get/file/form/', views.get_file_page, name='get-file-form'),
    path('get/datasource/data/', views.GetDataSourceInfoApiView.as_view(), name='datasource-data'),

]









