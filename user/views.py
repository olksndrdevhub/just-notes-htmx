from django_htmx.http import HttpResponseClientRedirect, reswap, trigger_client_event

from django.shortcuts import render, redirect
from django.contrib import messages
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse
from django.contrib.auth.password_validation import validate_password

from .models import NoteUser


# Create your views here.
def profile_view(request):
    '''
    Profile Page
    '''
    context = {}
    template_name = 'profile.html'

    # update user profile
    data = request.POST
    user = request.user

    # update password if needed
    if 'currentPassword' in request.POST:
        # check if currentPassword is valid
        if user and user.check_password(request.POST.get('currentPassword')):
            # check if new password matched with confirmation
            if request.POST.get('password') != request.POST.get('password2'):
                # return an error if not matched
                messages.add_message(request, messages.ERROR,
                                     "Passwords didn't match!")
                response = render(request, template_name, context)
                response = reswap(response, 'none')
                response = trigger_client_event(
                    response,
                    "passwordValidation",
                    {"result": "error",
                     "fieldsIds": ['password', 'password2']},
                    after='swap')
                return response
            try:
                # try to validate a password
                validate_password(request.POST.get('password'))
            except forms.ValidationError as errors:
                # return errors if password not valid
                for error in errors:
                    messages.add_message(request, messages.ERROR, f'Error: {error}')
                response = render(request, template_name, context)
                response = reswap(response, 'none')
                response = trigger_client_event(
                    response,
                    "passwordValidation",
                    {"result": "error",
                     "fieldsIds": ['password', 'password2']},
                    after='swap')
                return response
            # update password for user
            if user.is_dummy:
                messages.add_message(request, messages.WARNING,
                                     "You can't change password for dummy user!")
            else:
                user.set_password(request.POST.get('password'))
                # add success message
                messages.add_message(request, messages.SUCCESS, "Password changed!")
        else:
            # return error if currentPassword is not valid
            messages.add_message(request, messages.ERROR,
                                 "Invalid current password!")
            response = render(request, template_name, context)
            response = reswap(response, 'none')
            response = trigger_client_event(
                response,
                "passwordValidation",
                {"result": "error",
                 "fieldsIds": ['currentPassword']},
                after='swap'
            )
            return response

    if 'email' in data:
        try:
            # check if user with provided email exist
            match_user = NoteUser.objects.get(email=data['email'])
            # if user exist and are not the same user -> error
            # else if users are the same - we didn't need to update email
            if match_user and match_user.id is not user.id:
                messages.add_message(
                    request,
                    messages.ERROR,
                    f'Error: email {data["email"]} already used...'
                )
                return render(request, template_name, context)
        # if muptiple users finded with provided email -> eror
        except NoteUser.MultipleObjectsReturned:
            messages.add_message(
                request,
                messages.ERROR,
                f'Error: email {data["email"]} already used...'
            )
            return render(request, template_name, context)
        except NoteUser.DoesNotExist:
            if user.is_dummy:
                messages.add_message(request, messages.WARNING,
                                     "You can't change email for dummy user!")
            else:
                # email not used, can be saved for user
                user.email = data['email']

        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        user.save()
        messages.add_message(request, messages.SUCCESS,
                             'Profile updated!')

    response = render(request, template_name, context)
    response = trigger_client_event(
        response,
        "passwordValidation",
        {"result": "success"},
        after='swap'
    )
    return response


def logout_view(request):
    '''
    Just Log Out view
    '''
    logout(request)
    messages.add_message(request, messages.WARNING, 'You was log out!')
    return redirect('login_view')


def login_view(request):
    '''
    Log In Page
    '''
    context = {}
    template_name = 'login.html'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 'You successfully log in!')
            return HttpResponseClientRedirect('/')
        messages.add_message(request, messages.ERROR,
                             'Error! Wrong email or password...')
    return render(request, template_name, context)


def register_view(request):
    '''
    Register Page
    '''
    context = {}
    tempalte_name = 'register.html'
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if NoteUser.objects.filter(email=email).exists():
            messages.add_message(
                request,
                messages.ERROR,
                f"User with email {email} already exists!"
            )
        elif password != password2:
            messages.add_message(
                request,
                messages.ERROR,
                "Your password didn't match!"
            )
        else:
            user = NoteUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
            )
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                "Registration success! You can log in now!"
            )
            return HttpResponseClientRedirect('/account/login/')
        return HttpResponse('Response')
    return render(request, tempalte_name, context)


def hx_send_email_confirmation(request):
    if request.htmx:
        # TODO send an email
        print('send email confirmation')
    return HttpResponse('Success, check your email!')
