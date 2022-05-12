from django.urls import path, include
from .views import UserRegisterView, UserEditView, PasswordsChangeView
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import url

# from UserRegister.views import CreateProfilePageView

urlpatterns = [
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    #path('password/', PasswordsChangeView.as_view(template_name='registration/change_password.html')),
    path('password/', views.password_reset.as_view(), name='password_reset'),
    path('password_success', views.password_success, name='password_success'),
    path('register/', views.register, name='register'),
    path('individual_register/', views.individual_register.as_view(), name='individual_register'),
    path('organization_register/', views.organization_register.as_view(), name='organization_register'),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #         views.activate, name='activate')
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]
