from django.contrib import messages
from django.shortcuts import render,redirect
from django.views import generic
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm, AuthenticationForm
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfileForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import DetailView, CreateView
from django.db.models.query_utils import Q
from EventsApp.models import User
from UserRegister.forms import IndividualSignUpForm, OrganizationSignUpForm, PasswordResetAuthForm
from django.contrib.auth import login, logout, authenticate
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token, pass_reset_code
from django.core.mail import EmailMessage


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


def logout_request(request):
    logout(request)
    return redirect('/')


class individual_register(CreateView):
    model = User
    form_class = IndividualSignUpForm
    template_name = 'registration/individual_register.html'

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            email = EmailMessage(
                'Welcome to Insportify!',
                render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': self.request.get_host(),
                    'uid': force_text(urlsafe_base64_encode(force_bytes(user.username))),
                    'token': account_activation_token.make_token(user),
                }),
                to=[form.cleaned_data.get('email')]
            )
            email.send()
            messages.success(self.request, 'Account created! Please confirm your email address to complete the '
                                           'registration')
        return redirect('/users/individual_register')


class organization_register(CreateView):
    model = User
    form_class = OrganizationSignUpForm
    template_name = 'registration/organization_register.html'

    def form_valid(self, form):
        print(form)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            email = EmailMessage(
                'Welcome to Insportify!',
                render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': self.request.get_host(),
                    'uid': force_text(urlsafe_base64_encode(force_bytes(user.username))),
                    'token': account_activation_token.make_token(user),
                }),
                to=[form.cleaned_data.get('email')]
            )
            email.send()
            messages.success(self.request, 'Account created! Please confirm your email address to complete the '
                                           'registration')
        return redirect('/users/organization_register')


def login_request(request):
    if request.method == 'POST':
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
    return render(request, 'registration/login.html', context={'form': AuthenticationForm()})


def logout_view(request):
    logout(request)
    return redirect('/')


class password_reset(generic.CreateView):
    model = User
    form_class = PasswordResetAuthForm
    template_name = 'registration/password_reset.html'

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            email = EmailMessage(
                'Password Reset Request from Insportify',
                render_to_string('acc_pass_reset_email.html', {
                    'user': user,
                    'domain': self.request.get_host(),
                    'uid': force_text(urlsafe_base64_encode(force_bytes(user.username))),
                    'token': pass_reset_code.make_token(user),
                }),
                to=[form.cleaned_data.get('email')]
            )
            email.send()
        # login(self.request, user)
        return redirect('/')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    email = EmailMessage(
                        'Password Reset Request from Insportify',
                        render_to_string('acc_pass_reset_email.html', {
                            'user': user,
                            'domain': request.get_host(),
                            'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                            'token': default_token_generator.make_token(user),
                        }),
                        to=[password_reset_form.cleaned_data.get('email')]
                    )
                    email.send()
                    return redirect("/users/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="registration/password_reset.html",
                  context={"password_reset_form": password_reset_form})


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('list-events')


def password_success(request):
    return reverse_lazy(request, 'registration/password_reset_complete.html', {})


class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')



