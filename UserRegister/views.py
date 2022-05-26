from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, AuthenticationForm
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfileForm
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import DetailView, CreateView
from EventsApp.models import User
from UserRegister.forms import IndividualSignUpForm, OrganizationSignUpForm, PasswordResetAuthForm
from django.contrib.auth import login, logout, authenticate
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token, pass_reset_code
from django.core.mail import EmailMessage
import random
import string

def register(request):
    user = User
    return render(request, 'registration/register_final.html', {'user': user})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(username=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'registration/invalid_acc_token.html', {})

class individual_register(CreateView):
    model = User
    form_class = IndividualSignUpForm
    template_name = 'registration/individual_register.html'

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            mail_subject = 'Welcome to Insportify!'

            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': "127.0.0.1:8000",
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.username))),
                'token': account_activation_token.make_token(user),
            })
            message = message
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            #return HttpResponse('Please confirm your email address to complete the registration')
        login(self.request, user)
        return redirect('/')


class organization_register(CreateView):
    model = User
    form_class = OrganizationSignUpForm
    template_name = 'registration/organization_register.html'

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            mail_subject = 'Welcome to Insportify!'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': "127.0.0.1",
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.username))),
                'token': account_activation_token.make_token(user),
            })
            message = message
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            #return HttpResponse('Please confirm your email address to complete the registration')
        login(self.request, user)
        return redirect('/')


def login_request(request):
    if request.method == 'POST':
        print(request)
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    return render(request, '../templates/login.html',
                  context={'form': AuthenticationForm()})


def logout_view(request):
    logout(request)
    return redirect('/')


class password_reset(generic.CreateView):
    model = User
    form_class = PasswordResetAuthForm
    template_name = 'registration/change_password_auth.html'
    print(form_class)

    def form_valid(self, form):
        if form.is_valid():
            #user = form.save()
            #user.save()
            mail_subject = 'Password Reset Request from Insportify'

            message = render_to_string('acc_pass_reset_email.html', {
                'token': ''.join(random.choice(string.ascii_lowercase) for i in range(5)),
            })
            message = message
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
        # login(self.request, user)
        return redirect('/')

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('list-events')


def password_success(request):
    return reverse_lazy(request, 'registration/password_success.html', {})


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('list-events')

    def get_object(self):
        return self.request.user
