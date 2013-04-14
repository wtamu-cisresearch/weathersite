from django.conf.urls import patterns, include, url

urlpatterns = patterns('weatherapp.views',
	url(r'^$', 'index'),
	url(r'^getdata/$', 'data_handler'),
	url(r'^csvexport/$', 'csv_export'),
)