from django.urls import path, include
from .views import UserRegisterView, UserEditView, PasswordsChangeView
from django.contrib.auth import views as auth_views
from . import views
#from UserRegister.views import CreateProfilePageView

urlpatterns = [
	
	#path('go/', UserRegisterView.as_view(), name='register'),
	path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
	#path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html')),
	path('password/', PasswordsChangeView.as_view(template_name='registration/change_password.html')),
	path('password_success', views.password_success, name='password_success'),
	path('register/' , views.register, name='register'),
	path('individual_register/' , views.individual_register.as_view(), name='individual_register'),
	path('organization_register/' , views.organization_register.as_view(), name='organization_register')
	#path('password_success', TemplateView.as_view(template_name='registration/password_success.html'),name='password_sucess')

]