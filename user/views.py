from django_htmx.http import HttpResponseClientRedirect

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse

from .models import NoteUser


# Create your views here.
def profile_view(request):
    '''
    Profile Page
    '''
    context = {}
    template_name = 'profile.html'

    if request.htmx:
        # update user profile
        data = request.POST
        user = request.user
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
                # email not used, can be saved for user
                user.email = data['email']

        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        user.save()

        messages.add_message(request, messages.SUCCESS,
                             'Profile updated!')

    return render(request, template_name, context)


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
