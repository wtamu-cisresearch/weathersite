from django.conf.urls import patterns, include, url

urlpatterns = patterns('weatherapp.views',
	url(r'^$', 'index'),
	url(r'^getdata/$', 'data_handler'),
)