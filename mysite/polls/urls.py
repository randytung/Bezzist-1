from django.conf.urls import patterns, url
from polls import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(),
        name='index'), #ex: /polls/
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(),
        name='detail'), #ex: /polls/5/
    url(r'^(?P<pk>\d+)/results/$', views.ResultsView.as_view(),
        name='results'),#ex: /polls/5/results
    url(r'^(?P<question_id>\d+)/vote/$', views.vote,
        name='vote'),#ex: /polls/5/vote
     url(r'^(?P<question_id>\d+)/add/$', views.add,
        name='add'),#ex: /polls/5/add
     url(r'^addq/$', views.addq,
        name='addq'),#ex: /polls/add
)
