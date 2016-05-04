from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import TwotterProfile, Twoot
from .forms import UserForm, TwotterProfileForm, TwootForm, SettingsForm

import json


# Create your views here.
def index(request):
    if request.user.is_authenticated():
        # Creates a Twotter Profile if the current user came from another app
        create_profile_for_user(str(request.user.username))

        twotter_profile = User.objects.get(username=request.user.username).twotter_profile
    else:
        twotter_profile = None

    twoots = Twoot.objects.all().order_by('-creation_date')
    context = {'twotter_profile': twotter_profile, 'twoots': twoots}

    return render(request, 'twotter/index.html', context)


def twotter_profile(request, username):
    twotter_profile = get_object_or_404(User, username=username).twotter_profile
    twoots = twotter_profile.twoots.all().order_by('-creation_date')

    context = {'twotter_profile': twotter_profile, 'twoots': twoots}

    return render(request, 'twotter/profile.html', context)


@login_required
def profile_settings(request):
    twotter_profile = get_object_or_404(User, username=request.user.username).twotter_profile
    saved = False

    if request.method == "POST":
        if request.POST["button"] == "Settings":
            settings_form = SettingsForm(instance=twotter_profile, data=request.POST)

            if settings_form.is_valid():
                twotter_profile = settings_form.save()
                saved = True
    elif request.method == "GET":
        settings_form = SettingsForm(instance=twotter_profile)

    context = {'twotter_profile': twotter_profile, 'settings_form': settings_form, 'saved': saved}

    return render(request, 'twotter/settings.html', context)


@login_required
def make_twoot(request):
    if request.method == "POST":
        print "Twoot received: "
        print request.POST.get("twoot_text")
        twoot_form = TwootForm({"text": request.POST.get("twoot_text")})

        if twoot_form.is_valid():
            twotter_profile = request.user.twotter_profile
            twotter_profile.twoot_count += 1
            twotter_profile.save()

            twoot = twoot_form.save(commit=False)
            twoot.twotter_profile = twotter_profile
            twoot.save()

            response_data = {}
            response_data["pk"] = twoot.pk
            response_data["username"] = twotter_profile.user.username
            response_data["avatar_url"] = twotter_profile.avatar_url
            response_data["creation_date"] = twoot.creation_date.isoformat()
            response_data["display_name"] = twotter_profile.display_name
            response_data["text"] = twoot.text
            response_data["twoot_count"] = twotter_profile.twoot_count

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            print twoot_form.errors
    else:
        return redirect('/twotter/')


@login_required
def delete_twoot(request):
    if request.method == "POST":
        twoot = get_object_or_404(Twoot, pk=request.POST.get("twoot_pk"))

        if request.user == twoot.twotter_profile.user:
            twoot.twotter_profile.twoot_count -= 1
            twoot.delete()

            return HttpResponse(json.dumps(""), content_type="application/json")
        else:
            print "Someone tried to delete a twoot that wasn't theirs!"
    else:
        return redirect('/twotter/')


def user_login_or_register(request):
    # First time visining page, present login forms
    if request.method == "GET":
        user_form = UserForm()
        twotter_profile_form = TwotterProfileForm()
        context = {'user_form': user_form, 'twotter_profile_form': twotter_profile_form}

        return render(request, 'twotter/login.html', context)
    elif request.method == "POST":
        if request.POST["button"] == "Login":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user:
                if user.is_active:    # Verify user is not banned
                    login(request, user)
                    return redirect('/twotter/')
            else:
                error = "Account or Password provided was incorrect."
                context = {'user_form': UserForm(), 'twotter_profile_form': TwotterProfileForm(), 'error': error}

                return render(request, 'twotter/login.html', context)
        elif request.POST["button"] == "Register":
            registered = False
            error = None

            user_form = UserForm(data=request.POST)
            twotter_profile_form = TwotterProfileForm(data=request.POST)

            if user_form.is_valid() and twotter_profile_form.is_valid():
                user = user_form.save(commit=False)
                user.set_password(user.password)
                user.save()

                twotter_profile = twotter_profile_form.save(commit=False)
                twotter_profile.user = user
                if twotter_profile.avatar_url == "":
                    twotter_profile.avatar_url = "http://i.imgur.com/3iMO8An.png"
                if twotter_profile.background_url == "":
                    twotter_profile.background_url = ""
                twotter_profile.save()

                registered = True

                # Authenticate and login!
                new_user = authenticate(
                                            username=user_form.cleaned_data['username'],
                                            password=user_form.cleaned_data['password'],
                                        )
                login(request, new_user)
            # Handle form errors
            else:
                error = user_form.errors
                error.update(twotter_profile_form.errors)

            context = {'user_form': user_form, 'twotter_profile_form': twotter_profile_form,
                    'registered': registered, 'error': error}

            return render(request, 'twotter/login.html', context)


@login_required
def user_logout(request):
    logout(request)

    return redirect('twotter/')


def redirect_to_index(request):
    return redirect('/twotter/')

# Function that creates the profile for the user if they created an acc
# From another app on this project
def create_profile_for_user(username):
  try:
    user = User.objects.get(username=username)
  except:
    user = None

  try:
    profile = TwotterProfile.objects.get(user__username=username)
  except:
    profile = None

  # Handle if the user exists in the project but not in this app
  if user and not profile and username != "admin":
    profile = TwotterProfile()

    profile.user = User.objects.get(username=username)
    profile.display_name = username
    profile.avatar_url = "http://i.imgur.com/3iMO8An.png"

    profile.save()