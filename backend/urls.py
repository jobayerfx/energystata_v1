from django.conf.urls import url
from . import views
#from backend.dash_apps import simple_graph
from backend.dash_apps import consumption
from backend.dash_apps import ar_working
urlpatterns = [
    url('', views.index, name='index')
]
