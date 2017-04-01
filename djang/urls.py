from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^columns/(?P<table_id>[0-9]+)/$', views.edit_columns, name='edit_columns'),
    url(r'^table/(?P<table_id>[0-9]+)/$', views.table_view, name='table_view'),
]

