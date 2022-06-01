from django.urls import path, include
from .views import UserRegisterView, UserEditView, PasswordsChangeView
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls import url

# from UserRegister.views import CreateProfilePageView

app_name = 'UserRegister'

urlpatterns = [
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('individual_register/', views.individual_register.as_view(), name='individual_register'),
    path('organization_register/', views.organization_register.as_view(), name='organization_register'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path("password_reset/", views.password_reset_request,
        name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),

]
