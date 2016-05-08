from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import TwotterProfile, Twoot, Favorite, ReTwoot, Notification
from .forms import UserForm, TwotterProfileForm, TwootForm, SettingsForm

from itertools import chain

import json

# Renders the main index page, generates twoot feed from all users
def index(request):
    if request.user.is_authenticated():
        # Creates a Twotter Profile if the current user came from another app
        create_profile_for_user(str(request.user.username))

        twotter_profile = User.objects.get(username=request.user.username).twotter_profile
    else:
        twotter_profile = None

    twoots = Twoot.objects.all().order_by('-creation_date')
    retwoots = ReTwoot.objects.all().order_by('-creation_date')

    # Merge profile twoots and rewtwoots in order of creation_date. 
    twoots = sorted( chain(retwoots, twoots), key=lambda twoot: twoot.creation_date, reverse=True)

    index_twoots = []
    twoot_set = set()
    # Pass index_twoots in by tuple, first element containing retwoot creation date if it's a tuple
    # The second element in the tuple always contains the twoot itself. set used to not repeat twoots
    for twoot in twoots:
        if isinstance(twoot, Twoot) and not twoot in twoot_set:
            index_twoots.append( (None, twoot) )
            twoot_set.add(twoot)
        elif isinstance(twoot, ReTwoot) and not twoot.twoot in twoot_set:
            index_twoots.append( (twoot, twoot.twoot) )
            twoot_set.add(twoot.twoot)

    context = {'twotter_profile': twotter_profile, 'twoots': index_twoots}

    return render(request, 'twotter/index.html', context)

# Renders user profile pages, generates twoot feed from that user and their favorites
def twotter_profile(request, username):
    twotter_profile = get_object_or_404(User, username=username).twotter_profile
    twoots = twotter_profile.twoots.all().order_by('-creation_date')
    retwoots = twotter_profile.retwoots.all().order_by('-creation_date')
    favorites = twotter_profile.favorites.all().order_by('-creation_date')

    # Merge profile twoots and rewtwoots in order of creation_date. 
    twoots = sorted( chain(twoots, retwoots), key=lambda twoot: twoot.creation_date, reverse=True)

    profile_twoots = []
    twoot_set = set()
    # Pass profile_twoots in by tuple, first element containing retwoot creation date if it's a tuple
    # The second element in the tuple always contains the twoot itself. set used to not repeat twoots
    for twoot in twoots:
        if isinstance(twoot, Twoot) and not twoot in twoot_set:
            profile_twoots.append( (None, twoot) )
            twoot_set.add(twoot)
        elif isinstance(twoot, ReTwoot) and not twoot.twoot in twoot_set:
            profile_twoots.append( (twoot.creation_date, twoot.twoot) )
            twoot_set.add(twoot.twoot)

    # Pass favorites in by tuple, first element containing favorite creation date, second the twoot favorited
    favorite_twoots = []
    for favorite in favorites:
        favorite_twoots.append( (favorite.creation_date, favorite.twoot) )

    context = {'twotter_profile': twotter_profile, 'twoots': profile_twoots, 'favorites': favorite_twoots}

    return render(request, 'twotter/profile.html', context)

# Renders a page for a single given twoot, displays who retwooted and favorited on the twoot
def view_twoot(request, twoot_pk):
    twoot = get_object_or_404(Twoot, pk=twoot_pk)

    context = {'twoot': twoot}

    return render(request, 'twotter/twoot.html', context)

# Renders the page for changing a profile's settings, employs SettingsForm for validation
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

# Renders the page for changing a profile's notifications
@login_required
def profile_notifications(request):
    twotter_profile = get_object_or_404(User, username=request.user.username).twotter_profile
    notification_count = twotter_profile.notification_count

    new_notifications = twotter_profile.notifications.all().order_by('-creation_date')[:notification_count]
    old_notifications = twotter_profile.notifications.all().order_by('-creation_date')[notification_count:]

    twotter_profile.notification_count = 0
    twotter_profile.save()

    context = {'twotter_profile': twotter_profile, 'new_notifications': new_notifications, 
                'old_notifications': old_notifications}

    return render(request, 'twotter/notifications.html', context)

# Intended to be accessed via AJAX call. Creates twoot on valid POST request, returns a json object
# containing all the data needed to dynamically generate the twoot on the page
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

