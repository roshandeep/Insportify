"""Insportify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .import views
from django.views.generic import TemplateView


urlpatterns = [
    path('', views.home, name='home'),
    #path('', views.User_Account.as_view(), name='user_account'),
    #path Converters
    #int : numbers
    #str : strings
    #path : whole urls /
    #slug : hyphen-and_underscores_stuff
    #path('', views.home, name="home"),
#    path('<int:year>/<str:month>/', views.home, name="home"),
    path('show/', views.all_events, name="list-events"),
    # path('add_venue/',views.add_venue, name='add-venue'),
    # path('list_venues/',views.list_venues, name='list-venues'),
    # path('show_venue/<venue_id>', views.show_venue, name='show-venue'),
    # path('add_event/',views.add_event, name='add-event'),
    # path('update_event/<event_id>',views.update_event, name='update-event'),
    # #path('', views.multiformvalidation, name='multiformvalidation'),
    #path('event_detail/',views.event_detail, name='event-detail'),
    path('profile/', views.user_profile, name='user_profile'),
    path('create/', views.multistep, name='multistep'),
#    path('add/', views.person_c    reate_view, name='person_add'),
#    path('<int:pk>/', views.person_update_view, name='person_change'),
    path('create/' , TemplateView.as_view(template_name='multi_step.html'),name='multistep'),
#    path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'), # AJAX
    #path('',TemplateView.as_view(template_name='multi_step.html'), name="multi-step"),
    #path('/multistep', views.multistep, name="multi-form")
    #path('multistepform_save/', views.multistepform_save, name='multistepform-save')
]