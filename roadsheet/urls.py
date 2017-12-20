from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.start, name='start'),
    #url(r'^contacts/', views.contacts, name='contacts'),
    #url(r'^userrequest/', views.userrequest, name='userrequest'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    #url(r'^profile/', views.profile, name='profile'),

]