# Intended to be accessed via AJAX call. Deletes twoot on valid POST request, returns a json object
# which contains among others, a primary key of the twoot to be deleted dynamically from the page
@login_required
def delete_twoot(request):
    if request.method == "POST":
        twoot = get_object_or_404(Twoot, pk=request.POST.get("twoot_pk"))

        if request.user == twoot.twotter_profile.user or request.user.username == "admin":
            twotter_profile = twoot.twotter_profile
            twotter_profile.twoot_count -= 1
            twotter_profile.save()

            favorites = twoot.favorites.all()

            for favorite in favorites:
                profile_that_favorited = favorite.twotter_profile
                profile_that_favorited.favorite_count -= 1
                profile_that_favorited.save()

            retwoots = twoot.retwoots.all()

            for retwoot in retwoots:
                profile_that_retwooted = retwoot.twotter_profile
                profile_that_retwooted.retwoot_count -= 1
                profile_that_retwooted.save()

            twoot.delete()

            response_data = {}
            response_data["pk"] = request.POST.get("twoot_pk")
            response_data["twoot_count"] = twotter_profile.twoot_count
            response_data["username"] = request.user.username

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            print "Someone tried to delete a twoot that wasn't theirs!"
    else:
        return redirect('/twotter/')

# Intended to be accessed via AJAX call. Favorites twoot on valid POST request
@login_required
def favorite_twoot(request):
    if request.method == "POST":
        twoot = get_object_or_404(Twoot, pk=request.POST.get("twoot_pk"))
        favorite = twoot.favorites.filter(twotter_profile__user__username=request.user.username)

        user_twotter_profile = request.user.twotter_profile

        if not favorite:
            favorite = Favorite()
            favorite.twoot = twoot
            favorite.twotter_profile = user_twotter_profile
            favorite.save()

            notification = Notification()
            notification.twotter_profile = twoot.twotter_profile
            notification.notifier_profile = request.user.twotter_profile
            notification.twoot = twoot
            notification.action = "favorited"
            notification.save()

            twoot.favorite_count += 1
            twoot.save()

            notified_twotter_profile = twoot.twotter_profile
            # Do not allow users to notify themselves
            if not notified_twotter_profile is user_twotter_profile:
                notified_twotter_profile.notification_count += 1
                notified_twotter_profile.save()

            user_twotter_profile.favorite_count += 1
            user_twotter_profile.save()

            response_data = {"favorite_count": twoot.favorite_count}

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif favorite:
            favorite.delete()

            twoot.favorite_count -= 1
            twoot.save()

            user_twotter_profile.favorite_count -= 1
            user_twotter_profile.save()

            response_data = {"favorite_count": twoot.favorite_count}

            return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return redirect('/twotter/')

# Intended to be accessed via AJAX call. Retwoots twoot on valid POST request
@login_required
def retwoot_twoot(request):
    if request.method == "POST":
        twoot = get_object_or_404(Twoot, pk=request.POST.get("twoot_pk"))
        retwoot = twoot.retwoots.filter(twotter_profile__user__username=request.user.username)

        user_twotter_profile = request.user.twotter_profile
        notified_twotter_profile = twoot.twotter_profile

        if not retwoot:
            retwoot = ReTwoot()
            retwoot.twoot = twoot
            retwoot.twotter_profile = user_twotter_profile
            retwoot.save()

            notification = Notification()
            notification.twotter_profile = twoot.twotter_profile
            notification.notifier_profile = request.user.twotter_profile
            notification.twoot = twoot
            notification.action = "retwooted"
            notification.save()

            twoot.retwoot_count += 1
            twoot.save()

            notified_twotter_profile = twoot.twotter_profile
            # Do not allow users to notify themselves
            if not notified_twotter_profile is user_twotter_profile:
                notified_twotter_profile.notification_count += 1
                notified_twotter_profile.save()

            user_twotter_profile.retwoot_count += 1
            user_twotter_profile.save()

            response_data = {"retwoot_count": twoot.retwoot_count}

            return HttpResponse(json.dumps(response_data), content_type="application/json")
        elif retwoot:
            retwoot.delete()

            twoot.retwoot_count -= 1
            twoot.save()

            user_twotter_profile.retwoot_count -= 1
            user_twotter_profile.save()

            response_data = {"retwoot_count": twoot.retwoot_count}

            return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return redirect('/twotter/')

# Renders the page which handles both registration and login. On valid registration,
# a user is added to django auth users, and a twotter profile is created for that user.
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

# Logs out the current user and returns them back to the index page.
@login_required
def user_logout(request):
    logout(request)

    return redirect('twotter/')

# Redirects the user bcak to the index page if the url entered is not caught by any of the parsers
def redirect_to_index(request):
    return redirect('/twotter/')

# Creates twotter profile for django auth user if they created the user account from another app
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
  if user and not profile:
    profile = TwotterProfile()

    profile.user = User.objects.get(username=username)
    profile.display_name = username
    profile.avatar_url = "http://i.imgur.com/3iMO8An.png"

    profile.save()