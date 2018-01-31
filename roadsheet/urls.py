# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.start, name='start'),
    #url(r'^contacts/', views.contacts, name='contacts'),
    #url(r'^userrequest/', views.userrequest, name='userrequest'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),

    # Путевые листы
    url(r'^roadsheet/(?P<sheet_id>[0-9]+)/$', views.roadsheet, name='roadsheet'), #OK
    url(r'^roadsheet/', views.roadsheet, name='roadsheet'), # OK
    url(r'^roadsheet_open/(?P<sheet_id>[0-9]+)/$', views.roadsheet_open, name='roadsheet_open'), # OK
    url(r'^roadsheet_close/(?P<sheet_id>[0-9]+)/$', views.roadsheet_close, name='roadsheet_close'),
    url(r'^roadsheet_delete/(?P<sheet_id>[0-9]+)/$', views.roadsheet_delete, name='roadsheet_delete'),


    url(r'^doc_add_tmc/', views.doc_add_tmc, name='doc_add_tmc'),

    url(r'^doc_part_tablet_sim/', views.doc_part_tablet_sim, name='doc_part_tablet_sim'),
    url(r'^doc_apart_tablet_sim/(?P<doc_id>[0-9]+)/$', views.doc_apart_tablet_sim, name='doc_apart_tablet_sim'),
    url(r'^doc_quality_tablet/', views.doc_quality_tablet, name='doc_quality_tablet'),
    url(r'^print/(?P<sheet_id>[0-9]+)/$', views.print_roadsheet, name='print_roadsheet'),






]
