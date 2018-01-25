from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.start, name='start'),
    #url(r'^contacts/', views.contacts, name='contacts'),
    #url(r'^userrequest/', views.userrequest, name='userrequest'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),
    url(r'^add_roadsheet/', views.roadsheet, name='add_roadsheet'),
    url(r'^doc_part_tablet_sim/', views.doc_part_tablet_sim, name='doc_part_tablet_sim'),
    url(r'^doc_apart_tablet_sim/(?P<doc_id>[0-9]+)/$', views.doc_apart_tablet_sim, name='doc_apart_tablet_sim'),
    url(r'^doc_quality_tablet/', views.doc_quality_tablet, name='doc_quality_tablet'),
    url(r'^print/(?P<sheet_id>[0-9]+)/$', views.print_roadsheet, name='print_roadsheet'),
    url(r'^begin_route/(?P<sheet_id>[0-9]+)/$', views.begin_route, name='begin_route'),
    url(r'^delete/(?P<sheet_id>[0-9]+)/$', views.delete_route, name='delete_route'),
    url(r'^edit/(?P<sheet_id>[0-9]+)/$', views.roadsheet, name='edit_draft'),
    url(r'^save_draft/', views.roadsheet, name='save_draft'),
    url(r'^close_route/(?P<sheet_id>[0-9]+)/$', views.close_route, name='close_route'),
    #url(r'^profile/', views.profile, name='profile'),

]
