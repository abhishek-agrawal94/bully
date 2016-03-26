from django.conf.urls import patterns, include, url
from HelloWorldApp import views
from django.views.generic import TemplateView


from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
	url(r'home/$',TemplateView.as_view(template_name='/home/husen/HelloWorld/HelloWorldApp/templates/index.html'),name="home"),
	url(r'form/$',views.form,name='form'),
	url(r'^form/output/$',views.return_data,name='return_data'),
    
)

