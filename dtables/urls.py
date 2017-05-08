from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^columns/(?P<table_id>[0-9]+)/$', views.edit_columns, name='edit_columns'),
    url(r'^table/(?P<table_id>[0-9]+)/$', views.table_view, name='table_view'),
    url(r'^get_tables/$', views.get_tables, name='get_tables'),
    url(r'^add_table/$', views.add_table, name='add_table'),
    url(r'^delete_table/$', views.delete_table, name='delete_table'),
    url(r'^update_table/$', views.update_table, name='update_table')
]
