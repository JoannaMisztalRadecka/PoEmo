from django.conf.urls import url

from . import views

app_name = 'poetry_generator'
urlpatterns = [
    # url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^$', views.make_poem, name='make_poem'),
    url(r'^(?P<text_id>[0-9]+)/$', views.detail, name='detail'),
    # # url(r'^select/$', views.select, name='select'),
    url(r'^(?P<inspiration_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<poem_id>[0-9]+)/poem/$', views.poem, name='poem'),
    # # ex: /polls/5/vote/
    # url(r'^(?P<inspiration_id>[0-9]+)/vote/$', views.vote, name='vote'),
]