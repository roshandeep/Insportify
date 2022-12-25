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
from . import views
from django.views.generic import TemplateView

# from .views import CheckoutSessionView

app_name = 'EventsApp'

urlpatterns = [
    path('', views.home, name='home'),
    path('show/', views.all_events, name="list-events"),
    path('committed/', views.committed_events, name="committed_events"),
    path('individual/profile/', views.user_profile, name='user_profile'),
    path('organization/profile/', views.organization_profile, name='organization_profile'),
    path('create/', views.multistep, name='multistep'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    # path('<int:event_id>/', views.event_by_id, name='event_by_id'),
    path('invite/<int:event_id>/', views.invite_by_id, name='invite_by_id'),
    path('invite/<int:event_id>/<str:email>/', views.invite_by_id, name='invite_by_id'),
    path('invite/', views.invite, name='invite'),
    path('delete/<int:event_id>/<str:date>/', views.delete_by_id, name='delete_by_id'),
    path('get_selected_sports_type/', views.get_selected_sports_type, name='get_selected_sports_type'),
    path('get_sports_type/', views.get_sports_type, name='get_sports_type'),
    path('get_sports_skill/', views.get_selected_sports_skill, name='get_selected_sports_skill'),
    path('get_sports_position/', views.get_selected_sports_positions, name='get_selected_sports_positions'),
    path('get_sports_position_and_skill/', views.get_selected_sports_position_and_skill,
         name='get_selected_sports_position_and_skill'),
    path('add_sports_positions/', views.add_sports_positions, name='add_sports_positions'),
    path('fetch_user_sports_positions/', views.fetch_user_sports_positions, name='fetch_user_sports_positions'),
    path('delete_sports_choice/', views.delete_sports_choice, name='delete_sports_choice'),
    path('add_user_locations/', views.add_user_locations, name='add_user_locations'),
    path('fetch_user_locations/', views.fetch_user_locations, name='fetch_user_locations'),
    path('delete_user_location/', views.delete_user_location, name='delete_user_location'),
    path('get_venue/', views.get_venue_details, name='get_venue'),
    path('add_organization_locations/', views.add_organization_locations, name='add_organization_locations'),
    path('fetch_organization_locations/', views.fetch_organization_locations, name='fetch_organization_locations'),
    path('get_organization_timings/', views.get_organization_timings, name='get_organization_timings'),
    path('get_user_availability/', views.get_user_availability, name='get_user_availability'),
    path('add_user_availability/', views.add_user_availability, name='add_user_availability'),
    path('delete_availability/', views.delete_availability, name='delete_availability'),
    path('upload/', views.logo_upload_view, name='logo_upload'),
    path('event_details/<int:event_id>/<str:event_date>/', views.event_details, name='event_details'),
    path('cart_summary/', views.cart_summary, name='cart_summary'),
    path('delete_cart_item/', views.delete_cart_item, name='delete_cart_item'),
    path('fetch_cart_items/', views.fetch_cart_items, name='fetch_cart_items'),
    path('show_advertisement/<str:header>/', views.show_advertisement, name='show_advertisement'),

    # PAYMENT URL'S
    path('payment-success/', views.paymentSuccess, name='payment-success'),
    path('payment-cancel/', views.paymentCancel, name='payment-cancel'),
    path('charge/', views.charge, name='charge'),
    path('pay_at_venue/', views.pay_at_venue, name='pay_at_venue'),
]
