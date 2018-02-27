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
    url(r'^roadsheet_delete/(?P<sheet_id>[0-9]+)/$', views.roadsheet_delete, name='roadsheet_delete'),
    url(r'^roadsheet_close/(?P<sheet_id>[0-9]+)/$', views.roadsheet_close, name='roadsheet_close'),

    # ТМЦ
    url(r'^doc_add_tmc/(?P<sheet_id>[0-9]+)/$', views.doc_add_tmc, name='doc_add_tmc'),
    url(r'^doc_add_tmc/$', views.doc_add_tmc, name='doc_add_tmc'),

    # Запросы на ремонт
    url(r'^doc_create_request/$', views.doc_create_request, name='doc_create_request'),
    url(r'^doc_create_request///$', views.doc_create_request, name='doc_create_request'),
    url(r'^doc_create_request/(?P<sheet_id>[0-9]+)/(?P<tablet_id>[0-9]+)/$', views.doc_create_request, name='doc_create_request'),

    # Сервисмен
    url(r'^request/(?P<req_id>[0-9]+)/get_to_sc$', views.req_get_to_sc, name='req_get_to_sc'),
    url(r'^request/(?P<req_id>[0-9]+)/get_from_sc$', views.req_get_from_sc, name='req_get_from_sc'),
    url(r'^request/(?P<req_id>[0-9]+)/get_foolish$', views.req_get_foolish, name='req_get_foolish'),
    url(r'^request/(?P<req_id>[0-9]+)/get_lost$', views.req_get_lost, name='req_get_lost'),


    url(r'^doc_part_tablet_sim/', views.doc_part_tablet_sim, name='doc_part_tablet_sim'),
    url(r'^doc_apart_tablet_sim/(?P<doc_id>[0-9]+)/$', views.doc_apart_tablet_sim, name='doc_apart_tablet_sim'),
    url(r'^doc_quality_tablet/', views.doc_quality_tablet, name='doc_quality_tablet'),
    url(r'^print/(?P<sheet_id>[0-9]+)/$', views.print_roadsheet, name='print_roadsheet'),


    # REPORTS
    url(r'^rep_osago/$', views.rep_osago, name='rep_osago'),
    url(r'^rep_to/$', views.rep_to, name='rep_to'),


]
