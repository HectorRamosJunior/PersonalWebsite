from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Score
from .forms import UserForm
import json

# Create your views here.
def index(request):
    return render(request, 'AggroEats/index.html')

# Creates a score object with the given post data
def create_score(request):
    if request.method == 'POST':
        score = Score()

        score.score = request.POST.get("score")
        score.user = request.user
        score.save()

        return HttpResponse(
                json.dumps(""),
                content_type="application/json"
            )
    else:
        return redirect("/AggroEats/")

# Returns the top 10 score objects' usernames and scores
def leaderboard(request):
    if request.method == 'POST':
        top_scores = Score.objects.all().order_by("-score")[:10]

        response_data = []

        # Makes 2d list of the scores and the scorers
        for score in top_scores:
            score_list = []
            score_list.append(score.user.username)
            score_list.append(score.score)

            response_data.append(score_list)

        return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )
    else:
        return redirect("/AggroEats/")

def user_register(request):
    registered = False
    error = None

    # They're making an account
    if request.method == 'POST':
        #Pull data for both forms from the forms.py file
        user_form = UserForm(data=request.POST)

        if user_form.is_valid(): #Safeguard against bad input
          user = user_form.save()
          user.set_password(user.password)
          user.save() 

          registered = True
        # If there was a form error, such as a username already taken
        else:
          error = user_form.errors
    # First time visiting page, present a clean Form
    else: 
        user_form = UserForm()

    context = {'user_form': user_form, 'registered': registered, 'error': error}

    return render(request, 'AggroEats/register.html', context)

def user_login(request):
    if request.method == 'POST': #Trying to login?
      username = request.POST.get('username') #Pulls the username field from the form
      password = request.POST.get('password') #POST.get returns 'none', not KeyError

      user = authenticate(username=username, password=password) #Legit login?

      if user: #if there's a account for the information provided
        if user.is_active: #Not BanHammered?
          login(request, user)
          return redirect('/AggroEats/')

      else: #Either acc or password is wrong
        error = "Account or Password provided was incorrect."
        return render(request, 'AggroEats/login.html', {'error': error})


    else: #GET, trying to login
        return render(request, 'AggroEats/login.html')

@login_required #make sure a user is logged on to use this
def user_logout(request):
    logout(request) #logs out the user

    return redirect('/AggroEats/') #Send em back to the index page