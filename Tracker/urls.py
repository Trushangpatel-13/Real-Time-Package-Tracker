
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^signin/', views.signIn, name='login'),
    url(r'^postsign/', views.postsign),
    url(r'^about/', views.about),
    url(r'^map/', views.map),
    url(r'^service/', views.service, name='service'),
    url(r'^logout/', views.logout, name='logout'),


    url(r'^static/(?P<path>.*)$', serve,{'document_root':settings.STATIC_ROOT}),

]

