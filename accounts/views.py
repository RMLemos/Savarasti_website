from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from accounts.forms import LoginForm, RegisterForm, RegisterUpdateForm, UserProfile
from django.contrib.auth import authenticate, login, logout
from accounts.models import Profile
from django.contrib import messages

def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('accounts:login')


    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )


def login_view(request):

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            authenticated_user = authenticate(
                username=form.cleaned_data.get('username', ''),
                password=form.cleaned_data.get('password', ''),
            )

            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('authors:dashboard')
            else:
                messages.error(request, 'Invalid credentials')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html', {
        'form': form,
    })


def user_update(request):
    form = RegisterUpdateForm(instance=request.user)

    if request.method != 'POST':
        return render(
            request,
            'accounts/user_update.html',
            {
                'form': form
            }
        )

    form = RegisterUpdateForm(data=request.POST, instance=request.user)

    if not form.is_valid():
        return render(
            request,
            'accounts/user_update.html',
            {
                'form': form
            }
        )

    form.save()
    return redirect('library:index')


def profile_view(request):
    profile = get_object_or_404(Profile.objects.filter(reader=request.user))

    context={
            'profile': profile,
        }

    return render(request, 'accounts/prolie.html', context)


def edit_profile(request):
    profile, created = Profile.objects.get_or_create(reader=request.user)
    if request.method == 'POST':
        form = UserProfile(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('library:index')
    else:
        form = UserProfile(instance=profile)
    return render(
        request,
        'accounts/profile_update.html',
        {
            'form': form
        }
    )



