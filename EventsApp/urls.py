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
    path('individual/profile/', views.user_profile, name='user_profile'),
    path('organization/profile/', views.organization_profile, name='organization_profile'),
    path('create/', views.multistep, name='multistep'),
    path('<int:event_id>/', views.event_by_id, name='event_by_id'),
    path('get_selected_sports_type/', views.get_selected_sports_type, name='get_selected_sports_type'),
    path('get_sports_category/', views.get_sports_category, name='get_sports_category'),

    # path('orderSummary/<pk>/', views.order_summary, name='orderSummary'),
    path('payment-success/', views.paymentSuccess, name='payment-success'),
    path('payment-cancel/', views.paymentCancel, name='payment-cancel'),
    path('create-checkout-session/<id>/', views.create_checkout_session, name='create-checkout-session'),
]
