from django.conf.urls import url

from . import views

urlpatterns = [
            url(r'^$', views.index, name='index'),
            url(r'insert/', views.insert),
            url(r'delete/', views.delete),
            url(r'update/', views.update),
            url(r'thanks/', views.thanks)
            ]
