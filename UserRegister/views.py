from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm, AuthenticationForm
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import DetailView, CreateView
from django.db.models.query_utils import Q
from EventsApp.models import User
from UserRegister.forms import IndividualSignUpForm, OrganizationSignUpForm, PasswordResetAuthForm, MVPSignUpForm
from django.contrib.auth import login, logout, authenticate
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token, pass_reset_code
from django.core.mail import EmailMessage


def register(request):
    return render(request, 'registration/register_final.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(email=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        if user.is_individual:
            return redirect('EventsApp:user_profile')
        elif user.is_organization:
            return redirect('EventsApp:organization_profile')
        # return redirect('/')
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
        localhost = '127.0.0.1:8000'
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.is_mvp = False  # self.request.POST.get('is_mvp') == "on"
            user.save()

            is_localhost = get_current_site(self.request).domain == localhost

            if is_localhost:
                ssl = 'http://'
            else:
                ssl = 'https://'
            domain = ''.join([ssl, get_current_site(self.request).domain])
            email = EmailMessage(
                'Welcome to Insportify!',
                render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': domain,
                    'uid': force_text(urlsafe_base64_encode(force_bytes(user.email))),
                    'token': account_activation_token.make_token(user),
                }),
                to=[form.cleaned_data.get('email')]
            )
            if is_localhost:
                print(email.body)
            else:
                print(email.body)
                email.send()
            messages.success(self.request,
                             'Account created! A verification email has been sent to your email address. Please confirm your email address to complete the registration.')
        return redirect('/users/individual_register')


class mvp_register(CreateView):
    model = User
    form_class = MVPSignUpForm
    template_name = 'registration/mvp_register.html'

    def form_valid(self, form):
        localhost = '127.0.0.1:8000'
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.is_mvp = True
            user.save()

            is_localhost = get_current_site(self.request).domain == localhost

            if is_localhost:
                ssl = 'http://'
            else:
                ssl = 'https://'
            domain = ''.join([ssl, get_current_site(self.request).domain])
            email = EmailMessage(
                'Welcome to Insportify!',
                render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': domain,
                    'uid': force_text(urlsafe_base64_encode(force_bytes(user.email))),
                    'token': account_activation_token.make_token(user),
                }),
                to=[form.cleaned_data.get('email')]
            )
            if is_localhost:
                print(email.body)
            else:

                email.send()
            messages.success(self.request,
                             'Account created! A verification email has been sent to your email address. Please confirm your email address to complete the registration.')
        return redirect('/users/mvp_register')


class organization_register(CreateView):
    model = User
    form_class = OrganizationSignUpForm
    template_name = 'registration/organization_register.html'

    def form_valid(self, form):
        localhost = '127.0.0.1:8000'
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            is_localhost = get_current_site(self.request).domain == localhost

            if is_localhost:
                ssl = 'http://'
            else:
                ssl = 'https://'
            domain = ''.join([ssl, get_current_site(self.request).domain])
            email = EmailMessage(
                'Welcome to Insportify!',
                render_to_string('acc_active_email.html', {
                    'user': user,
                    'domain': domain,
                    'uid': force_text(urlsafe_base64_encode(force_bytes(user.email))),
                    'token': account_activation_token.make_token(user),
                }),
                to=[form.cleaned_data.get('email')]
            )
            if is_localhost:
                print(email.body)
            else:

                email.send()
            messages.success(self.request,
                             'Account created! A verification email has been sent to your email address. Please confirm your email address to complete the registration.')
        return redirect('/users/organization_register')


def login_request(request):
    if request.method == 'POST':
        post = request.POST.copy()
        post['username'] = post['username'].lower()
        form = AuthenticationForm(data=post)
        if form.is_valid():
            username = form.cleaned_data.get('username').lower()
            password = form.cleaned_data.get('password')
            # print(username, password)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Invalid email or password")
        else:
            messages.error(request, "Invalid email or password")
    elif request.method == 'GET':
        if request.GET.get('next', ""):
            messages.info(
                request, "Please Log-in or Sign-up below to access this feature and more of INsportify!")
    return render(request, 'registration/login.html', context={'form': AuthenticationForm()})


def logout_view(request):
    logout(request)
    return redirect('/')


class password_reset(generic.CreateView):
    model = User
    form_class = PasswordResetAuthForm
    template_name = 'registration/password_reset.html'

    def form_valid(self, form):
        localhost = '127.0.0.1:8000'
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            is_localhost = get_current_site(self.request).domain == localhost
            if get_current_site(self.request).domain == localhost:
                ssl = 'http://'
            else:
                ssl = 'https://'
            domain = ''.join([ssl, get_current_site(self.request).domain])
            email = EmailMessage(
                'Password Reset Request from Insportify',
                render_to_string('acc_pass_reset_email.html', {
                    'user': user,
                    'domain': domain,
                    'uid': force_text(urlsafe_base64_encode(force_bytes(user.email))),
                    'token': pass_reset_code.make_token(user),
                }),
                to=[form.cleaned_data.get('email').lower()]
            )
            if is_localhost:
                print(email.body)
            else:
                email.send()
        # login(self.request, user)
        return redirect('/')


def password_reset_request(request):
    localhost = '127.0.0.1:8000'
    if request.method == "POST":
        post = request.POST.copy()
        post['email'] = post['email'].lower()
        password_reset_form = PasswordResetForm(post)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email'].lower()
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    is_localhost = get_current_site(request).domain == localhost
                    if get_current_site(request).domain == localhost:
                        ssl = 'http://'
                    else:
                        ssl = 'https://'
                    domain = ''.join([ssl, get_current_site(request).domain])
                    email = EmailMessage(
                        'Password Reset Request from Insportify',
                        render_to_string('acc_pass_reset_email.html', {
                            'user': user,
                            'domain': domain,
                            'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                            'token': default_token_generator.make_token(user),
                        }),
                        to=[password_reset_form.cleaned_data.get(
                            'email').lower()]
                    )
                    if is_localhost:
                        print(email.body)
                    else:
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
